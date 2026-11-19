# Matriks Metodologi Penulisan Ilmiah (PKL UBSI, Audit/Analitik, & Jurnal SINTA 1-6)

Dokumen acuan resmi untuk menyusun bagian **Metode Penelitian**, **Kerangka Analisis**, dan **Struktur Pengujian** sesuai jenis dokumen tanpa menulis definisi buku teks dasar yang bertele-tele.

---

## 1. Laporan / Proposal PKL UBSI (Prodi Teknologi Informasi - S1)

| Jenis / Outline PKL | Metode Pengumpulan Data | Metode Pengembangan / Analisis Teknis | Output & Artefak Wajib |
| :--- | :--- | :--- | :--- |
| **Proposal PKL (3 Bab)** | Observasi awal, wawancara singkat pembimbing lapangan, studi pustaka | Identifikasi masalah sistem berjalan (*root cause*), ruang lingkup, dan rancangan jadwal PKL | Bab I-III + Tabel Jadwal Kerja & Dokumentasi Awal |
| **Outline 1: Proyek Inovasi Perangkat Lunak (6 Bab)** | Observasi langsung, wawancara *stakeholder*, studi dokumentasi SOP | **SDLC (*Waterfall* / *Prototyping* / *Agile Scrum*)**, pemodelan **UML** (*Use Case, Activity, Class, Sequence Diagram*), **ERD & LRS**, dan uji **Black-Box (*Equivalence Partitioning*)** atau **UAT** | Artefak kode/prototipe, Skema Basis Data, Tabel Uji Black-Box |
| **Outline 2: Analisa Program Mobile (4 Bab)** | Observasi alur aplikasi, wawancara pengguna/pengelola, tinjauan dokumentasi API | Analisis arsitektur *client-server*, izin sistem operasi / keamanan (*permissions*), alur UI/UX layar ke layar, dan pengujian fungsional perangkat seluler | Peta Alur Layar, Analisis API/Hak Akses, Tabel Temuan Program |
| **Outline 3: Jaringan Komputer (4 Bab)** | Survei infrastruktur fisik, wawancara administrator jaringan, pengambilan log/trafik | **NDLC (*Network Development Life Cycle*)** atau *Top-Down Network Design*, desain topologi fisik & logis, alokasi IP/VLAN/Routing/Firewall, serta uji **QoS** (*Throughput, Delay, Jitter, Packet Loss* acuan **TIPHON**) | Topologi Jaringan, Tabel Alokasi IP, Grafik & Tabel Nilai QoS |
| **Outline 4: Analisis Sistem (4 Bab)** | Observasi unit kerja, wawancara terstruktur 5W+1H, pengumpulan berkas masukan/keluaran | Kerangka **PIECES** (*Performance, Information, Economy, Control, Efficiency, Service*) atau analisis proses bisnis *As-Is* vs *To-Be* + pemodelan UML sistem berjalan & rancangan solusi usulan | Spesifikasi Dokumen Masukan/Keluaran, Use Case & Activity Diagram, Matriks Masalah & Usulan |

**Aturan Penulisan Metode PKL:**
- Jangan tulis definisi umum seperti *"Menurut Rosa dan Shalahuddin, UML adalah..."* panjang-panjang; langsung jelaskan **objek apa yang diamati**, **siapa narasumbernya**, dan **diagram/alat uji apa yang dipakai pada sistem instansi**.

---

## 2. Laporan Biasa, Makalah Akademik, Laporan Analitik Data, & Audit TI

| Jenis Laporan | Kerangka Metodologi Wajib | Struktur Analisis & Validasi |
| :--- | :--- | :--- |
| **Audit Tata Kelola & Keamanan TI** | **COBIT 2019** (Domain EDM/APO/BAI/DSS/MEA), **ISO/IEC 27001**, atau **OWASP ASVS** | Setiap temuan audit wajib memakai struktur **CCCE (*Condition, Criteria, Cause, Effect*)**, skala **Capability Level (0-5)** terverifikasi, matriks **Risiko (Likelihood x Impact)**, dan konsistensi angka rekapitulasi vs lampiran (diuji lewat `challenge_text_and_math.py`). |
| **Laporan Analitik Data / BI** | **CRISP-DM** (*Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment*) | Jelaskan periode dataset, jumlah baris/sampel bersih, teknik pembersihan (*handling missing value/outlier*), serta pastikan angka di teks narasi cocok 100% dengan tabel dan grafik. |
| **Makalah Kuliah / Kajian Kebijakan** | **BAB I s.d. BAB IV/V** (angka Romawi) dengan pendekatan studi kasus, komparatif, atau analisis deskriptif kualitatif | Fokus pada satu rumusan masalah per sub-bab, didukung minimal 5-10 rujukan jurnal terverifikasi 5 tahun terakhir. |

---

## 3. Jurnal Ilmiah Terakreditasi SINTA 1-6 (Struktur IMRaD Ketat)

Jurnal ilmiah tidak sama dengan laporan PKL. Hapus sejarah instansi berhalaman-halaman dan teori dasar buku teks; rangkum menjadi **3-5 paragraf metode yang padat** sesuai rumpun ilmu:

### A. Rumpun Informatika, Sistem Informasi, & Keamanan Siber
1. **Rekayasa Perangkat Lunak (RPL) & Otomatisasi**:
   - Gunakan **SDLC** (*Waterfall / Prototype / Agile*) + rancangan arsitektur (UML / API) + minimal satu pengujian terukur: **Black-Box Testing**, **ISO/IEC 25010** (*Functional Suitability, Performance Efficiency, Usability, Security*), atau **System Usability Scale (SUS)** dengan jumlah responden nyata.
2. **Kecerdasan Buatan, Data Mining, & Machine Learning**:
   - Gunakan **CRISP-DM** + sebutkan sumber & ukuran dataset secara jujur + skema pembagian data (*Train/Validation/Test* atau *K-Fold Cross Validation*) + metrik evaluasi (**Accuracy, Precision, Recall, F1-Score, ROC-AUC** untuk klasifikasi; **MAE, RMSE, R2** untuk regresi; **Silhouette Score / Davies-Bouldin Index** untuk klastering).
3. **Sistem Pendukung Keputusan (SPK / MCDM)**:
   - Sebutkan kriteria, bobot, alternatif, dan algoritma (**AHP, TOPSIS, SAW, WP, MOORA, atau VIKOR**) secara runtut hingga normalisasi matriks, nilai preferensi akhir, dan uji konsistensi/sensitivitas (`CR <= 0.1` untuk AHP).
4. **Keamanan Siber & Forensik Digital**:
   - Gunakan kerangka **NIST SP 800-86** / **OWASP Mobile Top 10** (*Acquisition, Examination, Analysis, Reporting*) untuk memetakan *attack vector*, izin sistem (`Manifest/AccessibilityService`), alur lalu lintas C2, dan kontrol mitigasi (RASP, FDS, FIDO2).
5. **Evaluasi Penerimaan & Kesuksesan Sistem Informasi**:
   - Gunakan model **TAM**, **UTAUT/UTAUT2**, **EUCS**, atau **DeLone & McLean** disertai ukuran sampel, uji validitas & reliabilitas (Cronbach's Alpha), dan analisis regresi/SEM.

### B. Rumpun Ilmu Hukum, Hukum Siber, & Kebijakan Publik
1. **Penelitian Hukum Normatif (*Doctrinal Legal Research*)**:
   - Wajib menyebut kombinasi pendekatan secara eksplisit: **Pendekatan Perundang-Undangan (*Statute Approach*)**, **Pendekatan Konseptual (*Conceptual Approach*)**, **Pendekatan Kasus (*Case Approach*)**, atau **Pendekatan Perbandingan (*Comparative Approach*)**.
   - Sebutkan bahan hukum primer dengan nomor, tahun, dan pasal pasti (misal: **UU No. 1 Tahun 2023 tentang KUHP Pasal 332-337 & 492**, **UU No. 1 Tahun 2024**, **UU No. 27 Tahun 2022 tentang PDP Pasal 35**, **POJK No. 22 Tahun 2023**) serta teknik penarikan kesimpulan (interpretasi sistematis, gramatikal, teleologis).
2. **Penelitian Hukum Normatif-Empiris (*Socio-Legal*)**:
   - Gabungkan telaah norma hukum positif dengan data penegakan hukum (*law in action*) dari Kepolisian (Subdit Siber/Dittipidsiber), OJK/LAPS SJK, atau putusan pengadilan yang dapat diverifikasi.

---

## 4. Kunci Benang Merah Anti-Revisi (*Golden Thread*)

Setiap artikel jurnal dan laporan wajib lolos pemeriksaan 1-ke-1 berikut sebelum masuk gerbang **Peer Reviewer (Fase 4)**:
`Judul <-> Tujuan di Akhir Pendahuluan <-> Tahapan di Metode <-> Bukti/Tabel di Hasil & Pembahasan <-> Jawaban di Kesimpulan`.
Jika ada data numerik atau responden yang belum dimiliki pengguna, tandai jujur dengan `[ISI DATA NYATA: ...]` dan **dilarang keras mengarang angka**.
