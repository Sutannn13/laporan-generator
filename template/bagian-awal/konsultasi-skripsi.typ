#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// LEMBAR KONSULTASI SKRIPSI (KARTU BIMBINGAN)
// =============================================================================

#page(
  header: none,
  footer: context {
    let page-num = counter(page).display("i")
    align(center)[#text(size: 12pt)[#page-num]]
  }
)[
  #heading(level: 1, numbering: none, outlined: true)[Lembar Konsultasi Skripsi]

  #align(center)[
    #text(size: 14pt, weight: "bold")[
      LEMBAR KONSULTASI SKRIPSI\
      #upper(universitas)
    ]
  ]

  #v(0.6cm)
  #table(
    columns: (4cm, 0.4cm, 1fr),
    stroke: none,
    inset: (y: 3pt),
    [NIM], [:], [#nim #if nim-2 != none [\ #nim-2]],
    [Nama Lengkap], [:], [#penulis #if penulis-2 != none [\ #penulis-2]],
    [Dosen Pembimbing I], [:], [#dosen-pembimbing-1],
    [Dosen Pembimbing II], [:], [#dosen-pembimbing-2],
    [Judul Skripsi], [:], [#judul],
  )

  #v(0.4cm)
  #table(
    columns: (0.8cm, 2.5cm, 1fr, 2.5cm),
    stroke: 0.5pt + black,
    align: (center, center, left, center),
    [*No*], [*Tanggal*], [*Pokok Bahasan / Catatan Dosen*], [*Paraf Pembimbing*],
    [1], [15/09/2026], [Pengajuan judul dan perumusan masalah penelitian], [],
    [2], [22/09/2026], [Revisi BAB I (Latar belakang & identifikasi masalah)], [],
    [3], [06/10/2026], [Bimbingan BAB II (Landasan teori & penelitian terkait)], [],
    [4], [20/10/2026], [Bimbingan BAB III (Analisis masalah & rancangan algoritma)], [],
    [5], [03/11/2026], [Bimbingan BAB IV (Desain basis data & code generation)], [],
    [6], [17/11/2026], [Bimbingan BAB IV (Testing) & BAB V (Kesimpulan/Saran)], [],
    [7], [24/11/2026], [Review kelengkapan draf skripsi & persetujuan sidang], [],
    [8], [01/12/2026], [Persetujuan akhir naskah skripsi siap diujikan], [],
  )

  #v(0.6cm)
  #align(center)[
    #let tgl = if tanggal-persetujuan != none { tanggal-persetujuan } else { kota + ", " + datetime.today().display("[day] [month repr:long] [year]") }
    #tgl\
    Menyetujui,\
    #text(weight: "bold")[Dosen Pembimbing I]\
    #v(1.8cm)
    *( #dosen-pembimbing-1 )*
  ]
]
