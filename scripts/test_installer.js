/**
 * Contract & Isolated Integration Tests for the Unified 1-Skill Bundle & Zero-Clone Installer.
 *
 * Covers:
 * 1. Single-skill bundle contract (exactly 1 SKILL.md under .agents/skills/, valid links,
 *    zero personal paths, zero em-dashes, lean runtime size < 3.5 MB).
 * 2. Fresh zero-clone global install in isolated temp HOME + clean cwd.
 * 3. Idempotent re-install (2x consecutive runs produce identical state, zero temp dirs left).
 * 4. Non-destructive workspace install (pre-existing AGENTS.md, CLAUDE.md, .windsurfrules,
 *    .github/copilot-instructions.md remain byte-for-byte untouched).
 * 5. Fail-fast missing-uv behavior (--require-uv and sinta-agent buat exit non-zero with guidance).
 * 6. Clean uninstall + status verification.
 * 7. Backward-compatible scaffold flag precedence (e.g., `cli.js install --type proposal --yes`).
 */

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const CLI_JS = path.join(REPO_ROOT, 'bin', 'cli.js');
const SINTA_AGENT_JS = path.join(REPO_ROOT, 'bin', 'sinta-agent.js');
const SKILLS_ROOT = path.join(REPO_ROOT, '.agents', 'skills');
const HUB_DIR = path.join(SKILLS_ROOT, 'laporan-generator');

function walkFiles(dir, out = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walkFiles(p, out);
    else if (ent.isFile()) out.push(p);
  }
  return out;
}

function runNode(scriptPath, args, opts = {}) {
  return spawnSync(process.execPath, [scriptPath, ...args], {
    encoding: 'utf8',
    cwd: opts.cwd || REPO_ROOT,
    env: opts.env || process.env,
  });
}

function testBundleContract() {
  // 1. Exactly 1 skill folder and 1 SKILL.md under .agents/skills/
  const topEntries = fs.readdirSync(SKILLS_ROOT, { withFileTypes: true }).filter(e => e.isDirectory());
  assert.deepStrictEqual(
    topEntries.map(e => e.name),
    ['laporan-generator'],
    `Expected exactly 1 skill folder under .agents/skills/, found: ${topEntries.map(e => e.name).join(', ')}`
  );

  const allFiles = walkFiles(SKILLS_ROOT);
  const skillMdFiles = allFiles.filter(f => path.basename(f).toLowerCase() === 'skill.md');
  assert.strictEqual(
    skillMdFiles.length,
    1,
    `Expected exactly 1 SKILL.md under .agents/skills/ for npx skills add, found ${skillMdFiles.length}: ${skillMdFiles.join(', ')}`
  );

  // 2. Lean runtime size (< 3.5 MB) and zero bloat / __pycache__ / examples
  const totalBytes = allFiles.reduce((acc, f) => acc + fs.statSync(f).size, 0);
  const totalMB = totalBytes / (1024 * 1024);
  assert.ok(totalMB < 3.5, `Unified skill bundle too large (${totalMB.toFixed(2)} MB >= 3.5 MB)`);
  assert.ok(!allFiles.some(f => f.includes('__pycache__') || f.endsWith('.pyc')), 'Found __pycache__/.pyc inside skill bundle');
  assert.ok(!fs.existsSync(path.join(HUB_DIR, 'examples')), 'Found legacy examples/ bloat inside skill bundle');

  // 3. Valid frontmatter, relative reference links, zero em-dashes, and zero personal machine paths
  const skillMdText = fs.readFileSync(skillMdFiles[0], 'utf8');
  assert.ok(/^---\r?\nname:\s*laporan-generator\b/m.test(skillMdText), 'SKILL.md missing valid name: laporan-generator frontmatter');

  const refMatches = [...skillMdText.matchAll(/\(references\/([^)]+\.md)\)/g)];
  assert.ok(refMatches.length >= 4, 'SKILL.md should route to at least 4 reference guides');
  for (const m of refMatches) {
    const refPath = path.join(HUB_DIR, 'references', m[1]);
    assert.ok(fs.existsSync(refPath), `Broken reference link in SKILL.md: references/${m[1]}`);
  }

  const mdFiles = [
    ...allFiles.filter(f => f.endsWith('.md')),
    path.join(REPO_ROOT, '.agents', 'rules', 'sinta-journal-prompt.md'),
  ];
  for (const mf of mdFiles) {
    const content = fs.readFileSync(mf, 'utf8');
    assert.ok(!content.includes('\u2014'), `Forbidden em-dash found in ${mf}`);
    assert.ok(!/Sutan\s+Arlie\s+Johan|Sutan%20Arlie%20Johan|DATA%20SUTAN|DATA\s+SUTAN/i.test(content), `Hardcoded personal path found in ${mf}`);
  }

  console.log(`PASS: Bundle Contract (1 SKILL.md, ${allFiles.length} files, ${totalMB.toFixed(2)} MB, 0 personal paths, 0 em-dashes)`);
}

function testZeroCloneInstaller() {
  const tmpBase = fs.mkdtempSync(path.join(os.tmpdir(), 'lg-installer-test-'));
  const tmpHome = path.join(tmpBase, 'home');
  const tmpCwd = path.join(tmpBase, 'empty-cwd');
  const tmpProject = path.join(tmpBase, 'user-project');
  fs.mkdirSync(tmpHome, { recursive: true });
  fs.mkdirSync(tmpCwd, { recursive: true });
  fs.mkdirSync(tmpProject, { recursive: true });

  try {
    // 1. Fresh zero-clone global install from an empty cwd
    const r1 = runNode(CLI_JS, ['install', '--home', tmpHome, '--json'], { cwd: tmpCwd });
    assert.strictEqual(r1.status, 0, `Fresh install failed:\n${r1.stdout}\n${r1.stderr}`);
    const payload1 = JSON.parse(r1.stdout);
    assert.strictEqual(payload1.skill, 'laporan-generator');
    assert.ok(payload1.installedSkills.length >= 5, 'Expected >= 5 global agent skill targets');
    assert.deepStrictEqual(fs.readdirSync(tmpCwd), [], 'Global zero-clone install must not write any files into user cwd');

    const globalSkillDir = path.join(tmpHome, '.gemini', 'config', 'skills', 'laporan-generator');
    assert.ok(fs.existsSync(path.join(globalSkillDir, 'SKILL.md')));
    assert.ok(fs.existsSync(path.join(globalSkillDir, 'references', 'mode-ilmiah.md')));
    assert.ok(fs.existsSync(path.join(globalSkillDir, 'references', 'jurnal-sinta.md')));
    assert.ok(fs.existsSync(path.join(globalSkillDir, 'references', 'humanizer-id.md')));
    assert.ok(fs.existsSync(path.join(globalSkillDir, 'presets', 'sinta-catalog.json.gz')));
    assert.ok(fs.existsSync(path.join(globalSkillDir, 'scripts', 'audit_humanizer.py')));
    assert.ok(fs.existsSync(path.join(globalSkillDir, 'template', 'gambar', 'logo-ubsi.png')));

    // 2. Status check passes (exit 0)
    const st1 = runNode(CLI_JS, ['status', '--home', tmpHome, '--json'], { cwd: tmpCwd });
    assert.strictEqual(st1.status, 0, `Status check failed:\n${st1.stdout}\n${st1.stderr}`);
    const stJson = JSON.parse(st1.stdout);
    assert.ok(stJson.checks.every(c => c.status === 'INSTALLED'), `Expected all checks INSTALLED: ${st1.stdout}`);

    // 3. Idempotency: second install produces identical file count & zero staging dirs left
    const r2 = runNode(CLI_JS, ['install', '--home', tmpHome, '--json'], { cwd: tmpCwd });
    assert.strictEqual(r2.status, 0, `Idempotent re-install failed:\n${r2.stdout}\n${r2.stderr}`);
    const payload2 = JSON.parse(r2.stdout);
    assert.strictEqual(payload2.installedSkills[0].filesCount, payload1.installedSkills[0].filesCount);
    const parentEntries = fs.readdirSync(path.dirname(globalSkillDir));
    assert.ok(!parentEntries.some(n => n.includes('.tmp-')), `Staging temp dir leaked: ${parentEntries.join(', ')}`);

    // 4. Non-destructive workspace install: pre-existing user docs MUST NOT be overwritten
    const protectedFiles = {
      'AGENTS.md': '# User Custom AGENTS\nDo not touch.\n',
      'CLAUDE.md': '# User Custom CLAUDE\nDo not touch.\n',
      '.windsurfrules': 'user-windsurf-rules\n',
      [path.join('.github', 'copilot-instructions.md')]: 'user-copilot-rules\n',
    };
    for (const [rel, body] of Object.entries(protectedFiles)) {
      const p = path.join(tmpProject, rel);
      fs.mkdirSync(path.dirname(p), { recursive: true });
      fs.writeFileSync(p, body, 'utf8');
    }

    const rWs = runNode(CLI_JS, ['install', '--home', tmpHome, '--workspace', tmpProject, '--json'], { cwd: tmpProject });
    assert.strictEqual(rWs.status, 0, `Workspace install failed:\n${rWs.stdout}\n${rWs.stderr}`);
    for (const [rel, body] of Object.entries(protectedFiles)) {
      const actual = fs.readFileSync(path.join(tmpProject, rel), 'utf8');
      assert.strictEqual(actual, body, `Installer destructively modified user-owned ${rel}!`);
    }
    assert.ok(fs.existsSync(path.join(tmpProject, '.agents', 'skills', 'laporan-generator', 'SKILL.md')));
    assert.ok(fs.existsSync(path.join(tmpProject, '.cursor', 'rules', 'laporan-generator.mdc')));

    // 5. Fail-fast missing-uv checks (empty PATH containing only Node binary directory)
    const strippedEnv = { ...process.env, PATH: path.dirname(process.execPath), Path: path.dirname(process.execPath) };
    const rNoUv = runNode(CLI_JS, ['install', '--home', tmpHome, '--require-uv'], { cwd: tmpCwd, env: strippedEnv });
    assert.notStrictEqual(rNoUv.status, 0, 'Expected --require-uv to fail with non-zero exit when uv is absent');
    assert.ok(/uv/i.test(rNoUv.stderr + rNoUv.stdout), 'Expected actionable uv installation hint on stderr');

    const rAgentNoUv = runNode(SINTA_AGENT_JS, ['buat', '--help'], { cwd: tmpCwd, env: strippedEnv });
    assert.notStrictEqual(rAgentNoUv.status, 0, 'Expected sinta-agent buat to fail non-zero (not fake 0) when uv is absent');
    assert.ok(/uv/i.test(rAgentNoUv.stderr + rAgentNoUv.stdout), 'Expected actionable uv error from sinta-agent');

    // 6. Clean uninstall removes managed files while leaving user AGENTS.md intact
    const rUn = runNode(CLI_JS, ['uninstall', '--home', tmpHome, '--workspace', tmpProject, '--json'], { cwd: tmpCwd });
    assert.strictEqual(rUn.status, 0, `Uninstall failed:\n${rUn.stdout}\n${rUn.stderr}`);
    assert.ok(!fs.existsSync(globalSkillDir), 'Global skill directory was not removed on uninstall');
    assert.ok(!fs.existsSync(path.join(tmpProject, '.agents', 'skills', 'laporan-generator')), 'Workspace skill dir not removed');
    assert.strictEqual(fs.readFileSync(path.join(tmpProject, 'AGENTS.md'), 'utf8'), protectedFiles['AGENTS.md']);

    const stAfter = runNode(CLI_JS, ['status', '--home', tmpHome, '--json'], { cwd: tmpCwd });
    assert.strictEqual(stAfter.status, 1, 'Expected status exit code 1 after uninstall');

    // 7. Backward-compatible scaffold precedence when --type flag is present
    const rScaffold = runNode(CLI_JS, ['install', '--type', 'proposal', '--yes'], { cwd: tmpCwd });
    assert.strictEqual(rScaffold.status, 0, `Backward-compat scaffold failed:\n${rScaffold.stdout}\n${rScaffold.stderr}`);
    assert.ok(fs.existsSync(path.join(tmpCwd, 'install', 'main.typ')), 'Expected --type flag to scaffold Typst project into ./install');

    console.log('PASS: Zero-Clone Installer (fresh, status, idempotent, non-destructive, missing-uv fail-fast, uninstall, scaffold compat)');
  } finally {
    fs.rmSync(tmpBase, { recursive: true, force: true });
  }
}

testBundleContract();
testZeroCloneInstaller();
