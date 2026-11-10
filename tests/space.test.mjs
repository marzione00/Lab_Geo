import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
await import('../src/planets.js');
const worlds=globalThis.GeoPlanets;
const catalog=JSON.parse(fs.readFileSync(new URL('../content/catalogue.json',import.meta.url))).modules;
test('Ogni modulo ha un pianeta distinto e ogni spedizione ha collegamenti validi',()=>{
 assert.deepEqual(worlds.planets.map(p=>p.id),catalog.filter(m=>m.category==='moduli').map(m=>m.id));
 assert.equal(new Set(worlds.planets.map(p=>p.name)).size,17);
 assert.equal(new Set(worlds.planets.map(p=>p.kind)).size,17);
 assert.equal(Object.keys(worlds.expeditions).length,11);
 for(const [id,parents] of Object.entries(worlds.expeditions)){assert(catalog.some(m=>m.id===id));assert(parents.every(id=>worlds.planets.some(p=>p.id===id)));}
 for(const p of Object.values(worlds.byId)){assert(p.speed>0&&p.speed<.08);assert(fs.existsSync(new URL('../assets/space/'+(p.id==='M01'?'day':'p-'+p.id)+'.webp',import.meta.url)));}
});
