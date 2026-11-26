# /// script
# requires-python = ">=3.10"
# ///
"""
Maintainer & Multi-Agent Sync Installer for the Unified Single Skill (`laporan-generator`):
- Keeps `.agents/skills/laporan-generator/` as the single source of truth (1 SKILL.md across the repo,
  ready for `npx skills add Sutannn13/laporan-generator` and zero-clone `npx` installs).
- Syncs runtime Python scripts, SINTA presets, minimal template assets (`logo-ubsi.png` + `simbol_*.png`),
  `references/` (mode-ilmiah, jurnal-sinta, humanizer-id, methodology, anti-slop), `humanizer_id/`, & `data/`.
- Non-destructive by default on external workspaces: NEVER overwrites user-owned AGENTS.md/CLAUDE.md unless
  syncing the repository root itself or `--sync-repo-docs` is explicitly requested.
"""
import argparse
import json
import os
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_NAME = "laporan-generator"
SKILLS_ROOT = os.path.join(ROOT_DIR, ".agents", "skills")
SOURCE_SKILL_DIR = os.path.join(SKILLS_ROOT, SKILL_NAME)
RULE_SRC = os.path.join(ROOT_DIR, ".agents", "rules", "sinta-journal-prompt.md")
LEGACY_SKILL_NAMES = ("jurnal-sinta", "mode-ilmiah", "humanizer-id")

RUNTIME_SCRIPTS = [
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

CMD_LAPORAN_GENERATOR = """---
description: Buat atau edit in-place Laporan/Proposal PKL UBSI, Skripsi/TA, Laporan Tugas/Audit TI/Analitik, Jurnal SINTA 1-6, atau Dosir Referensi Mendeley dalam Word (.docx OpenXML)
---

# Perintah /laporan-generator

Aktifkan skill terpadu `laporan-generator` (`SKILL.md`) dan muat hanya berkas rujukan yang relevan di `references/`:
1. Prioritaskan **Word (`.docx`) Python OpenXML** memakai skrip ter-bundle di `<skill_dir>/scripts/`.
2. Klasifikasikan jenis dokumen (`Laporan/Proposal PKL UBSI`, `Skripsi/TA UBSI 2026`, `Laporan Tugas/Audit/Analitik`, `Jurnal SINTA 1-6`, atau `Dosir Referensi Mendeley`).
3. Terapkan `references/mode-ilmiah.md`, `references/matriks-metodologi-ilmiah.md`, `references/antislop-akademik-id.md`, serta `references/humanizer-id.md` (`--preset akademik --kampus ubsi` khusus naskah Bahasa Indonesia), dan patuhi hukum **R1-R4**.
4. Verifikasi akhir wajib:
   - `python "<skill_dir>/scripts/audit_humanizer.py" "<draf_teks.md>" --preset akademik --kampus ubsi`
   - `uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"`
   - `uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --mendeley-mode`
"""

CMD_MODE_ILMIAH = """---
description: Jalankan Sistem Operasi Tim Akademik 6 Fase & 6 Peran (Editor Kepala, Peneliti Literatur, Arsitek Metodologi, Penulis, Peer Reviewer 100 Poin, Inspektur)
---

# Perintah /mode-ilmiah

Aktifkan skill terpadu `laporan-generator` dan baca `references/mode-ilmiah.md`. Jalankan alur lengkap 6 fase secara berurutan dengan penyuntingan `references/humanizer-id.md` (`--preset akademik --kampus ubsi`) untuk naskah Bahasa Indonesia, kepatuhan **R1-R4** Mendeley, bebas halusinasi, serta pemeriksaan otomatis `check_antislop_academic.py` dan `verify_sinta_refs.py`.
"""

CMD_JURNAL_SINTA = """---
description: Buat Jurnal Ilmiah SINTA 1-6 (2 Kolom / 1 Kolom, DOI Crossref 2022-2026), Laporan PKL, atau lanjutkan draf .docx in-place patuh R1-R4
---

# Perintah /jurnal-sinta (Multi-Agent Command)

Aktifkan skill terpadu `laporan-generator` dan baca `references/jurnal-sinta.md` bersama `references/mode-ilmiah.md`:
1. **Jika membuat Jurnal SINTA 1-6 baru dari nol**: tanyakan 3 opsi (peringkat SINTA `1-6`, tata letak `2col`/`1col`, gaya sitasi `ieee`/`apa`) lalu jalankan generator dengan `--mendeley-mode` (R1).
2. **Jika menyunting berkas `.docx` milik pengguna**: inspeksi DNA template dahulu (`--inspect-docx`) dan sunting *live in-place* (R2) tanpa menulis Daftar Pustaka ke `.docx` (R1).
3. **Standar R3 & Anti-Slop**: rujukan `.txt` terpisah wajib terbitan `2022-2026`, DOI Crossref HTTP 200, dan link PDF langsung HTTP 200; lulus `check_antislop_academic.py` (`std >= 5.5` kata, 0 em-dash).
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
   uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "$ARGUMENTS" --mendeley-mode
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


def _is_runtime_image(fname):
    low = fname.lower()
    return low == "logo-ubsi.png" or (low.startswith("simbol_") and low.endswith(".png"))


def sync_source_skill_assets():
    """Keep `.agents/skills/laporan-generator/` synced with root runtime scripts, presets, and minimal images."""
    synced = []
    for src_rel, dst_name in RUNTIME_SCRIPTS:
        src_p = os.path.join(ROOT_DIR, src_rel.replace("/", os.sep))
        dst_p = os.path.join(SOURCE_SKILL_DIR, "scripts", dst_name)
        if copy_if_different(src_p, dst_p):
            synced.append(dst_p)

    for preset_file in ("sinta-journals.json", "sinta-catalog.json.gz"):
        src_p = os.path.join(ROOT_DIR, "presets", preset_file)
        dst_p = os.path.join(SOURCE_SKILL_DIR, "presets", preset_file)
        if copy_if_different(src_p, dst_p):
            synced.append(dst_p)

    gambar_src_dir = os.path.join(ROOT_DIR, "template", "gambar")
    gambar_dst_dir = os.path.join(SOURCE_SKILL_DIR, "template", "gambar")
    os.makedirs(gambar_dst_dir, exist_ok=True)
    if os.path.isdir(gambar_src_dir):
        for fname in os.listdir(gambar_src_dir):
            if _is_runtime_image(fname):
                if copy_if_different(os.path.join(gambar_src_dir, fname), os.path.join(gambar_dst_dir, fname)):
                    synced.append(os.path.join(gambar_dst_dir, fname))
    # Prune non-runtime sample images and legacy examples dir from the skill bundle
    for fname in os.listdir(gambar_dst_dir):
        if not _is_runtime_image(fname):
            os.remove(os.path.join(gambar_dst_dir, fname))
    legacy_ex = os.path.join(SOURCE_SKILL_DIR, "examples")
    if os.path.isdir(legacy_ex):
        shutil.rmtree(legacy_ex, ignore_errors=True)
    return synced


def copy_unified_skill_bundle(target_skill_dir):
    """Copy the single unified `laporan-generator` bundle into target_skill_dir (excluding __pycache__ & bloat)."""
    src_abs = os.path.abspath(SOURCE_SKILL_DIR)
    dst_abs = os.path.abspath(target_skill_dir)
    installed = []

    if src_abs == dst_abs:
        for cur_root, dirs, files in os.walk(src_abs):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fname in files:
                if fname.endswith((".pyc", ".pyo")):
                    continue
                installed.append(os.path.join(cur_root, fname))
        return installed

    parent = os.path.dirname(dst_abs)
    os.makedirs(parent, exist_ok=True)
    stage_dir = os.path.join(parent, f".{SKILL_NAME}.stage-{os.getpid()}")
    if os.path.exists(stage_dir):
        shutil.rmtree(stage_dir, ignore_errors=True)

    try:
        for cur_root, dirs, files in os.walk(src_abs):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "examples")]
            rel_dir = os.path.relpath(cur_root, src_abs)
            for fname in files:
                if fname.endswith((".pyc", ".pyo", ".bak")) or fname in (".DS_Store", "Thumbs.db"):
                    continue
                rel_file = fname if rel_dir == "." else os.path.join(rel_dir, fname)
                norm_rel = rel_file.replace("\\", "/")
                if norm_rel.startswith("template/gambar/") and not _is_runtime_image(fname):
                    continue
                dst_stage = os.path.join(stage_dir, rel_file)
                os.makedirs(os.path.dirname(dst_stage), exist_ok=True)
                shutil.copy2(os.path.join(cur_root, fname), dst_stage)
                installed.append(os.path.join(dst_abs, rel_file))

        if os.path.exists(dst_abs):
            shutil.rmtree(dst_abs)
        os.replace(stage_dir, dst_abs)
    except Exception:
        if os.path.exists(stage_dir):
            shutil.rmtree(stage_dir, ignore_errors=True)
        raise

    return installed


def build_agents_md(rule_text, skill_text):
    return f"""# AGENTS.md - Panduan Universal AI Agent & CLI (Antigravity, Claude Code, Cursor, OpenCode, Freebuff, KiloCode)

Repositori ini menyediakan **1 skill terpadu (`laporan-generator`)** untuk pembuatan, pengeditan *in-place*, penyuntingan bahasa Indonesia baku (`humanizer-id` preset UBSI), dan audit otomatis **Jurnal Ilmiah Terakreditasi SINTA 1-6** (Word `.docx` & Typst `.pdf`), **Jurnal Internasional Bereputasi (Scopus Q1-Q4)**, **Skripsi/Tugas Akhir & Laporan/Proposal PKL UBSI (SK Rektor 2026)**, serta **Laporan Audit/Analitik Data**.

## Pemasangan Tanpa Clone (1 Baris)
```powershell
npx skills add Sutannn13/laporan-generator
# atau installer bawaan beserta slash command & cek runtime uv (kompatibel npm 12+):
npx -y --allow-git=all github:Sutannn13/laporan-generator install
```

## Daftar Slash Commands / Perintah Agent
- `/laporan-generator` : Pintu utama skill terpadu (PKL UBSI, Skripsi 2026, Audit TI, Jurnal SINTA 1-6, & Dosir Referensi).
- `/mode-ilmiah`       : **Sistem Operasi Tim Akademik 6 Peran + Peer Reviewer >= 85/100** (`references/mode-ilmiah.md`).
- `/jurnal-sinta`      : Mode Jurnal SINTA 1-6 (6 instansi, 1/2 kolom, DOI Crossref & PDF HTTP 200, `references/jurnal-sinta.md`).
- `/sinta-buat`        : Generate cepat dokumen Word Jurnal SINTA 1-6 mode Mendeley (`R1`).
- `/sinta-cek`         : Inspeksi struktur internal `.docx` (`--inspect-docx`), cek Anti-Slop Burstiness, dan test suite (`npm run test:all`).

## Pintasan CLI Maintainer
```powershell
npm run sinta                            # Wizard interaktif Jurnal SINTA 1-6 (.docx)
npm run sinta:inspect -- "<file.docx>"   # Inspeksi template/draf .docx dari jurnal kampus lain
npm run sinta:showcase                   # Generate ulang contoh di contoh-template-ai/
npm run agent:install                    # Sinkronkan 1 skill terpadu, presets, & rules ke semua agent
npm run test:all                         # Jalankan seluruh test suite (Typst + Installer + Audit XML SINTA)
```

---

{rule_text}

---

{skill_text}
"""


def install_all(target_workspace=None, install_global=True, home_dir=None, sync_repo_docs=None):
    ws = os.path.abspath(target_workspace or ROOT_DIR)
    is_repo_root = ws == os.path.abspath(ROOT_DIR)
    should_sync_repo_docs = is_repo_root if sync_repo_docs is None else bool(sync_repo_docs)

    sync_source_skill_assets()

    with open(os.path.join(SOURCE_SKILL_DIR, "SKILL.md"), "r", encoding="utf-8") as f:
        skill_text = f.read()
    with open(RULE_SRC, "r", encoding="utf-8") as f:
        rule_text = f.read()

    rule_body = rule_text.split("---", 2)[-1].strip() if rule_text.startswith("---") else rule_text
    agents_md_content = build_agents_md(rule_body, skill_text)
    installed_paths = []

    # 1. Universal Entry Files ONLY for repo root maintainer docs (never overwrite external user projects!)
    if should_sync_repo_docs:
        for univ_file in ("AGENTS.md", "CLAUDE.md", "knowledge.md"):
            p = os.path.join(ws, univ_file)
            write_text(p, agents_md_content)
            installed_paths.append(("Universal Entry", p))

    # 2. Single Unified Skill Bundle (Workspace + Global)
    skill_roots = [
        ("Antigravity (Workspace)", os.path.join(ws, ".agents", "skills")),
        ("OpenCode CLI (Workspace)", os.path.join(ws, ".opencode", "skills")),
        ("Freebuff CLI (Workspace)", os.path.join(ws, ".freebuff", "skills")),
    ]
    home = os.path.abspath(home_dir) if home_dir else os.path.expanduser("~")
    if install_global:
        skill_roots.extend(
            [
                ("Antigravity (Global)", os.path.join(home, ".gemini", "config", "skills")),
                ("Universal Agents (Global)", os.path.join(home, ".agents", "skills")),
                ("Claude Code (Global)", os.path.join(home, ".claude", "skills")),
                ("OpenCode CLI (Global)", os.path.join(home, ".config", "opencode", "skills")),
                ("Freebuff CLI (Global)", os.path.join(home, ".config", "freebuff", "skills")),
            ]
        )

    for label, sroot in skill_roots:
        for p in copy_unified_skill_bundle(os.path.join(sroot, SKILL_NAME)):
            installed_paths.append((f"{label} / {SKILL_NAME}", p))
        # Clean legacy duplicate skill folders inside repo-local roots only
        if sroot.startswith(ws):
            for legacy in LEGACY_SKILL_NAMES:
                leg_dir = os.path.join(sroot, legacy)
                if os.path.isdir(leg_dir):
                    shutil.rmtree(leg_dir, ignore_errors=True)

    # 3. Rule Sync (Scoped files only on external workspaces)
    rule_targets = [("Antigravity Rule (Workspace)", os.path.join(ws, ".agents", "rules", "sinta-journal-prompt.md"))]
    if install_global:
        rule_targets.append(("Antigravity Rule (Global)", os.path.join(home, ".gemini", "config", "rules", "sinta-journal-prompt.md")))
    for label, rp in rule_targets:
        copy_if_different(RULE_SRC, rp)
        installed_paths.append((label, rp))

    # 4. Multi-Agent Slash Commands (Workspace + Global)
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
        ("KiloCode Rule (Workspace)", os.path.join(ws, ".kilocode", "rules", "laporan-generator.md"), agents_md_content),
        ("Roo Code Rule", os.path.join(ws, ".roo", "rules", "laporan-generator.md"), agents_md_content),
        (
            "Cursor Rule",
            os.path.join(ws, ".cursor", "rules", "laporan-generator.mdc"),
            "---\ndescription: Protokol Skill Terpadu laporan-generator (Mode Ilmiah, Jurnal SINTA 1-6, PKL/Skripsi UBSI, R1-R4)\nglobs: *\nalwaysApply: true\n---\n\n" + agents_md_content,
        ),
    ]
    if should_sync_repo_docs:
        other_rules.extend(
            [
                ("Cline Rule", os.path.join(ws, ".clinerules", "jurnal-sinta.md"), agents_md_content),
                ("Windsurf Rule", os.path.join(ws, ".windsurfrules"), agents_md_content),
                ("GitHub Copilot Rule", os.path.join(ws, ".github", "copilot-instructions.md"), agents_md_content),
            ]
        )
    if install_global:
        other_rules.append(("KiloCode Rule (Global)", os.path.join(home, ".kilocode", "rules", "laporan-generator.md"), agents_md_content))

    for label, ap, content in other_rules:
        write_text(ap, content)
        installed_paths.append((label, ap))

    return installed_paths


def check_status(target_workspace=None, home_dir=None):
    ws = os.path.abspath(target_workspace or ROOT_DIR)
    home = os.path.abspath(home_dir) if home_dir else os.path.expanduser("~")
    checks = [
        ("Unified Skill laporan-generator (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "SKILL.md")),
        ("Unified Skill References: mode-ilmiah (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "references", "mode-ilmiah.md")),
        ("Unified Skill References: jurnal-sinta (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "references", "jurnal-sinta.md")),
        ("Unified Skill References: humanizer-id (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "references", "humanizer-id.md")),
        ("Unified Skill Bundled Script (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "scripts", "generate_sinta_journal_docx.py")),
        ("Unified Skill Humanizer CLI (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "scripts", "audit_humanizer.py")),
        ("Unified Skill SINTA Catalog (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "presets", "sinta-catalog.json.gz")),
        ("Unified Skill UBSI Preset (Workspace)", os.path.join(ws, ".agents", "skills", SKILL_NAME, "data", "pedoman-kampus-ubsi.json")),
        ("Antigravity laporan-generator (Global)", os.path.join(home, ".gemini", "config", "skills", SKILL_NAME, "SKILL.md")),
        ("Universal Agents laporan-generator (Global)", os.path.join(home, ".agents", "skills", SKILL_NAME, "SKILL.md")),
        ("Claude Code laporan-generator (Global)", os.path.join(home, ".claude", "skills", SKILL_NAME, "SKILL.md")),
        ("Antigravity Bundled Script (Global)", os.path.join(home, ".gemini", "config", "skills", SKILL_NAME, "scripts", "generate_sinta_journal_docx.py")),
        ("Antigravity Humanizer UBSI Preset (Global)", os.path.join(home, ".gemini", "config", "skills", SKILL_NAME, "data", "pedoman-kampus-ubsi.json")),
        ("Antigravity Rule (Global)", os.path.join(home, ".gemini", "config", "rules", "sinta-journal-prompt.md")),
        ("KiloCode /laporan-generator (Global)", os.path.join(home, ".kilocode", "workflows", "laporan-generator.md")),
        ("OpenCode CLI /laporan-generator (Global)", os.path.join(home, ".config", "opencode", "commands", "laporan-generator.md")),
        ("Freebuff CLI /laporan-generator (Global)", os.path.join(home, ".config", "freebuff", "commands", "laporan-generator.md")),
        ("Claude Code CLI /laporan-generator (Global)", os.path.join(home, ".claude", "commands", "laporan-generator.md")),
    ]
    report = [
        {"agent": name, "status": "INSTALLED" if os.path.exists(path) else "MISSING", "path": path}
        for name, path in checks
    ]
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Universal Installer 1 Skill Terpadu (`laporan-generator`: Mode Ilmiah, Jurnal SINTA 1-6, Humanizer ID UBSI, & Bundled Scripts/Presets)"
    )
    parser.add_argument("--target", default=ROOT_DIR, help="Folder proyek target instalasi (default: workspace saat ini)")
    parser.add_argument("--home", default=None, help="Override direktori home user (untuk pengujian terisolasi)")
    parser.add_argument("--no-global", action="store_true", help="Hanya pasang di folder proyek tanpa direktori global user")
    parser.add_argument("--sync-repo-docs", action="store_true", help="Izinkan pembaruan AGENTS.md/CLAUDE.md di direktori target")
    parser.add_argument("--status", action="store_true", help="Cek status instalasi di seluruh AI Agent & CLI")
    args = parser.parse_args()

    if args.status:
        check_status(args.target, home_dir=args.home)
        return

    installed = install_all(
        target_workspace=args.target,
        install_global=not args.no_global,
        home_dir=args.home,
        sync_repo_docs=True if args.sync_repo_docs else None,
    )
    print(f"[BERHASIL] Terpasang {len(installed)} berkas skill terpadu '{SKILL_NAME}', references, scripts, presets, & slash commands.")


if __name__ == "__main__":
    main()
