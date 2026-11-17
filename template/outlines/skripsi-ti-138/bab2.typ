#import "../../../lib.typ": *

= Landasan Teori

Bab ini menguraikan teori-teori dasar, formulasi ilmiah, penelitian terdahulu, serta profil objek kajian yang mendukung fokus penelitian ilmiah ini. Pembahasan diarahkan pada konsep dasar metodologi, pembuktian matematis/komputasional, serta perangkat bantu pengolahan data yang digunakan.

== Tinjauan Pustaka
Tinjauan pustaka memuat telaah teoritis terhadap konsep-konsep kunci yang digunakan dalam memecahkan masalah penelitian:

+ *Konsep Teori Utama dan Variabel Penelitian:*\
  Paparkan definisi operasional, konstruk teoritis, dan karakteristik masing-masing variabel yang diamati dalam penelitian. Jelaskan hubungan logis antar variabel berdasarkan rujukan pustaka yang diakui.

+ *Metode Analisis dan Algoritma Ilmiah:*\
  Jelaskan prinsip kerja metode komputasi, algoritma machine learning, atau teknik analisis statistik yang diterapkan (misalnya metode klasifikasi, regresi, pengelompokan (*clustering*), pengujian hipotesis, atau uji korelasi). Sertakan notasi matematis yang melandasi metode tersebut:
  
  $ y = beta_0 + sum_(i=1)^n beta_i x_i + epsilon $

+ *Perangkat Lunak Pengolahan dan Komputasi Data:*\
  Uraikan komponen perangkat lunak atau pustaka bahasa pemrograman yang digunakan untuk pemrosesan data (seperti Python, R, SPSS, pandas, scikit-learn, atau RapidMiner) beserta parameter konfigurasinya.

== Penelitian Terkait
Bagian ini memaparkan kajian literatur terhadap sedikitnya 5 publikasi jurnal ilmiah sejenis dalam kurun waktu 5 tahun terakhir, dengan sitasi standar APA (*American Psychological Association*):

+ Menjelaskan persamaan, perbedaan, dan celah penelitian (*research gap*) antara penelitian yang telah terbit dengan penelitian yang sedang dilaksanakan.
+ Mengidentifikasi kontribusi baru yang diusulkan oleh penulis.

#figure(
  table(
    columns: (0.8cm, 3.5cm, 3cm, 4cm, 3.5cm),
    stroke: 0.5pt + black,
    align: (center, left, left, left, left),
    [*No*], [*Peneliti & Tahun*], [*Judul Publikasi*], [*Metode / Model*], [*Temuan & Batasan*],
    [1], [Suryanto dkk. (2023)], [Analisis Data Mining Pola Transaksi Penjualan], [Metode Asosiasi], [Akurasi aturan asosiasi mencapai 85%],
    [2], [Wijaya & Hartono (2024)], [Perbandingan Algoritma Klasifikasi Data], [Decision Tree & Naive Bayes], [Naive Bayes unggul pada dataset berdimensi tinggi],
    [3], [Putri (2022)], [Penerapan Analisis Regresi Pada Kinerja Layanan], [Regresi Linier Berganda], [Menemukan korelasi positif variabel layanan],
    [4], [Handayani dkk. (2025)], [Model Pengelompokan Data Mahasiswa], [K-Means Clustering], [Terbentuk 3 klaster performa akademik],
    [5], [Nugroho (2023)], [Evaluasi Model Prediksi Berbasis Sentimen], [Support Vector Machine], [Tingkat presisi analisis sentimen 89%],
  ),
  caption: [Matriks Sintesis Penelitian Terkait],
)
#sumber([Hasil Tinjauan Pustaka Peneliti, 2026])

== Tinjauan Organisasi/Objek Penelitian
Uraikan gambaran umum mengenai institusi, komunitas, atau objek yang dijadikan tempat pengambilan data penelitian ilmiah:
+ *Profil Objek Penelitian:* Sejarah singkat, lingkup operasional, visi dan misi, atau deskripsi domain tempat data dikumpulkan.
+ *Karakteristik Lingkungan Data:* Kondisi infrastruktur pencatatan data dan relevansinya terhadap topik skripsi yang diteliti.
