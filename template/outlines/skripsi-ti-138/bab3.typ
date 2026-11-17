#import "../../../lib.typ": *

= Metodologi Penelitian

Bab ini menguraikan kerangka kerja sistematis yang ditempuh dalam pelaksanaan penelitian, instrumen yang digunakan, karakteristik populasi dan penentuan sampel, serta tahapan pemrosesan dan analisis data.

== Tahapan Penelitian
Jelaskan alur tahapan penelitian secara runtut mulai dari tahap awal perumusan masalah hingga penarikan kesimpulan akhir:
+ *Tahap Inisiasi:* Identifikasi masalah, studi kepustakaan, dan perumusan hipotesis penelitian.
+ *Tahap Pengumpulan Data:* Penyusunan instrumen, penentuan sampel, dan akuisisi data lapangan.
+ *Tahap Pra-Pemrosesan Data (_Data Preprocessing_):* Pembersihan data (*data cleaning*), penanganan nilai hilang (*missing values*), normalisasi, dan transformasi data.
+ *Tahap Pemodelan dan Analisis:* Penerapan metode algoritma komputasi atau formula statistik untuk mengolah dataset.
+ *Tahap Evaluasi dan Validasi:* Pengukuran kinerja model menggunakan metrik evaluasi ilmiah (*confusion matrix*, akurasi, presisi, recall, RMSE, atau uji signifikansi p-value).
+ *Tahap Penarikan Kesimpulan:* Interpretasi temuan penelitian dan penyusunan rekomendasi.

#figure(
  rect(width: 85%, height: 5.5cm, stroke: 1pt + black)[
    #set align(center + horizon)
    Diagram Alir Kerangka Kerja / Tahapan Penelitian Ilmiah
  ],
  caption: [Diagram Alir Tahapan Penelitian],
)
#sumber([Hasil Rancangan Alur Penelitian, 2026])

== Instrumen Penelitian
Uraikan alat bantu yang dirancang dan digunakan oleh peneliti agar kegiatan pengumpulan data berjalan secara objektif dan sistematis:
+ *Instrumen Pengumpulan Data:* Kuesioner terstruktur dengan skala Likert, panduan wawancara mendalam, lembar observasi lapangan, atau skrip otomatis (*web scraping/API crawler*).
+ *Instrumen Perangkat Keras dan Perangkat Lunak:* Spesifikasi workstation komputasi, sistem operasi, serta lingkungan terintegrasi (*IDE/notebook*) yang digunakan untuk mengeksekusi analisis data.

== Metode Pengumpulan Data, Populasi, dan Sampel Penelitian
Bagian ini merinci teknik pengumpulan data lapangan serta penentuan subjek penelitian:
+ *Populasi Penelitian:* Keseluruhan entitas atau data transaksi yang memiliki karakteristik tertentu yang menjadi fokus penyelidikan.
+ *Sampel Penelitian & Teknik Sampling:* Jumlah sampel yang dipilih serta teknik pengambilan sampel (misalnya *Probability Sampling*, *Stratified Random Sampling*, atau *Purposive Sampling*). Sertakan rumus perhitungan ukuran sampel (seperti rumus Slovin atau formula Cochran):

  $ n = N / (1 + N e^2) $

+ *Prosedur Pengumpulan Data:* Pelaksanaan pengamatan, wawancara, dan verifikasi keabsahan dokumen data di lokasi penelitian.

== Metode Analisis Data
Jelaskan prosedur matematis dan komputasional dalam mengolah data mentah menjadi wawasan informasi baru yang bermakna:
+ *Teknik Analisis Deskriptif:* Perhitungan mean, median, standar deviasi, dan visualisasi distribusi frekuensi data.
+ *Teknik Analisis Inferensial / Algoritmik:* Uji asumsi klasik (normalitas, linearitas, multikolinearitas), eksekusi algoritma pemodelan, serta pengujian signifikansi hipotesis penelitian pada tingkat kepercayaan tertentu (misalnya $alpha = 0.05$).
