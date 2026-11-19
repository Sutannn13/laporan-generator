import { useRef, useState } from "react";
import { PROCESS_STEPS } from "../data/siteContent";
import { AutumnGrowthTree, Kicker, LockGlyph, SplitHeading } from "./OverstoryVisuals";

export default function WorkflowInteractiveSection({ unlocked = false, onRequireUnlock }) {
  const svgRef = useRef(null);
  const [copiedCmd, setCopiedCmd] = useState("");

  const handleStepAction = (cmd) => {
    if (!unlocked) {
      if (onRequireUnlock) onRequireUnlock();
      return;
    }
    const done = () => {
      setCopiedCmd(cmd);
      window.setTimeout(() => setCopiedCmd(""), 1800);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(cmd).then(done, done);
    } else {
      done();
    }
  };

  return (
    <section
      id="alur-kerja"
      className="ovs-sec ovs-process"
      data-process=""
      data-sec="alur-kerja"
      aria-labelledby="ovs-proc-heading"
    >
      <div className="ovs-wrap">
        <Kicker n="04" text="Alur Kerja Tool & Mode Ilmiah" />
        <SplitHeading
          id="ovs-proc-heading"
          className="ovs-h2 ovs-h2-wide"
          text="Dari pemasangan skill hingga berkas .docx siap unggah dalam empat tahap."
        />

        <div className="ovs-proc-grid">
          <div className="ovs-tree-col">
            <div className="ovs-tree-stick">
              <AutumnGrowthTree svgRef={svgRef} />
            </div>
          </div>

          <ol className="ovs-steps">
            {PROCESS_STEPS.map((step, idx) => (
              <li
                key={step.name}
                className={`ovs-step${idx === 0 ? " ovs-on" : ""}`}
              >
                <p className="ovs-step-k">
                  <span>0{idx + 1}</span>
                  <b>{step.name}</b>
                  <em>{step.when}</em>
                </p>
                <h3>{step.title}</h3>
                <p className="ovs-step-desc">{step.text}</p>
                <button
                  type="button"
                  className="ovs-step-cmd"
                  data-locked={!unlocked ? "" : undefined}
                  onClick={() => handleStepAction(step.command)}
                  title={
                    unlocked
                      ? "Klik untuk menyalin perintah ini"
                      : "Beri bintang di GitHub untuk membuka salin perintah"
                  }
                >
                  {!unlocked ? <LockGlyph unlocked={false} size={13} /> : null}
                  <span aria-live="polite">
                    {!unlocked
                      ? `Buka kunci CLI (Star GitHub) · Tahap 0${idx + 1}`
                      : copiedCmd === step.command
                        ? "Perintah tersalin"
                        : step.command}
                  </span>
                </button>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </section>
  );
}
