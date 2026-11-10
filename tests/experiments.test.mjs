import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';import test from 'node:test';
const data=JSON.parse(fs.readFileSync('content/experiments.json','utf8'));
const modules=JSON.parse(fs.readFileSync('content/catalogue.json','utf8')).modules;
const sandbox={window:{GEO_LABS:data,GeoREngine:{},GeoPlanets:{byId:Object.fromEntries(modules.map(m=>[m.id,{name:m.id}]))}}};vm.runInNewContext(fs.readFileSync('src/security.js','utf8'),sandbox.window);vm.runInNewContext(fs.readFileSync('src/experiments.js','utf8'),sandbox);const labs=sandbox.window.GeoLabs;
test('Copertura di tutti i 17 moduli e delle 147 sezioni senza collegamenti vuoti',()=>{
 assert.equal(data.activities.length,139);assert.equal(data.coverage.length,147);const ids=new Set(data.activities.map(a=>a.id));assert.equal(ids.size,139);assert.equal(new Set(data.activities.map(a=>a.module)).size,17);
 for(const c of data.coverage){assert(c.activities.length);assert(c.activities.every(id=>ids.has(id)));if(c.role==='esperimento')assert(c.activities.every(id=>data.activities.find(a=>a.id===id).section===c.section));}
 for(const a of data.activities){assert(a.code&&a.formula&&a.action&&a.conclusion&&a.limits&&a.symbols);assert.equal(a.prose.length,2);assert(!/[\x00-\x1f]/.test(a.symbols+a.prose.join(" ")),a.id+" contains escaped control characters");assert(a.controls.length>=2);assert(fs.existsSync(a.source));assert(fs.existsSync('assets/experiments/'+a.id+'-1.svg'));assert(fs.existsSync('assets/experiments/'+a.id+'.json'));}
});
test('Parametri e collegamenti respingono valori fuori dominio',()=>{
 for(const a of data.activities){const p=labs.validate(a,{});assert.equal(p.seed,17);assert.equal(labs.parseHash('#laboratorio/'+a.id).activity,a.id);assert.throws(()=>labs.validate(a,{seed:NaN}));assert.throws(()=>labs.validate(a,{seed:100000}));for(const c of a.controls){if(c.type==='select')assert.throws(()=>labs.validate(a,{[c.key]:'__invalid__'}));}}
 assert.equal(labs.parseHash('#laboratorio/unknown').type,'notfound');
});
test('Le undici spedizioni collegano soltanto attività implementate',()=>{assert.equal(Object.keys(labs.missions).length,11);for(const m of Object.values(labs.missions)){assert.equal(m.steps.length,3);for(const [, ...ids]of m.steps)for(const id of ids)assert(labs.byId.has(id),id);}});
test('Pacchetti wasm con versioni e impronte vincolate, asset realmente presenti',()=>{
 const lock=JSON.parse(fs.readFileSync('vendor/r-packages-lock.json'));assert(lock.some(p=>p.package==='ggplot2'));assert(lock.some(p=>p.package==='svglite'));for(const p of lock){assert.equal(p.sha256.length,64);assert(fs.existsSync('vendor/r-repo/bin/emscripten/contrib/4.6/'+p.file));}
 const html=fs.readFileSync('config/security.json','utf8');assert(html.includes("connect-src 'self'"));assert(!html.includes(" 'unsafe-eval'"));
});
