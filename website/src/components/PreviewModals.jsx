import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { ChevronLeft, ChevronRight, Download, ExternalLink, Maximize2, Minimize2, X } from "lucide-react";

function useModalLifecycle(isOpen, onClose, panelRef, closeBtnRef) {
  const prevFocusRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return undefined;
    prevFocusRef.current = document.activeElement;
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const focusTimer = window.setTimeout(() => {
      closeBtnRef.current?.focus();
    }, 35);

    const onKey = (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        onClose();
        return;
      }
      if (e.key === "Tab" && panelRef.current) {
        const focusable = Array.from(
          panelRef.current.querySelectorAll("a[href], button:not([disabled]), iframe")
        );
        if (!focusable.length) return;
        if (e.shiftKey && document.activeElement === focusable[0]) {
          e.preventDefault();
          focusable[focusable.length - 1].focus();
        } else if (!e.shiftKey && document.activeElement === focusable[focusable.length - 1]) {
          e.preventDefault();
          focusable[0].focus();
        }
      }
    };

    document.addEventListener("keydown", onKey, true);
    return () => {
      window.clearTimeout(focusTimer);
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey, true);
      if (prevFocusRef.current && typeof prevFocusRef.current.focus === "function") {
        prevFocusRef.current.focus();
      }
    };
  }, [isOpen, onClose, panelRef, closeBtnRef]);
}

export function PdfPreviewModal({ item, onClose }) {
  const baseUrl = import.meta.env.BASE_URL;
  const panelRef = useRef(null);
  const closeBtnRef = useRef(null);
  const [iframeLoaded, setIframeLoaded] = useState(false);
  const prefersReducedMotion = useReducedMotion();

  useEffect(() => {
    if (item) setIframeLoaded(false);
  }, [item]);

  useModalLifecycle(Boolean(item), onClose, panelRef, closeBtnRef);

  const pdfHref = item ? `${baseUrl}${item.previewUrl}` : "";

  return (
    <AnimatePresence>
      {item ? (
        <motion.div
          key={`pdf-modal-${item.id}`}
          role="dialog"
          aria-modal="true"
          aria-labelledby="pdf-modal-title"
          className="ovs-modal-backdrop"
          onClick={onClose}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: prefersReducedMotion ? 0.08 : 0.22, ease: "easeOut" }}
        >
          <motion.div
            ref={panelRef}
            className="ovs-modal-panel ovs-modal-panel-pdf"
            onClick={(e) => e.stopPropagation()}
            initial={
              prefersReducedMotion
                ? { opacity: 0 }
                : { opacity: 0, y: 24, scale: 0.965 }
            }
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={
              prefersReducedMotion
                ? { opacity: 0 }
                : { opacity: 0, y: 18, scale: 0.97 }
            }
            transition={{
              duration: prefersReducedMotion ? 0.08 : 0.3,
              ease: [0.22, 1, 0.36, 1],
            }}
          >
            <div className="ovs-modal-head">
              <div className="ovs-modal-title-wrap">
                <h3 id="pdf-modal-title" className="ovs-modal-title">
                  {item.title}
                </h3>
                <p className="ovs-modal-sub">
                  Pratinjau PDF lokal · {item.outlineOrPreset} · Sampel Teranonimisasi Opsi A
                </p>
              </div>

              <div className="ovs-modal-actions">
                <a
                  href={pdfHref}
                  target="_blank"
                  rel="noreferrer"
                  className="ovs-btn ovs-btn-line ovs-btn-sm"
                >
                  <ExternalLink size={14} aria-hidden="true" />
                  <span>Tab Baru</span>
                </a>
                <a
                  href={pdfHref}
                  download
                  className="ovs-btn ovs-btn-dark ovs-btn-sm"
                >
                  <Download size={14} aria-hidden="true" />
                  <span>Unduh PDF</span>
                </a>
                <button
                  ref={closeBtnRef}
                  type="button"
                  onClick={onClose}
                  aria-label="Tutup pratinjau PDF"
                  className="ovs-icon-btn ovs-modal-close"
                >
                  <X size={18} aria-hidden="true" />
                </button>
              </div>
            </div>

            <div className="ovs-modal-pdf-body">
              {!iframeLoaded ? (
                <div className="ovs-modal-loading">
                  <span className="ovs-modal-spinner" aria-hidden="true" />
                  <p>Memuat dokumen PDF lokal ({item.title})...</p>
                </div>
              ) : null}
              <iframe
                src={pdfHref}
                onLoad={() => setIframeLoaded(true)}
                title={`Pratinjau PDF ${item.title}`}
                className="ovs-modal-iframe"
              />
            </div>

            <div className="ovs-modal-mobile-bar">
              <span>Tampilan PDF seluler terbatas?</span>
              <a
                href={pdfHref}
                target="_blank"
                rel="noreferrer"
                className="ovs-btn ovs-btn-dark ovs-btn-sm"
              >
                <ExternalLink size={14} aria-hidden="true" />
                <span>Buka PDF Penuh</span>
              </a>
            </div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}

export function DiagramLightboxModal({ diagram, onClose }) {
  const baseUrl = import.meta.env.BASE_URL;
  const panelRef = useRef(null);
  const closeBtnRef = useRef(null);
  const prefersReducedMotion = useReducedMotion();
  const [zoomed, setZoomed] = useState(false);
  const [activeIdx, setActiveIdx] = useState(0);

  const galleryList =
    diagram && Array.isArray(diagram.galleryList) && diagram.galleryList.length > 1
      ? diagram.galleryList
      : null;

  useEffect(() => {
    if (!diagram) return;
    setZoomed(false);
    setActiveIdx(typeof diagram.galleryIndex === "number" ? diagram.galleryIndex : 0);
  }, [diagram]);

  useModalLifecycle(Boolean(diagram), onClose, panelRef, closeBtnRef);

  const activeItem = galleryList ? galleryList[activeIdx] || diagram : diagram;

  useEffect(() => {
    if (!diagram || !galleryList) return undefined;
    const onArrow = (e) => {
      if (e.key === "ArrowRight") {
        e.preventDefault();
        setZoomed(false);
        setActiveIdx((prev) => (prev + 1) % galleryList.length);
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        setZoomed(false);
        setActiveIdx((prev) => (prev - 1 + galleryList.length) % galleryList.length);
      }
    };
    window.addEventListener("keydown", onArrow);
    return () => window.removeEventListener("keydown", onArrow);
  }, [diagram, galleryList]);

  const handleStep = (delta) => {
    if (!galleryList) return;
    setZoomed(false);
    setActiveIdx((prev) => (prev + delta + galleryList.length) % galleryList.length);
  };

  return (
    <AnimatePresence>
      {diagram && activeItem ? (
        <motion.div
          key="diagram-lightbox-backdrop"
          role="dialog"
          aria-modal="true"
          aria-labelledby="diagram-modal-title"
          className="ovs-modal-backdrop"
          onClick={onClose}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: prefersReducedMotion ? 0.08 : 0.22, ease: "easeOut" }}
        >
          <motion.div
            ref={panelRef}
            className="ovs-modal-panel ovs-modal-panel-img"
            onClick={(e) => e.stopPropagation()}
            initial={
              prefersReducedMotion
                ? { opacity: 0 }
                : { opacity: 0, y: 24, scale: 0.96 }
            }
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={
              prefersReducedMotion
                ? { opacity: 0 }
                : { opacity: 0, y: 18, scale: 0.965 }
            }
            transition={{
              duration: prefersReducedMotion ? 0.08 : 0.3,
              ease: [0.22, 1, 0.36, 1],
            }}
          >
            <div className="ovs-modal-head">
              <div className="ovs-modal-title-wrap">
                {activeItem.tag ? (
                  <span className="ovs-modal-tag">
                    {activeItem.tag}
                    {galleryList ? ` · ${activeIdx + 1} / ${galleryList.length}` : ""}
                  </span>
                ) : null}
                <h3 id="diagram-modal-title" className="ovs-modal-title">
                  {activeItem.title}
                </h3>
                <p className="ovs-modal-sub">{activeItem.caption}</p>
              </div>

              <div className="ovs-modal-actions">
                <button
                  type="button"
                  onClick={() => setZoomed((z) => !z)}
                  className="ovs-btn ovs-btn-line ovs-btn-sm"
                  aria-pressed={zoomed}
                >
                  {zoomed ? (
                    <Minimize2 size={14} aria-hidden="true" />
                  ) : (
                    <Maximize2 size={14} aria-hidden="true" />
                  )}
                  <span>{zoomed ? "Pas Layar" : "Perbesar"}</span>
                </button>
                <a
                  href={`${baseUrl}${activeItem.src}`}
                  download
                  className="ovs-btn ovs-btn-dark ovs-btn-sm"
                >
                  <Download size={14} aria-hidden="true" />
                  <span>Unduh PNG</span>
                </a>
                <button
                  ref={closeBtnRef}
                  type="button"
                  onClick={onClose}
                  aria-label="Tutup pratinjau gambar"
                  className="ovs-icon-btn ovs-modal-close"
                >
                  <X size={18} aria-hidden="true" />
                </button>
              </div>
            </div>

            <div className="ovs-modal-img-stage" data-zoomed={zoomed ? "" : undefined}>
              <AnimatePresence mode="wait" initial={false}>
                <motion.img
                  key={activeItem.src}
                  src={`${baseUrl}${activeItem.src}`}
                  alt={activeItem.title}
                  className="ovs-modal-img"
                  initial={prefersReducedMotion ? false : { opacity: 0, scale: 0.985 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={prefersReducedMotion ? { opacity: 0 } : { opacity: 0, scale: 0.985 }}
                  transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
                />
              </AnimatePresence>
            </div>

            {galleryList ? (
              <div className="ovs-modal-nav-bar">
                <button
                  type="button"
                  className="ovs-btn ovs-btn-line ovs-btn-sm"
                  onClick={() => handleStep(-1)}
                >
                  <ChevronLeft size={15} aria-hidden="true" />
                  <span>Sebelumnya</span>
                </button>
                <span className="ovs-modal-counter">
                  Diagram {activeIdx + 1} dari {galleryList.length}
                </span>
                <button
                  type="button"
                  className="ovs-btn ovs-btn-line ovs-btn-sm"
                  onClick={() => handleStep(1)}
                >
                  <span>Berikutnya</span>
                  <ChevronRight size={15} aria-hidden="true" />
                </button>
              </div>
            ) : null}
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
