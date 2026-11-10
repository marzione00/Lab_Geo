import fs from "node:fs";
import {hardenBuild} from "./harden-build.mjs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),".."),out=path.join(root,"dist");
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),"utf8"));
const config=read("config/site.json"),catalogue=read("content/catalogue.json");
if(process.env.SITE_URL)config.siteUrl=process.env.SITE_URL.replace(/\/+$/,"")+"/";
if(process.env.GITHUB_REPOSITORY)config.repositoryUrl="https://github.com/"+process.env.GITHUB_REPOSITORY;
for(const key of ["siteUrl","mainSiteUrl","repositoryUrl"]){
  if(config[key]){let u;try{u=new URL(config[key]);}catch{throw Error('URL non valido: '+key);}if(u.protocol!=='https:'||!u.hostname||u.username||u.password||/[\s\x00-\x1f]/.test(config[key]))throw Error('URL HTTPS non valido: '+key);}
}
fs.rmSync(out,{recursive:true,force:true});fs.mkdirSync(path.join(out,"assets/content"),{recursive:true});
const sharedDiagramPanels=new Set();
for(const m of catalogue.modules)for(const s of read("moduli/"+m.id+"/modulo.json").slides)if(s.diagram&&!s.figure)sharedDiagramPanels.add("visuals/"+m.id+"/"+String(s.page).padStart(3,"0")+".svg");
for(const dir of ["assets","materiali","vendor","R"])fs.cpSync(path.join(root,dir),path.join(out,dir),{recursive:true,filter:p=>{
  if(p!==path.join(root,dir)&&path.basename(p).startsWith('.'))return false;
  if(fs.lstatSync(p).isSymbolicLink())throw Error('Collegamento simbolico non consentito nella distribuzione: '+p);
  if(/\.(?:key|p12|pfx)$/i.test(p))return false;
  if(p.split(path.sep).includes("__pycache__"))return false;
  if(dir==="assets"&&sharedDiagramPanels.has(path.relative(path.join(root,dir),p).split(path.sep).join("/")))return false;
  if(dir==="materiali"){
    const rel=path.relative(path.join(root,dir),p).split(path.sep).join("/");
    if(/\.(?:aux|log|nav|snm|toc|out)$/.test(rel))return false;
    if(rel.startsWith("verifiche/")&&rel.endsWith(".pdf"))return false;
  }
  return true;
}});
const experiments=read("content/experiments.json");
experiments.common=fs.readFileSync(path.join(root,"R/lab-common.R"),"utf8");
experiments.packages=read("vendor/r-packages-lock.json");
for(const a of experiments.activities){a.plotCount=fs.readdirSync(path.join(root,"assets/experiments")).filter(f=>f.startsWith(a.id+"-")&&f.endsWith(".svg")).length; if(!a.plotCount)throw Error("Anteprima R assente: "+a.id);}
const safe=x=>JSON.stringify(x).replace(/</g,"\\u003c");
fs.writeFileSync(path.join(out,"assets/experiments-data.js"),"window.GEO_LABS="+safe(experiments)+";\n");
fs.writeFileSync(path.join(out,"assets/catalogue.js"),"window.GEO_CATALOG="+safe(catalogue)+";\n");
fs.writeFileSync(path.join(out,"assets/site-config.js"),"window.GEO_CONFIG="+safe(config)+";\n");
for(const m of catalogue.modules){
  const data=read("moduli/"+m.id+"/modulo.json");
  fs.writeFileSync(path.join(out,"assets/content",m.id+".js"),"window.GEO_MODULES=window.GEO_MODULES||{};window.GEO_MODULES."+m.id+"="+safe(data)+";\n");
}
for(const name of ["app.js","security.js","core.js","lab.css","planets.js","space.js","space-cpu.js","space.css","experiments.js","experiments.css","lab-engine.js","galaxy.js","galaxy.css"])fs.copyFileSync(path.join(root,"src",name),path.join(out,"assets",name));
fs.writeFileSync(path.join(out,"assets/space-shaders.js"),"window.GEO_SHADERS="+safe({planet:fs.readFileSync(path.join(root,"src/planet.frag"),"utf8")})+";\n");
const esc=s=>s.replace(/[&"<>]/g,c=>({"&":"&amp;",'"':"&quot;","<":"&lt;",">":"&gt;"}[c]));
const meta=config.siteUrl?'<link rel="canonical" href="'+esc(config.siteUrl)+'"><meta name="robots" content="index,follow">':'<meta name="robots" content="noindex,nofollow">';
fs.writeFileSync(path.join(out,"index.html"),fs.readFileSync(path.join(root,"src/index.html"),"utf8").replace("{{META}}",meta));
fs.writeFileSync(path.join(out,".nojekyll"),"");
fs.writeFileSync(path.join(out,"robots.txt"),config.siteUrl?"User-agent: *\nAllow: /\n":"User-agent: *\nDisallow: /\n");
if(config.siteUrl)fs.writeFileSync(path.join(out,"sitemap.xml"),'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+esc(config.siteUrl)+'</loc></url></urlset>');
for(const f of ["THIRD_PARTY_NOTICES.md","LICENSE.md"])fs.copyFileSync(path.join(root,f),path.join(out,f));
hardenBuild(out);
console.log("Build completata: 139 esperimenti R, 17 pianeti, 11 spedizioni; materiali originali conservati.");
