#import "../sinta.typ": *

#show: jurnal-sinta.with(
  sinta-level: 4,      // Pilihan: 1 (IJAIN-UAD), 2 (JTIIK-UB), 3 (JISKA-UIN), 4 (JKI-UBSI), 5 (TEKNOIF-ITP), 6 (METIK-Jayakarta)
  layout-mode: "2col", // Pilihan: "2col" (Layout Terbagi 2 / 2 Kolom), "1col" (Layout Biasa / 1 Kolom), atau "default"
  judul-id: "Analisis Sistem Pengelolaan Publikasi Berita dan Perancangan Aplikasi Press Release Auto-Generator pada Dinas Komunikasi dan Informatika Kota Contoh",
  judul-en: "Analysis of News Publication Management System and Design of Press Release Auto-Generator Application at the Department of Communication and Informatics of Contoh City",
  penulis: ("Penulis Contoh*", "Penulis Pendamping Contoh"),
  afiliasi: "Program Studi Teknologi Informasi, Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika, Kota Contoh, Indonesia",
  email-korespondensi: "penulis.contoh@contoh.ac.id, pendamping.contoh@contoh.ac.id",
  abstrak-id: [
    Bidang Pengelolaan Informasi dan Komunikasi Publik (Humas) pada Dinas Komunikasi dan Informatika Kota Contoh bertanggung jawab atas peliputan kegiatan kedinasan, penyusunan siaran pers (_press release_), dan publikasi informasi ke portal `portal.kotacontoh.go.id` serta akun media sosial `@humas_kotacontoh`. Berdasarkan observasi dan wawancara, proses yang berjalan saat ini masih menghadapi tiga kendala utama: pengetikan draf berita secara manual di Microsoft Word memakan waktu 1 hingga 2 jam per rilis, verifikasi pimpinan melalui pesan instan menyulitkan pelacakan riwayat revisi, serta pengarsipan di komputer lokal berisiko menyebabkan kehilangan dokumen. Penelitian ini menganalisis prosedur sistem berjalan menggunakan pemodelan _Unified Modeling Language_ (UML) dan merancang Aplikasi _Press Release Auto-Generator_ berbasis formulir 5W+1H terstruktur. Hasil perancangan menunjukkan bahwa standarisasi masukan 5W+1H, antarmuka verifikasi berjenjang, serta repositori arsip terpusat mampu memangkas tahapan manual dan menjaga konsistensi redaksional berita instansi.
  ],
  kata-kunci-id: ("Analisis Sistem", "Humas Pemerintah Daerah", "Otomatisasi Press Release", "Sistem Informasi Publikasi", "UML"),
  abstrak-en: [
    The Public Information and Communication Division of the Department of Communication and Informatics of Contoh City manages official event coverage, press release drafting, and multi-channel publication. Field observation and interviews revealed three operational bottlenecks: manual press release drafting in Microsoft Word requires 1 to 2 hours per article, manuscript verification via instant messaging obscures revision history, and local folder archiving exposes files to data loss. This study analyzes the ongoing system using Unified Modeling Language (UML) diagrams and proposes a structured 5W+1H Press Release Auto-Generator application to standardize institutional news publishing.
  ],
  kata-kunci-en: ("Press Release Automation", "Public Information System", "Public Relations", "System Analysis", "UML"),
)

= Pendahuluan
Dinas Komunikasi dan Informatika (Diskominfo) Kota Contoh merupakan perangkat daerah yang menyelenggarakan pelayanan publik di bidang komunikasi, informatika, dan keterbukaan informasi pada wilayah Kota Contoh [1], [2]. Fungsi pengelolaan informasi dan publikasi berada pada Bidang Pengelolaan Informasi dan Komunikasi Publik (Humas) yang meliput agenda kedinasan lintas unit kerja setiap pekan [3], [12].

Proses produksi berita dari catatan lapangan menjadi naskah siaran pers (_press release_) saat ini masih dikerjakan secara manual menggunakan Microsoft Word dengan durasi 1 hingga 2 jam per kegiatan [4], [5]. Pengajuan draf naskah kepada Kepala Bidang melalui pesan instan menyulitkan pelacakan riwayat revisi (_version tracking_) dan memperlambat waktu tayang [6], [13]. Penelitian ini menganalisis sistem berjalan dengan diagram UML [8], [10] serta merancang Aplikasi _Press Release Auto-Generator_ berbasis input 5W+1H terstruktur [11], [15].

= Metode Penelitian
== Teknik Pengumpulan Data
Penelitian dilaksanakan pada Bidang Pengelolaan Informasi dan Komunikasi Publik Dinas Komunikasi dan Informatika Kota Contoh melalui tiga tahapan [4], [7]:
1. *Observasi Lapangan*: Peliputan langsung agenda kedinasan, pencatatan unsur 5W+1H, dan penyusunan naskah berita [1], [2].
2. *Wawancara Terstruktur*: Diskusi dengan Pranata Humas dan staf pengelola publikasi mengenai alur verifikasi dan kendala pengarsipan [3], [12].
3. *Studi Pustaka*: Kajian literatur rekayasa perangkat lunak, pemodelan UML, tata kelola sistem informasi web, serta pengujian perangkat lunak [9], [10], [14], [15].

== Metode Analisis Sistem
Analisis dilakukan dengan memetakan spesifikasi dokumen masukan-keluaran, memodelkan interaksi aktor pada _Use Case Diagram_ serta aliran kerja pada _Activity Diagram_ [8], [10], lalu menyusun spesifikasi solusi _Press Release Auto-Generator_ [11], [15].

= Hasil dan Pembahasan
== Analisis Prosedur dan Dokumen Sistem Berjalan
Alur pengelolaan publikasi berita yang berjalan meliputi enam tahapan: peliputan kegiatan 5W+1H, pengetikan draf di Microsoft Word, pengiriman file `.docx` via pesan instan, koreksi dan persetujuan pimpinan, publikasi ke portal web `portal.kotacontoh.go.id` dan media sosial `@humas_kotacontoh`, serta pengarsipan lokal [1], [5], [13].

#figure(
  image("gambar/gambar_3_2_use_case_berjalan.png", width: 95%),
  caption: [Use Case Diagram Sistem Publikasi Berita Berjalan],
)

== Evaluasi Masalah dan Usulan Solusi
Melalui Aplikasi _Press Release Auto-Generator_, staf Humas memasukkan parameter kegiatan ke dalam formulir 5W+1H terstruktur, melakukan verifikasi berjenjang dengan log revisi yang terekam, dan menyimpan dokumen di repositori terpusat [6], [14], [15].

#figure(
  image("gambar/gambar_3_3_activity_diagram_berjalan.png", width: 95%),
  caption: [Activity Diagram Sistem Publikasi Berita Berjalan],
)

= Kesimpulan
Alur publikasi berita yang berjalan masih terkendala oleh pengetikan manual, verifikasi via pesan instan, dan pengarsipan lokal. Perancangan Aplikasi _Press Release Auto-Generator_ berbasis input 5W+1H terstruktur mampu menstandarkan format berita dan mempercepat proses verifikasi di lingkungan Humas Diskominfo Kota Contoh.

= Daftar Pustaka
#set par(first-line-indent: 0cm, hanging-indent: 0.6cm)
#set text(size: 8.5pt)

[1] W. E. Putri and A. M. Afrilia, "Comparative Study of Local Government Website Quality as Implementation Of E-Government Public Relations in Public Information Disclosure," _Jurnal Media dan Komunikasi Indonesia_, vol. 4, no. 2, pp. 143-156, 2023, doi: https://doi.org/10.22146/jmki.83056.

[2] Y. Vitriani and N. Novriyanto, "Digital Transformation in Government Public Relations: A Strategic Information System Framework for Governance and Transparency in the Riau Provincial Government of Indonesia," _Engineering and Technology Journal_, vol. 10, no. 8, pp. 1-10, 2025, doi: https://doi.org/10.47191/etj/v10i08.51.

[3] F. Nurfalah, M. Nuruzzaman, S. Khumayah, and N. Irawan, "Digital Communication Strategy for Government Public Relations in Indonesia and Thailand," _International Journal of Communication and Public Relation_, vol. 11, no. 1, pp. 1-16, 2026, doi: https://doi.org/10.47604/ijcpr.3595.

[4] N. T. Muay, E. Sediyono, and J. Tambotoh, "Integration Waterfall and Scrum Methodology in The Development of SIMARGA Web Application," _Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi)_, vol. 8, no. 2, pp. 223-233, 2024, doi: https://doi.org/10.29207/resti.v8i2.5652.

[5] D. Wahyuni and M. L. Hamzah, "Analisa Tingkat Usability Website Menggunakan Metode System Usability Scale dan Post Study System Usability Questionnaire," _Jurnal Testing dan Implementasi Sistem Informasi_, vol. 2, no. 1, pp. 52-58, 2024, doi: https://doi.org/10.55583/jtisi.v2i1.384.

[6] A. F. Rusdi, B. Hardian, and T. Raharjo, "Service Automation Implementation for Delivering CaaS at the Ministry of Finance of Indonesia," _Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi)_, vol. 7, no. 5, pp. 1174-1181, 2023, doi: https://doi.org/10.29207/resti.v7i5.5032.

[7] A. Tedyyana, M. Fauzi, D. Enda, F. Ratnawati, and E. Syam, "Perancangan Aplikasi Tanggap Api Berbasis Android Menggunakan Metode Design Sprint," _Jurnal Teknologi Informasi dan Ilmu Komputer_, vol. 9, no. 2, pp. 215-224, 2022, doi: https://doi.org/10.25126/jtiik.2022914022.

[8] A. Zaenudin and Y. Syahidin, "Rancangan Sistem Informasi Pengaduan Masyarakat Berbasis Web Pada Kantor Kecamatan Dengan Fitur Notifikasi Telegram," _Jutisi: Jurnal Ilmiah Teknik Informatika dan Sistem Informasi_, vol. 11, no. 1, pp. 1-12, 2022, doi: https://doi.org/10.35889/jutisi.v11i1.812.

[9] E. Mufida, N. Iriadi, and D. Andriansyah, "Pemeringkatan Kinerja Dosen pada Perguruan Tinggi Swasta Menggunakan Algoritma Simple Additive Weighting," _JISKA (Jurnal Informatika Sunan Kalijaga)_, vol. 9, no. 1, pp. 59-69, 2024, doi: https://doi.org/10.14421/jiska.2024.9.1.59-69.

[10] A. Amani Bestari and A. Voutama, "Penerapan UML pada Sistem Informasi Pengaduan Masyarakat Berbasis Web," _JATI (Jurnal Mahasiswa Teknik Informatika)_, vol. 8, no. 3, pp. 2655-2662, 2024, doi: https://doi.org/10.36040/jati.v8i3.9528.

[11] V. Feladi, "Pengembangan Sistem Informasi Sekolah Berbasis Web di SMA Wisuda Pontianak," _Jurnal Khatulistiwa Informatika_, vol. 11, no. 1, pp. 61-67, 2023, doi: https://doi.org/10.31294/jki.v11i1.14618.

[12] S. Maryanti, N. Komariah, and S. Rodiah, "Diseminasi Informasi Publik oleh Pejabat Pengelola Informasi dan Dokumentasi Kota Banjar sebagai Upaya Keterbukaan Informasi Publik," _Moderat: Jurnal Ilmiah Ilmu Pemerintahan_, vol. 8, no. 3, pp. 495-506, 2022, doi: https://doi.org/10.25157/moderat.v8i3.2715.

[13] I. Aprylianti and A. R. Purwanti, "Dampak Aplikasi Lapor Sleman Terhadap Penyaluran Pelayanan Pengaduan Masyarakat di Kabupaten Sleman ditinjau dari Undang-Undang Nomor 25 Tahun 2009 Tentang Pelayanan Publik," _AURELIA: Jurnal Penelitian dan Pengabdian Masyarakat Indonesia_, vol. 1, no. 1, pp. 1-10, 2022, doi: https://doi.org/10.57235/aurelia.v1i1.85.

[14] A. Tirtayasa and D. Y. Kristiyanto, "Sistem Pendukung Keputusan Pemilihan Ketua RT/RW Berbasis Web MVC Menggunakan Metode TOPSIS," _Jurnal Teknoif Teknik Informatika Institut Teknologi Padang_, vol. 11, no. 2, pp. 54-61, 2023, doi: https://doi.org/10.21063/jtif.2023.v11.2.54-61.

[15] S. D. S. Saian, N. L. Kakihary, and T. Wahyono, "Pengujian Content Management System (CMS) Sekolahku Menggunakan Metode Black Box Testing dengan Teknik Boundary Value Analysis," _IT-Explore: Jurnal Penerapan Teknologi Informasi dan Komunikasi_, vol. 1, no. 2, pp. 100-113, 2022, doi: https://doi.org/10.24246/itexplore.v1i2.2022.pp100-113.
