#import "../../../lib.typ": *

= Landasan Teori

Bab ini menguraikan landasan teori yang mencakup konsep dasar bahasa pemrograman dan kerangka kerja aplikasi bergerak, metode algoritma penyelesaian masalah, teori perancangan model bisnis (*Business Model Canvas* / BMC), penelitian terkait, serta metode pengujian dan peralatan pendukung.

== Tinjauan Pustaka

=== Konsep Dasar Aplikasi
Uraikan konsep dasar arsitektur aplikasi *mobile* dan paradigma bahasa pemrograman yang digunakan dalam pembangunan aplikasi *startup*:
+ *Bahasa Pemrograman dan Framework:* Konsep dasar bahasa pemrograman (seperti Kotlin, Java, Dart/Flutter, atau TypeScript/React Native), prinsip *clean architecture*, dan pola manajemen *state*.
+ *Arsitektur Client-Server & REST API:* Mekanisme pertukaran data JSON antara aplikasi *mobile* klien dengan peladen web (*backend server*) melalui protokol HTTPS.

=== Metode Algoritma
Paparkan teori algoritma komputasi yang diimplementasikan dalam aplikasi untuk memecahkan persoalan bisnis (misalnya algoritma rekomendasi produk, kalkulasi ongkos kirim/rute terdekat, algoritma pencarian barang, atau metode klasifikasi preferensi pengguna):

#figure(
  rect(width: 80%, height: 4.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Diagram Alir / Notasi Matematika Algoritma Penyelesaian Kasus
  ],
  caption: [Alur Logika Algoritma Pemrosesan Aplikasi],
)
#sumber([Hasil Kajian Teori Algoritma, 2026])

=== Business Model Canvas (BMC)
Jelaskan konsep dasar *Business Model Canvas* (BMC) menurut Osterwalder & Pigneur sebagai alat manajemen strategis untuk menggambarkan, menilai, dan memvalidasi model bisnis baru. Uraikan 9 blok penyusun BMC:
+ *Customer Segments:* Kelompok pelanggan sasaran yang ingin dilayani.
+ *Value Propositions:* Nilai manfaat unik dan pemecahan masalah yang ditawarkan kepada pelanggan.
+ *Channels:* Saluran komunikasi, distribusi, dan penjualan untuk menyampaikan *value*.
+ *Customer Relationships:* Bentuk hubungan dan interaksi yang dibangun dengan tiap segmen pelanggan.
+ *Revenue Streams:* Sumber pendapatan yang diperoleh dari tiap segmen pelanggan.
+ *Key Resources:* Aset utama yang dibutuhkan untuk menjalankan model bisnis.
+ *Key Activities:* Aktivitas operasional terpenting yang wajib dijalankan.
+ *Key Partnerships:* Jaringan mitra dan pemasok kunci di luar organisasi.
+ *Cost Structure:* Seluruh pos pengeluaran biaya untuk mengoperasikan bisnis.

== Penelitian Terkait
Sub-bab ini menyajikan telaah terhadap minimal 5 artikel jurnal ilmiah nasional/internasional sejenis dalam 5 tahun terakhir (menggunakan format APA):

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3cm, 4cm, 3.5cm),
    stroke: 0.5pt + black,
    align: (center, left, left, left, left),
    [*No*], [*Peneliti & Tahun*], [*Judul Penelitian*], [*Model Bisnis / Metode*], [*Hasil & Diferensiasi*],
    [1], [Maulana dkk. (2023)], [Penerapan BMC Pada Startup E-Commerce Lokal], [BMC & Lean Startup], [Validasi segmen pasar UMKM terbukti efektif],
    [2], [Saputra & Firdaus (2024)], [Aplikasi Mobile Agribisnis Berbasis Android], [RUP & REST API], [Mempercepat waktu pencocokan pembeli 30%],
    [3], [Lestari (2022)], [Analisis Penerimaan Pengguna Aplikasi Startup], [Technology Acceptance Model], [Persepsi kemudahan bernilai tinggi (> 80%)],
    [4], [Ramadhan dkk. (2025)], [Model Monetisasi Freemium Platform Digital], [Freemium & Subscription], [Tingkat retensi pengguna bulanan stabil],
    [5], [Utami & Nugroho (2023)], [Pengujian Blackbox Pada Sistem E-Marketplace], [Equivalence Partitioning], [Menemukan 12 defek kritis pra-rilis],
  ),
  caption: [Matriks Sintesis Penelitian Terkait StartUp Digital],
)
#sumber([Hasil Tinjauan Pustaka Peneliti, 2026])

== Teori Pendukung

=== Pengujian Aplikasi
Jelaskan konsep pengujian fungsionalitas perangkat lunak (metode *Black Box Testing* dengan *Equivalence Partitioning* atau *Boundary Value Analysis*, serta pengujian *White Box* jika diperlukan) untuk memverifikasi keandalan aplikasi sebelum didistribusikan ke pengguna.

=== Peralatan Pendukung
Uraikan lingkungan pengembangan terpadu dan perangkat bantu perancangan yang dipakai dalam pembuatan aplikasi:
+ *Android Studio / VS Code:* Lingkungan pengembangan aplikasi mobile resmi.
+ *Firebase / Supabase:* Layanan basis data awan (*Cloud Firestore*), autentikasi pengguna, dan penyimpanan berkas.
+ *Google Play Console:* Platform pengelolaan dan distribusi rilis aplikasi resmi Google.
+ *Figma:* Perangkat bantu perancangan antarmuka pengguna (*UI/UX Design & Prototyping*).
