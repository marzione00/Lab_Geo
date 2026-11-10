import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {compareMetrics} from './metrics-comparison.mjs';
const row=(name,value)=>({grandezza:name,valore:value});
const baseline=[row('A','1'),row('B','2')];
test('Comparison rejects missing, extra, renamed and duplicate metrics',()=>{
  for(const actual of [[row('A','1')],[...baseline,row('C','3')],[row('OTHER','1'),row('B','2')]]) assert(compareMetrics(actual,baseline).length);
  for(const actual of [[],[row('A',1),row('A',1)],null,[{grandezza:'A'}]]) assert.throws(()=>compareMetrics(actual,baseline));
  assert.throws(()=>compareMetrics(baseline,undefined));
});
test('Comparison rejects invalid numeric values, type changes and unequal text',()=>{
  for(const v of ['non disponibile','',null,false,'NaN','Infinity']) assert(compareMetrics([row('A',v)],[row('A',1)]).length);
  for(const v of [NaN,Infinity,undefined,{},'1e999']) assert.throws(()=>compareMetrics([row('A',v)],[row('A',1)]));
  for(const [a,b] of [['TRUE','FALSE'],['hash1','hash2'],[null,'NA'],[false,'FALSE']]) assert(compareMetrics([row('A',a)],[row('A',b)]).length);
});
test('Comparison matches names, numeric formatting and the documented tolerance',()=>{
  assert.deepEqual(compareMetrics([row('B',2),row('A',' 1.0 ')],baseline),[]);
  assert.deepEqual(compareMetrics([row('A',.000009)],[row('A',0)]),[]);
  assert(compareMetrics([row('A',1.1)],[row('A',1)]).length);
  for(const v of [null,false,'NA','TRUE']) assert.deepEqual(compareMetrics([row('A',v)],[row('A',v)]),[]);
  for(const file of fs.readdirSync('assets/experiments').filter(f=>f.endsWith('.json'))){const m=JSON.parse(fs.readFileSync('assets/experiments/'+file)).metrics;assert.deepEqual(compareMetrics(m,m),[],file);}
});
test('Browser harness counts structural and numerical differences as failures',async()=>{
  for(const [i,metrics] of [[row('A',1)],[row('A','missing'),row('B',2)],[row('RENAMED',1),row('B',2)],[row('A',9),row('B',2)]].entries()){
    let run;const elements=Object.fromEntries(['#start','#status','#report','#results'].map(k=>[k,{addEventListener:(_,fn)=>run=fn,append:()=>{},textContent:''}]));
    const values={document:{querySelector:k=>elements[k],createElement:()=>({})},GeoREngine:{subscribe:()=>()=>{},run:async()=>({figures:['<svg/>'],csv:'x\n1',metrics})},GeoSecurity:{svg:()=>{}},GEO_LABS:{activities:[{id:'regression',controls:[]}]},GEO_QA_BASELINES:{regression:{metrics:baseline}}};
    try{Object.assign(globalThis,values);await import('./experiments-harness.js?regression='+i);await run();const result=JSON.parse(elements['#report'].textContent);assert.equal(result.passed,0);assert.equal(result.failed,1);assert.equal(result.results[0].ok,false);assert(result.results[0].differences.length);}
    finally{for(const key of Object.keys(values))delete globalThis[key];}
  }
});
