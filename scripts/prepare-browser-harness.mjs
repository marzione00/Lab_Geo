import fs from 'node:fs';
for(const file of ['experiments-harness.html','experiments-harness.js','metrics-comparison.mjs'])fs.copyFileSync('tests/'+file,'dist/'+file);
const activities=JSON.parse(fs.readFileSync('content/experiments.json')).activities;
const baselines=Object.fromEntries(activities.map(a=>[a.id,JSON.parse(fs.readFileSync('assets/experiments/'+a.id+'.json'))]));
fs.writeFileSync('dist/experiments-baselines.js','window.GEO_QA_BASELINES='+JSON.stringify(baselines).replace(/</g,'\\u003c')+';\n');
console.log('Browser harness prepared; rebuild before publication to remove QA-only files.');
