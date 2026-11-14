// The page loads classic scripts that share state through globals named Geo* and GEO_*.
// This check makes the dependency graph explicit: every global read while a script loads must be defined
// by an earlier script in index.html, every other read must be defined somewhere, and each global has one owner.
// Reads inside functions count as deferred, even when the function happens to run during loading.
import fs from 'node:fs';
import * as espree from 'espree';

const GENERATED = {
  'integrity.js': ['GEO_INTEGRITY'],
  'site-config.js': ['GEO_CONFIG'],
  'catalogue.js': ['GEO_CATALOG'],
  'space-shaders.js': ['GEO_SHADERS'],
  'experiments-data.js': ['GEO_LABS'],
  'narrative-data.js': ['GEO_NARRATIVE'],
  'research-data.js': ['GEO_RESEARCH'],
};
// Loaded on demand by app.js with SRI; never read while a script loads.
const ON_DEMAND = {
  'experiments-details.js': ['GEO_LABS_DETAILS'],
  'solution-data.js': ['GEO_SOLUTIONS'],
};
// assets/content/*.js add entries to window.GEO_MODULES, the cache that app.js creates.
const HOSTS = new Set(['root', 'window', 'globalThis', 'self']);
const NAME = /^(Geo|GEO_)[A-Za-z_]*$/;

const order = [...fs.readFileSync('src/index.html', 'utf8').matchAll(/<script defer src="assets\/([^"]+)"/g)].map(
  m => m[1],
);
const owner = new Map(),
  defined = new Set(),
  report = [],
  problems = [];
const own = (name, file) => {
  if (owner.has(name) && owner.get(name) !== file)
    problems.push(`${name} is defined by both ${owner.get(name)} and ${file}`);
  owner.set(name, file);
};
for (const [file, names] of Object.entries(ON_DEMAND)) names.forEach(n => own(n, file));

function analyse(file, source) {
  const ast = espree.parse(source, { ecmaVersion: 'latest', sourceType: 'script' });
  const defines = new Set(),
    loadReads = new Set(),
    laterReads = new Set();
  const wrapper = node =>
    node.type === 'ExpressionStatement' &&
    node.expression.type === 'CallExpression' &&
    /Function/.test(node.expression.callee.type);
  const global = node =>
    node?.type === 'MemberExpression' &&
    !node.computed &&
    node.object.type === 'Identifier' &&
    HOSTS.has(node.object.name) &&
    NAME.test(node.property.name)
      ? node.property.name
      : null;
  function walk(node, depth, assigned) {
    if (!node || typeof node.type !== 'string') return;
    if (/Function/.test(node.type) && !node.__wrapper) depth++;
    const name = global(node);
    if (name) (assigned ? defines : depth === 0 ? loadReads : laterReads).add(name);
    for (const [key, value] of Object.entries(node)) {
      if (key === 'parent' || !value || typeof value !== 'object') continue;
      const target = node.type === 'AssignmentExpression' && key === 'left';
      for (const child of Array.isArray(value) ? value : [value]) walk(child, depth, target);
    }
  }
  for (const statement of ast.body) {
    if (wrapper(statement)) statement.expression.callee.__wrapper = true;
    walk(statement, 0, false);
  }
  return { defines, loadReads, laterReads };
}

for (const file of order) {
  if (GENERATED[file]) {
    GENERATED[file].forEach(n => (own(n, file), defined.add(n)));
    report.push({ file, generated: true, defines: GENERATED[file] });
    continue;
  }
  const { defines, loadReads, laterReads } = analyse(file, fs.readFileSync('src/' + file, 'utf8'));
  for (const n of loadReads)
    if (!defined.has(n) && !defines.has(n))
      problems.push(`${file} reads ${n} while loading, before any script defines it`);
  defines.forEach(n => (own(n, file), defined.add(n)));
  report.push({
    file,
    defines: [...defines].sort(),
    readsWhileLoading: [...loadReads].sort(),
    readsLater: [...laterReads].sort(),
  });
}
for (const entry of report)
  for (const n of entry.readsLater || [])
    if (!owner.has(n)) problems.push(`${entry.file} reads ${n}, which no script defines`);

fs.writeFileSync(
  'qa/modules.json',
  JSON.stringify({ order, owners: Object.fromEntries(owner), scripts: report }, null, 2) + '\n',
);
if (problems.length) {
  console.error(problems.join('\n'));
  process.exit(1);
}
console.log(
  `Modules: ${order.length} scripts, ${owner.size} globals with one owner each; load order satisfies every load-time read.`,
);
