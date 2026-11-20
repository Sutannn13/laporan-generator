import { useMemo, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Download,
  Eye,
  Layers,
  Maximize2,
  Search,
  X,
} from "lucide-react";
import { DIAGRAM_GALLERY, SHOWCASE_ITEMS } from "../data/siteContent";
import {
  ArrowIcon,
  ChargeInstallButton,
  Kicker,
  SplitHeading,
  useSlidingPill,
} from "./OverstoryVisuals";

const buildFilterOptions = (items) => {
  const countCat = (cat) => items.filter((it) => it.category === cat).length;
  const opts = [
    { id: "all", label: "Semua", count: items.length },
    { id: "pdf", label: "Pratinjau PDF", count: countCat("pdf") },
    { id: "pkl", label: "PKL OpenXML", count: countCat("pkl") },
    { id: "skripsi", label: "Skripsi TI", count: countCat("skripsi") },
    { id: "audit", label: "Laporan Audit", count: countCat("audit") },
    { id: "sinta", label: "Jurnal SINTA", count: countCat("sinta") },
  ];
  return opts.filter((o) => o.id === "all" || o.count > 0);
};

const FILTER_OPTIONS = buildFilterOptions(SHOWCASE_ITEMS);

// Real compiled companion sheets from website/public/thumbnails/ so every volume displays
// both its cover and an authentic interior spread on the exhibition light-table.
const COMPANION_SHEETS = {
  "pdf-pkl": {
    thumb: "thumbnails/pkl-outline4-uml.webp",
    primaryLabel: "Sampul A4 UBSI",
    companionLabel: "Halaman UML (Bab III)",
  },
  "docx-pkl": {
    thumb: "thumbnails/pkl-outline4-cover.webp",
    primaryLabel: "Halaman UML (Bab III)",
    companionLabel: "Sampul A4 UBSI",
  },
  "pdf-skripsi": {
    thumb: "thumbnails/skripsi-outline156-isi.webp",
    primaryLabel: "Sampul Skripsi UBSI",
    companionLabel: "Halaman Uji Ed25519 & QR",
  },
  "docx-skripsi": {
    thumb: "thumbnails/skripsi-outline156-cover.webp",
    primaryLabel: "Halaman Uji Ed25519 & QR",
    companionLabel: "Sampul Skripsi UBSI",
  },
  "pdf-jki": {
    thumb: "thumbnails/jki-phishing-hasil.webp",
    primaryLabel: "Halaman Pertama 2-Kolom",
    companionLabel: "Hasil & Confusion Matrix",
  },
  "docx-jki-2col": {
    thumb: "thumbnails/jki-phishing-p1.webp",
    primaryLabel: "Hasil & Confusion Matrix",
    companionLabel: "Halaman Pertama 2-Kolom",
  },
  "pdf-audit": {
    thumb: "thumbnails/audit-cobit-isi.webp",
    primaryLabel: "Sampul Audit TI COBIT",
    companionLabel: "Grafik Kapabilitas & Risiko",
  },
  "docx-audit": {
    thumb: "thumbnails/audit-cobit-cover.webp",
    primaryLabel: "Grafik Kapabilitas & Risiko",
    companionLabel: "Sampul Audit TI COBIT",
  },
};

export default function ShowcaseGallerySection({
  filter,
  onFilterChange,
  onPreviewPdf,
  onPreviewDiagram,
  onInstallClick,
}) {
  const [query, setQuery] = useState("");
  const [activeId, setActiveId] = useState(SHOWCASE_ITEMS[0]?.id || "");
  const [showingCompanion, setShowingCompanion] = useState(false);
  const [diagramsOpen, setDiagramsOpen] = useState(true);
  const segContainerRef = useRef(null);
  const segBtnRefs = useRef([]);
  const exhibitRef = useRef(null);
  const prefersReducedMotion = useReducedMotion();
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

  const activeIndex = useMemo(() => {
    if (!filteredItems.length) return -1;
    const found = filteredItems.findIndex((it) => it.id === activeId);
    return found >= 0 ? found : 0;
  }, [filteredItems, activeId]);

  const activeItem = activeIndex >= 0 ? filteredItems[activeIndex] : null;
  const activeCompanion = activeItem ? COMPANION_SHEETS[activeItem.id] : null;

  const handleReset = () => {
    onFilterChange("all");
    setQuery("");
    setShowingCompanion(false);
  };

  const handleOpenSpecimen = (item) => {
    if (!item) return;
    if (item.previewUrl) {
      onPreviewPdf(item);
      return;
    }
    onPreviewDiagram({
      src: item.thumb,
      title: item.title,
      tag: `${item.docType} · .${item.format.toUpperCase()}`,
      caption: `${item.outlineOrPreset} (${item.anonymizedLabel})`,
    });
  };

  const handleFilterSelect = (optId, idx) => {
    onFilterChange(optId);
    setShowingCompanion(false);
    segBtnRefs.current[idx]?.scrollIntoView({
      behavior: prefersReducedMotion ? "auto" : "smooth",
      block: "nearest",
      inline: "center",
    });
  };

  const selectSpecimen = (id, scrollToStage = false) => {
    setActiveId(id);
    setShowingCompanion(false);
    if (scrollToStage && exhibitRef.current) {
      const rect = exhibitRef.current.getBoundingClientRect();
      if (rect.top < 72 || rect.top > window.innerHeight * 0.65) {
        exhibitRef.current.scrollIntoView({
          behavior: prefersReducedMotion ? "auto" : "smooth",
          block: "start",
        });
      }
    }
  };

  const stepSpecimen = (delta) => {
    if (filteredItems.length <= 1) return;
    const nextIdx = (activeIndex + delta + filteredItems.length) % filteredItems.length;
    setActiveId(filteredItems[nextIdx].id);
    setShowingCompanion(false);
  };

  const isFiltering = filter !== "all" || query.trim().length > 0;
  const frontThumb =
    activeItem && showingCompanion && activeCompanion
      ? activeCompanion.thumb
      : activeItem?.thumb || "";
  const backThumb =
    activeItem && showingCompanion
      ? activeItem.thumb
      : activeCompanion?.thumb || "";
  const activeSheetLabel =
    showingCompanion && activeCompanion
      ? activeCompanion.companionLabel
      : activeCompanion?.primaryLabel || "Halaman Utama";

  return (
    <section
      id="hasil-output"
      className="ovs-work"
      data-sec="hasil-output"
      aria-labelledby="ovs-work-heading"
    >
      <div className="ovs-wrap">
        <div className="ovs-work-head">
          <Kicker n="03" text="Galeri Output Teranonimisasi (Opsi A)" />
          <SplitHeading
            id="ovs-work-heading"
            text="Sampel dokumen nyata dari halaman pertama hingga lampiran."
          />
          <p className="ovs-lede">
            Seluruh {SHOWCASE_ITEMS.length} dokumen (.pdf dan .docx) serta {DIAGRAM_GALLERY.length} diagram 300 DPI di bawah berasal dari hasil kompilasi asli tool ini yang telah dianonimisasi penuh.
          </p>
        </div>

        {/* Borderless Architectural Filter Rail + Baseline Search */}
        <div className="ovs-work-toolbar">
          <div className="ovs-seg-scroll">
            <div
              ref={segContainerRef}
              className="ovs-seg"
              role="group"
              aria-label="Filter kategori dokumen"
            >
              <span
                className="ovs-seg-underline"
                aria-hidden="true"
                style={{
                  width: `${segPillBox.w}px`,
                  opacity: segPillBox.ready ? 1 : 0,
                  transform: `translate3d(${segPillBox.x}px, 0, 0)`,
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
                  onClick={() => handleFilterSelect(opt.id, idx)}
                >
                  <span>{opt.label}</span>
                  <span className="ovs-seg-count">{opt.count}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="ovs-search-wrap">
            <Search size={15} className="ovs-search-ico" aria-hidden="true" />
            <label htmlFor="ovs-gallery-search" className="ovs-sr">
              Cari sampel preset atau jurnal
            </label>
            <input
              id="ovs-gallery-search"
              type="text"
              inputMode="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Cari Skripsi, PKL, JKI, SINTA 4..."
            />
            {query ? (
              <button
                type="button"
                className="ovs-search-clear"
                onClick={() => setQuery("")}
                aria-label="Hapus kata kunci pencarian"
              >
                <X size={14} aria-hidden="true" />
              </button>
            ) : null}
          </div>
        </div>

        {isFiltering ? (
          <div className="ovs-work-status">
            <p aria-live="polite">
              Menampilkan <strong>{filteredItems.length}</strong> dari {SHOWCASE_ITEMS.length} sampel dokumen
            </p>
            <button type="button" className="ovs-work-reset-link" onClick={handleReset}>
              Reset filter
            </button>
          </div>
        ) : null}

        {filteredItems.length === 0 || !activeItem ? (
          <motion.div
            initial={prefersReducedMotion ? false : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="ovs-empty-gallery"
          >
            <p>Tidak ditemukan sampel yang cocok dengan kata kunci pencarian tersebut.</p>
            <button type="button" className="ovs-btn ovs-btn-dark" onClick={handleReset}>
              <span>Tampilkan Semua {SHOWCASE_ITEMS.length} Sampel</span>
            </button>
          </motion.div>
        ) : (
          <>
            {/* Live Exhibition Light-Table: Monumental Dual-Sheet ISO A4 Spread + Open Colophon */}
            <div ref={exhibitRef} className="ovs-exhibit" data-wcard="">
              <div className="ovs-desk">
                <div className="ovs-spread-stage">
                  <div className="ovs-desk-marks" aria-hidden="true">
                    <span />
                    <span />
                    <span />
                    <span />
                  </div>
                  <AnimatePresence mode="wait" initial={false}>
                    <motion.div
                      key={`${activeItem.id}-${showingCompanion ? "back" : "front"}`}
                      className="ovs-spread"
                      initial={
                        prefersReducedMotion
                          ? { opacity: 0 }
                          : { opacity: 0, y: 12, scale: 0.985 }
                      }
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={
                        prefersReducedMotion
                          ? { opacity: 0 }
                          : { opacity: 0, y: -10, scale: 0.985 }
                      }
                      transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
                    >
                      {backThumb ? (
                        <button
                          type="button"
                          className="ovs-sheet-back"
                          onClick={() => setShowingCompanion((prev) => !prev)}
                          aria-label={
                            showingCompanion
                              ? `Tampilkan ${activeCompanion?.primaryLabel || "lembar utama"}`
                              : `Tampilkan ${activeCompanion?.companionLabel || "lembar isi"}`
                          }
                        >
                          <img
                            src={`${baseUrl}${backThumb}`}
                            alt={`Lembar pendamping A4: ${activeItem.title}`}
                          />
                        </button>
                      ) : null}

                      <button
                        type="button"
                        className="ovs-sheet-front"
                        onClick={() => handleOpenSpecimen(activeItem)}
                        aria-label={
                          activeItem.previewUrl
                            ? `Buka pratinjau PDF penuh: ${activeItem.title}`
                            : `Perbesar lembar A4: ${activeItem.title}`
                        }
                      >
                        <img
                          src={`${baseUrl}${frontThumb}`}
                          alt={`Lembar A4 teranonimisasi: ${activeItem.title}`}
                        />
                        <span className="ovs-sheet-cue" aria-hidden="true">
                          {activeItem.previewUrl ? <Eye size={14} /> : <Maximize2 size={14} />}
                          <span>{activeItem.previewUrl ? "Pratinjau Penuh" : "Perbesar"}</span>
                        </span>
                      </button>
                    </motion.div>
                  </AnimatePresence>
                </div>

                <div className="ovs-desk-foot">
                  <span className="ovs-desk-spec">
                    ISO A4 · 210 × 297 MM · {activeSheetLabel}
                  </span>
                  {activeCompanion ? (
                    <button
                      type="button"
                      className="ovs-sheet-flip"
                      onClick={() => setShowingCompanion((prev) => !prev)}
                    >
                      <Layers size={13} aria-hidden="true" />
                      <span>
                        {showingCompanion ? "Lihat Lembar Utama" : "Tukar ke Lembar Isi"}
                      </span>
                    </button>
                  ) : null}
                </div>
              </div>

              {/* Right Editorial Colophon (Borderless, Generous Type Hierarchy) */}
              <div className="ovs-colophon">
                <div className="ovs-colophon-top">
                  <div className="ovs-colophon-meta">
                    <span className="ovs-colophon-count">
                      {String(activeIndex + 1).padStart(2, "0")} /{" "}
                      {String(filteredItems.length).padStart(2, "0")}
                    </span>
                    <span className="ovs-colophon-cat">{activeItem.docType}</span>
                    <span className="ovs-colophon-fmt">.{activeItem.format}</span>
                  </div>

                  {filteredItems.length > 1 ? (
                    <div className="ovs-colophon-nav" aria-label="Navigasi spesimen">
                      <button
                        type="button"
                        className="ovs-step-btn"
                        onClick={() => stepSpecimen(-1)}
                        aria-label="Spesimen sebelumnya"
                      >
                        <ChevronLeft size={16} aria-hidden="true" />
                      </button>
                      <button
                        type="button"
                        className="ovs-step-btn"
                        onClick={() => stepSpecimen(1)}
                        aria-label="Spesimen berikutnya"
                      >
                        <ChevronRight size={16} aria-hidden="true" />
                      </button>
                    </div>
                  ) : null}
                </div>

                <AnimatePresence mode="wait" initial={false}>
                  <motion.div
                    key={activeItem.id}
                    className="ovs-colophon-content"
                    initial={prefersReducedMotion ? { opacity: 0 } : { opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={prefersReducedMotion ? { opacity: 0 } : { opacity: 0, y: -6 }}
                    transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
                  >
                    <p className="ovs-colophon-outline">{activeItem.outlineOrPreset}</p>
                    <h3 className="ovs-colophon-title">{activeItem.title}</h3>
                    <p className="ovs-colophon-summary">{activeItem.summary}</p>

                    <dl className="ovs-colophon-specs">
                      <div>
                        <dt>Volume</dt>
                        <dd>{activeItem.metricBig}</dd>
                      </div>
                      <div>
                        <dt>Tata Letak</dt>
                        <dd>{activeItem.layout}</dd>
                      </div>
                      <div>
                        <dt>Standar</dt>
                        <dd>{activeItem.citation}</dd>
                      </div>
                    </dl>

                    <div className="ovs-colophon-actions">
                      <button
                        type="button"
                        className="ovs-spec-primary"
                        onClick={() => handleOpenSpecimen(activeItem)}
                      >
                        {activeItem.previewUrl ? (
                          <Eye size={15} aria-hidden="true" />
                        ) : (
                          <Maximize2 size={15} aria-hidden="true" />
                        )}
                        <span>
                          {activeItem.previewUrl ? "Buka Pratinjau PDF" : "Perbesar Halaman"}
                        </span>
                      </button>

                      <a
                        href={`${baseUrl}${activeItem.downloadUrl}`}
                        download
                        className="ovs-spec-secondary"
                      >
                        <Download size={15} aria-hidden="true" />
                        <span>Unduh .{activeItem.format}</span>
                      </a>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>
            </div>

            {/* Borderless Architectural Specimen Catalogue Index (Zero Card Boxes) */}
            <div className="ovs-catalogue" aria-label="Indeks katalog spesimen dokumen">
              <div className="ovs-cat-head" aria-hidden="true">
                <span>No.</span>
                <span>Lembar</span>
                <span>Judul &amp; Skema Dokumen</span>
                <span>Kategori &amp; Volume</span>
                <span>Format</span>
                <span className="ovs-cat-head-end">Aksi</span>
              </div>

              <ol className="ovs-cat-list">
                {filteredItems.map((item, idx) => {
                  const isActive = item.id === activeItem.id;
                  const serialNo = String(idx + 1).padStart(2, "0");
                  const downloadHref = `${baseUrl}${item.downloadUrl}`;

                  return (
                    <li
                      key={item.id}
                      id={`showcase-${item.id}`}
                      className="ovs-cat-row"
                      data-active={isActive ? "" : undefined}
                    >
                      <button
                        type="button"
                        className="ovs-cat-select"
                        aria-current={isActive ? "true" : undefined}
                        onClick={() => selectSpecimen(item.id, true)}
                      >
                        <span className="ovs-cat-idx">{serialNo}</span>

                        <span className="ovs-cat-proof" aria-hidden="true">
                          <img src={`${baseUrl}${item.thumb}`} alt="" loading="lazy" />
                        </span>

                        <span className="ovs-cat-main">
                          <strong className="ovs-cat-title">{item.title}</strong>
                          <span className="ovs-cat-sub">{item.outlineOrPreset}</span>
                        </span>

                        <span className="ovs-cat-kind">
                          <span>{item.docType}</span>
                          <span className="ovs-cat-vol">{item.metricBig}</span>
                        </span>

                        <span className="ovs-cat-fmt">.{item.format}</span>
                      </button>

                      <div className="ovs-cat-actions">
                        <button
                          type="button"
                          className="ovs-cat-ico-btn"
                          onClick={() => handleOpenSpecimen(item)}
                          aria-label={`Pratinjau ${item.title}`}
                          title="Pratinjau dokumen"
                        >
                          <Eye size={15} aria-hidden="true" />
                        </button>
                        <a
                          href={downloadHref}
                          download
                          className="ovs-cat-ico-btn"
                          aria-label={`Unduh .${item.format} ${item.title}`}
                          title={`Unduh .${item.format}`}
                        >
                          <Download size={15} aria-hidden="true" />
                        </a>
                      </div>
                    </li>
                  );
                })}
              </ol>
            </div>

            {/* Borderless Closing Editorial Press Band (Zero Boxed CTA Card) */}
            <div className="ovs-press-band">
              <div className="ovs-press-copy">
                <p className="ovs-press-kicker">Eksekusi Lokal · Tanpa Cloud</p>
                <p className="ovs-press-title">
                  Kompilasi dokumen Anda berikutnya langsung di terminal lokal.
                </p>
              </div>
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
            </div>
          </>
        )}

        {/* 6 Technical Diagrams (300 DPI) - Seamless Architectural Contact Sheet */}
        <div id="galeri-diagram" className="ovs-diag-wrap">
          <div className="ovs-diag-head">
            <div>
              <h3 className="ovs-diag-h">
                Enam plat diagram 300 DPI hasil skrip lokal.
              </h3>
              <p className="ovs-lede ovs-diag-lede">
                Klik salah satu plat untuk memperbesar resolusi penuh di lightbox.
              </p>
            </div>

            <button
              type="button"
              className="ovs-diag-toggle"
              aria-expanded={diagramsOpen}
              aria-controls="ovs-diag-drawer"
              onClick={() => setDiagramsOpen((prev) => !prev)}
            >
              <span>
                {diagramsOpen
                  ? "Tutup Plat Diagram"
                  : `Buka Plat Diagram (${DIAGRAM_GALLERY.length})`}
              </span>
              <ChevronDown
                size={16}
                className="ovs-diag-chevron"
                data-open={diagramsOpen ? "" : undefined}
                aria-hidden="true"
              />
            </button>
          </div>

          <AnimatePresence initial={false}>
            {diagramsOpen ? (
              <motion.div
                id="ovs-diag-drawer"
                key="diagram-drawer"
                initial={prefersReducedMotion ? false : { height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={prefersReducedMotion ? { opacity: 0 } : { height: 0, opacity: 0 }}
                transition={{ duration: 0.36, ease: [0.22, 1, 0.36, 1] }}
                style={{ overflow: "hidden" }}
              >
                <div className="ovs-contact-sheet">
                  {DIAGRAM_GALLERY.map((dg, idx) => (
                    <button
                      key={dg.src}
                      type="button"
                      className="ovs-plate"
                      onClick={() =>
                        onPreviewDiagram({
                          ...dg,
                          galleryIndex: idx,
                          galleryList: DIAGRAM_GALLERY,
                        })
                      }
                    >
                      <div className="ovs-plate-stage">
                        <div className="ovs-plate-mat">
                          <img
                            src={`${baseUrl}${dg.src}`}
                            alt={dg.title}
                            loading="lazy"
                          />
                        </div>
                        <span className="ovs-diag-zoom" aria-hidden="true">
                          <Maximize2 size={13} />
                        </span>
                      </div>

                      <div className="ovs-plate-meta">
                        <div className="ovs-diag-meta-top">
                          <span className="ovs-diag-fig">Fig. 0{idx + 1}</span>
                          <span className="ovs-diag-tag">{dg.tag}</span>
                        </div>
                        <strong className="ovs-diag-title">{dg.title}</strong>
                        <span className="ovs-diag-cap">{dg.caption}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </motion.div>
            ) : null}
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}
