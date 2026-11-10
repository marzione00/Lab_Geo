"""Regressioni HTTP/Chromium; richiede security/requirements.txt e il browser installato."""
from pathlib import Path
import json,os,socket,subprocess,time,urllib.request
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa/browser';OUT.mkdir(parents=True,exist_ok=True)
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
server=subprocess.Popen(['node','scripts/serve.mjs'],cwd=ROOT,env=dict(os.environ,PORT=str(port)),stdout=subprocess.DEVNULL)
url=f'http://127.0.0.1:{port}/'
checks=[];errors=[];layouts=[];page=None;context=None
def assert_layout(label):
 result=page.evaluate("""async () => {
  await document.fonts.ready;
  const width=innerWidth, scrollWidth=document.documentElement.scrollWidth;
  return {url:location.href,width,scrollWidth,candidates:scrollWidth>width ?
   [...document.querySelectorAll('body *')].map(el=>{
    const r=el.getBoundingClientRect();
    return {tag:el.tagName,id:el.id,classes:el.getAttribute('class'),left:r.left,right:r.right};
   }).filter(r=>r.right>width || r.left<0).slice(0,40):[]};
 }""")
 result['label']=label;layouts.append(result)
 (OUT/'layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2))
 assert result['scrollWidth']<=result['width'], 'Horizontal overflow: '+json.dumps(result,ensure_ascii=False)

subprocess.run(['node','scripts/prepare-browser-harness.mjs'],cwd=ROOT,check=True)
try:
 for _ in range(100):
  try:urllib.request.urlopen(url,timeout=.5);break
  except Exception:time.sleep(.1)
 else:raise RuntimeError('Server locale non disponibile.')
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  context=browser.new_context(viewport={'width':1440,'height':1000})
  context.tracing.start(screenshots=True,snapshots=True,sources=True)
  page=context.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
  try:
   page.goto(url+'#catalogo')
   page.wait_for_function("document.querySelectorAll('.module-card').length===28")
   page.screenshot(path=str(OUT/'indice.png'),full_page=False)
   page.locator('#cerca-moduli').fill('P11')
   assert page.locator('.module-card').count()==1
   page.locator('[data-filter="moduli"]').click()
   assert page.locator('.module-card').count()==0
   checks.append('Ricerca e filtri combinati')
   page.goto(url+'#indice')
   expect(page.locator('.galaxy-node')).to_have_count(17)
   for node in page.locator('.galaxy-node').all():
    node.hover()
    identifier=node.get_attribute('data-destination')
    expect(page.locator('#galaxy-travel')).to_have_attribute('href','#modulo-'+identifier)
    expect(page.locator('.galaxy-node[aria-pressed="true"]')).to_have_count(1)
   page.locator('[data-destination="M14"]').hover()
   expect(page.locator('#destination-name')).to_have_text('Ignis')
   page.locator('#galaxy-travel').click()
   page.get_by_role('heading',name='Estremi, pericolosità e rischio',exact=True).wait_for()
   checks.append('Galassia: 17 destinazioni, scheda coerente, viaggio al modulo')
   activities=json.loads((ROOT/'content/experiments.json').read_text())['activities']
   modules=json.loads((ROOT/'content/catalogue.json').read_text())['modules']
   for m in modules:
    page.goto(url+'#modulo-'+m['id'])
    page.get_by_role('heading',name=m['title'],exact=True).wait_for()
    if m['category']=='progetti':
     expect(page.locator('.mission-stage')).to_have_count(3)
    else:
     expect(page.locator('.experiment-card')).to_have_count(sum(a['module']==m['id'] for a in activities))
    page.goto(url+'#modulo-'+m['id']+'/slide/3')
    expect(page.locator('.slide-frame img')).to_have_attribute('src','assets/slides/'+m['id']+'/003.svg')
    page.wait_for_function("document.querySelector('.slide-frame img')?.complete && document.querySelector('.slide-frame img')?.naturalWidth>0")
   checks.append('28 moduli e prima slide di contenuto')
   page.goto(url+'#esperimenti')
   expect(page.locator('.experiment-card')).to_have_count(len(activities))
   page.locator('#search-experiments').fill('bootstrap')
   expect(page.locator('.experiment-card')).to_have_count(6)
   page.locator('#filter-experiments').select_option('M05')
   expect(page.locator('.experiment-card')).to_have_count(4)
   checks.append('Catalogo esperimenti, ricerca e filtro per modulo')
   page.goto(url+'#laboratorio/m05-intervalli')
   expect(page.locator('#lab-result-meta')).to_contain_text('CALCOLO R COMPLETATO',timeout=120000)
   coverage=page.locator('#lab-metrics .lab-metric strong').first
   expect(coverage).to_have_text('0.935')
   page.locator('#lab-compare').click()
   page.locator('#param-rho').fill('0.3')
   expect(coverage).to_have_text('0.38',timeout=60000)
   page.locator('#lab-compare').click()
   expect(page.locator('#lab-comparison article')).to_have_count(2)
   expect(page.locator('#lab-comparison img')).to_have_count(2)
   page.get_by_role('button',name='Formalismo e codice',exact=True).click()
   page.locator('#lab-theory mjx-container[jax="SVG"]').first.wait_for()
   expect(page.locator('#lab-code-editor')).to_be_visible()
   assert page.locator('[data-mml-node="merror"],mjx-merror').count()==0
   page.screenshot(path=str(OUT/'laboratorio-r.png'),full_page=False)
   checks.append('R/WebAssembly, copertura, confronto A/B e formalismo')
   imported=dict(application='GeoStatLab',version=1,activity='m05-intervalli',parameters={},code='stop("IMPORTED_CODE_EXECUTED")',notes='<img src=x onerror=alert(1)>')
   page.locator('#lab-import-file').set_input_files(dict(name='configuration.json',mimeType='application/json',buffer=json.dumps(imported).encode()))
   expect(page.locator('#lab-code-editor')).to_have_value(imported['code'])
   expect(page.locator('#lab-auto')).not_to_be_checked()
   page.locator('#lab-run').click()
   expect(page.locator('#lab-error')).to_contain_text('Controllalo')
   assert page.locator('[onerror]').count()==0
   checks.append('Imported R requires explicit review; HTML notes stay text')
   page.goto(url+'#modulo-M01/slide/6')
   page.get_by_role('tab',name='Testo e formule').click()
   expect(page.locator('.reading-diagram image')).to_have_attribute('href','assets/slides/M01/006.svg')
   checks.append('Diagramma TikZ con risorsa vettoriale condivisa')

   page.goto(url+'#modulo-P11/slide/10')
   expect(page.locator('.page-counter')).to_have_text('10 / 17')
   page.get_by_role('tab',name='Testo e formule').click()
   page.locator('mjx-container[jax="SVG"]').first.wait_for()
   assert page.locator('[data-mml-node="merror"],mjx-merror').count()==0
   page.screenshot(path=str(OUT/'formule.png'),full_page=False)
   checks.append('Formalismo SVG nella lettura testuale')
   page.locator('#mark-done').click()
   page.reload()
   expect(page.locator('#mark-done')).to_have_attribute('aria-pressed','true')
   checks.append('Persistenza del progresso')
   page.goto(url+'#modulo-M05/slide/105')
   expect(page.locator('.page-counter')).to_have_text('105 / 105')
   expect(page.get_by_role('button',name='Slide successiva',exact=True)).to_be_disabled()
   page.goto(url+'#modulo-M05/slide/106')
   page.get_by_role('heading',name='Pagina non trovata',exact=True).wait_for()
   checks.append('Limiti della paginazione e rotta invalida')
   page.goto(url+'#modulo-T00/codici')
   page.locator('#select-code').select_option('T00_PY_N01')
   assert page.locator('#download-code').get_attribute('href').endswith('T00_N01.py')
   assert 'import' in page.locator('#current-code').inner_text()
   checks.append('Laboratorio Python e collegamento al file')
   page.set_viewport_size({'width':390,'height':844})
   page.goto(url+'#indice')
   page.wait_for_selector('.galaxy-home')
   assert_layout('home mobile')
   page.screenshot(path=str(OUT/'mobile.png'),full_page=False)
   page.goto(url+'#modulo-M05/slide/44')
   expect(page.locator('.page-counter')).to_have_text('44 / 105')
   page.get_by_role('tab',name='Testo e formule').click()
   page.locator('mjx-container[jax="SVG"]').first.wait_for()
   assert_layout('lettura con formule mobile')
   checks.append('Viewport mobile 390 px')
   # Keep the strict overflow assertion; cover every planetary header at narrow,
   # intermediate and desktop widths. Clipped decorations must not hide content.
   for width in [320,390,430,768,1440]:
    page.set_viewport_size({'width':width,'height':844})
    page.goto(url+'#indice')
    page.locator('.galaxy-home').wait_for()
    assert_layout('home')
    for m in modules:
     page.goto(url+'#modulo-'+m['id'])
     page.get_by_role('heading',name=m['title'],exact=True).wait_for()
     assert_layout(m['id'])
    page.goto(url+'#modulo-M05/slide/44')
    expect(page.locator('.page-counter')).to_have_text('44 / 105')
    page.get_by_role('tab',name='Testo e formule').click()
    page.locator('mjx-container[jax="SVG"]').first.wait_for()
    assert_layout('lettura con formule')
   checks.append('Home, 28 moduli e formule senza overflow a 320/390/430/768/1440 px')
   page.goto(url+'experiments-harness.html')
   page.locator('#start').click()
   expect(page.locator('#status')).to_have_text('COMPLETATO · 139 superati · 0 errori',timeout=600000)
   result=json.loads(page.locator('#report').inner_text())
   assert result['failed'] == 0 and result['passed'] == 139
   assert all(r['ok'] and not r['differences'] for r in result['results'])
   (OUT/'all-experiments.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
   checks.append('139 R experiments and all generated SVGs with security validation')
   assert not errors,errors
  except Exception:
   try: page.screenshot(path=str(OUT/'errore.png'),full_page=False)
   except Exception: pass
   raise
  finally:
   context.tracing.stop(path=str(OUT/'trace.zip'))
   browser.close()
 (OUT/'esito.json').write_text(json.dumps(dict(esito='superato',controlli=checks,errori_javascript=errors),ensure_ascii=False,indent=2))
 print('Browser:',len(checks),'gruppi di controlli superati.')
except Exception as exc:
 (OUT/'esito.json').write_text(json.dumps(dict(esito='fallito',controlli=checks,errori_javascript=errors,errore=str(exc)),ensure_ascii=False,indent=2))
 raise
finally:
 for name in ['experiments-harness.html','experiments-harness.js','experiments-baselines.js','metrics-comparison.mjs']:(ROOT/'dist'/name).unlink(missing_ok=True)
 server.terminate()
 server.wait(timeout=10)
