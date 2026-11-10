"""Original procedural galaxy illustration; deterministic, no external textures.
Regenerate with Python 3 and Pillow: python3 scripts/generate-galaxy.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math, random
rng=random.Random(170139)
W,H=1800,1250
im=Image.new("RGB",(W,H),(3,9,18))
fog=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(fog)
def project(rad,angle):
 x=rad*math.cos(angle); y=rad*math.sin(angle)*.65
 a=-.20
 return W*.50+x*math.cos(a)-y*math.sin(a),H*.48+x*math.sin(a)+y*math.cos(a)
for i in range(22000):
 rad=rng.random()**.55*790
 angle=(i%4)*math.pi/2+rad*.0065+rng.gauss(0,.16+.10*rad/790)
 x,y=project(rad,angle); s=rng.uniform(1,8)
 t=rad/790
 color=(int(43-20*t),int(48+20*t),int(65+28*t))
 d.ellipse((x-s,y-s,x+s,y+s),fill=color)
fog=fog.filter(ImageFilter.GaussianBlur(13))
from PIL import ImageChops
im=ImageChops.add(im,fog)
d=ImageDraw.Draw(im)
for i in range(52000):
 rad=rng.random()**.57*820
 angle=(i%4)*math.pi/2+rad*.0065+rng.gauss(0,.095+.12*rad/820)
 x,y=project(rad,angle)
 brightness=rng.uniform(.25,1)*(1-rad/1200)
 base=(199,205,238) if rng.random()>.18 else (110,159,213)
 s=rng.choices([.35,.55,.9,1.4],[45,35,18,2])[0]
 d.ellipse((x-s,y-s,x+s,y+s),fill=tuple(int(v*brightness) for v in base))
# Warm, diffuse nucleus; retain navigational contrast.
core=Image.new('RGB',(W,H)); cd=ImageDraw.Draw(core)
for rad in range(210,0,-2):
 t=(1-rad/210)**2
 x,y=project(0,0)
 cd.ellipse((x-rad,y-rad*.72,x+rad,y+rad*.72),fill=(int(152*t),int(128*t),int(101*t)))
im=ImageChops.add(im,core.filter(ImageFilter.GaussianBlur(21)))
d=ImageDraw.Draw(im)
for _ in range(900):
 x,y=rng.randrange(W),rng.randrange(H); b=rng.randrange(45,170); s=rng.choice([.4,.6,1])
 d.ellipse((x-s,y-s,x+s,y+s),fill=(int(b*.72),int(b*.87),b))
for x,y in [(260,170),(1500,880),(700,1060),(1320,175),(360,910),(1600,410)]:
 d.line((x-5,y,x+5,y),fill=(74,125,155)); d.line((x,y-5,x,y+5),fill=(74,125,155));d.ellipse((x-1,y-1,x+1,y+1),fill=(215,235,250))
out=Path(__file__).resolve().parents[1]/'assets/space/galaxy.webp'
im.save(out,quality=88,method=6)
print(out, out.stat().st_size)
