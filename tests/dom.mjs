/* Prova del DOM virtuale e di tutte le formule; non sostituisce Chromium/CSP. */
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import {fileURLToPath} from "node:url";
const {JSDOM,ResourceLoader,VirtualConsole}=await import(process.env.JSDOM_MODULE||"jsdom");
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),".."),dist=path.join(root,"dist");
const errors=[];
class LocalResources extends ResourceLoader{
  fetch(url){
    const u=new URL(url);if(u.origin!=="https://geostat.test"){errors.push("Richiesta esterna: "+url);return null;}
    const f=path.resolve(dist,"."+u.pathname);if(!f.startsWith(dist+path.sep)||!fs.existsSync(f)){errors.push("Risorsa assente: "+u.pathname);return null;}
    return Promise.resolve(fs.readFileSync(f));
  }
}
const vc=new VirtualConsole();vc.on("jsdomError",e=>errors.push(e.message));
const dom=new JSDOM(fs.readFileSync(path.join(dist,"index.html"),"utf8"),{url:"https://geostat.test/#catalogo",runScripts:"dangerously",resources:new LocalResources(),pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};w.matchMedia=()=>({matches:false});const gl=new Proxy({getShaderParameter:()=>true,getProgramParameter:()=>true,getUniformLocation:(_,n)=>n,getAttribLocation:()=>0},{get:(o,k)=>k in o?o[k]:k.toUpperCase()===k?1:()=>({})});w.HTMLCanvasElement.prototype.getContext=()=>gl;w.Image=class{set src(v){this.width=2048;this.height=1024;setTimeout(()=>this.onload(),0);}};}});
const w=dom.window,d=w.document;
async function until(fn){for(let i=0;i<1000;i++){if(fn())return;await new Promise(r=>setTimeout(r,10));}throw Error("Timeout nel DOM virtuale.");}
await until(()=>d.querySelectorAll(".module-card").length===28);
const snapshots=process.env.SNAPSHOTS_DIR;
function snapshot(name){if(snapshots){fs.mkdirSync(snapshots,{recursive:true});fs.writeFileSync(path.join(snapshots,name+".html"),dom.serialize());}}
snapshot("indice");
d.getElementById("cerca-moduli").value="P11";d.getElementById("cerca-moduli").dispatchEvent(new w.Event("input"));
assert.equal(d.querySelectorAll(".module-card").length,1);
d.querySelector('[data-filter="moduli"]').click();assert.equal(d.querySelectorAll(".module-card").length,0);
const catalog=w.GEO_CATALOG.modules;
w.location.hash='#mappa';await until(()=>d.querySelectorAll('.world-card').length===17);
d.querySelector('[data-sector="Inferenza"]').click();assert.equal(d.querySelectorAll('.world-card').length,4);
assert([...d.querySelectorAll('.world-card')].every(a=>a.href.includes('modulo-M0')));
d.querySelector('[data-sector="all"]').click();assert.equal(d.querySelectorAll('.world-card').length,17);
await until(()=>w.GeoSpace.debug().ready);assert.equal(w.GeoSpace.debug().paused,false);
for(const m of catalog){w.location.hash="#modulo-"+m.id;await until(()=>d.querySelector(".lab-module-header h1")?.textContent===m.title);if(m.category==='progetti')assert.equal(d.querySelectorAll(".mission-stage").length,3);else assert.equal(d.querySelectorAll(".experiment-card").length,w.GeoLabs.count(m.id));}
snapshot("modulo");
w.location.hash="#modulo-P11/slide/10";await until(()=>d.querySelector("#tab-testo"));
assert.equal(w.GeoSpace.debug().paused,false);assert.equal(d.querySelector('[data-planet]').dataset.planet,'P11');
d.getElementById('motion-toggle').click();assert.equal(w.GeoSpace.debug().paused,true);d.getElementById('motion-toggle').click();assert.equal(w.GeoSpace.debug().paused,false);
d.querySelector("#tab-testo").click();await until(()=>d.querySelector("mjx-container[jax=SVG]"));
assert.equal(d.querySelectorAll('[data-mml-node="merror"]').length,0);snapshot("formule");
d.getElementById("mark-done").click();assert.equal(d.getElementById("mark-done").getAttribute("aria-pressed"),"true");
assert(w.localStorage.getItem("geostat-r6-progress").includes("P11:10"));
w.location.hash="#modulo-T00/codici";await until(()=>d.getElementById("select-code"));
d.getElementById("select-code").value="T00_PY_N01";d.getElementById("select-code").dispatchEvent(new w.Event("change"));
assert(d.getElementById("download-code").href.endsWith("T00_N01.py"));assert(d.getElementById("current-code").textContent.includes("import"));
w.location.hash="#modulo-M05/slide/105";await until(()=>d.querySelector(".page-counter")?.textContent==="105 / 105");assert(d.querySelector('[data-step="1"]').disabled);
w.location.hash="#modulo-M05/slide/106";await until(()=>d.querySelector(".error h1")?.textContent==="Pagina non trovata");
let formulas=0;
for(const m of catalog){
 const data=JSON.parse(fs.readFileSync(path.join(root,"moduli",m.id,"modulo.json"),"utf8"));
 for(const s of data.slides){
  const inputs=[s.formula,s.formulaAside].filter(Boolean).map(t=>"\\begin{gathered}"+t+"\\end{gathered}");
  for(const field of ["body","aside","caption","recall"]){for(const match of (s[field]||"").matchAll(/\$([^$]+)\$/g))inputs.push(match[1]);}
  for(const tex of inputs){
   let timer;
   const node=await Promise.race([w.MathJax.tex2svgPromise(tex,{display:true}),new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(m.id+" p."+s.page+" "+tex+" "+JSON.stringify(errors))),2500);})]);
   clearTimeout(timer);
   const problem=node.querySelector('[data-mml-node="merror"]');
   assert(!problem,m.id+" p."+s.page+": "+tex+" "+problem?.textContent);formulas++;
  }
 }
}
let labFormulas=0;
for(const a of w.GEO_LABS.activities){
 const inputs=[a.formula];
 for(const field of [a.symbols,...a.prose])for(const match of (field||'').matchAll(/\$([^$]+)\$/g))inputs.push(match[1]);
 for(const tex of inputs){let node;try{node=await w.MathJax.tex2svgPromise(tex,{display:true});}catch(err){throw new Error(a.id+': '+tex+' · '+err.message);}const problem=node.querySelector('[data-mml-node="merror"]');assert(!problem,a.id+': '+tex+' '+problem?.textContent);labFormulas++;}
}
assert.deepEqual(errors,[]);
const result={esito:"superato",ambiente:"jsdom 26.1.0; DOM virtuale, senza verifica CSS/CSP del browser",moduli:28,laboratori_T00_R_e_Python:40,formule_verificate:formulas,formule_esperimenti:labFormulas,errori:errors};
fs.mkdirSync(path.join(root,"qa"),{recursive:true});fs.writeFileSync(path.join(root,"qa/dom.json"),JSON.stringify(result,null,2));
console.log(labFormulas+" espressioni dei laboratori verificate.");
console.log("DOM virtuale: 28 moduli e "+formulas+" espressioni matematiche verificati.");
w.close();
