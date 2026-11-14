import fs from 'node:fs';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import vm from 'node:vm';
import { hardenBuild } from './harden-build.mjs';
import { compactCourseSVG } from './compact-course-svg.mjs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'),
  out = path.join(root, 'dist');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const config = read('config/site.json'),
  catalogue = read('content/catalogue.json');
if (process.env.SITE_URL) config.siteUrl = process.env.SITE_URL.replace(/\/+$/, '') + '/';
if (process.env.GITHUB_REPOSITORY) config.repositoryUrl = 'https://github.com/' + process.env.GITHUB_REPOSITORY;
for (const key of ['siteUrl', 'mainSiteUrl', 'repositoryUrl']) {
  if (config[key]) {
    let u;
    try {
      u = new URL(config[key]);
    } catch {
      throw Error('URL non valido: ' + key);
    }
    // eslint-disable-next-line no-control-regex -- control characters are exactly what this check rejects
    if (u.protocol !== 'https:' || !u.hostname || u.username || u.password || /[\s\x00-\x1f]/.test(config[key]))
      throw Error('URL HTTPS non valido: ' + key);
  }
}
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(path.join(out, 'assets/content'), { recursive: true });
const sharedDiagramPanels = new Set();
for (const m of catalogue.modules)
  for (const s of read('moduli/' + m.id + '/modulo.json').slides)
    if (s.diagram && !s.figure)
      sharedDiagramPanels.add('visuals/' + m.id + '/' + String(s.page).padStart(3, '0') + '.svg');
for (const dir of ['assets', 'vendor', 'R'])
  fs.cpSync(path.join(root, dir), path.join(out, dir), {
    recursive: true,
    filter: p => {
      if (p !== path.join(root, dir) && path.basename(p).startsWith('.')) return false;
      if (fs.lstatSync(p).isSymbolicLink())
        throw Error('Collegamento simbolico non consentito nella distribuzione: ' + p);
      if (/\.(?:key|p12|pfx)$/i.test(p)) return false;
      if (p.split(path.sep).includes('__pycache__')) return false;
      if (dir === 'assets' && sharedDiagramPanels.has(path.relative(path.join(root, dir), p).split(path.sep).join('/')))
        return false;
      // Original provider responses remain available inside each downloadable project.zip.
      // The runtime reads only data.csv; avoid publishing a second uncompressed copy.
      if (
        dir === 'assets' &&
        /^research\/[^/]+\/(?:raw-[^/]+|source\.(?:csv|json))$/.test(
          path.relative(path.join(root, dir), p).split(path.sep).join('/'),
        )
      )
        return false;

      return true;
    },
  });
execFileSync('python3', [path.join(root, 'scripts/public_materials.py'), '--output', path.join(out, 'materiali')], {
  stdio: 'inherit',
});
const experiments = read('content/experiments.json');
experiments.common = fs.readFileSync(path.join(root, 'R/lab-common.R'), 'utf8');
experiments.packages = read('vendor/r-packages-lock.json');
for (const a of experiments.activities) {
  a.plotCount = fs
    .readdirSync(path.join(root, 'assets/experiments'))
    .filter(f => f.startsWith(a.id + '-') && f.endsWith('.svg')).length;
  if (!a.plotCount) throw Error('Anteprima R assente: ' + a.id);
}
const research = fs
  .readdirSync(path.join(root, 'content'))
  .filter(f => /^research-.*\.json$/.test(f))
  .map(f => read('content/' + f))
  .sort((a, b) => a.level - b.level);
for (const p of research) {
  const directory = path.join(root, 'assets/research', p.id),
    provenance = read('assets/research/' + p.id + '/provenance.json');
  p.dataSHA256 = crypto
    .createHash('sha256')
    .update(fs.readFileSync(path.join(directory, 'data.csv')))
    .digest('hex');
  p.rows = provenance.rows;
  p.retrievedAt = provenance.retrievedAt.slice(0, 10);
  p.plotCount = fs.readdirSync(directory).filter(f => /^figure-\d+\.svg$/.test(f)).length;
  if (!p.plotCount) throw Error('Figure R mancanti: ' + p.id);
}
const safe = x => JSON.stringify(x).replace(/</g, '\\u003c');
fs.writeFileSync(path.join(out, 'assets/research-data.js'), 'window.GEO_RESEARCH=' + safe(research) + ';\n');
fs.writeFileSync(
  path.join(out, 'assets/solution-data.js'),
  'window.GEO_SOLUTIONS=' +
    safe({
      research: read('content/solution-guides-research.json'),
      course: read('content/course-solutions-prepared.json'),
    }) +
    ';\n',
);
fs.writeFileSync(
  path.join(out, 'assets/narrative-data.js'),
  'window.GEO_NARRATIVE=' +
    safe({ ...read('content/narrative.json'), activities: read('content/narrative-m05.json') }) +
    ';\n',
);
// The index keeps what catalogue, search and routing read; the heavy fields load with the lab views.
const LAB_DETAIL_FIELDS = ['prose', 'controls', 'limits', 'code', 'symbols', 'conclusion'];
const details = { activities: {}, common: experiments.common, packages: experiments.packages };
for (const a of experiments.activities) {
  details.activities[a.id] = {};
  for (const k of LAB_DETAIL_FIELDS)
    if (k in a) {
      details.activities[a.id][k] = a[k];
      delete a[k];
    }
}
const labCount = experiments.activities.length;
delete experiments.common;
delete experiments.packages;
fs.writeFileSync(path.join(out, 'assets/experiments-data.js'), 'window.GEO_LABS=' + safe(experiments) + ';\n');
fs.writeFileSync(
  path.join(out, 'assets/experiments-details.js'),
  'window.GEO_LABS_DETAILS=' +
    safe(details) +
    ';\n(function(L,D){if(!L||!D)return;for(const a of L.activities)Object.assign(a,D.activities[a.id]);L.common=D.common;L.packages=D.packages;L.detailed=true;})(window.GEO_LABS,window.GEO_LABS_DETAILS);\n',
);
fs.writeFileSync(path.join(out, 'assets/catalogue.js'), 'window.GEO_CATALOG=' + safe(catalogue) + ';\n');
fs.writeFileSync(path.join(out, 'assets/site-config.js'), 'window.GEO_CONFIG=' + safe(config) + ';\n');
for (const m of catalogue.modules) {
  const data = read('moduli/' + m.id + '/modulo.json');
  for (const slide of data.slides) delete slide.review;
  fs.writeFileSync(
    path.join(out, 'assets/content', m.id + '.js'),
    'window.GEO_MODULES=window.GEO_MODULES||{};window.GEO_MODULES.' + m.id + '=' + safe(data) + ';\n',
  );
}
for (const name of [
  'html.js',
  'static.css',
  'app.js',
  'security.js',
  'core.js',
  'lab.css',
  'planets.js',
  'space.js',
  'space-cpu.js',
  'space.css',
  'experiments.js',
  'experiments.css',
  'lab-engine.js',
  'astro-model.js',
  'system-scene.js',
  'galaxy-model.js',
  'galaxy-scene.js',
  'galaxy.js',
  'galaxy.css',
  'narrative.js',
  'narrative.css',
  'cosmos.js',
  'cosmos-worker.js',
  'code-terminal.js',
  'code-terminal.css',
  'solution-terminal.js',
  'solution-terminal.css',
  'learning-paths.js',
  'learning-paths.css',
  'explorations.js',
  'planet-families.js',
  'research-projects.js',
  'research-projects.css',
])
  fs.copyFileSync(path.join(root, 'src', name), path.join(out, 'assets', name));
fs.writeFileSync(
  path.join(out, 'assets/space-shaders.js'),
  'window.GEO_SHADERS=' + safe({ planet: fs.readFileSync(path.join(root, 'src/planet.frag'), 'utf8') }) + ';\n',
);
const esc = s => s.replace(/[&"<>]/g, c => ({ '&': '&amp;', '"': '&quot;', '<': '&lt;', '>': '&gt;' })[c]);
const astro = {};
vm.createContext(astro);
for (const f of ['planets', 'planet-families', 'astro-model'])
  vm.runInContext(fs.readFileSync(path.join(root, 'src', f + '.js'), 'utf8'), astro);
const counts = {
  experiments: labCount,
  systems: astro.GeoAstro.systems.length,
  worlds: astro.GeoAstro.systems.reduce((n, s) => n + s.planets.length, 0),
  missions: catalogue.modules.filter(m => m.category === 'progetti').length,
};
const meta = config.siteUrl
  ? '<link rel="canonical" href="' + esc(config.siteUrl) + '"><meta name="robots" content="index,follow">'
  : '<meta name="robots" content="noindex,nofollow">';
const text = x => esc(String(x ?? ''));
const absolute = rel => (config.siteUrl ? new URL(rel, config.siteUrl).href : '');
const description =
  'Statistica e coding R per la geologia. ' +
  counts.experiments +
  ' esperimenti interattivi, ' +
  counts.systems +
  ' sistemi stellari e ' +
  counts.worlds +
  ' pianeti esplorabili, formalismo matematico e R eseguito nel browser.';
// Link previews: Open Graph and Twitter cards; absolute URLs only when the public address is known.
const social =
  [
    ['og:type', 'website'],
    ['og:locale', 'it_IT'],
    ['og:site_name', config.title],
    ['og:title', config.title + ' · ' + config.subtitle],
    ['og:description', description],
    ['og:image', absolute('assets/social-card.jpg') || 'assets/social-card.jpg'],
    ['og:image:width', '1200'],
    ['og:image:height', '630'],
    ['og:image:alt', config.title + ', atlante del corso di statistica e coding R'],
    ...(config.siteUrl ? [['og:url', config.siteUrl]] : []),
  ]
    .map(([property, content]) => '<meta property="' + property + '" content="' + text(content) + '">')
    .join('') + '<meta name="twitter:card" content="summary_large_image">';
fs.writeFileSync(
  path.join(out, 'index.html'),
  fs
    .readFileSync(path.join(root, 'src/index.html'), 'utf8')
    .replace('{{META}}', meta)
    .replace('{{SOCIAL}}', social)
    .replaceAll('{{N_MODULES}}', String(catalogue.modules.length))
    .replaceAll('{{N_EXPERIMENTS}}', String(counts.experiments))
    .replaceAll('{{N_SYSTEMS}}', String(counts.systems))
    .replaceAll('{{N_WORLDS}}', String(counts.worlds))
    .replaceAll('{{N_MISSIONS}}', String(counts.missions))
    .replaceAll('{{AUTHOR}}', esc(config.author || ''))
    .replaceAll('{{MAIN_SITE_NAME}}', esc(config.mainSiteName || ''))
    .replaceAll(
      '{{MAIN_SITE_LINK}}',
      config.mainSiteUrl
        ? '<a class="main-site-link" href="' +
            esc(config.mainSiteUrl) +
            '" aria-label="Torna al sito principale: ' +
            esc(config.mainSiteName || 'sito personale') +
            '">← Sito principale</a>'
        : '',
    ),
);
fs.writeFileSync(path.join(out, '.nojekyll'), '');
fs.writeFileSync(
  path.join(out, 'robots.txt'),
  config.siteUrl ? 'User-agent: *\nAllow: /\n' : 'User-agent: *\nDisallow: /\n',
);
// Script-free pages per module (percorso/): readable without JavaScript, indexable, linked into the atlas.
const pagesDir = path.join(out, 'percorso');
fs.mkdirSync(pagesDir, { recursive: true });
const staticPages = [];
function staticPage(file, title, summary, body) {
  staticPages.push('percorso/' + file);
  fs.writeFileSync(
    path.join(pagesDir, file),
    '<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' +
      text(title) +
      '</title><meta name="description" content="' +
      text(summary) +
      '"><meta name="robots" content="' +
      (config.siteUrl ? 'index,follow' : 'noindex,nofollow') +
      '">' +
      (config.siteUrl ? '<link rel="canonical" href="' + text(absolute('percorso/' + file)) + '">' : '') +
      '<link rel="stylesheet" href="../assets/static.css"></head><body><header><p class="eyebrow">' +
      text(config.title + ' · ' + config.subtitle) +
      '</p></header><main>' +
      body +
      '</main><footer><p>' +
      text(config.author) +
      ' · <a href="../index.html">Atlante interattivo</a> · <a href="index.html">Indice testuale</a></p></footer></body></html>\n',
  );
}
for (const m of catalogue.modules) {
  const sections = [];
  for (const s of read('moduli/' + m.id + '/modulo.json').slides) {
    if (sections.at(-1)?.title !== s.section) sections.push({ title: s.section, slides: [] });
    sections.at(-1).slides.push(s);
  }
  const labs = experiments.activities.filter(a => a.module === m.id);
  staticPage(
    m.id + '.html',
    config.title + ' · ' + m.id + ' · ' + m.title,
    m.subtitle,
    '<p class="eyebrow">' +
      text(m.id + (m.category === 'progetti' ? ' · Spedizione applicativa' : ' · Modulo')) +
      '</p><h1>' +
      text(m.title) +
      '</h1><p class="lead">' +
      text(m.subtitle) +
      '</p><p class="actions"><a href="../#modulo-' +
      text(m.id) +
      '">Apri nell’atlante interattivo</a>' +
      (m.pdf ? '<a href="../' + text(m.pdf) + '">Fascicolo PDF</a>' : '') +
      '</p>' +
      (labs.length
        ? '<h2>Esperimenti</h2><ul>' +
          labs
            .map(
              a =>
                '<li><a href="../#laboratorio/' + text(a.id) + '">' + text(a.title) + '</a>: ' + text(a.goal) + '</li>',
            )
            .join('') +
          '</ul>'
        : '') +
      '<h2>Slide</h2>' +
      sections
        .map(
          section =>
            '<h3>' +
            text(section.title) +
            '</h3><ul>' +
            section.slides
              .map(
                s =>
                  '<li><a href="../#modulo-' +
                  text(m.id) +
                  '/slide/' +
                  text(s.page) +
                  '">' +
                  text(s.title) +
                  '</a></li>',
              )
              .join('') +
            '</ul>',
        )
        .join(''),
  );
}
staticPage(
  'index.html',
  config.title + ' · Indice testuale dei moduli',
  description,
  '<h1>Indice testuale dei moduli</h1><p class="lead">' +
    text(description) +
    '</p>' +
    [
      ['moduli', 'Moduli del corso'],
      ['progetti', 'Spedizioni applicative'],
    ]
      .map(
        ([category, label]) =>
          '<h2>' +
          text(label) +
          '</h2><ul>' +
          catalogue.modules
            .filter(m => m.category === category)
            .map(
              m =>
                '<li><a href="' +
                text(m.id) +
                '.html">' +
                text(m.id + ' · ' + m.title) +
                '</a>: ' +
                text(m.subtitle) +
                '</li>',
            )
            .join('') +
          '</ul>',
      )
      .join(''),
);
if (config.siteUrl)
  fs.writeFileSync(
    path.join(out, 'sitemap.xml'),
    '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
      [config.siteUrl, ...staticPages.map(absolute)].map(u => '<url><loc>' + esc(u) + '</loc></url>').join('') +
      '</urlset>',
  );
for (const f of ['THIRD_PARTY_NOTICES.md', 'LICENSE.md']) fs.copyFileSync(path.join(root, f), path.join(out, f));
// Compact generated SVG markup without changing coordinates, colours or precision.
// Keep the editable course assets untouched.
let svgBytesSaved = 0;
for (const dir of ['assets/slides', 'assets/visuals']) {
  for (const entry of fs.readdirSync(path.join(out, dir), { recursive: true })) {
    if (!entry.endsWith('.svg')) continue;
    const file = path.join(out, dir, entry),
      source = fs.readFileSync(file, 'utf8');
    const compact = compactCourseSVG(
      source.replace(/\b(?:fill|stroke|transform)="(?:rgb|matrix)\([^"<>]*\)"/g, value => value.replace(/,\s+/g, ',')),
    );
    svgBytesSaved += Buffer.byteLength(source) - Buffer.byteLength(compact);
    if (compact !== source) fs.writeFileSync(file, compact);
  }
}
console.log('SVG: ' + svgBytesSaved + ' byte risparmiati senza modifiche grafiche.');
hardenBuild(out);
execFileSync(
  'python3',
  [path.join(root, 'scripts/public_materials.py'), '--output', path.join(out, 'materiali'), '--manifest-only'],
  { stdio: 'inherit' },
);
console.log(
  'Build completata: ' +
    counts.experiments +
    ' esperimenti R, ' +
    counts.systems +
    ' sistemi stellari, ' +
    counts.worlds +
    ' pianeti e ' +
    counts.missions +
    ' spedizioni; materiali originali conservati.',
);
