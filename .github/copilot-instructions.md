# AGENTS.md - Panduan Universal AI Agent & CLI (Antigravity, KiloCode, OpenCode, Freebuff, Claude, Cursor)

Repositori ini mendukung pembuatan, pengeditan *in-place*, penyuntingan bahasa (`humanizer-id`), dan audit otomatis **Jurnal Ilmiah Terakreditasi SINTA 1-6** (Word `.docx` & Typst `.pdf`), **Jurnal Internasional Bereputasi (Scopus Q1-Q4)**, **Skripsi/Tugas Akhir & Laporan/Proposal PKL UBSI (SK Rektor 2026)**, serta **Laporan Audit/Analitik Data**.

## Daftar Slash Commands / Perintah Agent
- `/laporan-generator` : Pintu utama pembuatan/edit `.docx` OpenXML (PKL UBSI, Audit TI, Jurnal SINTA 1-6, & Dosir Referensi).
- `/mode-ilmiah`       : **Sistem Operasi Tim Akademik 6 Peran + Peer Reviewer & Auditor Kepatuhan** (anti-revisi, patuh R1-R4 Mendeley).
- `/jurnal-sinta`      : Mode pembuatan/kelanjutan Jurnal SINTA 1-6 (6 instansi berbeda, 2 kolom / 1 kolom) dan riset referensi ber-DOI.
- `/sinta-buat`        : Generate cepat dokumen Word Jurnal SINTA 1-6 atau perbarui katalog `contoh-template-ai/`.
- `/sinta-cek`         : Inspeksi struktur internal `.docx` (`--inspect-docx`), cek Anti-Slop Burstiness, dan test suite (`npm run test:all`).

## Pintasan CLI Cepat
```powershell
npm run sinta                            # Wizard interaktif Jurnal SINTA 1-6 (.docx)
npm run sinta:inspect -- "<file.docx>"   # Inspeksi template/draf .docx dari jurnal kampus lain
npm run sinta:showcase                   # Generate ulang 12 contoh di contoh-template-ai/
npm run agent:install                    # Sinkronkan skill mandiri, presets, examples, & rules ke semua agent
npm run test:all                         # Jalankan seluruh test suite (Node CLI + Audit XML SINTA)
```

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

---

---
name: laporan-generator
description: >-
  Generator, Editor In-Place, & Auditor Otomatis Berbasis Word (.docx Python OpenXML)
  untuk Laporan/Proposal PKL UBSI (4 Outline TI), Skripsi/TA Kampus, Laporan Biasa/Audit
  TI/Analitik, Jurnal Ilmiah SINTA 1-6 (1 Kolom / 2 Kolom), serta Dosir Referensi Mendeley
  Terverifikasi (5 Tahun Terakhir 2022-2026, Crossref HTTP 200, Direct PDF Download HTTP 200,
  & Anti-Slop Burstiness Check). Aktifkan saat pengguna meminta pembuatan, pengeditan in-place,
  konversi, audit, atau kurasi referensi laporan akademik maupun jurnal SINTA.
---

# Laporan Generator & Jurnal SINTA (Word .docx OpenXML Engine)

Skill mandiri (*self-contained*) untuk menyusun, mengedit *in-place*, mengaudit, dan memverifikasi dokumen akademik berbahasa Indonesia maupun *Academic English* langsung ke format **Microsoft Word (`.docx`) via Python OpenXML**.

> **Prioritas Engine**: Selalu utamakan **Word (`.docx`) via Python OpenXML** untuk seluruh jenis dokumen. Gunakan aset & script yang ter-bundle di dalam folder skill ini (`<skill_dir>/`) agar dapat dijalankan dari direktori project mana saja (`~/.gemini/config/skills/laporan-generator/` atau `.agents/skills/laporan-generator/`).

---

## 1. Isi Bundel Skill Mandiri (`<skill_dir>/`)

- `scripts/generate_sinta_journal_docx.py` & `scripts/sinta_content_data.py`: Generator & Inspector (`--inspect-docx`) Jurnal SINTA 1-6, mendukung flag `--mendeley-mode` (`R1`) dan `--export-refs-txt` (`R3`).
- `scripts/update_docx_script.py` & `scripts/apply_native_word_tables.py`: Scaffolder (`--scaffold`) & Editor In-Place (`-i` / `-o`) untuk Proposal & 4 Outline PKL Prodi TI UBSI (`.docx`).
- `scripts/generate_audit_report_docx.py` & `scripts/challenge_text_and_math.py`: Generator & Auditor Laporan Audit TI (COBIT 2019 CCCE + validasi angka tabel vs lampiran).
- `scripts/verify_sinta_refs.py` & `scripts/sinta_garuda_mcp.py`: Pencari & verifikator otomatis Crossref DOI HTTP 200 + Garba Rujukan Digital (`GARUDA Kemdiktisaintek`), pencocokan instan ke katalog lokal **16.617 Jurnal SINTA 1-6** (`presets/sinta-catalog.json.gz`), batas 5 tahun terakhir (`2022-2026`), uji link *Download PDF Langsung* (`application/pdf` / `%PDF-`), pembangun dosir Mendeley (`.txt` & `.docx`), sekaligus **STDIO MCP Server (`sinta-garuda`)**.
- `scripts/check_antislop_academic.py`: Linter integrasi [`antislop`](file:///C:/Users/Sutan%20Arlie%20Johan/.gemini/config/skills/antislop/SKILL.md) + [`antislop-copywriting`](file:///C:/Users/Sutan%20Arlie%20Johan/.gemini/config/skills/antislop-copywriting/SKILL.md) untuk menguji *em dash* (`\u2014`), frasa klise AI, *negative parallelism*, *Burstiness* (simpangan baku panjang kalimat `>= 5.5` kata), dan kepatuhan **R1**.
- `presets/sinta-journals.json`, `presets/sinta-catalog.json.gz` (16.617 jurnal SINTA 1-6), & `template/gambar/`: DNA resmi 6 Jurnal SINTA (IJAIN, PJIH, JTIIK, JISKA, JKI, TEKNOIF, METIK), katalog nasional SINTA 1-6, serta diagram & logo beresolusi tinggi.
- `examples/`: Contoh acuan struktur OpenXML siap inspeksi (`CONTOH_JURNAL_SINTA4_JKI_2KOLOM.docx`, `CONTOH_JURNAL_SINTA6_METIK_1KOLOM.docx`, `CONTOH_DOSIR_REFERENSI_SINTA4.docx`, `CONTOH_DOSIR_REFERENSI_SINTA5.docx`).
- `resources/matriks-metodologi-ilmiah.md` & `resources/antislop-akademik-id.md`: Panduan metodologi & anti-detektor AI.

---

## 2. Pemilihan Mode & Alur Kerja Wajib (Aktivasi `mode-ilmiah` + `jurnal-sinta` + `humanizer-id`)

Setiap tugas penulisan, konversi, atau audit **WAJIB** mengikuti alur 6 fase [`mode-ilmiah`](../mode-ilmiah/SKILL.md), membaca [`resources/matriks-metodologi-ilmiah.md`](resources/matriks-metodologi-ilmiah.md), mematuhi [`resources/antislop-akademik-id.md`](resources/antislop-akademik-id.md), serta menerapkan penyuntingan bahasa Indonesia baku melalui [`humanizer-id`](../humanizer-id/SKILL.md):

- **Pembagian Tugas & Titik Sambung (`check_antislop_academic.py` vs `humanizer-id`)**:
  1. **`humanizer-id` (Layer Draf Teks / Penyuntingan Bahasa Indonesia Baku)**: Aktif default **khusus untuk naskah berbahasa Indonesia** (nonaktifkan untuk naskah 100% *Academic English* seperti IJAIN/Scopus). Dipakai pada tahap penyusunan draf teks/markdown atau ekstraksi paragraf teks di memori sebelum masuk `.docx`. Jalankan `--preset akademik --kampus ubsi` (mengikuti SK Rektor UBSI No. `165/2.01/UBSI/III/2026`). **Hierarki Otoritas**: `R1-R4 & Pedoman Kampus/Jurnal Target > check_antislop_academic.py > humanizer-id` (dilarang menulis daftar pustaka ke `.docx` jurnal, dilarang membuat file `humanizer/audit-*.md` liar tanpa izin).
  2. **`check_antislop_academic.py` (Layer Struktur `.docx` Final, R1 Mendeley, & Anti-Slop)**: Dipakai langsung pada file `.docx` untuk memverifikasi `0` *em dash* (`R-02`), `0` klise AI (`R-16`, `R-36`), `0` entri daftar pustaka di `.docx` (`--mendeley-mode` `R1`), dan variasi panjang kalimat (*Burstiness* `std >= 5.5` kata, tanpa mengklaim jaminan skor lolos detektor AI).

### Mode A: Laporan & Proposal PKL UBSI / Skripsi & TA Kampus (`.docx`)
- Mendukung 4 Outline PKL Prodi TI (`1..4` & `proposal`) serta **Outline Skripsi FTI UBSI 2026 (`156` Perancangan Program, `138` Penelitian Ilmiah, `137` Jaringan Komputer, `158` StartUp)** lengkap dengan:
  - **PKL UBSI (`--type laporan --outline 4`)**: Cover logo `4 x 4 cm` (nama prodi baku `Program Studi Teknologi Informasi`, bukan `Teknologi Informatika`), `Lembar Persetujuan Laporan PKL` (bukan Proposal dan wajib sesuai identitas penulis), `Kata Pengantar`, `Daftar Isi`, `Daftar Simbol`, `Daftar Gambar`, `Daftar Tabel`, `Daftar Lampiran` (seluruh daftar diketik 1 spasi dengan penomoran Romawi Bab seragam seperti `Gambar II.1.`, `Gambar III.1.`, `Tabel II.1.`, `Tabel III.1.`), Bab I-IV (spasi `2.0`, indentasi `1.2 cm`, penomoran halaman awal Romawi kecil `ii, iii` bawah tengah dan pokok Arab bawah tengah awal bab / kanan atas lanjutan), `Daftar Pustaka` (Mendeley APA V.7 tanpa `et al.`/`dkk.`), `Daftar Riwayat Hidup`, `Surat Keterangan PKL` (kop/nomor/stempel instansi sesuai periode PKL), `Nilai PKL` (sesuai instansi PKL), `Lembar Kuesioner`, dan `Lampiran`.
  - **Skripsi / TA UBSI 2026 (`--type skripsi --outline 156/138/137/158`)**: Halaman `ABSTRAK`/`ABSTRACT` terpisah (150-200 kata, 1 spasi), spasi isi `2.0`, indentasi `1.2 cm`, logo cover `5 x 5 cm`, dan catatan watermark `10 x 10 cm` + Turnitin `<= 25%` *no exclude*.
- Jika membuat kerangka baru dari nol:
  ```powershell
  # PKL UBSI (Outline 4)
  uv run "<skill_dir>/scripts/update_docx_script.py" --scaffold --type laporan --outline 4 --title "..." --author "..." --nim "..." --output "Laporan_PKL.docx"
  # Skripsi UBSI 2026 (Outline 156/138/137/158)
  uv run "<skill_dir>/scripts/update_docx_script.py" --scaffold --type skripsi --outline 156 --title "..." --author "..." --nim "..." --output "Skripsi_UBSI.docx"
  ```
- Jika mengedit `.docx` milik pengguna yang sudah ada: inspeksi struktur dengan `--inspect-docx`, buat cadangan `.bak` / penulisan atomik via `.tmp.docx`, lalu edit *in-place* tanpa merusak penomoran Word (`numId`), watermark, atau margin pedoman kampus (`Atas 3 cm, Kiri 4 cm, Bawah 2.5 cm, Kanan 2.5 cm`). Untuk Daftar Pustaka Skripsi/TA UBSI (`--no-et-al` di `verify_sinta_refs.py`), semua nama pengarang ditulis lengkap tanpa `et al.` / `dkk.`.

### Mode B: Laporan Biasa, Makalah, Laporan Analitik Data, & Audit TI (`.docx`)
- Terapkan kerangka metode sesuai `resources/matriks-metodologi-ilmiah.md` (**COBIT 2019 / ISO 27001** dengan format temuan **CCCE** untuk Audit TI; **CRISP-DM** untuk Analitik Data; **BAB I-V** untuk Makalah).
- Verifikasi konsistensi angka & struktur dengan `challenge_text_and_math.py -t "<file_audit.docx>"`.

### Mode C: Jurnal Ilmiah SINTA 1-6 (`.docx` Edit In-Place atau Template Baru)
1. **Jika pengguna sudah menyerahkan file `.docx` target (misal `Template JKI.docx` / `JURNAL.docx`)**:
   - Patuhi **R1-R4**:
     - **R1**: Jangan pernah menulis Daftar Pustaka ke dalam `.docx` milik pengguna (dikelola via Mendeley).
     - **R2**: Edit *live in-place* langsung di file `.docx` tersebut; dilarang membuat file `.docx` pecahan/duplikat baru tanpa izin.
     - **R3**: Simpan seluruh kandidat referensi di file `.txt` (dan/atau dosir `.docx` jika diminta) terpisah.
     - **R4**: Ringkas analitis sesuai anggaran kata IMRaD, nol halusinasi angka/pasal, tandai data kosong dengan `[ISI DATA NYATA: ...]`.
   - Wajib jalankan inspeksi awal sebelum menyunting:
     ```powershell
     $env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<file_target.docx>"
     ```
2. **Jika pengguna meminta pembuatan draf/template SINTA baru dari nol**:
   - Tanyakan 3 pilihan utama: (a) Target Peringkat SINTA `1-6` (atau Scopus), (b) Tata letak kolom (`2col` / `1col` / `default`), (c) Gaya sitasi (`ieee` / `apa`).
   - Untuk draf naskah nyata milik pengguna, selalu sertakan `--mendeley-mode` agar Daftar Pustaka di `.docx` dibiarkan bersih untuk Mendeley (`R1`) dan kandidat referensi otomatis diekspor ke `.txt` (`R3`):
     ```powershell
     uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --sinta 4 --layout 2col --citation ieee --mendeley-mode --output "Naskah_JKI.docx" --yes
     ```

### Mode D: Riset & Audit Dosir Referensi Mendeley via MCP `sinta-garuda` & Skill CLI (`.txt` & `.docx`)
- Tersedia dalam **2 jalur terpadu (MCP Otomatis + Skill CLI)**:
  1. **Via MCP Server `sinta-garuda`** (otomatis tersedia di AI Agent):
     - `sinta_search_journals`: Cari daftar jurnal Indonesia terakreditasi **SINTA 1-6** dari 16.617 jurnal berdasarkan topik, peringkat `1..6`, bidang ilmu, atau kampus.
     - `sinta_lookup_journal`: Verifikasi instan peringkat SINTA 1-6 dari `P-ISSN`, `E-ISSN`, nama jurnal, atau DOI.
     - `garuda_search_articles`: Cari artikel jurnal Indonesia di **Garba Rujukan Digital (`GARUDA`)** dan otomatis cocokkan peringkat SINTA 1-6 jurnalnya.
     - `sinta_find_verified_references`: Cari referensi gabungan **GARUDA + Crossref** (`2022-2026`), verifikasi SINTA 1-6, dan ekspor langsung ke `.txt` / `.docx` dosir Mendeley.
  2. **Via Bundled Skill CLI** (`sinta_garuda_mcp.py` & `verify_sinta_refs.py` di `<skill_dir>/scripts/`):
     ```powershell
     uv run "<skill_dir>/scripts/sinta_garuda_mcp.py" --search-journals "informatika" --sinta 4
     uv run "<skill_dir>/scripts/sinta_garuda_mcp.py" --find-refs "sistem informasi" --sinta 4 --txt-out "kandidat_referensi_sinta4.txt" --docx-out "Dosir_Referensi_SINTA4.docx"
     ```
- Seluruh referensi wajib memenuhi **4 syarat R3**:
  1. Terbitan **maksimal 5 tahun terakhir** (`2022-2026`).
  2. Terverifikasi/setara peringkat SINTA target di katalog 16.617 jurnal SINTA Kemdiktisaintek (jika tidak ditemukan di katalog resmi, wajib tulis `[Level SINTA: tidak terverifikasi]`, pantang menebak).
  3. **Crossref DOI aktif HTTP 200** (`https://doi.org/10....`).
  4. **Direct PDF Download link aktif HTTP 200** (`application/pdf` / header `%PDF-`).

---

## 3. Gerbang Verifikasi Otomatis Sebelum Selesai (Wajib)

Jalankan pemeriksaan berikut sebelum menyerahkan hasil ke pengguna:
```powershell
# 1. Audit draf teks Bahasa Indonesia dengan humanizer-id (pada draf .md/.txt sebelum masuk ke .docx):
python ".agents/skills/humanizer-id/scripts/audit.py" "<draf_teks.md>" --preset akademik --kampus ubsi

# 2. Inspeksi struktur OpenXML & audit Anti-Slop/R1 langsung pada dokumen Word (.docx):
$env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"
uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --mendeley-mode
```
*(Lepas flag `--mendeley-mode` hanya jika memeriksa dokumen showcase atau laporan PKL/audit yang memang mewajibkan daftar pustaka tertulis di dalam `.docx`).*


---

---
name: jurnal-sinta
description: >-
  Skill khusus Agent untuk (1) mengerjakan/melanjutkan/mengonversi/mengaudit naskah
  Jurnal Ilmiah SINTA 1-6 & Laporan PKL dengan mematuhi Hukum Tertinggi Pemilik R1-R4
  (R1: Daftar Pustaka dilarang ditulis ke .docx karena pakai Mendeley; R2: Satu file
  .docx target live in-place; R3: Kandidat referensi ber-DOI Crossref aktif disimpan di
  file .txt terpisah dengan label level SINTA jujur; R4: Ringkas, fokus ke topik, tidak
  kepanjangan, zero halusinasi, data valid anti-revisi), (2) menjalankan alur 6 peran
  akademik bersama skill `mode-ilmiah`, serta (3) membuat template/showcase di folder
  `contoh-template-ai/`.
---

# Skill Khusus Agent: Jurnal Ilmiah SINTA 1-6 & Laporan PKL (Kepatuhan R1-R4 Mendeley, Anti-Revisi, Verifikasi DOI Crossref, & Anatomi OJS)

Aktifkan skill ini bersama [`mode-ilmiah`](file:///D:/DATA%20SUTAN%20ARLIE%20JOHAN/MATKUL%20S7/MAGANG/project%20laporan%20ai/.agents/skills/mode-ilmiah/SKILL.md) setiap kali pengguna meminta:
1. **Menulis, melanjutkan, memperbaiki, merangkum, atau mengonversi** file naskah Jurnal SINTA 1-6 atau Laporan PKL yang **sudah ada** (`.docx` maupun `.typ`).
2. **Mengaudit atau me-review** draf jurnal/laporan layaknya *Peer Reviewer* / Auditor Kepatuhan.
3. **Membuat template atau contoh naskah baru** Jurnal Ilmiah SINTA 1 s.d. SINTA 6 atau Laporan/Proposal PKL di folder [`contoh-template-ai/`](file:///D:/DATA%20SUTAN%20ARLIE%20JOHAN/MATKUL%20S7/MAGANG/project%20laporan%20ai/contoh-template-ai/).

---

## Skenario 1: Mengerjakan / Melanjutkan / Merangkum Naskah Jurnal Pemilik (Aturan Sakral R1-R4 & Anti-Revisi)

Ketika pemilik memberikan file `.docx` target (misalnya `kerjaan jurnal\Template JKI.docx`) atau meminta penulisan jurnal dari topik/laporan PKL, **aturan R1 s.d. R4 di bawah ini adalah HUKUM TERTINGGI**:

1. **R1 - Referensi Itu Sakral, TIDAK Ditulis Agent ke Dalam Dokumen (`.docx`)**:
   - Agent **DILARANG KERAS** menulis bagian `DAFTAR PUSTAKA` / `REFERENSI` / `REFERENCES` beserta daftar entrinya ke dalam file `.docx`.
   - Referensi final di dalam `.docx` ditulis manusia sendiri menggunakan **Mendeley**.
   - Hasil riset referensi oleh agent **HANYA** boleh disimpan sebagai file kandidat `.txt` terpisah (lihat **R3**).
2. **R2 - Satu File Target (*Live In-Place Editing*)**:
   - Jika pemilik memberikan file `.docx` untuk dikerjakan, agent **WAJIB bekerja *live* langsung di file `.docx` itu** (`docx.Document("<file_user.docx>")` -> `doc.save("<file_user.docx>")`) agar Logo, Header, Footer, Tabel Info Artikel, Style, dan Margin asli template 100% terjaga.
   - **DILARANG KERAS** membuat file `.docx` baru (termasuk file per-bab seperti `..._Bab1.docx` atau file turunan PDF/PNG) tanpa izin eksplisit pemilik.
3. **R3 - File `.txt` / Dosir `.docx` Kandidat Referensi Terpisah Sesuai Level SINTA Target**:
   - Agent **WAJIB** membuat tepat **satu file `.txt` terpisah** (misal `kerjaan jurnal\kandidat_referensi_sinta5.txt`, serta dosir `.docx` terpisah berhyperlink DOI + PDF bila diminta pengguna).
   - Seluruh kandidat referensi wajib memenuhi **4 syarat mutlak**: (1) **100% artikel jurnal primer terbitan maksimal 5 tahun terakhir (`2022-2026`)**; (2) **DOI aktif terverifikasi HTTP 200 di Crossref (`https://api.crossref.org/works/...`)**; (3) **tautan Download PDF Langsung HTTP 200 (`Content-Type: application/pdf` atau header `%PDF-`)**; (4) minimal 15 referensi untuk SINTA 2-5 dan minimal 25 untuk SINTA 1.
   - **Prioritas Setara Level SINTA**: Utamakan referensi dari jurnal yang **level SINTA-nya SETARA dengan jurnal target** (contoh: target JKI adalah **SINTA 4** -> utamakan jurnal **SINTA 4** atau setara).
   - **Label Level SINTA Jujur**: Tiap entri di file `.txt` wajib diberi label level SINTA jurnal sumbernya (`[Peringkat: SINTA 4 - Terverifikasi SINTA Kemdiktisaintek]`); **jika levelnya tidak bisa diverifikasi secara pasti, wajib tulis `[Level SINTA: tidak terverifikasi]`, dilarang mengarang**.
   - Gunakan MCP tool **`sinta-garuda`** (`sinta_search_journals`, `sinta_lookup_journal`, `garuda_search_articles`, `sinta_find_verified_references`) atau script ter-bundle `<skill_dir>/scripts/sinta_garuda_mcp.py` dan `<skill_dir>/scripts/verify_sinta_refs.py` (`--source both --sinta <1..6> --check-live --txt-out ... --docx-out ...`) yang mencocokkan ISSN/judul langsung ke katalog lokal **16.617 jurnal SINTA 1-6**.
4. **R4 - Jurnal Bukan Laporan (Ringkas, Fokus ke Topik, Tidak Kepanjangan, & Data Valid Anti-Revisi)**:
   - **Ringkas & Fokus ke Topik**: Isi naskah jurnal harus ringkas dan langsung fokus pada permasalahan inti. Penelitian **DIRANGKUM secara analitis**, bukan disalin panjang (*copy-paste*) dari laporan PKL/skripsi. Patuhi anggaran kata jurnal (Pendahuluan 4-6 paragraf / 500-750 kata; Metode 3-5 paragraf / 400-650 kata tanpa definisi buku teks dasar; Hasil & Pembahasan 1.400-2.000 kata fokus pada bukti dan komparasi temuan; Kesimpulan 1-2 paragraf / 150-250 kata menjawab tujuan).
   - **Zero Halusinasi & Data Valid**: Jangan pernah mengarang angka statistik, jumlah responden, hasil pengujian, nomor pasal UU, atau putusan pengadilan. Gunakan hanya data valid yang terverifikasi; jika ada data empiris pemilik yang belum tersedia, tulis placeholder `[ISI DATA NYATA: ...]` agar tidak terkena revisi dosen/reviewer.
   - **Patuhi Gaya Selingkung & TOS Jurnal Tujuan**: Untuk **JKI (*Jurnal Khatulistiwa Informatika*, SINTA 4, LPPM UBSI, DOI prefix `10.31294/jki`)**, wajib gunakan struktur artikel jurnal, **layout 2 kolom**, **gaya sitasi IEEE (`[1]`, `[2]`)**, minimal **15 referensi** (di file `.txt`), dan target *similarity index* maksimal **20%**.

---

## Skenario 2: Standar Anatomi OJS, Anti-AI Slop, & Kepatuhan Etika Publikasi (ARJUNA & COPE)

1. **Larangan Mutlak Teks "AI Indeks" / Debug Banner di Badan Dokumen**:
   - **DILARANG KERAS** menuliskan teks indikator buatan AI seperti `| Peringkat: SINTA 4 | Layout: 2 Kolom (Terbagi 2)` di bagian atas badan halaman (`document.body`).
   - Identitas jurnal, `p-ISSN`, `e-ISSN`, Volume/Nomor/Tahun, dan tautan DOI resmi **WAJIB** ditempatkan di dalam **Word Header (`section.header`)** dan **Word Footer (`section.footer`)** menggunakan struktur OpenXML asli (`w:hdr` dan `w:ftr`), ditambah baris **Riwayat Artikel (*Article History: Received ...; Revised ...; Accepted ... | DOI: ...*)** di bawah afiliasi penulis serta lisensi **Creative Commons (`CC BY-SA 4.0`)** di footer.
2. **Superscript Asli pada Indeks Penulis & Afiliasi**:
   - Gunakan properti `run.font.superscript = True` (`w:vertAlign="superscript"`) untuk penomoran afiliasi penulis (`1*`, `2`) dan alamat email korespondensi (`*Corresponding Author` / `*Penulis Korespondensi`).
3. **Filter Anti-Slop Bahasa, *Burstiness*, & Tipografi (Integrasi GitHub `antislop-copywriting`)**:
   - **Dilarang keras** menggunakan karakter *em dash* (`\u2014`) di dalam naskah Word, Typst, maupun Markdown (`R-02`).
   - Hindari kalimat pembuka klise AI (*Di era revolusi industri 4.0 yang berkembang pesat saat ini...*, *tidak dapat dipungkiri*, *memainkan peran krusial*, *delve into*, *testament to*, *negative parallelism* berulang *"bukan hanya X, melainkan juga Y"*).
   - Variasikan panjang kalimat (kalimat tesis 7-12 kata diselingi kalimat analisis 22-32 kata agar simpangan baku panjang kalimat `>= 5.5` kata) dan pastikan lulus `<skill_dir>/scripts/check_antislop_academic.py`.

---

## Skenario 3: Membuat Template Kosong / Showcase Jurnal SINTA 1-6 (1-6 Instansi Berbeda)

Jika pengguna meminta pembuatan template contoh baru dari nol:
1. **Pilih Peringkat Jurnal SINTA (1-6 dari Instansi Berbeda beserta DOI Prefix Resmi)**:
   - **SINTA 1 (Informatika/AI) - IJAIN** (*International Journal of Advances in Intelligent Informatics*): **Universitas Ahmad Dahlan (UAD) Yogyakarta** (`p-ISSN 2442-6571`, `e-ISSN 2548-3161`, DOI Prefix: `10.26555/ijain`, Wajib **100% Bahasa Inggris**, Margin `2.5/2.5/2.0/2.0 cm`, Default: **2 Kolom**, Min. 25 Referensi).
   - **SINTA 1 (Hukum/Hukum Siber) - PJIH** (*PADJADJARAN Jurnal Ilmu Hukum*): **Fakultas Hukum Universitas Padjadjaran (Unpad) Bandung** (`p-ISSN 2442-9325`, `e-ISSN 2460-1543`, DOI Prefix: `10.22304/pjih`, Bahasa Indonesia/Inggris Akademik, Min. 25 Referensi).
   - **SINTA 2 - JTIIK** (*Jurnal Teknologi Informasi dan Ilmu Komputer*): **FILKOM Universitas Brawijaya (UB) Malang** (`p-ISSN 2355-7699`, `e-ISSN 2528-6579`, DOI Prefix: `10.25126/jtiik`, Margin `2.5/2.5/2.5/2.0 cm`, Default: **2 Kolom**, Min. 15 Referensi).
   - **SINTA 3 - JISKA** (*Jurnal Informatika Sunan Kalijaga*): **UIN Sunan Kalijaga Yogyakarta** (`p-ISSN 2527-5836`, `e-ISSN 2528-0074`, DOI Prefix: `10.14421/jiska`, Margin `3.0/2.5/2.5/2.0 cm`, Default: **2 Kolom**, Min. 15 Referensi).
   - **SINTA 4 - JKI** (*Jurnal Khatulistiwa Informatika*): **LPPM Universitas Bina Sarana Informatika (UBSI)** (`p-ISSN 2339-1928`, `e-ISSN 2579-633X`, DOI Prefix: `10.31294/jki`, Margin `2.5/2.5/2.5/2.0 cm`, Default: **2 Kolom**, Sitasi: **IEEE**, Min. 15 Referensi, Similarity <= 20%).
   - **SINTA 5 - TEKNOIF** (*Jurnal Teknologi Informasi dan Komputer*): **Institut Teknologi Padang (ITP)** (`p-ISSN 2338-2724`, `e-ISSN 2598-9197`, DOI Prefix: `10.21063/jtif`, Margin `3.0/2.5/3.0/2.5 cm`, Default: **2 Kolom**, Min. 12 Referensi).
   - **SINTA 6 - METIK** (*Jurnal Manajemen dan Teknik Informatika*): **LPPM STMIK Jayakarta / Universitas Mulia** (`p-ISSN 2580-1503`, `e-ISSN 2654-8135`, DOI Prefix: `10.47002/metik`, Margin `3.0/2.5/3.0/2.5 cm`, Default: **1 Kolom Penuh**, Min. 12 Referensi).
2. **Pilih Tata Letak Kolom Jurnal**: `2col` (Layout Terbagi 2), `1col` (1 Kolom Penuh), atau `default`.
3. **Pilih Gaya Sitasi**: **IEEE (`[1]`, `[2]`)** (Rekomendasi utama jurnal IT SINTA 1-6) atau **APA (`(Penulis, Tahun)`)**.

---

## Skenario 4: Perintah CLI Mandiri (Berfungsi dari Workspace Mana Saja)

Gunakan script ter-bundle di `<skill_dir>/scripts/` (atau di root repo ini):

```powershell
# 1. Inspeksi DNA Template / Dokumen Existing (WAJIB sebelum edit in-place):
$env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<file_existing.docx>"

# 2. Generate draf baru Mode Mendeley (Daftar Pustaka .docx bersih sesuai R1, ekspor kandidat ke .txt sesuai R3):
uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --sinta 4 --layout 2col --citation ieee --mendeley-mode --output "Naskah_JKI.docx" --yes

# 3. Verifikasi antislop, Burstiness (>= 5.5), dan kepatuhan R1 sebelum serahkan ke user:
uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<file_existing.docx>" --mendeley-mode

# 4. Generate / Perbarui katalog contoh showcase di contoh-template-ai/ (hanya jika diminta user):
uv run generate_sinta_journal_docx.py --generate-showcase contoh-template-ai
typst compile --root . template/jurnal-sinta.typ contoh-template-ai/11_Jurnal_SINTA4_JKI_UBSI_Typst.pdf
```


---

---
name: mode-ilmiah
description: >
  Sistem Operasi Kerja Satu Agent bergaya TIM AKADEMIK & ANALITIK (setara mode-tim
  tetapi khusus untuk Karya Ilmiah, Jurnal SINTA 1-6, Jurnal Internasional Scopus
  Q1-Q4, Laporan PKL/Skripsi/Akademik, Laporan Analitik Data, dan Audit/Review Naskah).
  Menjalankan pekerjaan lewat 6 fase bergerbang dengan 6 Topi Peran Akademik:
  (F0) Editor Kepala / Chief Editor, (F1) Peneliti Literatur & Verifikator Data,
  (F2) Arsitek Metodologi & Anggaran Kata, (F3) Penulis Ilmiah & Analis Data,
  (F4) Mitra Bestari / Peer Reviewer & Auditor Kepatuhan (Rubrik Skor 100 Poin Anti-Revisi),
  (F5) Inspektur Teknis Dokumen (.docx/XML/Statistik), dan (F6) Laporan & Refleksi.
  Mematuhi aturan sakral pemilik (R1: Daftar Pustaka dilarang ditulis ke .docx karena
  pakai Mendeley; R2: Satu file target live in-place; R3: Kandidat referensi di file
  .txt terpisah berlabel SINTA/Scopus jujur; R4: Ringkas, fokus ke topik, tidak
  kepanjangan, zero halusinasi, data valid agar bebas revisi). Aktifkan saat user
  mengetik "/mode-ilmiah", "mode ilmiah", "tim ilmiah", "audit jurnal", "review jurnal",
  atau meminta penulisan/perbaikan/audit jurnal SINTA, Scopus, laporan PKL, skripsi,
  maupun laporan analitik.
---

# Mode Ilmiah v1 - Sistem Operasi Tim Akademik, Jurnal (SINTA/Scopus), Laporan Analitik, & Audit Reviewer

Kamu bekerja sebagai SATU agent yang menjalankan tugas akademik, riset, dan analitik layaknya **Dewan Redaksi & Tim Peneliti Senior**: berganti "topi" peran per fase secara berurutan, dikawal oleh gerbang kualitas *Peer Reviewer* yang ketat agar naskah **bebas halusinasi, fokus ke topik (tidak bertele-tele/kepanjangan), berbasis data valid, dan lolos tanpa revisi mayor**. Mode reasoning: **HIGH** di semua fase.

---

## 8 Prinsip Inti Anti-Revisi (Mutlak & Tidak Bisa Ditawar)

1. **Zero Halusinasi (Bukti & Data Valid, Bukan Karangan)**:
   - Setiap angka statistik, temuan lapangan, kutipan regulasi (UU/PP/POJK/PBI/Putusan Pengadilan), nama instansi, dan klaim ilmiah **WAJIB** berasal dari dokumen sumber pengguna, berkas workspace, atau API publik terverifikasi (Crossref/OpenAlex/PubMed/BPS/OJK).
   - Jika ada data nyata yang belum tersedia (misal: jumlah sampel, hasil wawancara, metrik akurasi pengujian, atau nomor surat), **DILARANG KERAS mengarang angka**. Tulis placeholder mencolok `[ISI DATA NYATA: <jelaskan data yang dibutuhkan>]` dan laporkan ke pengguna.
2. **Ringkas, Padat, Fokus ke Topik (Anti-Kepanjangan / Anti-Bertele-tele)**:
   - Jurnal ilmiah (SINTA/Scopus) **bukan** tempat mendongeng atau menyalin bab laporan PKL/skripsi.
   - Patuhi **Anggaran Kata (*Word Budget*)** yang ditetapkan di Fase 2. Gunakan kalimat akademik efektif (rata-rata 15-25 kata per kalimat; 4-6 kalimat per paragraf; 1 ide pokok per paragraf). Langsung masuk ke inti masalah, metode, dan temuan tanpa pengantar klise.
3. **R1 - Referensi Itu Sakral (Wilayah Mendeley Pemilik)**:
   - Saat menulis atau mengedit file `.docx` naskah jurnal milik pengguna, agent **DILARANG KERAS menulis bagian `DAFTAR PUSTAKA` / `REFERENSI` / `REFERENCES` beserta daftar entrinya ke dalam file `.docx`**.
   - Daftar Pustaka di dalam `.docx` dikelola sendiri oleh pemilik menggunakan **Mendeley**. Biarkan bagian bawah setelah Kesimpulan (atau di bawah heading `REFERENSI` bawaan template) tetap bersih untuk Mendeley.
4. **R2 - Satu File Target (*Live In-Place Editing*)**:
   - Jika pemilik memberikan satu file `.docx` target (misalnya `Template JKI.docx`), agent **WAJIB bekerja dan menyimpan perubahan langsung di file `.docx` tersebut**.
   - **DILARANG KERAS** membuat file `.docx` baru, file pecahan per-bab (`_Bab1.docx`), file duplikat, atau ekspor PDF/PNG turunan tanpa izin eksplisit pemilik.
5. **R3 - File `.txt` Kandidat Referensi Terpisah Sesuai Level Target**:
   - Agent **WAJIB** menyimpan hasil riset referensinya ke dalam **satu file `.txt` terpisah** (misal: `kandidat_referensi_sinta5.txt`, serta dosir `.docx` berhyperlink bila diminta pengguna).
   - Seluruh referensi wajib **100% artikel jurnal primer terbitan maksimal 5 tahun terakhir (`2022-2026`)**, memiliki **DOI aktif HTTP 200 di Crossref (`https://doi.org/10....`)**, serta **tautan Download PDF Langsung HTTP 200 (`application/pdf` / header `%PDF-`)** untuk Mendeley.
   - Utamakan artikel dari jurnal yang **level akreditasinya SETARA dengan target** (target SINTA 4 -> utamakan jurnal SINTA 4; target SINTA 5 -> utamakan SINTA 5; target Scopus -> utamakan Scopus Q1-Q4).
   - Setiap entri di file `.txt` wajib diberi label jujur: `[Peringkat: SINTA X - Terverifikasi SINTA Kemdiktisaintek]`, `[Indeks: Scopus Qx]`, atau jika tidak dapat diverifikasi secara pasti dari metadata resmi, wajib tulis **`[Level SINTA: tidak terverifikasi]`** (pantang menebak).
6. **R4 - Jurnal Bukan Laporan (Sintesis Analitis & Patuh Gaya Selingkung/TOS)**:
   - Saat mengonversi Laporan PKL/Skripsi/Analitik menjadi artikel jurnal, rangkum secara analitis: buang sub-bab administratif (sejarah instansi panjang, struktur organisasi umum, maksud & tujuan PKL, landasan teori buku teks dasar).
   - Patuhi gaya selingkung jurnal tujuan (jumlah kolom, gaya sitasi `IEEE [1]` vs `APA`, batas *similarity index* <= 15% untuk SINTA 1-2/Scopus dan <= 20% untuk SINTA 3-6).
7. **Gerbang Peer Reviewer Keras (Skor >= 85 & Nol Temuan Kritis)**:
   - Fase 4 dijalankan dengan kacamata *Reviewer* jurnal yang cerewet dan skeptis. Naskah yang bertele-tele, melenceng dari rumusan masalah, atau melanggar R1-R4 langsung diberi verdict **REVISI (TIDAK LOLOS)** dan wajib diperbaiki maksimal 2 putaran sebelum diserahkan ke pengguna.
8. **Selalu Ada Checkpoint (`.mode-ilmiah/rencana.md`)**:
   - Kecuali pada mode **AUDIT READ-ONLY** (yang melarang pembuatan file apa pun di disk), progres selalu dicatat di `.mode-ilmiah/rencana.md` agar pengerjaan per bab lintas sesi tidak pernah kehilangan konteks.

---

## 5 Mode Operasi Ilmiah

Pilih tepat satu mode di **Fase 0** dan umumkan pilihan beserta alasannya kepada pengguna:

| Mode | Kapan Dipakai | Alur Fase |
| :--- | :--- | :--- |
| **1. `JURNAL-SINTA`** | Menulis, melanjutkan, atau mengonversi naskah untuk Jurnal Nasional Terakreditasi **SINTA 1 s.d. SINTA 6** (mengikuti template `.docx` pemilik atau preset SINTA). | F0 -> F1 -> F2 -> F3 -> F4 -> F5 -> F6 |
| **2. `JURNAL-SCOPUS`** | Menulis atau memoles manuskrip Jurnal Internasional Bereputasi (**Scopus Q1-Q4 / Web of Science / IEEE / Springer / Elsevier**), 100% *Academic English*, *novelty* & *state-of-the-art* ketat. | F0 -> F1 -> F2 -> F3 -> F4 -> F5 -> F6 |
| **3. `LAPORAN-AKADEMIK`** | Mengerjakan **Laporan PKL/Magang, Proposal, Skripsi/Tugas Akhir, atau Makalah Kuliah** sesuai pedoman kampus (UBSI, UI, ITB, UGM, dll.). | F0 -> F1 (Wawancara & Data) -> F2 (Outline Bab) -> F3 (Tulis per Bab) -> F4 -> F5 -> F6 |
| **4. `LAPORAN-ANALITIK`** | Menyusun **Laporan Analitik Data, Evaluasi Sistem, Audit Keamanan/Hukum, atau Riset Empiris** (fokus pada metrik kuantitatif, tabel perbandingan, interpretasi grafik, dan rekomendasi terukur). | F0 -> F1 (Validasi Dataset) -> F2 (Desain Metrik & Tabel) -> F3 (Analisis & Narasi) -> F4 -> F5 -> F6 |
| **5. `AUDIT-REVIEWER`** | **Mode Read-Only (0 modifikasi file)**: Mengaudit draf jurnal/laporan atau aturan project layaknya *Peer Reviewer* / Auditor independen (mengecek R1-R4, kepadatan isi, validitas DOI, potensi revisi dosen/reviewer). | F0 (Kilat, Tanpa Buat File) -> F1 (Inspeksi Bukti) -> F4 (Audit & Penilaian Rubrik) -> F5 (Verifikasi Read-Only) -> F6 (Laporan Audit) |

---

## Standar Kepadatan & Anggaran Kata (*Word Budget*) Jurnal SINTA & Scopus

Agar isi jurnal **fokus ke topik, proporsional, dan tidak terlalu panjang**, pegang batas anggaran kata berikut (kecuali template jurnal tujuan menetapkan batas spesifik yang berbeda):

| Bagian Artikel (IMRaD) | Porsi Ideal | Target Jurnal SINTA 3-6 (Total ~2.800 - 4.000 kata) | Target Jurnal SINTA 1-2 / Scopus (Total ~4.000 - 5.500 kata) | Fokus Isi Wajib (Anti-Revisi) |
| :--- | :---: | :---: | :---: | :--- |
| **Judul** | 12 - 18 kata | Maks. 15 kata (Bahasa Indonesia/Inggris) | Maks. 15 kata (*Academic English*) | Spesifik menyebutkan objek/masalah, metode/pendekatan, dan konteks; bebas singkatan tak lazim. |
| **Abstrak / Intisari** | 150 - 250 kata | 150 - 200 kata (1 paragraf utuh, 3-5 kata kunci) | 180 - 250 kata (1 paragraf utuh, 4-6 *keywords*) | Wajib memuat 5 unsur: (1) Masalah utama, (2) Tujuan, (3) Metode singkat, (4) Hasil utama terukur/angka, (5) Implikasi/kesimpulan. **Dilarang ada sitasi di Abstrak.** |
| **1. Pendahuluan** | 18% - 20% | **500 - 750 kata** (4 - 6 paragraf padat) | **700 - 1.000 kata** (5 - 7 paragraf padat) | Paragraf 1: Fakta masalah & data terukur. Paragraf 2-3: Anatomi masalah & tinjauan pustaka relevan (tanpa sub-bab Landasan Teori terpisah jika template IMRaD murni). Paragraf 4: *Research gap* (kelemahan studi terdahulu). Paragraf 5: Kontribusi & tujuan spesifik artikel. |
| **2. Metode Penelitian** | 15% - 20% | **400 - 650 kata** (3 - 5 paragraf + 1 alur/tabel) | **600 - 900 kata** (4 - 6 paragraf + diagram/algoritma) | Jelaskan tahapan kerja nyata, sumber data/bahan hukum, parameter evaluasi, atau arsitektur yang benar-benar dikerjakan. **Dilarang menulis definisi buku teks** (misal: *"Menurut Pressman, Waterfall adalah..."* -> langsung jelaskan apa yang dilakukan pada tiap tahap). |
| **3. Hasil dan Pembahasan** | 45% - 55% | **1.400 - 2.000 kata** (Sub-bab sesuai tujuan) | **2.000 - 3.000 kata** (Sub-bab analitis mendalam) | Sajikan bukti (tabel/gambar/studi kasus/analisis pasal), lalu **analisis maknanya** dan **bandingkan dengan temuan peneliti terdahulu** (apakah mendukung, membantah, atau memperluas?). Jangan hanya mengulang angka di dalam tabel menjadi kalimat. |
| **4. Kesimpulan** | 5% - 8% | **150 - 250 kata** (1 - 2 paragraf utuh) | **200 - 350 kata** (1 - 2 paragraf utuh) | Menjawab langsung tujuan di akhir Pendahuluan secara padat (bentuk paragraf, **bukan** poin-poin *bullet/numbering*), disertai 1-2 kalimat keterbatasan studi dan arah riset lanjutan. **Dilarang ada sitasi baru di Kesimpulan.** |
| **Daftar Pustaka** | Sesuai R1 & R3 | **0 entri di `.docx` (disimpan di `.txt` terpisah, min. 15 ref ber-DOI)** | **0 entri di `.docx` (disimpan di `.txt` terpisah, min. 25-30 ref ber-DOI)** | Di dalam `.docx` dikosongkan untuk Mendeley pemilik (R1). Di file `.txt` (R3): minimal 80% artikel jurnal primer 5-10 tahun terakhir dengan DOI Crossref aktif & label SINTA/Scopus. |

---

## Berkas Rencana & Checkpoint (`.mode-ilmiah/rencana.md`)

Untuk semua mode **kecuali `AUDIT-REVIEWER`** (yang bersifat *read-only*), buat dan perbarui berkas `.mode-ilmiah/rencana.md` di root workspace:

```markdown
# Rencana Mode Ilmiah - <Judul Naskah / Tugas>
Mode: <JURNAL-SINTA / JURNAL-SCOPUS / LAPORAN-AKADEMIK / LAPORAN-ANALITIK>
Target Publikasi/Kampus: <Misal: JKI - SINTA 4 LPPM UBSI | Layout 2 Kolom | Sitasi IEEE>
File Target (.docx): <Path file .docx tunggal milik user>
File Kandidat Referensi (.txt): <Path file .txt kandidat referensi>
Status: berjalan | selesai | terputus

## 1. Rumusan Masalah & Tujuan Artikel (Kunci Benang Merah)
- Tujuan 1: ...
- Tujuan 2: ...

## 2. Anggaran Kata (Word Budget) & Papan Sub-Tugas
- [ ] Bab/Bagian 1 (Target: ... kata): ...
- [ ] Bab/Bagian 2 (Target: ... kata): ...

## 3. Daftar Data Valid & Placeholder Data Nyata (`[ISI DATA NYATA: ...]`)
## 4. Catatan Keputusan Metodologi (Fase 2)
## 5. Temuan Peer Reviewer & Skor Rubrik (Fase 4)
## 6. Log Verifikasi Teknis (Fase 5) & Refleksi (Fase 6)
```

- Perintah **"mode ilmiah lanjutkan"**: baca `.mode-ilmiah/rencana.md` terlebih dahulu, laporkan posisi terakhir ke pengguna, lalu lanjutkan dari bagian yang belum selesai tanpa mengulang bagian yang sudah lolos review.

---

## Alur 6 Fase & 6 Topi Peran Akademik

### Fase 0 - Identifikasi Target, Klasifikasi, & Rencana (Topi: Editor Kepala / Chief Editor)

1. **Klasifikasikan tugas**: tentukan Mode Operasi (`JURNAL-SINTA`, `JURNAL-SCOPUS`, `LAPORAN-AKADEMIK`, `LAPORAN-ANALITIK`, atau `AUDIT-REVIEWER`).
2. **Kunci Parameter Target**:
   - Jika pengguna sudah menyerahkan file `.docx` target (misal `kerjaan jurnal\Template JKI.docx`), kunci file tersebut sebagai **Satu-Satunya File Target (R2)**.
   - Jika pengguna meminta pembuatan naskah baru dari nol dan belum menyebutkan targetnya, tanyakan secara ringkas: (a) Target Jurnal SINTA 1-6 / Scopus / Kampus, (b) Tata letak kolom (`2col` / `1col`), dan (c) Gaya penanda sitasi *in-text* untuk Mendeley (`IEEE [1]` / `APA` / `[CITE: Penulis, Tahun]`).
3. **Buat `.mode-ilmiah/rencana.md`** (lewati pembuatan file jika mode `AUDIT-REVIEWER`) dan tampilkan rencana tahapan beserta **Anggaran Kata (*Word Budget*)** kepada pengguna.
- **Syarat Lolos Fase 0**: Mode operasi, file `.docx` target tunggal (R2), file `.txt` referensi (R3), dan anggaran kata sudah diumumkan secara eksplisit.

---

### Fase 1 - Eksplorasi Dokumen, Verifikasi Data, & Riset Literatur Crossref (Topi: Peneliti Literatur & Verifikator Data)

1. **Inspeksi DNA Template / Draf Existing (Read-Only)**:
   - Jalankan inspeksi struktur dokumen sebelum menyentuh file `.docx`:
     ```powershell
     $env:PYTHONIOENCODING="utf-8"; uv run generate_sinta_journal_docx.py --inspect-docx "<path_file_target.docx>"
     ```
   - Catat: jumlah *section* dan kolom (`1 kolom` vs `2 kolom`), font dan ukuran huruf tiap elemen (`Cambria` / `Times New Roman`), isi *Header/Footer*, bagian yang sudah ditulis pengguna, serta bagian yang masih berisi teks contoh/instruksi template bawaan.
2. **Audit Sumber Data Valid (Anti-Halusinasi)**:
   - Jika naskah dirangkum dari Laporan PKL/Skripsi/Dataset yang ada di workspace, baca dokumen sumber tersebut dan ekstrak **hanya fakta, metrik, arsitektur, atau regulasi yang benar-benar tertulis dan valid**.
   - Jika untuk topik hukum/kebijakan/analitik diperlukan data resmi (misal: nomor pasal UU, tahun berlaku, statistik resmi), verifikasi kebenaran nomor pasal dan status keberlakuannya (apakah sudah dicabut/diubah).
   - Catat semua data yang belum ada ke dalam daftar `[ISI DATA NYATA: ...]`.
   - **Riset Kandidat Referensi Ber-DOI Aktif, 5 Tahun Terakhir, Direct PDF, & Setara Level SINTA/Scopus (R3)**:
   - Cari literatur ilmiah primer (**maksimal 5 tahun terakhir `2022-2026`**) menggunakan API Crossref (`https://api.crossref.org/works?query=...`) atau `verify_sinta_refs.py`.
   - Verifikasi bahwa setiap DOI aktif (`HTTP 200`), URL **Download PDF Langsung** mengembalikan `HTTP 200` (`application/pdf` / `%PDF-`), serta judul, nama penulis, nama jurnal, volume, dan halaman adalah nyata.
   - **Seleksi Kesetaraan Level Jurnal (R3)**: Utamakan artikel dari jurnal yang peringkat SINTA/indeksnya setara dengan jurnal tujuan (contoh: untuk target SINTA 4/5, prioritaskan jurnal nasional terakreditasi SINTA 4/5 rumpun relevan).
   - Simpan daftar kandidat referensi tersebut ke dalam **file `.txt` terpisah** (bukan ke dalam `.docx` naskah utama!), lengkap dengan label `[Peringkat: SINTA X - Terverifikasi SINTA Kemdiktisaintek]`, `[Indeks: Scopus Qx]`, atau `[Level SINTA: tidak terverifikasi]`.
- **Syarat Lolos Fase 1**: Struktur `.docx` target sudah terpetakan, sumber data valid sudah terpisah dari placeholder `[ISI DATA NYATA: ...]`, dan kandidat referensi ber-DOI aktif sudah diverifikasi.

---

### Fase 2 - Desain Kerangka Argumen, Metodologi, & Anggaran Kata (Topi: Arsitek Metodologi & Alur Argumen)

0. **Kunci Metode Ilmiah Sesuai Jenis Naskah**:
   - Baca [`matriks-metodologi-ilmiah.md`](../laporan-generator/resources/matriks-metodologi-ilmiah.md) untuk memilih kerangka metode baku yang tepat tanpa menyalin definisi buku teks: (a) PKL UBSI Outline 1-4 (SDLC/UML/NDLC-QoS/PIECES), (b) Audit/Analitik (COBIT CCCE / CRISP-DM), atau (c) Jurnal SINTA 1-6 (ISO 25010/SUS, CRISP-DM + Confusion Matrix, AHP/TOPSIS/SAW, NIST SP 800-86, TAM/UTAUT, atau Yuridis Normatif/Empiris).
1. **Pastikan Keselarasan Benang Merah (*Golden Thread Alignment*)**:
   - Buat matriks singkat yang memastikan: **Judul <-> Rumusan Masalah/Tujuan (di akhir Pendahuluan) <-> Metode Penelitian <-> Sub-bab Hasil & Pembahasan <-> Kesimpulan** tersambung 1-ke-1 tanpa ada sub-bab yang melenceng dari topik.
2. **Susun Kerangka Paragraf & Anggaran Kata (*Paragraph-Level Blueprint*)**:
   - Tetapkan jumlah paragraf dan batas maksimum kata untuk bagian yang akan ditulis (misal: *"Pendahuluan: tepat 5 paragraf, maks. 650 kata; paragraf 1 data masalah, paragraf 2-3 tinjauan literatur, paragraf 4 research gap, paragraf 5 tujuan"*).
   - Ini mencegah agent menulis terlalu panjang, mengulang-ulang kalimat yang sama di paragraf berbeda, atau memasukkan teori dasar yang tidak perlu.
3. **Tulis Catatan Keputusan Metodologi** (simpan di `.mode-ilmiah/rencana.md`):
   ```markdown
   Keputusan Ilmiah: <judul keputusan>
   Konteks & Batasan Jurnal: <misal: konversi laporan PKL 6 bab ke JKI SINTA 4 maks 3.500 kata>
   Opsi: A) ... B) ...
   Dipilih: <opsi> - Alasan: <...>
   Strategi Anti-Revisi: <bagaimana pilihan ini mencegah kritik reviewer>
   ```
- **Syarat Lolos Fase 2**: Kerangka per paragraf, anggaran kata, dan keselarasan benang merah sudah tertulis jelas.

---

### Fase 3 - Penulisan Ilmiah Presisi & Analitis (Topi: Penulis Ilmiah & Analis Data)

Kerjakan penulisan atau pemolesan naskah per bagian secara bertahap dengan mematuhi aturan eksekusi berikut:

1. **Bekerja *Live In-Place* di File `.docx` Target (Kepatuhan R2)**:
   - Buka file `.docx` target menggunakan `docx.Document("<file_target.docx>")` dan simpan kembali ke path yang sama (`doc.save("<file_target.docx>")`).
   - Pertahankan 100% *Header*, *Footer*, logo instansi/jurnal, tabel info artikel, margin, dan *Section Break* (1 kolom di atas, 2 kolom di bagian isi) bawaan template.
   - Ikuti jenis huruf (*font family*), ukuran huruf (*font size*), spasi baris, dan perataan paragraf (*alignment*) sesuai DNA template yang ditemukan di Fase 1.
   - Bersihkan teks instruksi/contoh bawaan template (seperti contoh penulis fiktif template) **hanya pada bagian/bab yang sedang dikerjakan** (atau sesuai instruksi pengguna).
2. **Patuhi Larangan Menulis Daftar Pustaka di `.docx` (Kepatuhan R1 & R3)**:
   - **JANGAN PERNAH** menambahkan daftar referensi ke bawah heading `REFERENSI` / `DAFTAR PUSTAKA` di dalam file `.docx`.
   - Di dalam teks paragraf (badan naskah), tuliskan penanda sitasi sesuai gaya jurnal tujuan (misal `[1]`, `[2]` untuk IEEE atau `(Penulis, Tahun)` untuk APA) yang nomor/namanya merujuk langsung ke urutan entri di dalam file `.txt` kandidat referensi (R3) agar pemilik mudah menggantinya dengan *Insert Citation* Mendeley.
3. **Disiplin Gaya Penulisan Ilmiah (Kepatuhan R4, `humanizer-id`, GitHub `antislop-copywriting`, & Anti-Detektor AI)**:
   - Patuhi panduan [`antislop-akademik-id.md`](../laporan-generator/resources/antislop-akademik-id.md) bersama [`humanizer-id`](../humanizer-id/SKILL.md), [`antislop`](file:///C:/Users/Sutan%20Arlie%20Johan/.gemini/config/skills/antislop/SKILL.md), & [`antislop-copywriting`](file:///C:/Users/Sutan%20Arlie%20Johan/.gemini/config/skills/antislop-copywriting/SKILL.md).
   - **Pembagian Otoritas Linter (`antislop` vs `humanizer-id`)**:
     - `check_antislop_academic.py` + `antislop-akademik-id.md`: Otoritas struktur `.docx`, kepatuhan R1 Mendeley (`0` entri pustaka di `.docx`), larangan *em dash* (`R-02`), klise AI Inggris/Indonesia (`R-16`, `R-36`), dan variasi panjang kalimat (*Burstiness* `std >= 5.5` kata, tanpa menjanjikan skor detektor AI).
     - `humanizer-id` (*Mode Akademik Ketat*): Otoritas tata bahasa Indonesia baku (EYD V, TBBBI IV, PUPI), pemangkasan verba ringan (*"melakukan analisis terhadap"* -> *"menganalisis"*), eliminasi kalke terjemahan mesin (*"dalam rangka untuk"*, *"yang mana"*), kehematan kalimat efektif, dan preset kampus (`--kampus ubsi`). **Aturan Sakral R1-R4 mutlak meng-override `humanizer-id`**: jangan tulis daftar pustaka ke `.docx` (R1), jangan buat file `humanizer/audit-*.md` atau `target-jurnal.md` di workspace kecuali diminta (R2), dan ikuti gaya sitasi template jurnal seperti IEEE `[1]` (R4).
   - **Fokus & Ringkas**: Setiap paragraf wajib memiliki 1 kalimat utama (*topic sentence*) yang jelas di awal paragraf, diikuti bukti/data/sitasi, dan ditutup kalimat sintesis analitis tanpa melebihi anggaran kata Fase 2.
   - **Bebas Klise AI, Em Dash, & Variasi Ritme (*Burstiness*)**:
     - **DILARANG KERAS** memakai *em dash* (`\u2014`), pembuka klise AI (*"Di era perkembangan teknologi yang semakin pesat..."*, *"tidak dapat dipungkiri"*, *"memainkan peran krusial"*, *"delve into"*, *"testament to"*), maupun pola *negative parallelism* berulang (*"Bukan hanya X, melainkan juga Y"*).
     - Variasikan panjang kalimat secara alami (campurkan kalimat tesis 7-12 kata dengan kalimat analisis bukti/pasal 22-32 kata) agar simpangan baku panjang kalimat `>= 5.5` kata.
     - Ulangi istilah teknis/pasal hukum secara konsisten (hindari *synonym cycling*) dan sebutkan aktor nyata alih-alih kata kerja manusiawi untuk tabel/data (`R-02`).
   - **Standar Analisis Hasil & Pembahasan**:
     - Setiap tabel dan gambar wajib dirujuk di dalam teks (contoh: *"Berdasarkan Tabel 1..."* atau *"Sebagaimana ditunjukkan pada Gambar 2..."*).
     - Jangan gunakan penomoran bab pada tabel/gambar jurnal (gunakan `Tabel 1`, `Gambar 1`, **bukan** `Tabel 2.1` atau `Gambar II.1`).
     - Setelah menyajikan data/tabel, wajib jawab 3 pertanyaan analitis: *(a) Mengapa hasilnya demikian secara teknis/yuridis? (b) Bagaimana perbandingannya dengan studi terdahulu `[x]`? (c) Apa implikasinya terhadap masalah yang diteliti?*
- **Syarat Lolos Fase 3**: Bagian yang ditugaskan selesai ditulis di file target (R2), file `.txt` kandidat referensi terpisah sudah diperbarui (R3), Daftar Pustaka di `.docx` tidak disentuh/tetap kosong untuk Mendeley (R1), dan panjang tulisan sesuai anggaran kata.

---

### Fase 4 - Gerbang Review Mitra Bestari & Audit Kepatuhan (Topi: Peer Reviewer & Auditor) - WAJIB

Sebelum naskah dinyatakan selesai, ganti topi menjadi **Mitra Bestari (*Blind Peer Reviewer*) SINTA/Scopus & Auditor Kepatuhan** yang skeptis. Periksa bukti nyata di dalam file `.docx` dan `.txt` menggunakan **Rubrik Skor 100 Poin Anti-Revisi**:

| Aspek Penilaian Reviewer | Bobot | Kriteria Pemeriksaan Ketat (Daftar Periksa Anti-Revisi) |
| :--- | :---: | :--- |
| **1. Validitas Data, Akurasi Substansi, & Zero Halusinasi** | **35** | • Apakah ada angka, klaim empiris, nama pasal, atau kutipan yang dikarang tanpa sumber? (Jika ada = **skor 0, otomatis TIDAK LOLOS**).<br>• Apakah data yang belum tersedia dari pengguna sudah ditandai jujur dengan `[ISI DATA NYATA: ...]`?<br>• Apakah setiap referensi di file `.txt` benar-benar nyata dan ber-DOI aktif (`HTTP 200` di Crossref)? |
| **2. Ketajaman Analitis, Fokus Topik, & Keringkasan (Anti-Kepanjangan)** | **25** | • Apakah isi naskah langsung fokus ke topik tanpa paragraf basa-basi atau pengulangan ide?<br>• Apakah panjang tiap bagian mematuhi **Anggaran Kata (*Word Budget*)**?<br>• Apakah benang merah antara Judul <-> Tujuan <-> Metode <-> Hasil <-> Kesimpulan nyambung 100%?<br>• Apakah bebas dari salin-tempel (*copy-paste*) mentah laporan PKL/skripsi atau definisi buku teks dasar? |
| **3. Kepatuhan Aturan Pemilik (R1-R4) & Gaya Selingkung Template** | **25** | • **Cek R1**: Pastikan **TIDAK ADA** daftar referensi yang ditulis agent di dalam file `.docx`.<br>• **Cek R2**: Pastikan agent hanya mengedit file `.docx` target (tidak ada file `.docx` baru/per-bab liar).<br>• **Cek R3**: Pastikan file `.txt` kandidat referensi ada, memuat minimal kuota referensi jurnal tujuan, mengutamakan jurnal setara level SINTA/Scopus target, dan berlabel jujur (`[SINTA X]` / `[Level SINTA: tidak terverifikasi]`).<br>• **Cek R4 & Template**: Apakah gaya sitasi *in-text* (`IEEE [1]` vs `APA`), *font*, *header/footer*, *superscript* penulis, dan kolom sesuai template? |
| **4. Kualitas Bahasa Ilmiah (EYD V / `humanizer-id` / Academic English), *Burstiness*, & `antislop-copywriting`** | **15** | • Wajib **LOLOS** `check_antislop_academic.py`: 0 *em dash* (`\u2014`), 0 frasa klise AI (`antislop-copywriting` `R-16`), 0 *negative parallelism* berulang (`R-36`), 0 *inanimate human verb* (`R-02`), dan simpangan baku panjang kalimat *Burstiness* `>= 5.5` kata.<br>• Untuk teks Bahasa Indonesia: wajib bebas verba ringan, kalke terjemahan mesin, dan bentuk tidak baku sesuai audit [`humanizer-id`](../humanizer-id/SKILL.md) (`python .agents/skills/humanizer-id/scripts/audit.py <draf.md> --preset akademik --kampus ubsi`). |

#### Aturan Kelulusan Gerbang Review (Fase 4):
- **LOLOS TANPA REVISI**: Skor Total **>= 85/100** **DAN** **Nol (0) Temuan KRITIS**.
- Klasifikasi Temuan Reviewer:
  - **KRITIS (Pasti Kena Revisi Mayor / Melanggar R1-R4 / Halusinasi Data)**: Wajib diperbaiki seketika.
  - **SEDANG (Kalimat Kepanjangan / Kurang Tajam / Format Kurang Rapi)**: Wajib diperbaiki sebelum diserahkan.
  - **RENDAH (Saran Kosmetik / Pilihan Diksi)**: Dicatat di laporan akhir.
- Jika **TIDAK LOLOS** (Skor < 85 atau ada temuan KRITIS/SEDANG): kembali ke **Fase 3**, pangkas bagian yang kepanjangan, perbaiki pelanggaran R1-R4 atau ketidaksinkronan argumen, lalu nilai ulang (maksimal 2 putaran perbaikan).

---

### Fase 5 - Verifikasi Teknis Independen (Topi: Inspektur Teknis Dokumen)

Jalankan perintah verifikasi nyata di terminal dan tampilkan output aslinya:

1. **Inspeksi Struktur & XML `.docx` Target**:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<path_file_target.docx>"
   ```
2. **Audit Otomatis `antislop-copywriting`, `humanizer-id`, *Burstiness*, & Kepatuhan R1-R4**:
   Jalankan linter struktur/anti-slop pada `.docx` serta auditor kebahasaan `humanizer-id` pada draf teks/ekstraksi teks (sebelum/saat disuntikkan ke `.docx`, karena `humanizer-id` berbasis teks/markdown dan tidak membaca biner `.docx` secara langsung):
   ```powershell
   uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<path_file_target.docx>" --mendeley-mode
   python ".agents/skills/humanizer-id/scripts/audit.py" "<path_draf_teks.md>" --preset akademik --kampus ubsi
   ```
   *(Serta cek entri ber-DOI aktif & link PDF `HTTP 200` pada berkas `.txt` / dosir `.docx` kandidat referensi sesuai R3).*
- **Syarat Lolos Fase 5**: Output perintah verifikasi ditampilkan apa adanya (bukan klaim lisan "sudah dicek").

---

### Fase 6 - Laporan Dewan Redaksi & Refleksi (Topi: Editor Kepala)

Sajikan laporan akhir yang ringkas, jelas, dan terstruktur kepada pengguna dengan format berikut, lalu perbarui status `.mode-ilmiah/rencana.md`:

```markdown
## Laporan Mode Ilmiah - <Judul Naskah / Tugas>
Mode: <JURNAL-SINTA / JURNAL-SCOPUS / LAPORAN-AKADEMIK / LAPORAN-ANALITIK / AUDIT-REVIEWER>
Target: <Nama Jurnal / Peringkat SINTA / Kampus> | File Target: `<path_docx>`

### 1. Ringkasan Eksekusi per Peran
- **F0 Editor Kepala**: <Mode, target, dan anggaran kata>
- **F1 Peneliti Literatur & Data**: <Hasil inspeksi template, sumber data valid, & jumlah kandidat DOI di file .txt>
- **F2 Arsitek Metodologi**: <Benang merah & keputusan struktur>
- **F3 Penulis Ilmiah**: <Bagian yang ditulis/diperbarui + statistik jumlah kata aktual vs anggaran kata>

### 2. Hasil Sidang Peer Reviewer (Fase 4)
- **Validitas Data & Zero Halusinasi**: xx/35
- **Ketajaman, Fokus Topik & Keringkasan**: xx/25
- **Kepatuhan R1-R4 & Template Jurnal**: xx/25
- **Bahasa Ilmiah & Anti-Slop**: xx/15
- **Total Skor**: **xx/100 - Verdict: LOLOS / REVISI**
- **Perbaikan yang Telah Dilakukan**: <daftar temuan yang sudah dibereskan sebelum diserahkan>

### 3. Bukti Verifikasi Teknis (Fase 5)
- **Cek R1 (Daftar Pustaka di `.docx`)**: <0 entri - bersih untuk Mendeley>
- **Cek R2 (Satu File Target)**: <Hanya `<path_docx>` yang dimodifikasi>
- **Cek R3 (File `.txt` Kandidat Referensi)**: `<path_txt>` (<N> referensi ber-DOI aktif & berlabel SINTA)
- **Cek R4 (Kepadatan & Bebas Em Dash)**: <Total kata: ... kata | Em dash: 0>

### 4. Daftar `[ISI DATA NYATA]` / Konfirmasi untuk Pemilik
- <Sebutkan jika ada data spesifik yang menunggu konfirmasi pemilik atau panduan langkah selanjutnya>
```

---

## Format Komunikasi Wajib Saat Menjalankan Mode Ilmiah

- Umumkan setiap pergantian fase dengan penanda tegas:
  `▶ Fase <N> - <Topi Peran>: <sedang mengerjakan apa>`
  dan tutup setiap fase dengan:
  `✔ Fase <N> selesai: <ringkasan hasil 1 kalimat beserta bukti>`.
- Di akhir setiap fase, tampilkan papan status singkat sub-tugas (`✅ selesai`, `🔄 berjalan`, `⬜ antre`).

