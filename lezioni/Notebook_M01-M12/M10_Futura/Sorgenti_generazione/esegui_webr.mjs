// Esecuzione opzionale con Node >=18 e npm install webr@0.6.1.
// Eseguire dalla cartella M10_Futura: node Sorgenti_generazione/esegui_webr.mjs
// Il pacchetto WebR e le sue risorse vanno installati prima; gli HTML già prodotti
// sono interamente offline e non richiedono questo runtime.
import { WebR } from 'webr';
import { fileURLToPath } from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const w=new WebR({interactive:false});
await w.init();
await w.FS.mkdir('/project');
await w.FS.mount('NODEFS',{root},'/project');
try {
  await w.evalRVoid('setwd("/project")');
  const shelter=await new w.Shelter();
  const out=await shelter.captureR('source("Sorgenti_generazione/esegui_tutti.R",encoding="UTF-8")',
    {withAutoprint:true,captureStreams:true,captureConditions:true});
  for(const line of out.output??[]) console.log(line.type,line.data??line);
  if((out.output??[]).some(item=>item.type==="error"))
    throw new Error("Esecuzione R non riuscita: consultare Verifiche/esecuzione_blocchi.csv.");
  await shelter.purge();
} finally {w.close();}
