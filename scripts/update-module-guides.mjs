import fs from 'node:fs';
import vm from 'node:vm';
import {pathToFileURL} from 'node:url';
const begin='<!-- BEGIN INTERACTIVE GUIDE -->', end='<!-- END INTERACTIVE GUIDE -->';
export function moduleGuides() {
  const data=JSON.parse(fs.readFileSync('content/experiments.json'));
  const context={window:{GEO_LABS:data,GeoREngine:{}}};
  vm.runInNewContext(fs.readFileSync('src/experiments.js','utf8'),context);
  const missions=context.window.GeoLabs.missions, byId=new Map(data.activities.map(a=>[a.id,a]));
  const result=new Map();
  for(const m of JSON.parse(fs.readFileSync('content/catalogue.json')).modules){
    let body='## Percorso interattivo\n\n';
    if(m.category==='progetti'){
      const mission=missions[m.id];body+=mission.intro+'\n\nLe tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.\n\n';
      for(const [title,...ids] of mission.steps){body+='### '+title+'\n\n';for(const id of ids){const a=byId.get(id);body+='- **'+a.title+'** — '+a.goal+' [Programma R](../../'+a.source+'); rotta del sito: `#laboratorio/'+id+'`.\n';}body+='\n';}
    }else{
      const activities=data.activities.filter(a=>a.module===m.id);
      body+=activities.length+' esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-'+m.id+'`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.\n\n| Esperimento | Domanda e operazione | Codice riproducibile |\n|---|---|---|\n';
      for(const a of activities)body+='| **'+a.title+'** · `#laboratorio/'+a.id+'` | '+a.goal.replaceAll('|','\\|')+' | [R](../../'+a.source+') |\n';
    }
    body+='\nOgni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.\n';
    const file='moduli/'+m.id+'/README.md', original=fs.readFileSync(file,'utf8');
    const clean=original.replace(new RegExp(begin+'[\\s\\S]*?'+end+'\\n*'),'');
    const insertion=clean.indexOf('\n\n',clean.indexOf('\n\n')+2)+2;
    result.set(file,clean.slice(0,insertion)+begin+'\n'+body+end+'\n\n'+clean.slice(insertion));
  }
  return result;
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href){for(const [file,text]of moduleGuides())fs.writeFileSync(file,text);console.log('28 module guides updated from the current catalogue and missions.');}
