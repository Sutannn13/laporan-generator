#import "../../../lib.typ": *

= Analisis Jaringan Berjalan

Bab ini menguraikan profil tempat riset, analisis arsitektur dan skema jaringan komputer yang sedang berjalan (*existing network*), pemetaan celah keamanan, spesifikasi perangkat keras dan lunak, serta identifikasi masalah dan alternatif pemecahannya.

== Tinjauan Perusahaan
Uraikan gambaran umum institusi tempat penelitian berlangsung. Pada halaman lampiran, kegiatan ini wajib dibuktikan dengan Surat Keterangan Riset asli yang ber-kop surat resmi perusahaan, bertanda tangan pejabat berwenang, dan berstempel basah.

=== Sejarah Perusahaan
Paparkan sejarah pendirian institusi, bidang bisnis atau layanan publik yang diselenggarakan, visi dan misi, serta peran teknologi informasi dalam mendukung operasional harian organisasi.

=== Struktur Organisasi dan Fungsi
Gambarkan struktur organisasi perusahaan dan uraikan uraian tugas (*job description*) serta fungsi masing-masing divisi, khususnya unit pengelola teknologi informasi dan jaringan.

#figure(
  rect(width: 85%, height: 5.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Bagan Struktur Organisasi Instansi / Perusahaan
  ],
  caption: [Struktur Organisasi Perusahaan],
)
#sumber([Profil Organisasi Instansi, 2026])

== Skema Jaringan Berjalan

=== Topologi Jaringan
Jelaskan topologi fisik dan logis yang diterapkan pada jaringan berjalan (misalnya topologi *Star* atau *Tree* sederhana yang belum terkelola optimal).

=== Arsitektur Jaringan
Uraikan arsitektur jaringan berjalan secara detail:
+ *Skema Pengalamatan IP (IP Addressing):* Blok alamat IP yang dialokasikan, kelas IP (*Classless/Classful*), *subnet mask*, *gateway*, dan DNS server yang dikonfigurasi.
+ *Pemodelan Protokol:* Penerapan lapisan TCP/IP pada jaringan operasional.
+ *Alokasi Pita Data (Bandwidth):* Kapasitas langganan *Internet Service Provider* (ISP) dan metode distribusinya kepada pengguna akhir (*end-user*).

=== Skema Jaringan
Gambarkan diagram skema jaringan berjalan secara komprehensif. Skema wajib dimodelkan dan ditangkap layar (*capture*) menggunakan perangkat lunak simulator jaringan resmi (*Cisco Packet Tracer*, *GNS3*, atau *Boson NetSim*).

#figure(
  rect(width: 90%, height: 6.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Diagram Tangkapan Layar Skema Jaringan Berjalan (Cisco Packet Tracer / GNS3)
  ],
  caption: [Skema Jaringan Berjalan Saat Ini],
)
#sumber([Hasil Observasi dan Pemodelan Simulator, 2026])

=== Keamanan Jaringan
Deskripsikan kondisi sistem keamanan jaringan berjalan, meliputi kebijakan *firewall*, filter port, keberadaan server proxy, autentikasi nirkabel (Wi-Fi WPA2/WPA3), serta proteksi antivirus pada simpul klien.

=== Spesifikasi Hardware dan Software Jaringan
Tabelkan seluruh inventaris perangkat keras dan perangkat lunak jaringan yang digunakan saat ini:

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3.5cm, 1.5cm, 1fr),
    stroke: 0.5pt + black,
    align: (center, left, left, center, left),
    [*No*], [*Nama Perangkat*], [*Tipe / Model*], [*Jumlah*], [*Fungsi Operasional*],
    [1], [Router Utama], [MikroTik RouterBOARD RB750Gr3], [1 Unit], [Gateway internet & perutean lokal],
    [2], [Switch Distribusi], [Unmanaged Switch 24-Port 10/100], [2 Unit], [Penghubung kabel workstation],
    [3], [Access Point], [TP-Link Wireless N Access Point], [3 Unit], [Distribusi sinyal nirkabel pengguna],
    [4], [Server Lokal], [PC Server Intel Xeon 16GB RAM], [1 Unit], [Penyimpanan berkas dan database],
    [5], [Sistem Operasi Jaringan], [RouterOS v7.x / Windows Server], [-], [Sistem operasi platform jaringan],
  ),
  caption: [Spesifikasi Hardware dan Software Jaringan Berjalan],
)
#sumber([Hasil Inventarisasi Departemen IT, 2026])

== Permasalahan
Jabarkan seluruh kendala dan kerentanan yang teridentifikasi pada jaringan berjalan:
+ *Kendala Trafik & Bandwidth:* Terjadinya perebutan kapasitas *bandwidth* karena belum diterapkannya manajemen antrean, sehingga unduhan dari satu klien melumpuhkan pengguna lain.
+ *Kendala Keamanan & Broadcast:* Seluruh komputer berada dalam satu segmen jaringan (*single broadcast domain*), memudahkan penyebaran malware dan memicu *broadcast storm*.
+ *Kendala Ketersediaan Tautan:* Ketiadaan jalur cadangan (*backup link/redundancy*) yang menyebabkan koneksi terputus total saat perangkat *switch* atau kabel utama mengalami gangguan.

== Alternatif Pemecahan Masalah
Uraikan langkah strategis teknis yang direkomendasikan untuk menanggulangi permasalahan di atas:
+ Menerapkan segmentasi jaringan virtual (*Virtual LAN* / VLAN) untuk memisahkan domain antar divisi.
+ Mengkonfigurasi manajemen *bandwidth* terpusat menggunakan metode *Queue Tree* atau *Hierarchical Token Bucket* (HTB).
+ Mengimplementasikan sistem pertahanan *firewall filter rules* dan VPN terenkripsi untuk keamanan akses jarak jauh.
