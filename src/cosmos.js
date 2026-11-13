/* A persistent decorative scene. Planet/map renderers retain their own geometry. */
(function(root){
 'use strict';
 const host=document.getElementById('deep-space');if(!host)return;
 const source=document.currentScript?.src||new URL('assets/cosmos.js',location.href).href;
 const reduced=root.matchMedia?.('(prefers-reduced-motion: reduce)');
 const canvas=document.createElement('canvas');canvas.setAttribute('aria-hidden','true');host.append(canvas);
 let ctx;try{ctx=canvas.getContext('2d');}catch{return;}
 if(!ctx||typeof ctx.createRadialGradient!=='function')return;
 let width=1,height=1,dpr=1,frame=0,last=0,time=0,paused=reduced?.matches||false;
 let px=0,py=0,tx=0,ty=0,texture=null,worker=null,request=0,resizeTimer=0,disposed=false;
 let seed=14783;const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
 const normal=()=>Math.sqrt(-2*Math.log(Math.max(.00001,random())))*Math.cos(Math.PI*2*random());
 const colors=['#b8d1ef','#d5e4f0','#e8c9a0','#a4d5e7'];
 const stars=Array.from({length:2100},()=>({x:random(),y:random(),z:.15+random()*.85,r:Math.pow(random(),4)*1.25+.19,a:random()*.65+.12,c:Math.floor(random()*4)}));
 const near=Array.from({length:30},()=>({x:random(),y:random(),z:1.3+random(),r:.7+random()*.75,a:.45+random()*.5,c:Math.floor(random()*4)}));
 const points=Array.from({length:12000},()=>{const r=Math.pow(random(),.72),arm=Math.floor(random()*3),a=r*8.8+arm*2.094395+normal()*(.17+.1*r);return{x:r*Math.cos(a),y:r*Math.sin(a),z:normal()*.018,a:.12+random()*.62,s:.25+random()*.72,r};});
 function glow(c,x,y,r,color,alpha=1){c.globalAlpha=alpha;const g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,color);g.addColorStop(1,'rgba(0,0,0,0)');c.fillStyle=g;c.fillRect(x-r,y-r,r*2,r*2);c.globalAlpha=1;}
 function galaxy(size,tilt){const image=document.createElement('canvas');image.width=image.height=size;const c=image.getContext('2d');c.translate(size/2,size/2);c.rotate(-.4);const r=size*.44;glow(c,0,0,r*.7,'rgba(80,117,176,.16)');for(const p of points){c.fillStyle=p.r<.17?`rgba(249,222,180,${p.a})`:`rgba(141,181,232,${p.a*.72})`;c.fillRect(p.x*r,(p.y*tilt+p.z)*r,p.s,p.s);}c.save();c.scale(1,tilt);glow(c,0,0,r*.3,'rgba(225,204,170,.5)');glow(c,0,0,r*.105,'rgba(255,237,206,.78)');c.restore();return image;}
 let galaxies;try{galaxies=[galaxy(440,.48),galaxy(320,.22)];}catch{return;}
 function star(s,bright){const x=((s.x*width+px*10*s.z+time*.32*s.z)%(width+30)+width+30)%(width+30)-15,y=s.y*height+py*6*s.z;ctx.globalAlpha=s.a;ctx.fillStyle=colors[s.c];ctx.beginPath();ctx.arc(x,y,s.r,0,Math.PI*2);ctx.fill();if(bright){glow(ctx,x,y,s.r*9,s.c===2?'rgba(233,181,120,.18)':'rgba(129,184,232,.23)',s.a);ctx.globalAlpha=.23*s.a;ctx.fillStyle=colors[s.c];ctx.fillRect(x-s.r*5,y-.22,s.r*10,.44);ctx.fillRect(x-.22,y-s.r*5,.44,s.r*10);}}
 function draw(){if(disposed)return;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);ctx.globalAlpha=1;if(texture)ctx.drawImage(texture,-18+px*7+Math.sin(time*.025)*2,-18+py*5,width+36,height+36);
  const scale=width<700?.6:1;
  [[.115,.77,270,-.38,.0004],[.88,.28,170,.48,-.00025]].forEach((v,i)=>{const size=Math.min(v[2]*scale,width*.3);ctx.save();ctx.translate(width*v[0]+px*2,height*v[1]+py*2);ctx.rotate(v[3]+time*v[4]);ctx.drawImage(galaxies[i],-size/2,-size/2,size,size);ctx.restore();});
  const count=width<700?900:stars.length;for(let i=0;i<count;i++)star(stars[i],false);for(const s of near)star(s,true);ctx.globalAlpha=1;
 }
 function tick(now){frame=0;if(disposed||document.hidden||paused){last=0;return;}if(!last)last=now;if(now-last>=65){time+=Math.min((now-last)/1000,.12);last=now;px+=(tx-px)*.08;py+=(ty-py)*.08;draw();}frame=requestAnimationFrame(tick);}
 function schedule(){cancelAnimationFrame(frame);frame=0;last=0;draw();if(!paused&&!document.hidden&&!disposed)frame=requestAnimationFrame(tick);}
 function paintNebula(){if(disposed||!worker)return;const ratio=Math.min(1,1600/width,1200/height);worker.postMessage({id:++request,width:Math.max(1,Math.round(width*ratio)),height:Math.max(1,Math.round(height*ratio))});}
 function resize(){width=Math.max(1,innerWidth);height=Math.max(1,innerHeight);dpr=Math.min(devicePixelRatio||1,1.5,2200/width);canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);draw();clearTimeout(resizeTimer);resizeTimer=setTimeout(paintNebula,180);}
 try{if(typeof Worker==='function'){worker=new Worker(new URL('cosmos-worker.js',source));worker.onmessage=({data:r})=>{if(disposed||r.id!==request)return;const c=document.createElement('canvas');c.width=r.width;c.height=r.height;const context=c.getContext('2d'),im=context.createImageData(r.width,r.height);im.data.set(new Uint8ClampedArray(r.pixels));context.putImageData(im,0,0);texture=c;host.dataset.ready='true';draw();};worker.onerror=()=>{worker?.terminate();worker=null;};}}catch{worker=null;}
 document.addEventListener('geospace:pause',e=>{paused=!!e.detail.paused;schedule();});
 document.addEventListener('visibilitychange',schedule);
 root.addEventListener('resize',resize);
 root.addEventListener('pointermove',e=>{if(paused||reduced?.matches||e.pointerType==='touch')return;tx=e.clientX/width-.5;ty=e.clientY/height-.5;},{passive:true});
 document.addEventListener('pointerleave',()=>{tx=ty=0;});
 root.addEventListener('pagehide',e=>{cancelAnimationFrame(frame);clearTimeout(resizeTimer);last=0;if(!e.persisted){disposed=true;worker?.terminate();texture=null;}});
 root.addEventListener('pageshow',()=>{if(!disposed)schedule();});
 root.GeoCosmos=Object.freeze({debug:()=>({ready:!!texture,paused,time,stars:width<700?930:2130,worker:!!worker})});
 resize();schedule();
})(window);
