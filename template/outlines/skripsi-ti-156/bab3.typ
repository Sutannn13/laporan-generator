#import "../../../lib.typ": *

= Analisis dan Perancangan Aplikasi

Bab ini memaparkan gambaran umum instansi atau tempat riset, analisis masalah dan kebutuhan sistem, serta rancangan formal algoritma yang diterapkan dalam pembangunan perangkat lunak.

== Tinjauan Perusahaan
Bila penelitian skripsi dilakukan melalui riset lapangan pada instansi atau perusahaan, uraikan gambaran umum tempat riset tersebut. Pada halaman lampiran, kegiatan ini dibuktikan dengan Surat Keterangan Riset ber-kop resmi, bermaterai/berstempel, dan ditandatangani pejabat yang berwenang. Jika riset dilakukan di lebih dari satu tempat, cukup tampilkan salah satu tinjauan instansi utama saja.

=== Sejarah Perusahaan
Uraikan sejarah singkat berdirinya instansi atau perusahaan, visi dan misi organisasi, bidang usaha atau pelayanan publik yang dijalankan, serta perkembangan teknologi informasi yang diterapkan di lingkungan kerja tersebut.

=== Struktur Organisasi
Gambarkan bagan struktur organisasi instansi atau perusahaan beserta pembagian tugas, fungsi pokok, wewenang, dan tanggung jawab masing-masing bagian yang berhubungan langsung dengan operasional sistem.

#figure(
  rect(width: 85%, height: 5.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Bagan Struktur Organisasi Instansi / Perusahaan
  ],
  caption: [Struktur Organisasi Instansi],
)
#sumber([Profil Organisasi Instansi, 2026])

== Analisis Aplikasi
Bagian ini menyajikan analisis komprehensif mengenai permasalahan sistem dan rumusan kebutuhan perangkat lunak yang dirancang.

=== Analisis Masalah
Uraikan hasil analisis terhadap sistem yang sedang berjalan, kendala operasional yang dihadapi, serta akar penyebab timbulnya inefisiensi. Jelaskan solusi alternatif yang ditawarkan melalui pembangunan perangkat lunak aplikasi berbasis sains/komputasi cerdas.

=== Analisis Kebutuhan
Rumuskan spesifikasi kebutuhan sistem yang wajib dipenuhi oleh perangkat lunak yang dibangun, mencakup:
+ *Kebutuhan Fungsional (Functional Requirements):*
  - Kemampuan sistem mengolah data masukan dan memproses kalkulasi algoritma.
  - Pengelolaan hak akses pengguna (*User Role Authentication*).
  - Penyajian visualisasi hasil pemrosesan dan pembuatan laporan periodik.
+ *Kebutuhan Non-Fungsional (Non-Functional Requirements):*
  - Keandalan (*Reliability*) dan ketersediaan sistem saat menangani transaksi data.
  - Keamanan akses data (*Security*) dan validasi masukan pengguna.
  - Kompatibilitas terhadap platform target (*Usability & Compatibility*).

== Rancangan Algoritma
Pada sub-bab ini diuraikan secara formal mengenai model matematis dan logika algoritma yang digunakan untuk menyelesaikan permasalahan kasus yang diteliti.

Sebagai ilustrasi pemodelan sains, berikut contoh spesifikasi formal algoritma lintasan terpendek (*Dijkstra Algorithm*) pada graf berbobot positif $G = (V, E)$:

```pascal
Procedure Dijkstra(G: Weighted connected simple graph, with all weight positive)
{ G memiliki simpul-simpul a = v0, v1, ..., vn = z dan bobot w(vi, vj) }
{ di mana w(vi, vj) = tak hingga jika {vi, vj} bukan sisi dalam graf G }
for i := 1 to n
    L(vi) := infinity
L(a) := 0
S := empty_set
{ Label awal diinisialisasi: simpul awal bernilai 0 dan simpul lain bernilai tak hingga }

while z not in S
begin
    u := simpul bukan anggota S dengan L(u) minimal
    S := S union {u}
    for all simpul v bukan anggota S
        if L(u) + w(u, v) < L(v) then
            L(v) := L(u) + w(u, v)
        { Memperbarui label jarak minimum simpul yang bertetangga }
end
{ L(z) adalah panjang lintasan terpendek dari simpul a ke simpul z }
```

Paparkan variabel, representasi himpunan simpul, dan matriks ketetanggaan (*adjacency matrix*) yang menjadi masukan bagi algoritma di atas sesuai dengan kasus nyata yang dianalisis dalam penelitian skripsi ini.
