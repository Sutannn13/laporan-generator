---
description: Buat Jurnal Ilmiah SINTA 1-6 (2 Kolom / 1 Kolom, DOI Crossref 2022-2026), Laporan PKL, atau lanjutkan draf .docx in-place patuh R1-R4
---

# Perintah /jurnal-sinta (Multi-Agent Command)

Jalankan protokol penuh **Jurnal Ilmiah SINTA 1-6 & Laporan PKL**:

1. **Jika membuat Jurnal SINTA 1-6 baru dari nol**:
   - Tanyakan 3 pilihan (jika belum disebutkan pengguna):
     a) **Peringkat SINTA (1-6 dari Instansi Berbeda)**: `1` IJAIN/PJIH, `2` JTIIK, `3` JISKA, `4` JKI UBSI, `5` TEKNOIF, `6` METIK.
     b) **Tata Letak Kolom**: `2col` (Layout Terbagi 2) atau `1col` (1 Kolom Penuh).
     c) **Gaya Sitasi**: `ieee` (`[1]`, `[2]`) atau `apa` (`(Penulis, Tahun)`).
   - Untuk draf naskah pengguna (R1 Mendeley), tambahkan `--mendeley-mode` agar Daftar Pustaka di `.docx` bersih dan referensi diekspor ke `.txt` (`R3`):
     ```powershell
     uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --sinta <1..6> --layout <2col|1col> --citation <ieee|apa> --mendeley-mode --output "<Naskah.docx>" --yes
     ```

2. **Jika melanjutkan / mengedit file `.docx` milik pengguna**:
   - Inspeksi DNA template terlebih dahulu (`--inspect-docx`) dan bekerja *live in-place* (R2) tanpa menulis Daftar Pustaka ke `.docx` (R1).

3. **Standar Kualitas, R3 (5 Tahun + Direct PDF), & Anti-Slop**:
   - Referensi kandidat di `.txt`/`.docx` terpisah wajib terbitan **2022-2026** (maks. 5 tahun terakhir), DOI Crossref HTTP 200, dan tautan **Download PDF Langsung HTTP 200**.
   - Verifikasi akhir menggunakan `check_antislop_academic.py` (0 *em dash*, bebas klise `antislop-copywriting`, simpangan baku panjang kalimat *Burstiness* `>= 5.5` kata).
