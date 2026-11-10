import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import vm from "node:vm";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),".."),dist=path.join(root,"dist");
const exists=p=>{if(!fs.existsSync(path.join(dist,p)))throw Error("Risorsa assente: "+p);};
const ctx=vm.createContext({window:{}});
vm.runInContext(fs.readFileSync(path.join(dist,"assets/catalogue.js"),"utf8"),ctx);
const c=ctx.window.GEO_CATALOG;
let pages=0,visuals=0,labs=0;
for(const m of c.modules){
  exists(m.pdf);exists(m.script);
  vm.runInContext(fs.readFileSync(path.join(dist,"assets/content",m.id+".js"),"utf8"),ctx);
  const d=ctx.window.GEO_MODULES[m.id];if(d.slides.length!==m.pages)throw Error(m.id);
  for(const s of d.slides){pages++;exists(s.image);if(s.codePath)exists(s.codePath);if(s.figure||s.diagram){visuals++;if(s.figure)exists("assets/visuals/"+m.id+"/"+String(s.page).padStart(3,"0")+".svg");}}
  for(const l of d.laboratories){labs++;exists(l.path);}
}
for(const f of ["assets/mark.svg","assets/topography.svg","assets/lab.css","assets/app.js","vendor/mathjax/tex-svg.js","materiali/Guida_corso_R6.pdf","materiali/audit/Registro_slide_R6.html"])exists(f);
if(c.modules.length!==28||pages!==861||visuals!==494||labs!==360)throw Error("Copertura incompleta.");
const source=fs.readFileSync(path.join(dist,"index.html"),"utf8");if(source.includes("{{"))throw Error("Segnaposto non risolto.");
for(const match of source.matchAll(/(?:src|href)="([^"#]+)"/g)){if(!/^[a-z]+:/.test(match[1]))exists(match[1]);}
console.log("Distribuzione verificata: 28 fascicoli, 861 slide vettoriali, 494 pannelli visuali, 360 laboratori R/Python.");
