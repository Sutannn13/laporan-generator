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
