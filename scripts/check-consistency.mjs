import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { moduleGuides } from './update-module-guides.mjs';
import vm from 'node:vm';
import { solutionDocument } from './prepare-solution-documents.mjs';
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const catalogue = read('content/experiments.json'),
  activities = catalogue.activities;
assert.equal(catalogue.version, read('package.json').version, 'Application/catalogue version');
assert.equal(read('package-lock.json').packages[''].version, read('package.json').version, 'Root package lock version');
assert.equal(read('package-lock.json').version, read('package.json').version, 'Package lock version');
assert.deepEqual(read('content/experiments-draft.json'), activities, 'Native-check catalogue differs');
const ids = new Set(activities.map(a => a.id)),
  owners = new Map(),
  limits = new Set();
for (const file of fs.readdirSync('content').filter(f => /^prose-.*\.json$/.test(f))) {
  for (const [id, fields] of Object.entries(read('content/' + file))) {
    assert(ids.has(id), 'Orphan editorial activity: ' + id);
    assert(!owners.has(id), 'Duplicate editorial activity: ' + id);
    owners.set(id, file);
    const activity = activities.find(a => a.id === id);
    for (const [key, value] of Object.entries(fields))
      assert.deepEqual(activity[key], value, 'Editorial drift: ' + id + '.' + key);
  }
}
assert.equal(owners.size, activities.length, 'Missing editorial source');
for (const a of activities) {
  assert(a.limits.trim(), 'Empty limits: ' + a.id);
  assert(!a.limits.startsWith('I dati sono sintetici e il modello'), 'Generic limits: ' + a.id);
  assert(!limits.has(a.limits), 'Repeated limits: ' + a.id);
  limits.add(a.limits);
}
for (const [file, expected] of moduleGuides())
  assert.equal(fs.readFileSync(file, 'utf8'), expected, 'Module guide drift: ' + file);
const { archiveMembersCompared: members } = JSON.parse(
  execFileSync('python3', ['scripts/labs/package-downloads.py', '--check'], { encoding: 'utf8' }),
);
const originalGuides = read('content/course-solutions.json'),
  preparedGuides = read('content/course-solutions-prepared.json');
assert.deepEqual(Object.keys(originalGuides), Object.keys(preparedGuides), 'Course solution membership');
for (const [id, g] of Object.entries(preparedGuides)) {
  const { code, stages, ...fields } = g;
  assert.deepEqual(
    { ...fields, stages: stages.map(({ code: _code, ...s }) => s) },
    originalGuides[id],
    'Prepared course guide drift: ' + id,
  );
  assert(code && stages.every(s => s.code), 'Missing course program: ' + id);
  let next = 1;
  for (const stage of stages) {
    assert.equal(stage.fromLine, next);
    assert(stage.toLine >= next);
    next = stage.toLine + 1;
  }
  assert.equal(
    next,
    fs
      .readFileSync('materiali/R/' + id + '_figure.R', 'utf8')
      .trimEnd()
      .split('\n').length + 1,
    'Source coverage: ' + id,
  );
}
const guides = read('content/solution-guides-research.json');
const scope = { GEO_LABS: { common: fs.readFileSync('R/lab-common.R', 'utf8') } };
for (const file of ['html', 'code-terminal', 'research-projects'])
  vm.runInNewContext(fs.readFileSync('src/' + file + '.js', 'utf8'), scope);
for (const [id, g] of Object.entries(guides)) {
  const a = read('content/research-' + id + '.json'),
    base = 'assets/research/' + id + '/';
  assert.equal(fs.readFileSync(base + 'SOLUZIONE.txt', 'utf8'), solutionDocument(a, g), 'Download guide drift: ' + id);
  assert.equal(
    fs.readFileSync(base + id + '.R', 'utf8'),
    scope.GeoResearch.script(a, Object.fromEntries(a.controls.map(c => [c.key, c.value]))),
    'Download R drift: ' + id,
  );
}
const researchMembers = Number(
  execFileSync(
    'python3',
    [
      '-c',
      `import pathlib,zipfile
count=0
for p in sorted(pathlib.Path('assets/research').iterdir()):
 if not p.is_dir(): continue
 files={f.relative_to(p).as_posix():f for f in p.rglob('*') if f.is_file() and f.name!='project.zip'}
 with zipfile.ZipFile(p/'project.zip') as z:
  assert len(z.namelist())==len(set(z.namelist())), f'Duplicate entries: {p}'
  assert set(z.namelist())==set(files), f'Archive membership: {p}'
  for name,f in files.items():
   assert z.read(name)==f.read_bytes(), f'Archive drift: {p}/{name}'
   count+=1
print(count)`,
    ],
    { encoding: 'utf8' },
  ).trim(),
);
const docs = [
  ...fs.readdirSync('.').filter(f => f.endsWith('.md')),
  ...fs
    .readdirSync('docs')
    .filter(f => f.endsWith('.md'))
    .map(f => 'docs/' + f),
  ...read('content/catalogue.json').modules.map(m => 'moduli/' + m.id + '/README.md'),
];
for (const file of docs)
  for (const [, link] of fs.readFileSync(file, 'utf8').matchAll(/\]\(([^)]+)\)/g)) {
    if (link.includes('://') || link.startsWith('#')) continue;
    assert(
      fs.existsSync(path.resolve(path.dirname(file), link.split('#')[0])),
      'Broken documentation link: ' + file + ' → ' + link,
    );
  }
assert(!fs.existsSync('scripts/labs/prepare-browser-qa.py'), 'Obsolete browser preparer');
assert(
  !/function (?:modulePage|orbitalLabel|expeditionLinks)\b/.test(fs.readFileSync('src/app.js', 'utf8')),
  'Obsolete page implementation',
);
const report = {
  version: read('package.json').version,
  status: 'passed',
  activities: activities.length,
  specificLimits: limits.size,
  moduleGuides: 28,
  documents: docs.length,
  archiveMembersCompared: members,
  researchArchiveMembersCompared: researchMembers,
  courseSolutions: Object.keys(preparedGuides).length,
  researchSolutions: Object.keys(guides).length,
  checks: [
    'derived-counts',
    'editorial-single-owner',
    'generated-catalogue',
    'module-guides',
    'download-membership-and-bytes',
    'section-csv',
    'documentation-links',
    'obsolete-code-removal',
    'prepared-course-guides',
    'downloaded-solution-guides',
    'downloaded-research-programs',
    'research-archive-membership-and-bytes',
  ],
};
// Counts shown on the site are derived at build time; sources must not repeat them as literals.
{
  const astro = {};
  vm.createContext(astro);
  for (const f of ['planets', 'planet-families', 'astro-model'])
    vm.runInContext(fs.readFileSync('src/' + f + '.js', 'utf8'), astro);
  const n = {
    experiments: activities.length,
    systems: astro.GeoAstro.systems.length,
    worlds: astro.GeoAstro.systems.reduce((t, x) => t + x.planets.length, 0),
    missions: read('content/catalogue.json').modules.filter(m => m.category === 'progetti').length,
  };
  for (const file of [
    'src/index.html',
    ...fs
      .readdirSync('src')
      .filter(f => f.endsWith('.js'))
      .map(f => 'src/' + f),
  ]) {
    const hit = fs
      .readFileSync(file, 'utf8')
      .match(/\b\d+ (?:esperimenti|sistemi|spedizioni|pianeti|esplorazioni|programmi R)\b/i);
    assert(!hit, 'Hard-coded count in ' + file + ': ' + hit?.[0] + ' (derive it from the data)');
  }
  const html = fs.readFileSync('dist/index.html', 'utf8');
  assert(!/\{\{[A-Z_]+\}\}/.test(html), 'Unresolved placeholder in dist/index.html');
  for (const text of [
    n.experiments + ' esperimenti',
    n.systems + ' sistemi',
    n.missions + ' spedizioni',
    n.worlds + ' pianeti',
  ])
    assert(html.includes(text), 'dist/index.html lacks derived count: ' + text);
  const readme = fs.readFileSync('README.md', 'utf8');
  for (const [re, v, label] of [
    [/\b(\d+) esperimenti\b/g, n.experiments, 'experiments'],
    [/\b(\d+) spedizioni\b/g, n.missions, 'missions'],
    [/\b(\d+) sistemi\b/g, n.systems, 'systems'],
  ])
    for (const m of readme.matchAll(re)) assert.equal(+m[1], v, 'README ' + label + ' count');
}
fs.writeFileSync('qa/consistency.json', JSON.stringify(report, null, 2) + '\n');
console.log(
  'Consistency: ' +
    activities.length +
    ' activities, 28 guides, ' +
    members +
    ' archived source files and ' +
    docs.length +
    ' documents verified.',
);
