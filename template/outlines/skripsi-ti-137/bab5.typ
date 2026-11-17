#import "../../../lib.typ": *

= Penutup

== Kesimpulan
Berdasarkan hasil analisis jaringan berjalan, perancangan arsitektur jaringan usulan, simulasi pengujian awal, dan pengujian akhir yang telah dilaksanakan, dapat dirumuskan beberapa kesimpulan pokok sebagai berikut:
+ Infrastruktur jaringan berjalan pada objek riset mengalami kendala kongesti lalu lintas data dan kerentanan keamanan akibat ketiadaan segmentasi jaringan dan pembagian kapasitas *bandwidth* yang merata.
+ Perancangan jaringan usulan dengan penerapan *Virtual LAN* (VLAN), manajemen antrean *Hierarchical Token Bucket* (HTB), dan penyaringan *firewall* terbukti efektif menata lalu lintas data secara terisolasi dan proporsional.
+ Hasil simulasi pengujian akhir menunjukkan peningkatan performa yang sangat signifikan, di mana tingkat kehilangan paket (*packet loss*) berhasil ditekan hingga di bawah 1%, latensi transmisi berkurang drastis, dan stabilitas konektivitas terjamin sesuai standar TIPHON.

== Saran
Untuk menjamin kesinambungan dan keandalan sistem jaringan di masa yang akan datang, penulis memberikan sejumlah rekomendasi strategis yang terbagi ke dalam tiga aspek:

+ *Aspek Manajerial:*\
  Manajemen instansi disarankan untuk menetapkan kebijakan keamanan informasi (*Information Security Policy*) yang mengatur hak akses staf terhadap jaringan, serta menyelenggarakan pelatihan operasional rutin bagi staf teknis dalam menangani insiden jaringan.

+ *Aspek Sistem:*\
  Pada pengembangan sistem selanjutnya, disarankan untuk mengimplementasikan teknologi *Multi-Protocol Label Switching* (MPLS) atau *Software-Defined Wide Area Network* (SD-WAN), serta memasang sistem deteksi intrusi otomatis (*Intrusion Prevention System* / IPS) guna memperkuat ketahanan perimeter jaringan institusi.

+ *Aspek Penelitian Lanjutan:*\
  Bagi peneliti berikutnya, disarankan untuk meneliti perbandingan performa protokol perutean dinamis lain (seperti IS-IS atau BGP) pada skala topologi multi-gedung yang lebih kompleks, atau mengeksplorasi otomasi konfigurasi jaringan berbasis skrip Python dan Ansible.
