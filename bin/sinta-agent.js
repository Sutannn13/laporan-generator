#!/usr/bin/env node

const { spawnSync } = require('child_process');
const path = require('path');
const { checkRuntimes, runCli } = require('./install-skill');
const tui = require('./tui');

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
  const st = tui.makeStyle();
  console.log(tui.renderBanner({ version: '1.2.0' }));
  tui.printIntro('sinta-agent', '1.2.0');
  tui.printStep('Universal AI Agent CLI: Antigravity, Claude Code, Cursor, OpenCode, Freebuff, KiloCode, & Roo');
  tui.printBox('Perintah (Tanpa git clone, kompatibel npm 12+)', [
    `${st.amber('npx skills add Sutannn13/laporan-generator')}`,
    `  ${st.muted('Pasang 1 skill terpadu via skills.sh')}`,
    `${st.ivory('npx -y --allow-git=all github:Sutannn13/laporan-generator install [--workspace [dir]]')}`,
    `  ${st.muted('Pasang 1 skill terpadu + 5 slash commands (pure Node, tanpa clone)')}`,
    `${st.ivory('npx -y --allow-git=all github:Sutannn13/laporan-generator status [--json]')}`,
    `  ${st.muted('Cek status pemasangan skill & kesiapan runtime uv/Python')}`,
    `${st.ivory('npx -y --allow-git=all github:Sutannn13/laporan-generator uninstall')}`,
    `  ${st.muted('Hapus berkas terkelola milik skill laporan-generator')}`,
    `${st.ivory('npx -y --allow-git=all -p github:Sutannn13/laporan-generator sinta-agent buat [opsi]')}`,
    `  ${st.muted('Jalankan generator Jurnal SINTA 1-6 (.docx)')}`,
    `${st.ivory('npx -y --allow-git=all -p github:Sutannn13/laporan-generator sinta-agent cek "<file.docx>"')}`,
    `  ${st.muted('Inspeksi DNA template .docx eksternal / draf existing')}`,
    `${st.ivory('npx -y --allow-git=all -p github:Sutannn13/laporan-generator sinta-agent showcase')}`,
    `  ${st.muted('Generate ulang contoh di folder contoh-template-ai/')}`,
  ]);
  tui.printBox('Slash Commands di dalam Chat AI Agent', [
    `${st.amber('/laporan-generator')}  ${st.muted('Pintu utama semua dokumen (PKL, Skripsi UBSI, Audit COBIT, Jurnal SINTA)')}`,
    `${st.amber('/mode-ilmiah')}        ${st.muted('Alur tim akademik 6 fase + rubrik Peer Reviewer >= 85/100')}`,
    `${st.amber('/jurnal-sinta')}       ${st.muted('Mode Jurnal SINTA 1-6 (1/2 kolom, DOI Crossref, patuh R1-R4 Mendeley)')}`,
    `${st.amber('/sinta-buat')}         ${st.muted('Generate cepat Word (.docx) mode Mendeley')}`,
    `${st.amber('/sinta-cek')}          ${st.muted('Inspeksi XML & audit Anti-Slop + Burstiness')}`,
  ]);
  tui.printOutro('Gunakan subperintah di atas untuk mulai bekerja tanpa git clone.');
}
