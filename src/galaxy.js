/* Galaxy navigation: presentation derives from the shared course/planet catalogues. */
(function(){
  'use strict';
  const positions={T00:[19,76],M01:[30,63],M02:[13,51],M03:[18,29],M04:[33,21],M05:[38,39],M06:[49,15],M07:[64,20],M08:[76,30],M09:[87,44],M10:[83,63],M11:[70,76],M12:[57,84],M13:[44,74],M14:[59,59],M15:[64,39],M16:[43,55]};
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let hoverTimer;
  const cleanup=()=>clearTimeout(hoverTimer);
  function mount(main){
    cleanup();
    const worlds=window.GeoPlanets, modules=window.GEO_CATALOG.modules;
    let selected='M01';
    const node=p=>'<button type="button" class="galaxy-node" data-destination="'+p.id+'" style="--gx:'+positions[p.id][0]+'%;--gy:'+positions[p.id][1]+'%;--world-color:'+p.atmosphere+'" aria-pressed="false" aria-controls="destination-detail" aria-label="'+esc(p.id+' · '+p.name+' · '+modules.find(m=>m.id===p.id).title)+'"><span class="galaxy-orbit"><span class="planet-slot '+(p.rings?'ringed':'')+'" data-planet="'+p.id+'" aria-hidden="true"></span></span><span class="galaxy-node-label"><small>'+p.id+'</small> '+esc(p.name)+'</span></button>';
    main.innerHTML='<section class="galaxy-home" aria-labelledby="galaxy-title"><div class="galaxy-heading"><div><p class="eyebrow">STATISTICA E CODING R / SCIENZE DELLA TERRA</p><h1 id="galaxy-title">La galassia del corso<span>.</span></h1><p>Ogni pianeta, un laboratorio. Scegli una destinazione e comincia a esplorare.</p></div><a class="galaxy-index" href="#catalogo">Indice dei moduli <span aria-hidden="true">↗</span></a></div><div class="galaxy-navigation"><div class="galaxy-chart" role="group" aria-label="Seleziona un pianeta del corso"><div class="galaxy-art" aria-hidden="true"></div><svg class="galaxy-grid" viewBox="0 0 1000 700" preserveAspectRatio="none" aria-hidden="true"><ellipse cx="500" cy="350" rx="390" ry="235"/><ellipse cx="500" cy="350" rx="275" ry="165"/><ellipse cx="500" cy="350" rx="150" ry="90"/><path d="M 500 30 V 670 M 40 350 H 960"/><path class="galaxy-course-route" d="'+worlds.planets.map(p=>positions[p.id]).map(([x,y],i)=>(i?'L':'M')+' '+x*10+' '+y*7).join(' ')+'"/><path id="galaxy-selected-route"/></svg>'+worlds.sectors.map((sector,i)=>'<span class="galaxy-region region-'+i+'">'+String(i+1).padStart(2,'0')+' / '+esc(sector)+'</span>').join('')+''+worlds.planets.map(node).join('')+'<div class="galaxy-map-caption"><span>'+worlds.planets.length+' DESTINAZIONI DISPONIBILI</span><span>MAPPA ILLUSTRATIVA · ROTTA LIBERA</span></div></div><aside id="destination-detail" class="destination-detail" aria-labelledby="destination-name"><div class="destination-signal"><span></span> DESTINAZIONE SELEZIONATA</div><div class="destination-portrait" aria-hidden="true"><div class="portrait-orbit"></div><div id="destination-planet" class="planet-slot" data-planet="M01"></div></div><p class="destination-sector" id="destination-sector"></p><h2 id="destination-name"></h2><p class="destination-type" id="destination-type"></p><div class="destination-subject"><h3 id="destination-title"></h3><p id="destination-description"></p></div><div class="destination-meta"><span><strong id="destination-count"></strong> esperimenti</span><span>R + ggplot2</span></div><a id="galaxy-travel" class="galaxy-travel" href="#modulo-M01">Viaggia <span aria-hidden="true">↗</span></a><p class="galaxy-help">Passa su un pianeta o selezionalo con un tocco. Premi Viaggia per aprire il modulo.</p><button class="galaxy-return" type="button">Scegli un altro pianeta ↑</button></aside></div><div class="galaxy-footer"><p><span class="galaxy-beacon"></span> '+window.GeoLabs.activities.length+' esperimenti interattivi <span class="galaxy-separator">/</span> R eseguito nel browser</p><a href="#progetti">Le '+Object.keys(window.GeoLabs.missions).length+' spedizioni applicative <span aria-hidden="true">→</span></a></div></section>';
    const get=id=>main.querySelector('#'+id);
    function select(id){
      cleanup();
      const p=worlds.byId[id],m=modules.find(x=>x.id===id); if(!p||!m)return;
      selected=id;
      main.querySelectorAll('[data-destination]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.destination===id)));
      get('destination-sector').textContent=p.sector+' / '+id;
      get('destination-name').textContent=p.name;
      get('destination-type').textContent=p.description;
      get('destination-title').textContent=m.title;
      get('destination-description').textContent=m.subtitle;
      get('destination-count').textContent=window.GeoLabs.count(id);
      get('galaxy-travel').setAttribute('href','#modulo-'+id);
      get('galaxy-travel').setAttribute('aria-label','Viaggia verso '+p.name+': '+m.title);
      const portrait=get('destination-planet');portrait.dataset.planet=id;portrait.classList.toggle('ringed',Boolean(p.rings));
      const [x,y]=positions[id];
      get('galaxy-selected-route').setAttribute('d','M '+x*10+' '+y*7+' L '+Math.min(970,x*10+65)+' '+(y*7-55)+' H 980');
      window.GeoSpace?.refresh();
    }
    main.querySelectorAll('[data-destination]').forEach(button=>{
      button.addEventListener('pointerenter',e=>{cleanup();if(e.pointerType!=='touch')hoverTimer=setTimeout(()=>{if(button.isConnected)select(button.dataset.destination);},180);});
      button.addEventListener('pointerleave',cleanup);
      button.addEventListener('focus',()=>select(button.dataset.destination));
      button.addEventListener('click',()=>{select(button.dataset.destination);if(window.matchMedia('(max-width: 540px)').matches)get('destination-detail').scrollIntoView({block:'nearest',behavior:'instant'});});
      button.addEventListener('keydown',e=>{
        const keys=['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End'];if(!keys.includes(e.key))return;
        e.preventDefault();e.stopPropagation();const nodes=[...main.querySelectorAll('[data-destination]')],i=nodes.indexOf(button);
        nodes[e.key==='Home'?0:e.key==='End'?nodes.length-1:(i+(e.key==='ArrowLeft'||e.key==='ArrowUp'?-1:1)+nodes.length)%nodes.length].focus();
      });
    });
    get('galaxy-travel').addEventListener('click',e=>{
      if(e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||!window.GeoSpace)return;
      e.preventDefault();window.GeoSpace.travel(selected,main.querySelector('[data-destination="'+selected+'"] .planet-slot'));
    });
    main.querySelector('.galaxy-return').addEventListener('click',()=>{const node=main.querySelector('[data-destination="'+selected+'"]');node.focus({preventScroll:true});main.querySelector('.galaxy-chart').scrollIntoView({block:'start',behavior:'instant'});});
    select(selected);
  }
  window.GeoGalaxy=Object.freeze({mount,cleanup});
})();
