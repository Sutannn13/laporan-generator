---
trigger: always_on
description: Protokol wajib Laporan Generator (skill terpadu), Mode Ilmiah, Jurnal SINTA 1-6/Scopus, Laporan PKL/Skripsi UBSI, aturan R1-R4 Mendeley, & Anti-Revisi
---

# Protokol Pengarahan Agent: Skill Terpadu `laporan-generator` (Mode Ilmiah, Jurnal SINTA 1-6 / Scopus, PKL & Skripsi UBSI, Aturan R1-R4, & Anti-Revisi)

Setiap kali pengguna meminta pembuatan, penulisan, kelanjutan, konversi, atau **Audit / Review** **Jurnal Ilmiah SINTA 1-6**, **Jurnal Scopus**, **Laporan/Proposal PKL UBSI**, **Skripsi / Tugas Akhir**, maupun **Laporan Tugas / Audit / Analitik**, Agent **WAJIB** mengaktifkan skill tunggal terpadu `laporan-generator` (`.agents/skills/laporan-generator/SKILL.md` atau direktori skill global), lalu memuat rujukan on-demand yang relevan dari `references/` (`mode-ilmiah.md`, `jurnal-sinta.md`, `matriks-metodologi-ilmiah.md`, `antislop-akademik-id.md`, dan `humanizer-id.md` khusus naskah Bahasa Indonesia; nonaktifkan `humanizer-id.md` untuk naskah 100% *Academic English* seperti IJAIN/Scopus).

**Hierarki Otoritas Mutlak (Jika Ada Benturan Aturan)**:
1. `Hukum Pemilik (R1-R4) & Pedoman Resmi Kampus/OJS Target` (termasuk SK Rektor UBSI 2026: semua pengarang Skripsi/TA ditulis lengkap tanpa `et al.`)
2. `mode-ilmiah & check_antislop_academic.py`
3. `humanizer-id` (hanya bekerja pada teks/draf `.md`/`.txt` atau ekstraksi teks memori; dilarang menulis Daftar Pustaka ke `.docx` jurnal R1, dilarang membuat berkas liar `humanizer/audit-*.md` / `jurnal/target-jurnal.md` tanpa izin R2).

**Keamanan File In-Place (R2 Atomic Guard)**:
Sebelum menyimpan hasil suntingan *in-place* ke berkas `.docx` milik pengguna, selalu buat salinan cadangan sementara dan gunakan penulisan sementara + *atomic replace* (`atomic_save_docx`) agar file asli tidak rusak bila eksekusi terhenti di tengah.

---

## 1. Hukum Tertinggi Pengerjaan Naskah Jurnal Pemilik (R1-R4 & Prinsip Anti-Revisi)

1. **R1 - Referensi Itu Sakral, DILARANG Ditulis Agent ke Dalam Dokumen (`.docx`)**:
   - Agent **DILARANG KERAS** menulis bagian `DAFTAR PUSTAKA` / `REFERENSI` / `REFERENCES` beserta daftar entrinya ke dalam file `.docx` naskah jurnal.
   - Daftar Pustaka final di dalam `.docx` ditulis sendiri oleh manusia (pemilik memakai **Mendeley**). Hasil riset referensi agent **HANYA** boleh disimpan di file `.txt` kandidat terpisah sesuai **R3**.
2. **R2 - Satu File Target (*Live In-Place Editing*, Dilarang Buat File `.docx` Baru/Turunan)**:
   - Jika pemilik memberikan satu file `.docx` untuk dikerjakan (misal `Template JKI.docx`), agent **WAJIB bekerja *live* langsung di file `.docx` itu**.
   - **DILARANG KERAS** membuat file `.docx` baru (termasuk file per-bab seperti `..._Bab1.docx` atau file turunan PDF/PNG) tanpa izin eksplisit pemilik.
3. **R3 - File `.txt` & Dosir `.docx` Kandidat Referensi Terpisah Sesuai Level SINTA Target**:
   - Agent **WAJIB** membuat file `.txt` kandidat referensi terpisah (serta dosir `.docx` berhyperlink DOI & PDF bila diminta pengguna).
   - Seluruh kandidat referensi wajib **100% artikel jurnal primer terbitan maksimal 5 tahun terakhir (`2022-2026`)**, memiliki **DOI aktif terverifikasi HTTP 200 di Crossref (`https://doi.org/10....`)**, serta **tautan Download PDF Langsung HTTP 200 (`application/pdf` / header `%PDF-`)**, dan **diutamakan dari jurnal yang level SINTA-nya SETARA dengan jurnal target** (minimal 15 referensi untuk SINTA 2-5 dan minimal 25 untuk SINTA 1).
   - Tiap entri di file `.txt` wajib diberi label level SINTA jurnal sumbernya (`[Peringkat: SINTA 4 - Terverifikasi SINTA Kemdiktisaintek]`); **jika levelnya tidak bisa diverifikasi secara pasti, tulis `[Level SINTA: tidak terverifikasi]`, jangan mengarang**.
4. **R4 - Jurnal Bukan Laporan (Ringkas, Fokus ke Topik, Tidak Kepanjangan, & Data Valid Anti-Revisi)**:
   - Isi naskah jurnal harus **ringkas, padat, fokus ke topik, dan tidak kepanjangan**: penelitian **DIRANGKUM secara analitis**, bukan disalin panjang dari laporan PKL/skripsi (Pendahuluan 4-6 paragraf / 500-750 kata; Metode 3-5 paragraf / 400-650 kata; Hasil & Pembahasan fokus pada bukti & analisis komparatif; Kesimpulan 1-2 paragraf menjawab tujuan).
   - **Zero Halusinasi & Data Valid**: Jangan pernah mengarang angka statistik, hasil uji, nama pasal, atau klaim tanpa bukti. Gunakan data valid dari laporan sumber atau instansi resmi; tandai data yang belum tersedia dengan `[ISI DATA NYATA: ...]`.
   - Patuhi TOS dan gaya selingkung template jurnal tujuan (untuk **JKI - SINTA 4 LPPM UBSI**: struktur artikel jurnal, layout 2 kolom, gaya sitasi **IEEE `[1]`, `[2]`**, min. 15 referensi di file `.txt`, batas *similarity* maksimal **20%**).

---

## 2. Mode Buat Template / Showcase Jurnal SINTA 1-6 Baru dari Nol (Interaktif Wajib)

Hanya ketika pengguna secara eksplisit meminta pembuatan **template kosong / contoh showcase baru** (bukan mengerjakan file `.docx` target milik pengguna), tanyakan 3 pilihan utama ini:

1. **Pilihan Peringkat Jurnal SINTA (1-6 dari Instansi Berbeda beserta DOI Prefix Resmi)**:
   - **SINTA 1 (Informatika/AI) - IJAIN** (UAD Yogyakarta, `10.26555/ijain`, 100% Inggris, 2 Kolom, Min. 25 Ref)
   - **SINTA 1 (Hukum/Hukum Siber) - PJIH** (Unpad, `10.22304/pjih`, 2/1 Kolom, Min. 25 Ref)
   - **SINTA 2 - JTIIK** (FILKOM UB, `10.25126/jtiik`, 2 Kolom, Min. 15 Ref)
   - **SINTA 3 - JISKA** (UIN Sunan Kalijaga, `10.14421/jiska`, 2 Kolom, Min. 15 Ref)
   - **SINTA 4 - JKI** (LPPM UBSI, `10.31294/jki`, 2 Kolom, IEEE, Min. 15 Ref, Similarity <= 20%)
   - **SINTA 5 - TEKNOIF** (ITP, `10.21063/jtif`, 2 Kolom, Min. 12 Ref)
   - **SINTA 6 - METIK** (LPPM STMIK Jayakarta / Univ. Mulia, `10.47002/metik`, 1 Kolom, Min. 12 Ref)
2. **Pilihan Tata Letak Kolom Jurnal**: `2col`, `1col`, atau `default`.
3. **Pilihan Gaya Sitasi**: **IEEE (`[1]`, `[2]`)** atau **APA (`(Penulis, Tahun)`)**.

---

## 3. Aturan Ketat Anti-Slop Jurnal, Tipografi OpenXML, & Etika Publikasi (ARJUNA & COPE)

1. **Bebas Teks "AI Indeks" / Debug Banner**: Dilarang keras menaruh teks `| Peringkat: SINTA X | Layout: 2 Kolom` di badan halaman. Semua metadata jurnal (`Journal Name`, `Vol/No/Tahun`, `p-ISSN`, `e-ISSN`, dan `DOI`) wajib ditempatkan di **Word Header (`w:hdr`)** dan **Footer (`w:ftr`)**, disertai blok **Riwayat Artikel (*Received / Revised / Accepted*)** dan lisensi **CC BY-SA 4.0**.
2. **Superscript Asli, Tipografi Bersih, *Burstiness*, & Anti-Slop**: Gunakan `w:vertAlign="superscript"` untuk indeks afiliasi penulis (`1*`, `2`). Dilarang menggunakan karakter *em dash* (`\u2014`), frasa klise AI (`R-16`), atau *negative parallelism* berulang (`R-36`). Variasikan panjang kalimat secara alami (`std >= 5.5` kata) dan wajib lulus `<skill_dir>/scripts/check_antislop_academic.py`.
3. **Inspeksi Dokumen Existing Sebelum Edit**: Jalankan `$env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<nama_file.docx>"` sebelum menyunting file `.docx` yang sudah ada.
