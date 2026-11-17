#import "../../../lib.typ": *

= Analisis dan Perancangan Aplikasi

Bab ini menyajikan tinjauan model bisnis kanvas (*Business Model Canvas* / BMC), analisis kebutuhan sistem, pemodelan diagram UML, rancangan antarmuka dan basis data, proses implementasi hingga rilis Google Play Store, spesifikasi lingkungan, pengujian fungsionalitas, serta pembagian uraian tugas anggota tim.

== Tinjauan StartUp
Jelaskan profil identitas usaha rintisan (*startup*), visi bisnis, serta penjabaran rinci dari 9 blok *Business Model Canvas* (BMC):

#figure(
  table(
    columns: (1fr, 1fr, 1.2fr, 1fr, 1fr),
    stroke: 0.5pt + black,
    align: (left, left, left, left, left),
    [*Key Partners*\
     - Komunitas mitra produsen lokal\
     - Penyedia layanan gerbang pembayaran (_Payment Gateway_)\
     - Mitra jasa logistik dan kurir pengiriman
    ],
    [*Key Activities*\
     - Pengembangan dan pemeliharaan aplikasi mobile\
     - Kurasi katalog produk dan verifikasi data transaksi\
     - Pemasaran digital dan operasional layanan pelanggan
    ],
    [*Value Propositions*\
     - Pemotongan mata rantai distribusi agar harga lebih adil\
     - Kemudahan pemesanan langsung dari gawai pintar\
     - Transparansi pelacakan status pesanan secara _real-time_
    ],
    [*Customer Relationships*\
     - Bantuan layanan obrolan langsung (_Live Chat_)\
     - Program loyalitas dan poin diskon transaksi\
     - Komunitas pengguna aktif di media sosial
    ],
    [*Customer Segments*\
     - Konsumen rumah tangga dan pelaku usaha kuliner\
     - Produsen lokal dan kelompok tani/pengrajin mandiri
    ],
    table.cell(colspan: 2)[*Key Resources*\
     - Repositori kode dan arsitektur server awan (_Cloud Server_)\
     - Hak kepemilikan merek dagang dan akun Google Play Console\
     - Tim pengembang perangkat lunak dan analis bisnis
    ],
    table.cell(colspan: 3)[*Channels*\
     - Aplikasi resmi pada Google Play Store\
     - Situs web promosi (_landing page_)\
     - Iklan bertarget di media sosial (Instagram, TikTok)
    ],
    table.cell(colspan: 2)[*Cost Structure*\
     - Biaya langganan server dan pangkalan data awan\
     - Biaya pendaftaran akun Google Play Developer\
     - Anggaran kampanye pemasaran digital dan operasional tim
    ],
    table.cell(colspan: 3)[*Revenue Streams*\
     - Komisi persentase dari setiap transaksi berhasil (_take-rate_)\
     - Biaya penempatan iklan premium produk mitra\
     - Layanan langganan fitur analitik eksklusif
    ],
  ),
  caption: [Matriks Business Model Canvas (BMC) StartUp],
)
#sumber([Hasil Perancangan Model Bisnis Tim StartUp, 2026])

== Analisis Kebutuhan

=== Analisis Kebutuhan Aplikasi
Uraikan kebutuhan fungsional aplikasi dari sudut pandang interaksi pengguna:
+ Pengguna dapat mendaftar dan masuk menggunakan akun Google atau nomor telepon.
+ Pengguna dapat menjelajahi katalog produk, melakukan pencarian dengan filter kategori, dan melihat detail produk.
+ Pengguna dapat memasukkan barang ke keranjang belanja, memilih opsi pengiriman, dan melakukan pembayaran digital.
+ Pengguna dapat melacak status pemrosesan pesanan dan memberikan ulasan/rating.

=== Rancangan Diagram Use Case
Petakan fungsionalitas aplikasi dan interaksi antar aktor (*Pelanggan*, *Mitra Produsen*, dan *Administrator*) menggunakan Use Case Diagram:

#figure(
  rect(width: 85%, height: 6cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Diagram Use Case Sistem Aplikasi StartUp
  ],
  caption: [Use Case Diagram Aplikasi StartUp],
)
#sumber([Hasil Pemodelan Sistem, 2026])

=== Rancangan Diagram Aktivitas
Gambarkan alur kerja aktivitas sistem (*Activity Diagram*) pada proses transaksi utama:

#figure(
  rect(width: 85%, height: 6cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Activity Diagram Alur Pemesanan dan Transaksi Pembayaran
  ],
  caption: [Activity Diagram Alur Transaksi Utama],
)
#sumber([Hasil Pemodelan Sistem, 2026])

=== Rancangan User Interface
Sajikan rancangan tata letak (*mockup / wireframe*) antarmuka aplikasi mobile:

#figure(
  rect(width: 90%, height: 6cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Desain Mockup Antarmuka Pengguna (Halaman Beranda, Detail Produk, Keranjang, Transaksi)
  ],
  caption: [Rancangan Antarmuka Pengguna (UI/UX Mockup)],
)
#sumber([Hasil Desain Antarmuka Figma, 2026])

=== Rancangan Database
Rancangan basis data memetakan skema penyimpanan terstruktur:
+ *Entity Relationship Diagram (ERD):* Menampilkan seluruh entitas data, atribut, kunci primer/asing, dan kardinalitas relasi.
+ *Logical Record Structure (LRS):* Struktur logis tabel relasional yang dihasilkan dari transformasi diagram relasi entitas.

#figure(
  rect(width: 85%, height: 5.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Diagram Relasi Entitas (ERD) dan Logical Record Structure (LRS)
  ],
  caption: [Diagram ERD dan LRS Basis Data],
)
#sumber([Hasil Perancangan Basis Data, 2026])

== Implementasi

=== Proses Implementasi
Uraikan langkah-langkah penulisan kode program (*coding*), konfigurasi modul otentikasi, perakitan komponen antarmuka, serta integrasi layanan *backend* (API / Firebase).

=== Hasil Implementasi
Tampilkan bukti tangkapan layar luaran aplikasi yang telah terbit dan aktif terdaftar di Google Play Store:

#figure(
  rect(width: 90%, height: 6.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Tangkapan Layar Bukti Publikasi Aplikasi Pada Halaman Google Play Store
  ],
  caption: [Tampilan Aplikasi yang Terdaftar di Google Play Store],
)
#sumber([Tangkapan Layar Google Play Console / Play Store, 2026])

== Spesifikasi Aplikasi

=== Hardware
Tabelkan spesifikasi perangkat keras workstation yang digunakan dalam pengembangan aplikasi *startup*:
+ Prosesor : Minimal Intel Core i5 / AMD Ryzen 5 generasi mutakhir.
+ Memori RAM : Minimal 16 GB DDR4/DDR5.
+ Penyimpanan : Minimal 512 GB NVMe SSD.
+ Smartphone Fisik Uji : Perangkat Android dengan RAM 4 GB (OS Android versi 11 ke atas).

=== Software
Tabelkan spesifikasi perangkat lunak lingkungan pengembang:
+ Sistem Operasi : Windows 11 64-bit / macOS Sonoma.
+ IDE & SDK : Android Studio Hedgehog / Koala dengan Android SDK Platform API 34.
+ Framework / Bahasa : Flutter SDK v3.x / Kotlin v1.9+.
+ Basis Data : Cloud Firestore / PostgreSQL v16.
+ Akun Distribusi : Akun Pengembang Resmi Google Play Developer Console.

== Pengujian Aplikasi
Pengujian aplikasi mobile dilaksanakan menggunakan metode *Black Box Testing* guna memverifikasi seluruh skenario pengujian fungsional:

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3.5cm, 3.5cm, 2cm),
    stroke: 0.5pt + black,
    align: (center, left, left, left, center),
    [*No*], [*Fitur Pengujian*], [*Skenario Aksi*], [*Hasil yang Diharapkan*], [*Status*],
    [1], [Registrasi Pengguna], [Input email valid dan password], [Akun berhasil terdaftar dan masuk verifikasi], [Valid],
    [2], [Pencarian Produk], [Ketik kata kunci nama produk], [Daftar produk terkait muncul seketika], [Valid],
    [3], [Checkout Pesanan], [Pilih alamat dan metode bayar], [Nomor tagihan terbuat dan transaksi tercatat], [Valid],
    [4], [Notifikasi Pesanan], [Status pesanan diubah oleh mitra], [Notifikasi push muncul pada bilah status ponsel], [Valid],
  ),
  caption: [Hasil Pengujian Fungsionalitas Black Box Testing],
)
#sumber([Hasil Pengujian Aplikasi Tim StartUp, 2026])

== Uraian Tugas
Skripsi *startup* dikerjakan secara kolaboratif oleh tim mahasiswa (maksimal 2 orang). Berikut pembagian peran, tanggung jawab, dan urutan pengerjaan tugas dari awal hingga akhir:

=== Project Manager / Sistem Analis
Penanggung jawab utama manajemen proyek dan analisis kebutuhan:
+ Mengidentifikasi masalah industri, memvalidasi segmen pasar, dan menyusun *Business Model Canvas* (BMC).
+ Menyusun dokumen spesifikasi kebutuhan sistem (*Software Requirements Specification*).
+ Memodelkan diagram arsitektur sistem dan diagram UML (Use Case, Activity, Sequence).
+ Mengelola jadwal rilis, koordinasi tim, serta penyusunan materi presentasi *Pitch Deck*.

=== Database Administrator / Programmer
Penanggung jawab utama rancang bangun teknis dan pengkodean perangkat lunak:
+ Merancang skema basis data konseptual dan fisik (ERD & LRS) serta aturan keamanan data.
+ Menulis kode program aplikasi mobile pada Android Studio menggunakan kerangka kerja yang dipilih.
+ Mengintegrasikan layanan API, gerbang pembayaran (*Payment Gateway*), dan notifikasi *cloud*.
+ Membangun berkas paket rilis (*Android App Bundle* / `.aab`) dan mempublikasikannya ke Google Play Console.

=== Pengujian Sistem
Tanggung jawab bersama tim dalam menjamin kualitas aplikasi:
+ Menyusun skenario pengujian *black box* dan mendokumentasikan setiap temuan cacat sistem (*bug log*).
+ Melaksanakan pengujian penerimaan pengguna (*User Acceptance Test* / UAT) melalui penyebaran kuesioner kepada target calon pelanggan.
