#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// LEMBAR PERNYATAAN KEASLIAN SKRIPSI
// =============================================================================

#page(
  header: none,
  footer: context {
    let page-num = counter(page).display("i")
    align(center)[#text(size: 12pt)[#page-num]]
  }
)[
  #heading(level: 1, numbering: none, outlined: true)[Lembar Pernyataan Keaslian Skripsi]

  #align(center)[
    #text(size: 14pt, weight: "bold")[
      PERNYATAAN KEASLIAN SKRIPSI
    ]
  ]

  #v(1cm)
  Saya yang bertanda tangan di bawah ini:

  #v(0.3cm)
  #table(
    columns: (4cm, 0.4cm, 1fr),
    stroke: none,
    inset: (y: 5pt),
    [Nama Mahasiswa], [:], [#penulis #if penulis-2 != none [\ #penulis-2]],
    [NIM], [:], [#nim #if nim-2 != none [\ #nim-2]],
    [Program Studi], [:], [#program-studi],
    [Fakultas], [:], [#fakultas],
    [Jenjang], [:], [#jenjang],
  )

  #v(0.5cm)
  Dengan ini menyatakan bahwa Skripsi dengan judul:

  #align(center)[
    #text(weight: "bold")[*\"#upper(judul)\"*]
  ]

  merupakan hasil karya ilmiah asli yang saya susun sendiri, bukan merupakan tiruan, plagiarisme, atau pengutipan karya orang lain tanpa menyebutkan sumbernya secara sah dan benar sesuai etika ilmiah.

  Apabila di kemudian hari terbukti atau dapat dibuktikan bahwa skripsi ini merupakan hasil jiplakan/plagiarisme dari karya orang lain, maka saya bersedia menerima sanksi akademik berupa pencabutan gelar sarjana dan sanksi hukum lainnya sesuai dengan peraturan perundang-undangan yang berlaku di lingkungan #universitas.

  Demikian pernyataan keaslian ini dibuat dengan penuh kesadaran dan tanpa ada paksaan dari pihak mana pun.

  #v(1.5cm)
  #align(right)[
    #block(width: 7cm)[
      #set align(center)
      #let tgl = if tanggal-persetujuan != none { tanggal-persetujuan } else { kota + ", " + datetime.today().display("[day] [month repr:long] [year]") }
      #tgl\
      Yang menyatakan,\
      #v(0.8cm)
      #rect(width: 3cm, height: 1.5cm, stroke: 0.5pt + luma(120))[
        #set align(center + horizon)
        #text(size: 8pt, fill: luma(80))[Materai\ Rp 10.000]
      ]
      #v(0.3cm)
      #text(weight: "bold")[*( #penulis )*]\
      NIM: #nim
    ]
  ]
]
