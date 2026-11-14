// Characterisation harness for refactors: renders 32 routes of dist/ in jsdom and records title and main.innerHTML.
// Usage: node scripts/characterize-routes.mjs before.json   (refactor, rebuild)   node scripts/characterize-routes.mjs after.json
//        node scripts/characterize-routes.mjs --compare before.json after.json
import fs from 'node:fs';
import path from 'node:path';
if (process.argv[2] === '--compare') {
  const [a, b] = process.argv.slice(3).map(f => JSON.parse(fs.readFileSync(f, 'utf8')).snap);
  const changed = Object.keys(a).filter(r => JSON.stringify(a[r]) !== JSON.stringify(b[r]));
  console.log(
    changed.length ? 'Changed routes: ' + changed.join(', ') : 'All ' + Object.keys(a).length + ' routes identical.',
  );
  process.exit(changed.length ? 1 : 0);
}
const { JSDOM, ResourceLoader, VirtualConsole } = await import('jsdom');
const dist = path.resolve('dist'),
  out = process.argv[2];
class Local extends ResourceLoader {
  fetch(url) {
    const u = new URL(url);
    const f = path.resolve(dist, '.' + u.pathname);
    return fs.existsSync(f) ? Promise.resolve(fs.readFileSync(f)) : null;
  }
}
const vc = new VirtualConsole();
const errors = [];
vc.on('jsdomError', e => errors.push(e.message));
const dom = new JSDOM(fs.readFileSync(path.join(dist, 'index.html'), 'utf8'), {
  url: 'https://geostat.test/#catalogo',
  runScripts: 'dangerously',
  resources: new Local(),
  pretendToBeVisual: true,
  virtualConsole: vc,
  beforeParse(w) {
    w.scrollTo = () => {};
    w.HTMLElement.prototype.scrollIntoView = () => {};
    w.matchMedia = () => ({ matches: true, addEventListener() {} });
    w.HTMLCanvasElement.prototype.getContext = () => null;
    w.Image = class {
      set src(v) {
        setTimeout(() => this.onerror?.(), 0);
      }
    };
    w.Math.random = (() => {
      let s = 1;
      return () => (s = (s * 16807) % 2147483647) / 2147483647;
    })();
  },
});
const w = dom.window,
  d = w.document;
const sleep = ms => new Promise(r => setTimeout(r, ms));
for (let i = 0; i < 500 && d.querySelectorAll('.module-card').length !== 28; i++) await sleep(10);
const labs = w.GEO_LABS.activities.filter((a, i) => i % 9 === 0).map(a => '#laboratorio/' + a.id);
const routes = [
  '#catalogo',
  '#esperimenti',
  '#progetti',
  '#materiali',
  '#taccuino',
  '#modulo-M05',
  '#modulo-P01',
  '#modulo-P07',
  '#modulo-M05/slide/3',
  '#modulo-T00',
  '#esplorazione/M05-b',
  '#taccuino-esplorazioni',
  '#inesistente',
  '#laboratorio/non-esiste',
  ...labs,
  '#laboratorio/m05-estimandi?c=%7B%22seed%22%3A7%7D',
  '#laboratorio/m05-estimandi?c=rotto',
];
const snap = {};
for (const r of routes) {
  w.location.hash = r;
  let last = '',
    stable = 0;
  for (let i = 0; i < 300 && stable < 5; i++) {
    await sleep(20);
    const h = d.querySelector('main').innerHTML;
    if (h === last && !h.includes('class="loading"')) stable++;
    else {
      stable = 0;
      last = h;
    }
  }
  snap[r] = { title: d.title, html: d.querySelector('main').innerHTML.replace(/blob:[^"]+/g, 'blob:') };
}
fs.writeFileSync(out, JSON.stringify({ errors, snap }, null, 1));
console.log('routes', routes.length, 'errors', errors.length);
process.exit(0);
