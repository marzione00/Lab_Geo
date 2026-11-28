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
let labs = 0;
vm.runInContext(fs.readFileSync(path.join(dist, 'assets/lesson-index.js'), 'utf8'), ctx);
const lessonIndex = ctx.window.GEO_LESSON_INDEX;
// Every module and expedition is a lesson a tappe: no slides, figures or PDF of an earlier edition.
for (const m of c.modules) {
  vm.runInContext(fs.readFileSync(path.join(dist, 'assets/content', m.id + '.js'), 'utf8'), ctx);
  const d = ctx.window.GEO_MODULES[m.id];
  if (!lessonIndex[m.id]) throw Error('Lezione assente: ' + m.id);
  if (m.pdf || m.pages || m.script || d.slides || d.figureCode) throw Error('Strato precedente pubblicato per ' + m.id);
  exists(lessonIndex[m.id].pdf);
  exists(lessonIndex[m.id].download);
  for (const l of d.laboratories) {
    labs++;
    exists(l.path);
  }
}
for (const dir of ['assets/slides', 'assets/visuals', 'materiali/pdf', 'materiali/sorgenti', 'materiali/estratti'])
  if (fs.existsSync(path.join(dist, dir))) throw Error('Cartella dello strato precedente pubblicata: ' + dir);
for (const f of [
  'assets/mark.svg',
  'assets/topography.svg',
  'assets/lab.css',
  'assets/app.js',
  'vendor/mathjax/tex-svg.js',
])
  exists(f);
for (const f of [
  'materiali/audit',
  'materiali/Guida_corso_R6.pdf',
  'materiali/Indice_corso.html',
  'materiali/Rapporto_revisione_R6.pdf',
  'materiali/sorgenti/Rapporto_revisione_R6.tex',
  'materiali/sorgenti/revisione_R6.json',
  'materiali/sorgenti/revisione_R6.py',
  'materiali/documentazione/CONSEGNA_R6.json',
]) {
  if (fs.existsSync(path.join(dist, f))) throw Error('Documento editoriale pubblicato: ' + f);
}
for (const f of ['index.html', 'assets/app.js', 'materiali/LEGGIMI.txt']) {
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
const tappe = Object.values(lessonIndex).reduce((n, l) => n + l.pages, 0);
if (c.modules.length !== 32 || Object.keys(lessonIndex).length !== 32 || labs !== 360)
  throw Error('Copertura incompleta.');
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
  for (const [, href] of html.matchAll(/href="([^"#]+)"/g))
    if (!/^[a-z]+:/.test(href)) exists(path.posix.join('percorso', href));
}
for (const f of ['assets/social-card.jpg', 'assets/static.css']) exists(f);
console.log(
  'Distribuzione verificata: ' +
    c.modules.length +
    ' lezioni a tappe (' +
    c.modules.filter(m => m.category === 'moduli').length +
    ' moduli e 11 spedizioni, ' +
    tappe +
    ' tappe), 360 laboratori R/Python, ' +
    textPages.length +
    ' pagine testuali.',
);
