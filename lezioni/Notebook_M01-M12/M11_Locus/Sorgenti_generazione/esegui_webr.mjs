// Opzionale: Node, WebR0.6.1 e libreria sf WASM preparata prima dell'analisi.
// Uso: node Sorgenti_generazione/esegui_webr.mjs /percorso/libreria_webr_sf
// Per un computer ordinario si raccomanda R nativo con sf installato.
import { WebR } from 'webr';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const sfLibrary=process.argv[2];
if(!sfLibrary)throw new Error('Indicare una libreria sf compilata per WebR, oppure usare R/esegui_notebook.R con R nativo.');
const root=fileURLToPath(new URL('../',import.meta.url));
const w=new WebR({interactive:false});await w.init();
try{
 await w.FS.mkdir('/project');await w.FS.mount('NODEFS',{root},'/project');
 await w.FS.mkdir('/persistlib');await w.FS.mount('NODEFS',{root:path.resolve(sfLibrary)},'/persistlib');
 await w.evalRVoid('.libPaths(c("/persistlib",.libPaths()));setwd("/project")');
 const sh=await new w.Shelter();
 const cap=await sh.captureR('source("Sorgenti_generazione/esegui_tutti.R",encoding="UTF-8")',
   {withAutoprint:true,captureStreams:true,captureConditions:true});
 for(const o of cap.output??[])console.log(o.type,o.data??o);
 if((cap.output??[]).some(o=>o.type==='error'))throw new Error('Esecuzione R non riuscita: leggere Verifiche/esecuzione_blocchi.csv.');
 await sh.purge();
}finally{w.close();}
