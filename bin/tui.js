/**
 * Zero-dependency terminal UI & 3D block-shadow banner for Laporan Generator CLI.
 *
 * Design invariants:
 * - Pure Node.js stdlib only (no external npm dependencies).
 * - Respects NO_COLOR / FORCE_COLOR and degrades cleanly on narrow (< 72 cols) or non-TTY pipes.
 * - Never prints banners in machine-readable modes (callers skip banner on --json / inspect).
 */

const ANSI_SHADOW_GLYPHS = {
  L: [
    '██╗    ',
    '██║    ',
    '██║    ',
    '██║    ',
    '██████╗',
    '╚═════╝',
  ],
  A: [
    ' █████╗ ',
    '██╔══██╗',
    '███████║',
    '██╔══██║',
    '██║  ██║',
    '╚═╝  ╚═╝',
  ],
  P: [
    '██████╗ ',
    '██╔══██╗',
    '██████╔╝',
    '██╔═══╝ ',
    '██║     ',
    '╚═╝     ',
  ],
  O: [
    ' █████╗ ',
    '██╔══██╗',
    '██║  ██║',
    '██║  ██║',
    '╚█████╔╝',
    ' ╚════╝ ',
  ],
  R: [
    '██████╗ ',
    '██╔══██╗',
    '██████╔╝',
    '██╔══██╗',
    '██║  ██║',
    '╚═╝  ╚═╝',
  ],
  N: [
    '██╗  ██╗',
    '███╗ ██║',
    '████╗██║',
    '██╔████║',
    '██║╚███║',
    '╚═╝ ╚══╝',
  ],
  G: [
    ' █████╗ ',
    '██╔═══╝ ',
    '██║ ███╗',
    '██║  ██║',
    '╚█████╔╝',
    ' ╚════╝ ',
  ],
  E: [
    '██████╗',
    '██╔═══╝',
    '█████╗ ',
    '██╔══╝ ',
    '██████╗',
    '╚═════╝',
  ],
  T: [
    '██████╗',
    '╚═██╔═╝',
    '  ██║  ',
    '  ██║  ',
    '  ██║  ',
    '  ╚═╝  ',
  ],
};

// Warm amber-to-ivory vertical gradient matching the website's Overstory palette (#f1b24a -> #f4f6f0)
const BANNER_ROW_RGB_TOP = [
  [244, 246, 240], // ivory highlight
  [247, 217, 148], // pale gold
  [241, 178, 74],  // project amber (--ovs-soft)
  [217, 130, 59],  // autumn leaf (--ovs-leaf2)
  [184, 96, 38],   // warm terracotta
  [136, 78, 42],   // bark shadow
];

const BANNER_ROW_RGB_BOTTOM = [
  [241, 178, 74],  // project amber
  [234, 158, 66],  // warm gold
  [217, 130, 59],  // autumn leaf
  [192, 102, 42],  // deep ochre
  [165, 69, 26],   // project accent (--ovs-accent)
  [118, 66, 38],   // shadow base
];

function supportsColor(stream = process.stdout) {
  if (process.env.NO_COLOR !== undefined && process.env.NO_COLOR !== '') return false;
  if (process.env.FORCE_COLOR && process.env.FORCE_COLOR !== '0') return true;
  return Boolean(stream && stream.isTTY);
}

function supportsTrueColor() {
  const ct = String(process.env.COLORTERM || '').toLowerCase();
  if (ct === 'truecolor' || ct === '24bit') return true;
  if (process.env.WT_SESSION || process.env.TERM_PROGRAM === 'vscode') return true;
  return false;
}

function supportsUnicode() {
  if (process.platform !== 'win32') return true;
  if (process.env.WT_SESSION || process.env.TERM_PROGRAM === 'vscode' || process.env.ConEmuTask) return true;
  const lang = `${process.env.LC_ALL || ''}${process.env.LC_CTYPE || ''}${process.env.LANG || ''}`;
  if (/utf-?8/i.test(lang)) return true;
  // Windows 10/11 Node.js stdout writes UTF-8 cleanly in modern terminals unless explicitly ASCII-only
  return process.env.TERM !== 'dumb';
}

function getTerminalColumns() {
  const envCols = Number.parseInt(process.env.COLUMNS || '', 10);
  if (Number.isFinite(envCols) && envCols > 0) return envCols;
  if (process.stdout && Number.isFinite(process.stdout.columns) && process.stdout.columns > 0) {
    return process.stdout.columns;
  }
  return 100;
}

function makeStyle() {
  const color = supportsColor();
  const trueColor = color && supportsTrueColor();
  const reset = '\x1b[0m';
  const wrap = (code, s) => (color ? `\x1b[${code}m${s}${reset}` : String(s));
  const rgb = (r, g, b, s) => {
    if (!color) return String(s);
    if (trueColor) return `\x1b[38;2;${r};${g};${b}m${s}${reset}`;
    return `\x1b[33m${s}${reset}`;
  };
  const bgBadge = (s) => {
    if (!color) return `[${s}]`;
    if (trueColor) return `\x1b[48;2;241;178;74m\x1b[38;2;16;21;13m\x1b[1m ${s} ${reset}`;
    return `\x1b[43m\x1b[30m\x1b[1m ${s} ${reset}`;
  };

  return {
    color,
    unicode: supportsUnicode(),
    bold: (s) => wrap('1', s),
    dim: (s) => wrap('2', s),
    amber: (s) => rgb(241, 178, 74, s),
    accent: (s) => rgb(217, 130, 59, s),
    green: (s) => (trueColor ? rgb(118, 214, 138, s) : wrap('32', s)),
    red: (s) => (trueColor ? rgb(235, 108, 92, s) : wrap('31', s)),
    muted: (s) => (trueColor ? rgb(148, 158, 146, s) : wrap('90', s)),
    ivory: (s) => (trueColor ? rgb(244, 246, 240, s) : wrap('97', s)),
    rgb,
    badge: bgBadge,
  };
}

function composeWord(word) {
  const chars = Array.from(word.toUpperCase()).filter((ch) => ANSI_SHADOW_GLYPHS[ch]);
  const rows = ['', '', '', '', '', ''];
  chars.forEach((ch, idx) => {
    const g = ANSI_SHADOW_GLYPHS[ch];
    const gap = idx > 0 ? ' ' : '';
    for (let r = 0; r < 6; r++) {
      rows[r] += gap + g[r];
    }
  });
  return rows;
}

function stripAnsi(str) {
  return String(str).replace(/\x1b\[[0-9;]*m/g, '');
}

function renderBanner({ version = '1.2.0', subtitle = 'Unified Academic Skill & OpenXML Engine' } = {}) {
  const st = makeStyle();
  const cols = getTerminalColumns();

  if (!st.unicode || cols < 80) {
    const bar = '+--------------------------------------------------+';
    return [
      '',
      st.amber(bar),
      st.amber('|') + '  ' + st.bold(st.ivory('LAPORAN GENERATOR')) + st.muted(` v${version}`.padEnd(31)) + st.amber('|'),
      st.amber('|') + '  ' + st.muted(subtitle.slice(0, 46).padEnd(46)) + '  ' + st.amber('|'),
      st.amber(bar),
      '',
    ].join('\n');
  }

  const line1 = composeWord('LAPORAN');
  const line2 = composeWord('GENERATOR');
  const out = [''];

  line1.forEach((row, idx) => {
    const [r, g, b] = BANNER_ROW_RGB_TOP[idx];
    out.push('  ' + st.rgb(r, g, b, row));
  });
  line2.forEach((row, idx) => {
    const [r, g, b] = BANNER_ROW_RGB_BOTTOM[idx];
    out.push('  ' + st.rgb(r, g, b, row));
  });

  out.push('');
  return out.join('\n');
}

function railChars(st) {
  if (st.unicode) {
    return {
      bar: '│',
      top: '┌',
      bottom: '└',
      diamond: '◇',
      dot: '●',
      check: '✓',
      cross: '■',
      warn: '▲',
      h: '─',
      tr: '╮',
      br: '╯',
      tl: '├',
    };
  }
  return {
    bar: '|',
    top: '+',
    bottom: '+',
    diamond: 'o',
    dot: '*',
    check: '[OK]',
    cross: '[X]',
    warn: '[!]',
    h: '-',
    tr: '+',
    br: '+',
    tl: '+',
  };
}

function printIntro(label, version = '') {
  const st = makeStyle();
  const c = railChars(st);
  const tag = version ? `${label} v${version}` : label;
  console.log(`${st.muted(c.top)}  ${st.badge(tag)}`);
  console.log(st.muted(c.bar));
}

function printStep(text, tone = 'info') {
  const st = makeStyle();
  const c = railChars(st);
  const glyph =
    tone === 'ok'
      ? st.green(c.check)
      : tone === 'warn'
        ? st.amber(c.warn)
        : tone === 'err'
          ? st.red(c.cross)
          : st.amber(c.diamond);
  console.log(`${glyph}  ${text}`);
  console.log(st.muted(c.bar));
}

function printBox(title, lines, tone = 'info') {
  const st = makeStyle();
  const c = railChars(st);
  const cols = getTerminalColumns();
  const maxContentWidth = Math.max(
    stripAnsi(title).length + 4,
    ...lines.map((l) => stripAnsi(l).length)
  );
  const innerWidth = Math.min(Math.max(44, maxContentWidth + 2), Math.max(44, cols - 8));
  const titleLen = stripAnsi(title).length;
  const topFill = Math.max(2, innerWidth - titleLen - 1);
  const borderColor = tone === 'warn' ? st.amber : tone === 'ok' ? st.green : st.muted;
  const leadGlyph = tone === 'warn' ? st.amber(c.warn) : tone === 'ok' ? st.green(c.diamond) : st.amber(c.diamond);

  console.log(`${leadGlyph}  ${st.bold(st.ivory(title))} ${borderColor(c.h.repeat(topFill) + c.tr)}`);
  console.log(`${borderColor(c.bar)}${' '.repeat(innerWidth + 2)}${borderColor(c.bar)}`);
  for (const rawLine of lines) {
    const plainLen = stripAnsi(rawLine).length;
    const pad = Math.max(0, innerWidth - plainLen);
    console.log(`${borderColor(c.bar)}  ${rawLine}${' '.repeat(pad)}${borderColor(c.bar)}`);
  }
  console.log(`${borderColor(c.bar)}${' '.repeat(innerWidth + 2)}${borderColor(c.bar)}`);
  console.log(`${borderColor(c.tl + c.h.repeat(innerWidth + 2) + c.br)}`);
  console.log(st.muted(c.bar));
}

function printOutro(text, tone = 'ok') {
  const st = makeStyle();
  const c = railChars(st);
  const msg = tone === 'err' ? st.red(text) : tone === 'warn' ? st.amber(text) : st.ivory(text);
  console.log(`${st.muted(c.bottom)}  ${msg}\n`);
}

module.exports = {
  composeWord,
  makeStyle,
  printBox,
  printIntro,
  printOutro,
  printStep,
  renderBanner,
  stripAnsi,
};
