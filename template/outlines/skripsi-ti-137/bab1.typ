#import "../../../lib.typ": *

= Pendahuluan

== Latar Belakang Masalah
Latar belakang masalah memaparkan latar belakang pemilihan infrastruktur jaringan komputer pada instansi atau perusahaan sebagai objek penelitian skripsi. Jelaskan kondisi operasional jaringan saat ini, peran strategis ketersediaan dan keandalan komunikasi data dalam mendukung aktivitas bisnis, serta urgensi dilakukannya perancangan ulang atau optimasi jaringan (misalnya terkait manajemen *bandwidth*, segmentasi jaringan, efisiensi perutean (*routing*), atau sistem pertahanan keamanan siber mutakhir).

== Identifikasi Permasalahan
Identifikasi permasalahan merinci secara spesifik permasalahan atau celah teknis yang ditemukan pada infrastruktur jaringan berjalan:
+ Kepadatan lalu lintas data (*network congestion*) dan keterbatasan pembagian *bandwidth* antar divisi.
+ Kerentanan arsitektur jaringan terhadap akses ilegal, serangan siber, atau ketiadaan pemisahan hak akses (*broadcast domain* yang terlalu luas).
+ Ketiadaan mekanisme *failover* atau sistem redundansi yang mengakibatkan gangguan operasional (*downtime*) saat terjadi kegagalan perangkat tautan data.

== Perumusan Masalah
Perumusan masalah disusun dalam format kalimat tanya yang terukur dan terarah sesuai kasus jaringan yang diteliti:
+ Bagaimana menganalisis kinerja, kelemahan, dan topologi infrastruktur jaringan berjalan pada instansi objek riset?
+ Bagaimana merancang konfigurasi jaringan usulan berbasis teknologi mutakhir (seperti VLAN, VPN, OSPF, atau manajemen keamanan *firewall*) guna mengatasi permasalahan yang ada?
+ Bagaimana membuktikan efektivitas peningkatan performa dan keamanan jaringan usulan melalui simulasi pengujian awal dan pengujian akhir?

== Tujuan dan Manfaat
Tujuan dan manfaat memaparkan arah sasaran dan faedah nyata dari pelaksanaan penelitian skripsi:

1. *Tujuan Penelitian:*
   + Membangun rancangan infrastruktur jaringan komputer usulan yang teroptimasi, aman, dan memiliki ketersediaan tinggi (*high availability*).
   + Menerapkan manajemen *bandwidth* dan mekanisme keamanan jaringan bertingkat untuk menunjang produktivitas operasional kerja.
   + Membuktikan secara empiris keberhasilan rancangan usulan melalui komparasi parameter *Quality of Service* (QoS) sebelum dan sesudah perbaikan.

2. *Manfaat Penelitian:*
   + *Bagi Penulis:* Memenuhi salah satu persyaratan kelulusan Program Sarjana (S1) Program Studi Teknologi Informasi Fakultas Teknik dan Informatika Universitas Bina Sarana Informatika.
   + *Bagi Perusahaan / Instansi Objek Riset:*
     - Meningkatkan stabilitas, kecepatan transmisi, dan keamanan data internal institusi.
     - Memperoleh panduan arsitektur dan dokumentasi konfigurasi jaringan yang terstandarisasi.
   + *Bagi Pembaca / Akademisi:*
     - Memberikan referensi praktis mengenai rekayasa infrastruktur jaringan dan pemecahan kendala jaringan di dunia industri nyata.

== Metode Penelitian

=== Teknik Pengumpulan Data
Teknik pengumpulan data yang digunakan dalam perancangan skripsi jaringan ini meliputi:
+ *Observasi:*\
  Melakukan peninjauan langsung ke lokasi penelitian guna mengamati penataan kabel (*cabling structure*), letak rak server, perangkat jaringan aktif (router, switch, access point), serta pola distribusi lalu lintas jaringan.
+ *Wawancara:*\
  Melakukan tanya jawab teknis dengan administrator jaringan (*network engineer*) atau penanggung jawab IT terkait kebijakan akses, riwayat gangguan jaringan, dan kebutuhan pengembangan institusi.
+ *Studi Pustaka:*\
  Mempelajari literatur ilmiah dari buku teks rekayasa jaringan, standar protokol RFC, serta minimal 5 artikel jurnal ilmiah terindeks dalam 5 tahun terakhir yang relevan dengan tema manajemen atau keamanan jaringan.

=== Model Pengembangan Jaringan
Model perancangan jaringan mengadopsi siklus hidup pengembangan jaringan terstruktur seperti *Network Development Life Cycle* (NDLC) atau model PPDIOO (*Prepare, Plan, Design, Implement, Operate, Optimize*). Tahapan NDLC mencakup:
+ *Analysis:* Menganalisis topologi, perangkat, dan beban trafik jaringan berjalan.
+ *Design:* Merancang topologi usulan, skema pengalamatan IP, dan kebijakan keamanan.
+ *Simulation Prototyping:* Mensimulasikan rancangan pada aplikasi simulator jaringan.
+ *Implementation:* Menerapkan konfigurasi pada skenario uji.
+ *Monitoring & Management:* Mengukur performa dan melakukan pengawasan berkala.

== Ruang Lingkup
Ruang lingkup memberikan batasan spesifik agar pembahasan perancangan jaringan tidak meluas:
+ Penelitian difokuskan pada perancangan jaringan usulan tingkat lanjut (tidak diperkenankan hanya menggunakan jaringan LAN sederhana) pada divisi atau gedung yang diteliti.
+ Pembahasan mencakup perancangan topologi logis, konfigurasi perutean, manajemen alokasi kapasitas pita (*bandwidth*), dan kebijakan keamanan perangkat lunak/keras.
+ Pengujian dilakukan melalui perangkat lunak simulator jaringan (*Cisco Packet Tracer*, *GNS3*, atau *EVE-NG*) dengan komparasi parameter uji sebelum dan sesudah usulan.
