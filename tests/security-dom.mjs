import {JSDOM} from 'jsdom';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const dom = new JSDOM('<main id="main"></main>', {url:'https://geostat.test/',runScripts:'outside-only'});
const w=dom.window;
w.eval(fs.readFileSync('src/security.js','utf8'));
const S=w.GeoSecurity;
for(const payload of [
 '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
 '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>',
 '<svg xmlns="http://www.w3.org/2000/svg"><foreignObject/></svg>',
 '<svg xmlns="http://www.w3.org/2000/svg"><use href="https://invalid.test/x"/></svg>',
 '<svg xmlns="http://www.w3.org/2000/svg"><style>@import "https://invalid.test/x";</style></svg>',
 '<svg xmlns="http://www.w3.org/2000/svg"><rect style="fill:url(https://invalid.test/x)"/></svg>',
 '<!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]><svg xmlns="http://www.w3.org/2000/svg"/>',
 '<?xml-stylesheet href="https://invalid.test/x"?><svg xmlns="http://www.w3.org/2000/svg"/>'
])assert.throws(()=>S.svg(payload));
assert(S.svg('<svg xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="cpMC4wMHw2NDguMDA="><rect width="1" height="1"/></clipPath></defs><g clip-path="url(#cpMC4wMHw2NDguMDA=)"><path d="M0 0L1 1"/></g></svg>'));
let figures=0;
for(const f of fs.readdirSync('assets/experiments').filter(f=>f.endsWith('.svg'))){assert(S.svg(fs.readFileSync('assets/experiments/'+f,'utf8')).startsWith('<svg'));figures++;}
const data=JSON.parse(fs.readFileSync('content/experiments.json'));
const catalogue=JSON.parse(fs.readFileSync('content/catalogue.json'));
const a=data.activities.find(a=>a.id==='m05-intervalli');
let executions=0;
w.GEO_LABS=data;w.GEO_CATALOG=catalogue;w.GeoPlanets={byId:Object.fromEntries(catalogue.modules.map(m=>[m.id,{name:m.id}]))};
w.GeoREngine={subscribe:()=>()=>{},paramsCode:()=>'',reset:()=>{},init:async()=>{},run:async()=>{executions++;throw Error('Test execution reached');}};
w.fetch=async()=>{throw Error('No preview needed');};
// Keep timers inert; exercise the event handlers explicitly.
w.setTimeout=()=>1;w.clearTimeout=()=>{};
w.eval(fs.readFileSync('src/experiments.js','utf8'));
const main=w.document.querySelector('main');w.GeoLabs.experiment(main,a);
const input=w.document.querySelector('#lab-import-file');
const imported=JSON.stringify({application:'GeoStatLab',version:1,activity:a.id,parameters:{},code:'stop("UNREVIEWED")',notes:'<img src=x onerror=alert(1)>'});
Object.defineProperty(input,'files',{value:[{size:imported.length,text:async()=>imported}],configurable:true});
input.dispatchEvent(new w.Event('change'));await new Promise(r=>setTimeout(r,0));
assert.equal(executions,0);assert.equal(w.document.querySelector('#lab-auto').checked,false);
assert.equal(w.document.querySelector('#lab-code-editor').value,'stop("UNREVIEWED")');
assert.equal(w.document.querySelectorAll('[onerror]').length,0);
w.document.querySelector('#lab-run').click();await new Promise(r=>setTimeout(r,0));assert.equal(executions,0);
assert(w.document.querySelector('#lab-error').textContent.includes('Controllalo'));
w.document.querySelector('#lab-run-code').click();await new Promise(r=>setTimeout(r,0));assert.equal(executions,1);
assert(w.document.querySelector('#lab-error').textContent.includes('Test execution reached'));
w.GeoLabs.cleanup();w.close();
console.log('DOM security: 8 hostile SVG payloads rejected, '+figures+' valid R figures accepted, imported code requires explicit execution.');
