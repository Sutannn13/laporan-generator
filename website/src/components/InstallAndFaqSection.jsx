import { useState } from "react";
import { FAQS, QUICK_INSTALL_CMD, REPO_URL, UPSTREAM_REPO_URL } from "../data/siteContent";
import {
  ArrowIcon,
  AutumnCanopy,
  ChargeInstallButton,
  Kicker,
  LockGlyph,
  SplitHeading,
} from "./OverstoryVisuals";

export default function InstallAndFaqSection({
  scheme,
  unlocked = false,
  onInstallClick,
  onNavigate,
}) {
  const [openFaqIdx, setOpenFaqIdx] = useState(0);
  const [copied, setCopied] = useState(false);

  const handleQuickAction = () => {
    if (!unlocked) {
      onInstallClick();
      return;
    }
    const markCopied = () => {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2200);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(QUICK_INSTALL_CMD).then(markCopied, markCopied);
    } else {
      markCopied();
    }
  };

  return (
    <>
      {/* ( 06 ) 2-Column Split FAQ */}
      <section
        id="faq"
        className="ovs-sec ovs-faq"
        data-sec="faq"
        aria-labelledby="ovs-faq-heading"
      >
        <div className="ovs-wrap ovs-faq-grid">
          <div>
            <Kicker n="06" text="Pertanyaan Umum" />
            <SplitHeading
              id="ovs-faq-heading"
              text="Hal teknis yang paling sering ditanyakan sebelum mulai."
            />

            <div className="ovs-faq-card">
              <p>
                {unlocked
                  ? "Akses CLI sudah terbuka. Salin perintah pemasangan satu langkah atau periksa kode sumbernya di GitHub."
                  : "Siap memasang keempat skill mandiri ke komputer lokal Anda? Beri bintang terlebih dahulu pada repositori GitHub kami untuk membuka perintah instalasi."}
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
                <button
                  type="button"
                  className="ovs-btn ovs-btn-dark"
                  onClick={handleQuickAction}
                >
                  {!unlocked ? <LockGlyph unlocked={false} size={14} /> : null}
                  <span aria-live="polite">
                    {!unlocked
                      ? "Buka Kunci CLI (Star GitHub)"
                      : copied
                        ? "Perintah Tersalin"
                        : "Salin npm run agent:install"}
                  </span>
                </button>
                <a
                  href={REPO_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="ovs-btn ovs-btn-line"
                >
                  <span>Buka GitHub</span>
                </a>
              </div>
              <p
                style={{
                  marginTop: "14px",
                  fontSize: "12.5px",
                  lineHeight: 1.5,
                  color: "var(--ovs-ink2)",
                }}
              >
                Repositori{" "}
                <a
                  href={REPO_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ textDecoration: "underline", textUnderlineOffset: "3px" }}
                >
                  Sutannn13/laporan-generator
                </a>{" "}
                merupakan fork pengembangan dari{" "}
                <a
                  href={UPSTREAM_REPO_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ textDecoration: "underline", textUnderlineOffset: "3px" }}
                >
                  fatidaprilian/templatebsi
                </a>
                .
              </p>
            </div>
          </div>

          <div className="ovs-acc">
            {FAQS.map((item, idx) => {
              const isOpen = openFaqIdx === idx;
              return (
                <div
                  key={item.q}
                  className="ovs-acc-item"
                  data-open={isOpen ? "" : undefined}
                >
                  <h3>
                    <button
                      type="button"
                      aria-expanded={isOpen}
                      aria-controls={`ovs-faq-ans-${idx}`}
                      onClick={() => setOpenFaqIdx(isOpen ? -1 : idx)}
                    >
                      <span>{item.q}</span>
                      <span className="ovs-plus" aria-hidden="true" />
                    </button>
                  </h3>

                  <div
                    id={`ovs-faq-ans-${idx}`}
                    className="ovs-fold"
                    role="region"
                    aria-label={item.q}
                  >
                    <div>
                      <p>{item.a}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Finale Canopy Window */}
      <section className="ovs-fin" data-fin="" aria-labelledby="ovs-fin-heading">
        <div className="ovs-window">
          <AutumnCanopy seed={54} scheme={scheme} lazy />

          <div className="ovs-fin-copy">
            <h2 id="ovs-fin-heading" className="ovs-fin-h">
              Siap menyusun laporan dan jurnal tanpa revisi format?
            </h2>
            <p>
              Pasang skill ke coding agent lokal Anda, jalankan audit bahasa baku UBSI, dan hasilkan berkas Word (.docx) yang tetap bersih bagi Mendeley.
            </p>
            <div className="ovs-fin-actions">
              <ChargeInstallButton
                href="#pasang-skill"
                onClick={(e) => {
                  if (e?.preventDefault) e.preventDefault();
                  onInstallClick();
                }}
                variant="dark"
                className="ovs-btn-xl"
              >
                <span>Install Skill</span>
                <ArrowIcon />
              </ChargeInstallButton>
              <a
                href="#hasil-output"
                onClick={onNavigate("#hasil-output")}
                className="ovs-btn ovs-btn-glass ovs-btn-xl"
              >
                <span>Lihat Hasil Output</span>
              </a>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
