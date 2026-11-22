#!/usr/bin/env python3
"""GeoStat Lab: esegue in webR (Chromium, sito compilato) tutti i frammenti R delle lezioni.

Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)

Uso dalla radice del repository, dopo npm run build:
    python3 -I scripts/lessons/verify_webr.py [ID ...]
Scrive lezioni/webr/<ID>.json con stato, uscita e impronta di ogni frammento e con la versione di R
del browser. L'importatore usa queste uscite come riferimento dove il frammento è stato eseguito
senza errori e l'impronta coincide; i frammenti che richiedono pacchetti assenti in webR conservano
l'uscita dell'esecuzione nativa.
"""
import importlib.util, json, os, socket, subprocess, sys, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('import_lesson', ROOT / 'scripts/lessons/import_lesson.py')
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)
OUT = ROOT / 'lezioni' / 'webr'
OUT.mkdir(exist_ok=True)
config = json.loads((ROOT / 'lezioni' / 'lezioni.json').read_text(encoding='utf-8'))
ids = sys.argv[1:] or list(config)

norm = lambda s: '\n'.join(l.rstrip() for l in s.replace('\r', '').strip('\n').split('\n'))


with socket.socket() as s:
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
server = subprocess.Popen(['node', 'scripts/serve.mjs'], cwd=ROOT, env=dict(os.environ, PORT=str(port)),
                          stdout=subprocess.DEVNULL)
url = f'http://127.0.0.1:{port}/'
try:
    for _ in range(100):
        try:
            urllib.request.urlopen(url, timeout=.5)
            break
        except Exception:
            time.sleep(.1)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for lid in ids:
            context = browser.new_context()
            context.add_init_script("try{localStorage.setItem('geostat:briefing:v1','seen')}catch(e){}")
            page = context.new_page()
            page.goto(url + '#lezione-' + lid + '/1')
            page.wait_for_timeout(500)
            for _ in range(300):
                if page.evaluate(f"!!window.GEO_LESSONS?.['{lid}']"):
                    break
                page.wait_for_timeout(100)
            files = page.evaluate(f"Object.keys(window.GEO_LESSONS['{lid}'].code)")
            files.sort(key=lambda f: (int(f.split('_')[0]) if f[0].isdigit() else 0, f))
            hashes = importer.fragment_hashes(json.loads((ROOT / 'content/lezioni' / (lid + '.json')).read_text(encoding='utf-8')),
                                     ROOT / config[lid]['source'])
            result, started = {}, time.time()
            for f in files:
                t0 = time.time()
                r = page.evaluate("""async ([id, f]) => {
                  const L = window.GEO_LESSONS[id], c = L.code[f];
                  if (c.needs) return { skipped: c.needs };
                  try {
                    const r = await window.GeoREngine.runSnippet({ project: L.project,
                      deps: c.deps.map(d => L.code[d].code), code: c.code });
                    return { status: r.status, output: r.output, R: r.R, figures: r.figures.length };
                  } catch (err) { return { status: 'failed', output: String(err.message || err) }; }
                }""", [lid, f])
                ref = page.evaluate("([id, f]) => window.GEO_LESSONS[id].code[f].output || ''", [lid, f])
                if 'skipped' not in r:
                    r['same'] = norm(r['output']) == norm(ref)
                r['hash'], r['seconds'] = hashes[f], round(time.time() - t0, 1)
                result[f] = r
                mark = 'salto' if 'skipped' in r else ('=' if r['same'] else r['status'] + ' ≠')
                print(lid, f, mark, r['seconds'], flush=True)
            # Script delle schede del quaderno: devono girare in webR senza errori.
            cards = page.evaluate("""async id => {
              const L = window.GEO_LESSONS[id], out = {};
              for (const c of L.exercises?.cards || []) {
                try {
                  const r = await window.GeoREngine.runSnippet({ project: L.project, code: c.script.code });
                  out[c.script.file] = { status: r.status, tail: r.output.split('\\n').slice(-3).join('\\n') };
                } catch (err) { out[c.script.file] = { status: 'failed', tail: String(err.message || err) }; }
              }
              return out;
            }""", lid)
            for f, r in cards.items():
                print(lid, f, r['status'], flush=True)
            R = next((r['R'] for r in result.values() if r.get('R')), None)
            record = {'R': R, 'fragments': result}
            if cards:
                record['cards'] = cards
            (OUT / (lid + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=1) + '\n',
                                               encoding='utf-8')
            done = [r for r in result.values() if 'skipped' not in r]
            print(lid, 'uguali', sum(r['same'] for r in done), 'su', len(done), 'errori',
                  sum(r['status'] != 'ok' for r in done), 'tempo', round(time.time() - started), flush=True)
            context.close()
        browser.close()
finally:
    server.terminate()
