// Opzionale: Node, WebR0.6.1 e libreria terra WASM preparata prima dell'analisi.
// Uso: node Sorgenti_generazione/esegui_webr.mjs /percorso/libreria_webr_terra
// Per un computer ordinario si raccomanda R nativo con terra installato.
import { WebR } from 'webr';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const terraLibrary=process.argv[2];
if(!terraLibrary)throw new Error('Indicare una libreria terra compilata per WebR, oppure usare R/esegui_notebook.R con R nativo.');
const root=fileURLToPath(new URL('../',import.meta.url));
const w=new WebR({interactive:false});await w.init();
try{
 await w.FS.mkdir('/project');await w.FS.mount('NODEFS',{root},'/project');
 await w.FS.mkdir('/persistlib');await w.FS.mount('NODEFS',{root:path.resolve(terraLibrary)},'/persistlib');
 await w.evalRVoid('.libPaths(c("/persistlib",.libPaths()));setwd("/project")');
 const sh=await new w.Shelter();
 const cap=await sh.captureR('source("Sorgenti_generazione/esegui_tutti.R",encoding="UTF-8")',
   {withAutoprint:true,captureStreams:true,captureConditions:true});
 for(const o of cap.output??[])console.log(o.type,o.data??o);
 if((cap.output??[]).some(o=>o.type==='error'))throw new Error('Esecuzione R non riuscita: leggere Verifiche/esecuzione_blocchi.csv.');
 await sh.purge();
}finally{w.close();}
