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

1. **R1 - Daftar Pustaka Jurnal Wilayah Mendeley**: Saat menulis atau menyunting `.docx` naskah jurnal milik pengguna, **DILARANG KERAS** menuliskan bagian `DAFTAR PUSTAKA` / `REFERENSI` / `REFERENCES` beserta entrinya ke dalam `.docx`. Gunakan `--mendeley-mode`; biarkan daftar pustaka diisi pengguna via Mendeley Cite.
2. **R2 - Live In-Place Satu Berkas + Atomic Guard**: Jika pengguna menyerahkan satu berkas `.docx` target, sunting langsung berkas tersebut memakai `atomic_save_docx()` (cadangan `.bak` + staging `.tmp.docx`). **DILARANG** membuat file `.docx` pecahan/duplikat atau berkas liar (`humanizer/audit-*.md`) tanpa izin eksplisit.
3. **R3 - Dosir Referensi Terpisah (`.txt` / `.docx`)**: Simpan seluruh kandidat referensi di berkas `.txt` terpisah (dan dosir `.docx` bila diminta). Syarat mutlak: artikel jurnal primer **maks. 5 tahun terakhir (`2022-2026`)**, **DOI Crossref aktif HTTP 200**, tautan **PDF langsung HTTP 200**, setara peringkat SINTA target, dan label jujur (`[Peringkat: SINTA X - Terverifikasi]` atau `[Level SINTA: tidak terverifikasi]`, dilarang mengarang).
4. **R4 - Ringkas Analitis, Zero Halusinasi, & Data Valid**: Jurnal bukan salinan laporan PKL/skripsi; patuhi anggaran kata IMRaD. Dilarang mengarang angka statistik, jumlah responden, hasil uji, atau nomor pasal. Tandai data lapangan yang belum tersedia dengan `[ISI DATA NYATA: ...]`.

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
- **PKL Prodi TI** (`--type laporan --outline 1..4` atau `--type proposal`): logo sampul `4 x 4 cm`, penomoran Romawi Bab (`Gambar II.1.`, `Tabel III.1.`), tanpa `et al.`/`dkk.`.
- **Skripsi / TA UBSI 2026** (`--type skripsi --outline 156|138|137|158`): `ABSTRAK`/`ABSTRACT` terpisah (150-200 kata, 1 spasi), logo sampul `5 x 5 cm`, watermark Behind Text `10 x 10 cm`, semua pengarang Daftar Pustaka ditulis lengkap (`--no-et-al`).
```powershell
# Scaffold baru (bekerja dari direktori kerja mana saja):
uv run "<skill_dir>/scripts/update_docx_script.py" --scaffold --type laporan --outline 4 --title "JUDUL" --author "Nama" --nim "12345678" --output "Laporan_PKL.docx"
uv run "<skill_dir>/scripts/update_docx_script.py" --scaffold --type skripsi --outline 156 --title "JUDUL" --author "Nama" --nim "12345678" --output "Skripsi_UBSI.docx"
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

# 2. Inspeksi struktur OpenXML & audit Anti-Slop + Burstiness (>= 5.5) + Kepatuhan R1 pada .docx final:
$env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"
uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --mendeley-mode
```
*(Lepas `--mendeley-mode` hanya untuk laporan PKL/Skripsi/Audit yang memang mewajibkan Daftar Pustaka tertulis di dalam `.docx`.)*
