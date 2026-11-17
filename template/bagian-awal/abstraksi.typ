#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// ABSTRAKSI (BAHASA INDONESIA & BAHASA INGGRIS)
// =============================================================================

#page(
  header: none,
  footer: context {
    let page-num = counter(page).display("i")
    align(center)[#text(size: 12pt)[#page-num]]
  }
)[
  #heading(level: 1, numbering: none, outlined: true)[Abstraksi]

  #align(center)[
    #text(size: 14pt, weight: "bold")[ABSTRAK]
  ]

  #v(0.6cm)
  #set par(leading: 6pt, first-line-indent: 0cm, justify: true) // Spasi 1 untuk abstrak
  #text(weight: "bold")[
    #penulis (#nim), "#upper(judul)".
  ]

  #v(0.4cm)
  #abstrak-id

  #v(0.5cm)
  #text(weight: "bold")[Kata Kunci: #kata-kunci-id]

  #v(1.2cm)
  #line(length: 100%, stroke: 0.5pt + luma(150))
  #v(0.8cm)

  #align(center)[
    #text(size: 14pt, weight: "bold")[ABSTRACT]
  ]

  #v(0.6cm)
  #set text(style: "italic")
  #text(weight: "bold")[
    #penulis (#nim), "#upper(judul)".
  ]

  #v(0.4cm)
  #abstrak-en

  #v(0.5cm)
  #text(weight: "bold", style: "normal")[Keywords: #text(style: "italic")[#kata-kunci-en]]
]
