#import "../../../lib.typ": *

= Implementasi dan Pengujian Software

Bab ini menguraikan realisasi desain basis data, arsitektur perangkat lunak, antarmuka pengguna, pembentukan kode (*code generation*), pengujian modul program (*testing*), serta lingkungan pendukung instalasi dan publikasi software.

== Desain

=== Database
Paparkan rancangan basis data yang digunakan untuk mendukung penyimpanan data aplikasi:
+ *Entity Relationship Diagram (ERD) / Skema Relasi:* Memetakan entitas data, atribut primer/asing, dan derajat relasi antar tabel.
+ *Kamus Data / Spesifikasi Tabel:* Menjelaskan struktur rinci setiap field (nama field, tipe data, panjang ukuran, keterangan fungsi).

#figure(
  table(
    columns: (0.8cm, 3.5cm, 2.5cm, 2cm, 1fr),
    stroke: 0.5pt + black,
    align: (center, left, left, center, left),
    [*No*], [*Nama Field*], [*Tipe Data*], [*Ukuran*], [*Keterangan*],
    [1], [id_pengguna], [VARCHAR], [10], [Kunci Primer (_Primary Key_)],
    [2], [nama_lengkap], [VARCHAR], [100], [Nama lengkap akun pengguna],
    [3], [kata_sandi], [VARCHAR], [255], [Hash kredensial autentikasi],
    [4], [level_akses], [ENUM], [-], [Hak akses (_admin/operator/user_)],
  ),
  caption: [Struktur Tabel Pengguna Sistem],
)
#sumber([Hasil Rancangan Basis Data, 2026])

=== Software Architecture
Pada sub-bab ini diuraikan pseudocode dan diagram arsitektur alur pemrosesan algoritma yang diimplementasikan pada perangkat lunak.

Berikut adalah pseudocode algoritma lintasan terpendek pada arsitektur perangkat lunak yang dibangun:

```python
def dijkstra(graph, source):
    # Inisialisasi jarak simpul
    dist = {vertex: float('infinity') for vertex in graph}
    previous = {vertex: None for vertex in graph}
    dist[source] = 0
    q = list(graph.keys())

    while q:
        # Ambil simpul dalam himpunan Q dengan nilai jarak terkecil
        u = min(q, key=lambda vertex: dist[vertex])
        if dist[u] == float('infinity'):
            break
        q.remove(u)

        # Perbarui jarak ketetanggaan
        for neighbor, weight in graph[u].items():
            if neighbor in q:
                alt = dist[u] + weight
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    previous[neighbor] = u

    return dist, previous
```

=== User Interface
Menampilkan dan menjelaskan rancangan antarmuka pengguna (*User Interface*) dari form-form utama sistem, alur navigasi menu, dan responsivitas tampilan.

#figure(
  rect(width: 85%, height: 6cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Mockup / Tangkapan Layar Tampilan Antarmuka Form Utama Sistem
  ],
  caption: [Rancangan Antarmuka Menu Utama Aplikasi],
)
#sumber([Hasil Desain Antarmuka Sistem, 2026])

== Code Generation
Bagian ini menyajikan implementasi kode program:
+ Apabila perangkat lunak dikembangkan dengan paradigma Pemrograman Berorientasi Objek (OOP), tampilkan representasi struktur *class*, pewarisan (*inheritance*), dan enkapsulasi modul utama.
+ Apabila dikembangkan dengan paradigma Terstruktur, tampilkan *listing program* pada modul fungsional atau fungsi pemrosesan utama yang mengeksekusi logika algoritma inti.

== Testing
Pengujian modul perangkat lunak dilakukan untuk memastikan fungsionalitas aplikasi bebas dari cacat logika dan sesuai dengan spesifikasi kebutuhan yang ditetapkan. Metode pengujian dapat menggunakan pengujian unit (*Unit Testing*) maupun pengujian kotak hitam (*Black Box Testing*).

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3.5cm, 3.5cm, 2cm),
    stroke: 0.5pt + black,
    align: (center, left, left, left, center),
    [*No*], [*Skenario Pengujian*], [*Masukan / Aksi*], [*Hasil yang Diharapkan*], [*Status*],
    [1], [Autentikasi Login], [Input user dan password valid], [Masuk ke halaman dashboard sesuai hak akses], [Valid],
    [2], [Validasi Form Input], [Kosongkan field wajib simpan], [Sistem menampilkan pesan peringatan data kosong], [Valid],
    [3], [Kalkulasi Algoritma], [Pilih titik awal dan tujuan], [Sistem menampilkan rute terpendek dengan akurat], [Valid],
    [4], [Cetak Laporan], [Klik tombol cetak PDF laporan], [Dokumen laporan terunduh rapi berformat standar], [Valid],
  ),
  caption: [Hasil Pengujian Black Box Testing],
)
#sumber([Hasil Pengujian Sistem, 2026])

== Support
Menjelaskan infrastruktur pendukung pengoperasian perangkat lunak di lingkungan produksi.

=== Publikasi Software
Jelaskan media atau target publikasi di mana perangkat lunak akan dijalankan (misalnya berbasis Web server dengan protokol HTTPS, aplikasi Desktop mandiri, aplikasi Android terdistribusi pada Google Play Store, atau lingkungan *cloud container*).

=== Spesifikasi Hardware dan Software
Rincikan kebutuhan minimum perangkat keras dan perangkat lunak yang wajib dipenuhi untuk menjalankan sistem:

1. *Spesifikasi Perangkat Keras (Hardware):*
   + Prosesor : Minimal Multi-Core 2.0 GHz (atau setara).
   + Memori RAM : Minimal 4 GB (Disarankan 8 GB).
   + Ruang Penyimpanan : Minimal 500 MB ruang kosong SSD/HDD.
   + Resolusi Layar : Minimal 1366 x 768 piksel.

2. *Spesifikasi Perangkat Lunak (Software):*
   + Sistem Operasi : Windows 10/11, Linux Ubuntu 22.04 LTS, atau macOS Monterey.
   + Web Server / Runtime : Node.js v20+ / Apache HTTP Server / Python 3.11+.
   + Basis Data : MySQL v8.0 / PostgreSQL v15 / SQLite3.
   + Web Browser : Google Chrome / Mozilla Firefox / Microsoft Edge versi mutakhir.
