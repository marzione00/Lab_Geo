"""Bake procedural albedo for the Canvas 2D renderer (moderngl, Pillow, numpy).
The ordinary Node build uses the committed textures and needs no Python packages.
"""
from pathlib import Path
import subprocess,json
import moderngl
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1]
data=json.loads(subprocess.check_output(['node','--input-type=module','-e',"await import('./src/planets.js');console.log(JSON.stringify(Object.values(globalThis.GeoPlanets.byId)))"],cwd=root))
ctx=moderngl.create_standalone_context(backend='egl',require=330)
original=(root/'src/planet.frag').read_text()
helpers=original[original.index('const float PI'):original.index('void main()')]
body=original[original.index('   vec3 pos=q*3.3'):original.index('   surface=pow(albedo')]
header='''#version 330
out vec4 fragColor;
uniform float uKind,uSeed,uTilt,uAngle,uTime;
uniform vec3 uLand,uDeep,uHigh;
'''
frag=header+helpers+'''void main(){
vec2 uv=gl_FragCoord.xy/vec2(1024,512);
float lat=(.5-uv.y)*PI,lon=(.5-uv.x)*2.*PI;
vec3 q=vec3(cos(lat)*cos(lon),sin(lat),cos(lat)*sin(lon)),n=q;
float emission=0.,water=0.,cloudAlpha=0.;
'''+body+'''albedo=mix(albedo,vec3(1.,.31,.035),min(1.,emission));
fragColor=vec4(albedo,1.);
}'''
program=ctx.program(vertex_shader='#version 330\nin vec2 aPosition;void main(){gl_Position=vec4(aPosition,0,1);}',fragment_shader=frag)
quad=ctx.simple_vertex_array(program,ctx.buffer(np.array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1],dtype='f4').tobytes()),'aPosition')
fbo=ctx.simple_framebuffer((1024,512));fbo.use();ctx.viewport=(0,0,1024,512)
def setu(k,v):
 if k in program:program[k]=v
def rgb(s):return tuple(int(s[i:i+2],16)/255 for i in (1,3,5))
for p in data:
 if p['kind']==0:continue
 for k,v in {'uKind':p['kind'],'uSeed':p['seed'],'uTilt':p['tilt'],'uAngle':0,'uTime':0,'uLand':rgb(p['land']),'uDeep':rgb(p['deep']),'uHigh':rgb(p['high'])}.items():setu(k,v)
 quad.render(moderngl.TRIANGLES)
 im=Image.frombytes('RGB',(1024,512),fbo.read(components=3))
 im.save(root/'assets/space'/('p-'+p['id']+'.webp'),quality=87,method=6)
print('Baked',len(data)-1,'planet textures.')
