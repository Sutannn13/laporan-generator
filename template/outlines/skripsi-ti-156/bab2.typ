#import "../../../lib.typ": *

= Landasan Teori

Landasan teori menguraikan konsep dasar, teori ilmiah, dan algoritma yang menjadi fondasi dalam penyelesaian masalah dan pembangunan perangkat lunak. Pembahasan tidak sekadar memuat definisi kamus, melainkan menyajikan telaah mendalam terhadap prinsip kerja teori, formulasi algoritma, serta perangkat pendukung (*tools*) yang digunakan.

== Tinjauan Pustaka

Tinjauan pustaka memuat penjelasan mengenai teori-teori inti pendukung penelitian:

+ *Konsep Dasar Program dan Rekayasa Perangkat Lunak:*\
  Uraikan paradigma pemrograman yang digunakan (misalnya Pemrograman Berorientasi Objek / OOP atau Pemrograman Terstruktur), siklus hidup pengembangan perangkat lunak, serta arsitektur aplikasi (seperti *Model-View-Controller* / MVC).

+ *Metode dan Teori Algoritma:*\
  Paparkan teori komputasi atau algoritma yang diimplementasikan untuk memecahkan masalah (misalnya algoritma pencarian lintasan terpendek, optimasi, graf, klasifikasi, enkripsi, atau pemrosesan data sains). Uraikan formula matematis, notasi komputasi, dan kompleksitas waktu/ruang dari algoritma tersebut.

+ *Pengujian Aplikasi (Software Testing):*\
  Jelaskan konsep dan metode pengujian perangkat lunak yang diterapkan, seperti pengujian unit (*Unit Testing*), pengujian kotak hitam (*Black Box Testing*), atau pengujian penerimaan pengguna (*User Acceptance Test* / UAT) guna memverifikasi integritas fungsi program.

+ *Peralatan Pendukung Sistem (Unified Modelling Language / UML):*\
  Jelaskan teori pemodelan berorientasi objek menggunakan UML beserta notasi dan tujuan penggunaan masing-masing diagram:
  - *Activity Diagram*: Memodelkan aliran alur kerja (_workflow_) dan runtutan proses bisnis sistem.
  - *Use Case Diagram*: Mendefinisikan interaksi antara aktor (*user/system*) dengan fitur-fitur fungsional perangkat lunak.
  - *Sequence Diagram*: Menggambarkan kolaborasi dan pertukaran pesan antar objek berdasarkan urutan waktu.
  - *Class Diagram*: Menggambarkan struktur statis kelas-kelas sistem beserta atribut, operasi, dan relasi antar kelas (apabila aplikasi dibangun secara berorientasi objek).
  - *Deployment Diagram*: Memetakan konfigurasi fisik simpul perangkat keras dan artefak perangkat lunak yang berjalan di dalamnya.

  _Catatan:_ Penerapan diagram UML harus memiliki konsistensi yang ketat terhadap rancangan sistem pada Bab III dan Bab IV.

== Penelitian Terkait

Sub-bab ini menyajikan kajian literatur terhadap penelitian-penelitian terdahulu yang relevan dari jurnal ilmiah nasional maupun internasional bereputasi:

+ Memaparkan perbandingan antara sistem atau aplikasi yang dikembangkan dengan penelitian sejenis yang telah dipublikasikan sebelumnya.
+ Mengidentifikasi kontribusi, perbedaan variabel, pembaruan algoritma, atau peningkatan efisiensi yang ditawarkan oleh penelitian skripsi ini.
+ Menyertakan kutipan pustaka dengan format standar APA (*American Psychological Association*) mengacu pada referensi jurnal minimal 5 tahun terakhir dari tahun berjalan (minimal memuat 5 kutipan jurnal terkait).

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3cm, 4cm, 3.5cm),
    stroke: 0.5pt + black,
    align: (center, left, left, left, left),
    [*No*], [*Peneliti & Tahun*], [*Judul Penelitian*], [*Metode / Algoritma*], [*Hasil & Relevansi*],
    [1], [Pratama & Lestari (2023)], [Penerapan Algoritma Dijkstra Pada Rute Distribusi], [Algoritma Dijkstra], [Mempersingkat waktu tempuh pengiriman hingga 18%],
    [2], [Setiawan dkk. (2024)], [Optimasi Pencarian Jalur Cepat Berbasis Graf], [Graph Search Algorithm], [Peningkatan efisiensi komputasi simpul graf],
    [3], [Rahmawati (2022)], [Sistem Antrean Pelayanan Bengkel Berbasis Mobile], [Waterfall & SQLite], [Menurunkan waktu tunggu riil pelanggan],
    [4], [Kusuma & Hidayat (2025)], [Model Klasifikasi Data Sains Berbasis Web], [Metode Komputasi Sains], [Akurasi pemrosesan data mencapai 92%],
    [5], [Widodo (2023)], [Implementasi REST API Pada Aplikasi Terdistribusi], [Client-Server Architecture], [Integrasi layanan multi-platform yang andal],
  ),
  caption: [Matriks Perbandingan Penelitian Terkait],
)
#sumber([Hasil Kajian Pustaka Peneliti, 2026])
