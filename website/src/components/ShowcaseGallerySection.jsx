import { useEffect, useMemo, useRef, useState } from "react";
import gsap from "gsap";
import { DIAGRAM_GALLERY, SHOWCASE_ITEMS } from "../data/siteContent";
import { ArrowIcon, Kicker, SplitHeading, useSlidingPill } from "./OverstoryVisuals";

const buildFilterOptions = (items) => {
  const countCat = (cat) => items.filter((it) => it.category === cat).length;
  const opts = [
    { id: "all", label: `Semua (${items.length})` },
    { id: "pdf", label: `Pratinjau PDF (${countCat("pdf")})` },
    { id: "pkl", label: `PKL OpenXML (${countCat("pkl")})` },
    { id: "skripsi", label: `Skripsi TI (${countCat("skripsi")})` },
    { id: "audit", label: `Laporan Audit (${countCat("audit")})` },
    { id: "sinta", label: `Jurnal SINTA (${countCat("sinta")})` },
  ];
  return opts.filter((o) => o.id === "all" || !o.label.endsWith("(0)"));
};

const FILTER_OPTIONS = buildFilterOptions(SHOWCASE_ITEMS);

export default function ShowcaseGallerySection({
  filter,
  onFilterChange,
  onPreviewPdf,
  onPreviewDiagram,
  onInstallClick,
}) {
  const [query, setQuery] = useState("");
  const segContainerRef = useRef(null);
  const segBtnRefs = useRef([]);
  const gridRef = useRef(null);
  const firstRenderRef = useRef(true);
  const baseUrl = import.meta.env.BASE_URL;

  const activeFilterIdx = useMemo(
    () => Math.max(0, FILTER_OPTIONS.findIndex((o) => o.id === filter)),
    [filter]
  );
  const segPillBox = useSlidingPill(segContainerRef, segBtnRefs, activeFilterIdx);

  const filteredItems = useMemo(() => {
    const q = query.trim().toLowerCase();
    return SHOWCASE_ITEMS.filter((item) => {
      const catMatch = filter === "all" || item.category === filter;
      if (!catMatch) return false;
      if (!q) return true;
      return (
        item.title.toLowerCase().includes(q) ||
        item.docType.toLowerCase().includes(q) ||
        item.outlineOrPreset.toLowerCase().includes(q) ||
        item.summary.toLowerCase().includes(q)
      );
    });
  }, [filter, query]);

  // Smooth staggered card transition whenever filter changes
  useEffect(() => {
    if (firstRenderRef.current) {
      firstRenderRef.current = false;
      return;
    }
    const grid = gridRef.current;
    if (!grid || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const cards = grid.querySelectorAll(".ovs-card");
    if (!cards.length) return;
    gsap.fromTo(
      cards,
      { opacity: 0, y: 18, scale: 0.985 },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.5,
        stagger: 0.035,
        ease: "expo.out",
        overwrite: true,
      }
    );
  }, [filter]);

  const handleReset = () => {
    onFilterChange("all");
    setQuery("");
  };

  const handleCardStageClick = (item) => {
    if (item.previewUrl) {
      onPreviewPdf(item);
      return;
    }
    onPreviewDiagram({
      src: item.thumb,
      title: item.title,
      caption: `${item.docType} · ${item.outlineOrPreset} (${item.anonymizedLabel})`,
    });
  };

  const nextCardFullSpan = filteredItems.length % 2 === 0;

  return (
    <section
      id="hasil-output"
      className="ovs-work"
      data-sec="hasil-output"
      aria-labelledby="ovs-work-heading"
    >
      <div className="ovs-wrap">
        <div className="ovs-work-head">
          <div>
            <Kicker n="03" text="Galeri Output Teranonimisasi (Opsi A)" />
            <SplitHeading
              id="ovs-work-heading"
              text="Sampel dokumen nyata dari halaman pertama hingga lampiran."
            />
          </div>
          <p className="ovs-lede">
            Seluruh {SHOWCASE_ITEMS.length} dokumen (.pdf dan .docx) serta {DIAGRAM_GALLERY.length} diagram 300 DPI di bawah berasal dari hasil kompilasi asli tool ini yang telah dianonimisasi penuh.
          </p>
        </div>

        <div className="ovs-work-toolbar">
          <div
            ref={segContainerRef}
            className="ovs-seg"
            role="group"
            aria-label="Filter kategori dokumen"
          >
            <span
              className="ovs-sliding-pill ovs-sliding-pill-ink"
              aria-hidden="true"
              style={{
                width: `${segPillBox.w}px`,
                height: `${segPillBox.h}px`,
                opacity: segPillBox.ready ? 1 : 0,
                transform: `translate3d(${segPillBox.x}px, ${segPillBox.y}px, 0)`,
              }}
            />
            {FILTER_OPTIONS.map((opt, idx) => (
              <button
                key={opt.id}
                ref={(el) => {
                  segBtnRefs.current[idx] = el;
                }}
                type="button"
                aria-pressed={filter === opt.id}
                onClick={() => onFilterChange(opt.id)}
              >
                {opt.label}
              </button>
            ))}
          </div>

          <div className="ovs-search-wrap">
            <svg
              className="ovs-svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              aria-hidden="true"
              style={{ opacity: 0.65 }}
            >
              <circle
                cx="11"
                cy="11"
                r="7"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
              />
              <path
                d="M20 20l-4.2-4.2"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
              />
            </svg>
            <label htmlFor="ovs-gallery-search" className="ovs-sr">
              Cari sampel preset atau jurnal
            </label>
            <input
              id="ovs-gallery-search"
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Cari Skripsi, PKL, JKI, SINTA 1..."
            />
          </div>
        </div>

        {filteredItems.length === 0 ? (
          <div
            className="ovs-faq-card"
            style={{ marginTop: 0, width: "100%", alignItems: "center", textAlign: "center" }}
          >
            <p>
              Tidak ditemukan sampel yang cocok dengan kata kunci pencarian tersebut.
            </p>
            <button type="button" className="ovs-btn ovs-btn-dark" onClick={handleReset}>
              <span>Tampilkan Semua {SHOWCASE_ITEMS.length} Sampel</span>
            </button>
          </div>
        ) : (
          <div ref={gridRef} className="ovs-work-grid">
            {filteredItems.map((item) => {
              const thumbSrc = `${baseUrl}${item.thumb}`;
              const downloadHref = `${baseUrl}${item.downloadUrl}`;
              return (
                <article
                  key={item.id}
                  id={`showcase-${item.id}`}
                  className="ovs-card"
                  data-wcard=""
                  style={{
                    "--t1": item.tint[0],
                    "--t2": item.tint[1],
                  }}
                >
                  <button
                    type="button"
                    className="ovs-card-art"
                    onClick={() => handleCardStageClick(item)}
                    aria-label={
                      item.previewUrl
                        ? `Buka pratinjau PDF ${item.title}`
                        : `Perbesar halaman pertama ${item.title}`
                    }
                  >
                    <span className="ovs-card-sun" aria-hidden="true" />
                    <div className="ovs-doc-frame">
                      <img
                        src={thumbSrc}
                        alt={`Halaman pertama teranonimisasi: ${item.title}`}
                        loading="lazy"
                      />
                    </div>
                    <span className="ovs-doc-peek" aria-hidden="true">
                      {item.previewUrl ? "Pratinjau PDF" : "Perbesar Halaman"}
                    </span>
                  </button>

                  <div className="ovs-card-meta">
                    <p className="ovs-card-client">
                      <strong>{item.docType}</strong>
                      <span>
                        {item.outlineOrPreset} · {item.anonymizedLabel}
                      </span>
                    </p>

                    <div className="ovs-card-body-left">
                      <h3 className="ovs-card-title">{item.title}</h3>
                      <p className="ovs-card-summary">{item.summary}</p>
                      <div className="ovs-card-actions">
                        {item.previewUrl ? (
                          <button
                            type="button"
                            className="ovs-btn ovs-btn-dark ovs-btn-sm"
                            onClick={() => onPreviewPdf(item)}
                          >
                            <span>Buka Pratinjau PDF</span>
                          </button>
                        ) : (
                          <button
                            type="button"
                            className="ovs-btn ovs-btn-line ovs-btn-sm"
                            onClick={() => handleCardStageClick(item)}
                          >
                            <span>Perbesar Halaman</span>
                          </button>
                        )}
                        <a
                          href={downloadHref}
                          download
                          className="ovs-btn ovs-btn-line ovs-btn-sm"
                        >
                          <span>Unduh .{item.format}</span>
                        </a>
                      </div>
                    </div>

                    <p className="ovs-card-metric">
                      <b>{item.metricBig}</b>
                      <span>
                        {item.layout} · {item.citation}
                      </span>
                    </p>
                  </div>
                </article>
              );
            })}

            <article
              className="ovs-card ovs-card-next"
              data-span={nextCardFullSpan ? "full" : undefined}
            >
              <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                <span className="ovs-kicker-n" style={{ color: "#10150d", fontWeight: 600 }}>
                  ( Siap Dipakai Lokal )
                </span>
                <p className="ovs-card-next-t">
                  Buat dokumen Anda berikutnya langsung di IDE tanpa cloud.
                </p>
              </div>
              <a
                href="#pasang-skill"
                onClick={(e) => {
                  e.preventDefault();
                  onInstallClick();
                }}
                className="ovs-btn ovs-btn-dark ovs-btn-xl"
              >
                <span>Install Skill</span>
                <ArrowIcon />
              </a>
            </article>
          </div>
        )}

        {/* 6 Technical Diagrams (300 DPI) */}
        <div id="galeri-diagram" className="ovs-diag-wrap">
          <div className="ovs-work-head" style={{ marginBottom: "8px" }}>
            <div>
              <p className="ovs-kicker" style={{ marginBottom: "10px" }}>
                <span className="ovs-kicker-n">( 300 DPI )</span>
                <span>Lampiran Visual & Diagram Otomatis</span>
              </p>
              <h3
                style={{
                  fontSize: "clamp(24px, 2.8vw, 38px)",
                  letterSpacing: "-0.04em",
                  fontWeight: 500,
                  lineHeight: 1.1,
                }}
              >
                Enam diagram teknis hasil skrip generator lokal.
              </h3>
            </div>
            <p className="ovs-lede" style={{ fontSize: "15px" }}>
              Klik salah satu diagram untuk memperbesar resolusi penuh di jendela pratinjau.
            </p>
          </div>

          <div className="ovs-diag-grid">
            {DIAGRAM_GALLERY.map((dg) => (
              <button
                key={dg.src}
                type="button"
                className="ovs-diag-card"
                onClick={() => onPreviewDiagram(dg)}
              >
                <div className="ovs-diag-thumb">
                  <img
                    src={`${baseUrl}${dg.src}`}
                    alt={dg.title}
                    loading="lazy"
                  />
                </div>
                <div className="ovs-diag-meta">
                  <span className="ovs-diag-tag">{dg.tag}</span>
                  <strong style={{ fontSize: "16px", fontWeight: 500, letterSpacing: "-0.02em" }}>
                    {dg.title}
                  </strong>
                  <span style={{ fontSize: "13.5px", color: "var(--ovs-ink2)", lineHeight: 1.48 }}>
                    {dg.caption}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
