---
description: Inspeksi struktur template .docx (--inspect-docx), audit Anti-Slop Burstiness, dan jalankan test suite SINTA 1-6
---

# Perintah /sinta-cek

1. Inspeksi struktur internal & audit anti-slop pada dokumen target (`$ARGUMENTS`):
   ```powershell
   uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "$ARGUMENTS"
   uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "$ARGUMENTS"
   ```
2. Audit penuh repositori:
   ```powershell
   npm run test:all
   ```
