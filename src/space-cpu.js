/* Orthographic sphere renderer for browsers without WebGL.
   Texture coordinates rotate on a sphere; lighting and the limb remain fixed. */
(function(root){
 'use strict';
 const TAU=Math.PI*2;
 function create(canvas){
  const ctx=canvas.getContext('2d',{alpha:true}),textures=new Map(),pending=new Set(),cache=new Map();
  if(!ctx)throw Error('Canvas 2D non disponibile');
  let cloud=null,night=null;
  function load(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const x=c.getContext('2d',{willReadFrequently:true});x.drawImage(im,0,0);resolve({w:c.width,h:c.height,p:x.getImageData(0,0,c.width,c.height).data});};im.onerror=reject;im.src=src;});}
  function texture(id){if(textures.has(id))return textures.get(id);if(!pending.has(id)){pending.add(id);load('assets/space/'+(id==='M01'?'day':'p-'+id)+'.webp').then(t=>{textures.set(id,t);window.GeoSpace?.refresh();}).catch(()=>pending.delete(id));}return null;}
  function projection(p,res,hero){
   const key=p.id+':'+res+':'+hero;if(cache.has(key))return cache.get(key);
   const c=document.createElement('canvas');c.width=res;c.height=res;const x=c.getContext('2d');const im=x.createImageData(res,res);
   const indices=[],uv=[],lights=[],rims=[],specs=[];
   const axis=-p.tilt,ca=Math.cos(axis),sa=Math.sin(axis),cx=Math.cos(-.24),sx=Math.sin(-.24);
   let lx=hero?-.42:-.6,ly=hero?.84:.65,lz=hero?-.36:.8;let len=Math.hypot(lx,ly,lz);lx/=len;ly/=len;lz/=len;
   const hx=lx,hy=ly,hz=lz+1,hn=Math.hypot(hx,hy,hz);
   for(let y=0;y<res;y++)for(let xx=0;xx<res;xx++){
    const nx=(xx+.5)/res*2-1,ny=1-(y+.5)/res*2,d=nx*nx+ny*ny;if(d>=1)continue;
    const nz=Math.sqrt(1-d),qx=ca*nx-sa*ny,qy=sa*nx+ca*ny,qz=nz;
    const yy=cx*qy-sx*qz,zz=sx*qy+cx*qz;
    const pixel=(y*res+xx)*4;indices.push(pixel);im.data[pixel+3]=Math.min(255,(1-Math.sqrt(d))*res*.5*255);uv.push(.5-Math.atan2(zz,qx)/TAU,.5-Math.asin(Math.max(-1,Math.min(1,yy)))/Math.PI);
    const lit=nx*lx+ny*ly+nz*lz;lights.push(lit);
    rims.push(Math.pow(1-nz,4.2)*(.03+Math.max(0,lit)*.4));
    specs.push(Math.pow(Math.max(0,(nx*hx+ny*hy+nz*hz)/hn),100)*.5);
   }
   const result={c,x,im,indices:new Uint32Array(indices),uv:new Float32Array(uv),lights:new Float32Array(lights),rims:new Float32Array(rims),specs:new Float32Array(specs)};
   if(cache.size>50)cache.delete(cache.keys().next().value);cache.set(key,result);return result;
  }
  function paint(p,g,time,opacity=1,offset=0){
   const tex=texture(p.id);if(!tex)return;
   const res=g.r>170?512:g.r>90?224:144,hero=g.hero>.4?1:0;
   const a=projection(p,res,hero),out=a.im.data,angle=p.phase-time*p.speed+offset,shift=angle/TAU;
   const atm=[1,3,5].map(i=>parseInt(p.atmosphere.slice(i,i+2),16));
   for(let i=0;i<a.indices.length;i++){
    const v=a.uv[i*2+1],flow=(p.kind===4||p.kind===10)?time*.004*(1-2*v)/TAU:0;
    const u=(a.uv[i*2]+shift+flow)%1,un=u<0?u+1:u,idx=(Math.min(tex.h-1,Math.floor(v*tex.h))*tex.w+Math.min(tex.w-1,Math.floor(un*tex.w)))*4;
    let r=tex.p[idx],gg=tex.p[idx+1],b=tex.p[idx+2],light=a.lights[i],shade=.12+Math.max(0,light)*.91;
    if(p.kind===14&&r>gg*1.8&&r>100){shade=Math.max(.8,shade);}
    let rr=r*shade,gc=gg*shade,bb=b*shade;
    if(p.kind===0&&cloud){
     const cu=(a.uv[i*2]+(angle*1.012+.04)/TAU)%1,cv=cu<0?cu+1:cu;
     const ci=(Math.min(cloud.h-1,Math.floor(v*cloud.h))*cloud.w+Math.min(cloud.w-1,Math.floor(cv*cloud.w)))*4;
     const cl=Math.max(0,Math.min(.88,(cloud.p[ci+2]/255-.2)/.72))*.88;
     const white=255*(.07+Math.max(0,light)*.86);
     rr=rr*(1-cl)+white*.88*cl;gc=gc*(1-cl)+white*.94*cl;bb=bb*(1-cl)+white*cl;
     const water=1-cloud.p[(Math.min(cloud.h-1,Math.floor(v*cloud.h))*cloud.w+Math.min(cloud.w-1,Math.floor(un*cloud.w)))*4+1]/255;
     const spec=a.specs[i]*water*(1-cl)*150;rr+=spec;gc+=spec;bb+=spec;
     if(light<.08&&night){const ni=(Math.min(night.h-1,Math.floor(v*night.h))*night.w+Math.min(night.w-1,Math.floor(un*night.w)))*4,nf=Math.min(1,(.08-light)*5);rr+=night.p[ni]*nf*.65;gc+=night.p[ni+1]*nf*.65;bb+=night.p[ni+2]*nf*.65;}
    }
    if(p.kind===14&&r>gg*1.8&&r>100){rr*=1.3;gc*=1.4;bb*=1.5;}
    const o=a.indices[i],rim=a.rims[i];out[o]=Math.min(255,rr+atm[0]*rim);out[o+1]=Math.min(255,gc+atm[1]*rim);out[o+2]=Math.min(255,bb+atm[2]*rim);
   }
   a.x.putImageData(a.im,0,0);ctx.save();ctx.globalAlpha=opacity;
   const glow=ctx.createRadialGradient(g.x,g.y,g.r*.98,g.x,g.y,g.r*1.095);glow.addColorStop(0,p.atmosphere+'77');glow.addColorStop(.16,p.atmosphere+'35');glow.addColorStop(1,p.atmosphere+'00');ctx.fillStyle=glow;ctx.beginPath();ctx.arc(g.x,g.y,g.r*1.1,0,TAU);ctx.fill();
   if(hero){const sunx=g.x-g.r*.452,suny=g.y-g.r*.905,sun=ctx.createRadialGradient(sunx,suny,0,sunx,suny,g.r*.07);sun.addColorStop(0,'#fff4dcff');sun.addColorStop(.06,'#ffe8bdc9');sun.addColorStop(.2,'#f4c0884d');sun.addColorStop(1,'#f4c08800');ctx.fillStyle=sun;ctx.beginPath();ctx.arc(sunx,suny,g.r*.07,0,TAU);ctx.fill();}
   function rings(front){ctx.save();ctx.translate(g.x,g.y);ctx.rotate(-.34);ctx.scale(1,.43);for(let k=0;k<30;k++){let radius=g.r*(1.22+k*.025);if(k>15&&k<18)continue;ctx.strokeStyle=p.high+(k%3?'72':'b0');ctx.lineWidth=g.r*.018;ctx.beginPath();ctx.arc(0,0,radius,front?0:0,front?Math.PI:TAU);ctx.stroke();}ctx.restore();}
   if(p.rings)rings(false);ctx.drawImage(a.c,g.x-g.r,g.y-g.r,g.r*2,g.r*2);if(p.rings)rings(true);ctx.restore();
  }
  const ready=Promise.all([load('assets/space/day.webp').then(t=>textures.set('M01',t)),load('assets/space/surface.webp').then(t=>cloud=t),load('assets/space/night.webp').then(t=>night=t)]);
  return {ctx,ready,paint,clear(w,h,dpr){ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,w,h);ctx.setTransform(dpr,0,0,dpr,0,0);}};
 }
 root.GeoCPU=Object.freeze({create});
})(globalThis);
