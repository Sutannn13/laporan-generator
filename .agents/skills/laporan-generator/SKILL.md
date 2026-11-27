---
name: laporan-generator
description: >-
  Skill akademik terpadu berbasis Word (.docx Python OpenXML) & Typst (.pdf) untuk
  Laporan/Proposal PKL UBSI (Outline 1-4), Skripsi/TA UBSI 2026 (Outline 156/138/137/158),
  Laporan Audit TI COBIT 2019 & Analitik Data, Jurnal Ilmiah SINTA 1-6 / Scopus (1-2 kolom),
  Mode Ilmiah 6 fase dengan rubrik Peer Reviewer >= 85/100, kurasi referensi Mendeley
  (2022-2026, DOI Crossref & PDF HTTP 200), dan penyuntingan Bahasa Indonesia baku
  (humanizer-id preset UBSI). Aktifkan untuk penulisan, suntingan in-place, konversi,
  audit naskah, atau pencarian referensi ilmiah.
---

# Laporan Generator - Skill Akademik Terpadu (Word .docx OpenXML Engine)

Satu skill mandiri (*self-contained*) yang menyatukan seluruh alur kerja akademik tanpa perlu menggandakan banyak skill terpisah: **Engine Word OpenXML**, **Mode Ilmiah 6 Fase**, **Preset Jurnal SINTA 1-6 & DOI**, serta **Penyuntingan Bahasa Indonesia Baku (`humanizer-id` UBSI)**.

> **Prioritas Engine & Lokasi Aset**: Utamakan **Microsoft Word (`.docx`) via Python OpenXML**. Seluruh script, preset katalog 16.617 jurnal SINTA, dataset kebahasaan, dan logo kampus sudah ter-bundle di dalam direktori skill ini (`<skill_dir>/`) agar dapat dijalankan dari folder proyek mana saja tanpa *clone* repositori.

---

## 1. Hukum Tertinggi & Hierarki Otoritas (Mutlak: R1-R4)

Jika terjadi benturan antar aturan, urutan prioritasnya mutlak:
`Hukum Pemilik (R1-R4) & Pedoman Resmi Kampus/OJS Target > mode-ilmiah & check_antislop_academic.py > humanizer-id`

1. **R1 - Daftar Pustaka Jurnal Wilayah Mendeley (Khusus Jurnal SINTA/Scopus)**: Saat menulis atau menyunting `.docx` naskah **jurnal**, **DILARANG KERAS** menuliskan bagian `DAFTAR PUSTAKA` / `REFERENSI` / `REFERENCES` beserta entrinya ke dalam `.docx`. Gunakan `--mendeley-mode`; biarkan daftar pustaka diisi pengguna via Mendeley Cite. *(Khusus Laporan/Proposal PKL & Skripsi UBSI: tulis langsung Daftar Pustaka APA V.7 terverifikasi nyata ke dalam `.docx` tanpa `et al.` / `dkk.` sesuai SK Rektor UBSI 2026, sekaligus ekspor salinan berkas `.txt` untuk impor Mendeley.)*
2. **R2 - Live In-Place Satu Berkas + Atomic Guard**: Jika pengguna menyerahkan satu berkas `.docx` target, sunting langsung berkas tersebut memakai `atomic_save_docx()` (cadangan `.bak` + staging `.tmp.docx`). **DILARANG** membuat file `.docx` pecahan/duplikat atau berkas liar (`humanizer/audit-*.md`) tanpa izin eksplisit.
3. **R3 - Dosir Referensi Terpisah (`.txt` / `.docx`)**: Simpan seluruh kandidat referensi di berkas `.txt` terpisah (dan dosir `.docx` bila diminta). Syarat mutlak: artikel jurnal primer **maks. 5 tahun terakhir (`2022-2026`)**, **DOI Crossref aktif HTTP 200**, tautan **PDF langsung HTTP 200**, setara peringkat SINTA target, dan label jujur (`[Peringkat: SINTA X - Terverifikasi]` atau `[Level SINTA: tidak terverifikasi]`, dilarang mengarang).
4. **R4 - Proporsional sesuai Jenis Dokumen, Substantif Penuh, & Zero Halusinasi**:
   - **Jurnal SINTA/Scopus**: ringkas analitis patuh anggaran kata IMRaD (bukan salinan laporan PKL/skripsi).
   - **Laporan PKL / Skripsi UBSI**: tulis **penuh dan substantif** seluruh bagian konseptual, landasan teori (berbasis rujukan nyata dari `sinta_garuda_mcp.py`, `verify_sinta_refs.py`, atau dokumentasi resmi), arsitektur solusi, dan metode SDLC; baca *source code* proyek di workspace jika tersedia.
   - **Batas Ketat `[ISI DATA NYATA: ...]`**: Dilarang mengarang angka statistik, jumlah responden, hasil uji, atau nomor pasal. Namun placeholder `[ISI DATA NYATA: ...]` **HANYA** boleh dipakai untuk fakta empiris/administratif privat yang belum tersedia (misal NIP pembimbing, angka survei aktual, tangkapan layar aplikasi, atau log pengujian Black-Box nyata). **DILARANG** menaruh placeholder pada landasan teori, definisi konsep domain, atau kerangka metode.

---

## 2. Peta Modul On-Demand (Progressive Disclosure)

Baca **HANYA** berkas rujukan di `references/` yang relevan dengan tugas pengguna agar konteks tetap hemat dan presisi:

| Kebutuhan / Skenario Pengguna | Berkas Rujukan Wajib Dibaca | Kapan Dimuat |
| :--- | :--- | :--- |
| Alur kerja 6 fase, anggaran kata IMRaD, & rubrik Peer Reviewer >= 85/100 | [`references/mode-ilmiah.md`](references/mode-ilmiah.md) | Semua tugas penulisan, konversi, atau audit (`/mode-ilmiah`) |
| Jurnal SINTA 1-6 lintas kampus (IJAIN, PJIH, JTIIK, JISKA, JKI, TEKNOIF, METIK), DNA OJS, & R1-R4 | [`references/jurnal-sinta.md`](references/jurnal-sinta.md) | Penulisan, konversi, inspeksi, atau template Jurnal SINTA/Scopus (`/jurnal-sinta`) |
| Pilihan metodologi baku (PKL 1-4, Skripsi 156/138/137/158, Audit COBIT CCCE, CRISP-DM, SINTA) | [`references/matriks-metodologi-ilmiah.md`](references/matriks-metodologi-ilmiah.md) | Fase penyusunan kerangka/metode untuk semua jenis laporan & jurnal |
| Filter Anti-Slop (0 em-dash, bebas klise AI, Burstiness `std >= 5.5` kata) | [`references/antislop-akademik-id.md`](references/antislop-akademik-id.md) | Sebelum penulisan akhir & audit kualitas teks |
| Penyuntingan Bahasa Indonesia baku (EYD V, TBBBI IV, preset SK Rektor UBSI 2026) | [`references/humanizer-id.md`](references/humanizer-id.md) | **Default khusus naskah Bahasa Indonesia** (nonaktifkan untuk naskah 100% *Academic English*). Sub-kaidah mendalam tersedia di `references/humanizer/*.md`. |

---

## 3. Jalur Eksekusi per Jenis Dokumen (`<skill_dir>/scripts/`)

### A. Laporan / Proposal PKL & Skripsi UBSI 2026 (`.docx`)
- Margin baku SK Rektor UBSI No. `165/2.01/UBSI/III/2026`: A4, Atas `3.0 cm`, Kiri `4.0 cm`, Bawah `2.5 cm`, Kanan `2.5 cm`, Times New Roman `12 pt`, spasi `2.0`, indentasi `1.2 cm`.
- **9 Outline Resmi UBSI 2026 (Wajib Patuhi Judul Bab & Sub-Bab Bawaan Scaffolder)**:
  - **Proposal PKL** (`--type proposal`): 3 Bab (`BAB I PENDAHULUAN`, `BAB II TEMPAT DAN WAKTU PKL`, `BAB III PENUTUP`).
  - **PKL Outline 1 - Proyek Inovasi Perangkat Lunak** (`--type laporan --outline 1`): 6 Bab (`BAB I LATAR BELAKANG IDE APLIKASI`, `BAB II ANALISIS MASALAH`, `BAB III SOLUSI INOVASI`, `BAB IV TUJUAN DAN MANFAAT APLIKASI`, `BAB V METODE PENGEMBANGAN PERANGKAT LUNAK`, `BAB VI PENUTUP`).
  - **PKL Outline 2 (Mobile) / 3 (Jaringan) / 4 (Analisis Sistem)** (`--type laporan --outline 2|3|4`): 4 Bab (`BAB I PENDAHULUAN`, `BAB II LANDASAN TEORI`, `BAB III PEMBAHASAN`, `BAB IV PENUTUP`).
  - **Skripsi / TA UBSI 2026** (`--type skripsi --outline 156|138|137|158`): Outline `156/138/137` (5 Bab) dan Outline `158` StartUp (4 Bab), `ABSTRAK`/`ABSTRACT` terpisah (150-200 kata, 1 spasi), logo sampul `5 x 5 cm`, watermark Behind Text `10 x 10 cm`.
- **Aturan Anti-Rusak Logo & Anti-Draf Kosong (Wajib untuk PKL/Skripsi)**:
  1. **Wajib mulai dari `--scaffold`** (`update_docx_script.py`) lalu sunting paragraf isi secara *in-place*. **DILARANG** membuat `.docx` dari nol tanpa `logo-ubsi.png`, dan **DILARANG** menimpa `p.text = ...` pada paragraf yang memuat `<w:drawing>` (logo sampul) agar logo tidak terhapus.
  2. **Baca *source code* proyek di workspace** (misal `composer.json`, `package.json`, `routes/`, `database/migrations/`, `app/Models/`) jika tersedia untuk mengambil fakta nyata sistem.
  3. **Tulis uraian konseptual & landasan teori secara utuh** dengan rujukan nyata (`sinta_garuda_mcp.py` / `verify_sinta_refs.py` / dokumentasi resmi). Tulis Daftar Pustaka APA V.7 tanpa `et al.`/`dkk.` langsung ke dalam `.docx` dan ekspor salinan `.txt` untuk Mendeley.
  4. **Batasi `[ISI DATA NYATA: ...]`** strictly untuk data privat lapangan yang memang tidak ada di brief maupun workspace (NIP pembimbing, hasil survei aktual, tangkapan layar aplikasi, log uji Black-Box nyata).
```powershell
# Scaffold baru sesuai outline resmi (bekerja dari direktori kerja mana saja):
uv run "<skill_dir>/scripts/update_docx_script.py" --scaffold --type laporan --outline 1 --title "JUDUL" --author "Nama" --nim "12345678" --instansi "Nama Instansi" --output "Laporan_PKL.docx"
uv run "<skill_dir>/scripts/update_docx_script.py" --scaffold --type skripsi --outline 156 --title "JUDUL" --author "Nama" --nim "12345678" --instansi "Nama Instansi" --output "Skripsi_UBSI.docx"
```

### B. Laporan Audit TI (COBIT 2019 CCCE), Analitik Data, & Makalah (`.docx`)
- Terapkan kerangka metode dari [`references/matriks-metodologi-ilmiah.md`](references/matriks-metodologi-ilmiah.md) (`COBIT 2019 CCCE`, `CRISP-DM`, atau `BAB I-V`).
- Generator & verifikator konsistensi angka tabel vs lampiran:
```powershell
uv run "<skill_dir>/scripts/generate_audit_report_docx.py" --output "Laporan_Audit.docx"
uv run "<skill_dir>/scripts/challenge_text_and_math.py" -t "Laporan_Audit.docx"
```

### C. Jurnal Ilmiah SINTA 1-6 & Scopus (`.docx` In-Place atau Template Baru)
- **Sunting file `.docx` target pengguna**: wajib inspeksi DNA template dulu (`--inspect-docx`), lalu sunting *live in-place* patuh R1-R4.
- **Buat draf/template SINTA baru dari nol**: jika pengguna belum menentukan pilihan, tanyakan 3 opsi utama: (1) Peringkat SINTA `1-6`, (2) Tata letak kolom (`2col` / `1col`), (3) Gaya sitasi (`ieee` / `apa`).
```powershell
$env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"
uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --sinta 4 --layout 2col --citation ieee --mendeley-mode --output "Naskah_JKI.docx" --yes
```

### D. Riset & Verifikasi Referensi SINTA 1-6 + GARUDA + Crossref (`.txt` & `.docx`)
- Gunakan katalog lokal **16.617 Jurnal SINTA 1-6** (`<skill_dir>/presets/sinta-catalog.json.gz`) melalui MCP server `sinta-garuda` atau CLI langsung:
```powershell
uv run "<skill_dir>/scripts/sinta_garuda_mcp.py" --search-journals "informatika" --sinta 4
uv run "<skill_dir>/scripts/sinta_garuda_mcp.py" --find-refs "sistem informasi" --sinta 4 --txt-out "kandidat_referensi_sinta4.txt" --docx-out "Dosir_Referensi_SINTA4.docx"
uv run "<skill_dir>/scripts/verify_sinta_refs.py" --help
```

---

## 4. Gerbang Verifikasi Otomatis Sebelum Serah Terima (Wajib)

Jalankan perintah verifikasi nyata berikut sebelum menyerahkan hasil ke pengguna (dan tampilkan hasilnya apa adanya):
```powershell
# 1. Audit kebahasaan Bahasa Indonesia preset UBSI (khusus draf teks/markdown berbahasa Indonesia, pure Python stdlib):
python "<skill_dir>/scripts/audit_humanizer.py" "<draf_teks.md>" --preset akademik --kampus ubsi

# 2. Inspeksi struktur OpenXML pada .docx final:
$env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"

# 3a. Gerbang khusus JURNAL SINTA/SCOPUS (wajib 0 entri daftar pustaka di .docx sesuai R1):
uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --mendeley-mode

# 3b. Gerbang khusus LAPORAN PKL / SKRIPSI UBSI (wajib logo sampul <w:drawing>, prose substantif, & bebas draf kosong):
uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --require-cover-logo --max-placeholders 8 --min-words 2000
```
