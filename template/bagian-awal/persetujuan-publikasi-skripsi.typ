#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// LEMBAR PERNYATAAN PERSETUJUAN PUBLIKASI KARYA ILMIAH
// =============================================================================

#page(
  header: none,
  footer: context {
    let page-num = counter(page).display("i")
    align(center)[#text(size: 12pt)[#page-num]]
  }
)[
  #heading(level: 1, numbering: none, outlined: true)[Lembar Pernyataan Persetujuan Publikasi Karya Ilmiah]

  #align(center)[
    #text(size: 14pt, weight: "bold")[
      PERNYATAAN PERSETUJUAN PUBLIKASI KARYA ILMIAH\
      UNTUK KEPENTINGAN AKADEMIS
    ]
  ]

  #v(0.8cm)
  Sebagai sivitas akademika #universitas, saya yang bertanda tangan di bawah ini:

  #v(0.3cm)
  #table(
    columns: (4cm, 0.4cm, 1fr),
    stroke: none,
    inset: (y: 4pt),
    [Nama Mahasiswa], [:], [#penulis #if penulis-2 != none [\ #penulis-2]],
    [NIM], [:], [#nim #if nim-2 != none [\ #nim-2]],
    [Program Studi], [:], [#program-studi],
    [Fakultas], [:], [#fakultas],
    [Jenis Karya], [:], [Skripsi / Tugas Akhir],
  )

  #v(0.4cm)
  Demi pengembangan ilmu pengetahuan, menyetujui untuk memberikan kepada #universitas *Hak Bebas Royalti Non-Eksklusif (_Non-Exclusive Royalty-Free Right_)* atas karya ilmiah saya yang berjudul:

  #align(center)[
    #text(weight: "bold")[*\"#upper(judul)\"*]
  ]

  beserta perangkat yang ada (jika diperlukan). Dengan Hak Bebas Royalti Non-Eksklusif ini, #universitas berhak menyimpan, mengalihmedia/formatkan, mengelola dalam bentuk pangkalan data (_database_), merawat, dan mempublikasikan tugas akhir saya di repositori institusi selama tetap mencantumkan nama saya sebagai penulis/pencipta dan sebagai pemilik Hak Cipta.

  Demikian pernyataan ini saya buat dengan sebenarnya.

  #v(1.2cm)
  #align(right)[
    #block(width: 7cm)[
      #set align(center)
      #let tgl = if tanggal-persetujuan != none { tanggal-persetujuan } else { kota + ", " + datetime.today().display("[day] [month repr:long] [year]") }
      #tgl\
      Yang menyatakan,\
      #v(2cm)
      #text(weight: "bold")[*( #penulis )*]\
      NIM: #nim
    ]
  ]
]
