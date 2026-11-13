(function(){
 'use strict';
 let canvas=document.getElementById('space-canvas');const pause=document.getElementById('motion-toggle');
 const flightLayer=document.getElementById('flight-layer'),flightTitle=document.getElementById('flight-title');
 const reduced=window.matchMedia?window.matchMedia('(prefers-reduced-motion: reduce)'):{matches:false};
 let gl,cpu,program,locations,ready=false,failed=false,paused=reduced.matches,frame=0,last=0,time=0,flight=null;
 let width=1,height=1,dpr=1,slots=[],currentId='M01',currentType='indice',flightTimer=0;
 const planet=window.GeoPlanets.byId;
 const rgb=hex=>[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255);
 const colors=Object.fromEntries(Object.values(planet).map(p=>[p.id,[rgb(p.land),rgb(p.deep),rgb(p.high),rgb(p.atmosphere)]]));
 const ease=t=>t*t*(3-2*t),mix=(a,b,t)=>a+(b-a)*t;
 function compile(type,text){const s=gl.createShader(type);gl.shaderSource(s,text);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;}
 function geometry(el){const r=el.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2,r:Math.min(r.width,r.height)/2,hero:Number(el.dataset.hero||0)};}
 function drawPlanet(p,g,opacity=1,angleOffset=0){
  if(!p||g.r<1)return;
  if(cpu){if(g.y+g.r*2>0&&g.y-g.r*2<height&&g.x+g.r*2>0&&g.x-g.r*2<width)cpu.paint(p,g,time,opacity,angleOffset);return;}
  const extent=g.r*(p.rings?2.08:1.13),x=Math.max(0,Math.floor((g.x-extent)*dpr)),y=Math.max(0,Math.floor((height-g.y-extent)*dpr));
  const right=Math.min(canvas.width,Math.ceil((g.x+extent)*dpr)),top=Math.min(canvas.height,Math.ceil((height-g.y+extent)*dpr));
  if(right<=x||top<=y)return;
  gl.scissor(x,y,right-x,top-y);
  gl.uniform2f(locations.uCenter,g.x*dpr,g.y*dpr);gl.uniform1f(locations.uRadius,g.r*dpr);
  gl.uniform1f(locations.uAngle,p.phase-time*p.speed+angleOffset);gl.uniform1f(locations.uKind,p.kind);
  gl.uniform1f(locations.uSeed,p.seed);gl.uniform1f(locations.uTilt,p.tilt);gl.uniform1f(locations.uRings,p.rings?1:0);
  gl.uniform1f(locations.uHero,g.hero||0);gl.uniform1f(locations.uOpacity,opacity);
  ['uLand','uDeep','uHigh','uAtmosphere'].forEach((key,i)=>gl.uniform3fv(locations[key],colors[p.id][i]));
  gl.drawArrays(gl.TRIANGLES,0,6);
 }
 function render(now){
  if(!ready||failed)return;
  if(cpu)cpu.clear(canvas.width,canvas.height,dpr);
  else{gl.viewport(0,0,canvas.width,canvas.height);gl.disable(gl.SCISSOR_TEST);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.enable(gl.SCISSOR_TEST);gl.uniform2f(locations.uResolution,canvas.width,canvas.height);gl.uniform1f(locations.uTime,time);}
  if(flight){
   const t=Math.min(1,(now-flight.started)/flight.duration),e=ease(t);
   const landing=document.querySelector('.module-planet[data-planet="'+flight.id+'"]');
   const target=landing?geometry(landing):{x:width*.82,y:height*.72,r:Math.min(width*.46,height*.66),hero:.6};
   if(flight.previous&&t<.55){const old={x:width*.83-e*width*1.2,y:height*.79,r:Math.min(width*.44,height*.65)*(1-e*.4),hero:.15};drawPlanet(planet[flight.previous],old,1-ease(Math.min(1,t/.55)));}
   const g={x:mix(flight.from.x,target.x,e),y:mix(flight.from.y,target.y,e),r:mix(flight.from.r,target.r,e),hero:mix(flight.from.hero,target.hero,e)};
   drawPlanet(planet[flight.id],g,Math.min(1,t*5+.2));
  }else{
   for(const el of slots){if(!el.isConnected||el.closest('[hidden]'))continue;const p=planet[el.dataset.planet];if(!p)continue;const g=geometry(el);drawPlanet(p,g);
    if(p.moon&&g.r>130){const lunar={...p,id:p.id,kind:1,rings:false,seed:p.seed+20,phase:.4};drawPlanet(lunar,{x:g.x-g.r*.91,y:g.y-g.r*.55,r:g.r*.09,hero:0},.9,.5);}
   }
  }
 }
 function tick(now){frame=0;if(document.hidden||!canvas.isConnected){last=0;return;}if(!last)last=now;
  if(now-last>=32){if(!paused)time+=Math.min((now-last)/1000,.12);last=now;render(now);}
  if(ready&&(!paused||flight))frame=requestAnimationFrame(tick);
 }
 function schedule(){if(frame)cancelAnimationFrame(frame);frame=0;last=0;render(performance.now());if(ready&&(!paused||flight)&&!document.hidden)frame=requestAnimationFrame(tick);}
 function resize(){width=Math.max(1,window.innerWidth);height=Math.max(1,window.innerHeight);dpr=Math.min(window.devicePixelRatio||1,1.5,1800/width);canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);render(performance.now());}
 function syncPause(){pause.textContent=paused?'Riprendi rotazione':'Pausa rotazione';pause.setAttribute('aria-pressed',String(paused));document.dispatchEvent(new CustomEvent("geospace:pause",{detail:{paused}}));schedule();}
 function refresh(){slots=[...document.querySelectorAll('[data-planet]')];render(performance.now());}
 function cancelFlight(){clearTimeout(flightTimer);flight=null;document.body.classList.remove('in-flight');flightLayer.hidden=true;schedule();}
 function finishFlight(){if(!flight)return;const id=flight.id;cancelFlight();if(location.hash!=='#modulo-'+id)location.hash='#modulo-'+id;refresh();document.getElementById('contenuto').focus({preventScroll:true});document.getElementById('annuncio').textContent='Arrivo: '+id+' · '+planet[id].name;}
 function travel(id,origin){
  if(!planet[id]||(id===currentId&&currentType!=='indice')||paused||reduced.matches||!ready){location.hash='#modulo-'+id;return;}
  cancelFlight();const from=origin?geometry(origin):{x:width*1.3,y:height*.63,r:60,hero:0};
  flight={id,from,previous:currentType==='module'||currentType==='slide'||currentType==='code'?currentId:null,started:performance.now(),duration:1450};
  document.body.classList.add('in-flight');flightTitle.textContent=id+' / '+planet[id].name;
  document.getElementById('flight-subtitle').textContent=window.GEO_CATALOG.modules.find(m=>m.id===id)?.title||'';
  flightLayer.hidden=false;document.getElementById('annuncio').textContent='In viaggio verso '+flightTitle.textContent;
  flightTimer=setTimeout(finishFlight,1450);location.hash='#modulo-'+id;document.getElementById('skip-flight').focus({preventScroll:true});schedule();
 }
 function onRoute(route){if(flight&&(route.id!==flight.id||route.type!=='module'))cancelFlight();currentType=route.type;if(route.id)currentId=route.id;else if(route.type==='indice')currentId='M01';document.body.dataset.page=route.type;document.body.dataset.world=currentId;refresh();}
 async function fallback(err){
  if(!cpu){try{const next=canvas.cloneNode(false);canvas.replaceWith(next);canvas=next;cpu=window.GeoCPU.create(canvas);await cpu.ready;ready=true;failed=false;canvas.hidden=false;pause.disabled=false;document.body.dataset.space='canvas';refresh();resize();syncPause();return;}catch(error){console.warn('GeoStat: rendering non disponibile.',error);}}
  failed=true;ready=false;canvas.hidden=true;pause.disabled=true;pause.textContent='Vista essenziale';document.body.classList.add('space-fallback');console.warn('GeoStat: grafica non disponibile.',err);
 }
 async function initialize(){try{
  gl=canvas.getContext('webgl',{alpha:true,antialias:false,depth:false,premultipliedAlpha:false,powerPreference:'low-power'});
  if(!gl){await fallback('WebGL non disponibile');return;}
  program=gl.createProgram();const vs=compile(gl.VERTEX_SHADER,'attribute vec2 aPosition;void main(){gl_Position=vec4(aPosition,0.,1.);}'),fs=compile(gl.FRAGMENT_SHADER,window.GEO_SHADERS.planet);
  gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));
  gl.useProgram(program);gl.deleteShader(vs);gl.deleteShader(fs);const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
  const pos=gl.getAttribLocation(program,'aPosition');gl.enableVertexAttribArray(pos);gl.vertexAttribPointer(pos,2,gl.FLOAT,false,0,0);
  locations={};['uResolution','uCenter','uRadius','uAngle','uTime','uKind','uSeed','uTilt','uRings','uOpacity','uHero','uLand','uDeep','uHigh','uAtmosphere'].forEach(n=>locations[n]=gl.getUniformLocation(program,n));
  const names=['Day','Surface','Night'];const images=await Promise.all(names.map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error('Texture '+name+' non disponibile'));im.src='assets/space/'+name.toLowerCase()+'.webp';})));
  images.forEach((im,i)=>{const t=gl.createTexture();gl.activeTexture(gl.TEXTURE0+i);gl.bindTexture(gl.TEXTURE_2D,t);gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,im);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.REPEAT);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.uniform1i(gl.getUniformLocation(program,'u'+names[i]),i);});
  gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);ready=true;failed=false;canvas.hidden=false;pause.disabled=false;document.body.classList.remove('space-fallback');document.body.dataset.space='ready';refresh();resize();syncPause();
 }catch(e){fallback(e);}}
 document.addEventListener('click',event=>{const a=event.target.closest('a[href]');if(!a||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||a.target||a.hasAttribute('download'))return;const match=/^#modulo-(T00|M\d{2}|P\d{2})$/.exec(a.getAttribute('href'));if(!match||!planet[match[1]])return;event.preventDefault();travel(match[1],a.querySelector('[data-planet]')||a.closest('[data-world-card]')?.querySelector('[data-planet]'));});
 pause.addEventListener('click',()=>{paused=!paused;syncPause();});
 document.getElementById('skip-flight').addEventListener('click',finishFlight);
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&flight){e.preventDefault();finishFlight();}});
 window.addEventListener('resize',resize);window.addEventListener('scroll',()=>{if(paused)render(performance.now());},{passive:true});
 document.addEventListener('visibilitychange',()=>{if(document.hidden&&flight)finishFlight();schedule();});
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();fallback('Contesto grafico perso');});canvas.addEventListener('webglcontextrestored',initialize);
 window.GeoSpace=Object.freeze({refresh,onRoute,travel,debug:()=>({renderer:cpu?'canvas':'webgl',ready,failed,paused,time,currentId,currentType,flight:flight?.id,visibleWorlds:slots.filter(x=>x.isConnected).map(x=>x.dataset.planet)})});
 initialize();
})();
