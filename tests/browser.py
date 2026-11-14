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
def wait_true(pg,expr,arg=None,timeout=15000):
 # Polls through DevTools evaluation: wait_for_function re-evaluates strings with eval, which the CSP blocks.
 end=time.time()+timeout/1000
 while time.time()<end:
  if (pg.evaluate(expr,arg) if arg is not None else pg.evaluate(expr)):return
  pg.wait_for_timeout(100)
 raise AssertionError('Timeout: '+expr[:100])
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
  # Every context starts as a returning reader (briefing and hints seen) unless first_visit=True.
  SEEN="try{localStorage.setItem('geostat:briefing:v1','seen');for(const k of ['system','module','experiment'])localStorage.setItem('geostat:hint:'+k,'seen')}catch(e){}"
  _new_context=browser.new_context
  def new_context(first_visit=False,**options):
   c=_new_context(**options)
   if not first_visit:c.add_init_script(SEEN)
   return c
  browser.new_context=new_context
  context=browser.new_context(viewport={'width':1440,'height':1000})
  context.tracing.start(screenshots=True,snapshots=True,sources=True)
  page=context.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
  try:
   page.goto(url+'#catalogo')
   wait_true(page,"document.querySelectorAll('.module-card').length===28")
   page.screenshot(path=str(OUT/'indice.png'),full_page=False)
   page.locator('#cerca-moduli').fill('P11')
   assert page.locator('.module-card').count()==1
   page.locator('[data-filter="moduli"]').click()
   assert page.locator('.module-card').count()==0
   checks.append('Ricerca e filtri combinati')
   page.goto(url+'#indice')
   expect(page.locator('.galaxy-node')).to_have_count(17)
   # Stop automatic motion while targeting labels; camera controls stay active.
   page.locator('#motion-toggle').click()
   expect(page.locator('#motion-toggle')).to_have_attribute('aria-pressed','true')
   wait_true(page,"window.GeoGalaxy?.debug()?.worlds.every(p=>p.screen)")
   before=page.evaluate('GeoGalaxy.debug().worlds.map(p=>p.screen.x)')
   page.locator('#galaxy-viewport').press('ArrowRight')
   wait_true(page,'(old)=>GeoGalaxy.debug().worlds.some((p,i)=>Math.abs(p.screen.x-old[i])>1)',before)
   page.get_by_role('button',name='Ripristina la vista della galassia',exact=True).click()
   for node in page.locator('.galaxy-node').all():
    node.hover()
    identifier=node.get_attribute('data-destination')
    expect(page.locator('#galaxy-travel')).to_have_attribute('href','#sistema-'+identifier)
    expect(page.locator('.galaxy-node[aria-pressed="true"]')).to_have_count(1)
   page.locator('[data-destination="M14"]').hover()
   expect(page.locator('#destination-name')).to_have_text('Pyra')
   page.locator('#motion-toggle').click()
   page.locator('#galaxy-travel').click()
   page.locator('#system-title').wait_for()
   expect(page.locator('[data-body]')).to_have_count(6)
   for body in page.locator('[data-body]').all():
    body.click()
    expect(body).to_have_attribute('aria-pressed','true')
   page.locator('[data-body="star"]').click()
   page.locator('#locate-module').click()
   expect(page.locator('#body-name')).to_have_text('Ignis')
   page.locator('#enter-module').click()
   page.get_by_role('heading',name='Estremi, pericolosità e rischio',exact=True).wait_for()
   assert page.evaluate('GeoGalaxy.debug()') is None
   checks.append('Galassia 3D: camera, pausa, 17 destinazioni, viaggio e smontaggio della scena')
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
    wait_true(page,"document.querySelector('.slide-frame img')?.complete && document.querySelector('.slide-frame img')?.naturalWidth>0")
   checks.append('28 moduli e prima slide di contenuto')
   page.goto(url+'#esperimenti')
   expect(page.locator('.experiment-card')).to_have_count(len(activities))
   page.locator('#search-experiments').fill('bootstrap')
   expect(page.locator('.experiment-card')).to_have_count(6)
   page.locator('#filter-experiments').select_option('M05')
   expect(page.locator('.experiment-card')).to_have_count(4)
   checks.append('Catalogo esperimenti, ricerca e filtro per modulo')
   page.goto(url+'#laboratorio/m05-intervalli')
   expect(page.locator('#narrative-scene')).to_be_visible()
   expect(page.locator('#save-fieldbook')).to_be_disabled()
   page.locator('#lab-run').click()
   expect(page.locator('#lab-result-meta')).to_contain_text('CALCOLO R COMPLETATO',timeout=120000)
   coverage=page.locator('#lab-metrics .lab-metric strong').first
   expect(coverage).to_have_text('0.935')
   page.locator('#lab-compare').click()
   page.locator('#param-rho').fill('0.3')
   expect(coverage).to_have_text('0.38',timeout=60000)
   page.locator('#lab-compare').click()
   expect(page.locator('#lab-comparison article')).to_have_count(2)
   expect(page.locator('#lab-comparison img')).to_have_count(2)
   expect(page.locator('#narrative-comparison')).to_contain_text('correlazione')
   expect(page.locator('#narrative-result-text')).to_contain_text('38%')
   page.locator('#save-fieldbook').click()
   expect(page.locator('#fieldbook-status')).to_contain_text('conservate')
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
    page.goto(url+'#sistema-M01')
    page.locator('#system-title').wait_for()
    assert_layout('sistema stellare')
    page.locator('#locate-module').click()
    expect(page.locator('#body-name')).to_have_text('Terra')
    assert_layout('pianeta in primo piano')
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
   page.goto('about:blank')  # isolate the timing probes from the animated page and the trace recorder
   shifts=[]
   for vw,vh in [(390,844),(1440,900)]:
    for r in ['#indice','#catalogo','#esperimenti','#modulo-M05','#laboratorio/m05-estimandi','#sistema-M05','#modulo-P01']:
     fresh=browser.new_context(viewport={'width':vw,'height':vh})
     fresh.add_init_script("window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});")
     probe=fresh.new_page();probe.goto(url+r);probe.wait_for_timeout(3000)
     shifts.append(dict(route=r,width=vw,cls=round(probe.evaluate('window.__cls'),4)));fresh.close()
   (OUT/'layout-shift.json').write_text(json.dumps(shifts,ensure_ascii=False,indent=2))
   worst=max(shifts,key=lambda x:x['cls'])
   assert worst['cls']<0.1,'Layout shift: '+json.dumps(worst,ensure_ascii=False)
   checks.append('Layout shift sotto 0,1 al primo caricamento su 7 rotte a 390 e 1440 px')
   budget=[]
   for r in ['#indice','#sistema-M05','#modulo-M05']:
    fresh=browser.new_context(viewport={'width':1440,'height':900})
    fresh.add_init_script("window.__long=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.__long.push(e.duration)}).observe({type:'longtask',buffered:true});")
    probe=fresh.new_page();probe.goto(url+r);probe.wait_for_timeout(3000);probe.evaluate('window.__long=[]');probe.wait_for_timeout(10000)
    budget.append(dict(route=r,longtask_ms=round(probe.evaluate('window.__long.reduce((a,b)=>a+b,0)')),space=probe.evaluate('window.GeoSpace?.debug().renderer')));fresh.close()
   (OUT/'main-thread.json').write_text(json.dumps(budget,ensure_ascii=False,indent=2))
   assert all(x['longtask_ms']<500 for x in budget),'Main thread: '+json.dumps(budget,ensure_ascii=False)
   checks.append('Thread principale: meno di 500 ms di task lunghi in 10 s su home, sistema e modulo')
   fresh=browser.new_context(viewport={'width':1440,'height':900})
   fresh.add_init_script("try{localStorage.setItem('geostat:force-webgl','1')}catch(e){}")
   probe=fresh.new_page();probe.on('pageerror',lambda e:errors.append(str(e)))
   probe.goto(url+'#indice');probe.wait_for_timeout(3000)
   assert probe.evaluate('window.GeoGalaxy.debug()?.renderer')=='webgl','WebGL path not exercised'
   probe.goto(url+'#sistema-M05');probe.wait_for_timeout(6000)
   probe.evaluate("window.__slow=0;let p=0;const f=t=>{if(p&&t-p>120)window.__slow++;p=t;requestAnimationFrame(f)};requestAnimationFrame(f)");probe.wait_for_timeout(4000)
   assert probe.evaluate('window.__slow')<8,'WebGL system view stays slow without falling back'
   fresh.close()
   # Module pages use the GeoSpace renderer: its watchdog must fire even when intervals alternate around 120 ms.
   fresh=browser.new_context(viewport={'width':1440,'height':900})
   fresh.add_init_script("try{localStorage.setItem('geostat:force-webgl','1')}catch(e){}")
   probe=fresh.new_page();probe.on('pageerror',lambda e:errors.append(str(e)))
   probe.goto(url+'#modulo-M05');probe.wait_for_timeout(6000)
   probe.evaluate("window.__slow=0;let p=0;const f=t=>{if(p&&t-p>100)window.__slow++;p=t;requestAnimationFrame(f)};requestAnimationFrame(f)");probe.wait_for_timeout(4000)
   assert probe.evaluate('window.__slow')<8,'WebGL module view stays slow without falling back: '+str(probe.evaluate('window.GeoSpace.debug().renderer'))
   fresh.close()
   checks.append('Percorso WebGL forzato: galassia in WebGL; viste di sistema e di modulo fluide o ripiegate sul canvas')
   axe=(ROOT/'node_modules/axe-core/axe.min.js').read_text(encoding='utf-8');violations={}
   # Briefing: first visit to the home page only, Esc closes it and returns focus, axe with the dialog open.
   for vw,vh in [(390,844),(1440,900)]:
    fresh=browser.new_context(first_visit=True,viewport={'width':vw,'height':vh});probe=fresh.new_page()
    probe.on('pageerror',lambda e:errors.append(str(e)))
    probe.goto(url+'#indice');probe.wait_for_selector('dialog.briefing[open]',timeout=10000);probe.wait_for_timeout(800)
    probe.evaluate(axe)
    found=probe.evaluate("async()=>(await axe.run(document,{resultTypes:['violations']})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target.join(' '))}))")
    assert not found,'Briefing accessibility at %d px: %s'%(vw,json.dumps(found,ensure_ascii=False))
    probe.keyboard.press('Escape');probe.wait_for_timeout(300)
    assert probe.evaluate("!document.querySelector('dialog.briefing') && document.activeElement.id==='contenuto'"),'Esc must close the briefing and return focus'
    probe.reload();probe.wait_for_timeout(2500)
    assert not probe.evaluate("!!document.querySelector('dialog.briefing')"),'Briefing shown twice'
    fresh.close()
   fresh=browser.new_context(first_visit=True,viewport={'width':1440,'height':900});probe=fresh.new_page()
   probe.goto(url+'#laboratorio/m05-estimandi');probe.wait_for_timeout(3000)
   assert not probe.evaluate("!!document.querySelector('dialog.briefing')"),'A deep link must open the page directly'
   assert probe.evaluate("!!document.querySelector('.briefing-hint')"),'First-visit hint missing on the laboratory'
   fresh.close()
   # Audio: no AudioContext before consent; consent starts it; the choice survives a reload but waits for a gesture.
   fresh=browser.new_context(first_visit=True,viewport={'width':1440,'height':900})
   fresh.add_init_script("window.__ac=0;const A=window.AudioContext;window.AudioContext=class extends A{constructor(...a){super(...a);window.__ac++}};window.__long=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.__long.push(e.duration)}).observe({type:'longtask',buffered:true});")
   probe=fresh.new_page();probe.on('pageerror',lambda e:errors.append(str(e)))
   probe.goto(url+'#indice');probe.wait_for_selector('dialog.briefing[open]',timeout=10000)
   assert probe.evaluate('window.__ac')==0,'AudioContext created before consent'
   probe.click('[data-audio=on]');probe.wait_for_timeout(1500)
   assert probe.evaluate('window.GeoAudio?.state().running'),'Audio did not start after consent'
   probe.keyboard.press('Escape')
   audio_budget={}
   for r in ['#indice','#modulo-M05']:
    probe.goto(url+r);probe.wait_for_timeout(2500);probe.evaluate('window.__long=[]');probe.wait_for_timeout(10000)
    audio_budget[r]=round(probe.evaluate('window.__long.reduce((a,b)=>a+b,0)'))
   assert all(v<500 for v in audio_budget.values()),'Main thread with audio: '+json.dumps(audio_budget)
   probe.reload();probe.wait_for_timeout(1500)
   assert probe.get_attribute('#audio-toggle','aria-pressed')=='true' and probe.evaluate('window.__ac')==0,'Audio must wait for a gesture after reload'
   probe.mouse.click(5,5);probe.wait_for_timeout(1200)
   assert probe.evaluate('window.GeoAudio?.state().running'),'Audio did not resume at the first interaction'
   probe.click('#audio-toggle');probe.wait_for_timeout(900)
   assert probe.evaluate("!window.GeoAudio.state().enabled && localStorage.getItem('geostat:audio')==='off'"),'Audio switch'
   fresh.close()
   (OUT/'briefing-audio.json').write_text(json.dumps(dict(audio_longtask_ms=audio_budget),indent=2))
   checks.append('Briefing alla prima visita, Esc e focus, axe a 390 e 1440 px; audio solo dopo il consenso, scelta ricordata, task lunghi sotto 500 ms')
   for r in ['#indice','#catalogo','#esperimenti','#progetti','#materiali','#taccuino','#sistema-M05','#modulo-M05','#modulo-M05/slide/3','#laboratorio/m05-estimandi','#esplorazione/M05-b']:
    fresh=browser.new_context(viewport={'width':1440,'height':900});probe=fresh.new_page();probe.goto(url+r);probe.wait_for_timeout(2500);probe.evaluate(axe)
    found=probe.evaluate("async()=>(await axe.run(document,{resultTypes:['violations'],rules:{'label-content-name-mismatch':{enabled:true}}})).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target.join(' '))}))")
    if found:violations[r]=found
    fresh.close()
   (OUT/'axe.json').write_text(json.dumps(violations,ensure_ascii=False,indent=2))
   assert not violations,'Accessibility: '+json.dumps(violations,ensure_ascii=False)[:2000]
   checks.append('axe-core 4.14: nessuna violazione su 11 rotte')
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
