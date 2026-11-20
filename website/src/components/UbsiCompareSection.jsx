import { useRef, useState } from "react";
import { COMPARE_ROWS } from "../data/siteContent";
import { ArrowIcon, Kicker, useSlidingPill } from "./OverstoryVisuals";

export default function UbsiCompareSection() {
  const [activeIdx, setActiveIdx] = useState(0);
  const [slideDir, setSlideDir] = useState("next");
  const dotsContainerRef = useRef(null);
  const tabRefs = useRef([]);
  const current = COMPARE_ROWS[activeIdx] || COMPARE_ROWS[0];
  const pillBox = useSlidingPill(dotsContainerRef, tabRefs, activeIdx);

  const selectIndex = (nextIdx, explicitDir) => {
    if (nextIdx === activeIdx) return;
    setSlideDir(explicitDir || (nextIdx > activeIdx ? "next" : "prev"));
    setActiveIdx(nextIdx);
    tabRefs.current[nextIdx]?.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
      block: "nearest",
      inline: "center",
    });
  };

  const handlePrev = () => {
    const next = (activeIdx - 1 + COMPARE_ROWS.length) % COMPARE_ROWS.length;
    selectIndex(next, "prev");
  };

  const handleNext = () => {
    const next = (activeIdx + 1) % COMPARE_ROWS.length;
    selectIndex(next, "next");
  };

  const handleTabKeyDown = (idx, e) => {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    e.preventDefault();
    const isNext = e.key === "ArrowRight";
    const next = (idx + (isNext ? 1 : -1) + COMPARE_ROWS.length) % COMPARE_ROWS.length;
    selectIndex(next, isNext ? "next" : "prev");
    tabRefs.current[next]?.focus();
  };

  return (
    <section
      id="standar-ubsi"
      className="ovs-shade"
      data-sec="standar-ubsi"
      aria-labelledby="ovs-ubsi-heading"
    >
      <div className="ovs-dapple" aria-hidden="true">
        <i />
        <i />
        <i />
      </div>

      <div className="ovs-wrap ovs-quote-wrap">
        <Kicker
          n="05"
          text="Standar SK Rektor UBSI No. 165/2.01/UBSI/III/2026"
          light
        />

        <h2 id="ovs-ubsi-heading" className="ovs-sr">
          Ringkasan Kontras 7 Spesifikasi Pedoman UBSI 2026
        </h2>

        <div
          key={activeIdx}
          className="ovs-ubsi-stage"
          data-dir={slideDir}
          aria-live="polite"
        >
          <p className="ovs-ubsi-spotlight">{current.headline}</p>

          <div className="ovs-ubsi-contrast">
            <div className="ovs-ubsi-box">
              <span>Risiko Pengetikan Manual · {current.aspect}</span>
              <p>{current.manual}</p>
            </div>
            <div className="ovs-ubsi-box" data-engine="">
              <span>Implementasi Otomatis Engine · {current.aspect}</span>
              <p>{current.engine}</p>
            </div>
          </div>
        </div>

        <div className="ovs-quote-nav">
          <button
            type="button"
            className="ovs-round"
            aria-label="Spesifikasi sebelumnya"
            onClick={handlePrev}
          >
            <svg className="ovs-svg" viewBox="0 0 16 16" aria-hidden="true">
              <path
                d="M13 8H3m4-4L3 8l4 4"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>

          <div className="ovs-dots-scroll">
            <div
              ref={dotsContainerRef}
              className="ovs-dots"
              role="tablist"
              aria-label="Pilih spesifikasi pedoman UBSI"
            >
              <span
                className="ovs-sliding-pill ovs-sliding-pill-amber"
                aria-hidden="true"
                style={{
                  width: `${pillBox.w}px`,
                  height: `${pillBox.h}px`,
                  opacity: pillBox.ready ? 1 : 0,
                  transform: `translate3d(${pillBox.x}px, ${pillBox.y}px, 0)`,
                }}
              />
              {COMPARE_ROWS.map((row, idx) => (
                <button
                  key={row.shortTab}
                  ref={(el) => {
                    tabRefs.current[idx] = el;
                  }}
                  type="button"
                  role="tab"
                  tabIndex={idx === activeIdx ? 0 : -1}
                  aria-selected={idx === activeIdx}
                  aria-current={idx === activeIdx ? "true" : undefined}
                  onClick={() => selectIndex(idx)}
                  onKeyDown={(e) => handleTabKeyDown(idx, e)}
                >
                  {row.shortTab}
                </button>
              ))}
            </div>
          </div>

          <button
            type="button"
            className="ovs-round"
            aria-label="Spesifikasi berikutnya"
            onClick={handleNext}
          >
            <ArrowIcon />
          </button>
        </div>
      </div>
    </section>
  );
}
