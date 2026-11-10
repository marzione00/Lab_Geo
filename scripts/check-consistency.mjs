import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {inflateRawSync} from 'node:zlib';
import {moduleGuides} from './update-module-guides.mjs';
const read=file=>JSON.parse(fs.readFileSync(file,'utf8'));
const catalogue=read('content/experiments.json'), activities=catalogue.activities;
assert.equal(catalogue.version,read('package.json').version,'Application/catalogue version');
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
// The two generated download archives use ordinary ZIP, without ZIP64/encryption.
function checkArchive(file){
 const bytes=fs.readFileSync(file);let end=bytes.length-22;
 while(end>=Math.max(0,bytes.length-65557)&&bytes.readUInt32LE(end)!==0x06054b50)end--;
 assert(end>=0,'ZIP directory absent');const count=bytes.readUInt16LE(end+10);let pos=bytes.readUInt32LE(end+16),checked=0;
 for(let i=0;i<count;i++){
  assert.equal(bytes.readUInt32LE(pos),0x02014b50);
  const method=bytes.readUInt16LE(pos+10),size=bytes.readUInt32LE(pos+20),len=bytes.readUInt16LE(pos+28),extra=bytes.readUInt16LE(pos+30),comment=bytes.readUInt16LE(pos+32),offset=bytes.readUInt32LE(pos+42);
  const name=bytes.subarray(pos+46,pos+46+len).toString('utf8');pos+=46+len+extra+comment;
  assert(!path.isAbsolute(name)&&!name.split('/').includes('..'),'Invalid archive member');
  if(name==='LEGGIMI.txt')continue;
  assert(fs.existsSync(name)&&fs.statSync(name).isFile(),'Archive source absent: '+name);
  assert.equal(bytes.readUInt32LE(offset),0x04034b50);
  const start=offset+30+bytes.readUInt16LE(offset+26)+bytes.readUInt16LE(offset+28);
  assert(method===0||method===8,'Unsupported ZIP method');
  const data=method===8?inflateRawSync(bytes.subarray(start,start+size)):bytes.subarray(start,start+size);
  assert(data.equals(fs.readFileSync(name)),'Stale download: '+file+' / '+name);checked++;
 }
 return checked;
}
const archiveFiles=['assets/downloads/GeoStatLab_codice_dati_R6.zip','assets/downloads/GeoStatLab_esperimenti_R.zip'];
const members=archiveFiles.reduce((sum,file)=>sum+checkArchive(file),0);
const docs=[...fs.readdirSync('.').filter(f=>f.endsWith('.md')),...fs.readdirSync('docs').filter(f=>f.endsWith('.md')).map(f=>'docs/'+f),...read('content/catalogue.json').modules.map(m=>'moduli/'+m.id+'/README.md')];
for(const file of docs)for(const [,link]of fs.readFileSync(file,'utf8').matchAll(/\]\(([^)]+)\)/g)){
 if(link.includes('://')||link.startsWith('#'))continue;
 assert(fs.existsSync(path.resolve(path.dirname(file),link.split('#')[0])),'Broken documentation link: '+file+' → '+link);
}
assert(!fs.existsSync('scripts/labs/prepare-browser-qa.py'),'Obsolete browser preparer');
assert(!/function (?:modulePage|orbitalLabel|expeditionLinks)\b/.test(fs.readFileSync('src/app.js','utf8')),'Obsolete page implementation');
const report={version:read('package.json').version,status:'passed',activities:activities.length,specificLimits:limits.size,moduleGuides:28,documents:docs.length,archiveMembersCompared:members,checks:['editorial-single-owner','generated-catalogue','module-guides','download-bytes','documentation-links','obsolete-code-removal']};
fs.writeFileSync('qa/consistency.json',JSON.stringify(report,null,2)+'\n');
console.log('Consistency: '+activities.length+' activities, 28 guides, '+members+' archived source files and '+docs.length+' documents verified.');
