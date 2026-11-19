#import "../../../lib.typ": *

= Pembahasan

== Tinjauan Institusi
=== Sejarah Dinas Komunikasi dan Informatika Kota Contoh
Dinas Komunikasi dan Informatika (Diskominfo) Kota Contoh merupakan perangkat daerah yang dibentuk berdasarkan Peraturan Daerah Kota Contoh tentang Pembentukan dan Susunan Perangkat Daerah untuk menyelenggarakan urusan pemerintahan bidang komunikasi dan informatika, statistik sektoral, serta persandian. Instansi ini berkedudukan di Jalan Raya Pemerintahan Nomor 1, Kota Contoh, dan bertanggung jawab langsung kepada Wali Kota Contoh melalui Sekretaris Daerah.

Sebagai pengelola layanan informasi publik daerah, Diskominfo Kota Contoh mengoordinasikan diseminasi informasi pembangunan, pengelolaan portal web resmi pemerintah daerah, layanan Pejabat Pengelola Informasi dan Dokumentasi (PPID), serta pengembangan infrastruktur aplikasi pemerintahan berbasis elektronik (SPBE) di seluruh wilayah kecamatan Kota Contoh.

=== Visi dan Misi Dinas Komunikasi dan Informatika Kota Contoh
Visi dan misi Diskominfo Kota Contoh dirumuskan untuk mendukung terwujudnya tata kelola pemerintahan daerah yang transparan dan berbasis digital:

*Visi*:
Terwujudnya pelayanan informasi publik dan infrastruktur digital Kota Contoh yang transparan, terpadu, akuntabel, dan responsif bagi masyarakat.

*Misi*:
1. Meningkatkan kualitas diseminasi informasi publik dan komunikasi pemerintahan daerah secara cepat dan akurat.
2. Mengembangkan infrastruktur teknologi informasi dan aplikasi layanan pemerintahan berbasis elektronik yang terintegrasi.
3. Memperkuat tata kelola keamanan informasi, statistik sektoral, dan keterbukaan data publik daerah.
4. Meningkatkan literasi digital dan partisipasi masyarakat dalam pengawasan layanan publik.

=== Struktur Organisasi dan Fungsi Bagian Humas
Struktur organisasi Dinas Komunikasi dan Informatika Kota Contoh dipimpin oleh seorang Kepala Dinas yang membawahi unit-unit kerja berikut:
1. Sekretariat Dinas (Subbagian Umum dan Kepegawaian; Subbagian Keuangan dan Perencanaan)
2. Bidang Pengelolaan Informasi dan Komunikasi Publik (Humas)
3. Bidang Infrastruktur dan Aplikasi Informatika
4. Bidang Layanan E-Government
5. Bidang Statistik dan Persandian
6. Kelompok Jabatan Fungsional (Pranata Humas dan Pranata Komputer)

#figure(
  image("../../gambar/gambar_3_1_struktur_organisasi.png", width: 95%),
  caption: [Struktur Organisasi Dinas Komunikasi dan Informatika Kota Contoh],
)
#sumber([Dinas Komunikasi dan Informatika Kota Contoh, 2026])

Bidang Pengelolaan Informasi dan Komunikasi Publik (Humas) bertugas melaksanakan peliputan agenda kedinasan, dokumentasi visual, penyusunan siaran pers (_press release_), pengelolaan konten portal web resmi, serta penyebarluasan informasi publik melalui kanal media sosial resmi pemerintah daerah.

== Analisis Sistem Berjalan
Analisis sistem berjalan bertujuan untuk membedah secara komprehensif alur proses kerja pengelolaan publikasi berita dan siaran pers yang saat ini diterapkan pada Bagian Humas Dinas Komunikasi dan Informatika Kota Contoh. Analisis ini mencakup uraian prosedur operasional, identifikasi bentuk dokumen masukan dan keluaran, serta pemodelan sistem menggunakan _Unified Modelling Language_ (UML) berupa _Use Case Diagram_ dan _Activity Diagram_.

=== Prosedur Sistem Berjalan
Proses pengelolaan publikasi berita pada Bagian Humas Dinas Komunikasi dan Informatika Kota Contoh melibatkan beberapa tahapan yang saling terhubung, dimulai dari peliputan lapangan hingga tahap pengarsipan. Rincian prosedur operasional sistem berjalan adalah sebagai berikut:

1. *Prosedur Peliputan dan Pengumpulan Data Kegiatan*
  Staf Humas menerima jadwal agenda kedinasan dari pimpinan atau panitia pelaksana kegiatan (seperti Bidang Pelayanan Publik, Infrastruktur Digital, atau Kecamatan). Staf Humas kemudian mendatangi lokasi acara untuk melakukan peliputan langsung. Pada tahap ini, staf mengumpulkan data fakta lapangan berpedoman pada kaidah 5W+1H (_What, Who, Where, When, Why, How_), mencatat poin inti pidato/sambutan narasumber, dan mengambil dokumentasi visual berupa foto kegiatan menggunakan kamera digital atau telepon pintar kedinasan.

2. *Prosedur Penyusunan Draf Naskah Berita (_Press Release_)*
  Setelah kegiatan selesai, staf Humas kembali ke ruang kerja untuk memproses hasil liputan. Staf membuka aplikasi pengolah kata Microsoft Word di komputer kerja dan menyusun draf berita secara manual dari awal. Staf merangkai kalimat judul, pembuka, tubuh berita, dan kutipan narasumber secara mandiri. Karena belum tersedianya format templat terotomatisasi, proses penyusunan draf berita ini membutuhkan waktu sekitar 1 hingga 2 jam untuk setiap berita dan sangat bergantung pada gaya penulisan masing-masing staf.

3. *Prosedur Pengajuan dan Verifikasi Naskah Berita*
  Draf naskah berita yang telah selesai disusun dalam format file dokumen Microsoft Word (`.docx`) atau salinan teks ringkas selanjutnya dikirimkan oleh staf Humas kepada Pimpinan (Kepala Bidang Pengelolaan Informasi Publik atau Pranata Humas) melalui aplikasi pesan instan WhatsApp. Pemilihan media komunikasi WhatsApp dilakukan dengan alasan kepraktisan dan mobilitas pimpinan yang kerap berada di luar kantor untuk tugas dinas.

4. *Prosedur Koreksi dan Persetujuan (_Approval_) Naskah*
  Pimpinan menerima dan membaca draf naskah berita yang dikirimkan melalui WhatsApp. Pada tahapan ini terdapat dua kemungkinan:
  a. Apabila naskah dinilai belum sesuai, terdapat kekeliruan data, atau penggunaan redaksi yang kurang tepat, pimpinan memberikan arahan dan catatan revisi melalui pesan balasan WhatsApp. Staf Humas kemudian membuka kembali file draf berita di komputer, melakukan perbaikan sesuai catatan, dan mengirimkan kembali hasil revisi kepada pimpinan.
  b. Apabila naskah dinilai telah akurat, berimbang, dan memenuhi standar etika publikasi kedinasan, pimpinan memberikan persetujuan resmi (_approval_ / ACC) berupa pesan konfirmasi tertulis via WhatsApp.

5. *Prosedur Publikasi Berita*
  Setelah memperoleh persetujuan resmi, staf Humas segera menyiapkan berkas publikasi untuk disebarluaskan ke kanal komunikasi instansi:
  a. *Publikasi Portal Website*: Staf melakukan proses masuk (_login_) ke sistem manajemen konten (_Content Management System_ / CMS) portal resmi Diskominfo Kota Contoh (`portal.kotacontoh.go.id`). Naskah berita disalin ke editor artikel web, foto kegiatan diunggah dan disematkan, kemudian artikel diterbitkan (_publish_).
  b. *Publikasi Media Sosial*: Staf merangkum inti naskah berita menjadi teks takarir (_caption_) media sosial dan memadukannya dengan materi visual (infografis atau foto pilihan), lalu mengunggahnya pada akun resmi Instagram Dinas Komunikasi dan Informatika Kota Contoh (`@humas_kotacontoh`).

6. *Prosedur Pengarsipan Berita dan Dokumentasi*
  Setelah proses publikasi selesai, staf Humas mengarsipkan dokumen naskah final berformat `.docx` beserta foto-foto kegiatan ke dalam folder penyimpanan lokal komputer kerja staf atau repositori Google Drive pribadi staf. Pengarsipan ini dilakukan sebagai rekam jejak publikasi internal Humas.

=== Spesifikasi Bentuk Dokumen Sistem Berjalan
Spesifikasi bentuk dokumen menguraikan seluruh berkas administratif yang mengalir pada sistem berjalan, baik dokumen yang berperan sebagai masukan (_input_) maupun keluaran (_output_) proses kerja publikasi Humas Diskominfo Kota Contoh.

==== Dokumen Masukan (_Input_)
Dokumen masukan merupakan data awal yang digunakan oleh staf Humas sebagai bahan dasar perumusan berita publikasi. Rincian dokumen masukan adalah sebagai berikut:

1. *Lembar Catatan Peliputan (Notula Lapangan)*
  - Nama Dokumen : Lembar Catatan Peliputan Lapangan
  - Fungsi : Sebagai rekaman data fakta mentah 5W+1H, kronologi acara, dan kutipan sambutan pejabat/narasumber
  - Sumber : Panitia Pelaksana / Narasumber Kegiatan Diskominfo Kota Contoh
  - Tujuan : Staf Humas (Penulis Berita)
  - Media : Kertas fisik / Catatan digital (_smartphone_)
  - Jumlah : 1 (satu) berkas per agenda
  - Frekuensi : Setiap kali kegiatan kedinasan diliput
  - Format : Teks catatan bebas berpedoman unsur 5W+1H

2. *Foto Dokumentasi Acara*
  - Nama Dokumen : Berkas Foto Dokumentasi Kegiatan
  - Fungsi : Sebagai bukti visual kegiatan dan materi pendukung publikasi berita
  - Sumber : Kamera / Telepon Pintar Staf Dokumentasi Humas
  - Tujuan : Staf Humas & Media Publikasi
  - Media : Berkas elektronik (format JPEG/PNG)
  - Jumlah : 5 sampai dengan 20 foto per kegiatan
  - Frekuensi : Setiap pelaksanaan agenda kegiatan
  - Format : Gambar digital beresolusi tinggi

Rekapitulasi karakteristik dokumen masukan sistem berjalan disajikan pada Tabel III.1 berikut:

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3.8cm, 2.5cm, 2.3cm, 2cm),
    inset: (x: 5pt, y: 6pt),
    align: (center + horizon, left + horizon, left + horizon, left + horizon, center + horizon, left + horizon),
    [*No.*], [*Nama Dokumen*], [*Fungsi*], [*Sumber*], [*Media*], [*Jumlah*],
    [1.], [Lembar Catatan Peliputan Lapangan], [Sumber fakta mentah 5W+1H dan kutipan narasumber], [Narasumber / Panitia Kegiatan], [Kertas / Catatan Digital], [1 berkas per acara],
    [2.], [Foto Dokumentasi Acara], [Bukti visual kegiatan dan lampiran rilis publikasi], [Staf Liputan Humas], [File Elektronik (JPEG/PNG)], [5--20 foto per acara],
  ),
  caption: [Spesifikasi Dokumen Masukan Sistem Berjalan],
)
#sumber([Bagian Humas Diskominfo Kota Contoh, 2026])

==== Dokumen Keluaran (_Output_)
Dokumen keluaran merupakan hasil olahan data peliputan yang diproduksi oleh Bagian Humas Diskominfo Kota Contoh untuk disebarkan kepada pimpinan maupun masyarakat umum. Rincian dokumen keluaran adalah sebagai berikut:

1. *Draf Naskah Berita (_Press Release_)*
  - Nama Dokumen : Draf Siaran Pers / Naskah Berita
  - Fungsi : Naskah formal berisi uraian berita lengkap yang diajukan untuk proses verifikasi dan persetujuan
  - Sumber : Staf Humas
  - Tujuan : Kepala Bidang Pengelolaan Informasi Publik / Pimpinan Diskominfo Kota Contoh
  - Media : Berkas elektronik Microsoft Word (`.docx`) dikirimkan via WhatsApp
  - Jumlah : 1 (satu) berkas
  - Frekuensi : Setiap selesai kegiatan peliputan
  - Format : Naskah ketikan Word berstruktur judul, _dateline_, tubuh berita, dan penutup

2. *Artikel Berita Portal Website Resmi*
  - Nama Dokumen : Artikel Publikasi Website Diskominfo Kota Contoh
  - Fungsi : Menyebarluaskan berita resmi program dan kebijakan Diskominfo Kota Contoh ke publik luas
  - Sumber : Staf Humas / Administrator Web
  - Tujuan : Masyarakat umum, aparatur sipil negara (ASN), dan insan media massa
  - Media : Halaman web daring (_online_) pada portal `portal.kotacontoh.go.id`
  - Jumlah : 1 (satu) tautan artikel per rilis
  - Frekuensi : Setiap rilis berita yang telah disetujui pimpinan
  - Format : Teks berbasis HTML disertai foto utama

3. *Materi Publikasi Media Sosial (Instagram)*
  - Nama Dokumen : Konten Publikasi Media Sosial Resmi
  - Fungsi : Memberikan informasi ringkas dan visual yang menarik kepada pengguna media sosial
  - Sumber : Staf Humas / Pengelola Media Sosial
  - Tujuan : Pengikut (_followers_) akun Instagram dan publik pengguna media sosial
  - Media : Aplikasi Instagram (`@humas_kotacontoh`)
  - Jumlah : 1 (satu) unggahan (_post/carousel_)
  - Frekuensi : Bersamaan atau sesaat setelah publikasi di portal website
  - Format : Gambar grafis/foto digital disertai teks keterangan (_caption_)

Rekapitulasi karakteristik dokumen keluaran sistem berjalan disajikan pada Tabel III.2 berikut:

#figure(
  table(
    columns: (0.8cm, 3.2cm, 3.8cm, 2.3cm, 2.4cm, 2.5cm),
    inset: (x: 5pt, y: 6pt),
    align: (center + horizon, left + horizon, left + horizon, left + horizon, center + horizon, left + horizon),
    [*No.*], [*Nama Dokumen*], [*Fungsi*], [*Sumber*], [*Media*], [*Tujuan*],
    [1.], [Draf Naskah Berita (_Press Release_)], [Materi naskah berita untuk proses penelaahan dan persetujuan], [Staf Humas], [File Word (`.docx`) / WhatsApp], [Kepala Bidang / Pimpinan],
    [2.], [Artikel Berita Portal Website], [Informasi berita resmi instansi bagi masyarakat dan media], [Staf Humas (Admin Web)], [Halaman Web (`portal.kotacontoh.go.id`)], [Masyarakat / Publik],
    [3.], [Konten Media Sosial (Instagram)], [Publikasi ringkas grafis dan teks untuk pengguna jejaring sosial], [Staf Humas (Admin Medsos)], [Akun Instagram (`@humas_kotacontoh`)], [Warganet / Publik],
  ),
  caption: [Spesifikasi Dokumen Keluaran Sistem Berjalan],
)
#sumber([Bagian Humas Diskominfo Kota Contoh, 2026])

=== Use Case Diagram Sistem Berjalan
_Use Case Diagram_ digunakan untuk memodelkan fungsionalitas sistem berjalan dengan memetakan interaksi antara aktor (pengguna) dengan proses-proses yang berlangsung pada tata kelola publikasi berita Bagian Humas Diskominfo Kota Contoh.

==== Deskripsi Aktor Sistem Berjalan
Aktor yang terlibat dalam sistem pengelolaan publikasi berita berjalan beserta perannya diuraikan pada Tabel III.3 berikut:

#figure(
  table(
    columns: (0.8cm, 3.5cm, 10.5cm),
    inset: (x: 6pt, y: 7pt),
    align: (center + horizon, left + horizon, left + horizon),
    [*No.*], [*Aktor*], [*Deskripsi Peran dan Tanggung Jawab*],
    [1.], [Staf Humas], [Petugas pelaksana yang bertugas melakukan peliputan kegiatan di lapangan, menyusun draf naskah berita di Microsoft Word, mengajukan naskah ke pimpinan via WhatsApp, melakukan revisi perbaikan, menerbitkan berita ke portal web dan media sosial, serta mengarsipkan dokumen.],
    [2.], [Pimpinan (Kepala Bidang)], [Pejabat struktural yang bertindak sebagai verifikator materi publikasi, bertugas menerima draf berita dari staf via WhatsApp, menelaah kebenaran informasi dan etika redaksional, memberikan catatan revisi, serta memberikan persetujuan (_approval_) publikasi.],
    [3.], [Masyarakat / Publik], [Pihak eksternal sebagai penerima informasi yang mengakses, membaca, dan memperoleh wawasan program kedinasan melalui portal website resmi maupun kanal media sosial Diskominfo Kota Contoh.],
  ),
  caption: [Deskripsi Aktor Sistem Berjalan],
)
#sumber([Hasil Analisis Sistem Berjalan, 2026])

==== Deskripsi Use Case Sistem Berjalan
Daftar _use case_ fungsional pada sistem berjalan diuraikan pada Tabel III.4 berikut:

#figure(
  table(
    columns: (0.8cm, 4.2cm, 9.8cm),
    inset: (x: 6pt, y: 6pt),
    align: (center + horizon, left + horizon, left + horizon),
    [*No.*], [*Nama Use Case*], [*Deskripsi Fungsionalitas*],
    [1.], [Meliput Agenda Kegiatan], [Staf Humas mendatangi lokasi acara, mencatat poin fakta 5W+1H, dan mengambil dokumentasi foto visual.],
    [2.], [Menyusun Draf Berita (Word)], [Staf Humas mengetik naskah draf siaran pers secara manual menggunakan aplikasi pengolah kata Microsoft Word.],
    [3.], [Mengirimkan Draf via WhatsApp], [Staf Humas mengirimkan berkas draf naskah berita kepada pimpinan melalui pesan instan WhatsApp.],
    [4.], [Menelaah Draf Berita], [Pimpinan membaca dan memeriksa kelayakan draf berita yang diajukan.],
    [5.], [Memberikan Catatan Revisi], [Pimpinan mengirimkan instruksi koreksi redaksi melalui WhatsApp jika naskah belum memenuhi standar.],
    [6.], [Memperbaiki Draf Berita], [Staf Humas membuka kembali berkas draf dan melakukan revisi sesuai catatan pimpinan.],
    [7.], [Menyetujui Naskah (_Approval_)], [Pimpinan memberikan konfirmasi persetujuan resmi publikasi melalui pesan WhatsApp.],
    [8.], [Menerbitkan Berita ke Website], [Staf Humas mengunggah naskah berita final dan foto kegiatan ke CMS portal resmi Diskominfo Kota Contoh.],
    [9.], [Mengunggah Konten ke Instagram], [Staf Humas menyusun takarir ringkas dan mengunggah materi visual ke akun media sosial Instagram Diskominfo Kota Contoh.],
    [10.], [Mengarsipkan Dokumen Berita], [Staf Humas menyimpan file naskah Word dan foto ke media penyimpanan lokal komputer staf.],
    [11.], [Membaca Informasi Publikasi], [Masyarakat mengakses dan membaca berita melalui website dan media sosial.],
  ),
  caption: [Deskripsi Use Case Sistem Berjalan],
)
#sumber([Hasil Analisis Sistem Berjalan, 2026])

==== Diagram Use Case Sistem Berjalan
Visualisasi keterhubungan aktor dan use case pada sistem berjalan dimodelkan pada Gambar III.2 berikut:

#figure(
  image("../../gambar/gambar_3_2_use_case_berjalan.png", width: 95%),
  caption: [Use Case Diagram Sistem Pengelolaan Publikasi Berita Berjalan],
)
#sumber([Hasil Analisis Sistem Berjalan, 2026])

=== Activity Diagram Sistem Berjalan
_Activity Diagram_ memodelkan dinamika aliran aktivitas operasional (_workflow_) sistem berjalan secara berurutan antar-entitas yang berinteraksi.

==== Skenario Aktivitas Sistem Berjalan
Runtutan aktivitas pada sistem berjalan dipaparkan pada Tabel III.5 berikut:

#figure(
  table(
    columns: (0.8cm, 3.2cm, 3.5cm, 7.3cm),
    inset: (x: 5pt, y: 6pt),
    align: (center + horizon, left + horizon, left + horizon, left + horizon),
    [*No.*], [*Entitas Asal*], [*Aktivitas Operasional*], [*Keluaran / Tindak Lanjut*],
    [1.], [Staf Humas], [Meliput kegiatan kedinasan], [Tercatat data 5W+1H dan terkumpul dokumentasi foto],
    [2.], [Staf Humas], [Menyusun draf naskah berita di MS Word], [File draf naskah berita (`.docx`) selesai diketik manual],
    [3.], [Staf Humas], [Mengirimkan draf berita via WhatsApp], [Berkas naskah terkirim ke kontak pimpinan],
    [4.], [Pimpinan], [Menerima dan menelaah naskah berita], [Pengambilan keputusan kelayakan naskah (_Decision_)],
    [5.], [Pimpinan], [Pemeriksaan: Apakah naskah disetujui?], [Jika *Tidak*: Mengirim catatan revisi via chat WhatsApp\ Jika *Ya*: Mengirim konfirmasi persetujuan (ACC)],
    [6.], [Staf Humas], [Merespons hasil telaah pimpinan], [Jika ada revisi: Membuka Word, merevisi, dan mengirim ulang\ Jika disetujui: Mempersiapkan materi publikasi],
    [7.], [Staf Humas], [Menerbitkan berita ke website dan medsos], [Artikel tayang di web resmi dan postingan tayang di Instagram],
    [8.], [Staf Humas], [Menyimpan file naskah dan foto kegiatan], [Berkas tersimpan di direktori penyimpanan lokal (Selesai)],
  ),
  caption: [Skenario Aliran Kerja (_Workflow_) Sistem Berjalan],
)
#sumber([Hasil Analisis Sistem Berjalan, 2026])

==== Diagram Aktivitas Sistem Berjalan
Visualisasi pemodelan aliran kerja dengan pembagian lajur tanggung jawab (_swimlane_) disajikan pada Gambar III.3 berikut:

#figure(
  image("../../gambar/gambar_3_3_activity_diagram_berjalan.png", width: 95%),
  caption: [Activity Diagram Sistem Pengelolaan Publikasi Berita Berjalan],
)
#sumber([Hasil Analisis Sistem Berjalan, 2026])

== Permasalahan Pokok
Berdasarkan analisis terhadap prosedur operasional sistem berjalan, penulis mengidentifikasi beberapa titik kendala dan kelemahan utama pada tata kelola publikasi berita di Bagian Humas Dinas Komunikasi dan Informatika Kota Contoh:

=== Kendala pada Proses Penyusunan Naskah Berita
Penyusunan naskah rilis pers dari data mentah lapangan masih dikerjakan secara manual dari awal menggunakan Microsoft Word. Proses ini memakan waktu yang cukup lama (1 hingga 2 jam per berita), sehingga seringkali menyebabkan keterlambatan penayangan berita di portal resmi. Selain itu, gaya penulisan dan struktur berita menjadi sangat bervariasi bergantung pada staf yang bertugas, yang berpotensi memicu inkonsistensi kaidah jurnalistik kedinasan.

=== Kendala pada Proses Verifikasi dan Persetujuan
Proses pengajuan verifikasi dan persetujuan yang bertumpu pada aplikasi pesan instan WhatsApp memiliki berbagai risiko operasional. Dokumen naskah berita rawan tertimbun oleh pesan dinas lainnya, penelusuran riwayat revisi (_version tracking_) menjadi sulit dilakukan, serta tidak adanya kepastian durasi penelaahan yang menyebabkan terhambatnya proses publikasi.

=== Kendala pada Proses Pengarsipan Dokumen
Pengarsipan naskah berita dan dokumentasi foto yang hanya tersimpan di media penyimpanan lokal laptop staf atau akun pribadi menyebabkan dokumen rawan hilang, rusak akibat infeksi virus, atau sulit diakses kembali saat dibutuhkan oleh staf lain untuk laporan pertanggungjawaban kedinasan.

== Pemecahan Masalah
Berdasarkan analisis mendalam terhadap ketiga titik kendala pokok sistem berjalan di Bagian Humas Dinas Komunikasi dan Informatika Kota Contoh, penulis merumuskan alternatif pemecahan masalah dengan merancang dan mengimplementasikan sistem otomasi rilis berita berbasis web, yaitu *Aplikasi Press Release Auto-Generator* (dapat diakses pada tautan resmi: `https://press-release-kotacontoh.contoh.go.id/`).

Sistem usulan ini dirancang secara khusus untuk mentransformasi tata kelola produksi siaran pers kedinasan dari pendekatan konvensional yang memakan waktu 1 hingga 2 jam (45–90 menit) menjadi sistem otomasi terintegrasi yang mampu memproses berkas rilis dalam waktu kurang dari 5 hingga 10 menit. Melalui pendekatan rekayasa piranti lunak modern, sistem mengombinasikan antarmuka formulir interaktif 3-langkah (_stepper wizard_), modul formula fakta inti 5W+1H dengan pemantauan kelengkapan waktu nyata (_real-time checklist badges_), pemodelan input dinamis kontekstual berdasarkan 6 jenis kegiatan kedinasan, integrasi model kecerdasan buatan Google Gemini dengan rekayasa _prompt_ berstandar jurnalistik kehumasan pemerintah, modul audit kutipan narasumber (_quote review_) guna mencegah distorsi makna dan halusinasi data (*zero hallucination*), gerbang validasi integritas faktual (*factual gatekeeper*), hingga ekspor otomatis ke format dokumen Microsoft Word (`.docx`) ber-kop dinas resmi Dinas Komunikasi dan Informatika Kota Contoh serta takarir media sosial Instagram.

=== Usulan Prosedur Sistem
Prosedur sistem usulan mencakup penyempurnaan alur kerja operasional publikasi berita kehumasan yang terintegrasi ke dalam lima tahapan utama:

1. *Prosedur Penginputan Data Kegiatan dan Parameter 5W+1H Terstruktur*:
   Staf Humas yang telah selesai melaksanakan peliputan agenda kedinasan (seperti sosialisasi keterbukaan informasi publik, bimbingan teknis layanan digital, rapat koordinasi perangkat daerah, maupun peringatan hari besar nasional) mengakses sistem melalui peramban web pada domain `https://press-release-kotacontoh.contoh.go.id/`. Staf diarahkan pada antarmuka alur 3-langkah (*stepper wizard*):
   - *Formula Fakta Inti 5W+1H*: Staf dipandu oleh 6 kartu status interaktif (*What*, *Who*, *Where*, *When*, *Why*, dan *How*). Sistem menerapkan prinsip ketat di mana kecerdasan buatan tidak diizinkan menebak data yang kosong, sehingga seluruh fakta dasar wajib diinput secara valid.
   - *Klasifikasi Jenis Kegiatan dan Input Kontekstual*: Sistem menyediakan 6 pilihan kategori agenda kedinasan, yaitu: (1) Bimbingan / sosialisasi / seminar; (2) Lomba / perayaan; (3) Upacara / ziarah / peringatan; (4) Pelayanan / bakti sosial / kebersihan; (5) Rapat / kunjungan / koordinasi; serta (6) Kegiatan lainnya. Pemilihan kategori ini secara dinamis memicu kemunculan kolom input kontekstual (seperti nama pemateri dan poin materi faktual untuk bimbingan, cabang lomba dan nama pemenang resmi untuk lomba, urutan prosesi dan makna peringatan untuk upacara, bentuk layanan dan penerima manfaat untuk pelayanan, serta agenda rapat dan kesepakatan yang disetujui untuk rapat koordinasi).
   - *Lokasi Dateline Resmi Kota Contoh*: Sistem menyediakan opsi pilihan seluruh wilayah kecamatan resmi di Kota Contoh (Kecamatan Utara, Selatan, Timur, Barat, dan Pusat) guna menjamin konsistensi penulisan _dateline_ jurnalistik.
   - *Daftar Pihak yang Hadir dan Kutipan Narasumber*: Staf dapat mencatat hingga 10 nama pihak yang hadir beserta jabatannya, serta mendaftarkan hingga 5 kutipan langsung narasumber pejabat secara akurat.
   - *Unggah Foto Dokumentasi*: Staf mengunggah foto dokumentasi kegiatan beresolusi tinggi yang divalidasi integritas ekstensinya menggunakan pemeriksaan biner (*magic bytes*) untuk mencegah masuknya berkas palsu atau berbahaya.

2. *Prosedur Pembentukan Draf Otomatis (AI Engine) dan Audit Redaksional*:
   Setelah formulir masukan divalidasi skema Zod pada sisi peramban, data dikirimkan ke modul pemrosesan `POST /api/generate` yang dilindungi oleh _Same-Origin Request Guard_ dan pembatas laju permintaan (_rate limiter_). Sistem menginstruksikan model komputasi cerdas Google Gemini melalui instruksi terstruktur berkaidah jurnalistik piramida terbalik (menghasilkan judul berita dinas yang memikat, teras berita/_lead_ berbasis 5W+1H, tubuh berita kronologis, penyematan kutipan, dan penutup). Bersamaan dengan pembentukan naskah, sistem menghasilkan:
   - *Modul Review Kutipan Langsung (`quoteReviews`)*: Menyajikan perbandingan berdampingan antara kutipan asli narasumber (*original*) terhadap hasil olahan AI (*cleaned*). Staf Humas wajib menelaah dan menyetujui variasi kutipan yang sah guna menjamin bahwa ucapan narasumber tidak mengalami distorsi makna atau halusinasi informasi.
   - *Modul Audit Fakta (`factAudits`)*: Memverifikasi kesesuaian antara klaim dalam naskah berita terhadap butir fakta masukan 5W+1H.
   - *Live Text Editor*: Menyediakan modul penyuntingan teks secara langsung agar staf dapat menyempurnakan diksi atau menyesuaikan gaya bahasa sebelum diajukan ke pimpinan.
   - *Generator Takarir Media Sosial*: Secara otomatis merangkum naskah rilis menjadi teks takarir (_caption_) ringkas, informatif, dan dilengkapi tanda pagar (_hashtag_) resmi siap unggah untuk akun Instagram `@humas_kotacontoh`.

3. *Prosedur Verifikasi dan Persetujuan (Approval) Naskah Berjenjang*:
   Draf naskah yang telah dimatangkan pada modul penyuntingan diajukan oleh staf Humas ke modul verifikasi pimpinan di dalam sistem. Pimpinan (Kepala Bidang Pengelolaan Informasi Publik atau Pranata Humas) menelaah naskah secara komprehensif melalui dasbor verifikasi. Pimpinan dapat menyematkan catatan koreksi pada sistem atau langsung memberikan persetujuan resmi (_approval_ ACC). Status naskah seketika diperbarui menjadi *Approved* disertai rekam jejak digital (*audit log*) pemeriksa, tanggal, dan waktu persetujuan.

4. *Prosedur Ekspor Dokumen Resmi (.docx) dan Validasi Faktual (Gatekeeper)*:
   Sistem menerapkan mekanisme gerbang integritas faktual (*Factual Gatekeeper Guard*), di mana tombol ekspor dokumen Microsoft Word (`.docx`) tetap dinonaktifkan (*locked*) hingga seluruh syarat keabsahan terpenuhi secara mutlak:
   - Seluruh kutipan narasumber telah ditelaah dan berstatus disetujui (*all quotes approved*).
   - Seluruh daftar periksa formula 5W+1H telah berstatus lengkap (*checklist complete*).
   - Berkas foto dokumentasi kegiatan telah terunggah dan terverifikasi.
   - Tidak ada modifikasi data formulir yang belum digenerasikan ulang.
   Setelah seluruh syarat terpenuhi, sistem mengekspor berkas melalui endpoint `POST /api/export-docx` menghasilkan file Microsoft Word terstandar dengan penamaan otomatis `press-release-diskominfo-YYYYMMDD-HHMMSS.docx`. Dokumen Word ini secara otomatis memuat lambang kementerian, kop surat dinas resmi Dinas Komunikasi dan Informatika Kota Contoh, garis ganda standar tata naskah dinas, tipografi baku, penataan foto kegiatan proporsional 300 DPI, dan identitas verifikator rilis pers. Berkas siap dicetak untuk arsip fisik maupun dibagikan ke mitra jurnalis, sementara naskah terverifikasi diterbitkan ke portal web `portal.kotacontoh.go.id` dan media sosial.

5. *Prosedur Pengarsipan Digital Terpusat*:
   Seluruh data masukan 5W+1H, riwayat penelaahan pimpinan, foto liputan asli, naskah rilis final, serta berkas ekspor Word disimpan secara terpusat pada repositori komputasi awan (*cloud storage*). Staf Humas maupun pimpinan dapat melakukan pencarian terindeks sewaktu-waktu berdasarkan tanggal agenda, kategori seksi, maupun kata kunci kegiatan guna penyusunan laporan pertanggungjawaban (LPJ) berkala.

=== Use Case Diagram Sistem Usulan
Pemodelan fungsionalitas sistem usulan mengidentifikasi interaksi antara pengguna dengan layanan terintegrasi yang disediakan oleh Aplikasi _Press Release Auto-Generator_.

==== Deskripsi Aktor Sistem Usulan
Aktor yang berinteraksi dengan sistem usulan dipaparkan pada Tabel III.6 berikut:

#figure(
  table(
    columns: (0.8cm, 3.8cm, 10.2cm),
    inset: (x: 6pt, y: 7pt),
    align: (center + horizon, left + horizon, left + horizon),
    [*No.*], [*Aktor*], [*Deskripsi Peran dan Tanggung Jawab dalam Sistem*],
    [1.], [Staf Humas], [Bertindak sebagai operator pelaksana yang menginput formula fakta 5W+1H, memilih kategori kegiatan dinamis, mengunggah foto berintegritas biner, memicu pembentukan draf AI, mengaudit komparasi kutipan narasumber, menyunting draf di Live Editor, memvalidasi takarir Instagram, mengajukan naskah ke pimpinan, dan mengunduh berkas Word (.docx) ber-kop resmi.],
    [2.], [Pimpinan (Kepala Bidang)], [Bertindak sebagai verifikator materi rilis yang menelaah draf berita pada dasbor sistem, memeriksa akurasi informasi dan etika kedinasan, menyematkan catatan revisi, memberikan persetujuan resmi (_approval_ ACC), serta memantau rekam jejak publikasi.],
    [3.], [Administrator Sistem], [Bertindak sebagai pengelola teknis yang bertugas memelihara akun pengguna, mengonfigurasi batas laju permintaan (_rate limit_), memantau konektivitas API Google Gemini, mengawasi log audit sistem, serta memastikan ketersediaan peladen repositori awan.],
  ),
  caption: [Deskripsi Aktor Sistem Usulan],
)
#sumber([Hasil Analisis dan Perancangan Sistem Usulan, 2026])

==== Deskripsi Use Case Sistem Usulan
Rincian fungsi-fungsi sistem usulan dirangkum pada Tabel III.7 berikut:

#figure(
  table(
    columns: (0.8cm, 4.4cm, 9.6cm),
    inset: (x: 6pt, y: 6pt),
    align: (center + horizon, left + horizon, left + horizon),
    [*No.*], [*Nama Use Case*], [*Deskripsi Fungsionalitas Sistem*],
    [1.], [Autentikasi Pengguna (Login)], [Memvalidasi identitas kredensial staf, pimpinan, atau admin guna mengamankan hak akses modul aplikasi.],
    [2.], [Input Fakta 5W+1H Terstruktur], [Menyediakan formulir interaktif dengan 6 kartu status waktu nyata (What, Who, Where, When, Why, How) yang mencegah data kosong.],
    [3.], [Pilih Jenis Kegiatan Dinamis], [Menyajikan 6 opsi kategori kegiatan (bimbingan, lomba, upacara, pelayanan, rapat, lainnya) beserta input kondisional khusus.],
    [4.], [Pilih Dateline Kecamatan Kota Contoh], [Menyediakan pilihan baku seluruh wilayah kecamatan di Kota Contoh untuk standarisasi _dateline_ berita.],
    [5.], [Unggah & Validasi Foto], [Menerima unggahan foto liputan dengan pemeriksaan ekstensi biner (_magic bytes_) dan optimasi kompresi visual.],
    [6.], [Bentuk Draf Berita (Gemini AI)], [Memproses data masukan menggunakan model AI dengan rekayasa _prompt_ jurnalistik piramida terbalik kedinasan.],
    [7.], [Audit Kutipan (Original vs Cleaned)], [Menyajikan modul perbandingan kutipan narasumber secara berdampingan untuk mencegah distorsi dan halusinasi makna.],
    [8.], [Audit Kepatuhan Fakta 5W+1H], [Memeriksa ketercakupan seluruh poin fakta masukan di dalam narasi berita yang dihasilkan oleh sistem.],
    [9.], [Sunting Naskah (Live Editor)], [Menyediakan pengolah kata interaktif bagi staf untuk menyempurnakan redaksi sebelum diajukan ke pimpinan.],
    [10.], [Generate Takarir Instagram], [Menghasilkan teks takarir (_caption_) ringkas dan tagar resmi siap unggah untuk akun media sosial Diskominfo Kota Contoh.],
    [11.], [Ajukan Naskah ke Verifikasi], [Mengirimkan berkas naskah ke daftar antrean telaah pimpinan secara terpusat di dalam sistem.],
    [12.], [Telaah & Catat Revisi], [Pimpinan memeriksa substansi naskah berita dan menyematkan catatan perbaikan jika naskah belum layak terbit.],
    [13.], [Setujui Naskah (Approval ACC)], [Pimpinan mengonfirmasi persetujuan resmi terbit sehingga status dokumen terkunci menjadi _Approved_.],
    [14.], [Validasi Factual Gatekeeper], [Mengunci fungsi unduh Word hingga seluruh kutipan disetujui, foto terunggah, dan fakta 5W+1H terisi lengkap.],
    [15.], [Ekspor Dokumen Resmi (.docx)], [Menghasilkan file Microsoft Word resmi ber-kop Diskominfo Kota Contoh, bertipografi dinas, dan berfoto resolusi tinggi.],
    [16.], [Kelola Arsip Publikasi Terpusat], [Menyimpan dan mengindeks seluruh naskah, foto, dan log persetujuan ke repositori awan yang mudah ditelusuri.],
  ),
  caption: [Deskripsi Use Case Sistem Usulan],
)
#sumber([Hasil Analisis dan Perancangan Sistem Usulan, 2026])

==== Diagram Use Case Sistem Usulan
Visualisasi relasi aktor dan _use case_ fungsional sistem usulan disajikan pada Gambar III.4 berikut:

#figure(
  image("../../gambar/gambar_3_4_use_case_usulan.png", width: 95%),
  caption: [Use Case Diagram Sistem Usulan Aplikasi Press Release Auto-Generator],
)
#sumber([Hasil Perancangan Sistem Usulan, 2026])

=== Activity Diagram Sistem Usulan
_Activity Diagram_ sistem usulan memodelkan dinamika aliran aktivitas terintegrasi antara Staf Humas, modul aplikasi web cerdas (Next.js & Gemini AI), Pimpinan verifikator, serta portal publikasi dan repositori awan.

==== Skenario Aktivitas Sistem Usulan
Runtutan aliran kerja (_workflow_) sistem usulan diuraikan pada Tabel III.8 berikut:

#figure(
  table(
    columns: (0.8cm, 3.0cm, 3.5cm, 7.5cm),
    inset: (x: 5pt, y: 6pt),
    align: (center + horizon, left + horizon, left + horizon, left + horizon),
    [*No.*], [*Entitas Pelaksana*], [*Aktivitas Operasional*], [*Keluaran / Respons Sistem*],
    [1.], [Staf Humas], [Mengisi formulir fakta 5W+1H, memilih jenis kegiatan dinamis, memilih kecamatan dateline, menginput kutipan, dan mengunggah foto], [Seluruh indikator kartu 5W+1H berubah hijau dan data masukan siap diproses],
    [2.], [Sistem Web & AI], [Memvalidasi integritas data (Zod) dan file biner gambar (_magic bytes_)], [Data dinyatakan sah dan lolos uji keamanan berkas masukan],
    [3.], [Sistem Web & AI], [Mengirim payload ke Gemini AI via endpoint terproteksi (`POST /api/generate`)], [Draf berita piramida terbalik, audit kutipan, audit fakta, dan takarir medsos terbentuk],
    [4.], [Staf Humas], [Menelaah komparasi kutipan (_original vs cleaned_), menyetujui kutipan, dan menyunting draf pada Live Editor], [Kutipan tervalidasi bebas distorsi makna dan naskah berita disempurnakan],
    [5.], [Staf Humas], [Mengirimkan pengajuan naskah berita ke antrean verifikasi pimpinan], [Status dokumen berubah menjadi *Under Review* dan notifikasi terkirim],
    [6.], [Pimpinan], [Membuka dasbor verifikasi dan memeriksa kelayakan rilis berita], [Pimpinan mengambil keputusan persetujuan (*Decision*)],
    [7.], [Pimpinan], [Pemeriksaan: Apakah naskah rilis disetujui?], [Jika *Revisi*: Menyematkan catatan revisi ke sistem (kembali ke Staf)\ Jika *ACC*: Menekan tombol persetujuan resmi (*Approved*)],
    [8.], [Sistem Web & AI], [Memeriksa pemenuhan syarat integritas melalui _Factual Gatekeeper Guard_], [Semua kutipan disetujui, foto valid, fakta lengkap: Tombol ekspor Word aktif],
    [9.], [Sistem Web & AI], [Membuat berkas Word dinas (`POST /api/export-docx`) dan menyimpan arsip ke _cloud_], [File `press-release-diskominfo-YYYYMMDD-HHMMSS.docx` terbentuk dan terarsip],
    [10.], [Staf Humas], [Mengunduh file `.docx` ber-kop dinas dan mempublikasikan ke web portal & medsos], [Siaran pers tersirkulasi resmi ke media massa dan arsip tersimpan rapi (Selesai)],
  ),
  caption: [Skenario Aliran Kerja (_Workflow_) Sistem Usulan],
)
#sumber([Hasil Analisis dan Perancangan Sistem Usulan, 2026])

==== Diagram Aktivitas Sistem Usulan
Pemodelan alur kerja sistem usulan menggunakan pembagian empat lajur tanggung jawab (_swimlane_) dimodelkan pada Gambar III.5 berikut:

#figure(
  image("../../gambar/gambar_3_5_activity_diagram_usulan.png", width: 95%),
  caption: [Activity Diagram Sistem Usulan Aplikasi Press Release Auto-Generator],
)
#sumber([Hasil Perancangan Sistem Usulan, 2026])

=== Rancangan Antarmuka Aplikasi Press Release Auto-Generator
Rancangan antarmuka pengguna (_user interface_) disusun berlandaskan prinsip ergonomi web responsif yang modern, bersih, dan intuitif, yang diadaptasi secara langsung dari implementasi sistem nyata pada alamat `https://press-release-kotacontoh.contoh.go.id/`. Antarmuka dibangun dengan palet warna resmi instansi (kombinasi hijau _forest_ `#1b4332`, emas kedinasan `#c59b27`, dan latar belakang _off-white_ yang nyaman di mata). Struktur antarmuka terbagi atas beberapa komponen utama:

1. *Bilah Navigasi dan Stepper Alur 3 Langkah*:
   Bagian kepala antarmuka menampilkan identitas institusi "HUMAS DISKOMINFO KOTA CONTOH" dan nama aplikasi *Press Release Generator V2*, disertai arahan operasional: "_Isi fakta 5W+1H, audit draf, setujui kutipan, lalu download dokumen Word_". Di samping kanan tersedia tombol *Reset draf* untuk mengosongkan formulir sewaktu-waktu. Alur kerja dipandu oleh indikator tahapan (_stepper wizard_) yang terbagi menjadi 3 langkah berurutan: (1) *Isi data 5W1H*, (2) *Review & edit*, dan (3) *Download DOCX*.

2. *Panel Kartu Pemantau Fakta Inti (Formula 5W+1H Badges)*:
   Sistem menyajikan 6 kartu status interaktif real-time di bagian atas formulir:
   - *What*: Menampilkan nama dan jenis agenda (indikator garis putus-putus oranye jika belum lengkap, garis hijau tegas jika terisi).
   - *Who*: Menampilkan instansi penyelenggara (terisi secara _default_ sebagai Dinas Komunikasi dan Informatika Kota Contoh).
   - *Where*: Menampilkan lokasi acara dan kecamatan _dateline_.
   - *When*: Menampilkan status pemilihan tanggal agenda.
   - *Why*: Menampilkan status kelengkapan latar belakang dan tujuan acara.
   - *How*: Menampilkan status urutan kronologi kegiatan.
   Sistem menegaskan aturan dasar: "_Field inti wajib diisi dengan fakta. AI tidak akan menebak data yang kosong._" Hal ini menjadi benteng utama dalam mencegah kekeliruan narasi sejak awal masukan data.

3. *Formulir Parameter Kegiatan Dinamis dan Kontekstual*:
   Formulir dirancang secara cerdas dengan fitur interaktif berikut:
   - *Pilihan 6 Kategori Agenda Kedinasan*: Kolom jenis kegiatan menyediakan opsi bimbingan/sosialisasi, lomba/perayaan, upacara/ziarah, pelayanan/sosial, rapat/koordinasi, dan kegiatan lainnya. Pilihan ini memunculkan kolom masukan kontekstual secara otomatis (misalnya kolom pemateri dan pokok materi untuk bimbingan, atau agenda dan hasil kesepakatan untuk rapat).
   - *Menu Pilihan 11 Dateline Kecamatan*: Menu _dropdown_ memuat seluruh wilayah kecamatan resmi di Kota Contoh.
   - *Daftar Hadir dan Kutipan Narasumber*: Modul pencatatan hingga 10 pihak yang hadir dan hingga 5 transkrip kutipan langsung narasumber pejabat.
   - *Unggah Foto Liputan*: Area unggah berkas foto dengan pratinjau instan dan verifikasi biner integritas gambar (*magic bytes*).

4. *Modul Audit Redaksional, Review Kutipan, dan Live Text Editor*:
   Setelah tombol pemrosesan ditekan, sistem berpindah ke langkah kedua (*Review & edit*):
   - *Review Komparasi Kutipan*: Menampilkan kutipan asli narasumber bersandingan dengan teks olahan kecerdasan buatan (*original vs cleaned*). Staf dapat menelaah dan mengonfirmasi kutipan yang disetujui guna menjamin bahwa ucapan narasumber 100% akurat dan tidak terpapar halusinasi model AI.
   - *Audit Fakta 5W+1H*: Panel verifikasi otomatis yang memeriksa ketercakupan setiap butir fakta lapangan di dalam draf naskah.
   - *Live Text Editor*: Pengolah kata langsung di dalam peramban untuk menyempurnakan diksi berita.
   - *Generator Takarir Instagram*: Menghasilkan takarir media sosial siap pakai untuk akun `@humas_kotacontoh` lengkap dengan tagar kedinasan.

5. *Modul Pratinjau Dokumen dan Factual Gatekeeper Guard*:
   Pada langkah ketiga (*Download DOCX*), sistem menyajikan pratinjau naskah ber-kop surat resmi Dinas Komunikasi dan Informatika Kota Contoh. Tombol unduh dokumen Microsoft Word (`.docx`) dilindungi oleh gerbang validasi faktual (*Factual Gatekeeper Guard*) yang hanya akan aktif apabila seluruh kutipan telah berstatus _approved_, foto telah terverifikasi, dan fakta 5W+1H terisi lengkap. Dokumen Word yang diunduh berformat baku dengan penamaan `press-release-diskominfo-YYYYMMDD-HHMMSS.docx` dan siap disebarkan ke media massa.

Visualisasi rancangan antarmuka formulir masukan fakta 5W+1H terstruktur dan modul otomasi rilis pers yang diadaptasi dari implementasi aplikasi web langsung disajikan pada Gambar III.6 berikut:

#figure(
  image("../../gambar/gambar_3_6_rancangan_antarmuka_generator.png", width: 100%),
  caption: [Rancangan Antarmuka Aplikasi Press Release Auto-Generator],
)
#sumber([Tangkapan Layar Antarmuka Aplikasi Web (press-release-kotacontoh.contoh.go.id), 2026])
