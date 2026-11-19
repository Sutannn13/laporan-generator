# /// script
# requires-python = ">=3.10"
# ///
"""
Universal Multi-Agent Self-Contained Skill, Bundled Assets, & Slash Command Installer:
- Antigravity IDE (.agents/skills, .agents/rules, ~/.gemini/config/...)
- KiloCode (.kilocode/rules, .kilocode/workflows, ~/.kilocode/...)
- OpenCode CLI (.opencode/commands, .opencode/skills, AGENTS.md, ~/.config/opencode/...)
- Freebuff / Codebuff CLI (.freebuff/commands, .freebuff/skills, knowledge.md, ~/.config/freebuff/...)
- Claude Code CLI (.claude/commands, CLAUDE.md, ~/.claude/commands/...)
- Roo Code & Cline (.roo/rules, .roo/commands, .clinerules)
- Cursor, Windsurf, & GitHub Copilot (.cursor/rules, .windsurfrules, .github/copilot-instructions.md)
"""
import argparse
import json
import os
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(ROOT_DIR, ".agents", "skills")
RULE_SRC = os.path.join(ROOT_DIR, ".agents", "rules", "sinta-journal-prompt.md")

LAPORAN_SCRIPTS = [
    ("generate_sinta_journal_docx.py", "generate_sinta_journal_docx.py"),
    ("scripts/__init__.py", "__init__.py"),
    ("scripts/docx_io.py", "docx_io.py"),
    ("scripts/sinta_content_data.py", "sinta_content_data.py"),
    ("scripts/update_docx_script.py", "update_docx_script.py"),
    ("scripts/apply_native_word_tables.py", "apply_native_word_tables.py"),
    ("scripts/generate_audit_report_docx.py", "generate_audit_report_docx.py"),
    ("scripts/generate_audit_diagrams.py", "generate_audit_diagrams.py"),
    ("scripts/generate_diagrams.py", "generate_diagrams.py"),
    ("scripts/challenge_text_and_math.py", "challenge_text_and_math.py"),
    ("scripts/check_antislop_academic.py", "check_antislop_academic.py"),
    ("scripts/verify_sinta_refs.py", "verify_sinta_refs.py"),
    ("scripts/sinta_garuda_mcp.py", "sinta_garuda_mcp.py"),
]

JURNAL_SCRIPTS = [
    ("generate_sinta_journal_docx.py", "generate_sinta_journal_docx.py"),
    ("scripts/__init__.py", "__init__.py"),
    ("scripts/docx_io.py", "docx_io.py"),
    ("scripts/sinta_content_data.py", "sinta_content_data.py"),
    ("scripts/check_antislop_academic.py", "check_antislop_academic.py"),
    ("scripts/verify_sinta_refs.py", "verify_sinta_refs.py"),
    ("scripts/sinta_garuda_mcp.py", "sinta_garuda_mcp.py"),
]

CMD_LAPORAN_GENERATOR = """---
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
"""

CMD_MODE_ILMIAH = """---
description: Jalankan Sistem Operasi Tim Akademik 6 Fase & 6 Peran (Editor Kepala, Peneliti Literatur, Arsitek Metodologi, Penulis, Peer Reviewer 100 Poin, Inspektur)
---

# Perintah /mode-ilmiah

Jalankan alur lengkap 6 fase skill `mode-ilmiah` secara berurutan dengan mode reasoning tinggi, penyuntingan `humanizer-id` (`--preset akademik --kampus ubsi`) untuk naskah Bahasa Indonesia, kepatuhan **R1-R4** Mendeley, bebas halusinasi, serta pemeriksaan otomatis `check_antislop_academic.py` dan `verify_sinta_refs.py`.
"""

CMD_JURNAL_SINTA = """---
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
"""

CMD_SINTA_BUAT = """---
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
"""

CMD_SINTA_CEK = """---
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
"""

COMMANDS = [
    ("laporan-generator.md", CMD_LAPORAN_GENERATOR),
    ("mode-ilmiah.md", CMD_MODE_ILMIAH),
    ("jurnal-sinta.md", CMD_JURNAL_SINTA),
    ("sinta-buat.md", CMD_SINTA_BUAT),
    ("sinta-cek.md", CMD_SINTA_CEK),
]


def write_text(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def copy_if_different(src, dst):
    if not os.path.exists(src):
        return False
    if os.path.abspath(src) == os.path.abspath(dst):
        return True
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    shutil.copy2(src, dst)
    return True


def install_skill_bundle(target_skill_dir, skill_name, script_pairs=(), include_full_assets=False):
    """Install SKILL.md and optionally bundle self-contained scripts, presets, images, resources, and examples."""
    installed = []
    src_skill_dir = os.path.join(SKILLS_ROOT, skill_name)
    src_skill_md = os.path.join(src_skill_dir, "SKILL.md")
    dst_skill_md = os.path.join(target_skill_dir, "SKILL.md")
    if copy_if_different(src_skill_md, dst_skill_md):
        installed.append(dst_skill_md)

    for src_rel, dst_name in script_pairs:
        src_p = os.path.join(ROOT_DIR, src_rel.replace("/", os.sep))
        dst_p = os.path.join(target_skill_dir, "scripts", dst_name)
        if copy_if_different(src_p, dst_p):
            installed.append(dst_p)

    if script_pairs:
        for preset_file in ("sinta-journals.json", "sinta-catalog.json.gz"):
            preset_src = os.path.join(ROOT_DIR, "presets", preset_file)
            preset_dst = os.path.join(target_skill_dir, "presets", preset_file)
            if copy_if_different(preset_src, preset_dst):
                installed.append(preset_dst)

        gambar_src_dir = os.path.join(ROOT_DIR, "template", "gambar")
        if os.path.isdir(gambar_src_dir):
            for fname in os.listdir(gambar_src_dir):
                if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    src_img = os.path.join(gambar_src_dir, fname)
                    dst_img = os.path.join(target_skill_dir, "template", "gambar", fname)
                    if copy_if_different(src_img, dst_img):
                        installed.append(dst_img)

    if include_full_assets:
        for sub_dir in ("resources", "examples"):
            src_sub = os.path.join(src_skill_dir, sub_dir)
            if os.path.isdir(src_sub):
                for fname in os.listdir(src_sub):
                    src_item = os.path.join(src_sub, fname)
                    if os.path.isfile(src_item):
                        dst_item = os.path.join(target_skill_dir, sub_dir, fname)
                        if copy_if_different(src_item, dst_item):
                            installed.append(dst_item)

    return installed


def install_humanizer_bundle(target_skill_dir):
    """Salin skill humanizer-id beserta dataset, sub-skill, modul jurnal, & skrip (tanpa __pycache__)."""
    src_root = os.path.join(SKILLS_ROOT, "humanizer-id")
    if not os.path.isdir(src_root):
        return []
    installed = []
    allowed_roots = ("SKILL.md", "LICENSE")
    for fname in allowed_roots:
        if copy_if_different(os.path.join(src_root, fname), os.path.join(target_skill_dir, fname)):
            installed.append(os.path.join(target_skill_dir, fname))
    for sub in ("data", "humanizer_id", "scripts", "skills", "jurnal"):
        src_sub = os.path.join(src_root, sub)
        if not os.path.isdir(src_sub):
            continue
        for cur_root, dirs, files in os.walk(src_sub):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            rel = os.path.relpath(cur_root, src_root)
            for fname in files:
                if fname.endswith((".pyc", ".pyo")):
                    continue
                src_f = os.path.join(cur_root, fname)
                dst_f = os.path.join(target_skill_dir, rel, fname)
                if copy_if_different(src_f, dst_f):
                    installed.append(dst_f)
    return installed


def build_agents_md(rule_text, mode_ilmiah_text, jurnal_sinta_text, laporan_gen_text):
    return f"""# AGENTS.md - Panduan Universal AI Agent & CLI (Antigravity, KiloCode, OpenCode, Freebuff, Claude, Cursor)

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

{rule_text}

---

{laporan_gen_text}

---

{jurnal_sinta_text}

---

{mode_ilmiah_text}
"""


def _read_skill(name):
    p = os.path.join(SKILLS_ROOT, name, "SKILL.md")
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def install_all(target_workspace=None, install_global=True):
    ws = os.path.abspath(target_workspace or ROOT_DIR)
    laporan_text = _read_skill("laporan-generator")
    jurnal_text = _read_skill("jurnal-sinta")
    mode_text = _read_skill("mode-ilmiah")
    with open(RULE_SRC, "r", encoding="utf-8") as f:
        rule_text = f.read()

    rule_body = rule_text.split("---", 2)[-1].strip() if rule_text.startswith("---") else rule_text
    agents_md_content = build_agents_md(rule_body, mode_text, jurnal_text, laporan_text)
    installed_paths = []

    # 1. Universal Entry Files (OpenCode, Freebuff/Codebuff, Codex, Cursor, Aider, Claude Code)
    for univ_file in ("AGENTS.md", "CLAUDE.md", "knowledge.md"):
        p = os.path.join(ws, univ_file)
        write_text(p, agents_md_content)
        installed_paths.append(("Universal Entry", p))

    # 2. Skill Bundles (Workspace .agents/, OpenCode, Freebuff)
    skill_roots = [
        ("Antigravity (Workspace)", os.path.join(ws, ".agents", "skills")),
        ("OpenCode CLI (Workspace)", os.path.join(ws, ".opencode", "skills")),
        ("Freebuff CLI (Workspace)", os.path.join(ws, ".freebuff", "skills")),
    ]
    home = os.path.expanduser("~")
    if install_global:
        skill_roots.extend(
            [
                ("Antigravity (Global)", os.path.join(home, ".gemini", "config", "skills")),
                ("OpenCode CLI (Global)", os.path.join(home, ".config", "opencode", "skills")),
                ("Freebuff CLI (Global)", os.path.join(home, ".config", "freebuff", "skills")),
            ]
        )

    for label, sroot in skill_roots:
        for p in install_skill_bundle(os.path.join(sroot, "laporan-generator"), "laporan-generator", LAPORAN_SCRIPTS, include_full_assets=True):
            installed_paths.append((f"{label} / laporan-generator", p))
        for p in install_skill_bundle(os.path.join(sroot, "jurnal-sinta"), "jurnal-sinta", JURNAL_SCRIPTS, include_full_assets=False):
            installed_paths.append((f"{label} / jurnal-sinta", p))
        for p in install_skill_bundle(os.path.join(sroot, "mode-ilmiah"), "mode-ilmiah", (), include_full_assets=False):
            installed_paths.append((f"{label} / mode-ilmiah", p))
        for p in install_humanizer_bundle(os.path.join(sroot, "humanizer-id")):
            installed_paths.append((f"{label} / humanizer-id", p))

    # 3. Rule Sync (Antigravity Workspace & Global)
    rule_targets = [("Antigravity Rule (Workspace)", os.path.join(ws, ".agents", "rules", "sinta-journal-prompt.md"))]
    if install_global:
        rule_targets.append(("Antigravity Rule (Global)", os.path.join(home, ".gemini", "config", "rules", "sinta-journal-prompt.md")))
    for label, rp in rule_targets:
        copy_if_different(RULE_SRC, rp)
        installed_paths.append((label, rp))

    # 4. Multi-Agent Slash Commands & Rules (Workspace + Global)
    cmd_dirs = [
        ("KiloCode Workflow (Workspace)", os.path.join(ws, ".kilocode", "workflows")),
        ("OpenCode Command (Workspace)", os.path.join(ws, ".opencode", "commands")),
        ("Freebuff Command (Workspace)", os.path.join(ws, ".freebuff", "commands")),
        ("Claude Code Command (Workspace)", os.path.join(ws, ".claude", "commands")),
        ("Roo Code Command (Workspace)", os.path.join(ws, ".roo", "commands")),
    ]
    if install_global:
        cmd_dirs.extend(
            [
                ("KiloCode Workflow (Global)", os.path.join(home, ".kilocode", "workflows")),
                ("OpenCode Command (Global)", os.path.join(home, ".config", "opencode", "commands")),
                ("Freebuff Command (Global)", os.path.join(home, ".config", "freebuff", "commands")),
                ("Claude Code Command (Global)", os.path.join(home, ".claude", "commands")),
            ]
        )
    for label, cdir in cmd_dirs:
        for cmd_name, cmd_body in COMMANDS:
            cp = os.path.join(cdir, cmd_name)
            write_text(cp, cmd_body)
            installed_paths.append((label, cp))

    other_rules = [
        ("KiloCode Rule (Workspace)", os.path.join(ws, ".kilocode", "rules", "jurnal-sinta.md"), agents_md_content),
        ("Roo Code Rule", os.path.join(ws, ".roo", "rules", "jurnal-sinta.md"), agents_md_content),
        ("Cline Rule", os.path.join(ws, ".clinerules", "jurnal-sinta.md"), agents_md_content),
        (
            "Cursor Rule",
            os.path.join(ws, ".cursor", "rules", "jurnal-sinta.mdc"),
            "---\ndescription: Protokol Laporan Generator, Mode Ilmiah, & Jurnal SINTA 1-6\nglobs: *\nalwaysApply: true\n---\n\n" + agents_md_content,
        ),
        ("Windsurf Rule", os.path.join(ws, ".windsurfrules"), agents_md_content),
        ("GitHub Copilot Rule", os.path.join(ws, ".github", "copilot-instructions.md"), agents_md_content),
    ]
    if install_global:
        other_rules.append(("KiloCode Rule (Global)", os.path.join(home, ".kilocode", "rules", "jurnal-sinta.md"), agents_md_content))

    for label, ap, content in other_rules:
        write_text(ap, content)
        installed_paths.append((label, ap))

    return installed_paths


def check_status(target_workspace=None):
    ws = os.path.abspath(target_workspace or ROOT_DIR)
    home = os.path.expanduser("~")
    checks = [
        ("Antigravity laporan-generator (Workspace)", os.path.join(ws, ".agents", "skills", "laporan-generator", "SKILL.md")),
        ("Antigravity laporan-generator Bundled Script (Workspace)", os.path.join(ws, ".agents", "skills", "laporan-generator", "scripts", "generate_sinta_journal_docx.py")),
        ("Antigravity laporan-generator Preset (Workspace)", os.path.join(ws, ".agents", "skills", "laporan-generator", "presets", "sinta-journals.json")),
        ("Antigravity laporan-generator Examples (Workspace)", os.path.join(ws, ".agents", "skills", "laporan-generator", "examples", "CONTOH_JURNAL_SINTA4_JKI_2KOLOM.docx")),
        ("Antigravity laporan-generator (Global)", os.path.join(home, ".gemini", "config", "skills", "laporan-generator", "SKILL.md")),
        ("Antigravity laporan-generator Bundled Script (Global)", os.path.join(home, ".gemini", "config", "skills", "laporan-generator", "scripts", "generate_sinta_journal_docx.py")),
        ("Antigravity laporan-generator Examples (Global)", os.path.join(home, ".gemini", "config", "skills", "laporan-generator", "examples", "CONTOH_DOSIR_REFERENSI_SINTA5.docx")),
        ("Antigravity jurnal-sinta (Workspace)", os.path.join(ws, ".agents", "skills", "jurnal-sinta", "SKILL.md")),
        ("Antigravity jurnal-sinta (Global)", os.path.join(home, ".gemini", "config", "skills", "jurnal-sinta", "SKILL.md")),
        ("Antigravity mode-ilmiah (Workspace)", os.path.join(ws, ".agents", "skills", "mode-ilmiah", "SKILL.md")),
        ("Antigravity mode-ilmiah (Global)", os.path.join(home, ".gemini", "config", "skills", "mode-ilmiah", "SKILL.md")),
        ("Antigravity humanizer-id (Workspace)", os.path.join(ws, ".agents", "skills", "humanizer-id", "SKILL.md")),
        ("Antigravity humanizer-id UBSI Preset (Global)", os.path.join(home, ".gemini", "config", "skills", "humanizer-id", "data", "pedoman-kampus-ubsi.json")),
        ("Antigravity humanizer-id (Global)", os.path.join(home, ".gemini", "config", "skills", "humanizer-id", "SKILL.md")),
        ("Antigravity Rule (Global)", os.path.join(home, ".gemini", "config", "rules", "sinta-journal-prompt.md")),
        ("KiloCode /laporan-generator (Global)", os.path.join(home, ".kilocode", "workflows", "laporan-generator.md")),
        ("OpenCode CLI /laporan-generator (Global)", os.path.join(home, ".config", "opencode", "commands", "laporan-generator.md")),
        ("Freebuff CLI /laporan-generator (Global)", os.path.join(home, ".config", "freebuff", "commands", "laporan-generator.md")),
        ("Claude Code CLI /laporan-generator (Global)", os.path.join(home, ".claude", "commands", "laporan-generator.md")),
        ("Universal AGENTS.md", os.path.join(ws, "AGENTS.md")),
    ]
    report = [
        {"agent": name, "status": "INSTALLED" if os.path.exists(path) else "MISSING", "path": path}
        for name, path in checks
    ]
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Universal Installer Skill Mandiri (laporan-generator, mode-ilmiah, jurnal-sinta + Bundled Scripts/Presets/Examples)"
    )
    parser.add_argument("--target", default=ROOT_DIR, help="Folder proyek target instalasi (default: workspace saat ini)")
    parser.add_argument("--no-global", action="store_true", help="Hanya pasang di folder proyek tanpa direktori global user")
    parser.add_argument("--status", action="store_true", help="Cek status instalasi di seluruh AI Agent & CLI")
    args = parser.parse_args()

    if args.status:
        check_status(args.target)
        return

    installed = install_all(target_workspace=args.target, install_global=not args.no_global)
    print(f"[BERHASIL] Terpasang {len(installed)} file konfigurasi, skill mandiri, scripts, presets, resources, & examples.")


if __name__ == "__main__":
    main()
