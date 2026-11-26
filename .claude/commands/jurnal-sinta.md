---
description: Buat Jurnal Ilmiah SINTA 1-6 (2 Kolom / 1 Kolom, DOI Crossref 2022-2026), Laporan PKL, atau lanjutkan draf .docx in-place patuh R1-R4
---

# Perintah /jurnal-sinta (Multi-Agent Command)

Aktifkan skill terpadu `laporan-generator` dan baca `references/jurnal-sinta.md` bersama `references/mode-ilmiah.md`:
1. **Jika membuat Jurnal SINTA 1-6 baru dari nol**: tanyakan 3 opsi (peringkat SINTA `1-6`, tata letak `2col`/`1col`, gaya sitasi `ieee`/`apa`) lalu jalankan generator dengan `--mendeley-mode` (R1).
2. **Jika menyunting berkas `.docx` milik pengguna**: inspeksi DNA template dahulu (`--inspect-docx`) dan sunting *live in-place* (R2) tanpa menulis Daftar Pustaka ke `.docx` (R1).
3. **Standar R3 & Anti-Slop**: rujukan `.txt` terpisah wajib terbitan `2022-2026`, DOI Crossref HTTP 200, dan link PDF langsung HTTP 200; lulus `check_antislop_academic.py` (`std >= 5.5` kata, 0 em-dash).
