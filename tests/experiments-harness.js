import {compareMetrics} from './metrics-comparison.mjs';
document.querySelector('#start').addEventListener('click', async () => {
  const button=document.querySelector('#start'), status=document.querySelector('#status');
  const report=document.querySelector('#report'), list=document.querySelector('#results');
  button.disabled=true; list.innerHTML=''; let passed=0, failed=0; const results=[];
  const off=GeoREngine.subscribe(s => {status.textContent=s.text+' · '+(passed+failed)+' / '+GEO_LABS.activities.length;});
  try {
    for (const a of GEO_LABS.activities) {
      const p=Object.fromEntries(a.controls.map(c=>[c.key,c.value])), start=performance.now();
      let entry;
      try {
        const r=await GeoREngine.run(a,p);
        if (!r.figures?.length || !r.metrics?.length || !r.csv) throw Error('Risultati incompleti');
        r.figures.forEach(GeoSecurity.svg);
        const differences=compareMetrics(r.metrics, GEO_QA_BASELINES[a.id]?.metrics);
        entry={id:a.id, ok:differences.length===0, figures:r.figures.length, ms:Math.round(performance.now()-start), differences};
      } catch (err) {entry={id:a.id, ok:false, error:err.message, differences:[]};}
      results.push(entry);
      if(entry.ok) passed++; else failed++;
      const li=document.createElement('li'); li.className=entry.ok?'':'fail';
      li.textContent=a.id+' · '+(entry.ok?'OK · '+entry.figures+' SVG':'ERRORE · '+(entry.error||entry.differences.map(d=>d.name+': '+d.reason).join('; ')));
      list.append(li);
      report.textContent=JSON.stringify({passed,failed,total:GEO_LABS.activities.length,last:entry},null,2);
    }
  } finally {
    off(); status.textContent='COMPLETATO · '+passed+' superati · '+failed+' errori';
    report.textContent=JSON.stringify({comparisonVersion:2,passed,failed,results},null,2); button.disabled=false;
  }
});
