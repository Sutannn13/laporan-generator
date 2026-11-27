#!/usr/bin/env node

const { spawnSync } = require('child_process');
const path = require('path');
const { checkRuntimes, runCli } = require('./install-skill');

const ROOT_DIR = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const sub = (args[0] || 'help').toLowerCase();
const rest = args.slice(1);

function runUv(scriptRelPath, scriptArgs = []) {
  const runtimes = checkRuntimes();
  if (!runtimes.uv.available) {
    console.error(
      '[GAGAL] Runtime `uv` tidak ditemukan di PATH.\n' +
      'Pasang `uv` terlebih dahulu agar generator Word (.docx) dapat berjalan:\n' +
      '  Windows (PowerShell): powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"\n' +
      '  macOS / Linux       : curl -LsSf https://astral.sh/uv/install.sh | sh'
    );
    process.exit(1);
  }

  const scriptAbs = path.join(ROOT_DIR, scriptRelPath);
  const res = spawnSync('uv', ['run', scriptAbs, ...scriptArgs], {
    cwd: process.cwd(),
    stdio: 'inherit',
    shell: false,
  });
  if (res.error) {
    console.error(`[GAGAL] Tidak dapat menjalankan uv: ${res.error.message}`);
    process.exit(1);
  }
  process.exit(typeof res.status === 'number' ? res.status : 1);
}

if (sub === 'install' || sub === 'setup' || sub === 'status' || sub === 'uninstall' || sub === 'remove') {
  process.exit(runCli([sub, ...rest]));
} else if (sub === 'buat' || sub === 'generate') {
  runUv('generate_sinta_journal_docx.py', rest);
} else if (sub === 'cek' || sub === 'inspect') {
  if (!rest[0]) {
    console.error('Gunakan: npx -y --allow-git=all -p github:Sutannn13/laporan-generator sinta-agent cek "<nama_file.docx>"');
    process.exit(1);
  }
  runUv('generate_sinta_journal_docx.py', ['--inspect-docx', ...rest]);
} else if (sub === 'showcase') {
  runUv('generate_sinta_journal_docx.py', ['--generate-showcase', rest[0] || 'contoh-template-ai']);
} else {
  console.log(`Laporan Generator & SINTA 1-6 Universal AI Agent CLI (sinta-agent)
Mendukung: Antigravity, Claude Code, Cursor, OpenCode, Freebuff, KiloCode, Windsurf, Cline, & Roo Code

Perintah (Tanpa git clone, kompatibel npm 12+):
  npx skills add Sutannn13/laporan-generator
      Pasang 1 skill terpadu via skills.sh
  npx -y --allow-git=all github:Sutannn13/laporan-generator install [--workspace [dir]]
      Pasang 1 skill terpadu + slash commands (pure Node, tanpa clone)
  npx -y --allow-git=all github:Sutannn13/laporan-generator status [--json]
      Cek status pemasangan skill & kesiapan runtime uv/Python
  npx -y --allow-git=all github:Sutannn13/laporan-generator uninstall
      Hapus berkas terkelola milik skill laporan-generator
  npx -y --allow-git=all -p github:Sutannn13/laporan-generator sinta-agent buat [opsi]
      Jalankan generator Jurnal SINTA 1-6 (.docx)
  npx -y --allow-git=all -p github:Sutannn13/laporan-generator sinta-agent cek "<file.docx>"
      Inspeksi DNA template .docx eksternal / draf existing
  npx -y --allow-git=all -p github:Sutannn13/laporan-generator sinta-agent showcase
      Generate ulang contoh di folder contoh-template-ai/

Slash Commands di dalam Chat AI Agent:
  /laporan-generator   Pintu utama semua dokumen (PKL, Skripsi UBSI, Audit COBIT, Jurnal SINTA)
  /mode-ilmiah         Alur tim akademik 6 fase + rubrik Peer Reviewer >= 85/100
  /jurnal-sinta        Mode Jurnal SINTA 1-6 (1/2 kolom, DOI Crossref, patuh R1-R4 Mendeley)
  /sinta-buat          Generate cepat Word (.docx) mode Mendeley
  /sinta-cek           Inspeksi XML & audit Anti-Slop + Burstiness
`);
}
