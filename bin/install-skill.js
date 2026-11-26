#!/usr/bin/env node
/**
 * Zero-Clone Pure-Node Skill Installer for `laporan-generator` (Unified Single Skill).
 *
 * Usage:
 *   npx -y github:Sutannn13/laporan-generator install [--workspace [dir]] [--no-global] [--require-uv]
 *   npx -y github:Sutannn13/laporan-generator status [--json] [--workspace [dir]]
 *   npx -y github:Sutannn13/laporan-generator uninstall [--workspace [dir]] [--no-global]
 *
 * Guarantees:
 * - Installs 1 unified skill (`laporan-generator`) containing references/, scripts/, presets/,
 *   humanizer_id/, data/, and minimal runtime template assets (logo-ubsi.png + simbol_*.png).
 * - Zero `git clone` folder left behind and zero `uv` dependency required just to install files.
 * - Non-destructive: NEVER overwrites user-owned AGENTS.md, CLAUDE.md, knowledge.md,
 *   .windsurfrules, or .github/copilot-instructions.md.
 * - Idempotent: repeated runs cleanly refresh managed files without creating duplicates.
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const PKG_ROOT = path.resolve(__dirname, '..');
const SKILL_NAME = 'laporan-generator';
const MANIFEST_FILE = '.laporan-generator-managed.json';
const PKG_VERSION = (() => {
  try {
    return JSON.parse(fs.readFileSync(path.join(PKG_ROOT, 'package.json'), 'utf8')).version || '1.0.0';
  } catch {
    return '1.0.0';
  }
})();

const COMMANDS = [
  {
    name: 'laporan-generator.md',
    body: `---
description: Buat atau edit in-place Laporan/Proposal PKL UBSI, Skripsi/TA, Laporan Audit TI/Analitik, Jurnal SINTA 1-6, atau Dosir Referensi Mendeley (.docx OpenXML)
---

# Perintah /laporan-generator

Aktifkan skill terpadu \`laporan-generator\` (\`SKILL.md\`) lalu muat hanya berkas rujukan yang relevan di \`references/\`:
1. Prioritaskan **Word (\`.docx\`) Python OpenXML** memakai skrip di \`<skill_dir>/scripts/\`.
2. Klasifikasikan dokumen (\`PKL UBSI\`, \`Skripsi/TA UBSI 2026\`, \`Audit COBIT / Analitik\`, \`Jurnal SINTA 1-6 / Scopus\`, atau \`Dosir Referensi Mendeley\`).
3. Muat \`references/mode-ilmiah.md\`, \`references/matriks-metodologi-ilmiah.md\`, \`references/antislop-akademik-id.md\`, serta \`references/humanizer-id.md\` (khusus naskah Bahasa Indonesia) dan patuhi hukum **R1-R4**.
4. Verifikasi akhir wajib:
   - \`python "<skill_dir>/scripts/audit_humanizer.py" "<draf_teks.md>" --preset akademik --kampus ubsi\`
   - \`uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<target.docx>"\`
   - \`uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<target.docx>" --mendeley-mode\`
`,
  },
  {
    name: 'mode-ilmiah.md',
    body: `---
description: Jalankan Sistem Operasi Tim Akademik 6 Fase & 6 Peran (Rubrik Peer Reviewer >= 85/100) dari skill terpadu laporan-generator
---

# Perintah /mode-ilmiah

Aktifkan skill \`laporan-generator\` dan muat \`references/mode-ilmiah.md\`. Jalankan alur lengkap 6 fase secara berurutan dengan kepatuhan **R1-R4** Mendeley, bebas halusinasi, penyuntingan \`references/humanizer-id.md\` (khusus naskah Bahasa Indonesia), serta verifikasi otomatis \`check_antislop_academic.py\` dan \`verify_sinta_refs.py\`.
`,
  },
  {
    name: 'jurnal-sinta.md',
    body: `---
description: Buat atau sunting in-place Jurnal Ilmiah SINTA 1-6 (1/2 Kolom, DOI Crossref 2022-2026) patuh R1-R4 Mendeley
---

# Perintah /jurnal-sinta

Aktifkan skill \`laporan-generator\` dan muat \`references/jurnal-sinta.md\` bersama \`references/mode-ilmiah.md\`:
1. Jika membuat Jurnal SINTA 1-6 baru dari nol, tanyakan 3 opsi (jika belum ditentukan): peringkat SINTA \`1-6\`, tata letak kolom (\`2col\` / \`1col\`), dan gaya sitasi (\`ieee\` / \`apa\`). Gunakan \`--mendeley-mode\` (R1).
2. Jika menyunting file \`.docx\` milik pengguna, wajib jalankan \`--inspect-docx\` dahulu dan sunting *live in-place* (R2) tanpa menulis Daftar Pustaka ke \`.docx\` (R1).
3. Referensi kandidat di \`.txt\` terpisah wajib terbitan \`2022-2026\`, DOI Crossref HTTP 200, dan tautan PDF langsung HTTP 200 (R3).
`,
  },
  {
    name: 'sinta-buat.md',
    body: `---
description: Generate cepat berkas Word (.docx) Jurnal SINTA 1-6 dalam mode Mendeley (R1)
---

# Perintah /sinta-buat

Jalankan generator Word dari bundel skill \`laporan-generator\`:
\`\`\`powershell
uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --sinta 4 --layout 2col --citation ieee --mendeley-mode --yes
\`\`\`
`,
  },
  {
    name: 'sinta-cek.md',
    body: `---
description: Inspeksi struktur internal .docx (--inspect-docx) dan audit Anti-Slop + Burstiness + R1 Mendeley
---

# Perintah /sinta-cek

Jalankan inspeksi dan audit pada dokumen target (\`$ARGUMENTS\`):
\`\`\`powershell
uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "$ARGUMENTS"
uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "$ARGUMENTS" --mendeley-mode
\`\`\`
`,
  },
];

function resolveHomeDir(explicitHome) {
  if (explicitHome) return path.resolve(explicitHome);
  if (process.env.LAPORAN_GENERATOR_HOME) return path.resolve(process.env.LAPORAN_GENERATOR_HOME);
  return os.homedir();
}

function resolveSourceSkillDir() {
  const src = path.join(PKG_ROOT, '.agents', 'skills', SKILL_NAME);
  if (!fs.existsSync(path.join(src, 'SKILL.md'))) {
    throw new Error(`Bundel skill utama tidak ditemukan di: ${src}`);
  }
  return src;
}

function resolveSourceRulePath() {
  const rule = path.join(PKG_ROOT, '.agents', 'rules', 'sinta-journal-prompt.md');
  return fs.existsSync(rule) ? rule : null;
}

function shouldSkipEntry(relPath, entryName) {
  if (entryName === '__pycache__' || entryName === '.DS_Store' || entryName === 'Thumbs.db') return true;
  if (entryName.endsWith('.pyc') || entryName.endsWith('.pyo') || entryName.endsWith('.bak')) return true;
  const norm = relPath.replace(/\\/g, '/');
  if (norm === 'examples' || norm.startsWith('examples/')) return true;
  if (norm.startsWith('template/gambar/')) {
    const base = path.basename(norm);
    if (base !== 'logo-ubsi.png' && !base.startsWith('simbol_')) return true;
  }
  return false;
}

function copySkillTree(srcDir, dstDir) {
  const absSrc = path.resolve(srcDir);
  const absDst = path.resolve(dstDir);
  if (absSrc === absDst) {
    return collectRelativeFiles(absDst);
  }

  // Stage to a sibling temporary folder before swapping to avoid leaving a half-copied skill on error.
  const parent = path.dirname(absDst);
  fs.mkdirSync(parent, { recursive: true });
  const stageDir = path.join(parent, `.${SKILL_NAME}.tmp-${process.pid}-${Date.now()}`);
  const copiedRel = [];

  try {
    fs.mkdirSync(stageDir, { recursive: true });
    function walk(curSrc, relPrefix) {
      for (const ent of fs.readdirSync(curSrc, { withFileTypes: true })) {
        const rel = relPrefix ? `${relPrefix}/${ent.name}` : ent.name;
        if (shouldSkipEntry(rel, ent.name)) continue;
        const sPath = path.join(curSrc, ent.name);
        const dPath = path.join(stageDir, ...rel.split('/'));
        if (ent.isDirectory()) {
          fs.mkdirSync(dPath, { recursive: true });
          walk(sPath, rel);
        } else if (ent.isFile()) {
          fs.mkdirSync(path.dirname(dPath), { recursive: true });
          fs.copyFileSync(sPath, dPath);
          copiedRel.push(rel);
        }
      }
    }
    walk(absSrc, '');

    const manifest = {
      managedBy: 'laporan-generator-cli',
      skill: SKILL_NAME,
      version: PKG_VERSION,
      filesCount: copiedRel.length,
    };
    fs.writeFileSync(path.join(stageDir, MANIFEST_FILE), JSON.stringify(manifest, null, 2) + '\n', 'utf8');

    if (fs.existsSync(absDst)) {
      fs.rmSync(absDst, { recursive: true, force: true });
    }
    fs.renameSync(stageDir, absDst);
  } catch (err) {
    if (fs.existsSync(stageDir)) {
      try {
        fs.rmSync(stageDir, { recursive: true, force: true });
      } catch {}
    }
    throw err;
  }

  return copiedRel;
}

function collectRelativeFiles(dir) {
  const out = [];
  function walk(cur, prefix) {
    for (const ent of fs.readdirSync(cur, { withFileTypes: true })) {
      const rel = prefix ? `${prefix}/${ent.name}` : ent.name;
      if (shouldSkipEntry(rel, ent.name)) continue;
      const p = path.join(cur, ent.name);
      if (ent.isDirectory()) walk(p, rel);
      else if (ent.isFile()) out.push(rel);
    }
  }
  walk(dir, '');
  return out;
}

function writeFileSafe(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, 'utf8');
}

function probeCommand(cmd, args = ['--version']) {
  const res = spawnSync(cmd, args, {
    encoding: 'utf8',
    stdio: 'pipe',
    shell: process.platform === 'win32',
  });
  if (res.error || res.status !== 0) {
    return { available: false, version: null, error: res.error ? res.error.message : (res.stderr || '').trim() };
  }
  const firstLine = String(res.stdout || res.stderr || '').trim().split(/\r?\n/)[0] || 'ok';
  return { available: true, version: firstLine, error: null };
}

function checkRuntimes() {
  const uv = probeCommand('uv', ['--version']);
  let python = probeCommand('python', ['--version']);
  if (!python.available) {
    python = probeCommand('python3', ['--version']);
  }
  return { uv, python };
}

function buildTargetPlan({ homeDir, workspaceDir, installGlobal }) {
  const skillTargets = [];
  const commandTargets = [];
  const ruleTargets = [];

  if (installGlobal) {
    skillTargets.push(
      { label: 'Antigravity (Global)', dir: path.join(homeDir, '.gemini', 'config', 'skills', SKILL_NAME) },
      { label: 'Universal Agents (Global)', dir: path.join(homeDir, '.agents', 'skills', SKILL_NAME) },
      { label: 'Claude Code (Global)', dir: path.join(homeDir, '.claude', 'skills', SKILL_NAME) },
      { label: 'OpenCode CLI (Global)', dir: path.join(homeDir, '.config', 'opencode', 'skills', SKILL_NAME) },
      { label: 'Freebuff CLI (Global)', dir: path.join(homeDir, '.config', 'freebuff', 'skills', SKILL_NAME) }
    );
    commandTargets.push(
      { label: 'Claude Code Commands (Global)', dir: path.join(homeDir, '.claude', 'commands') },
      { label: 'KiloCode Workflows (Global)', dir: path.join(homeDir, '.kilocode', 'workflows') },
      { label: 'OpenCode Commands (Global)', dir: path.join(homeDir, '.config', 'opencode', 'commands') },
      { label: 'Freebuff Commands (Global)', dir: path.join(homeDir, '.config', 'freebuff', 'commands') }
    );
    ruleTargets.push(
      { label: 'Antigravity Rule (Global)', file: path.join(homeDir, '.gemini', 'config', 'rules', 'sinta-journal-prompt.md'), kind: 'rule' },
      { label: 'KiloCode Rule (Global)', file: path.join(homeDir, '.kilocode', 'rules', 'laporan-generator.md'), kind: 'rule' }
    );
  }

  if (workspaceDir) {
    const ws = path.resolve(workspaceDir);
    skillTargets.push(
      { label: 'Workspace Skill (.agents)', dir: path.join(ws, '.agents', 'skills', SKILL_NAME) }
    );
    commandTargets.push(
      { label: 'Claude Code Commands (Workspace)', dir: path.join(ws, '.claude', 'commands') },
      { label: 'KiloCode Workflows (Workspace)', dir: path.join(ws, '.kilocode', 'workflows') },
      { label: 'OpenCode Commands (Workspace)', dir: path.join(ws, '.opencode', 'commands') },
      { label: 'Freebuff Commands (Workspace)', dir: path.join(ws, '.freebuff', 'commands') },
      { label: 'Roo Code Commands (Workspace)', dir: path.join(ws, '.roo', 'commands') }
    );
    // Scoped rule files only — NEVER touch user's AGENTS.md, CLAUDE.md, .windsurfrules, or copilot-instructions.md
    ruleTargets.push(
      { label: 'Antigravity Rule (Workspace)', file: path.join(ws, '.agents', 'rules', 'sinta-journal-prompt.md'), kind: 'rule' },
      { label: 'Cursor Scoped Rule (Workspace)', file: path.join(ws, '.cursor', 'rules', 'laporan-generator.mdc'), kind: 'cursor' },
      { label: 'KiloCode Scoped Rule (Workspace)', file: path.join(ws, '.kilocode', 'rules', 'laporan-generator.md'), kind: 'rule' },
      { label: 'Roo Scoped Rule (Workspace)', file: path.join(ws, '.roo', 'rules', 'laporan-generator.md'), kind: 'rule' }
    );
  }

  return { skillTargets, commandTargets, ruleTargets };
}

function installSkill(options = {}) {
  const homeDir = resolveHomeDir(options.home);
  const installGlobal = options.global !== false;
  const workspaceDir = options.workspace ? path.resolve(options.workspace) : null;

  if (!installGlobal && !workspaceDir) {
    throw new Error('Tidak ada target instalasi. Aktifkan instalasi global (default) atau berikan --workspace <folder>.');
  }

  const runtimes = checkRuntimes();
  if (options.requireUv && !runtimes.uv.available) {
    const err = new Error(
      'Runtime `uv` tidak ditemukan di PATH (--require-uv aktif).\n' +
      'Pasang uv terlebih dahulu:\n' +
      '  Windows (PowerShell): powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"\n' +
      '  macOS / Linux       : curl -LsSf https://astral.sh/uv/install.sh | sh'
    );
    err.code = 'MISSING_UV';
    throw err;
  }

  const srcSkillDir = resolveSourceSkillDir();
  const srcRulePath = resolveSourceRulePath();
  const ruleRaw = srcRulePath ? fs.readFileSync(srcRulePath, 'utf8') : '';
  const ruleBody = ruleRaw.startsWith('---') ? ruleRaw.split('---').slice(2).join('---').trim() : ruleRaw.trim();

  const plan = buildTargetPlan({ homeDir, workspaceDir, installGlobal });
  const installedSkills = [];
  const installedCommands = [];
  const installedRules = [];

  for (const target of plan.skillTargets) {
    const files = copySkillTree(srcSkillDir, target.dir);
    installedSkills.push({ label: target.label, path: target.dir, filesCount: files.length });
  }

  for (const cmdTarget of plan.commandTargets) {
    for (const cmd of COMMANDS) {
      const dst = path.join(cmdTarget.dir, cmd.name);
      writeFileSafe(dst, cmd.body);
      installedCommands.push({ label: cmdTarget.label, path: dst });
    }
  }

  if (ruleRaw) {
    for (const rTarget of plan.ruleTargets) {
      const content =
        rTarget.kind === 'cursor'
          ? `---\ndescription: Protokol Skill Terpadu laporan-generator (Mode Ilmiah, Jurnal SINTA 1-6, PKL/Skripsi UBSI, R1-R4)\nglobs: *\nalwaysApply: true\n---\n\n${ruleBody}\n`
          : ruleRaw;
      writeFileSafe(rTarget.file, content);
      installedRules.push({ label: rTarget.label, path: rTarget.file });
    }
  }

  return {
    skill: SKILL_NAME,
    version: PKG_VERSION,
    homeDir,
    workspaceDir,
    installedSkills,
    installedCommands,
    installedRules,
    runtimes,
  };
}

function getStatus(options = {}) {
  const homeDir = resolveHomeDir(options.home);
  const installGlobal = options.global !== false;
  const workspaceDir = options.workspace ? path.resolve(options.workspace) : null;
  const plan = buildTargetPlan({ homeDir, workspaceDir, installGlobal });

  const checks = [];
  for (const s of plan.skillTargets) {
    const skillMd = path.join(s.dir, 'SKILL.md');
    const catalog = path.join(s.dir, 'presets', 'sinta-catalog.json.gz');
    const modeRef = path.join(s.dir, 'references', 'mode-ilmiah.md');
    const humRef = path.join(s.dir, 'references', 'humanizer-id.md');
    const ok = fs.existsSync(skillMd) && fs.existsSync(catalog) && fs.existsSync(modeRef) && fs.existsSync(humRef);
    checks.push({
      agent: s.label,
      status: ok ? 'INSTALLED' : 'MISSING',
      path: skillMd,
    });
  }
  for (const c of plan.commandTargets) {
    const entry = path.join(c.dir, 'laporan-generator.md');
    checks.push({
      agent: `${c.label} (/laporan-generator)`,
      status: fs.existsSync(entry) ? 'INSTALLED' : 'MISSING',
      path: entry,
    });
  }
  for (const r of plan.ruleTargets) {
    checks.push({
      agent: r.label,
      status: fs.existsSync(r.file) ? 'INSTALLED' : 'MISSING',
      path: r.file,
    });
  }

  return {
    skill: SKILL_NAME,
    version: PKG_VERSION,
    homeDir,
    workspaceDir,
    runtimes: checkRuntimes(),
    checks,
  };
}

function uninstallSkill(options = {}) {
  const homeDir = resolveHomeDir(options.home);
  const installGlobal = options.global !== false;
  const workspaceDir = options.workspace ? path.resolve(options.workspace) : null;
  const plan = buildTargetPlan({ homeDir, workspaceDir, installGlobal });
  const removed = [];

  for (const s of plan.skillTargets) {
    const absTarget = path.resolve(s.dir);
    const absSource = path.resolve(resolveSourceSkillDir());
    if (absTarget === absSource) continue;
    if (fs.existsSync(absTarget)) {
      fs.rmSync(absTarget, { recursive: true, force: true });
      removed.push(absTarget);
    }
  }
  for (const c of plan.commandTargets) {
    for (const cmd of COMMANDS) {
      const p = path.join(c.dir, cmd.name);
      if (fs.existsSync(p)) {
        fs.unlinkSync(p);
        removed.push(p);
      }
    }
  }
  for (const r of plan.ruleTargets) {
    const absRule = path.resolve(r.file);
    const srcRule = resolveSourceRulePath();
    if (srcRule && absRule === path.resolve(srcRule)) continue;
    if (fs.existsSync(absRule)) {
      fs.unlinkSync(absRule);
      removed.push(absRule);
    }
  }

  return { removed };
}

function parseCliArgs(argv) {
  const out = {
    action: 'install',
    global: true,
    workspace: null,
    home: null,
    requireUv: false,
    json: false,
    help: false,
  };

  let idx = 0;
  if (argv[0] && !argv[0].startsWith('-')) {
    const sub = argv[0].toLowerCase();
    if (['install', 'install-skill', 'skill', 'setup', 'status', 'uninstall', 'remove'].includes(sub)) {
      out.action = (sub === 'remove' || sub === 'uninstall')
        ? 'uninstall'
        : (sub === 'status' ? 'status' : 'install');
      idx = 1;
    }
  }

  for (let i = idx; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') {
      out.help = true;
    } else if (a === '--no-global') {
      out.global = false;
    } else if (a === '--require-uv') {
      out.requireUv = true;
    } else if (a === '--json') {
      out.json = true;
    } else if (a === '--workspace' || a === '--target') {
      const next = argv[i + 1];
      if (next && !next.startsWith('-')) {
        out.workspace = next;
        i++;
      } else {
        out.workspace = process.cwd();
      }
    } else if (a.startsWith('--workspace=')) {
      out.workspace = a.slice('--workspace='.length) || process.cwd();
    } else if (a.startsWith('--target=')) {
      out.workspace = a.slice('--target='.length) || process.cwd();
    } else if (a === '--home') {
      out.home = argv[++i];
    } else if (a.startsWith('--home=')) {
      out.home = a.slice('--home='.length);
    }
  }

  return out;
}

function printUsage() {
  console.log(`Laporan Generator - Zero-Clone Unified Skill Installer (1 Skill: ${SKILL_NAME})

Penggunaan (tanpa git clone):
  npx skills add Sutannn13/laporan-generator
  npx -y github:Sutannn13/laporan-generator install [opsi]
  npx -y github:Sutannn13/laporan-generator status [--json]
  npx -y github:Sutannn13/laporan-generator uninstall [opsi]

Opsi:
  --workspace [dir]   Tambahkan pemasangan scoped ke folder proyek (tanpa menimpa AGENTS.md/CLAUDE.md)
  --no-global         Jangan pasang ke direktori global user (wajib bersama --workspace)
  --home <dir>        Override direktori home user (untuk pengujian terisolasi)
  --require-uv        Gagal dengan exit code != 0 jika runtime uv belum terpasang
  --json              Cetak output JSON (untuk status/install)
  -h, --help          Tampilkan bantuan ini
`);
}

function runCli(argv = process.argv.slice(2)) {
  const opts = parseCliArgs(argv);
  if (opts.help) {
    printUsage();
    return 0;
  }

  try {
    if (opts.action === 'status') {
      const st = getStatus(opts);
      if (opts.json) {
        console.log(JSON.stringify(st, null, 2));
      } else {
        console.log(`Status Skill Terpadu: ${st.skill} (v${st.version})`);
        console.log(`Runtime uv     : ${st.runtimes.uv.available ? `OK (${st.runtimes.uv.version})` : 'BELUM TERPASANG (dibutuhkan untuk generator .docx)'}`);
        console.log(`Runtime python : ${st.runtimes.python.available ? `OK (${st.runtimes.python.version})` : 'BELUM TERPASANG (opsional untuk audit_humanizer.py)'}`);
        console.log('');
        for (const c of st.checks) {
          console.log(`  [${c.status.padEnd(9)}] ${c.agent}`);
        }
      }
      return st.checks.every(c => c.status === 'INSTALLED') ? 0 : 1;
    }

    if (opts.action === 'uninstall') {
      const res = uninstallSkill(opts);
      if (opts.json) {
        console.log(JSON.stringify(res, null, 2));
      } else {
        console.log(`[BERHASIL] Menghapus ${res.removed.length} berkas/direktori terkelola milik skill '${SKILL_NAME}'.`);
      }
      return 0;
    }

    const res = installSkill(opts);
    if (opts.json) {
      console.log(JSON.stringify(res, null, 2));
    } else {
      console.log(`[BERHASIL] 1 Skill Terpadu '${res.skill}' (v${res.version}) terpasang tanpa git clone!`);
      console.log(`- Lokasi skill : ${res.installedSkills.length} direktori agent (${res.installedSkills[0]?.filesCount || 0} berkas per bundel, mencakup mode-ilmiah, jurnal-sinta, humanizer-id UBSI, & skrip OpenXML)`);
      console.log(`- Slash command: ${res.installedCommands.length} berkas (/laporan-generator, /mode-ilmiah, /jurnal-sinta, /sinta-buat, /sinta-cek)`);
      console.log(`- Aturan scoped: ${res.installedRules.length} berkas (AGENTS.md & CLAUDE.md proyek Anda tidak disentuh)`);
      if (res.runtimes.uv.available) {
        console.log(`- Runtime uv   : OK (${res.runtimes.uv.version})`);
      } else {
        console.warn(
          '\n[PERHATIAN] Runtime `uv` belum terdeteksi di PATH.\n' +
          'Skill sudah terpasang, tetapi skrip pembuat Word (.docx) & verifikator DOI membutuhkan `uv`.\n' +
          'Pasang cepat (PowerShell): powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"\n' +
          'Pasang cepat (macOS/Linux): curl -LsSf https://astral.sh/uv/install.sh | sh'
        );
      }
    }
    return 0;
  } catch (err) {
    if (opts.json) {
      console.error(JSON.stringify({ error: err.message, code: err.code || 'INSTALL_ERROR' }, null, 2));
    } else {
      console.error(`[GAGAL] ${err.message}`);
    }
    return 1;
  }
}

module.exports = {
  SKILL_NAME,
  MANIFEST_FILE,
  COMMANDS,
  checkRuntimes,
  getStatus,
  installSkill,
  parseCliArgs,
  runCli,
  uninstallSkill,
};

if (require.main === module) {
  process.exit(runCli(process.argv.slice(2)));
}
