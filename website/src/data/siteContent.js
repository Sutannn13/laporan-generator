export const REPO_URL = "https://github.com/Sutannn13/laporan-generator";
export const REPO_CLONE_URL = "https://github.com/Sutannn13/laporan-generator.git";
export const UPSTREAM_REPO_URL = "https://github.com/fatidaprilian/templatebsi";
export const UPSTREAM_CLONE_URL = "https://github.com/fatidaprilian/templatebsi.git";
export const GITHUB_API_REPO_URL = "https://api.github.com/repos/Sutannn13/laporan-generator";
export const SHIELDS_STARS_URL =
  "https://img.shields.io/github/stars/Sutannn13/laporan-generator.json";
export const QUICK_INSTALL_CMD =
  "git clone https://github.com/Sutannn13/laporan-generator.git && cd \"laporan-generator\" && npm run agent:install";

export const NAV_LINKS = [
  { label: "Prinsip R1-R4", href: "#aturan-r1-r4" },
  { label: "Skill & CLI", href: "#skill" },
  { label: "Galeri Output", href: "#hasil-output" },
  { label: "Alur Kerja", href: "#alur-kerja" },
  { label: "FAQ", href: "#faq" },
];

export const HERO_CONTENT = {
  status: "SK Rektor UBSI 165/2026 · Jurnal SINTA 1-6",
  lead: "Engine Dokumen Otomatis untuk",
  words: ["Laporan PKL", "Skripsi TI", "Jurnal SINTA", "Audit COBIT"],
  tail: "Siap Submit.",
  subtitle:
    "Susun, sunting in-place, dan audit berkas Word (.docx) serta Typst (.pdf) langsung di IDE Anda tanpa merusak sitasi Mendeley.",
  trustedLabel: "Terintegrasi di ekosistem coding agent dan pengolah dokumen proyek ini",
  cue: "Gulir ke prinsip R1-R4",
  aboveCanopy: "Above the canopy",
};

// Verified against AGENTS.md#L1, package.json#L25-L39, and scripts/install_agent_skills.py#L292-L395.
// svgKey maps to verbatim official SVG paths (Simple Icons + official KiloCode, Freebuff, and Antigravity brand marks).
export const MARQUEE_BRANDS = [
  { id: "vscode", name: "VS Code", svgKey: "visualstudiocode" },
  { id: "antigravity", name: "Antigravity (agy)", svgKey: "antigravity" },
  { id: "github", name: "GitHub", svgKey: "github" },
  { id: "claude", name: "Claude Code", svgKey: "claude" },
  { id: "cursor", name: "Cursor", svgKey: "cursor" },
  { id: "opencode", name: "OpenCode", svgKey: "opencode" },
  { id: "kilocode", name: "KiloCode", svgKey: "kilocode" },
  { id: "freebuff", name: "Freebuff", svgKey: "freebuff" },
  { id: "python", name: "Python OpenXML", svgKey: "python" },
  { id: "nodejs", name: "Node.js CLI", svgKey: "nodedotjs" },
  { id: "typst", name: "Typst PDF", svgKey: "typst" },
  { id: "mendeley", name: "Mendeley Cite", svgKey: "mendeley" },
];

export const MANIFESTO_CONTENT = {
  kicker: "Prinsip Inti & Aturan Sakral R1-R4",
  // [team] renders the overlapping R1-R4 circles; [chart] renders the terracotta verification pill.
  text:
    "Seluruh penyusunan naskah berjalan lokal di IDE tanpa peladen cloud. [team] Engine mengunci margin Word OpenXML, memverifikasi DOI Crossref aktif, [chart] dan menjaga Daftar Pustaka tetap murni milik Mendeley.",
};

// Strictly countable repository integers (zero fabricated claims, zero date ranges as big stats).
export const MANIFESTO_STATS = [
  {
    value: "0",
    label: "entri Daftar Pustaka yang ditulis AI ke berkas .docx jurnal (aturan R1 Mendeley)",
  },
  {
    value: "4",
    label: "skill mandiri terintegrasi di folder .agents/skills/ untuk seluruh alur naskah",
  },
  {
    value: "6",
    label: "peringkat preset jurnal nasional SINTA 1 sampai SINTA 6 lintas instansi",
  },
  {
    value: "29",
    label: "berkas contoh hasil output teranonimisasi di galeri publik (.docx, .pdf, diagram)",
  },
];

export const R1_R4_PRINCIPLES = [
  {
    code: "R1",
    title: "Daftar Pustaka Tetap Wilayah Mendeley",
    detail:
      "Agent dilarang menulis bagian DAFTAR PUSTAKA atau REFERENCES ke dalam berkas .docx jurnal. Bibliografi akhir disisipkan sendiri oleh penulis lewat Mendeley Cite.",
    guardTag: "--mendeley-mode",
  },
  {
    code: "R2",
    title: "Sunting Live In-Place Satu Berkas",
    detail:
      "Perubahan diterapkan langsung pada satu berkas .docx target memakai atomic_save_docx() sehingga logo kampus, header OJS, dan penomoran asli tetap utuh.",
    guardTag: "atomic_save_docx()",
  },
  {
    code: "R3",
    title: "Dosir Referensi .txt & .docx Terpisah",
    detail:
      "Kandidat rujukan disimpan di berkas .txt terpisah berlabel peringkat SINTA jujur, terbitan 2022-2026, DOI Crossref HTTP 200, dan tautan PDF langsung HTTP 200.",
    guardTag: "verify_sinta_refs.py",
  },
  {
    code: "R4",
    title: "Ringkas Analitis Tanpa Angka Karangan",
    detail:
      "Naskah jurnal dirangkum padat sesuai anggaran kata IMRaD tanpa menyalin mentah laporan PKL. Data lapangan kosong wajib ditandai [ISI DATA NYATA: ...].",
    guardTag: "check_antislop_academic.py",
  },
];

// 5 Horizontal Accordion Rows: 4 core skills + 1 CLI & usage studio
export const SKILL_ROWS = [
  {
    id: "laporan-generator",
    title: "laporan-generator",
    meta: "Engine .docx OpenXML",
    art: "docx",
    description:
      "Generator, editor in-place, dan auditor otomatis berbasis Python OpenXML (.docx) serta Typst (.pdf) untuk Proposal & 4 Outline PKL Prodi TI UBSI, Skripsi FTI 2026 (Outline 156, 138, 137, 158), serta Laporan Audit TI COBIT 2019 berformat temuan CCCE.",
    tags: [
      "Proposal & 4 Outline PKL UBSI",
      "Skripsi 156 / 138 / 137 / 158",
      "Audit TI COBIT 2019 CCCE",
      "update_docx_script.py",
      "challenge_text_and_math.py",
    ],
  },
  {
    id: "jurnal-sinta",
    title: "jurnal-sinta",
    meta: "Preset SINTA 1-6 & DOI",
    art: "sinta",
    description:
      "Menyediakan DNA tata letak OJS 1 kolom maupun 2 kolom untuk 6 peringkat SINTA lintas kampus (IJAIN UAD, PJIH Unpad, JTIIK UB, JISKA UIN Suka, JKI LPPM UBSI, TEKNOIF ITP, METIK), inspektor --inspect-docx, dan pencari referensi terverifikasi pada katalog 16.617 jurnal SINTA.",
    tags: [
      "IJAIN & PJIH (SINTA 1)",
      "JTIIK (S2) & JISKA (S3)",
      "JKI LPPM UBSI (SINTA 4)",
      "TEKNOIF (S5) & METIK (S6)",
      "Crossref & PDF HTTP 200",
      "MCP sinta-garuda",
    ],
  },
  {
    id: "mode-ilmiah",
    title: "mode-ilmiah",
    meta: "Alur 7 Tahap (Fase 0-6)",
    art: "workflow",
    description:
      "Sistem operasi kerja akademik 6 peran berurutan: Editor Kepala mengunci anggaran kata (F0), Peneliti memetakan template & DOI (F1), Arsitek menyusun benang merah metode (F2), Penulis menyunting live in-place (F3), Mitra Bestari menguji rubrik >= 85/100 (F4), dan Inspektur memvalidasi XML (F5-F6).",
    tags: [
      "Fase 0: Anggaran Kata",
      "Fase 1: Inspeksi & Riset DOI",
      "Fase 2: Matriks Metodologi",
      "Fase 3: Live In-Place R2",
      "Fase 4: Peer Review >= 85/100",
      "Fase 5-6: Audit XML & Serah Terima",
    ],
  },
  {
    id: "humanizer-id",
    title: "humanizer-id",
    meta: "Preset Akademik UBSI",
    art: "humanizer",
    description:
      "Penyunting bahasa Indonesia baku sesuai EYD Edisi V dan TBBBI Edisi IV yang dilengkapi preset khusus SK Rektor UBSI 2026 (--preset akademik --kampus ubsi). Memangkas kalimat terjemahan kaku, verba ringan berlebih, singkatan nonbaku, serta menjaga variasi panjang kalimat alami.",
    tags: [
      "--preset akademik --kampus ubsi",
      "EYD V & TBBBI IV",
      "Daftar Pustaka Tanpa et al.",
      "0 Em-Dash & Klise AI",
      "Burstiness >= 5.5 Kata",
    ],
  },
  {
    id: "pasang-skill",
    title: "Cara Pakai & CLI Scaffolder",
    meta: "Salin Perintah 1-Klik",
    art: "cli",
    isCliRow: true,
    description:
      "Pasang seluruh bundel skill mandiri sekali ke komputer lokal atau langsung buat kerangka dokumen baru dari terminal. Pilih skenario di bawah untuk menyalin perintahnya.",
    tags: [
      "/laporan-generator",
      "/mode-ilmiah",
      "/jurnal-sinta",
      "/sinta-buat",
      "/sinta-cek",
    ],
  },
];

export const INSTALL_TABS = [
  {
    id: "agent",
    label: "Pasang Skill Agent",
    command:
      "git clone https://github.com/Sutannn13/laporan-generator.git && cd \"laporan-generator\" && npm run agent:install",
    hint: "Menyinkronkan laporan-generator, mode-ilmiah, jurnal-sinta, dan humanizer-id ke Antigravity, Claude Code, Cursor, KiloCode, OpenCode, & Freebuff.",
  },
  {
    id: "cli",
    label: "Scaffold PKL (npx)",
    command:
      "npx github:Sutannn13/laporan-generator my-laporan --type laporan --outline 4 --yes",
    hint: "Membuat folder kerja PKL Prodi TI bersih sesuai outline pilihan (1: Inovasi, 2: Mobile, 3: Jaringan, 4: Analisis Sistem) atau --type proposal.",
  },
  {
    id: "skripsi",
    label: "Skripsi Word (.docx)",
    command:
      "uv run scripts/update_docx_script.py --scaffold --type skripsi --outline 156 --title \"JUDUL SKRIPSI\" --author \"Penulis Contoh\" --nim \"00000001\" --output \"Skripsi_UBSI.docx\"",
    hint: "Mendukung Kode Outline Skripsi FTI UBSI 2026: 156 (Perancangan), 138 (Penelitian), 137 (Jaringan), 158 (StartUp).",
  },
  {
    id: "sinta",
    label: "Generator SINTA",
    command:
      "uv run generate_sinta_journal_docx.py --sinta 4 --layout 2col --citation ieee --mendeley-mode --output \"Naskah_JKI.docx\" --yes && npm run test:all",
    hint: "Mengaktifkan --mendeley-mode (R1) agar Daftar Pustaka .docx tetap kosong untuk Mendeley serta memvalidasi XML & Anti-Slop.",
  },
];

// All 12 anonymized showcase specimens from website/public/ paired with Overstory's 4 seasonal art-stage tints.
export const SHOWCASE_ITEMS = [
  {
    id: "pdf-pkl",
    title: "Analisis Sistem Layanan PPID & Pengaduan Masyarakat Berbasis Web (23 Halaman)",
    docType: "Laporan Akhir PKL",
    outlineOrPreset: "Outline 4: Analisis Sistem (PIECES & UML)",
    format: "PDF",
    metricBig: "23 Hlm",
    layout: "1 Kolom A4 Margin 3/4/2.5/2.5 cm",
    citation: "Mendeley R1 · Tanpa et al.",
    summary:
      "Hasil render PDF dari berkas Word OpenXML: Sampul logo 5x5 cm, Pengesahan, Kata Pengantar, Daftar Isi, Bab I-IV (PIECES & 4 diagram UML), serta ruang Daftar Pustaka Mendeley (0 entri manual).",
    thumb: "thumbnails/pkl-outline4-cover.webp",
    previewUrl: "previews/01_Sampel_Laporan_PKL_UBSI_Outline4.pdf",
    downloadUrl: "previews/01_Sampel_Laporan_PKL_UBSI_Outline4.pdf",
    category: "pdf",
    tint: ["#cfe3d8", "#86b49a"],
    anonymizedLabel: "Penulis Contoh · NIM 00000001",
  },
  {
    id: "pdf-skripsi",
    title: "Skripsi TI UBSI Outline 156 - Verifikasi Dokumen Digital Ed25519 & Kode QR (47 Halaman)",
    docType: "Skripsi TI (S-1)",
    outlineOrPreset: "Outline 156: Perancangan Program (33 Hlm Isi)",
    format: "PDF",
    metricBig: "47 Hlm",
    layout: "A4 Spasi 2.0 · Margin 3/4/2.5/2.5 cm",
    citation: "Mendeley APA V.7 · Tanpa et al.",
    summary:
      "Hasil render PDF dari Word OpenXML sesuai SK Rektor UBSI 165/2026: Abstrak/Abstract terpisah (169 & 170 kata, spasi 1.0), Bab I-V (33 halaman isi), 5 diagram UML/LRS/QR nyata, dan 8 tabel spesifikasi serta uji Black-Box.",
    thumb: "thumbnails/skripsi-outline156-cover.webp",
    previewUrl: "previews/02_Sampel_Skripsi_TI_UBSI_Outline156.pdf",
    downloadUrl: "previews/02_Sampel_Skripsi_TI_UBSI_Outline156.pdf",
    category: "pdf",
    tint: ["#d4e0ee", "#7d9cc4"],
    anonymizedLabel: "Penulis Contoh · NIM 00000001",
  },
  {
    id: "pdf-jki",
    title: "JKI LPPM UBSI (SINTA 4) - Komparasi Random Forest & Gradient Boosting Deteksi Phishing (5 Hlm)",
    docType: "Jurnal Ilmiah SINTA 4",
    outlineOrPreset: "JKI LPPM UBSI · p-ISSN 2339-1928 · e-ISSN 2579-633X",
    format: "PDF",
    metricBig: "SINTA 4",
    layout: "2 Kolom · IEEE [1]-[16]",
    citation: "Mendeley R1 · 16 Ref SINTA 1-4",
    summary:
      "Hasil render PDF dari Word OpenXML: eksperimen nyata 11.055 rekaman UCI Phishing Websites (RF akurasi 97,69% vs GB 96,02%), header/footer OJS, superscript w:vertAlign, dan 0 entri daftar pustaka manual.",
    thumb: "thumbnails/jki-phishing-p1.webp",
    previewUrl: "previews/03_Sampel_Jurnal_SINTA4_JKI_UBSI_2Kolom.pdf",
    downloadUrl: "previews/03_Sampel_Jurnal_SINTA4_JKI_UBSI_2Kolom.pdf",
    category: "pdf",
    tint: ["#e9e2cf", "#c9a865"],
    anonymizedLabel: "Penulis Contoh · penulis.contoh@contoh.ac.id",
  },
  {
    id: "pdf-audit",
    title: "Laporan Audit Tata Kelola Keamanan & Kepatuhan PDP COBIT 2019 (53 Halaman)",
    docType: "Laporan Audit TI",
    outlineOrPreset: "COBIT 2019 (APO12, APO13, BAI06, DSS05, MEA03 · CCCE)",
    format: "PDF",
    metricBig: "53 Hlm",
    layout: "8 Seksi Romawi ii-vi & Arab 1-47",
    citation: "Mendeley R1 · 10 Jurnal OJS SINTA",
    summary:
      "Hasil render PDF dari Word OpenXML: simulasi terkontrol Portal Akademik Perguruan Tinggi Contoh, 44 butir checklist sinkron 100% dengan Tabel IV.1, kesenjangan kapabilitas 1,40 ke 3,40, matriks risiko 5x5, dan 5 temuan CCCE.",
    thumb: "thumbnails/audit-cobit-cover.webp",
    previewUrl: "previews/04_Sampel_Laporan_Audit_TI_COBIT2019.pdf",
    downloadUrl: "previews/04_Sampel_Laporan_Audit_TI_COBIT2019.pdf",
    category: "pdf",
    tint: ["#e6d9e4", "#b48aa8"],
    anonymizedLabel: "Penulis Contoh · NIM 00000001",
  },
  {
    id: "docx-pkl",
    title: "Laporan PKL UBSI Outline 4 Editable - Layanan PPID & Pengaduan (Word OpenXML)",
    docType: "Laporan Akhir PKL",
    outlineOrPreset: "Outline 4: Analisis Sistem (23 Halaman)",
    format: "DOCX",
    metricBig: "DOCX",
    layout: "A4 Margin 3/4/2.5/2.5 cm",
    citation: "Mendeley APA V.7 (R1)",
    summary:
      "Berkas Word (.docx) hasil scaffold update_docx_script.py dan mode-ilmiah: Times New Roman 12 pt spasi 2.0, indentasi 1.2 cm, 4 tabel spesifikasi & PIECES, serta 4 diagram 300 DPI.",
    thumb: "thumbnails/pkl-outline4-uml.webp",
    previewUrl: "previews/01_Sampel_Laporan_PKL_UBSI_Outline4.pdf",
    downloadUrl: "downloads/01_Sampel_Laporan_PKL_UBSI_Outline4.docx",
    category: "pkl",
    tint: ["#d4e0ee", "#7d9cc4"],
    anonymizedLabel: "Penulis Contoh · NIM 00000001",
  },
  {
    id: "docx-skripsi",
    title: "Skripsi TI UBSI Outline 156 Editable - Tanda Tangan Ed25519 & Kode QR (Word OpenXML)",
    docType: "Skripsi TI (S-1)",
    outlineOrPreset: "Outline 156: Perancangan Program (47 Halaman)",
    format: "DOCX",
    metricBig: "DOCX",
    layout: "5 Bab · 33 Hlm Isi Pokok",
    citation: "12 Jurnal OJS SINTA (R1/R3)",
    summary:
      "Berkas Word (.docx) hasil scaffold update_docx_script.py (--type skripsi --outline 156): uji vektor RFC 8032 nyata, kode QR Versi 13 (270 karakter), 10 skenario Black-Box Equivalence Partitioning, dan 0 entri daftar pustaka manual.",
    thumb: "thumbnails/skripsi-outline156-isi.webp",
    previewUrl: "previews/02_Sampel_Skripsi_TI_UBSI_Outline156.pdf",
    downloadUrl: "downloads/02_Sampel_Skripsi_TI_UBSI_Outline156.docx",
    category: "skripsi",
    tint: ["#e9e2cf", "#c9a865"],
    anonymizedLabel: "Penulis Contoh · NIM 00000001",
  },
  {
    id: "docx-jki-2col",
    title: "Jurnal SINTA 4 JKI UBSI Editable - Klasifikasi Situs Phishing 2 Kolom (Word OpenXML)",
    docType: "Jurnal Ilmiah SINTA 4",
    outlineOrPreset: "JKI LPPM UBSI · Layout 2 Kolom · Sitasi IEEE",
    format: "DOCX",
    metricBig: "DOCX",
    layout: "Section 1 (1Col) + Section 2 (2Col)",
    citation: "IEEE [1]-[16] · Mendeley Mode",
    summary:
      "Berkas Word (.docx) hasil generate_sinta_journal_docx.py (--sinta 4 --layout 2col --citation ieee --mendeley-mode): 4 tabel booktabs dengan header berulang, 3 grafik eksperimen 300 DPI, dan 16 rujukan SINTA 1-4 di berkas .txt R3.",
    thumb: "thumbnails/jki-phishing-hasil.webp",
    previewUrl: "previews/03_Sampel_Jurnal_SINTA4_JKI_UBSI_2Kolom.pdf",
    downloadUrl: "downloads/03_Sampel_Jurnal_SINTA4_JKI_UBSI_2Kolom.docx",
    category: "sinta",
    tint: ["#e6d9e4", "#b48aa8"],
    anonymizedLabel: "Penulis Contoh · penulis.contoh@contoh.ac.id",
  },
  {
    id: "docx-audit",
    title: "Laporan Audit TI COBIT 2019 Editable - Keamanan & Kepatuhan UU PDP (Word OpenXML)",
    docType: "Laporan Audit TI",
    outlineOrPreset: "COBIT 2019 · Format Temuan CCCE · 44 Butir Checklist",
    format: "DOCX",
    metricBig: "DOCX",
    layout: "A4 Margin 4/3/2.5/2.5 cm · 8 Seksi",
    citation: "Mendeley R1 · Tanpa et al.",
    summary:
      "Berkas Word (.docx) 53 halaman (10.902 kata, 327 paragraf, 15 tabel, 5 diagram 300 DPI): penomoran halaman Romawi dan Arab terpisah, Lampiran L-A s.d. L-E terverifikasi Crossref, dan ruang Daftar Pustaka Mendeley bersih.",
    thumb: "thumbnails/audit-cobit-isi.webp",
    previewUrl: "previews/04_Sampel_Laporan_Audit_TI_COBIT2019.pdf",
    downloadUrl: "downloads/04_Sampel_Laporan_Audit_TI_COBIT2019.docx",
    category: "audit",
    tint: ["#cfe3d8", "#86b49a"],
    anonymizedLabel: "Penulis Contoh · NIM 00000001",
  },
];

export const DIAGRAM_GALLERY = [
  {
    src: "diagrams/diagram_radar_capability.png",
    title: "Grafik Tingkat Kapabilitas COBIT 2019",
    tag: "Audit TI (APO13 - MEA03)",
    caption: "Perbandingan level saat ini vs target pada 5 domain COBIT 2019.",
  },
  {
    src: "diagrams/diagram_risk_matrix.png",
    title: "Matriks Penilaian Risiko 5x5",
    tag: "Audit TI (CCCE)",
    caption: "Pemetaan skor kemungkinan dan dampak risiko sistem informasi akademik.",
  },
  {
    src: "diagrams/diagram_arsitektur_siakad.png",
    title: "Arsitektur Multi-Tier Portal Akademik (Simulasi)",
    tag: "Audit Infrastruktur",
    caption: "Simulasi zona jaringan Portal Akademik Perguruan Tinggi Contoh (DMZ, Application Tier, Data Layer, & Audit Logging).",
  },
  {
    src: "diagrams/diagram_roadmap_perbaikan.png",
    title: "Roadmap Perbaikan Tata Kelola TI",
    tag: "Rekomendasi 3 Fase",
    caption: "Tahapan mitigasi jangka pendek, standardisasi proses, dan re-audit.",
  },
  {
    src: "diagrams/gambar_sinta1_apk_attack_flow.png",
    title: "Vektor Malicious APK & Matriks Hukum",
    tag: "SINTA 1 Hukum Siber",
    caption: "Korelasi eksploitasi teknis Android terhadap KUHP Baru, UU ITE, dan POJK 22/2023.",
  },
  {
    src: "diagrams/sampel_rancangan_antarmuka.png",
    title: "Mockup Aplikasi Press Release (Teranonimisasi)",
    tag: "Laporan PKL UML & UI",
    caption: "Visual antarmuka sistem usulan beresolusi 300 DPI hasil scripts/generate_diagrams.py.",
  },
];

// 4 Growth Steps matching Overstory's 01-04 Seed/Sapling/Branch/Canopy structure (accent word uses Bodoni Moda 400).
export const PROCESS_STEPS = [
  {
    name: "Pasang",
    when: "Langkah Awal",
    title: "Sinkronisasi Skill & Pilih Outline",
    text:
      "Pasang keempat skill mandiri ke IDE Anda dengan satu perintah, lalu tentukan target dokumen: Proposal/Laporan PKL UBSI, Skripsi FTI 2026, Audit COBIT, atau Jurnal SINTA 1-6.",
    command: "npm run agent:install",
  },
  {
    name: "Susun",
    when: "Mode Ilmiah Fase 0-3",
    title: "Inspeksi Template, Riset DOI, & Sunting In-Place",
    text:
      "Engine membaca anatomi XML berkas .docx target tanpa merusak format asli (R2), memverifikasi referensi 2022-2026 via Crossref HTTP 200 ke berkas .txt terpisah (R3), dan menyusun draf analitis hemat kata (R4).",
    command: "npm run sinta:inspect -- \"Template_JKI.docx\"",
  },
  {
    name: "Audit",
    when: "Mode Ilmiah Fase 4-5",
    title: "Penyuntingan Bahasa UBSI & Gerbang Reviewer",
    text:
      "Draf Bahasa Indonesia disunting memakai humanizer-id preset kampus UBSI, diuji rubrik Mitra Bestari minimal 85/100, lalu diperiksa check_antislop_academic.py untuk memastikan 0 em-dash dan 0 entri pustaka AI (R1).",
    command: "uv run scripts/check_antislop_academic.py --input \"Target.docx\" --mendeley-mode",
  },
  {
    name: "Terbit",
    when: "Mode Ilmiah Fase 6",
    title: "Sinkronisasi Mendeley Cite & Siap Unggah",
    text:
      "Anda menyisipkan Daftar Pustaka akhir secara mandiri melalui plugin Mendeley Cite pada penanda sitasi yang sudah tertata, lalu berkas .docx atau .pdf siap diunggah ke portal OJS maupun DigiSAYS UBSI.",
    command: "npm run test:all",
  },
];

// 7 Specifications of SK Rektor UBSI No. 165/2.01/UBSI/III/2026 for the #0e1a10 Dark Forest Band.
export const COMPARE_ROWS = [
  {
    shortTab: "01 Margin & Spasi",
    aspect: "Margin, Spasi, & Indentasi",
    headline:
      "Kertas A4 dengan batas Atas 3 cm, Kiri 4 cm, Bawah 2.5 cm, dan Kanan 2.5 cm dikunci langsung di level OpenXML.",
    manual:
      "Margin 3/4/2.5/2.5 cm dan indentasi 1.2 cm kerap bergeser saat menyalin teks antarbab di pengolah kata.",
    engine:
      "update_docx_script.py mengunci style XML Word & Typst: Times New Roman 12 pt, spasi 2.0, serta first-line indent 1.2 cm.",
  },
  {
    shortTab: "02 Tanpa et al.",
    aspect: "Penulisan Pengarang Daftar Pustaka",
    headline:
      "Seluruh nama pengarang Skripsi dan Laporan PKL ditulis utuh tanpa singkatan et al. maupun dkk. sesuai Bab II Poin 2.12.",
    manual:
      "Sering menyingkat nama pengarang dengan et al. atau dkk. sehingga melanggar Bab II Poin 2.12 butir 5 SK Rektor UBSI 2026.",
    engine:
      "Flag --no-et-al pada verify_sinta_refs.py mencetak nama seluruh penulis lengkap untuk UBSI, serta IEEE [1] untuk JKI SINTA 4.",
  },
  {
    shortTab: "03 Mendeley R1-R2",
    aspect: "Keamanan Field Mendeley Cite",
    headline:
      "Bagian Daftar Pustaka di dalam .docx jurnal dibiarkan bersih 100% agar field plugin Mendeley Cite tidak pernah rusak.",
    manual:
      "AI umum menimpa bagian Daftar Pustaka .docx secara langsung dan merusak kode XML plugin Mendeley.",
    engine:
      "Aturan R1 (--mendeley-mode) dan R2 (atomic_save_docx) menyunting naskah secara in-place dan mengekspor rujukan ke berkas .txt terpisah.",
  },
  {
    shortTab: "04 Logo & Abstrak",
    aspect: "Atribut Visual & Halaman Abstrak",
    headline:
      "Logo sampul 5 x 5 cm (Skripsi/TA) atau 4 x 4 cm (PKL), watermark 10 x 10 cm Behind Text pada scaffold Skripsi/TA, serta penomoran Romawi-Arab multi-seksi terpasang sejak awal.",
    manual:
      "Ukuran logo sampul, watermark Behind Text, nomor halaman Romawi/Arab antar-seksi, dan spasi halaman abstrak dwibahasa sering tidak seragam.",
    engine:
      "Scaffolder otomatis memisahkan lembar PERNYATAAN, ABSTRAK/ABSTRACT (1 spasi), watermark 10 x 10 cm (Skripsi/TA), dan bab utama berspasi 2.0.",
  },
  {
    shortTab: "05 DOI 2022-2026",
    aspect: "Validitas Referensi Jurnal Primer",
    headline:
      "Setiap kandidat rujukan diuji aktif HTTP 200 pada Crossref dan tautan PDF langsung sebelum masuk ke dosir .txt.",
    manual:
      "Rujukan berisiko memakai DOI mati, tautan PDF terkunci, atau melampaui batas usia publikasi 5 tahun terakhir.",
    engine:
      "verify_sinta_refs.py & MCP sinta-garuda memfilter terbitan 2022-2026 serta mencocokkan peringkat pada 16.617 jurnal SINTA.",
  },
  {
    shortTab: "06 Audit Bahasa",
    aspect: "Kualitas Bahasa Baku & Anti-Slop",
    headline:
      "Prosa akademik Indonesia disunting memakai preset kampus UBSI dan diuji variasi panjang kalimat alami.",
    manual:
      "Kalimat mentah terdengar seragam, penuh frasa klise terjemahan, dan menyelipkan tanda hubung panjang.",
    engine:
      "humanizer-id (--preset akademik --kampus ubsi) + check_antislop_academic.py menjamin 0 em-dash dan simpangan baku >= 5.5 kata.",
  },
  {
    shortTab: "07 Similarity",
    aspect: "Konsistensi Tabel & Ambang Turnitin",
    headline:
      "Angka pada tabel rekapitulasi diaudit silang terhadap lampiran untuk menjaga kesiapan uji kemiripan naskah.",
    manual:
      "Tabel rekapitulasi angka sering selisih terhadap lampiran dan melampaui batas kemiripan naskah.",
    engine:
      "challenge_text_and_math.py memverifikasi konsistensi angka otomatis untuk target Turnitin <= 25% UBSI (<= 20% JKI) dan berkas <= 5 MB.",
  },
];

export const FAQS = [
  {
    q: "Mengapa website ini tidak memiliki menu Login, Pricing, atau generator berbasis cloud?",
    a: "Laporan Generator UBSI adalah perangkat lunak sumber terbuka gratis (lisensi MIT) yang berjalan 100% lokal di komputer dan IDE Anda. Tidak ada akun, biaya langganan, ataupun unggahan naskah mahasiswa ke peladen pihak ketiga.",
  },
  {
    q: "Bagaimana aturan R1 mencegah bentrokan Daftar Pustaka dengan Mendeley?",
    a: "Aturan R1 melarang AI menuliskan bagian DAFTAR PUSTAKA atau REFERENCES ke dalam berkas .docx naskah jurnal. Agent hanya menyisipkan penanda sitasi seperti [1] sesuai nomor urut berkas kandidat referensi .txt terpisah (R3), sehingga Anda bebas menghasilkan bibliografi akhir lewat Mendeley Cite.",
  },
  {
    q: "Bisakah langsung menyunting file template .docx resmi dari kampus atau OJS?",
    a: "Bisa. Aturan R2 mewajibkan agent menginspeksi struktur XML dengan --inspect-docx lalu menyunting langsung berkas .docx target memakai atomic_save_docx(). Margin, header/footer OJS, logo instansi, dan penomoran tetap utuh selama berkas tidak sedang terkunci di Microsoft Word.",
  },
  {
    q: "Benarkah Daftar Pustaka Skripsi dan TA UBSI melarang singkatan et al. maupun dkk.?",
    a: "Benar. Merujuk Bab II Poin 2.12 butir 5 SK Rektor UBSI No. 165/2.01/UBSI/III/2026 di pedoman-kampus-ubsi.json, seluruh nama pengarang pada Daftar Pustaka Tugas Akhir dan Skripsi UBSI wajib ditulis lengkap tanpa et al. atau dkk. Sementara itu, artikel jurnal seperti JKI SINTA 4 mengikuti gaya IEEE masing-masing OJS.",
  },
  {
    q: "Bagaimana keamanan privasi pada 29 berkas contoh di galeri website ini?",
    a: "Seluruh 4 pratinjau PDF, 4 berkas unduhan .docx, 8 gambar mini WebP, dan 13 aset diagram/logo PNG di folder website/public/ merupakan sampel baru teranonimisasi penuh (Penulis Contoh, NIM 00000001, Kota Contoh, dan Perguruan Tinggi Contoh) tanpa data pribadi mahasiswa nyata.",
  },
  {
    q: "Bagaimana cara men-deploy halaman dokumentasi ini ke GitHub Pages?",
    a: "Jalankan npm run build di dalam direktori website/ lalu arahkan GitHub Pages ke hasil build website/dist. Konfigurasi Vite sudah memakai base './' sehingga seluruh aset termuat secara relatif tanpa tautan rusak.",
  },
];
