import { Fragment, useEffect, useMemo, useRef, useState } from "react";
import gsap from "gsap";
import {
  INSTALL_TABS,
  MANIFESTO_CONTENT,
  MANIFESTO_STATS,
  R1_R4_PRINCIPLES,
  REPO_URL,
  SKILL_ROWS,
  UPSTREAM_REPO_URL,
} from "../data/siteContent";
import {
  GitHubMark,
  Kicker,
  LockGlyph,
  ServicePreviewArt,
  SplitHeading,
  StarGlyph,
  useSlidingPill,
} from "./OverstoryVisuals";

function parseManifestoTokens(text) {
  return text
    .split(/\s+/)
    .filter(Boolean)
    .map((word) => {
      const m = word.match(/^\[(team|chart)\]$/);
      return m ? { pic: m[1], word: "" } : { pic: "", word };
    });
}

export default function EcosystemAndRules({
  openSkillIdx,
  onToggleSkillIdx,
  starGate,
}) {
  const [hoveredIdx, setHoveredIdx] = useState(0);
  const [cliTabIdx, setCliTabIdx] = useState(0);
  const [copiedId, setCopiedId] = useState("");
  const listRef = useRef(null);
  const prevRef = useRef(null);
  const showPrevRef = useRef(false);
  const cliTabsRef = useRef(null);
  const cliTabItemRefs = useRef([]);
  const cliBoxRef = useRef(null);

  const tokens = useMemo(() => parseManifestoTokens(MANIFESTO_CONTENT.text), []);
  const activeCliTab = INSTALL_TABS[cliTabIdx] || INSTALL_TABS[0];
  const cliPillBox = useSlidingPill(
    cliTabsRef,
    cliTabItemRefs,
    starGate.unlocked && openSkillIdx === 4 ? cliTabIdx : -1
  );

  // Animate unlock reveal when starGate.unlocked transitions to true
  useEffect(() => {
    if (!starGate.unlocked || !cliBoxRef.current) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    gsap.fromTo(
      cliBoxRef.current,
      { opacity: 0, y: 12, scale: 0.985 },
      { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "expo.out" }
    );
  }, [starGate.unlocked]);

  // Smooth GSAP quickTo floating preview card on collapsed accordion headers (fine pointer only)
  useEffect(() => {
    const listEl = listRef.current;
    const prevEl = prevRef.current;
    if (!listEl || !prevEl) return undefined;
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return undefined;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return undefined;

    gsap.set(prevEl, { autoAlpha: 0, scale: 0.86 });
    const xTo = gsap.quickTo(prevEl, "x", { duration: 0.5, ease: "power3.out" });
    const yTo = gsap.quickTo(prevEl, "y", { duration: 0.5, ease: "power3.out" });
    const rTo = gsap.quickTo(prevEl, "rotate", { duration: 0.65, ease: "power3.out" });
    let lastX = 0;

    const onMove = (e) => {
      const rect = listEl.getBoundingClientRect();
      const relX = e.clientX - rect.left;
      const clampedX = Math.min(Math.max(relX + 24, 16), Math.max(24, rect.width - 264));
      xTo(clampedX);
      yTo(e.clientY - rect.top - 84);
      const vel = Math.max(-7, Math.min(7, (relX - lastX) * 0.45));
      rTo(vel);
      lastX = relX;
    };

    const onLeave = () => {
      showPrevRef.current = false;
      gsap.to(prevEl, { autoAlpha: 0, scale: 0.86, duration: 0.3, ease: "power2.in" });
    };

    listEl.addEventListener("pointermove", onMove);
    listEl.addEventListener("pointerleave", onLeave);
    return () => {
      listEl.removeEventListener("pointermove", onMove);
      listEl.removeEventListener("pointerleave", onLeave);
    };
  }, []);

  const setFloatingVisible = (visible) => {
    const prevEl = prevRef.current;
    if (!prevEl) return;
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (showPrevRef.current === visible) return;
    showPrevRef.current = visible;
    gsap.to(prevEl, {
      autoAlpha: visible ? 1 : 0,
      scale: visible ? 1 : 0.86,
      duration: visible ? 0.42 : 0.28,
      ease: visible ? "expo.out" : "power2.in",
    });
  };

  const handleHeaderEnter = (idx) => {
    setHoveredIdx(idx);
    setFloatingVisible(openSkillIdx !== idx);
  };

  const handleCopyText = (id, text) => {
    const markDone = () => {
      setCopiedId(id);
      window.setTimeout(() => setCopiedId(""), 2000);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(markDone, markDone);
    } else {
      markDone();
    }
  };

  return (
    <>
      {/* ( 01 ) Manifesto + 4 Countable Repo Metrics + Machined 2x2 R1-R4 Ledger */}
      <section
        id="aturan-r1-r4"
        className="ovs-sec ovs-manifesto"
        data-sec="aturan-r1-r4"
        aria-label="Prinsip Inti dan Aturan Sakral R1-R4"
      >
        <div className="ovs-wrap">
          <Kicker n="01" text={MANIFESTO_CONTENT.kicker} />

          <p className="ovs-man" data-manifesto="">
            {tokens.map((tok, idx) =>
              tok.pic ? (
                <span
                  key={idx}
                  className={`ovs-pic ovs-pic-${tok.pic}`}
                  aria-hidden="true"
                >
                  {tok.pic === "team" ? (
                    <>
                      <i>
                        <b>R1</b>
                      </i>
                      <i>
                        <b>R2</b>
                      </i>
                      <i>
                        <b>R3</b>
                      </i>
                      <i>
                        <b>R4</b>
                      </i>
                    </>
                  ) : (
                    <svg className="ovs-svg" viewBox="0 0 80 40">
                      <path
                        d="M4 34 L20 26 L32 30 L48 16 L60 20 L76 6"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="3.2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                      <circle cx="76" cy="6" r="4" fill="currentColor" />
                    </svg>
                  )}
                </span>
              ) : (
                <Fragment key={idx}>
                  <span data-mw="">{tok.word}</span>{" "}
                </Fragment>
              )
            )}
          </p>

          <dl className="ovs-stats">
            {MANIFESTO_STATS.map((stat) => (
              <div key={stat.label} className="ovs-stat">
                <span className="ovs-stat-rule" aria-hidden="true" />
                <dd data-count={stat.value}>{stat.value}</dd>
                <dt>{stat.label}</dt>
              </div>
            ))}
          </dl>

          <div className="ovs-rules-ledger" aria-label="Empat Aturan Sakral Mendeley R1 sampai R4">
            {R1_R4_PRINCIPLES.map((rule) => (
              <article key={rule.code} className="ovs-rule-cell">
                <div className="ovs-rule-head">
                  <span className="ovs-rule-badge">Aturan {rule.code}</span>
                  <code className="ovs-rule-guard">{rule.guardTag}</code>
                </div>
                <h3 className="ovs-rule-title">{rule.title}</h3>
                <p className="ovs-rule-desc">{rule.detail}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* ( 02 ) 5 Horizontal Accordion Rows: 4 Skills + 1 Star-Gated CLI Studio */}
      <section
        id="skill"
        className="ovs-sec ovs-services"
        data-sec="skill"
        aria-labelledby="ovs-skill-heading"
      >
        <div className="ovs-wrap">
          <div className="ovs-head">
            <div>
              <Kicker n="02" text="Ekosistem Skill & Perintah" />
              <SplitHeading
                id="ovs-skill-heading"
                text="Empat skill terpadu dan satu baris perintah untuk seluruh format akademik."
              />
            </div>
            <p className="ovs-lede">
              Dipasang sekali ke coding agent lokal Anda. Setiap skill bekerja di atas berkas Word (.docx) dan Typst (.pdf) di komputer sendiri.
            </p>
          </div>

          <div ref={listRef} className="ovs-svc-list">
            <div ref={prevRef} className="ovs-svc-prev" aria-hidden="true">
              {SKILL_ROWS.map((row, idx) => (
                <div
                  key={row.id}
                  className="ovs-svc-art"
                  data-on={idx === hoveredIdx ? "" : undefined}
                >
                  <ServicePreviewArt art={row.art} />
                </div>
              ))}
            </div>

            {SKILL_ROWS.map((row, idx) => {
              const isOpen = openSkillIdx === idx;
              const rowMeta = row.isCliRow
                ? starGate.unlocked
                  ? "Terbuka · Salin 1-Klik"
                  : "Terkunci · Wajib Star GitHub"
                : row.meta;

              return (
                <div
                  key={row.id}
                  id={row.isCliRow ? "pasang-skill" : undefined}
                  className="ovs-svc-row"
                  data-open={isOpen ? "" : undefined}
                >
                  <h3
                    className="ovs-svc-h"
                    onPointerEnter={() => handleHeaderEnter(idx)}
                    onPointerLeave={() => setFloatingVisible(false)}
                  >
                    <button
                      type="button"
                      aria-expanded={isOpen}
                      aria-controls={`ovs-skill-panel-${row.id}`}
                      onClick={() => {
                        setFloatingVisible(false);
                        onToggleSkillIdx(isOpen ? -1 : idx);
                      }}
                      onFocus={() => handleHeaderEnter(idx)}
                    >
                      <span className="ovs-svc-n">0{idx + 1}</span>
                      <span className="ovs-svc-t">{row.title}</span>
                      <span className="ovs-svc-time">{rowMeta}</span>
                      <span className="ovs-plus" aria-hidden="true" />
                    </button>
                  </h3>

                  <div
                    id={`ovs-skill-panel-${row.id}`}
                    className="ovs-fold"
                    role="region"
                    aria-label={row.title}
                    onPointerEnter={() => setFloatingVisible(false)}
                  >
                    <div>
                      <div className="ovs-svc-body">
                        <p className="ovs-svc-desc">{row.description}</p>

                        {row.isCliRow ? (
                          starGate.unlocked ? (
                            <div ref={cliBoxRef} className="ovs-cli-box" data-unlocked="">
                              <div className="ovs-cli-top">
                                <div
                                  ref={cliTabsRef}
                                  className="ovs-cli-tabs"
                                  role="tablist"
                                  aria-label="Skenario perintah terminal"
                                >
                                  <span
                                    className="ovs-sliding-pill ovs-sliding-pill-amber"
                                    aria-hidden="true"
                                    style={{
                                      width: `${cliPillBox.w}px`,
                                      height: `${cliPillBox.h}px`,
                                      opacity: cliPillBox.ready ? 1 : 0,
                                      transform: `translate3d(${cliPillBox.x}px, ${cliPillBox.y}px, 0)`,
                                    }}
                                  />
                                  {INSTALL_TABS.map((tab, tIdx) => (
                                    <button
                                      key={tab.id}
                                      ref={(el) => {
                                        cliTabItemRefs.current[tIdx] = el;
                                      }}
                                      type="button"
                                      role="tab"
                                      aria-selected={cliTabIdx === tIdx}
                                      className="ovs-cli-tab"
                                      onClick={() => setCliTabIdx(tIdx)}
                                    >
                                      {tab.label}
                                    </button>
                                  ))}
                                </div>

                                <span className="ovs-unlocked-pill">
                                  <LockGlyph unlocked size={13} />
                                  <span>
                                    Terbuka
                                    {typeof starGate.starCount === "number"
                                      ? ` · ${starGate.starCount} Star`
                                      : ""}
                                  </span>
                                </span>
                              </div>

                              <div className="ovs-cli-cmd-row">
                                <code className="ovs-cli-cmd">
                                  <span className="ovs-cli-prompt" aria-hidden="true">
                                    &gt;
                                  </span>
                                  {activeCliTab.command}
                                </code>
                                <button
                                  type="button"
                                  className="ovs-btn ovs-btn-lime ovs-btn-sm"
                                  style={{ minWidth: "136px" }}
                                  onClick={() =>
                                    handleCopyText(activeCliTab.id, activeCliTab.command)
                                  }
                                >
                                  <span aria-live="polite">
                                    {copiedId === activeCliTab.id ? "Tersalin" : "Salin Perintah"}
                                  </span>
                                </button>
                              </div>

                              <p className="ovs-cli-hint">{activeCliTab.hint}</p>

                              <div className="ovs-fork-note">
                                <GitHubMark size={15} />
                                <span>
                                  Repositori utama:{" "}
                                  <a href={REPO_URL} target="_blank" rel="noopener noreferrer">
                                    Sutannn13/laporan-generator
                                  </a>{" "}
                                  (dikembangkan dari fork repositori rekan kami{" "}
                                  <a
                                    href={UPSTREAM_REPO_URL}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    fatidaprilian/templatebsi
                                  </a>
                                  ).
                                </span>
                              </div>
                            </div>
                          ) : (
                            <div className="ovs-star-vault" data-locked="">
                              <div className="ovs-star-vault-head">
                                <span className="ovs-star-repo-pill">
                                  <GitHubMark size={15} />
                                  <span>Sutannn13/laporan-generator</span>
                                </span>
                                <span className="ovs-star-badge">
                                  <StarGlyph filled size={14} />
                                  <span>
                                    {typeof starGate.starCount === "number"
                                      ? `${starGate.starCount} Bintang di GitHub`
                                      : "Memuat status GitHub"}
                                  </span>
                                </span>
                              </div>

                              <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                                <h4
                                  style={{
                                    fontSize: "clamp(19px, 1.8vw, 24px)",
                                    fontWeight: 500,
                                    letterSpacing: "-0.03em",
                                    lineHeight: 1.2,
                                  }}
                                >
                                  Beri bintang pada repositori untuk membuka akses instalasi skill.
                                </h4>
                                <p
                                  style={{
                                    fontSize: "14.5px",
                                    lineHeight: 1.55,
                                    color: "rgba(237, 241, 230, 0.78)",
                                    maxWidth: "46em",
                                  }}
                                >
                                  Untuk memasang dan menjalankan skill di dalam Laporan Generator UBSI, silakan kunjungi repositori GitHub proyek ini dan klik tombol Star di pojok kanan atas. Tidak perlu mengunggah bukti apa pun: panel perintah CLI akan terbuka otomatis begitu bintang terdeteksi.
                                </p>
                              </div>

                              <div className="ovs-star-redacted" aria-hidden="true">
                                <code>
                                  &gt; git clone https://github.com/Sutannn13/laporan-generator.git &amp;&amp; npm run agent:install
                                </code>
                                <span className="ovs-star-lock-tag">
                                  <LockGlyph unlocked={false} size={13} />
                                  <span>Terkunci</span>
                                </span>
                              </div>

                              <div className="ovs-star-actions">
                                <a
                                  href={REPO_URL}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  onClick={() => starGate.registerRepoVisit()}
                                  className="ovs-btn ovs-btn-lime"
                                >
                                  <StarGlyph filled={false} size={16} />
                                  <span>Buka GitHub &amp; Beri Bintang</span>
                                </a>

                                <button
                                  type="button"
                                  className="ovs-btn ovs-btn-glass"
                                  style={{
                                    background: "rgba(237, 241, 230, 0.1)",
                                    borderColor: "rgba(237, 241, 230, 0.24)",
                                    color: "#edf1e6",
                                  }}
                                  disabled={starGate.gatePhase === "checking"}
                                  onClick={() =>
                                    starGate.verifyStarsNow({
                                      allowExistingStar: starGate.gatePhase === "existing_confirm",
                                    })
                                  }
                                >
                                  <span>
                                    {starGate.gatePhase === "checking"
                                      ? "Memeriksa API..."
                                      : starGate.gatePhase === "existing_confirm"
                                        ? "Konfirmasi & Buka"
                                        : "Cek Status Bintang"}
                                  </span>
                                </button>
                              </div>

                              {starGate.statusMessage ? (
                                <p
                                  className="ovs-star-msg"
                                  data-phase={starGate.gatePhase}
                                  aria-live="polite"
                                >
                                  {starGate.statusMessage}
                                </p>
                              ) : null}

                              <div className="ovs-fork-note">
                                <GitHubMark size={15} />
                                <span>
                                  Proyek ini dikelola di{" "}
                                  <a href={REPO_URL} target="_blank" rel="noopener noreferrer">
                                    Sutannn13/laporan-generator
                                  </a>{" "}
                                  dan merupakan hasil pengembangan (fork) dari repositori rekan kami{" "}
                                  <a
                                    href={UPSTREAM_REPO_URL}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    fatidaprilian/templatebsi
                                  </a>
                                  .
                                </span>
                              </div>
                            </div>
                          )
                        ) : null}

                        <ul className="ovs-svc-tags">
                          {row.tags.map((tag) =>
                            row.isCliRow && tag.startsWith("/") ? (
                              <li key={tag} style={{ padding: 0, border: 0, background: "none" }}>
                                {starGate.unlocked ? (
                                  <button
                                    type="button"
                                    className="ovs-slash-chip"
                                    onClick={() => handleCopyText(tag, tag)}
                                    title={`Salin perintah ${tag}`}
                                  >
                                    <span>{copiedId === tag ? `${tag} tersalin` : tag}</span>
                                  </button>
                                ) : (
                                  <span
                                    className="ovs-slash-chip"
                                    style={{ opacity: 0.55, cursor: "not-allowed" }}
                                    title="Beri bintang di GitHub untuk mengaktifkan perintah"
                                  >
                                    <LockGlyph unlocked={false} size={12} />
                                    <span>{tag}</span>
                                  </span>
                                )}
                              </li>
                            ) : (
                              <li key={tag}>
                                {tag.endsWith(".py") || tag.startsWith("--") ? (
                                  <code className="ovs-code" style={{ fontSize: "12.5px" }}>
                                    {tag}
                                  </code>
                                ) : (
                                  tag
                                )}
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </>
  );
}
