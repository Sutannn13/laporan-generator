import { useEffect, useState } from "react";
import {
  NAV_LINKS,
  QUICK_INSTALL_CMD,
  REPO_URL,
  SKILL_ROWS,
  UPSTREAM_REPO_URL,
} from "../data/siteContent";
import { LockGlyph } from "./OverstoryVisuals";

function JakartaClock() {
  const [timeStr, setTimeStr] = useState("");

  useEffect(() => {
    let fmt;
    try {
      fmt = new Intl.DateTimeFormat("id-ID", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
        timeZone: "Asia/Jakarta",
      });
    } catch {
      fmt = new Intl.DateTimeFormat("id-ID", { hour: "2-digit", minute: "2-digit" });
    }
    const update = () => setTimeStr(`${fmt.format(new Date())} WIB`);
    update();
    const timer = window.setInterval(update, 15000);
    return () => window.clearInterval(timer);
  }, []);

  return <time>{timeStr || "--:-- WIB"}</time>;
}

const WORDMARK_TEXT = "TEMPLATEBSI";

export default function FooterSection({
  unlocked = false,
  onInstallClick,
  onNavigate,
  onSelectSkillRow,
}) {
  const [copied, setCopied] = useState(false);

  const handleCliAction = () => {
    if (!unlocked) {
      onInstallClick();
      return;
    }
    const done = () => {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2200);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(QUICK_INSTALL_CMD).then(done, done);
    } else {
      done();
    }
  };

  return (
    <footer className="ovs-foot">
      <div className="ovs-wrap">
        <div className="ovs-foot-top">
          <div>
            <p className="ovs-news-title">
              Pasang ke seluruh coding agent lokal dalam satu baris perintah.
            </p>
            <div className="ovs-news-row">
              <code
                className="ovs-news-code"
                style={
                  !unlocked
                    ? { filter: "blur(3.5px)", userSelect: "none", opacity: 0.55 }
                    : undefined
                }
                aria-hidden={!unlocked ? "true" : undefined}
              >
                {QUICK_INSTALL_CMD}
              </code>
              <button
                type="button"
                className="ovs-btn ovs-btn-lime ovs-btn-sm"
                onClick={handleCliAction}
              >
                {!unlocked ? <LockGlyph unlocked={false} size={13} /> : null}
                <span aria-live="polite">
                  {!unlocked ? "Buka Kunci CLI" : copied ? "Tersalin" : "Salin CLI"}
                </span>
              </button>
            </div>
            <p
              style={{
                marginTop: "12px",
                fontSize: "13px",
                lineHeight: 1.55,
                color: "rgba(237, 241, 230, 0.68)",
                maxWidth: "34em",
              }}
            >
              Repositori ini (
              <a
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: "var(--ovs-soft)", textDecoration: "underline", textUnderlineOffset: "3px" }}
              >
                Sutannn13/laporan-generator
              </a>
              ) adalah hasil pengembangan fork dari repositori rekan kami{" "}
              <a
                href={UPSTREAM_REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: "var(--ovs-soft)", textDecoration: "underline", textUnderlineOffset: "3px" }}
              >
                fatidaprilian/templatebsi
              </a>
              .
            </p>
          </div>

          <div className="ovs-foot-cols">
            <div>
              <p className="ovs-col-title">Navigasi</p>
              <ul>
                {NAV_LINKS.map((link) => (
                  <li key={link.href}>
                    <a href={link.href} onClick={onNavigate(link.href)}>
                      {link.label}
                    </a>
                  </li>
                ))}
                <li>
                  <a href="#standar-ubsi" onClick={onNavigate("#standar-ubsi")}>
                    Standar UBSI 2026
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <p className="ovs-col-title">Modul dalam 1 Skill</p>
              <ul>
                {SKILL_ROWS.slice(0, 4).map((skill, idx) => (
                  <li key={skill.id}>
                    <button
                      type="button"
                      className="ovs-foot-link"
                      onClick={() => onSelectSkillRow(idx)}
                    >
                      {skill.title}
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <p className="ovs-col-title">Repositori</p>
              <ul>
                <li className="ovs-clock">
                  <i aria-hidden="true" />
                  <JakartaClock />
                </li>
                <li>
                  <a href={REPO_URL} target="_blank" rel="noopener noreferrer">
                    GitHub Utama (Sutannn13)
                  </a>
                </li>
                <li>
                  <a href={UPSTREAM_REPO_URL} target="_blank" rel="noopener noreferrer">
                    Fork Asal (fatidaprilian)
                  </a>
                </li>
                <li>
                  <a href={`${REPO_URL}/blob/main/LICENSE`} target="_blank" rel="noopener noreferrer">
                    Lisensi MIT
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="ovs-wordmark" aria-hidden="true">
        {Array.from(WORDMARK_TEXT).map((ch, idx) => (
          <span key={idx}>{ch}</span>
        ))}
      </div>

      <div className="ovs-wrap ovs-foot-bottom">
        <span>© {new Date().getFullYear()} Laporan Generator UBSI · Lisensi MIT</span>
        <span>
          Fork dari{" "}
          <a
            href={UPSTREAM_REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "#edf1e6", textDecoration: "underline", textUnderlineOffset: "3px" }}
          >
            fatidaprilian/templatebsi
          </a>{" "}
          · Sampel Teranonimisasi (Opsi A)
        </span>
        <button
          type="button"
          className="ovs-top"
          onClick={onNavigate("#top")}
        >
          <span>Kembali ke atas</span>
          <svg className="ovs-svg" viewBox="0 0 16 16" aria-hidden="true">
            <path
              d="M8 13V3M4 7l4-4 4 4"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>
    </footer>
  );
}
