#!/usr/bin/env node

const { spawnSync } = require('child_process');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const sub = (args[0] || 'help').toLowerCase();
const rest = args.slice(1);

function runUv(scriptRelPath, scriptArgs = []) {
  const scriptAbs = path.join(ROOT_DIR, scriptRelPath);
  const res = spawnSync('uv', ['run', scriptAbs, ...scriptArgs], {
    cwd: ROOT_DIR,
    stdio: 'inherit',
    shell: process.platform === 'win32',
  });
  process.exit(res.status || 0);
}

if (sub === 'install' || sub === 'setup') {
  runUv('scripts/install_agent_skills.py', rest);
} else if (sub === 'status') {
  runUv('scripts/install_agent_skills.py', ['--status', ...rest]);
} else if (sub === 'buat' || sub === 'generate') {
  runUv('generate_sinta_journal_docx.py', rest);
} else if (sub === 'cek' || sub === 'inspect') {
  if (!rest[0]) {
    console.error('Gunakan: npx sinta-agent cek "<nama_file.docx>"');
    process.exit(1);
  }
  runUv('generate_sinta_journal_docx.py', ['--inspect-docx', ...rest]);
} else if (sub === 'showcase') {
  runUv('generate_sinta_journal_docx.py', ['--generate-showcase', rest[0] || 'contoh-template-ai']);
} else {
  console.log(`SINTA 1-6 & Laporan PKL Universal AI Agent CLI (sinta-agent)
Mendukung: Antigravity, KiloCode, OpenCode, Freebuff/Codebuff, Claude Code, Cursor, Windsurf, Cline, & Roo Code

Perintah:
  npx sinta-agent install [--target <folder>]  Pasang Skill & Slash Commands (/jurnal-sinta, /sinta-buat, /sinta-cek) ke semua AI Agent & CLI
  npx sinta-agent status                       Cek status instalasi di seluruh AI Agent (Workspace & Global)
  npx sinta-agent buat [opsi]                  Jalankan generator Jurnal SINTA 1-6 (.docx)
  npx sinta-agent cek "<file.docx>"            Inspeksi DNA template .docx dari jurnal kampus lain / draf existing
  npx sinta-agent showcase                     Generate ulang 12 contoh di folder contoh-template-ai/

Slash Commands di dalam Chat AI Agent (KiloCode / OpenCode / Freebuff / Antigravity / Claude):
  /jurnal-sinta   Mode interaktif pembuatan Jurnal SINTA 1-6 baru atau pengerjaan dokumen existing
  /sinta-buat     Generate cepat file Word (.docx) Jurnal SINTA 1-6
  /sinta-cek      Inspeksi template .docx eksternal & verifikasi kualitas SINTA
`);
}
