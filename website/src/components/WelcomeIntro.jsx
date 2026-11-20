import { useCallback, useEffect, useRef } from "react";

const TOTAL_MS = 3000;
const SKIP_EXIT_MS = 380;

// Logical SVG coordinate space for the Stickman & Pull-Cord stage
const VB_W = 420;
const VB_H = 260;
const CENTER_X = 210;
const ACTOR_PULL_X = CENTER_X - 26; // Clean Alan-Becker side silhouette: arms reach diagonally right to brass ring
const GROUND_Y = 236;
const BAR_REST_Y = 76;
const BAR_PULLED_Y = 144;
const CORD_LEN = 34;

// Stickman anatomical bone lengths (heroic editorial animator proportions)
const TORSO_LEN = 34;
const NECK_LEN = 12;
const UPPER_ARM = 21;
const LOWER_ARM = 20;
const UPPER_LEG = 24;
const LOWER_LEG = 24;

const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, t0, t1) => clamp((t - t0) / (t1 - t0), 0, 1);

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const easeOutQuad = (t) => 1 - (1 - t) * (1 - t);
const easeInOutQuart = (t) =>
  t < 0.5 ? 8 * t * t * t * t : 1 - Math.pow(-2 * t + 2, 4) / 2;
const easeOutBack = (t) => {
  const c1 = 1.4;
  const c3 = c1 + 1;
  return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
};

// Exact 2-bone analytical Inverse Kinematics (hands/feet lock with zero joint detachment)
function solveIK2(sx, sy, tx, ty, l1, l2, bendSign) {
  const dx = tx - sx;
  const dy = ty - sy;
  const rawDist = Math.hypot(dx, dy) || 0.001;
  const maxReach = l1 + l2 - 0.15;
  const minReach = Math.abs(l1 - l2) + 0.15;
  const d = clamp(rawDist, minReach, maxReach);
  const base = Math.atan2(dy, dx);
  const cosA = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1);
  const angle = base + bendSign * Math.acos(cosA);
  const mx = sx + Math.cos(angle) * l1;
  const my = sy + Math.sin(angle) * l1;
  const ex = sx + (dx / rawDist) * d;
  const ey = sy + (dy / rawDist) * d;
  return { mx, my, ex, ey };
}

// Forward Kinematics 2-bone helper (angle in radians from +Y downward, positive = right)
function solveFK2(sx, sy, a1, a2, l1, l2) {
  const mx = sx + Math.sin(a1) * l1;
  const my = sy + Math.cos(a1) * l1;
  const ex = mx + Math.sin(a1 + a2) * l2;
  const ey = my + Math.cos(a1 + a2) * l2;
  return { mx, my, ex, ey };
}

function limbPath(sx, sy, mx, my, ex, ey) {
  return `M${sx.toFixed(1)} ${sy.toFixed(1)} Q${mx.toFixed(1)} ${my.toFixed(1)} ${ex.toFixed(1)} ${ey.toFixed(1)}`;
}

export default function WelcomeIntro({ onRevealStart, onComplete }) {
  const rootRef = useRef(null);
  const curtainRef = useRef(null);
  const floorRef = useRef(null);
  const svgRef = useRef(null);
  const skipBtnRef = useRef(null);

  // Direct SVG element refs for 60-120fps zero-rerender skeletal animation
  const rigRefs = useRef({
    shadow: null,
    cord: null,
    ring: null,
    spark: null,
    scarf: null,
    torso: null,
    head: null,
    legL: null,
    legR: null,
    armL: null,
    armR: null,
    actorGroup: null,
  });

  const rafRef = useRef(0);
  const finishedRef = useRef(false);
  const revealFiredRef = useRef(false);
  const skipStateRef = useRef({ active: false, startAt: 0, startCurtainY: 0 });
  const baseUrl = import.meta.env.BASE_URL;

  const fireReveal = useCallback(() => {
    if (revealFiredRef.current) return;
    revealFiredRef.current = true;
    onRevealStart?.();
  }, [onRevealStart]);

  const finishIntro = useCallback(() => {
    if (finishedRef.current) return;
    finishedRef.current = true;
    if (rafRef.current) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = 0;
    }
    fireReveal();
    onComplete?.();
  }, [fireReveal, onComplete]);

  const handleSkip = useCallback(() => {
    if (finishedRef.current || skipStateRef.current.active) return;
    fireReveal();
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      finishIntro();
      return;
    }
    const curtainEl = curtainRef.current;
    let currentY = -120;
    if (curtainEl) {
      const m = curtainEl.style.transform.match(/translate3d\([^,]+,\s*([-\d.]+)px/);
      if (m) currentY = parseFloat(m[1]);
    }
    skipStateRef.current = {
      active: true,
      startAt: performance.now(),
      startCurtainY: currentY,
    };
  }, [fireReveal, finishIntro]);

  // Lock page scroll during the 3s intro and allow Escape to skip
  useEffect(() => {
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        handleSkip();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = prevOverflow;
      window.removeEventListener("keydown", onKey);
    };
  }, [handleSkip]);

  // 60fps Unified Skeletal Stickman + Cinema Roller Curtain Engine (3.00s exact)
  useEffect(() => {
    const rootEl = rootRef.current;
    const curtainEl = curtainRef.current;
    const floorEl = floorRef.current;
    const svgEl = svgRef.current;
    if (!rootEl || !curtainEl || !floorEl || !svgEl) return undefined;

    // Gentle reduced-motion crossfade alternative (respects prefers-reduced-motion)
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      fireReveal();
      curtainEl.style.transform = "translate3d(0, 0, 0)";
      const t1 = window.setTimeout(() => {
        rootEl.style.transition = "opacity 0.42s ease";
        rootEl.style.opacity = "0";
      }, 180);
      const t2 = window.setTimeout(finishIntro, 640);
      return () => {
        window.clearTimeout(t1);
        window.clearTimeout(t2);
      };
    }

    const startTime = performance.now();
    // Persistent secondary-motion state for the warm amber scarf
    let prevNeckX = 48;
    let prevNeckY = 160;
    let scarfLagX = -16;
    let scarfLagY = 4;

    const renderFrame = (now) => {
      if (finishedRef.current) return;

      const vh = rootEl.clientHeight || window.innerHeight || 800;
      const svgH = svgEl.clientHeight || 260;
      const scale = svgH / VB_H;

      // Fast skip exit path
      if (skipStateRef.current.active) {
        const st = clamp((now - skipStateRef.current.startAt) / SKIP_EXIT_MS, 0, 1);
        const eased = easeInOutCubic(st);
        const targetUpY = -(vh + 64);
        const cy = lerp(skipStateRef.current.startCurtainY, targetUpY, eased);
        curtainEl.style.transform = `translate3d(0, ${cy.toFixed(1)}px, 0)`;
        floorEl.style.opacity = (1 - eased).toFixed(3);
        if (rigRefs.current.actorGroup) {
          rigRefs.current.actorGroup.style.opacity = (1 - eased).toFixed(3);
        }
        if (skipBtnRef.current) {
          skipBtnRef.current.style.opacity = (1 - eased).toFixed(3);
        }
        if (st >= 1) {
          finishIntro();
          return;
        }
        rafRef.current = requestAnimationFrame(renderFrame);
        return;
      }

      const elapsed = now - startTime;
      const t = clamp(elapsed / 1000, 0, 3.05); // seconds: 0.00 -> 3.00

      // Trigger Hero entrance handoff right as the curtain crosses mid-viewport
      if (t >= 1.98) {
        fireReveal();
      }

      // =====================================================================
      // 1. CINEMA PROJECTION CURTAIN VERTICAL TRAJECTORY (barY & curtainYpx)
      //    Beat 1-2 (0.00-0.88s): Suspended cleanly at BAR_REST_Y (76)
      //    Beat 3   (0.88-1.50s): Stickman pulls heavily DOWN -> BAR_PULLED_Y (144)
      //    Beat 4   (1.50-1.64s): Ratchet micro-dip (+5.5u) & lock release click
      //    Beat 5   (1.64-2.74s): Spring roller glides ALL THE WAY UP off screen!
      // =====================================================================
      let curtainYpx = -(VB_H - BAR_REST_Y) * scale;
      let barY = BAR_REST_Y;
      let cordSwayX = Math.sin(t * 4.5) * 2.4 * (1 - seg(t, 0.72, 0.88));

      if (t < 0.88) {
        barY = BAR_REST_Y;
        curtainYpx = -(VB_H - barY) * scale;
      } else if (t < 1.50) {
        // Heavy downward tug with tactile resistance
        const pPull = easeOutCubic(seg(t, 0.88, 1.50));
        barY = lerp(BAR_REST_Y, BAR_PULLED_Y, pPull);
        curtainYpx = -(VB_H - barY) * scale;
        cordSwayX = Math.sin(pPull * Math.PI) * -4.5;
      } else if (t < 1.64) {
        // Spring-roller ratchet click (tiny downward catch -> upward release impulse)
        const pClick = seg(t, 1.50, 1.64);
        const dip = Math.sin(pClick * Math.PI) * 5.5;
        barY = BAR_PULLED_Y + dip;
        curtainYpx = -(VB_H - barY) * scale;
        cordSwayX = lerp(-2, 1.5, pClick);
      } else {
        // Silky cinema spring-roller glide ALL THE WAY UP past top of viewport
        const pUp = easeInOutQuart(seg(t, 1.64, 2.74));
        const startYpx = -(VB_H - BAR_PULLED_Y) * scale;
        const endYpx = -(vh + 76);
        curtainYpx = lerp(startYpx, endYpx, pUp);
        barY = VB_H + curtainYpx / scale;
        // Natural trailing pendulum sway on the brass pull-ring as screen ascends
        cordSwayX = Math.sin((t - 1.64) * 14) * Math.exp(-(t - 1.64) * 2.1) * 12;
      }

      const ringX = CENTER_X + cordSwayX;
      const ringY = barY + CORD_LEN;

      curtainEl.style.transform = `translate3d(0, ${curtainYpx.toFixed(1)}px, 0)`;

      // =====================================================================
      // 2. ARTICULATED STICKMAN KEYFRAMED MOTION (Clean Side-Profile Silhouette)
      // =====================================================================
      let pelvisX = ACTOR_PULL_X;
      let pelvisY = GROUND_Y - 46;
      let spineTilt = 0;
      let spineArch = 0;
      let headTilt = 0;
      let handGrabBlend = 0;

      let footLX = 0;
      let footLY = GROUND_Y;
      let footRX = 0;
      let footRY = GROUND_Y;
      let useFootIK = false;
      let legLFK = { a1: 0, a2: 0 };
      let legRFK = { a1: 0, a2: 0 };
      let armLFK = { a1: -0.25, a2: 0.3 };
      let armRFK = { a1: 0.25, a2: -0.3 };

      if (t < 0.48) {
        // BEAT 1: Confident Jog-In from left (0.00s -> 0.48s)
        const p = seg(t, 0.0, 0.48);
        const moveEased = easeOutQuad(p);
        pelvisX = lerp(34, ACTOR_PULL_X - 4, moveEased);
        const stride = p * Math.PI * 3.1;
        const damp = 1 - seg(p, 0.78, 1.0);
        const bounce = Math.abs(Math.sin(stride)) * 7 * damp;
        pelvisY = GROUND_Y - 45.5 - bounce;
        spineTilt = lerp(0.26, 0.06, seg(p, 0.72, 1.0));
        spineArch = 4 * damp;
        headTilt = -0.12;

        const swingL = Math.sin(stride) * 0.64 * damp;
        const swingR = -swingL;
        legLFK = { a1: swingL, a2: swingL > 0 ? -0.46 * damp : -0.2 * damp };
        legRFK = { a1: swingR, a2: swingR > 0 ? -0.46 * damp : -0.2 * damp };
        armLFK = { a1: -swingL * 0.85 - 0.1, a2: 0.56 * damp };
        armRFK = { a1: -swingR * 0.85 + 0.1, a2: 0.52 * damp };
      } else if (t < 0.66) {
        // BEAT 2A: Anticipation Deep Crouch looking up-right at brass ring (0.48s -> 0.66s)
        const p = easeInOutCubic(seg(t, 0.48, 0.66));
        pelvisX = lerp(ACTOR_PULL_X - 4, ACTOR_PULL_X, p);
        pelvisY = lerp(GROUND_Y - 45.5, GROUND_Y - 29, p);
        spineTilt = lerp(0.06, 0.36, p);
        spineArch = lerp(0, 7.5, p);
        headTilt = lerp(-0.12, -0.48, p);

        useFootIK = true;
        footLX = ACTOR_PULL_X - 18;
        footLY = GROUND_Y;
        footRX = ACTOR_PULL_X + 14;
        footRY = GROUND_Y;

        armLFK = { a1: lerp(-0.18, -0.86, p), a2: lerp(0.32, 0.22, p) };
        armRFK = { a1: lerp(0.18, -0.68, p), a2: lerp(0.22, 0.26, p) };
      } else if (t < 0.88) {
        // BEAT 2B: Athletic Diagonal Leap & Double-Hand Grab on brass ring (0.66s -> 0.88s)
        const p = seg(t, 0.66, 0.88);
        const jumpArc = easeOutCubic(p);
        pelvisX = lerp(ACTOR_PULL_X, ACTOR_PULL_X + 6, jumpArc);
        pelvisY = lerp(GROUND_Y - 29, BAR_REST_Y + CORD_LEN + 54, jumpArc);
        spineTilt = lerp(0.36, 0.18, jumpArc); // clean lean toward the golden ring!
        spineArch = lerp(7.5, -4.5, jumpArc);
        headTilt = -0.35;

        const tuck = easeOutQuad(seg(p, 0.25, 1.0));
        legLFK = { a1: lerp(-0.18, -0.34, tuck), a2: lerp(-0.14, -0.78, tuck) };
        legRFK = { a1: lerp(0.12, 0.32, tuck), a2: lerp(-0.12, -0.72, tuck) };

        armLFK = { a1: lerp(-0.86, 2.35, jumpArc), a2: -0.22 };
        armRFK = { a1: lerp(-0.68, 2.55, jumpArc), a2: -0.28 };
        handGrabBlend = easeOutCubic(seg(p, 0.42, 0.9));
      } else if (t < 1.50) {
        // BEAT 3: Heavy Bodyweight Pull-Down ("tarik kebawah", 0.88s -> 1.50s)
        // Clean side silhouette: body counter-leans left while BOTH arms stay IK-locked right onto the ring!
        const p = easeOutCubic(seg(t, 0.88, 1.50));
        pelvisX = lerp(ACTOR_PULL_X + 6, ACTOR_PULL_X - 8, p);
        const airHangY = BAR_REST_Y + CORD_LEN + 54;
        const groundPullY = GROUND_Y - 30;
        pelvisY = lerp(airHangY, groundPullY, p);
        spineTilt = lerp(0.18, -0.14, p); // leans back against load for authentic weight!
        spineArch = lerp(-4.5, 5.5, p);
        headTilt = 0.08;
        handGrabBlend = 1;

        if (p < 0.46) {
          const k = p / 0.46;
          legLFK = { a1: lerp(-0.34, 0.22, k), a2: lerp(-0.78, -0.95, k) };
          legRFK = { a1: lerp(0.32, 0.54, k), a2: lerp(-0.72, -1.02, k) };
        } else {
          // Braced power stance pulling down
          useFootIK = true;
          const land = easeOutCubic((p - 0.46) / 0.54);
          footLX = lerp(ACTOR_PULL_X - 18, ACTOR_PULL_X - 28, land);
          footLY = lerp(GROUND_Y - 12, GROUND_Y, land);
          footRX = lerp(ACTOR_PULL_X + 10, ACTOR_PULL_X + 18, land);
          footRY = lerp(GROUND_Y - 10, GROUND_Y, land);
        }
      } else if (t < 1.88) {
        // BEAT 4: Ratchet Click + Expressive Upward Release ("dijulur ke atas", 1.50s -> 1.88s)
        const p = seg(t, 1.50, 1.88);
        const rise = easeOutBack(clamp(p / 0.82, 0, 1));
        pelvisX = lerp(ACTOR_PULL_X - 8, ACTOR_PULL_X - 2, easeOutCubic(p));
        pelvisY = lerp(GROUND_Y - 30, GROUND_Y - 46, rise);
        spineTilt = lerp(-0.14, 0.08, rise);
        spineArch = lerp(5.5, -3, rise);
        headTilt = lerp(0.08, -0.36, rise);

        useFootIK = true;
        footLX = lerp(ACTOR_PULL_X - 28, ACTOR_PULL_X - 18, easeOutCubic(p));
        footLY = GROUND_Y;
        footRX = lerp(ACTOR_PULL_X + 18, ACTOR_PULL_X + 16, easeOutCubic(p));
        footRY = GROUND_Y;

        handGrabBlend = 1 - easeOutCubic(seg(t, 1.60, 1.72));
        armLFK = { a1: lerp(1.9, -0.34, rise), a2: lerp(-0.35, 0.28, rise) };
        armRFK = { a1: lerp(2.25, 2.68, rise), a2: lerp(-0.35, -0.16, rise) }; // sweeps gracefully skyward toward rising ring!
      } else {
        // BEAT 5: Confident Settle & Curtain-Clear Follow-Through (1.88s -> 3.00s)
        const p = seg(t, 1.88, 2.78);
        const settle = easeOutCubic(p);
        pelvisX = lerp(ACTOR_PULL_X - 2, ACTOR_PULL_X + 8, settle);
        pelvisY = GROUND_Y - 46 + Math.sin(settle * Math.PI) * 1.5;
        spineTilt = lerp(0.08, 0.0, settle);
        spineArch = lerp(-3, 0, settle);
        headTilt = lerp(-0.36, -0.06, settle);

        useFootIK = true;
        footLX = lerp(ACTOR_PULL_X - 18, ACTOR_PULL_X - 6, settle);
        footLY = GROUND_Y;
        footRX = lerp(ACTOR_PULL_X + 16, ACTOR_PULL_X + 22, settle);
        footRY = GROUND_Y;

        armLFK = { a1: lerp(-0.34, -0.16, settle), a2: lerp(0.28, 0.14, settle) };
        armRFK = { a1: lerp(2.68, 0.42, settle), a2: lerp(-0.16, -0.22, settle) };
      }

      // Compute upper-body spine & head coordinates
      const shX = pelvisX + Math.sin(spineTilt) * TORSO_LEN;
      const shY = pelvisY - Math.cos(spineTilt) * TORSO_LEN;
      const midSpineX = (pelvisX + shX) * 0.5 - Math.cos(spineTilt) * spineArch;
      const midSpineY = (pelvisY + shY) * 0.5 - Math.sin(spineTilt) * spineArch;
      const headX = shX + Math.sin(spineTilt + headTilt * 0.45) * NECK_LEN;
      const headY = shY - Math.cos(spineTilt + headTilt * 0.45) * NECK_LEN;

      // Compute legs (either IK to planted floor feet OR FK mid-air/running)
      let lLeg;
      let rLeg;
      if (useFootIK) {
        // Knee bends forward (+1 bends right in screen space)
        lLeg = solveIK2(pelvisX - 2, pelvisY, footLX, footLY, UPPER_LEG, LOWER_LEG, -1);
        rLeg = solveIK2(pelvisX + 2, pelvisY, footRX, footRY, UPPER_LEG, LOWER_LEG, -1);
      } else {
        lLeg = solveFK2(pelvisX - 1.5, pelvisY, legLFK.a1, legLFK.a2, UPPER_LEG, LOWER_LEG);
        rLeg = solveFK2(pelvisX + 1.5, pelvisY, legRFK.a1, legRFK.a2, UPPER_LEG, LOWER_LEG);
      }

      // Compute arms (blend smoothly between FK and 2-bone IK locked to brass ring!)
      const lArmFKPts = solveFK2(shX - 2, shY + 2, armLFK.a1, armLFK.a2, UPPER_ARM, LOWER_ARM);
      const rArmFKPts = solveFK2(shX + 2, shY + 2, armRFK.a1, armRFK.a2, UPPER_ARM, LOWER_ARM);
      let lArm = lArmFKPts;
      let rArm = rArmFKPts;

      if (handGrabBlend > 0.001) {
        const lArmIK = solveIK2(shX - 2, shY + 2, ringX - 3, ringY - 1.5, UPPER_ARM, LOWER_ARM, 1);
        const rArmIK = solveIK2(shX + 2, shY + 2, ringX + 1.5, ringY + 1.5, UPPER_ARM, LOWER_ARM, 1);
        lArm = {
          mx: lerp(lArmFKPts.mx, lArmIK.mx, handGrabBlend),
          my: lerp(lArmFKPts.my, lArmIK.my, handGrabBlend),
          ex: lerp(lArmFKPts.ex, lArmIK.ex, handGrabBlend),
          ey: lerp(lArmFKPts.ey, lArmIK.ey, handGrabBlend),
        };
        rArm = {
          mx: lerp(rArmFKPts.mx, rArmIK.mx, handGrabBlend),
          my: lerp(rArmFKPts.my, rArmIK.my, handGrabBlend),
          ex: lerp(rArmFKPts.ex, rArmIK.ex, handGrabBlend),
          ey: lerp(rArmFKPts.ey, rArmIK.ey, handGrabBlend),
        };
      }

      // Secondary-motion spring lag for the warm amber scarf behind neck
      const vx = shX - prevNeckX;
      const vy = shY - prevNeckY;
      prevNeckX = shX;
      prevNeckY = shY;
      scarfLagX = lerp(scarfLagX, clamp(-vx * 4.2 - 12, -32, 24), 0.16);
      scarfLagY = lerp(scarfLagY, clamp(-vy * 3.2 + 5, -16, 18), 0.16);
      const scarfCtrlX = shX + scarfLagX * 0.55;
      const scarfCtrlY = shY + 3 + scarfLagY * 0.35 + Math.sin(t * 11) * 1.8;
      const scarfEndX = shX + scarfLagX;
      const scarfEndY = shY + 5 + scarfLagY + Math.cos(t * 10) * 2.2;

      // =====================================================================
      // 3. APPLY DIRECT SVG DOM UPDATES (ZERO REACT RE-RENDERS)
      // =====================================================================
      const r = rigRefs.current;

      if (r.cord) {
        const midCordX = CENTER_X + cordSwayX * 0.45;
        const midCordY = barY + CORD_LEN * 0.55;
        r.cord.setAttribute(
          "d",
          `M${CENTER_X} ${barY.toFixed(1)} Q${midCordX.toFixed(1)} ${midCordY.toFixed(1)} ${ringX.toFixed(1)} ${(ringY - 6).toFixed(1)}`
        );
      }
      if (r.ring) {
        r.ring.setAttribute("cx", ringX.toFixed(1));
        r.ring.setAttribute("cy", ringY.toFixed(1));
      }
      if (r.spark) {
        // Minimalist editorial ratchet-release click arc at t = 1.48s..1.72s
        const sp = seg(t, 1.48, 1.72);
        const spAlpha = sp > 0 && sp < 1 ? Math.sin(sp * Math.PI) : 0;
        r.spark.setAttribute("opacity", spAlpha.toFixed(3));
        r.spark.setAttribute(
          "transform",
          `translate(${ringX.toFixed(1)} ${ringY.toFixed(1)}) scale(${(0.7 + sp * 0.65).toFixed(3)})`
        );
      }
      if (r.torso) {
        r.torso.setAttribute(
          "d",
          `M${pelvisX.toFixed(1)} ${pelvisY.toFixed(1)} Q${midSpineX.toFixed(1)} ${midSpineY.toFixed(1)} ${shX.toFixed(1)} ${shY.toFixed(1)}`
        );
      }
      if (r.head) {
        r.head.setAttribute("cx", headX.toFixed(1));
        r.head.setAttribute("cy", headY.toFixed(1));
      }
      if (r.scarf) {
        r.scarf.setAttribute(
          "d",
          `M${(shX - 1).toFixed(1)} ${(shY + 2).toFixed(1)} Q${scarfCtrlX.toFixed(1)} ${scarfCtrlY.toFixed(1)} ${scarfEndX.toFixed(1)} ${scarfEndY.toFixed(1)}`
        );
      }
      if (r.legL) {
        r.legL.setAttribute("d", limbPath(pelvisX - 1.5, pelvisY, lLeg.mx, lLeg.my, lLeg.ex, lLeg.ey));
      }
      if (r.legR) {
        r.legR.setAttribute("d", limbPath(pelvisX + 1.5, pelvisY, rLeg.mx, rLeg.my, rLeg.ex, rLeg.ey));
      }
      if (r.armL) {
        r.armL.setAttribute("d", limbPath(shX - 2, shY + 2, lArm.mx, lArm.my, lArm.ex, lArm.ey));
      }
      if (r.armR) {
        r.armR.setAttribute("d", limbPath(shX + 2, shY + 2, rArm.mx, rArm.my, rArm.ex, rArm.ey));
      }
      if (r.shadow) {
        // Dynamic ground contact shadow shrinks and softens as he leaps
        const heightOffGround = Math.max(0, GROUND_Y - 42 - pelvisY);
        const shadowScale = clamp(1 - heightOffGround / 90, 0.42, 1.15);
        r.shadow.setAttribute("cx", pelvisX.toFixed(1));
        r.shadow.setAttribute("rx", (20 * shadowScale).toFixed(1));
        r.shadow.setAttribute("opacity", (0.42 * shadowScale).toFixed(2));
      }

      // Smooth fade-out of bottom stage apron, stickman, and skip button as landing page opens
      const fadeOut = easeInOutCubic(seg(t, 2.08, 2.74));
      floorEl.style.opacity = (1 - fadeOut).toFixed(3);
      if (r.actorGroup) {
        r.actorGroup.style.opacity = (1 - fadeOut).toFixed(3);
      }
      if (skipBtnRef.current) {
        skipBtnRef.current.style.opacity = (1 - easeOutCubic(seg(t, 1.88, 2.28))).toFixed(3);
      }

      if (elapsed >= TOTAL_MS) {
        finishIntro();
        return;
      }
      rafRef.current = requestAnimationFrame(renderFrame);
    };

    rafRef.current = requestAnimationFrame(renderFrame);
    return () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = 0;
      }
    };
  }, [fireReveal, finishIntro]);

  return (
    <div
      ref={rootRef}
      className="ovs-intro"
      role="status"
      aria-label="Tirai pembuka Laporan Generator UBSI"
    >
      {/* Slim dark stage floor apron beneath the hanging cinema curtain (dissolves cleanly on lift) */}
      <div ref={floorRef} className="ovs-intro-floor" aria-hidden="true" />

      {/* Physical Wide-Screen Cinema Roller Curtain (pulls DOWN then glides ALL THE WAY UP) */}
      <div ref={curtainRef} className="ovs-curtain">
        {/* Subtle vertical woven-linen drape shading */}
        <div className="ovs-curtain-pleats" aria-hidden="true" />

        {/* Subtle A4 SK Rektor Margin Registration Hairlines printed onto the screen */}
        <div className="ovs-curtain-frame" aria-hidden="true">
          <span className="ovs-curtain-tick ovs-curtain-tick-tl">A4 · 3 / 4 / 2.5 cm</span>
          <span className="ovs-curtain-tick ovs-curtain-tick-tr">SK Rektor UBSI 165/2026</span>
        </div>

        {/* Centered Editorial Title Printed on the Cinema Projection Screen */}
        <div className="ovs-curtain-stage">
          <div className="ovs-intro-seal">
            <img
              src={`${baseUrl}diagrams/logo-ubsi.png`}
              alt=""
              width="44"
              height="44"
              className="ovs-intro-logo"
            />
          </div>

          <div className="ovs-intro-headline">
            <span className="ovs-intro-line">Laporan Generator</span>
            <span className="ovs-intro-line ovs-intro-line-serif">
              <em>UBSI</em> · SINTA 1-6
            </span>
          </div>

          <p className="ovs-curtain-sub">
            Engine OpenXML (.docx) &amp; Typst (.pdf) · Mendeley R1–R4
          </p>
        </div>

        {/* Weighted Oak & Brushed-Amber Bottom Roller Dowel Bar */}
        <div className="ovs-curtain-bar" aria-hidden="true">
          <span className="ovs-curtain-cap" />
          <span className="ovs-curtain-hub" />
          <span className="ovs-curtain-cap" />
        </div>
      </div>

      {/* Unified 60fps Articulated Stickman + Braided Pull-Cord + Brass Ring SVG */}
      <svg
        ref={svgRef}
        className="ovs-stickman-stage"
        viewBox={`0 0 ${VB_W} ${VB_H}`}
        fill="none"
        aria-hidden="true"
      >
        {/* Pull-cord & brushed-amber ring physically tethered to the moving curtain roller bar */}
        <path
          ref={(el) => {
            rigRefs.current.cord = el;
          }}
          d={`M${CENTER_X} ${BAR_REST_Y} Q${CENTER_X} ${BAR_REST_Y + 16} ${CENTER_X} ${BAR_REST_Y + CORD_LEN - 6}`}
          stroke="var(--ovs-soft)"
          strokeWidth="2.4"
          strokeLinecap="round"
        />
        <circle
          ref={(el) => {
            rigRefs.current.ring = el;
          }}
          cx={CENTER_X}
          cy={BAR_REST_Y + CORD_LEN}
          r="7.2"
          fill="#0e1a10"
          stroke="var(--ovs-soft)"
          strokeWidth="3"
        />

        {/* Minimalist Ratchet-Release Tension Arcs */}
        <g
          ref={(el) => {
            rigRefs.current.spark = el;
          }}
          opacity="0"
          stroke="var(--ovs-soft)"
          strokeWidth="1.8"
          strokeLinecap="round"
        >
          <path d="M-16 -4 L-23 -8" />
          <path d="M16 -4 L23 -8" />
          <path d="M-14 6 L-20 9" />
          <path d="M14 6 L20 9" />
        </g>

        {/* Articulated Editorial Stickman Actor */}
        <g
          ref={(el) => {
            rigRefs.current.actorGroup = el;
          }}
        >
          {/* Stage Ground Contact Shadow */}
          <ellipse
            ref={(el) => {
              rigRefs.current.shadow = el;
            }}
            cx="42"
            cy={GROUND_Y + 2}
            rx="18"
            ry="3.8"
            fill="#030704"
            opacity="0.38"
          />

          {/* Secondary-Motion Warm Amber Scarf */}
          <path
            ref={(el) => {
              rigRefs.current.scarf = el;
            }}
            d="M42 162 Q30 166 18 168"
            stroke="var(--ovs-soft)"
            strokeWidth="4.2"
            strokeLinecap="round"
          />

          {/* Back Limbs (subtle tonal depth separation) */}
          <path
            ref={(el) => {
              rigRefs.current.legL = el;
            }}
            d="M42 194 Q42 215 42 236"
            stroke="rgba(244, 246, 240, 0.72)"
            strokeWidth="4.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            ref={(el) => {
              rigRefs.current.armL = el;
            }}
            d="M42 165 Q36 180 34 194"
            stroke="rgba(244, 246, 240, 0.76)"
            strokeWidth="4.4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Flexible Curved Torso Spine */}
          <path
            ref={(el) => {
              rigRefs.current.torso = el;
            }}
            d="M42 194 Q44 178 44 163"
            stroke="#f4f6f0"
            strokeWidth="5.4"
            strokeLinecap="round"
          />

          {/* Front Limbs */}
          <path
            ref={(el) => {
              rigRefs.current.legR = el;
            }}
            d="M42 194 Q46 215 48 236"
            stroke="#f4f6f0"
            strokeWidth="5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            ref={(el) => {
              rigRefs.current.armR = el;
            }}
            d="M42 165 Q48 180 50 194"
            stroke="#f4f6f0"
            strokeWidth="4.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Iconic Minimalist Editorial Head */}
          <circle
            ref={(el) => {
              rigRefs.current.head = el;
            }}
            cx="44"
            cy="151"
            r="10.6"
            fill="#f4f6f0"
          />
        </g>
      </svg>

      <button
        ref={skipBtnRef}
        type="button"
        className="ovs-intro-skip"
        onClick={handleSkip}
        aria-label="Lewati animasi tirai pembuka"
      >
        <span>Lewati</span>
        <kbd>Esc</kbd>
      </button>
    </div>
  );
}
