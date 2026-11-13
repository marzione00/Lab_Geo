import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {JSDOM} from 'jsdom';
const source=fs.readFileSync('src/code-terminal.js','utf8');
const activities=JSON.parse(fs.readFileSync('content/experiments.json')).activities;
const context=vm.createContext({});vm.runInContext(source,context);const G=context.GeoCodeGuide;
test('The teaching view covers all 139 original programs without discarding source lines',()=>{
 let steps=0;
 for(const a of activities){const blocks=G.blocks(a.code);assert(blocks.length>0,a.id);steps+=blocks.length;
  assert.equal(blocks.map(b=>b.source).join('\n\n'),a.code,a.id);
  for(const b of blocks){assert(b.comment.length>20,a.id);assert.equal(a.code.split('\n').slice(b.start-1,b.end).join('\n'),b.source,a.id);}
  const annotated=G.annotated(a);assert.equal(annotated.split('\n').filter(line=>!line.startsWith('# ')).join('\n'),a.code);
 }
 assert(steps>600);
});
test('R terminal updates parameters, steps through real source and escapes untrusted custom code',()=>{
 const dom=new JSDOM('<section></section>',{runScripts:'outside-only'}),w=dom.window;w.eval(source);
 const a=activities.find(a=>a.id==='m05-distribuzioni'),p=Object.fromEntries(a.controls.map(c=>[c.key,c.value]));
 let downloads=0,edits=0;const host=w.document.querySelector('section'),terminal=w.GeoCodeGuide.mount(host,a,p,{download:()=>downloads++,edit:()=>edits++});
 assert(host.textContent.includes('replicate'));assert(host.querySelector('.r-parameters').open);
 terminal.update({...p,n:120});assert(host.querySelector('.r-parameters code').textContent.includes('n = 120'));
 host.querySelector('[data-r="focus"]').click();host.querySelector('[data-r="next"]').click();
 assert.equal(host.querySelectorAll('.r-code-block:not([hidden])').length,1);assert(host.querySelector('.r-step-count').textContent.includes('2 /'));
 host.querySelector('[data-r="comments"]').click();assert.equal(host.querySelectorAll('.r-code-comment:not([hidden])').length,0);
 host.querySelector('[data-r="download"]').click();host.querySelector('[data-r="edit"]').click();assert.equal(downloads,1);assert.equal(edits,1);
 const malicious='x <- "<img src=x onerror=alert(1)>"\n\nstop("custom")';terminal.update(p,malicious);
 assert.equal(host.querySelectorAll('img,script,[onerror]').length,0);assert(host.textContent.includes('spiegazioni del modello originale sono sospese'));
 assert.equal(w.GeoCodeGuide.annotated(a,malicious),malicious);
 terminal.update(p,a.code);assert(!host.querySelector('.r-step-reading').textContent.includes('sospese'));
 terminal.destroy();assert.equal(host.children.length,0);w.close();
});
test('Downloaded standard R scripts carry comments and the exact parameter configuration',()=>{
 const w=vm.createContext({GEO_LABS:{common:'# helper functions'},GeoSecurity:{}});vm.runInContext(source,w);w.window=w;vm.runInContext(fs.readFileSync('src/lab-engine.js','utf8'),w);
 const a=activities.find(a=>a.id==='m05-distribuzioni'),p=Object.fromEntries(a.controls.map(c=>[c.key,c.value]));p.n=120;
 const script=w.GeoREngine.script(a,p);assert(script.includes('# Numero di osservazioni\n  n = 120'));assert(script.includes('# Assegna il risultato a means.'));assert(script.includes(a.code.split('\n')[0]));
 const custom='stop("custom")';assert(w.GeoREngine.script(a,p,custom).includes(custom));
});
