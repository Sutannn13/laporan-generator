import { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { NAV_LINKS } from "../data/siteContent";
import { LockGlyph, useSlidingPill } from "./OverstoryVisuals";

export default function Navbar({
  scheme,
  activeSection,
  unlocked,
  onToggleScheme,
  onInstallClick,
  onNavigate,
}) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [hoverNavIdx, setHoverNavIdx] = useState(-1);
  const burgerRef = useRef(null);
  const sheetRef = useRef(null);
  const linksContainerRef = useRef(null);
  const linkItemRefs = useRef([]);
  const baseUrl = import.meta.env.BASE_URL;

  const activeNavIdx = useMemo(
    () => NAV_LINKS.findIndex((l) => l.href.slice(1) === activeSection),
    [activeSection]
  );
  const pillTargetIdx = hoverNavIdx >= 0 ? hoverNavIdx : activeNavIdx;
  const pillBox = useSlidingPill(linksContainerRef, linkItemRefs, pillTargetIdx);

  useEffect(() => {
    if (!menuOpen) return undefined;
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const firstFocusable = sheetRef.current?.querySelector("a, button");
    firstFocusable?.focus();

    const onKeyDown = (e) => {
      if (e.key === "Escape") {
        setMenuOpen(false);
        burgerRef.current?.focus();
      }
      if (e.key === "Tab" && sheetRef.current) {
        const nodes = Array.from(sheetRef.current.querySelectorAll("a, button"));
        if (!nodes.length) return;
        if (e.shiftKey && document.activeElement === nodes[0]) {
          e.preventDefault();
          nodes[nodes.length - 1].focus();
        } else if (!e.shiftKey && document.activeElement === nodes[nodes.length - 1]) {
          e.preventDefault();
          nodes[0].focus();
        }
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.body.style.overflow = prevOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [menuOpen]);

  const handleLinkClick = (href) => (e) => {
    setMenuOpen(false);
    if (onNavigate) {
      onNavigate(href)(e);
    }
  };

  const handleInstall = (e) => {
    e.preventDefault();
    setMenuOpen(false);
    onInstallClick();
  };

  return (
    <>
      <header className="ovs-nav">
        <div className="ovs-nav-in">
          <a
            className="ovs-brand"
            href="#top"
            onClick={handleLinkClick("#top")}
          >
            <img
              src={`${baseUrl}diagrams/logo-ubsi.png`}
              alt="Logo UBSI"
              width="28"
              height="28"
              className="ovs-brand-logo"
            />
            <span>Laporan Generator UBSI</span>
          </a>

          <nav
            ref={linksContainerRef}
            className="ovs-links"
            aria-label="Navigasi utama"
            onPointerLeave={() => setHoverNavIdx(-1)}
          >
            <span
              className="ovs-sliding-pill ovs-sliding-pill-nav"
              aria-hidden="true"
              style={{
                width: `${pillBox.w}px`,
                height: `${pillBox.h}px`,
                opacity: pillBox.ready && pillTargetIdx >= 0 ? 1 : 0,
                transform: `translate3d(${pillBox.x}px, ${pillBox.y}px, 0)`,
              }}
            />
            {NAV_LINKS.map((link, idx) => {
              const secId = link.href.slice(1);
              return (
                <a
                  key={link.href}
                  ref={(el) => {
                    linkItemRefs.current[idx] = el;
                  }}
                  href={link.href}
                  onClick={handleLinkClick(link.href)}
                  onPointerEnter={() => setHoverNavIdx(idx)}
                  onFocus={() => setHoverNavIdx(idx)}
                  onBlur={() => setHoverNavIdx(-1)}
                  data-on={activeSection === secId ? "" : undefined}
                >
                  {link.label}
                </a>
              );
            })}
          </nav>

          <div className="ovs-nav-end">
            <button
              type="button"
              className="ovs-icon-btn"
              onClick={onToggleScheme}
              aria-label={scheme === "dark" ? "Beralih ke mode terang" : "Beralih ke mode gelap"}
            >
              <svg className="ovs-svg" viewBox="0 0 24 24" aria-hidden="true">
                {scheme === "dark" ? (
                  <g fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round">
                    <circle cx="12" cy="12" r="4.2" />
                    <path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6" />
                  </g>
                ) : (
                  <path
                    d="M20 14.6A8.4 8.4 0 0 1 9.4 4a8.4 8.4 0 1 0 10.6 10.6z"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.7"
                    strokeLinejoin="round"
                  />
                )}
              </svg>
            </button>

            <a
              href="#pasang-skill"
              onClick={handleInstall}
              className="ovs-btn ovs-nav-cta"
            >
              {!unlocked && <LockGlyph unlocked={false} size={14} />}
              <span>Install Skill</span>
            </a>

            <button
              ref={burgerRef}
              type="button"
              className="ovs-icon-btn ovs-burger"
              aria-expanded={menuOpen}
              aria-controls="ovs-mobile-sheet"
              aria-label={menuOpen ? "Tutup menu navigasi" : "Buka menu navigasi"}
              onClick={() => setMenuOpen((prev) => !prev)}
            >
              <span />
              <span />
            </button>
          </div>
        </div>
      </header>

      <AnimatePresence>
        {menuOpen ? (
          <motion.div
            key="mobile-sheet-backdrop"
            className="ovs-sheet-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.24, ease: [0.22, 1, 0.36, 1] }}
            onClick={() => setMenuOpen(false)}
          >
            <motion.div
              id="ovs-mobile-sheet"
              ref={sheetRef}
              className="ovs-sheet"
              role="dialog"
              aria-modal="true"
              aria-label="Menu navigasi seluler"
              initial={{ opacity: 0, y: -18, scale: 0.985 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -14, scale: 0.985 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              onClick={(e) => e.stopPropagation()}
            >
              <nav className="ovs-sheet-nav" aria-label="Tautan navigasi seluler">
                {NAV_LINKS.map((link, idx) => (
                  <motion.a
                    key={link.href}
                    href={link.href}
                    onClick={handleLinkClick(link.href)}
                    className="ovs-sheet-link"
                    data-on={activeSection === link.href.slice(1) ? "" : undefined}
                    initial={{ opacity: 0, x: -12 }}
                    animate={{
                      opacity: 1,
                      x: 0,
                      transition: {
                        duration: 0.26,
                        delay: 0.04 + idx * 0.03,
                        ease: [0.22, 1, 0.36, 1],
                      },
                    }}
                    exit={{
                      opacity: 0,
                      x: -6,
                      transition: { duration: 0.14, delay: 0 },
                    }}
                  >
                    <span>0{idx + 1}</span>
                    <b>{link.label}</b>
                  </motion.a>
                ))}
              </nav>

              <div className="ovs-sheet-foot">
                <a
                  href="#pasang-skill"
                  onClick={handleInstall}
                  className="ovs-btn ovs-btn-dark ovs-btn-xl ovs-sheet-cta"
                >
                  {!unlocked && <LockGlyph unlocked={false} size={15} />}
                  <span>Install Skill</span>
                </a>
                <button
                  type="button"
                  className="ovs-btn ovs-btn-line ovs-sheet-theme"
                  onClick={onToggleScheme}
                >
                  <span>{scheme === "dark" ? "Mode Terang" : "Mode Gelap"}</span>
                </button>
              </div>
            </motion.div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </>
  );
}
