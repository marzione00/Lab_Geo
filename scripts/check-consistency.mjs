import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {moduleGuides} from './update-module-guides.mjs';
const read=file=>JSON.parse(fs.readFileSync(file,'utf8'));
const catalogue=read('content/experiments.json'), activities=catalogue.activities;
assert.equal(catalogue.version,read('package.json').version,'Application/catalogue version');
assert.equal(read('package-lock.json').packages[''].version,read('package.json').version,'Root package lock version');
assert.equal(read('package-lock.json').version,read('package.json').version,'Package lock version');
assert.deepEqual(read('content/experiments-draft.json'),activities,'Native-check catalogue differs');
const ids=new Set(activities.map(a=>a.id)), owners=new Map(), limits=new Set();
for(const file of fs.readdirSync('content').filter(f=>/^prose-.*\.json$/.test(f))){
 for(const [id,fields] of Object.entries(read('content/'+file))){
  assert(ids.has(id),'Orphan editorial activity: '+id);assert(!owners.has(id),'Duplicate editorial activity: '+id);owners.set(id,file);
  const activity=activities.find(a=>a.id===id);
  for(const [key,value]of Object.entries(fields))assert.deepEqual(activity[key],value,'Editorial drift: '+id+'.'+key);
 }
}
assert.equal(owners.size,activities.length,'Missing editorial source');
for(const a of activities){assert(a.limits.trim(),'Empty limits: '+a.id);assert(!a.limits.startsWith('I dati sono sintetici e il modello'),'Generic limits: '+a.id);assert(!limits.has(a.limits),'Repeated limits: '+a.id);limits.add(a.limits);}
for(const [file,expected]of moduleGuides())assert.equal(fs.readFileSync(file,'utf8'),expected,'Module guide drift: '+file);
const {archiveMembersCompared:members}=JSON.parse(execFileSync('python3',['scripts/labs/package-downloads.py','--check'],{encoding:'utf8'}));
const docs=[...fs.readdirSync('.').filter(f=>f.endsWith('.md')),...fs.readdirSync('docs').filter(f=>f.endsWith('.md')).map(f=>'docs/'+f),...read('content/catalogue.json').modules.map(m=>'moduli/'+m.id+'/README.md')];
for(const file of docs)for(const [,link]of fs.readFileSync(file,'utf8').matchAll(/\]\(([^)]+)\)/g)){
 if(link.includes('://')||link.startsWith('#'))continue;
 assert(fs.existsSync(path.resolve(path.dirname(file),link.split('#')[0])),'Broken documentation link: '+file+' → '+link);
}
assert(!fs.existsSync('scripts/labs/prepare-browser-qa.py'),'Obsolete browser preparer');
assert(!/function (?:modulePage|orbitalLabel|expeditionLinks)\b/.test(fs.readFileSync('src/app.js','utf8')),'Obsolete page implementation');
const report={version:read('package.json').version,status:'passed',activities:activities.length,specificLimits:limits.size,moduleGuides:28,documents:docs.length,archiveMembersCompared:members,checks:['editorial-single-owner','generated-catalogue','module-guides','download-membership-and-bytes','section-csv','documentation-links','obsolete-code-removal']};
fs.writeFileSync('qa/consistency.json',JSON.stringify(report,null,2)+'\n');
console.log('Consistency: '+activities.length+' activities, 28 guides, '+members+' archived source files and '+docs.length+' documents verified.');
