import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const scope={};for(const f of ['planets','astro-model','galaxy-model','core'])vm.runInNewContext(fs.readFileSync('src/'+f+'.js','utf8'),scope);
const A=scope.GeoAstro,M=scope.GeoGalaxyModel,C=scope.GeoCore;
const near=(a,b)=>assert(Math.abs(a-b)<1e-8);
test('Physical solar benchmarks and Kepler ratios are recovered',()=>{near(A.luminosity(1,5772),1);near(A.period(1,1),1);near(A.period(2,1),Math.sqrt(8));near(A.period(1,4),.5);assert(Math.abs(A.equilibrium(1,1,.3)-254.6)<.1);near(A.equilibrium(1,4,.3)/A.equilibrium(1,1,.3),.5);});
test('17 deterministic systems have 85 distinct worlds and exactly one correct module each',()=>{
 assert.equal(A.systems.length,17);assert.equal(new Set(A.systems.flatMap(s=>s.planets.map(p=>p.id))).size,85);assert.equal(new Set(A.systems.map(s=>s.star.type)).size,4);
 for(const s of A.systems){assert.equal(JSON.stringify(s),JSON.stringify(A.generate(s.id)));for(const variant of [0,1,25,9999]){const sys=A.generate(s.id,variant);assert.equal(sys.planets.filter(p=>p.isTarget).length,1);assert.equal(sys.target.moduleId,s.id);assert.equal(sys.target.name,scope.GeoPlanets.byId[s.id].name);assert.equal(sys.planets.length,5);
  near(sys.star.luminosity,A.luminosity(sys.star.radius,sys.star.temperature));let previous=0;for(const p of sys.planets){assert(p.axisAU>previous);previous=p.axisAU;assert([p.temperature,p.periodYears,p.flux,p.radiusEarth].every(n=>Number.isFinite(n)&&n>0));assert(p.albedo>=0&&p.albedo<1);near(p.periodYears,A.period(p.axisAU,sys.star.mass));near(Math.hypot(...A.position(p,0)),p.orbitRadius);const oneYear=A.position(p,p.periodYears),initial=A.position(p,0);oneYear.forEach((v,i)=>near(v,initial[i]));assert(fs.existsSync('assets/space/'+(p.textureId==='M01'?'day':'p-'+p.textureId)+'.webp'));}}
 }
 for(const id of ['M99','M00','P01','__proto__','M01/../../'])assert.equal(A.generate(id),null);
 assert.equal(A.generate('M01',-1),null);assert.notEqual(JSON.stringify(A.generate('M01')),JSON.stringify(A.generate('M01',1)));
});
test('Stellar systems have safe direct routes, and initial orbits remain in the chart',()=>{
 const modules=JSON.parse(fs.readFileSync('content/catalogue.json')).modules;
 for(const s of A.systems){assert.equal(C.parseRoute('#sistema-'+s.id,modules).type,'system');for(const [width,height]of [[300,520],[390,520],[580,570],[930,600]]){const camera=M.camera(0,.85,40*Math.max(1,height/width*.9),[0,0,0],width/height);for(const p of s.planets)for(const years of [0,.2,1])assert(M.project(A.position(p,years),camera.vp,width,height).visible);}}
 assert.equal(C.parseRoute('#sistema-M99',modules).type,'notfound');assert.equal(C.parseRoute('#sistema-P01',modules).type,'notfound');
});
