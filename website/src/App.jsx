import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import EcosystemAndRules from "./components/EcosystemAndRules";
import ShowcaseGallerySection from "./components/ShowcaseGallerySection";
import WorkflowInteractiveSection from "./components/WorkflowInteractiveSection";
import UbsiCompareSection from "./components/UbsiCompareSection";
import InstallAndFaqSection from "./components/InstallAndFaqSection";
import FooterSection from "./components/FooterSection";
import { DiagramLightboxModal, PdfPreviewModal } from "./components/PreviewModals";
import { useStarGate } from "./components/useStarGate";
import WelcomeIntro from "./components/WelcomeIntro";

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export default function App() {
  const rootRef = useRef(null);
  const progressBarRef = useRef(null);
  const scrollEngineRef = useRef({
    targetY: 0,
    currentY: 0,
    active: false,
    tween: null,
    stopTicker: null,
  });

  const starGate = useStarGate();

  const [scheme, setScheme] = useState(() => {
    if (typeof document !== "undefined") {
      return document.documentElement.getAttribute("data-scheme") === "dark" ? "dark" : "light";
    }
    return "light";
  });
  const [activeSection, setActiveSection] = useState("top");
  const [openSkillIdx, setOpenSkillIdx] = useState(0);
  const [showcaseFilter, setShowcaseFilter] = useState("all");
  const [pdfModalItem, setPdfModalItem] = useState(null);
  const [diagramModalItem, setDiagramModalItem] = useState(null);
  const [introDone, setIntroDone] = useState(false);
  const heroTlRef = useRef(null);
  const heroRevealQueuedRef = useRef(false);

  const handleIntroRevealStart = useCallback(() => {
    heroRevealQueuedRef.current = true;
    heroTlRef.current?.play(0);
  }, []);

  const handleIntroComplete = useCallback(() => {
    setIntroDone(true);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute("data-scheme", scheme);
    try {
      localStorage.setItem("ubsi-theme", scheme);
    } catch {
      // Ignore private browsing storage restrictions
    }
  }, [scheme]);

  // Passive rAF scroll state for sticky pill navbar, scroll progress bar, & active section tracking
  useEffect(() => {
    const root = rootRef.current;
    if (!root) return undefined;

    let lastY = window.scrollY;
    let rafId = 0;

    const onScroll = () => {
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        const y = window.scrollY;
        const maxScroll = Math.max(
          1,
          document.documentElement.scrollHeight - window.innerHeight
        );
        const progress = Math.min(1, Math.max(0, y / maxScroll));
        if (progressBarRef.current) {
          progressBarRef.current.style.transform = `scaleX(${progress.toFixed(4)})`;
        }

        root.toggleAttribute("data-solid", y > 44);
        if (y > lastY + 6 && y > 440) {
          root.setAttribute("data-navhide", "");
        } else if (y < lastY - 6 || y <= 80) {
          root.removeAttribute("data-navhide");
        }
        lastY = y;
      });
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    const secObserver = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.getAttribute("data-sec") || "");
          }
        }
      },
      { rootMargin: "-42% 0px -48% 0px" }
    );
    root.querySelectorAll("[data-sec]").forEach((el) => secObserver.observe(el));

    return () => {
      window.removeEventListener("scroll", onScroll);
      cancelAnimationFrame(rafId);
      secObserver.disconnect();
    };
  }, []);

  // Inertial GSAP Mouse-Wheel Smoother (fine pointer + no reduced motion; yields natively to trackpads & modals)
  useEffect(() => {
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return undefined;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return undefined;

    const state = scrollEngineRef.current;

    const tickWheel = () => {
      const dt = Math.min(2.4, gsap.ticker.deltaRatio(60));
      const factor = 1 - Math.pow(1 - 0.14, dt);
      state.currentY += (state.targetY - state.currentY) * factor;

      if (Math.abs(state.targetY - state.currentY) < 0.45) {
        state.currentY = state.targetY;
        window.scrollTo({ top: state.currentY, left: 0, behavior: "instant" });
        state.active = false;
        gsap.ticker.remove(tickWheel);
        ScrollTrigger.update();
        return;
      }

      window.scrollTo({ top: state.currentY, left: 0, behavior: "instant" });
      ScrollTrigger.update();
    };

    const stopWheelTicker = () => {
      if (state.active) {
        state.active = false;
        gsap.ticker.remove(tickWheel);
      }
    };
    state.stopTicker = stopWheelTicker;

    const hasScrollableAncestor = (node) => {
      let cur = node instanceof Element ? node : null;
      while (cur && cur !== document.body && cur !== document.documentElement) {
        const st = window.getComputedStyle(cur);
        const oy = st.overflowY;
        if ((oy === "auto" || oy === "scroll") && cur.scrollHeight > cur.clientHeight + 2) {
          return true;
        }
        cur = cur.parentElement;
      }
      return false;
    };

    const onWheel = (e) => {
      if (e.defaultPrevented || e.ctrlKey || e.metaKey) return;
      if (document.body.style.overflow === "hidden") return;
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      if (hasScrollableAncestor(e.target)) return;

      // Let high-frequency small-delta trackpad gestures use native 120Hz OS momentum
      const isDiscreteMouseWheel = e.deltaMode === 1 || Math.abs(e.deltaY) >= 38;
      if (!isDiscreteMouseWheel) {
        stopWheelTicker();
        return;
      }

      e.preventDefault();
      if (state.tween) {
        state.tween.kill();
        state.tween = null;
      }

      const maxScroll = Math.max(
        0,
        document.documentElement.scrollHeight - window.innerHeight
      );
      if (!state.active) {
        state.currentY = window.scrollY;
        state.targetY = window.scrollY;
        state.active = true;
        gsap.ticker.add(tickWheel);
      }

      const rawStep = e.deltaMode === 1 ? e.deltaY * 38 : e.deltaY * 0.94;
      state.targetY = Math.max(0, Math.min(maxScroll, state.targetY + rawStep));
    };

    window.addEventListener("wheel", onWheel, { passive: false });
    return () => {
      window.removeEventListener("wheel", onWheel);
      stopWheelTicker();
      if (state.tween) {
        state.tween.kill();
        state.tween = null;
      }
    };
  }, []);

  // Overstory GSAP Motion Choreography (isolated inside gsap.matchMedia, auto-reverted on reduced motion)
  useLayoutEffect(() => {
    const root = rootRef.current;
    if (!root) return undefined;

    const ctx = gsap.context(() => {
      const mm = gsap.matchMedia();
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        const q = gsap.utils.selector(root);

        // 1. Subtle Hero entrance (synced to WelcomeIntro curtain lift) + canopy depth scrub
        const heroTl = gsap
          .timeline({ paused: true, defaults: { ease: "expo.out" } })
          .fromTo(
            q("[data-hero] .ovs-canopy"),
            { scale: 1.045 },
            { scale: 1, duration: 1.15, ease: "expo.out", clearProps: "scale" },
            0
          )
          .fromTo(
            q("[data-hero] [data-hline]"),
            { yPercent: 108, rotate: 1.8 },
            { yPercent: 0, rotate: 0, duration: 1.15, stagger: 0.09 },
            0.06
          )
          .fromTo(
            q("[data-hero] .ovs-hero-sub, [data-hero] .ovs-hero-actions"),
            { y: 16, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.85, stagger: 0.08 },
            0.24
          );
        heroTlRef.current = heroTl;
        if (heroRevealQueuedRef.current) {
          heroTl.play(0);
        }

        const heroCanopy = q("[data-hero] .ovs-canopy")[0];
        if (heroCanopy) {
          gsap.to(heroCanopy, {
            yPercent: 8,
            ease: "none",
            scrollTrigger: {
              trigger: q("[data-hero]")[0],
              start: "top top",
              end: "bottom top",
              scrub: 0.4,
            },
          });
        }

        // 2. Baseline-masked word reveal on Section H2s
        q("[data-split]").forEach((heading) => {
          const words = heading.querySelectorAll("[data-w]");
          if (!words.length) return;
          gsap.fromTo(
            words,
            { yPercent: 110, rotate: 2.2 },
            {
              yPercent: 0,
              rotate: 0,
              duration: 1.15,
              stagger: 0.038,
              ease: "expo.out",
              scrollTrigger: {
                trigger: heading,
                start: "top 92%",
                once: true,
              },
            }
          );
        });

        // 2b. Batched smooth ledger & diagram entrance (gallery specimen cards use Motion AnimatePresence)
        const batchTargets = q(".ovs-rule-cell, .ovs-diag-card");
        if (batchTargets.length) {
          gsap.set(batchTargets, { opacity: 0, y: 22 });
          ScrollTrigger.batch(batchTargets, {
            start: "top 92%",
            once: true,
            onEnter: (batch) => {
              gsap.to(batch, {
                opacity: 1,
                y: 0,
                duration: 0.8,
                stagger: 0.055,
                ease: "expo.out",
                overwrite: "auto",
                clearProps: "transform,opacity",
              });
            },
          });
        }

        // 3. Manifesto scrubbed word-opacity + inline badge pop + stat rule & integer count-up
        const manifesto = q("[data-manifesto]")[0];
        if (manifesto) {
          gsap.fromTo(
            manifesto.querySelectorAll("[data-mw]"),
            { opacity: 0.22 },
            {
              opacity: 1,
              stagger: 0.06,
              ease: "none",
              scrollTrigger: {
                trigger: manifesto,
                start: "top 84%",
                end: "bottom 52%",
                scrub: 0.4,
              },
            }
          );
          gsap.fromTo(
            manifesto.querySelectorAll(".ovs-pic"),
            { scale: 0.65, rotate: -8 },
            {
              scale: 1,
              rotate: 0,
              duration: 0.75,
              stagger: 0.14,
              ease: "back.out(2)",
              scrollTrigger: {
                trigger: manifesto,
                start: "top 80%",
                once: true,
              },
            }
          );
        }

        q(".ovs-stat-rule").forEach((rule) => {
          gsap.fromTo(
            rule,
            { scaleX: 0 },
            {
              scaleX: 1,
              duration: 1.2,
              ease: "expo.inOut",
              scrollTrigger: {
                trigger: rule,
                start: "top 92%",
                once: true,
              },
            }
          );
        });

        q("[data-count]").forEach((dd) => {
          const targetVal = Number(dd.getAttribute("data-count") || "0");
          if (targetVal <= 0) return;
          const proxy = { val: 0 };
          gsap.to(proxy, {
            val: targetVal,
            duration: 1.5,
            ease: "expo.out",
            scrollTrigger: {
              trigger: dd,
              start: "top 92%",
              once: true,
            },
            onUpdate: () => {
              dd.textContent = String(Math.round(proxy.val));
            },
          });
        });

        // 4. Process 4-Step Botanical Tree Growth (strokeDashoffset + leaf bloom)
        const proc = q("[data-process]")[0];
        if (proc) {
          const stepsWrap = proc.querySelector(".ovs-steps");
          const growPaths = proc.querySelectorAll("[data-grow]");

          if (stepsWrap && growPaths.length) {
            const trunk0 = proc.querySelectorAll('[data-grow="0"]');
            const otherPaths = proc.querySelectorAll('[data-grow="1"], [data-grow="2"]');
            const sprout0 = proc.querySelectorAll('[data-leaves="0"] > *');
            const upperLeaves = proc.querySelectorAll(
              '[data-leaves="1"] > *, [data-leaves="2"] > *, [data-leaves="3"] > *'
            );

            gsap.set(trunk0, { strokeDasharray: 1, strokeDashoffset: 0.72 });
            gsap.set(otherPaths, { strokeDasharray: 1, strokeDashoffset: 1 });
            gsap.set(sprout0, {
              scale: 1,
              transformBox: "fill-box",
              transformOrigin: "50% 50%",
            });
            gsap.set(upperLeaves, {
              scale: 0,
              transformBox: "fill-box",
              transformOrigin: "50% 50%",
            });

            const tl = gsap.timeline({
              scrollTrigger: {
                trigger: stepsWrap,
                start: "top 75%",
                end: "bottom 72%",
                scrub: 0.65,
              },
            });

            for (let s = 0; s < 4; s++) {
              const pNodes = proc.querySelectorAll(`[data-grow="${s}"]`);
              if (pNodes.length) {
                tl.to(pNodes, { strokeDashoffset: 0, duration: 1, ease: "none" }, s);
              }
              if (s > 0) {
                const lNodes = proc.querySelectorAll(`[data-leaves="${s}"] > *`);
                if (lNodes.length) {
                  tl.to(
                    lNodes,
                    {
                      scale: 1,
                      duration: 0.65,
                      stagger: s === 3 ? 0.012 : 0.1,
                      ease: "back.out(2)",
                    },
                    s + 0.35
                  );
                }
              }
            }

            const sun = proc.querySelector("[data-sun]");
            if (sun) {
              tl.fromTo(
                sun,
                { attr: { cy: 196 } },
                { attr: { cy: 74 }, duration: 4, ease: "none" },
                0
              );
            }
          }

          proc.querySelectorAll(".ovs-step").forEach((stepEl) => {
            ScrollTrigger.create({
              trigger: stepEl,
              start: "top 64%",
              end: "bottom 60%",
              toggleClass: { targets: stepEl, className: "ovs-on" },
            });
          });
        }

        // 5. Finale Canopy Window subtle inset expansion
        const fin = q("[data-fin]")[0];
        if (fin) {
          const win = fin.querySelector(".ovs-window");
          if (win) {
            gsap.fromTo(
              win,
              { "--ovs-wi": "4.5%", "--ovs-wr": "44px" },
              {
                "--ovs-wi": "0%",
                "--ovs-wr": "36px",
                ease: "power2.out",
                scrollTrigger: {
                  trigger: fin,
                  start: "top 86%",
                  end: "top 32%",
                  scrub: 0.55,
                },
              }
            );
          }
        }

        // 6. Monumental Footer Wordmark baseline entrance
        const wmSpans = q(".ovs-wordmark span");
        if (wmSpans.length) {
          gsap.fromTo(
            wmSpans,
            { yPercent: 95 },
            {
              yPercent: 0,
              duration: 1.25,
              stagger: 0.035,
              ease: "expo.out",
              scrollTrigger: {
                trigger: q(".ovs-wordmark")[0],
                start: "top 98%",
                once: true,
              },
            }
          );
        }
      });
    }, root);

    const refreshId = requestAnimationFrame(() => ScrollTrigger.refresh());
    return () => {
      cancelAnimationFrame(refreshId);
      ctx.revert();
    };
  }, []);

  // Refresh ScrollTrigger positions when gallery filter, accordion, or unlock state changes height
  useEffect(() => {
    const t = window.setTimeout(() => ScrollTrigger.refresh(), 550);
    return () => window.clearTimeout(t);
  }, [openSkillIdx, showcaseFilter, starGate.unlocked]);

  const toggleScheme = () => {
    setScheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  const smoothScrollToElement = useCallback((el, block = "start") => {
    if (!el) return;
    rootRef.current?.removeAttribute("data-navhide");

    const maxScroll = Math.max(
      0,
      document.documentElement.scrollHeight - window.innerHeight
    );
    const rect = el.getBoundingClientRect();
    let rawY = 0;
    if (el === rootRef.current) {
      rawY = 0;
    } else if (block === "center") {
      rawY = window.scrollY + rect.top - Math.max(88, (window.innerHeight - rect.height) * 0.34);
    } else {
      rawY = window.scrollY + rect.top - 78;
    }
    const destY = Math.max(0, Math.min(maxScroll, rawY));

    const state = scrollEngineRef.current;
    if (state.stopTicker) state.stopTicker();
    if (state.tween) {
      state.tween.kill();
      state.tween = null;
    }

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      state.currentY = destY;
      state.targetY = destY;
      window.scrollTo({ top: destY, left: 0, behavior: "instant" });
      return;
    }

    const proxy = { y: window.scrollY };
    const distance = Math.abs(destY - proxy.y);
    if (distance < 3) return;

    state.tween = gsap.to(proxy, {
      y: destY,
      duration: Math.min(1.12, Math.max(0.55, distance / 2400)),
      ease: "expo.inOut",
      onUpdate: () => {
        state.currentY = proxy.y;
        state.targetY = proxy.y;
        window.scrollTo({ top: proxy.y, left: 0, behavior: "instant" });
        ScrollTrigger.update();
      },
      onComplete: () => {
        state.tween = null;
        ScrollTrigger.refresh();
      },
    });
  }, []);

  const handleNavigate = useCallback(
    (href) => (e) => {
      if (!href || !href.startsWith("#")) return;
      const id = href.slice(1);
      const target = id === "top" ? rootRef.current : document.getElementById(id);
      if (!target) return;
      if (e) e.preventDefault();
      smoothScrollToElement(target, "start");
    },
    [smoothScrollToElement]
  );

  const handleInstallClick = useCallback(() => {
    setOpenSkillIdx(4);
    rootRef.current?.removeAttribute("data-navhide");
    // Wait briefly so accordion grid-template-rows starts expanding before measuring target Y
    window.setTimeout(() => {
      const el = document.getElementById("pasang-skill") || document.getElementById("skill");
      if (el) {
        smoothScrollToElement(el, "center");
      }
    }, 60);
  }, [smoothScrollToElement]);

  const handleSelectSkillRow = useCallback(
    (idx) => {
      setOpenSkillIdx(idx);
      rootRef.current?.removeAttribute("data-navhide");
      window.setTimeout(() => {
        const el = document.getElementById("skill");
        if (el) {
          smoothScrollToElement(el, "start");
        }
      }, 60);
    },
    [smoothScrollToElement]
  );

  return (
    <div ref={rootRef} className="ovs-root" data-scheme={scheme} data-season="autumn">
      {!introDone ? (
        <WelcomeIntro
          onRevealStart={handleIntroRevealStart}
          onComplete={handleIntroComplete}
        />
      ) : null}

      <div className="ovs-scroll-progress" aria-hidden="true">
        <i ref={progressBarRef} />
      </div>

      <a className="ovs-skip" href="#ovs-main">
        Langsung ke isi utama
      </a>

      <Navbar
        scheme={scheme}
        activeSection={activeSection}
        unlocked={starGate.unlocked}
        onToggleScheme={toggleScheme}
        onInstallClick={handleInstallClick}
        onNavigate={handleNavigate}
      />

      <main id="ovs-main" className="w-full max-w-full overflow-x-clip">
        <HeroSection
          scheme={scheme}
          onInstallClick={handleInstallClick}
          onNavigate={handleNavigate}
        />

        <EcosystemAndRules
          openSkillIdx={openSkillIdx}
          onToggleSkillIdx={setOpenSkillIdx}
          starGate={starGate}
        />

        <ShowcaseGallerySection
          filter={showcaseFilter}
          onFilterChange={setShowcaseFilter}
          onPreviewPdf={(item) => setPdfModalItem(item)}
          onPreviewDiagram={(dg) => setDiagramModalItem(dg)}
          onInstallClick={handleInstallClick}
        />

        <WorkflowInteractiveSection
          unlocked={starGate.unlocked}
          onRequireUnlock={handleInstallClick}
        />

        <UbsiCompareSection />

        <InstallAndFaqSection
          scheme={scheme}
          unlocked={starGate.unlocked}
          onInstallClick={handleInstallClick}
          onNavigate={handleNavigate}
        />
      </main>

      <FooterSection
        unlocked={starGate.unlocked}
        onInstallClick={handleInstallClick}
        onNavigate={handleNavigate}
        onSelectSkillRow={handleSelectSkillRow}
      />

      <PdfPreviewModal item={pdfModalItem} onClose={() => setPdfModalItem(null)} />
      <DiagramLightboxModal
        diagram={diagramModalItem}
        onClose={() => setDiagramModalItem(null)}
      />
    </div>
  );
}
