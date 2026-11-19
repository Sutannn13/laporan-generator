import { Fragment, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import gsap from "gsap";

// Verbatim official SVG paths from Simple Icons (simple-icons@11 / simple-icons@latest)
const OFFICIAL_BRAND_PATHS = {
  visualstudiocode:
    "M23.15 2.587L18.21.21a1.494 1.494 0 0 0-1.705.29l-9.46 8.63-4.12-3.128a.999.999 0 0 0-1.276.057L.327 7.261A1 1 0 0 0 .326 8.74L3.899 12 .326 15.26a1 1 0 0 0 .001 1.479L1.65 17.94a.999.999 0 0 0 1.276.057l4.12-3.128 9.46 8.63a1.492 1.492 0 0 0 1.704.29l4.942-2.377A1.5 1.5 0 0 0 24 20.06V3.939a1.5 1.5 0 0 0-.85-1.352zm-5.146 14.861L10.826 12l7.178-5.448v10.896z",
  github:
    "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12",
  claude:
    "m4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z",
  cursor:
    "M11.503.131 1.891 5.678a.84.84 0 0 0-.42.726v11.188c0 .3.162.575.42.724l9.609 5.55a1 1 0 0 0 .998 0l9.61-5.55a.84.84 0 0 0 .42-.724V6.404a.84.84 0 0 0-.42-.726L12.497.131a1.01 1.01 0 0 0-.996 0M2.657 6.338h18.55c.263 0 .43.287.297.515L12.23 22.918c-.062.107-.229.064-.229-.06V12.335a.59.59 0 0 0-.295-.51l-9.11-5.257c-.109-.063-.064-.23.061-.23",
  opencode: "M22 24H2V0h20zM17 4.8H7v14.4h10z",
  python:
    "M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08z",
  nodedotjs:
    "M11.998,24c-0.321,0-0.641-0.084-0.922-0.247l-2.936-1.737c-0.438-0.245-0.224-0.332-0.08-0.383 c0.585-0.203,0.703-0.25,1.328-0.604c0.065-0.037,0.151-0.023,0.218,0.017l2.256,1.339c0.082,0.045,0.197,0.045,0.272,0l8.795-5.076 c0.082-0.047,0.134-0.141,0.134-0.238V6.921c0-0.099-0.053-0.192-0.137-0.242l-8.791-5.072c-0.081-0.047-0.189-0.047-0.271,0 L3.075,6.68C2.99,6.729,2.936,6.825,2.936,6.921v10.15c0,0.097,0.054,0.189,0.139,0.235l2.409,1.392 c1.307,0.654,2.108-0.116,2.108-0.89V7.787c0-0.142,0.114-0.253,0.256-0.253h1.115c0.139,0,0.255,0.112,0.255,0.253v10.021 c0,1.745-0.95,2.745-2.604,2.745c-0.508,0-0.909,0-2.026-0.551L2.28,18.675c-0.57-0.329-0.922-0.945-0.922-1.604V6.921 c0-0.659,0.353-1.275,0.922-1.603l8.795-5.082c0.557-0.315,1.296-0.315,1.848,0l8.794,5.082c0.57,0.329,0.924,0.944,0.924,1.603 v10.15c0,0.659-0.354,1.273-0.924,1.604l-8.794,5.078C12.643,23.916,12.324,24,11.998,24z M19.099,13.993 c0-1.9-1.284-2.406-3.987-2.763c-2.731-0.361-3.009-0.548-3.009-1.187c0-0.528,0.235-1.233,2.258-1.233 c1.807,0,2.473,0.389,2.747,1.607c0.024,0.115,0.129,0.199,0.247,0.199h1.141c0.071,0,0.138-0.031,0.186-0.081 c0.048-0.054,0.074-0.123,0.067-0.196c-0.177-2.098-1.571-3.076-4.388-3.076c-2.508,0-4.004,1.058-4.004,2.833 c0,1.925,1.488,2.457,3.895,2.695c2.88,0.282,3.103,0.703,3.103,1.269c0,0.983-0.789,1.402-2.642,1.402 c-2.327,0-2.839-0.584-3.011-1.742c-0.02-0.124-0.126-0.215-0.253-0.215h-1.137c-0.141,0-0.254,0.112-0.254,0.253 c0,1.482,0.806,3.248,4.655,3.248C17.501,17.007,19.099,15.91,19.099,13.993z",
  typst:
    "M12.654 17.846c0 1.114.16 1.861.479 2.242.32.381.901.572 1.743.572.872 0 1.99-.44 3.356-1.319l.871 1.45C16.547 22.931 14.44 24 12.785 24c-1.656 0-2.964-.395-3.922-1.187-.959-.82-1.438-2.256-1.438-4.307V6.989H5.246l-.349-1.626 2.528-.791V2.418L12.654 0v4.835l5.142-.395-.48 2.857-4.662-.176v10.725Z",
  mendeley:
    "M12.0037 9.1684h.019a2.355 2.355 0 011.5038 4.1655 1.8076 1.8076 0 01-.8561.452 2.348 2.348 0 01-.6487.0923h-.019c-.2246 0-.4421-.033-.6487-.0922a1.8126 1.8126 0 01-.8561-.4521 2.346 2.346 0 01-.8511-1.8106 2.358 2.358 0 012.3569-2.355m-9.9731 9.474c1.2652.1583 2.388-.762 2.5073-2.0573a2.4442 2.4442 0 00-.2136-1.236c-1.7724-3.8889 6.9726-3.978 5.4949-.3078l-.01.016c-.6988 1.1178-.3198 2.5695.841 3.2402.4272.2486.9003.3508 1.3625.3308.4622.02.9354-.0822 1.3624-.3308 1.161-.6717 1.54-2.1224.8412-3.2402l-.01-.016c-1.4778-3.6703 7.2682-3.581 5.4938.3077a2.4462 2.4462 0 00-.2126 1.2361c.1203 1.2953 1.2422 2.2156 2.5083 2.0572a2.345 2.345 0 001.4246-.7368s.5885-.4883.5795-1.7334c-.008-1.0156-.5795-1.578-.5795-1.578a2.2116 2.2116 0 00-1.8145-.6456c-1.6231-.036-1.8637-1.3073-1.4056-3.7033.1685-.4251.2416-.8802.2266-1.3354a3.4166 3.4166 0 00-2.1304-3.2953c-.039-.017-.0782-.03-.1183-.0461a1.5138 1.5138 0 00-.1343-.0461 3.4156 3.4156 0 00-4.004 1.4526c-.8171.8973-1.187 1.4417-2.0272 1.4417-.799 0-1.211-.5444-2.0271-1.4417a3.4126 3.4126 0 00-4.1374-1.4075c-.0401.016-.0792.029-.1193.0461a3.4156 3.4156 0 00-2.1294 3.2953c-.016.4552.0582.9103.2256 1.3354.4581 2.397.2175 3.6672-1.4045 3.7033-.795-.0852-1.3885.2426-1.988.8431-.6016.5995-.5514 2.2056 0 2.9063.4.5103.9423.8632 1.598.9454",
  // Official KiloCode extension SVG mark (kilocode.kilo-code/assets/icons/kilo-light.svg)
  kilocode: {
    viewBox: "91 91 330 330",
    paths: [
      "M322 377H377V421H307.857L278 391.143V322H322V377ZM421 307.857L391.143 278H322V322L377 322V377H421V307.857ZM234 278H190V322H234V278ZM91 391.143L120.857 421H234V377H135V278H91V391.143ZM371.172 189.999V120.856L341.315 90.9995H278V135H327.172V189.999H278V233.999H421V189.999H371.172ZM135 91H91V233.999H135V184.5H190V233.999H234V184.5L190 140.5H135V91ZM234 91H190V140.5H234V91Z",
    ],
  },
  // Official Freebuff symbol mark (https://freebuff.com/logo.svg)
  freebuff: {
    viewBox: "0 0 77.19 77.19",
    paths: [
      "M0 18.33C0 12.83 0 9.66 0.71 6.99C1.61 3.59 3.59 1.61 6.98 0.71C9.66 0 12.83 0 18.33 0L67.53 0C70.43 0 72.1 0 73.5 0.38C75.29 0.85 76.33 1.89 76.8 3.68C77.18 5.08 77.18 6.75 77.18 9.65C77.18 12.54 77.18 14.21 76.8 15.62C76.33 17.41 75.29 18.45 73.5 18.92C72.1 19.3 70.43 19.3 67.53 19.3L22.67 19.3C20.81 19.3 19.3 20.81 19.3 22.67L19.3 67.54C19.3 70.44 19.3 72.11 18.92 73.51C18.45 75.3 17.4 76.34 15.62 76.81C14.21 77.19 12.54 77.19 9.65 77.19C6.75 77.19 5.08 77.19 3.68 76.81C1.89 76.34 0.85 75.3 0.38 73.51C0 72.11 0 70.44 0 67.54Z",
      "M25.08 37.63C25.08 33.87 25.08 31.7 25.58 29.86C26.18 27.55 27.54 26.19 29.86 25.58C31.69 25.09 33.86 25.09 37.63 25.09L54.03 25.09C56.92 25.09 58.59 25.09 60 25.46C61.78 25.94 62.82 26.98 63.3 28.76C63.67 30.17 63.67 31.84 63.67 34.74C63.67 37.63 63.67 39.3 63.3 40.71C62.82 42.49 61.78 43.54 60 44.01C58.59 44.38 56.92 44.38 54.03 44.38L47.76 44.38C45.89 44.38 44.38 45.9 44.38 47.76L44.38 67.54C44.38 70.44 44.38 72.11 44 73.51C43.53 75.3 42.49 76.34 40.7 76.81C39.29 77.19 37.63 77.19 34.73 77.19C31.84 77.19 30.17 77.19 28.76 76.81C26.97 76.34 25.93 75.3 25.46 73.51C25.08 72.11 25.08 70.44 25.08 67.54Z",
    ],
  },
  // Official Google Antigravity IDE SVG mark (extensions/agy/img/logo.svg)
  antigravity: {
    viewBox: "14 16 84 84",
    paths: [
      "M89.6992 93.695C94.3659 97.195 101.366 94.8617 94.9492 88.445C75.6992 69.7783 79.7825 18.445 55.8659 18.445C31.9492 18.445 36.0325 69.7783 16.7825 88.445C9.78251 95.445 17.3658 97.195 22.0325 93.695C40.1159 81.445 38.9492 59.8617 55.8659 59.8617C72.7825 59.8617 71.6159 81.445 89.6992 93.695Z",
    ],
  },
};

export function ArrowIcon() {
  return (
    <svg className="ovs-svg ovs-arrow" viewBox="0 0 16 16" aria-hidden="true">
      <path
        d="M3 8h10M9 4l4 4-4 4"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function Kicker({ n, text, light = false }) {
  return (
    <p className={`ovs-kicker${light ? " ovs-kicker-light" : ""}`}>
      <span className="ovs-kicker-n">( {n} )</span>
      <span>{text}</span>
    </p>
  );
}

export function SplitHeading({ text, id, className = "ovs-h2", as: Tag = "h2" }) {
  const words = text.split(" ");
  return (
    <Tag id={id} className={className} data-split="">
      {words.map((word, idx) => (
        <Fragment key={idx}>
          <span className="ovs-w">
            <span data-w="">{word}</span>
          </span>
          {idx < words.length - 1 ? " " : null}
        </Fragment>
      ))}
    </Tag>
  );
}

export function MagneticLink({ href, onClick, className, children, target, rel }) {
  const linkRef = useRef(null);

  const handleMove = (e) => {
    const el = linkRef.current;
    if (!el || e.pointerType !== "mouse") return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const rect = el.getBoundingClientRect();
    const dx = (e.clientX - rect.left - rect.width / 2) * 0.18;
    const dy = (e.clientY - rect.top - rect.height / 2) * 0.26;
    gsap.to(el, { x: dx, y: dy, duration: 0.35, ease: "power3.out" });
  };

  const handleLeave = () => {
    const el = linkRef.current;
    if (!el) return;
    gsap.to(el, { x: 0, y: 0, duration: 0.7, ease: "elastic.out(1, 0.5)" });
  };

  return (
    <a
      ref={linkRef}
      href={href}
      target={target}
      rel={rel}
      onClick={onClick}
      onPointerMove={handleMove}
      onPointerLeave={handleLeave}
      className={className}
    >
      {children}
    </a>
  );
}

/*
 * Cursor-Directed Charge-to-White CTA Button (top-right Install Skill)
 * Starts subtly muted/faded yet readable; hovering charges a crisp pure-white (#ffffff)
 * energy fill directly from the cursor entry point with deep ink (#10150d) label.
 */
export function ChargeInstallButton({ href = "#pasang-skill", onClick, className = "", children }) {
  const btnRef = useRef(null);

  const updateOrigin = (e) => {
    const el = btnRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const cx = Math.round(e.clientX - rect.left);
    const cy = Math.round(e.clientY - rect.top);
    el.style.setProperty("--cx", `${cx}px`);
    el.style.setProperty("--cy", `${cy}px`);

    if (e.pointerType === "mouse" && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const dx = (e.clientX - rect.left - rect.width / 2) * 0.16;
      const dy = (e.clientY - rect.top - rect.height / 2) * 0.24;
      gsap.to(el, { x: dx, y: dy, duration: 0.32, ease: "power3.out" });
    }
  };

  const handleLeave = (e) => {
    const el = btnRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    el.style.setProperty("--cx", `${Math.round(e.clientX - rect.left)}px`);
    el.style.setProperty("--cy", `${Math.round(e.clientY - rect.top)}px`);
    gsap.to(el, { x: 0, y: 0, duration: 0.68, ease: "elastic.out(1, 0.5)" });
  };

  return (
    <a
      ref={btnRef}
      href={href}
      onClick={onClick}
      onPointerEnter={updateOrigin}
      onPointerMove={updateOrigin}
      onPointerLeave={handleLeave}
      className={`ovs-btn ovs-charge-btn ${className}`.trim()}
    >
      <span className="ovs-charge-fill" aria-hidden="true" />
      <span className="ovs-charge-meter" aria-hidden="true" />
      <span className="ovs-charge-content">{children}</span>
    </a>
  );
}

/*
 * 2D Measured Sliding Pill Hook for smooth tab / table-header transitions.
 * Tracks x, y, width, height so it works seamlessly even when pills wrap on mobile.
 */
export function useSlidingPill(containerRef, itemRefs, activeIndex) {
  const [box, setBox] = useState({ x: 0, y: 0, w: 0, h: 0, ready: false });

  useLayoutEffect(() => {
    const container = containerRef.current;
    const target = activeIndex >= 0 ? itemRefs.current[activeIndex] : null;
    if (!container || !target) {
      setBox((prev) => (prev.ready ? { ...prev, w: 0, ready: false } : prev));
      return undefined;
    }

    const measure = () => {
      const curTarget = itemRefs.current[activeIndex];
      if (!curTarget) return;
      setBox({
        x: curTarget.offsetLeft,
        y: curTarget.offsetTop,
        w: curTarget.offsetWidth,
        h: curTarget.offsetHeight,
        ready: true,
      });
    };

    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(container);
    ro.observe(target);
    return () => ro.disconnect();
  }, [containerRef, itemRefs, activeIndex]);

  return box;
}

export function GitHubMark({ className = "ovs-svg", size = 17 }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path fill="currentColor" d={OFFICIAL_BRAND_PATHS.github} />
    </svg>
  );
}

export function StarGlyph({ filled = false, size = 16 }) {
  return (
    <svg
      className="ovs-svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path
        d="M12 2.6l2.86 5.8 6.4.93-4.63 4.51 1.09 6.37L12 17.2l-5.72 3.01 1.09-6.37L2.74 9.33l6.4-.93L12 2.6z"
        fill={filled ? "currentColor" : "none"}
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function LockGlyph({ unlocked = false, size = 16 }) {
  return (
    <svg
      className="ovs-svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <rect
        x="4.5"
        y="10.5"
        width="15"
        height="10.5"
        rx="2.6"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.75"
      />
      <path
        d={
          unlocked
            ? "M8 10.5V7.2a4 4 0 0 1 7.6-1.7"
            : "M8 10.5V7.2a4 4 0 0 1 8 0v3.3"
        }
        fill="none"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
      />
    </svg>
  );
}

const NBSP = "\u00A0";
const MORPH_SCALE_X = 0.86;

export function MorphWord({ words }) {
  const [idx, setIdx] = useState(0);
  const outerRef = useRef(null);
  const innerRef = useRef(null);
  const pausedRef = useRef(false);
  const firstRunRef = useRef(true);

  useLayoutEffect(() => {
    const outer = outerRef.current;
    const inner = innerRef.current;
    if (!outer || !inner) return undefined;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const targetW = inner.offsetWidth * MORPH_SCALE_X;

    if (firstRunRef.current || reduced) {
      firstRunRef.current = false;
      outer.style.width = `${targetW}px`;
      return undefined;
    }

    const ctx = gsap.context(() => {
      gsap.to(outer, { width: targetW, duration: 0.65, ease: "expo.inOut" });
      gsap.fromTo(
        inner.children,
        { yPercent: 105, rotateX: -78, opacity: 0 },
        {
          yPercent: 0,
          rotateX: 0,
          opacity: 1,
          duration: 0.82,
          stagger: 0.038,
          ease: "expo.out",
          delay: 0.08,
        }
      );
    });
    return () => ctx.revert();
  }, [idx]);

  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced || words.length < 2) return undefined;

    const timer = window.setInterval(() => {
      const inner = innerRef.current;
      if (pausedRef.current || !inner || document.hidden) return;
      gsap.to(inner.children, {
        yPercent: -105,
        rotateX: 78,
        opacity: 0,
        duration: 0.4,
        stagger: 0.025,
        ease: "power3.in",
        onComplete: () => setIdx((prev) => (prev + 1) % words.length),
      });
    }, 3200);

    return () => window.clearInterval(timer);
  }, [words.length]);

  useEffect(() => {
    const inner = innerRef.current;
    if (!inner) return undefined;
    const ro = new ResizeObserver(() => {
      if (outerRef.current && innerRef.current) {
        outerRef.current.style.width = `${innerRef.current.offsetWidth * MORPH_SCALE_X}px`;
      }
    });
    ro.observe(inner);
    return () => ro.disconnect();
  }, [idx]);

  return (
    <span
      ref={outerRef}
      className="ovs-morph"
      onPointerEnter={() => {
        pausedRef.current = true;
      }}
      onPointerLeave={() => {
        pausedRef.current = false;
      }}
    >
      <span key={idx} ref={innerRef} className="ovs-morph-word">
        {Array.from(words[idx] || "").map((ch, cIdx) => (
          <span key={cIdx} className="ovs-ch">
            {ch === " " ? NBSP : ch}
          </span>
        ))}
      </span>
    </span>
  );
}

export function BrandMarqueeItem({ item }) {
  const spec = item.svgKey ? OFFICIAL_BRAND_PATHS[item.svgKey] : null;
  if (!spec) {
    return <span className="ovs-logo ovs-logo-neutral">{item.name}</span>;
  }
  const viewBox = typeof spec === "string" ? "0 0 24 24" : spec.viewBox;
  const paths = typeof spec === "string" ? [spec] : spec.paths;
  return (
    <span className="ovs-logo">
      <svg className="ovs-svg" viewBox={viewBox} aria-hidden="true">
        {paths.map((d, idx) => (
          <path key={idx} fill="currentColor" d={d} />
        ))}
      </svg>
      <span>{item.name}</span>
    </span>
  );
}

// Overstory's static-drawn procedural autumn canopy (seed=23, season="autumn")
const AUTUMN_PALETTE = {
  shadow: [46, 20, 10],
  mid: [146, 62, 18],
  lit: [224, 138, 36],
  glow: [252, 210, 116],
  twig: [46, 30, 22],
  shape: 0.5,
};

const SKY_SCHEME = {
  light: {
    stops: [
      [0, [100, 150, 208]],
      [0.55, [166, 202, 233]],
      [1, [212, 228, 241]],
    ],
    sun: [0.56, 0.28, 255, 255, 250, 0.62],
    cloud: [255, 255, 255, 0.9],
    haze: [194, 216, 236],
    stars: 0,
    leaf: 1,
  },
  dark: {
    stops: [
      [0, [8, 14, 34]],
      [0.55, [26, 40, 84]],
      [1, [74, 60, 108]],
    ],
    sun: [0.5, 0.92, 240, 150, 112, 0.42],
    cloud: [150, 140, 196, 0.32],
    haze: [34, 46, 84],
    stars: 1,
    leaf: 0.38,
  },
};

const CANOPY_LAYERS = [
  { reach: 0.6, band: 0.52, leaf: 0.011, twigs: 9, masses: 150, per: 24, haze: 0.44, blur: 0.5, res: 1.15 },
  { reach: 0.72, band: 0.58, leaf: 0.016, twigs: 8, masses: 120, per: 24, haze: 0.22, blur: 0, res: 1.15 },
  { reach: 0.86, band: 0.66, leaf: 0.023, twigs: 7, masses: 95, per: 22, haze: 0.08, blur: 0, res: 1 },
  { reach: 1.02, band: 0.86, leaf: 0.036, twigs: 6, masses: 72, per: 20, haze: 0, blur: 2.0, res: 0.8 },
];

const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const lerp = (a, b, t) => a + (b - a) * t;
const smoothstep = (e0, e1, x) => {
  const t = clamp((x - e0) / (e1 - e0), 0, 1);
  return t * t * (3 - 2 * t);
};

function makeRng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 1831565813) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const hash1 = (n) => {
  const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return s - Math.floor(s);
};

function noise2(x, y) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const fx = x - ix;
  const fy = y - iy;
  const h = (u, v) => hash1(u * 57 + v * 131);
  const ux = fx * fx * (3 - 2 * fx);
  const uy = fy * fy * (3 - 2 * fy);
  return lerp(lerp(h(ix, iy), h(ix + 1, iy), ux), lerp(h(ix, iy + 1), h(ix + 1, iy + 1), ux), uy);
}

function fbm(x, y) {
  let acc = 0;
  let amp = 0.5;
  let freq = 1;
  for (let i = 0; i < 5; i++) {
    acc += amp * noise2(x * freq, y * freq);
    freq *= 2.03;
    amp *= 0.5;
  }
  return acc / 0.96875;
}

const mixRgb = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
const rgbaStr = (rgb, a = 1) =>
  `rgba(${Math.round(rgb[0])},${Math.round(rgb[1])},${Math.round(rgb[2])},${a})`;

function sampleStops(stops, t) {
  for (let i = 1; i < stops.length; i++) {
    const prev = stops[i - 1];
    const cur = stops[i];
    if (t <= cur[0]) return mixRgb(prev[1], cur[1], (t - prev[0]) / (cur[0] - prev[0]));
  }
  return stops[stops.length - 1][1];
}

function clearingRadius(angle, layerIdx, seed) {
  const p1 = hash1(seed + 1) * 6.283;
  const p2 = hash1(seed + 2) * 6.283;
  const p3 = hash1(seed + 3) * 6.283;
  return (
    CANOPY_LAYERS[layerIdx].reach *
    (1 +
      0.13 * Math.sin(3 * angle + p1 + layerIdx * 0.55) +
      0.08 * Math.sin(5 * angle + p2 - layerIdx * 0.9) +
      0.05 * Math.sin(8 * angle + p3 + layerIdx * 1.7))
  );
}

function ellipseAxes(w, h) {
  return { rx: Math.max(w / 2, h * 0.34), ry: h / 2 };
}

function normDist(x, y, w, h) {
  const ax = ellipseAxes(w, h);
  const dx = (x - w / 2) / ax.rx;
  const dy = (y - h / 2) / ax.ry;
  return Math.sqrt(dx * dx + dy * dy);
}

function buildCanopyGeometry(w, h, layerIdx, seed) {
  const cfg = CANOPY_LAYERS[layerIdx];
  const rng = makeRng(seed * 977 + layerIdx * 7919 + 13);
  const gauss = () => (rng() + rng() + rng() - 1.5) / 0.75;
  const diag = Math.max(Math.sqrt(w * h), 1000);
  const leafUnit = cfg.leaf * diag;
  const cx = w / 2;
  const cy = h / 2;
  const areaScale = clamp((w * h) / (1612 * 1008), 0.62, 1.3);
  const twigs = [];
  const clusters = [];
  const maxBranchClusters = Math.round(cfg.masses * areaScale * 0.9);
  let forks = 0;

  const angleAt = (px, py) => {
    const ax = ellipseAxes(w, h);
    return Math.atan2((py - cy) / ax.ry, (px - cx) / ax.rx);
  };

  const growTwig = (sx, sy, dir, thick, depth) => {
    const pts = [sx, sy];
    const step = diag * 0.028;
    let x = sx;
    let y = sy;
    let a = dir;
    const stopDist = clearingRadius(angleAt(sx, sy), layerIdx, seed) + 0.02 + rng() * 0.08;
    for (let i = 0; i < 60; i++) {
      a += (rng() - 0.5) * 0.32;
      let toCenter = Math.atan2(cy - y, cx - x) - a;
      while (toCenter > Math.PI) toCenter -= Math.PI * 2;
      while (toCenter < -Math.PI) toCenter += Math.PI * 2;
      a += toCenter * 0.08;
      x += Math.cos(a) * step;
      y += Math.sin(a) * step;
      pts.push(x, y);
      const d = normDist(x, y, w, h);
      const cr = clearingRadius(angleAt(x, y), layerIdx, seed);
      if (d < cr + cfg.band * 0.75 && i % 2 === 0 && clusters.length < maxBranchClusters) {
        clusters.push({
          x: x + gauss() * leafUnit,
          y: y + gauss() * leafUnit,
          r: leafUnit * (1.9 + rng() * 1.2),
          n: Math.round(cfg.per * (0.7 + rng() * 0.5)),
          d,
        });
      }
      if (depth < 2 && i > 3 && forks < cfg.twigs * 2 && rng() < 0.16) {
        forks += 1;
        growTwig(x, y, a + (rng() < 0.5 ? -1 : 1) * (0.45 + rng() * 0.4), thick * 0.55, depth + 1);
      }
      if (d < Math.min(stopDist, cr + 0.04)) break;
    }
    clusters.push({
      x,
      y,
      r: leafUnit * 2.8,
      n: Math.round(cfg.per * 1.4),
      d: normDist(x, y, w, h),
    });
    twigs.push({ p: pts, w: thick });
  };

  for (let i = 0; i < cfg.twigs; i++) {
    const theta = (i / cfg.twigs) * Math.PI * 2 + rng() * 0.5;
    const ax = ellipseAxes(w, h);
    const sx = cx + Math.cos(theta) * ax.rx * 1.55;
    const sy = cy + Math.sin(theta) * ax.ry * 1.55;
    growTwig(sx, sy, Math.atan2(cy - sy, cx - sx) + (rng() - 0.5) * 0.7, leafUnit * (0.42 + rng() * 0.2), 0);
  }

  const targetMasses = Math.round(cfg.masses * areaScale);
  const nOff = hash1(seed + layerIdx) * 100;
  for (let tries = 0, added = 0; added < targetMasses && tries < targetMasses * 26; tries++) {
    const px = rng() * w;
    const py = rng() * h;
    const d = normDist(px, py, w, h);
    const cr = clearingRadius(angleAt(px, py), layerIdx, seed);
    if (d < cr || d > cr + cfg.band) continue;
    const nv = fbm(px / (diag * 0.12) + nOff, py / (diag * 0.12) - nOff);
    const inner = 1 - (d - cr) / cfg.band;
    if (nv >= 0.36 + inner * 0.12) {
      clusters.push({
        x: px,
        y: py,
        r: leafUnit * (1.9 + rng() * 1.6),
        n: Math.round(cfg.per * (0.8 + rng() * 0.5)),
        d,
      });
      added++;
    }
  }

  clusters.sort((a, b) => b.d - a.d);
  const leaves = [];
  for (const cl of clusters) {
    const cr = clearingRadius(angleAt(cl.x, cl.y), layerIdx, seed);
    const bandPos = clamp((cl.d - cr) / cfg.band, 0, 1);
    const vx = cx - cl.x;
    const vy = cy - cl.y;
    const vLen = Math.hypot(vx, vy) || 1;
    const sub = [];
    for (let i = 0; i < cl.n; i++) {
      const ox = gauss() * cl.r * 0.55;
      const oy = gauss() * cl.r * 0.55;
      const oLen = Math.hypot(ox, oy) || 1;
      const lit =
        0.5 +
        0.28 * ((ox * vx + oy * vy) / (oLen * vLen)) * Math.min(1, oLen / cl.r) +
        (rng() - 0.5) * 0.36 -
        bandPos * (0.3 + layerIdx * 0.07) +
        0.08;
      sub.push({
        x: cl.x + ox,
        y: cl.y + oy,
        s: leafUnit * (0.72 + rng() * 0.6),
        a: Math.atan2(oy, ox) + (rng() - 0.5) * 1.3,
        l: clamp(lit, 0, 1),
      });
    }
    sub.sort((a, b) => a.l - b.l);
    for (const lf of sub) leaves.push(lf);
  }
  return { twigs, leaves };
}

function drawSky(canvas, w, h, scheme, seed) {
  const sky = SKY_SCHEME[scheme] || SKY_SCHEME.light;
  const scale = 0.3;
  const cw = Math.max(8, Math.round(w * scale));
  const ch = Math.max(8, Math.round(h * scale));
  canvas.width = cw;
  canvas.height = ch;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const img = ctx.createImageData(cw, ch);
  const nOff = hash1(seed) * 50;
  const [sx, sy, sr, sg, sb, sa] = sky.sun;
  for (let y = 0; y < ch; y++) {
    const base = sampleStops(sky.stops, y / Math.max(1, ch - 1));
    for (let x = 0; x < cw; x++) {
      let col = base;
      const dx = x / cw - sx;
      const dy = (y / ch - sy) * (h / w);
      const sunAmt = Math.exp(-(dx * dx + dy * dy) * 9) * sa;
      col = mixRgb(col, [sr, sg, sb], sunAmt);
      const c1 = fbm(x / (cw * 0.16) + nOff, y / (ch * 0.2) - nOff * 0.5);
      const c2 = fbm(x / (cw * 0.05) - nOff, y / (ch * 0.07) + nOff);
      const cloudAmt = smoothstep(0.5, 0.82, c1 * 0.8 + c2 * 0.25) * sky.cloud[3];
      col = mixRgb(col, [sky.cloud[0], sky.cloud[1], sky.cloud[2]], cloudAmt);
      if (sky.stars && hash1(x * 13.1 + y * 71.7 + seed) > 0.9965) {
        col = mixRgb(col, [255, 250, 240], 0.75 * (1 - y / ch));
      }
      const idx = (y * cw + x) * 4;
      img.data[idx] = col[0];
      img.data[idx + 1] = col[1];
      img.data[idx + 2] = col[2];
      img.data[idx + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
}

function sampleLeafColor(pal, lit, hazeRgb, hazeAmt, leafBrightness) {
  let c;
  if (lit < 0.45) c = mixRgb(pal.shadow, pal.mid, lit / 0.45);
  else if (lit < 0.86) c = mixRgb(pal.mid, pal.lit, (lit - 0.45) / 0.41);
  else c = mixRgb(pal.lit, pal.glow, (lit - 0.86) / 0.14);
  c = c.map((v) => v * leafBrightness);
  return mixRgb(c, hazeRgb, hazeAmt);
}

function drawCanopyLayer(canvas, w, h, layerIdx, seed, scheme) {
  const cfg = CANOPY_LAYERS[layerIdx];
  const sky = SKY_SCHEME[scheme] || SKY_SCHEME.light;
  const dpr = Math.min((typeof window !== "undefined" && window.devicePixelRatio) || 1, 1.5) * cfg.res;
  const cw = Math.max(4, Math.round(w * dpr));
  const ch = Math.max(4, Math.round(h * dpr));
  const geom = buildCanopyGeometry(w, h, layerIdx, seed);
  const buf = cfg.blur > 0 ? document.createElement("canvas") : canvas;
  buf.width = cw;
  buf.height = ch;
  const ctx = buf.getContext("2d");
  if (!ctx) return;
  ctx.clearRect(0, 0, cw, ch);
  const hazeAmt = cfg.haze * (scheme === "dark" ? 0.7 : 1);
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.strokeStyle = rgbaStr(
    mixRgb(
      AUTUMN_PALETTE.twig.map((v) => v * (scheme === "dark" ? 0.5 : 1)),
      sky.haze,
      hazeAmt
    )
  );
  for (const tw of geom.twigs) {
    const count = tw.p.length / 2;
    for (let i = 1; i < count; i++) {
      ctx.lineWidth = Math.max(0.6, tw.w * (1 - (i / count) * 0.8)) * dpr;
      ctx.beginPath();
      ctx.moveTo(tw.p[(i - 1) * 2] * dpr, tw.p[(i - 1) * 2 + 1] * dpr);
      ctx.lineTo(tw.p[i * 2] * dpr, tw.p[i * 2 + 1] * dpr);
      ctx.stroke();
    }
  }
  const shape = AUTUMN_PALETTE.shape;
  const detail = layerIdx >= 2;
  for (const lf of geom.leaves) {
    const ca = Math.cos(lf.a) * dpr;
    const sa = Math.sin(lf.a) * dpr;
    ctx.setTransform(ca, sa, -sa, ca, lf.x * dpr, lf.y * dpr);
    const rx = lf.s * 0.5;
    const ry = lf.s * shape;
    ctx.fillStyle = rgbaStr(sampleLeafColor(AUTUMN_PALETTE, lf.l, sky.haze, hazeAmt, sky.leaf));
    ctx.beginPath();
    ctx.moveTo(-rx, 0);
    ctx.quadraticCurveTo(0, -ry, rx, 0);
    ctx.quadraticCurveTo(0, ry, -rx, 0);
    ctx.fill();
    if (lf.l > 0.72) {
      ctx.fillStyle = rgbaStr(
        sampleLeafColor(AUTUMN_PALETTE, Math.min(1, lf.l + 0.16), sky.haze, hazeAmt, sky.leaf),
        0.7
      );
      ctx.beginPath();
      ctx.moveTo(-rx * 0.55, 0);
      ctx.quadraticCurveTo(0, -ry * 0.5, rx * 0.7, 0);
      ctx.quadraticCurveTo(0, ry * 0.5, -rx * 0.55, 0);
      ctx.fill();
    }
    if (detail && lf.s > 14) {
      ctx.strokeStyle = rgbaStr(
        sampleLeafColor(AUTUMN_PALETTE, lf.l * 0.55, sky.haze, hazeAmt, sky.leaf),
        0.55
      );
      ctx.lineWidth = 0.7;
      ctx.beginPath();
      ctx.moveTo(-rx * 0.9, 0);
      ctx.lineTo(rx * 0.8, 0);
      ctx.stroke();
    }
  }
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (buf !== canvas) {
    canvas.width = cw;
    canvas.height = ch;
    const out = canvas.getContext("2d");
    if (!out) return;
    out.filter = `blur(${cfg.blur * dpr}px)`;
    out.drawImage(buf, 0, 0);
    out.filter = "none";
  }
}

export function AutumnCanopy({ seed = 23, scheme = "light", lazy = false }) {
  const wrapRef = useRef(null);
  const skyRef = useRef(null);
  const layerRefs = useRef([]);

  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return undefined;
    let rafId = 0;
    let alive = true;
    let triggered = !lazy;
    let prevSize = { w: 0, h: 0 };

    const renderOnce = () => {
      cancelAnimationFrame(rafId);
      const w = el.clientWidth;
      const h = el.clientHeight;
      if (w < 4 || h < 4) return;
      prevSize = { w, h };
      const tasks = [
        () => skyRef.current && drawSky(skyRef.current, w, h, scheme, seed),
        ...CANOPY_LAYERS.map((_, idx) => () => {
          const cv = layerRefs.current[idx];
          if (cv && cv.parentElement) {
            drawCanopyLayer(cv, cv.parentElement.clientWidth, cv.parentElement.clientHeight, idx, seed, scheme);
          }
        }),
      ];
      let stepIdx = 0;
      const tick = () => {
        if (!alive) return;
        try {
          tasks[stepIdx]();
        } catch {
          // Ignore transient canvas sizing issues during rapid resize
        }
        stepIdx += 1;
        if (stepIdx < tasks.length) {
          rafId = requestAnimationFrame(tick);
        }
      };
      rafId = requestAnimationFrame(tick);
    };

    const ro = new ResizeObserver(() => {
      if (!triggered) return;
      const w = el.clientWidth;
      const h = el.clientHeight;
      if (Math.abs(w - prevSize.w) >= 48 || Math.abs(h - prevSize.h) >= 140) {
        renderOnce();
      }
    });
    ro.observe(el);

    let io = null;
    if (lazy) {
      io = new IntersectionObserver(
        (entries) => {
          if (entries.some((e) => e.isIntersecting) && !triggered) {
            triggered = true;
            renderOnce();
          }
        },
        { rootMargin: "600px 0px" }
      );
      io.observe(el);
    } else {
      renderOnce();
    }

    return () => {
      alive = false;
      cancelAnimationFrame(rafId);
      ro.disconnect();
      if (io) io.disconnect();
    };
  }, [seed, scheme, lazy]);

  return (
    <div ref={wrapRef} className="ovs-canopy" aria-hidden="true">
      <div className="ovs-skybox">
        <canvas ref={skyRef} className="ovs-cv" />
      </div>
      {CANOPY_LAYERS.map((_, idx) => (
        <div key={idx} className="ovs-layer">
          <div className={`ovs-sway ovs-sway-${idx}`}>
            <canvas
              ref={(node) => {
                layerRefs.current[idx] = node;
              }}
              className="ovs-cv"
            />
          </div>
        </div>
      ))}
    </div>
  );
}

// 240x160 Service Preview Vector Cards matching Overstory's ko() art style
export function ServicePreviewArt({ art }) {
  if (art === "docx") {
    return (
      <svg className="ovs-svg" viewBox="0 0 240 160" aria-hidden="true">
        <rect width="240" height="160" rx="14" fill="var(--ovs-card)" />
        <rect x="18" y="18" width="88" height="124" rx="10" fill="var(--ovs-accent)" />
        <text x="34" y="88" fontSize="22" fontWeight="600" fill="var(--ovs-soft)">
          .DOCX
        </text>
        <rect x="120" y="22" width="102" height="12" rx="6" fill="var(--ovs-ink)" />
        <rect x="120" y="44" width="84" height="8" rx="4" fill="var(--ovs-line)" />
        <rect x="120" y="60" width="96" height="8" rx="4" fill="var(--ovs-line)" />
        <rect x="120" y="84" width="46" height="54" rx="8" fill="var(--ovs-soft)" />
        <rect x="174" y="84" width="48" height="54" rx="8" fill="var(--ovs-mist)" />
      </svg>
    );
  }
  if (art === "sinta") {
    return (
      <svg className="ovs-svg" viewBox="0 0 240 160" aria-hidden="true">
        <rect width="240" height="160" rx="14" fill="var(--ovs-card)" />
        <rect x="16" y="16" width="208" height="32" rx="8" fill="var(--ovs-mist)" />
        <rect x="28" y="28" width="96" height="8" rx="4" fill="var(--ovs-ink)" />
        <rect x="176" y="25" width="36" height="14" rx="7" fill="var(--ovs-accent)" />
        <rect x="16" y="58" width="98" height="86" rx="8" fill="var(--ovs-mist)" />
        <rect x="126" y="58" width="98" height="86" rx="8" fill="var(--ovs-mist)" />
        {[0, 1, 2, 3].map((r) => (
          <rect key={r} x="26" y={72 + r * 16} width="78" height="6" rx="3" fill="var(--ovs-line)" />
        ))}
        {[0, 1, 2, 3].map((r) => (
          <rect key={r} x="136" y={72 + r * 16} width="78" height="6" rx="3" fill="var(--ovs-line)" />
        ))}
      </svg>
    );
  }
  if (art === "workflow") {
    return (
      <svg className="ovs-svg" viewBox="0 0 240 160" aria-hidden="true">
        <rect width="240" height="160" rx="14" fill="var(--ovs-card)" />
        {[0, 1, 2, 3].map((idx) => (
          <g key={idx}>
            <circle
              cx={42 + idx * 52}
              cy="64"
              r="16"
              fill={idx === 2 ? "var(--ovs-accent)" : "var(--ovs-soft)"}
            />
            <rect x={26 + idx * 52} y="96" width="32" height="8" rx="4" fill="var(--ovs-ink)" />
            <rect x={22 + idx * 52} y="110" width="40" height="6" rx="3" fill="var(--ovs-line)" />
          </g>
        ))}
      </svg>
    );
  }
  if (art === "humanizer") {
    return (
      <svg className="ovs-svg" viewBox="0 0 240 160" aria-hidden="true">
        <rect width="240" height="160" rx="14" fill="var(--ovs-card)" />
        <rect x="18" y="20" width="76" height="24" rx="12" fill="var(--ovs-ink)" />
        <rect x="102" y="20" width="92" height="24" rx="12" fill="var(--ovs-soft)" />
        <path
          d="M24 118 C 56 96, 84 112, 116 82 S 172 88, 214 58"
          fill="none"
          stroke="var(--ovs-accent)"
          strokeWidth="4"
          strokeLinecap="round"
        />
        <circle cx="214" cy="58" r="6" fill="var(--ovs-accent)" />
      </svg>
    );
  }
  return (
    <svg className="ovs-svg" viewBox="0 0 240 160" aria-hidden="true">
      <rect width="240" height="160" rx="14" fill="#0e1a10" />
      {[
        [18, 52, "#f1b24a"],
        [78, 86, "#a9c6e4"],
        [18, 114, "#d9e3cf"],
        [18, 72, "#c9702a"],
        [98, 68, "#f1b24a"],
      ].map((bar, idx) => (
        <rect
          key={idx}
          x={bar[0]}
          y={28 + idx * 20}
          width={bar[1]}
          height="8"
          rx="4"
          fill={bar[2]}
          opacity="0.9"
        />
      ))}
      <rect x="152" y="108" width="68" height="30" rx="15" fill="#f1b24a" />
    </svg>
  );
}

// Overstory's 360x540 Botanical Autumn Tree SVG driven by GSAP ScrollTrigger strokeDashoffset + activeStep fallback
export function AutumnGrowthTree({ svgRef }) {
  const canopyDots = useMemo(() => {
    const rng = makeRng(427);
    return Array.from({ length: 44 }, () => {
      const ang = rng() * Math.PI * 2;
      const rad = Math.sqrt(rng());
      return {
        x: 182 + Math.cos(ang) * rad * 124,
        y: 134 + Math.sin(ang) * rad * 84,
        r: 10 + rng() * 15,
        l: rng(),
      };
    });
  }, []);

  const branchClusters = [
    [
      [96, 332],
      [262, 306],
    ],
    [
      [70, 214],
      [292, 186],
      [122, 270],
    ],
  ];

  return (
    <svg ref={svgRef} className="ovs-svg ovs-tree" viewBox="0 0 360 540" aria-hidden="true">
      <circle data-sun="" cx="300" cy="76" r="26" fill="var(--ovs-soft)" opacity="0.85" />
      <ellipse cx="180" cy="508" rx="130" ry="12" fill="var(--ovs-line)" />
      <g fill="none" stroke="var(--ovs-bark)" strokeLinecap="round">
        <path
          data-grow="0"
          pathLength={1}
          strokeWidth="9"
          d="M180 506 C 176 440, 188 380, 180 320 S 172 200, 182 120"
        />
        <path
          data-grow="1"
          pathLength={1}
          strokeWidth="4.5"
          d="M181 386 C 152 366, 122 354, 96 332"
        />
        <path
          data-grow="1"
          pathLength={1}
          strokeWidth="4.5"
          d="M180 356 C 210 340, 238 326, 262 306"
        />
        <path
          data-grow="2"
          pathLength={1}
          strokeWidth="3.5"
          d="M178 262 C 140 244, 104 238, 70 214"
        />
        <path
          data-grow="2"
          pathLength={1}
          strokeWidth="3.5"
          d="M182 232 C 220 216, 262 208, 292 186"
        />
        <path
          data-grow="2"
          pathLength={1}
          strokeWidth="3"
          d="M180 300 C 160 292, 140 286, 122 270"
        />
      </g>

      <g data-leaves="0">
        <path d="M180 470c-18-2-30-12-32-26 16 0 28 8 32 26z" fill="var(--ovs-accent)" />
        <path d="M181 462c16-6 30-4 38 8-14 6-28 4-38-8z" fill="var(--ovs-soft)" />
      </g>

      {branchClusters.map((group, gIdx) => (
        <g key={gIdx} data-leaves={gIdx + 1}>
          {group.map(([cx, cy], cIdx) => (
            <g key={cIdx}>
              <circle cx={cx} cy={cy} r="17" fill="var(--ovs-accent)" />
              <circle cx={cx + 9} cy={cy - 8} r="12" fill="var(--ovs-soft)" />
              <circle cx={cx - 10} cy={cy - 5} r="9" fill="var(--ovs-leaf2)" />
            </g>
          ))}
        </g>
      ))}

      <g data-leaves="3">
        {canopyDots.map((dot, idx) => (
          <circle
            key={idx}
            cx={dot.x}
            cy={dot.y}
            r={dot.r}
            fill={
              dot.l > 0.66
                ? "var(--ovs-soft)"
                : dot.l > 0.33
                  ? "var(--ovs-leaf2)"
                  : "var(--ovs-accent)"
            }
            opacity={0.82 + dot.l * 0.18}
          />
        ))}
      </g>
    </svg>
  );
}
