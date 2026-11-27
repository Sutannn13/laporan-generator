import { HERO_CONTENT, MARQUEE_BRANDS } from "../data/siteContent";
import {
  ArrowIcon,
  AutumnCanopy,
  BrandMarqueeItem,
  ChargeInstallButton,
  MorphWord,
} from "./OverstoryVisuals";

export default function HeroSection({ scheme, onInstallClick, onNavigate }) {
  const handleInstall = (e) => {
    e.preventDefault();
    onInstallClick();
  };

  return (
    <section
      id="top"
      className="ovs-hero"
      data-hero=""
      data-sec="top"
      aria-label="Pengantar Laporan Generator UBSI"
    >
      <AutumnCanopy seed={23} scheme={scheme} />

      <div className="ovs-copy">
        <p className="ovs-status">
          <i aria-hidden="true" />
          <span>{HERO_CONTENT.status}</span>
        </p>

        <h1 className="ovs-h1">
          <span className="ovs-line">
            <span data-hline="">{HERO_CONTENT.lead}</span>
          </span>
          <span className="ovs-line">
            <span data-hline="">
              <span className="ovs-sr">{HERO_CONTENT.words.join(", ")} </span>
              <span aria-hidden="true">
                <MorphWord words={HERO_CONTENT.words} />
              </span>{" "}
              {HERO_CONTENT.tail}
            </span>
          </span>
        </h1>

        <p className="ovs-hero-sub">{HERO_CONTENT.subtitle}</p>

        <div className="ovs-hero-actions">
          <ChargeInstallButton
            href="#pasang-skill"
            onClick={handleInstall}
            variant="dark"
            className="ovs-btn-xl"
          >
            <span>Install Skill</span>
            <ArrowIcon direction="down" />
          </ChargeInstallButton>
          <a
            href="#hasil-output"
            onClick={onNavigate("#hasil-output")}
            className="ovs-btn ovs-btn-glass ovs-btn-xl"
          >
            <span>Lihat Hasil Output</span>
          </a>
        </div>

        <p className="ovs-trusted">{HERO_CONTENT.trustedLabel}</p>

        <div
          className="ovs-marquee"
          role="region"
          aria-label="Ekosistem tool dan coding agent yang didukung"
        >
          <div className="ovs-marquee-track">
            {MARQUEE_BRANDS.map((brand) => (
              <BrandMarqueeItem key={brand.id} item={brand} />
            ))}
            <div className="ovs-marquee-clone" style={{ display: "contents" }} aria-hidden="true">
              {MARQUEE_BRANDS.map((brand) => (
                <BrandMarqueeItem key={`dup-${brand.id}`} item={brand} />
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="ovs-hero-mist" aria-hidden="true">
        <p className="ovs-above">{HERO_CONTENT.aboveCanopy}</p>
      </div>

      <a
        className="ovs-cue"
        href="#aturan-r1-r4"
        onClick={onNavigate("#aturan-r1-r4")}
      >
        <span className="ovs-cue-line" aria-hidden="true" />
        <span>{HERO_CONTENT.cue}</span>
      </a>
    </section>
  );
}
