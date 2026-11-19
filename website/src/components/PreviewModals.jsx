import { useEffect, useRef, useState } from "react";

function useModalLifecycle(isOpen, onClose, panelRef, closeBtnRef) {
  const prevFocusRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return undefined;
    prevFocusRef.current = document.activeElement;
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const focusTimer = window.setTimeout(() => {
      closeBtnRef.current?.focus();
    }, 25);

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

  useEffect(() => {
    if (item) setIframeLoaded(false);
  }, [item]);

  useModalLifecycle(Boolean(item), onClose, panelRef, closeBtnRef);

  if (!item) return null;
  const pdfHref = `${baseUrl}${item.previewUrl}`;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="pdf-modal-title"
      className="ovs-modal-backdrop"
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 80,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "16px",
        background: "rgba(14, 26, 16, 0.78)",
        backdropFilter: "blur(8px)",
      }}
    >
      <div
        ref={panelRef}
        className="ovs-modal-panel"
        onClick={(e) => e.stopPropagation()}
        style={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          maxWidth: "1040px",
          height: "88dvh",
          borderRadius: "28px",
          overflow: "hidden",
          background: "var(--ovs-card)",
          border: "1px solid var(--ovs-line)",
          boxShadow: "0 40px 90px -24px rgba(0, 0, 0, 0.55)",
        }}
      >
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "12px",
            padding: "16px 22px",
            borderBottom: "1px solid var(--ovs-line)",
            background: "var(--ovs-paper)",
          }}
        >
          <div style={{ minWidth: 0 }}>
            <h3
              id="pdf-modal-title"
              style={{
                fontSize: "17px",
                fontWeight: 600,
                letterSpacing: "-0.02em",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
            >
              {item.title}
            </h3>
            <p style={{ fontSize: "13px", color: "var(--ovs-ink2)" }}>
              Pratinjau PDF lokal · Sampel Teranonimisasi Opsi A
            </p>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
            <a
              href={pdfHref}
              target="_blank"
              rel="noreferrer"
              className="ovs-btn ovs-btn-line ovs-btn-sm"
            >
              <span>Tab Baru</span>
            </a>
            <a
              href={pdfHref}
              download
              className="ovs-btn ovs-btn-dark ovs-btn-sm"
            >
              <span>Unduh PDF</span>
            </a>
            <button
              ref={closeBtnRef}
              type="button"
              onClick={onClose}
              aria-label="Tutup pratinjau PDF"
              className="ovs-icon-btn"
              style={{ border: "1px solid var(--ovs-line)", background: "var(--ovs-card)" }}
            >
              <svg className="ovs-svg" viewBox="0 0 16 16" aria-hidden="true">
                <path
                  d="M4 4l8 8M12 4l-8 8"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.7"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          </div>
        </div>

        <div style={{ position: "relative", flex: 1, background: "var(--ovs-paper)" }}>
          {!iframeLoaded && (
            <div
              style={{
                position: "absolute",
                inset: 0,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: "10px",
                padding: "24px",
                textAlign: "center",
              }}
            >
              <p style={{ fontSize: "14px", color: "var(--ovs-ink2)" }}>
                Memuat dokumen PDF lokal ({item.title})...
              </p>
            </div>
          )}
          <iframe
            src={pdfHref}
            onLoad={() => setIframeLoaded(true)}
            title={`Pratinjau PDF ${item.title}`}
            style={{ position: "relative", zIndex: 2, width: "100%", height: "100%", border: 0 }}
          />
        </div>
      </div>
    </div>
  );
}

export function DiagramLightboxModal({ diagram, onClose }) {
  const baseUrl = import.meta.env.BASE_URL;
  const panelRef = useRef(null);
  const closeBtnRef = useRef(null);

  useModalLifecycle(Boolean(diagram), onClose, panelRef, closeBtnRef);

  if (!diagram) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="diagram-modal-title"
      className="ovs-modal-backdrop"
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 80,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "16px",
        background: "rgba(14, 26, 16, 0.8)",
        backdropFilter: "blur(8px)",
      }}
    >
      <div
        ref={panelRef}
        className="ovs-modal-panel"
        onClick={(e) => e.stopPropagation()}
        style={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          maxWidth: "1020px",
          maxHeight: "90dvh",
          borderRadius: "28px",
          overflow: "hidden",
          background: "var(--ovs-card)",
          border: "1px solid var(--ovs-line)",
          padding: "20px 24px 24px",
          boxShadow: "0 40px 90px -24px rgba(0, 0, 0, 0.55)",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "14px",
            paddingBottom: "14px",
          }}
        >
          <div>
            <h3
              id="diagram-modal-title"
              style={{ fontSize: "18px", fontWeight: 600, letterSpacing: "-0.02em" }}
            >
              {diagram.title}
            </h3>
            <p style={{ fontSize: "13.5px", color: "var(--ovs-ink2)" }}>{diagram.caption}</p>
          </div>
          <button
            ref={closeBtnRef}
            type="button"
            onClick={onClose}
            aria-label="Tutup pratinjau diagram"
            className="ovs-icon-btn"
            style={{ border: "1px solid var(--ovs-line)", background: "var(--ovs-paper)" }}
          >
            <svg className="ovs-svg" viewBox="0 0 16 16" aria-hidden="true">
              <path
                d="M4 4l8 8M12 4l-8 8"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.7"
                strokeLinecap="round"
              />
            </svg>
          </button>
        </div>

        <div
          style={{
            overflow: "auto",
            borderRadius: "18px",
            border: "1px solid var(--ovs-line)",
            background: "#ffffff",
            padding: "16px",
          }}
        >
          <img
            src={`${baseUrl}${diagram.src}`}
            alt={diagram.title}
            style={{
              display: "block",
              margin: "0 auto",
              maxHeight: "72dvh",
              width: "auto",
              objectFit: "contain",
            }}
          />
        </div>
      </div>
    </div>
  );
}
