---
description: Wizard cepat men-generate file Word (.docx) Jurnal SINTA 1-6 atau memperbarui showcase contoh-template-ai/
---

# Perintah /sinta-buat

1. Generate draf Word Mendeley-ready (`R1`):
   ```powershell
   uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --sinta 4 --layout 2col --citation ieee --mendeley-mode --yes
   ```
2. Untuk memperbarui katalog contoh di `contoh-template-ai/`:
   ```powershell
   npm run sinta:showcase
   ```
