---
description: Buat atau edit in-place Laporan/Proposal PKL UBSI, Skripsi/TA, Laporan Tugas/Audit TI/Analitik, Jurnal SINTA 1-6, atau Dosir Referensi Mendeley dalam Word (.docx OpenXML)
---

# Perintah /laporan-generator

Aktifkan skill terpadu `laporan-generator` (`SKILL.md`) dan muat hanya berkas rujukan yang relevan di `references/`:
1. Prioritaskan **Word (`.docx`) Python OpenXML** memakai skrip ter-bundle di `<skill_dir>/scripts/`.
2. Klasifikasikan jenis dokumen (`Laporan/Proposal PKL UBSI`, `Skripsi/TA UBSI 2026`, `Laporan Tugas/Audit/Analitik`, `Jurnal SINTA 1-6`, atau `Dosir Referensi Mendeley`).
3. Terapkan `references/mode-ilmiah.md`, `references/matriks-metodologi-ilmiah.md`, `references/antislop-akademik-id.md`, serta `references/humanizer-id.md` (`--preset akademik --kampus ubsi` khusus naskah Bahasa Indonesia), dan patuhi hukum **R1-R4**.
4. Khusus **Laporan PKL / Skripsi UBSI**: wajib mulai dari `update_docx_script.py --scaffold` sesuai outline resmi (Proposal, PKL 1-4, Skripsi 156/138/137/158), jaga logo sampul `<w:drawing>` saat edit *in-place*, tulis penuh bagian konseptual/teori dengan referensi terverifikasi nyata (APA V.7 tanpa `et al.` di `.docx` + salinan `.txt`), baca *source code* proyek jika ada, dan batasi `[ISI DATA NYATA: ...]` hanya untuk data privat lapangan.
5. Verifikasi akhir wajib:
   - `python "<skill_dir>/scripts/audit_humanizer.py" "<draf_teks.md>" --preset akademik --kampus ubsi`
   - `uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"`
   - Jurnal SINTA/Scopus: `uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --mendeley-mode`
   - PKL / Skripsi UBSI: `uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --require-cover-logo --max-placeholders 8 --min-words 2000`
