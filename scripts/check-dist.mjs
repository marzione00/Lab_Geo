import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import { createHash } from 'node:crypto';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'),
  dist = path.join(root, 'dist');
const exists = p => {
  if (!fs.existsSync(path.join(dist, p))) throw Error('Risorsa assente: ' + p);
};
const ctx = vm.createContext({ window: {} });
vm.runInContext(fs.readFileSync(path.join(dist, 'assets/catalogue.js'), 'utf8'), ctx);
const c = ctx.window.GEO_CATALOG;
let pages = 0,
  visuals = 0,
  labs = 0;
for (const m of c.modules) {
  exists(m.pdf);
  exists(m.script);
  vm.runInContext(fs.readFileSync(path.join(dist, 'assets/content', m.id + '.js'), 'utf8'), ctx);
  const d = ctx.window.GEO_MODULES[m.id];
  if (d.slides.length !== m.pages) throw Error(m.id);
  for (const s of d.slides) {
    if ('review' in s) throw Error('Nota editoriale pubblicata: ' + m.id);
    pages++;
    exists(s.image);
    if (s.codePath) exists(s.codePath);
    if (s.figure || s.diagram) {
      visuals++;
      if (s.figure) exists('assets/visuals/' + m.id + '/' + String(s.page).padStart(3, '0') + '.svg');
    }
  }
  for (const l of d.laboratories) {
    labs++;
    exists(l.path);
  }
}
for (const f of [
  'assets/mark.svg',
  'assets/topography.svg',
  'assets/lab.css',
  'assets/app.js',
  'vendor/mathjax/tex-svg.js',
  'materiali/Guida_corso_R6.pdf',
])
  exists(f);
for (const f of [
  'materiali/audit',
  'materiali/Rapporto_revisione_R6.pdf',
  'materiali/sorgenti/Rapporto_revisione_R6.tex',
  'materiali/sorgenti/revisione_R6.json',
  'materiali/sorgenti/revisione_R6.py',
  'materiali/documentazione/CONSEGNA_R6.json',
]) {
  if (fs.existsSync(path.join(dist, f))) throw Error('Documento editoriale pubblicato: ' + f);
}
for (const f of ['index.html', 'assets/app.js', 'materiali/Indice_corso.html', 'materiali/LEGGIMI.txt']) {
  if (
    /audit\/|Rapporto_revisione_R6|Registro_slide_R6|Nota della rilettura|Revisione delle slide|Rilettura delle slide/.test(
      fs.readFileSync(path.join(dist, f), 'utf8'),
    )
  )
    throw Error('Richiamo editoriale pubblicato: ' + f);
}
const materials = path.join(dist, 'materiali'),
  listed = new Set();
for (const line of fs.readFileSync(path.join(materials, 'MANIFEST_SHA256.txt'), 'utf8').trim().split('\n')) {
  const [, digest, name] = line.match(/^([a-f0-9]{64}) {2}(.+)$/) || [];
  if (!name || listed.has(name)) throw Error('Manifesto pubblico non valido: ' + line);
  if (
    createHash('sha256')
      .update(fs.readFileSync(path.join(materials, name)))
      .digest('hex') !== digest
  )
    throw Error('Impronta pubblica errata: ' + name);
  listed.add(name);
}
const actual = fs
  .readdirSync(materials, { recursive: true })
  .filter(name => name !== 'MANIFEST_SHA256.txt' && fs.statSync(path.join(materials, name)).isFile());
if (actual.length !== listed.size || actual.some(name => !listed.has(name)))
  throw Error('Manifesto pubblico incompleto');
if (c.modules.length !== 28 || pages !== 861 || visuals !== 494 || labs !== 360) throw Error('Copertura incompleta.');
const source = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
if (source.includes('{{')) throw Error('Segnaposto non risolto.');
for (const match of source.matchAll(/(?:src|href)="([^"#]+)"/g)) {
  if (!/^[a-z]+:/.test(match[1])) exists(match[1]);
}
// Script-free module pages: one per module plus the index, each with its CSP and no script element.
const textPages = fs.readdirSync(path.join(dist, 'percorso')).filter(f => f.endsWith('.html'));
if (textPages.length !== c.modules.length + 1) throw Error('Pagine testuali: ' + textPages.length);
for (const f of textPages) {
  const html = fs.readFileSync(path.join(dist, 'percorso', f), 'utf8');
  if (!html.includes('http-equiv="Content-Security-Policy"') || /<script\b/i.test(html))
    throw Error('Pagina testuale non conforme: ' + f);
  for (const [, href] of html.matchAll(/href="([^"#]+)"/g)) exists(path.posix.join('percorso', href));
}
for (const f of ['assets/social-card.jpg', 'assets/static.css']) exists(f);
console.log(
  'Distribuzione verificata: 28 fascicoli, 861 slide vettoriali, 494 pannelli visuali, 360 laboratori R/Python, ' +
    textPages.length +
    ' pagine testuali.',
);
