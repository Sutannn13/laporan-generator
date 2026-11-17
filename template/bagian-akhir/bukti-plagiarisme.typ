#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// BUKTI HASIL PENGECEKAN PLAGIARISME
// =============================================================================

#heading(level: 1, numbering: none, outlined: true)[Bukti Hasil Pengecekan Plagiarisme]

#v(1cm)
Berikut dilampirkan bukti hasil pengecekan orisinalitas dan tingkat kemiripan (_similarity index_) naskah skripsi menggunakan perangkat lunak resmi pendeteksi plagiarisme (*Turnitin*) yang difasilitasi oleh #universitas:

#v(0.5cm)
#table(
  columns: (4cm, 0.4cm, 1fr),
  stroke: none,
  inset: (y: 4pt),
  [Nama Mahasiswa], [:], [#penulis],
  [NIM], [:], [#nim],
  [Program Studi], [:], [#program-studi],
  [Judul Skripsi], [:], [#judul],
  [Tingkat Kemiripan], [:], [#text(weight: "bold")[#tingkat-kemiripan-plagiarisme] (Batas Maksimal: 25%)],
  [Tanggal Pengecekan], [:], [#tanggal-cek-plagiarisme],
)

#v(1cm)
#if file-bukti-plagiarisme != none [
  #align(center)[
    #image(file-bukti-plagiarisme, width: 85%)
  ]
] else [
  #rect(width: 100%, height: 11cm, stroke: (paint: luma(120), thickness: 1pt, dash: "dashed"))[
    #set align(center + horizon)
    #text(fill: luma(100))[
      Tempelkan berkas tangkapan layar / dokumen pindaian (*Scan / PDF*) hasil uji Turnitin di sini.\
      \
      Atur variabel `#file-bukti-plagiarisme = "gambar/scan-turnitin.png"` pada berkas `template/metadata.typ`.
    ]
  ]
]
