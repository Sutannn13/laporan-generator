#import "../../../lib.typ": *

= Hasil Penelitian dan Pembahasan

Bab ini menyajikan pemaparan komprehensif mengenai data yang dikumpulkan, langkah-langkah perhitungan metode, penyajian hasil analisis dalam bentuk tabel maupun grafik, serta telaah interpretatif yang tajam terhadap temuan penelitian dibandingkan dengan penelitian terdahulu.

== Deskripsi Data dan Dataset Penelitian
Uraikan karakteristik data yang dianalisis dalam penelitian:
+ *Sumber Data:* Data primer yang diperoleh melalui instrumen kuesioner/wawancara, atau data sekunder dari pangkalan data organisasi/repositori publik.
+ *Struktur Atribut:* Rincian atribut atau variabel dalam dataset, tipe data, rentang nilai, serta jumlah baris data yang digunakan setelah tahapan pra-pemrosesan (*data cleaning*).

#figure(
  table(
    columns: (0.8cm, 3.5cm, 2.5cm, 3cm, 1fr),
    stroke: 0.5pt + black,
    align: (center, left, left, center, left),
    [*No*], [*Atribut Data*], [*Tipe Data*], [*Rentang Nilai*], [*Deskripsi Fungsional*],
    [1], [id_responden], [Nominal], [R001 - R150], [Pengidentifikasi unik subjek sampel],
    [2], [skor_kemudahan], [Ordinal], [1 s.d. 5], [Tingkat persepsi kemudahan penggunaan],
    [3], [frekuensi_akses], [Numerik], [1 s.d. 60], [Jumlah frekuensi pemakaian per bulan],
    [4], [status_adopsi], [Biner], [Ya / Tidak], [Variabel target keputusan adopsi sistem],
  ),
  caption: [Struktur Dataset Penelitian Ilmiah],
)
#sumber([Hasil Pengolahan Dataset Penelitian, 2026])

== Implementasi Metode dan Perhitungan Analisis
Sajikan rincian teknis pelaksanaan analisis data:
+ *Langkah Komputasi:* Tampilkan tahapan pembobotan, normalisasi matriks, atau perulangan iterasi algoritma yang mengeksekusi data penelitian.
+ *Contoh Perhitungan Sampel:* Tampilkan formula komputasi secara transparan pada salah satu baris sampel data untuk membuktikan keabsahan kalkulasi.

== Hasil Pengujian Hipotesis dan Kinerja Model
Sajikan ringkasan hasil kalkulasi dan pengujian hipotesis penelitian:
+ *Metrik Evaluasi:* Sajikan tabel performa akurasi, presisi, recall, $F_1$-score, atau nilai koefisien determinasi ($R^2$).
+ *Uji Signifikansi Statistik:* Paparkan nilai statistik uji (t-hitung, F-hitung, atau $chi^2$) serta perbandingannya dengan nilai tabel pada derajat kebebasan dan taraf signifikansi tertentu ($p < 0.05$).

#figure(
  table(
    columns: (0.8cm, 3.5cm, 2.5cm, 2.5cm, 2.5cm, 2cm),
    stroke: 0.5pt + black,
    align: (center, left, center, center, center, center),
    [*No*], [*Hipotesis Penelitian*], [*Koefisien*], [*t-statistik*], [*p-value*], [*Kesimpulan*],
    [1], [Pengaruh Variabel X1 terhadap Y], [0.428], [4.152], [0.001], [Diterima],
    [2], [Pengaruh Variabel X2 terhadap Y], [0.315], [3.284], [0.003], [Diterima],
    [3], [Pengaruh Variabel X3 terhadap Y], [0.187], [1.995], [0.048], [Diterima],
  ),
  caption: [Hasil Uji Signifikansi Hipotesis Penelitian],
)
#sumber([Hasil Olah Data Statistik Peneliti, 2026])

== Pembahasan dan Analisis Komparatif
Pada bagian pembahasan, lakukan analisis kritis dan interpretasi mendalam terhadap hasil yang telah diperoleh:
+ *Makna Ilmiah Temuan:* Jelaskan faktor-faktor yang menyebabkan variabel tertentu memiliki pengaruh signifikan atau dominan terhadap masalah yang diteliti.
+ *Perbandingan dengan Penelitian Terdahulu:* Diskusikan keselarasan maupun pertentangan temuan ini dengan hasil penelitian-penelitian sebelumnya yang telah diulas pada Bab II.
+ *Implikasi Praktis dan Pemecahan Masalah:* Uraikan bagaimana temuan ilmiah ini memberikan solusi nyata terhadap kendala yang dihadapi objek penelitian di lapangan.
