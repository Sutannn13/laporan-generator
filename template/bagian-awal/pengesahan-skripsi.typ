#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// LEMBAR PERSETUJUAN DAN PENGESAHAN SKRIPSI
// =============================================================================

#page(
  header: none,
  footer: context {
    let page-num = counter(page).display("i")
    align(center)[#text(size: 12pt)[#page-num]]
  }
)[
  #heading(level: 1, numbering: none, outlined: true)[Lembar Persetujuan dan Pengesahan Skripsi]

  #align(center)[
    #text(size: 14pt, weight: "bold")[
      PERSETUJUAN DAN PENGESAHAN SKRIPSI
    ]
  ]

  #v(0.6cm)
  Skripsi ini diajukan oleh:

  #v(0.2cm)
  #table(
    columns: (4cm, 0.4cm, 1fr),
    stroke: none,
    inset: (y: 3pt),
    [Nama], [:], [#penulis #if penulis-2 != none [\ #penulis-2]],
    [NIM], [:], [#nim #if nim-2 != none [\ #nim-2]],
    [Jenjang], [:], [#jenjang],
    [Program Studi], [:], [#program-studi],
    [Fakultas], [:], [#fakultas],
    [Judul Skripsi], [:], [#judul],
  )

  #v(0.3cm)
  Telah dipertahankan di hadapan Dewan Penguji dan diterima sebagai bagian persyaratan yang diperlukan untuk memperoleh gelar Sarjana Komputer (S.Kom) pada Program Studi #program-studi Fakultas #fakultas #universitas.

  #v(0.6cm)
  #align(center)[
    #let tgl = if tanggal-persetujuan != none { tanggal-persetujuan } else { kota + ", " + datetime.today().display("[day] [month repr:long] [year]") }
    #tgl\
    #text(weight: "bold")[DEWAN PENGUJI]
  ]

  #v(0.4cm)
  #table(
    columns: (1fr, 1fr),
    stroke: none,
    align: (center, center),
    [
      *Dosen Pembimbing I*\
      #v(1.8cm)
      *( #dosen-pembimbing-1 )*
    ],
    [
      *Ketua Dewan Penguji*\
      #v(1.8cm)
      *( #dosen-penguji-1 )*
    ],
    [
      *Dosen Pembimbing II*\
      #v(1.8cm)
      *( #dosen-pembimbing-2 )*
    ],
    [
      *Anggota Dewan Penguji*\
      #v(1.8cm)
      *( #dosen-penguji-2 )*
    ],
  )

  #v(0.6cm)
  #align(center)[
    Mengetahui,\
    #text(weight: "bold")[Ketua Program Studi #program-studi]\
    #v(1.8cm)
    *( #ketua-prodi )*
  ]
]
