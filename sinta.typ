// Engine tata letak artikel jurnal ilmiah terindeks SINTA 1 s.d. SINTA 6
// Mendukung pemilihan SINTA 1-6 (6 instansi berbeda) dan opsi Layout 2 Kolom (Terbagi 2) vs 1 Kolom (Biasa)

#let sinta-presets = (
  "1": (
    rank: 1,
    short: "IJAIN",
    name: "International Journal of Advances in Intelligent Informatics",
    institution: "Universitas Ahmad Dahlan (UAD) Yogyakarta",
    p-issn: "2442-6571",
    e-issn: "2548-3161",
    doi: "https://doi.org/10.26555/ijain.v12i1.1920",
    default-layout: "2col",
    gutter: 0.6cm,
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.0cm, right: 2.0cm),
    title-size: 16pt,
    author-size: 11pt,
    affil-size: 9pt,
    abs-size: 9pt,
    h1-size: 10pt,
    h2-size: 10pt,
    body-size: 10pt,
    caption-size: 8pt,
    indent: 0.5cm,
    leading: 0.55em,
  ),
  "2": (
    rank: 2,
    short: "JTIIK",
    name: "Jurnal Teknologi Informasi dan Ilmu Komputer",
    institution: "Fakultas Ilmu Komputer (FILKOM), Universitas Brawijaya (UB)",
    p-issn: "2355-7699",
    e-issn: "2528-6579",
    doi: "https://doi.org/10.25126/jtiik.2026131842",
    default-layout: "2col",
    gutter: 0.6cm,
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.0cm),
    title-size: 14pt,
    author-size: 11pt,
    affil-size: 9pt,
    abs-size: 9pt,
    h1-size: 10pt,
    h2-size: 10pt,
    body-size: 10pt,
    caption-size: 9pt,
    indent: 0.75cm,
    leading: 0.55em,
  ),
  "3": (
    rank: 3,
    short: "JISKA",
    name: "JISKA (Jurnal Informatika Sunan Kalijaga)",
    institution: "UIN Sunan Kalijaga Yogyakarta",
    p-issn: "2527-5836",
    e-issn: "2528-0074",
    doi: "https://doi.org/10.14421/jiska.2026.11.1.1-14",
    default-layout: "2col",
    gutter: 0.6cm,
    margin: (top: 3.0cm, bottom: 2.5cm, left: 2.5cm, right: 2.0cm),
    title-size: 14pt,
    author-size: 10pt,
    affil-size: 9pt,
    abs-size: 9pt,
    h1-size: 10pt,
    h2-size: 10pt,
    body-size: 10pt,
    caption-size: 9pt,
    indent: 0.5cm,
    leading: 0.55em,
  ),
  "4": (
    rank: 4,
    short: "JKI",
    name: "Jurnal Khatulistiwa Informatika",
    institution: "LPPM Universitas Bina Sarana Informatika (UBSI)",
    p-issn: "2339-1928",
    e-issn: "2579-633X",
    doi: "https://doi.org/10.31294/jki.v14i1.21890",
    default-layout: "2col",
    gutter: 0.5cm,
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.0cm),
    title-size: 14pt,
    author-size: 10pt,
    affil-size: 9pt,
    abs-size: 9pt,
    h1-size: 10pt,
    h2-size: 10pt,
    body-size: 10pt,
    caption-size: 9pt,
    indent: 0.75cm,
    leading: 0.55em,
  ),
  "5": (
    rank: 5,
    short: "TEKNOIF",
    name: "Jurnal TEKNOIF (Jurnal Teknologi Informasi dan Komputer)",
    institution: "Institut Teknologi Padang (ITP)",
    p-issn: "2338-2724",
    e-issn: "2598-9197",
    doi: "https://doi.org/10.21063/jtif.2026.v14.1.1-12",
    default-layout: "2col",
    gutter: 0.6cm,
    margin: (top: 3.0cm, bottom: 2.5cm, left: 3.0cm, right: 2.5cm),
    title-size: 14pt,
    author-size: 11pt,
    affil-size: 9pt,
    abs-size: 9pt,
    h1-size: 11pt,
    h2-size: 10pt,
    body-size: 10pt,
    caption-size: 9pt,
    indent: 0.75cm,
    leading: 0.55em,
  ),
  "6": (
    rank: 6,
    short: "METIK",
    name: "Jurnal METIK (Jurnal Manajemen dan Teknik Informatika)",
    institution: "LPPM STMIK Jayakarta / Universitas Mulia",
    p-issn: "2580-1503",
    e-issn: "2654-8135",
    doi: "https://doi.org/10.47002/metik.v10i1.824",
    default-layout: "1col",
    gutter: 0.6cm,
    margin: (top: 3.0cm, bottom: 2.5cm, left: 3.0cm, right: 2.5cm),
    title-size: 14pt,
    author-size: 11pt,
    affil-size: 9pt,
    abs-size: 10pt,
    h1-size: 11pt,
    h2-size: 10pt,
    body-size: 10pt,
    caption-size: 10pt,
    indent: 1.0cm,
    leading: 0.65em,
  ),
)

#let jurnal-sinta(
  sinta-level: 4,
  layout-mode: "default", // "2col" (terbagi 2) | "1col" (biasa) | "default"
  judul-id: "",
  judul-en: "",
  penulis: (),
  afiliasi: "",
  email-korespondensi: "",
  abstrak-id: [],
  kata-kunci-id: (),
  abstrak-en: [],
  kata-kunci-en: (),
  volume: "Vol. 12, No. 2, Oktober 2026",
  body,
) = {
  let key = str(sinta-level)
  let spec = if key in sinta-presets { sinta-presets.at(key) } else { sinta-presets.at("4") }
  let active-layout = if layout-mode == "default" { spec.default-layout } else { layout-mode }
  let is-two-col = active-layout == "2col"

  set document(title: judul-id, author: penulis.join(", "))
  set page(
    paper: "a4",
    margin: spec.margin,
    numbering: "1",
    header: context {
      text(size: 8pt, fill: luma(80))[
        *#spec.name (#spec.short)* | p-ISSN: #spec.p-issn, e-ISSN: #spec.e-issn #h(1fr) #volume \
        _DOI: #spec.doi _
      ]
    },
    footer: context {
      text(size: 8pt, fill: luma(100))[
        #spec.institution | Open Access CC BY-SA 4.0 #h(1fr) #counter(page).display("1")
      ]
    }
  )

  set text(font: "Times New Roman", size: spec.body-size, lang: "id")

  // Bagian Atas: 1 Kolom Penuh (Judul, Penulis, Afiliasi, Abstrak ID & EN)
  align(center)[
    #text(size: spec.title-size, weight: "bold")[
      #if spec.rank == 4 { upper(judul-id) } else { judul-id }
    ]
    #if judul-en != "" [
      \ #v(2pt)
      #text(size: spec.title-size - 2pt, style: "italic")[#judul-en]
    ]
    #v(6pt)
    #text(size: spec.author-size, weight: "bold")[#penulis.join(", ")]
    \ #v(2pt)
    #text(size: spec.affil-size)[#afiliasi]
    #if email-korespondensi != "" [
      \ #text(size: spec.affil-size)[E-mail: #email-korespondensi]
    ]
  ]

  v(6pt)
  line(length: 100%, stroke: 0.6pt + luma(120))
  v(4pt)

  block(width: 100%)[
    #set par(justify: true, leading: 0.5em, first-line-indent: 0cm)
    #set text(size: spec.abs-size)
    *ABSTRAK* - #abstrak-id
    #if kata-kunci-id.len() > 0 [
      \ *Kata Kunci*: #kata-kunci-id.join("; ")
    ]
    #if abstrak-en != [] [
      #v(4pt)
      _*ABSTRACT*_ - #emph[#abstrak-en]
      #if kata-kunci-en.len() > 0 [
        \ _*Keywords*_: #emph[#kata-kunci-en.join("; ")]
      ]
    ]
  ]

  v(4pt)
  line(length: 100%, stroke: 0.6pt + luma(120))
  v(8pt)

  // Pengaturan Heading IMRaD (1. PENDAHULUAN, 2.1. Sub-bab)
  set heading(numbering: "1.1.")
  show heading.where(level: 1): it => {
    v(8pt)
    text(size: spec.h1-size, weight: "bold")[#counter(heading).display() #upper(it.body)]
    v(4pt)
  }
  show heading.where(level: 2): it => {
    v(6pt)
    text(size: spec.h2-size, weight: "bold")[#counter(heading).display() #it.body]
    v(3pt)
  }

  set par(
    justify: true,
    leading: spec.leading,
    first-line-indent: (amount: spec.indent, all: true),
  )

  show figure.where(kind: table): set figure.caption(position: top)
  show figure.caption: it => {
    set text(size: spec.caption-size, weight: "bold")
    align(center)[#it]
  }

  // Bagian Isi: 2 Kolom (Terbagi 2) atau 1 Kolom (Biasa)
  if is-two-col {
    columns(2, gutter: spec.gutter)[#body]
  } else {
    body
  }
}
