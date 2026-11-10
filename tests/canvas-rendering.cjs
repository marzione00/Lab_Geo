/* Optional real-pixel Canvas test; requires @napi-rs/canvas in the QA environment. */
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const {createCanvas,Image}=require('@napi-rs/canvas');
const root=path.resolve(__dirname,'..');process.chdir(root);
const context={console,Image,document:{createElement:()=>createCanvas(1,1)},window:{},Float32Array,Uint32Array};context.globalThis=context;vm.createContext(context);
vm.runInContext(fs.readFileSync('src/planets.js','utf8'),context);vm.runInContext(fs.readFileSync('src/space-cpu.js','utf8'),context);
(async()=>{
 const c=createCanvas(256,256),engine=context.GeoCPU.create(c);await engine.ready;
 const report=[];
 for(const p of Object.values(context.GeoPlanets.byId)){
  const geometry={x:128,y:128,r:p.rings?56:100,hero:0};engine.paint(p,geometry,0);
  await new Promise(r=>setTimeout(r,30));
  engine.clear(256,256,1);engine.paint(p,geometry,0);const a=engine.ctx.getImageData(0,0,256,256).data;
  engine.clear(256,256,1);engine.paint(p,geometry,10);const b=engine.ctx.getImageData(0,0,256,256).data;
  let changed=0,visible=0;
  for(let i=0;i<a.length;i+=4){if(a[i+3]>200){visible++;if(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2])>6)changed++;}}
  assert(visible>6000,p.id+' must be visible');assert(changed/visible>.05,p.id+' must rotate');report.push({id:p.id,changedPixels:changed,visiblePixels:visible});
 }
 fs.writeFileSync('qa/canvas-rendering.json',JSON.stringify({renderer:'Canvas 2D via napi-rs',worlds:report},null,2));
 console.log('Canvas: all 28 destinations show actual surface rotation.');
})().catch(e=>{console.error(e);process.exitCode=1;});
