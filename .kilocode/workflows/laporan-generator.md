---
description: Buat atau edit in-place Laporan/Proposal PKL UBSI, Skripsi/TA, Laporan Tugas/Audit TI/Analitik, Jurnal SINTA 1-6, atau Dosir Referensi Mendeley dalam Word (.docx OpenXML)
---

# Perintah /laporan-generator

Aktifkan skill `laporan-generator` bersama `mode-ilmiah`, `jurnal-sinta`, dan `humanizer-id` (khusus teks Bahasa Indonesia):
1. Prioritaskan **Word (`.docx`) Python OpenXML** memakai script ter-bundle di `<skill_dir>/scripts/`.
2. Tanyakan/klasifikasikan jenis dokumen (`Laporan/Proposal PKL UBSI`, `Skripsi/TA UBSI`, `Laporan Tugas/Audit/Analitik`, `Jurnal SINTA 1-6`, atau `Dosir Referensi Mendeley`).
3. Terapkan `resources/matriks-metodologi-ilmiah.md`, `resources/antislop-akademik-id.md`, `--preset akademik --kampus ubsi` (`humanizer-id` untuk teks Indonesia), dan patuhi hukum **R1-R4** (R1-R4 menang atas aturan sub-skill lain).
4. Verifikasi akhir wajib:
   - `uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"`
   - `uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>"`
