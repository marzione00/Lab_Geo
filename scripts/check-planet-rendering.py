"""Offline shader validation, including rotation for all 28 destinations."""
from pathlib import Path
import json,subprocess
import moderngl
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
data=json.loads(subprocess.check_output(['node','--input-type=module','-e',"await import('./src/planets.js');console.log(JSON.stringify(Object.values(globalThis.GeoPlanets.byId)))"],cwd=root))
ctx=moderngl.create_standalone_context(backend='egl',require=330)
frag=(root/'src/planet.frag').read_text().replace('precision highp float;','#version 330\nout vec4 fragColor;').replace('texture2D','texture').replace('gl_FragColor','fragColor')
program=ctx.program(vertex_shader='#version 330\nin vec2 aPosition;void main(){gl_Position=vec4(aPosition,0,1);}',fragment_shader=frag)
quad=ctx.simple_vertex_array(program,ctx.buffer(np.array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1],dtype='f4').tobytes()),'aPosition')
for i,name in enumerate(['Day','Surface','Night']):
 im=Image.open(root/'assets/space'/(name.lower()+'.webp')).convert('RGB');t=ctx.texture(im.size,3,im.tobytes());t.filter=(moderngl.LINEAR,moderngl.LINEAR);t.repeat_x=True;t.repeat_y=False;t.use(i);program['u'+name]=i
size=360;fbo=ctx.simple_framebuffer((size,size),components=4);fbo.use();ctx.viewport=(0,0,size,size)
def rgb(s):return tuple(int(s[i:i+2],16)/255 for i in (1,3,5))
sheet=Image.new('RGB',(5*size,4*(size+36)),(5,11,22));draw=ImageDraw.Draw(sheet)
changes=[]
for i,p in enumerate(data):
 for key,value in {'uResolution':(size,size),'uCenter':(size/2,size/2),'uRadius':85 if p['rings'] else 148,'uKind':p['kind'],'uSeed':p['seed'],'uTilt':p['tilt'],'uRings':int(p['rings']),'uOpacity':1,'uHero':0,'uLand':rgb(p['land']),'uDeep':rgb(p['deep']),'uHigh':rgb(p['high']),'uAtmosphere':rgb(p['atmosphere'])}.items():program[key]=value
 frames=[]
 for time in (0,10):
  program['uAngle']=p['phase']-time*p['speed'];program['uTime']=time;fbo.clear();quad.render(moderngl.TRIANGLES)
  im=Image.frombytes('RGBA',(size,size),fbo.read(components=4)).transpose(Image.Transpose.FLIP_TOP_BOTTOM);frames.append(im)
 a,b=[np.array(im).astype(float) for im in frames];mask=a[:,:,3]>250
 change=float(abs(a-b)[mask,:3].mean());assert change>1,(p['id'],change)
 # Outside the sphere and its rings, illumination and the silhouette remain fixed.
 assert np.array_equal(a[:,:,3],b[:,:,3]),p['id']
 changes.append({'id':p['id'],'mean_rgb_change_10_seconds':round(change,3),'silhouette_fixed':True})
 if i<17:
  x=(i%5)*size;y=(i//5)*(size+36);sheet.paste(frames[0],(x,y),frames[0]);draw.text((x+20,y+size+8),p['id']+' / '+p['name'],fill='#d3e5ed')
out=root/'qa';out.mkdir(exist_ok=True);sheet.save(out/'pianeti-collaudo.png')
(out/'rendering.json').write_text(json.dumps({'renderer':ctx.info['GL_RENDERER'],'shader_compiled':True,'destinations':changes},indent=2))
print('Shader compiled; 28 worlds rotate with fixed silhouettes.')
