#import "../../../lib.typ": *

= Rancangan Jaringan Usulan

Bab ini memaparkan realisasi rancangan jaringan usulan, arsitektur topologi baru, skema simulasi, implementasi keamanan, manajemen lalu lintas data, serta pengujian awal dan pengujian akhir komparatif berbasis simulator jaringan.

== Jaringan Usulan
Jaringan usulan dirancang untuk menjawab seluruh kelemahan jaringan berjalan melalui pembaharuan topologi berhirarki (*hierarchical network design*), segmentasi lalu lintas data, proteksi keamanan ketat, dan manajemen antrean data yang adaptif.

=== Topologi Jaringan
Jelaskan topologi usulan yang diimplementasikan (misalnya topologi *Hierarchical Tree* dengan pemisahan *Core Layer*, *Distribution Layer*, dan *Access Layer*) guna menjamin skalabilitas, kemudahan isolasi kendala, serta ketersediaan tinggi.

=== Skema Jaringan
Tampilkan diagram skema jaringan usulan yang dimodelkan dan disimulasikan menggunakan aplikasi simulator jaringan (*Cisco Packet Tracer*, *GNS3*, atau *Boson NetSim*). Skema ini wajib memuat simpul antarmuka antar perangkat, penomoran port, serta penetapan *VLAN ID*.

#figure(
  rect(width: 90%, height: 6.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Tangkapan Layar Skema Simulasi Jaringan Usulan (Cisco Packet Tracer / GNS3)
  ],
  caption: [Skema Jaringan Komputer Usulan],
)
#sumber([Hasil Perancangan Simulasi Peneliti, 2026])

=== Keamanan Jaringan
Uraikan konfigurasi keamanan tingkat lanjut yang diterapkan pada jaringan usulan:
+ *Firewall Filtering & Access Control:* Pembatasan paket berdasarkan IP sumber, IP tujuan, protokol, dan nomor port menggunakan aturan *drop* dan *reject* terstandarisasi.
+ *Port Security & DHCP Snooping:* Mencegah serangan *MAC flooding* serta menangkal keberadaan server DHCP ilegal (*rogue DHCP server*).
+ *Virtual Private Network (VPN):* Implementasi sambungan terowongan terenkripsi (misalnya L2TP/IPsec atau WireGuard) bagi staf yang bekerja jarak jauh (*remote worker*).

=== Rancangan Aplikasi Jaringan
Jelaskan konfigurasi layanan dan aplikasi pendukung jaringan yang dibangun untuk menunjang performa infrastruktur:
+ *Dynamic Host Configuration Protocol (DHCP) Server:* Pengalokasian IP dinamis secara terpisah untuk masing-masing segmen VLAN.
+ *Domain Name System (DNS) Caching:* Meningkatkan kecepatan resolusi nama domain lokal dan internet.
+ *Network Monitoring System (NMS):* Integrasi aplikasi pemonitor (PRTG, The Dude, atau Cacti) dengan protokol SNMP (*Simple Network Management Protocol*) untuk memantau status perangkat secara terpusat.

=== Manajemen Jaringan
Paparkan konfigurasi manajemen *bandwidth* dan penjaminan kualitas layanan (QoS):
+ Penerapan algoritma *Hierarchical Token Bucket* (HTB) atau *Queue Tree* untuk menetapkan batas jaminan minimum (*limit-at*) dan batas maksimum (*max-limit*) untuk tiap divisi kerja.
+ Pembagian prioritas paket data (*packet priority*), menempatkan paket transaksi bisnis utama pada prioritas tertinggi dibandingkan trafik unduhan reguler.

== Pengujian Jaringan
Pengujian dilakukan secara kuantitatif melalui simulasi guna membuktikan kebenaran hipotesis teknis dan efektivitas rancangan usulan terhadap penyelesaian masalah.

=== Pengujian Jaringan Awal
Pengujian awal dilaksanakan sebelum dilakukannya modifikasi jaringan guna membuktikan keberadaan masalah secara terukur:
+ *Uji Konektivitas & Latensi:* Perintah `ping` dan `traceroute` saat trafik sibuk untuk merekam waktu tunda (*delay*) dan persentase paket hilang (*packet loss*).
+ *Pencatatan Parameter QoS:* Menggunakan aplikasi pemonitor (*Wireshark* atau *PRTG*) untuk mengukur performa awal.

#figure(
  table(
    columns: (0.8cm, 3.5cm, 2.5cm, 2.5cm, 2.5cm, 2cm),
    stroke: 0.5pt + black,
    align: (center, left, center, center, center, center),
    [*No*], [*Skenario Pengujian Awal*], [*Throughput*], [*Packet Loss*], [*Delay*], [*Kategori*],
    [1], [Trafik Klien Divisi A (Unduh)], [450 Kbps], [18.2%], [320 ms], [Kurang],
    [2], [Akses Sistem Transaksi Utama], [120 Kbps], [24.5%], [480 ms], [Buruk],
    [3], [Streaming Video / Pertemuan Daring], [280 Kbps], [15.0%], [290 ms], [Kurang],
  ),
  caption: [Hasil Pengukuran Parameter Jaringan Berjalan (Sebelum Usulan)],
)
#sumber([Hasil Pengujian Awal Peneliti, 2026])

=== Pengujian Jaringan Akhir
Pengujian akhir dilakukan kembali setelah penerapan konfigurasi usulan menggunakan instrumen dan parameter pengukuran yang setara guna membuktikan keberhasilan usulan:

#figure(
  table(
    columns: (0.8cm, 3.5cm, 2.5cm, 2.5cm, 2.5cm, 2cm),
    stroke: 0.5pt + black,
    align: (center, left, center, center, center, center),
    [*No*], [*Skenario Pengujian Akhir*], [*Throughput*], [*Packet Loss*], [*Delay*], [*Kategori*],
    [1], [Trafik Klien Divisi A (VLAN 10)], [2.8 Mbps], [0.2%], [24 ms], [Sangat Bagus],
    [2], [Akses Sistem Transaksi (VLAN 20)], [4.5 Mbps], [0.0%], [12 ms], [Sangat Bagus],
    [3], [Pertemuan Daring (Prioritas QoS)], [3.2 Mbps], [0.5%], [28 ms], [Bagus],
  ),
  caption: [Hasil Pengukuran Parameter Jaringan Usulan (Setelah Implementasi)],
)
#sumber([Hasil Pengujian Akhir Simulasi Peneliti, 2026])

Hasil pengujian akhir membuktikan bahwa perancangan jaringan usulan berhasil mengeliminasi kemacetan trafik, menekan *packet loss* hingga di bawah 1%, dan menjamin ketersediaan *bandwidth* bagi operasional vital instansi.
