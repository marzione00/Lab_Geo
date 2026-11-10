/* Funzioni condivise dalla navigazione e dai controlli automatici. */
(function (root) {
  "use strict";
  const clean = s => String(s ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  function parseRoute(hash, modules) {
    const key = String(hash || "#indice").replace(/^#/, "");
    if (["indice", "mappa", "catalogo", "esperimenti", "progetti", "materiali", ""].includes(key)) return {type:key || "indice"};
    const match = /^modulo-(T00|M\d{2}|P\d{2})(?:\/(slide|codici)(?:\/(\d+))?)?$/.exec(key);
    if (!match) return {type:"notfound"};
    const mod = modules.find(m => m.id === match[1]);
    if (!mod) return {type:"notfound"};
    if (!match[2]) return {type:"module", id:mod.id};
    if (match[2] === "codici") return match[3] ? {type:"notfound"} : {type:"code", id:mod.id};
    const page = Number(match[3] || 3);
    return Number.isInteger(page) && page >= 1 && page <= mod.pages ? {type:"slide",id:mod.id,page} : {type:"notfound"};
  }
  function filterModules(modules, query="", category="tutti") {
    const terms=clean(query).split(/\s+/).filter(Boolean);
    return modules.filter(m => (category==="tutti" || m.category===category) && terms.every(t => clean([m.id,m.title,m.subtitle,...m.sections.map(s=>s.title),...(m.keywords||[])].join(" ")).includes(t)));
  }
  function loadProgress(storage) {
    try {
      const raw=storage.getItem("geostat-r6-progress") || "{}";if(raw.length>200000)return {done:[],last:null};
      const p=JSON.parse(raw);
      if (!p || typeof p!=="object" || Array.isArray(p)) return {done:[],last:null};
      return {done:Array.isArray(p.done)?[...new Set(p.done.slice(0,2000).filter(x=>/^(T00|M\d{2}|P\d{2}):\d+$/.test(x)))]:[],last:typeof p.last==="string"&&p.last.length<200?p.last:null};
    } catch { return {done:[],last:null}; }
  }
  function saveProgress(storage, p) {try {storage.setItem("geostat-r6-progress",JSON.stringify(p));return true;} catch{return false;}}
  root.GeoCore=Object.freeze({clean,parseRoute,filterModules,loadProgress,saveProgress});
})(globalThis);
