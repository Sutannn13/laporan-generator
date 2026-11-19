---
trigger: always_on
description: Protokol wajib Agent saat diminta membuat template baru (Jurnal SINTA 1-6 / Scopus / Laporan PKL), mengerjakan/melanjutkan/mengaudit dokumen laporan/jurnal yang sudah ada dengan Mode Ilmiah (R1-R4 Mendeley Workflow, Ringkas Fokus Topik, Zero Halusinasi, Anti-Revisi), serta mengelola folder contoh template `contoh-template-ai/`.
---

# Protokol Pengarahan Agent: Mode Ilmiah, Jurnal SINTA 1-6 / Scopus, Laporan PKL, Aturan Sakral Pemilik (R1-R4), & Anti-Revisi

Setiap kali pengguna meminta:
- Pembuatan, penulisan, kelanjutan, konversi, atau **Audit / Review** **Jurnal Ilmiah SINTA 1-6**, **Jurnal Scopus**, **Laporan/Proposal PKL UBSI**, **Skripsi / Tugas Akhir**, maupun **Laporan Tugas / Audit / Analitik**,
Agent **WAJIB** menggunakan pintu masuk terpadu [`laporan-generator`](file:///D:/DATA%20SUTAN%20ARLIE%20JOHAN/MATKUL%20S7/MAGANG/project%20laporan%20ai/.agents/skills/laporan-generator/SKILL.md) + [`mode-ilmiah`](file:///D:/DATA%20SUTAN%20ARLIE%20JOHAN/MATKUL%20S7/MAGANG/project%20laporan%20ai/.agents/skills/mode-ilmiah/SKILL.md) bersama [`jurnal-sinta`](file:///D:/DATA%20SUTAN%20ARLIE%20JOHAN/MATKUL%20S7/MAGANG/project%20laporan%20ai/.agents/skills/jurnal-sinta/SKILL.md), serta mengaktifkan [`humanizer-id`](file:///D:/DATA%20SUTAN%20ARLIE%20JOHAN/MATKUL%20S7/MAGANG/project%20laporan%20ai/.agents/skills/humanizer-id/SKILL.md) (`--preset akademik --kampus ubsi`) **secara default KHUSUS untuk naskah berbahasa Indonesia** (nonaktifkan untuk naskah 100% *Academic English* seperti IJAIN/Scopus).

**Hierarki Otoritas Mutlak (Jika Ada Benturan Aturan)**:
1. `Hukum Pemilik (R1-R4) & Pedoman Resmi Kampus/OJS Target` (termasuk SK Rektor UBSI 2026: semua pengarang Skripsi/TA ditulis lengkap tanpa `et al.`)
2. `mode-ilmiah & check_antislop_academic.py`
3. `humanizer-id` (hanya bekerja pada teks/draf `.md`/`.txt` atau ekstraksi teks memori; dilarang menulis Daftar Pustaka ke `.docx` jurnal R1, dilarang membuat berkas liar `humanizer/audit-*.md` / `jurnal/target-jurnal.md` tanpa izin R2).

**Keamanan File In-Place (R2 Atomic Guard)**:
Sebelum menyimpan hasil suntingan *in-place* ke berkas `.docx` milik pengguna, selalu buat salinan cadangan sementara dan gunakan penulisan sementara + *atomic replace* agar file asli tidak rusak bila eksekusi terhenti di tengah.

---

## 1. Hukum Tertinggi Pengerjaan Naskah Jurnal Pemilik (R1-R4 & Prinsip Anti-Revisi)

Saat pemilik meminta agent menulis, melanjutkan, merangkum, atau memperbaiki naskah jurnal (baik dari judul/topik baru maupun dari Laporan PKL/Analitik), aturan **R1 s.d. R4** ini berlaku mutlak di semua AI Agent (Antigravity, OpenCode, KiloCode, Claude, Cursor, Cline, Roo):

1. **R1 - Referensi Itu Sakral, DILARANG Ditulis Agent ke Dalam Dokumen (`.docx`)**:
   - Agent **DILARANG KERAS** menulis bagian `DAFTAR PUSTAKA` / `REFERENSI` / `REFERENCES` beserta daftar entrinya ke dalam file `.docx` naskah jurnal.
   - Daftar Pustaka final di dalam `.docx` ditulis sendiri oleh manusia (pemilik memakai **Mendeley**). Hasil riset referensi agent **HANYA** boleh disimpan di file `.txt` kandidat terpisah sesuai **R3**.
2. **R2 - Satu File Target (*Live In-Place Editing*, Dilarang Buat File `.docx` Baru/Turunan)**:
   - Jika pemilik memberikan satu file `.docx` untuk dikerjakan (misal `kerjaan jurnal\Template JKI.docx`), agent **WAJIB bekerja *live* langsung di file `.docx` itu**.
   - **DILARANG KERAS** membuat file `.docx` baru (termasuk file per-bab seperti `..._Bab1.docx` atau file turunan PDF/PNG) tanpa izin eksplisit pemilik.
3. **R3 - File `.txt` & Dosir `.docx` Kandidat Referensi Terpisah Sesuai Level SINTA Target**:
   - Agent **WAJIB** membuat file `.txt` kandidat referensi terpisah (misal `kerjaan jurnal\kandidat_referensi_sinta5.txt`, serta dosir `.docx` terpisah berhyperlink DOI & PDF bila diminta pengguna).
   - Seluruh kandidat referensi wajib **100% artikel jurnal primer terbitan maksimal 5 tahun terakhir (`2022-2026`)**, memiliki **DOI aktif terverifikasi HTTP 200 di Crossref (`https://doi.org/10....`)**, serta **tautan Download PDF Langsung HTTP 200 (`application/pdf` / header `%PDF-`)**, dan **diutamakan dari jurnal yang level SINTA-nya SETARA dengan jurnal target** (minimal 15 referensi untuk SINTA 2-5 dan minimal 25 untuk SINTA 1).
   - Tiap entri di file `.txt` wajib diberi label level SINTA jurnal sumbernya (`[Peringkat: SINTA 4 - Terverifikasi SINTA Kemdiktisaintek]`); **jika levelnya tidak bisa diverifikasi secara pasti, tulis `[Level SINTA: tidak terverifikasi]`, jangan mengarang**.
4. **R4 - Jurnal Bukan Laporan (Ringkas, Fokus ke Topik, Tidak Kepanjangan, & Data Valid Anti-Revisi)**:
   - Isi naskah jurnal harus **ringkas, padat, fokus ke topik, dan tidak kepanjangan**: penelitian **DIRANGKUM secara analitis**, bukan disalin panjang dari laporan PKL/skripsi (Pendahuluan 4-6 paragraf / 500-750 kata; Metode 3-5 paragraf / 400-650 kata; Hasil & Pembahasan fokus pada bukti & analisis komparatif; Kesimpulan 1-2 paragraf menjawab tujuan).
   - **Zero Halusinasi & Data Valid**: Jangan pernah mengarang angka statistik, hasil uji, nama pasal, atau klaim tanpa bukti. Gunakan data valid dari laporan sumber atau instansi resmi; tandai data yang belum tersedia dengan `[ISI DATA NYATA: ...]` agar naskah tidak terkena revisi dosen/reviewer.
   - Patuhi TOS dan gaya selingkung template jurnal tujuan (untuk **JKI - SINTA 4 LPPM UBSI**: struktur artikel jurnal, layout 2 kolom, gaya sitasi **IEEE `[1]`, `[2]`**, min. 15 referensi di file `.txt`, batas *similarity* maksimal **20%**).

---

## 2. Mode Buat Template / Showcase Jurnal SINTA 1-6 Baru dari Nol (Interaktif Wajib)

Hanya ketika pengguna secara eksplisit meminta pembuatan **template kosong / contoh showcase baru** (bukan mengerjakan file `.docx` target milik pengguna), tanyakan 3 pilihan utama ini:

1. **Pilihan Peringkat Jurnal SINTA (1-6 dari Instansi Berbeda beserta DOI Prefix Resmi)**:
   - **SINTA 1 (Informatika/AI) - IJAIN** (*International Journal of Advances in Intelligent Informatics*): **Universitas Ahmad Dahlan (UAD) Yogyakarta** (`p-ISSN: 2442-6571`, `e-ISSN: 2548-3161`, DOI Prefix: `10.26555/ijain`, Wajib 100% Bahasa Inggris, Default: **2 Kolom**, Min. 25 Referensi)
   - **SINTA 1 (Hukum/Hukum Siber) - PJIH** (*PADJADJARAN Jurnal Ilmu Hukum*): **Fakultas Hukum Universitas Padjadjaran (Unpad)** (`p-ISSN: 2442-9325`, `e-ISSN: 2460-1543`, DOI Prefix: `10.22304/pjih`, Default: **2 Kolom / 1 Kolom**, Min. 25 Referensi)
   - **SINTA 2 - JTIIK** (*Jurnal Teknologi Informasi dan Ilmu Komputer*): **FILKOM Universitas Brawijaya (UB) Malang** (`p-ISSN: 2355-7699`, `e-ISSN: 2528-6579`, DOI Prefix: `10.25126/jtiik`, Default: **2 Kolom**, Min. 15 Referensi)
   - **SINTA 3 - JISKA** (*Jurnal Informatika Sunan Kalijaga*): **UIN Sunan Kalijaga Yogyakarta** (`p-ISSN: 2527-5836`, `e-ISSN: 2528-0074`, DOI Prefix: `10.14421/jiska`, Default: **2 Kolom**, Min. 15 Referensi)
   - **SINTA 4 - JKI** (*Jurnal Khatulistiwa Informatika*): **LPPM Universitas Bina Sarana Informatika (UBSI)** (`p-ISSN: 2339-1928`, `e-ISSN: 2579-633X`, DOI Prefix: `10.31294/jki`, Default: **2 Kolom**, Sitasi: **IEEE**, Min. 15 Referensi, Similarity <= 20%)
   - **SINTA 5 - TEKNOIF** (*Jurnal Teknologi Informasi dan Komputer*): **Institut Teknologi Padang (ITP)** (`p-ISSN: 2338-2724`, `e-ISSN: 2598-9197`, DOI Prefix: `10.21063/jtif`, Default: **2 Kolom**, Min. 12 Referensi)
   - **SINTA 6 - METIK** (*Jurnal Manajemen dan Teknik Informatika*): **LPPM STMIK Jayakarta / Universitas Mulia** (`p-ISSN: 2580-1503`, `e-ISSN: 2654-8135`, DOI Prefix: `10.47002/metik`, Default: **1 Kolom Penuh**, Min. 12 Referensi)
2. **Pilihan Tata Letak Kolom Jurnal**: **Layout Terbagi 2 (`--layout 2col`)**, **Layout Biasa (`--layout 1col`)**, atau **Default Bawaan Jurnal (`--layout default`)**.
3. **Pilihan Gaya Sitasi**: **IEEE Style (`[1]`, `[2]`)** atau **APA Style (`(Penulis, Tahun)`)**.

---

## 3. Aturan Ketat Anti-Slop Jurnal, Tipografi OpenXML, & Etika Publikasi (ARJUNA & COPE)

1. **Bebas Teks "AI Indeks" / Debug Banner**: Dilarang keras menaruh teks `| Peringkat: SINTA X | Layout: 2 Kolom` di badan halaman. Semua metadata jurnal (`Journal Name`, `Vol/No/Tahun`, `p-ISSN`, `e-ISSN`, dan `DOI`) wajib ditempatkan di **Word Header (`w:hdr`)** dan **Footer (`w:ftr`)**, disertai blok **Riwayat Artikel (*Received / Revised / Accepted*)** dan lisensi **CC BY-SA 4.0**.
2. **Superscript Asli, Tipografi Bersih, *Burstiness*, & Anti-Slop**: Gunakan `w:vertAlign="superscript"` untuk indeks afiliasi penulis (`1*`, `2`). Dilarang menggunakan karakter *em dash* (`\u2014`), frasa klise AI (`antislop-copywriting` `R-16`), atau *negative parallelism* berulang (`R-36`). Variasikan panjang kalimat secara alami (`std >= 5.5` kata) agar aman dari detektor AI dan wajib lulus `check_antislop_academic.py`.
3. **Inspeksi Dokumen Existing Sebelum Edit**: Jalankan `$env:PYTHONIOENCODING="utf-8"; uv run generate_sinta_journal_docx.py --inspect-docx "<nama_file.docx>"` (atau dari `<skill_dir>/scripts/`) sebelum mengedit file `.docx` yang sudah ada.
