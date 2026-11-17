#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// LEMBAR PEDOMAN PENGGUNAAN HAK CIPTA
// =============================================================================

#page(
  header: none,
  footer: context {
    let page-num = counter(page).display("i")
    align(center)[#text(size: 12pt)[#page-num]]
  }
)[
  #heading(level: 1, numbering: none, outlined: true)[Lembar Pedoman Penggunaan Hak Cipta]

  #align(center)[
    #text(size: 14pt, weight: "bold")[
      PEDOMAN PENGGUNAAN HAK CIPTA
    ]
  ]

  #v(1cm)
  Hak cipta naskah skripsi ini berada pada penulis dan #universitas. Naskah skripsi terdaftar sebagai karya ilmiah sivitas akademika #universitas, dan dilindungi oleh Undang-Undang Hak Cipta Republik Indonesia.

  Ketentuan penggunaan karya ilmiah ini diatur sebagai berikut:

  + Naskah skripsi ini tidak boleh diperbanyak, digandakan, dipublikasikan kembali, atau dialihkan ke dalam bentuk apa pun, baik sebagian maupun seluruhnya, tanpa izin tertulis dari penulis atau #universitas.
  + Pengutipan isi naskah skripsi untuk keperluan penulisan karya ilmiah, tugas akhir, atau publikasi akademis lainnya diperkenankan terbatas hanya untuk tujuan pendidikan dan non-komersial, dengan kewajiban mencantumkan sitasi dan sumber rujukan yang sah sesuai etika ilmiah.
  + Pembuatan salinan digital atau cetak hanya diperkenankan untuk keperluan studi pustaka pribadi, penelitian mandiri, atau arsip perpustakaan #universitas.
  + Pelanggaran terhadap hak cipta ini akan dikenakan sanksi perdata dan/atau pidana sesuai dengan Undang-Undang Republik Indonesia Nomor 28 Tahun 2014 tentang Hak Cipta.

  #v(1.5cm)
  #align(center)[
    Ditetapkan di: #kota\
    Pada tanggal: #if tanggal-persetujuan != none { tanggal-persetujuan } else { datetime.today().display("[day] [month repr:long] [year]") }\
    #v(0.5cm)
    *#universitas*
  ]
]
