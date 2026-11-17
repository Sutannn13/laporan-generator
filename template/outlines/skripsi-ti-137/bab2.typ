#import "../../../lib.typ": *

= Landasan Teori

Bab ini menguraikan konsep dasar, prinsip kerja arsitektur jaringan komputer, protokol komunikasi data, manajemen alokasi sumber daya jaringan, sistem pertahanan keamanan, serta perangkat bantu simulasi yang menjadi rujukan ilmiah penelitian. Seluruh pembahasan wajib merujuk pada sumber literatur tepercaya (buku ilmiah dan jurnal bereputasi).

== Tinjauan Pustaka

Tinjauan pustaka memuat telaah mendalam terhadap konsep-konsep teknis rekayasa jaringan:

+ *Konsep Arsitektur dan Model Referensi Jaringan:*\
  Jelaskan prinsip transmisi data pada model referensi OSI (*Open Systems Interconnection*) 7-Layer dan arsitektur protokol TCP/IP. Uraikan fungsi enkapsulasi, penomoran port, serta format *header* paket pada lapisan jaringan (*Network Layer*) dan lapisan transpor (*Transport Layer*).

+ *Topologi dan Protokol Perutean (Routing Protocols):*\
  Jelaskan konsep topologi fisik dan logis, mekanisme segmentasi jaringan (*Virtual Local Area Network* / VLAN, *Inter-VLAN Routing*), serta protokol perutean dinamis (seperti OSPF, EIGRP, atau BGP) yang mengatur pertukaran tabel rute secara adaptif.

+ *Manajemen Bandwidth dan Quality of Service (QoS):*\
  Paparkan teori manajemen antrean paket (*Queue Management*, *Token Bucket*, *Simple Queue*, atau *Queue Tree*) serta parameter baku pengukuran QoS sesuai standar TIPHON (*Telecommunications and Internet Protocol Harmonization Over Networks*): *throughput*, *packet loss*, *delay/latency*, dan *jitter*.

+ *Sistem Keamanan Jaringan Komputer:*\
  Uraikan konsep pertahanan berlapis (*defense-in-depth*), *Access Control List* (ACL), *Stateful Firewall*, sistem deteksi dan pencegahan intrusi (IDS/IPS seperti Snort/Suricata), serta tunneling terenkripsi (*Virtual Private Network* / VPN IPsec atau WireGuard).

+ *Perangkat Lunak Simulasi dan Monitoring Jaringan:*\
  Jelaskan fungsi dan lingkungan operasional perangkat lunak simulasi (*Cisco Packet Tracer*, *GNS3*, atau *EVE-NG*) serta aplikasi pemonitor jaringan (*PRTG Network Monitor*, *The Dude*, atau *Wireshark*) yang digunakan dalam pengujian.

== Penelitian Terkait

Sub-bab ini menyajikan matriks telaah kritis terhadap minimal 5 artikel jurnal ilmiah nasional terakreditasi atau internasional bereputasi dalam 5 tahun terakhir, menggunakan format kutipan standar APA (*American Psychological Association*):

+ Mengkaji persamaan dan perbedaan metodologi, topologi usulan, serta teknik optimasi yang dikembangkan pada penelitian sejenis.
+ Menjelaskan kontribusi dan keunggulan konfigurasi yang diusulkan pada skripsi ini.

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3cm, 4cm, 3.5cm),
    stroke: 0.5pt + black,
    align: (center, left, left, left, left),
    [*No*], [*Peneliti & Tahun*], [*Judul Penelitian*], [*Metode / Protokol*], [*Temuan Kunci*],
    [1], [Hidayat & Saputra (2023)], [Optimasi Kinerja Jaringan Berbasis OSPF & VLAN], [OSPF Multi-Area & VLAN Tagging], [Mengurangi latensi routing hingga 22%],
    [2], [Wibowo dkk. (2024)], [Implementasi Firewall & Port Knocking Mikrotik], [Stateful Firewall & Port Knocking], [Mencegah serangan brute-force SSH secara efektif],
    [3], [Kurniawan (2022)], [Analisis QoS Manajemen Bandwidth Metode HTB], [Hierarchical Token Bucket], [Packet loss turun ke kategori sangat bagus (< 1%)],
    [4], [Pradana & Pratama (2025)], [Penerapan Site-to-Site IPsec VPN untuk Multi-Branch], [IPsec Tunneling AES-256], [Komunikasi antar cabang aman tanpa bocor data],
    [5], [Sari dkk. (2023)], [Monitoring Jaringan Komputer Menggunakan SNMP], [SNMP v3 & PRTG Network Monitor], [Notifikasi gangguan terpantau secara real-time],
  ),
  caption: [Matriks Sintesis Penelitian Terkait Jaringan Komputer],
)
#sumber([Hasil Kajian Pustaka Peneliti, 2026])
