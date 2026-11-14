"""Bake original, seamless planetary albedos for optional research worlds.

Run with Python 3 + moderngl + numpy + Pillow. EGL renders a spherical 3D
procedural field at 4096 x 2048; the 2048 x 1024 navigation mip is filtered
from that original. No downloaded or game textures are used. These images
contain no directional illumination: the scene supplies stellar lighting.
"""
from pathlib import Path
import hashlib
import json
import argparse
import tempfile

import moderngl
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = ["gaia", "temperate", "ocean", "forest", "plains", "swamp",
            "desert", "arctic", "rocky", "barren", "volcanic", "acid", "gas"]
SHADER = r"""#version 330
out vec4 fragColor;
uniform int family;
uniform float seed;
const float PI=3.141592653589793;

float hash(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float noise(vec3 p){
 vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
 return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),
                mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
            mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),
                mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);
}
mat3 spin=mat3(.00,.80,.60,-.80,.36,-.48,-.60,-.48,.64);
float fbm(vec3 p){float v=0.,a=.5;for(int j=0;j<7;j++){v+=a*noise(p);p=spin*p*2.03+vec3(1.2,3.7,2.1);a*=.5;}return v;}
float ridge(vec3 p){return 1.-abs(2.*fbm(p)-1.);}
vec3 warp(vec3 p){return vec3(fbm(p+vec3(17,0,0)),fbm(p+vec3(0,31,0)),fbm(p+vec3(0,0,43)))-.5;}
vec3 mix3(vec3 low,vec3 mid,vec3 high,float t){return t<.52?mix(low,mid,smoothstep(.14,.52,t)):mix(mid,high,smoothstep(.52,.84,t));}

float crater(vec3 q,float k){
 float lon=hash(vec3(k,seed,1.2))*2.*PI,sy=hash(vec3(k,seed,9.1))*2.-1.;
 vec3 center=vec3(sqrt(1.-sy*sy)*cos(lon),sy,sqrt(1.-sy*sy)*sin(lon));
 float radius=mix(.018,.145,pow(hash(vec3(k,seed,4.2)),2.));
 float d=length(q-center)/radius;
 return -.32*exp(-pow(d/.63,4.))+.28*exp(-pow((d-.98)/.14,2.))+.08*exp(-pow(d/.15,2.));
}

void main(){
 vec2 uv=gl_FragCoord.xy/vec2(4096.,2048.);
 float latitude=(.5-uv.y)*PI,longitude=(.5-uv.x)*2.*PI;
 vec3 q=vec3(cos(latitude)*cos(longitude),sin(latitude),cos(latitude)*sin(longitude));
 vec3 p=q*3.3+vec3(seed,seed*.37,-seed*.51);
 vec3 w=warp(p*.72);
 float terrain=fbm(p*1.3+w*1.9),detail=fbm(p*31.),fine=noise(p*230.);
 float ridges=pow(ridge(p*6.5+w*2.),9.);
 float humidity=fbm(p*1.2+vec3(44.6));
 float lat=abs(q.y),heat=1.-lat;
 vec3 col=vec3(.1);
 if(family<=5){
  float sea=.487;
  if(family==1)sea=.47;
  if(family==2)sea=.595;
  if(family==3)sea=.445;
  if(family==4)sea=.405;
  if(family==5)sea=.49;
  float land=smoothstep(sea-.003,sea+.005,terrain);
  float depth=smoothstep(sea-.14,sea,terrain);
  vec3 ocean=mix(vec3(.012,.055,.13),vec3(.023,.27,.36),pow(depth,3.));
  ocean=mix(ocean,vec3(.09,.45,.48),smoothstep(sea-.016,sea,terrain)*.48);
  vec3 soil=mix(vec3(.19,.29,.13),vec3(.53,.43,.25),smoothstep(.42,.63,humidity+.14*heat));
  if(family==0)soil=mix(vec3(.07,.25,.17),vec3(.4,.43,.22),smoothstep(.34,.64,humidity));
  if(family==3)soil=mix(vec3(.028,.13,.09),vec3(.18,.36,.16),humidity);
  if(family==4)soil=mix(vec3(.34,.38,.18),vec3(.68,.59,.30),humidity);
  if(family==5){soil=mix(vec3(.07,.18,.12),vec3(.29,.36,.15),humidity);ocean=mix(vec3(.025,.12,.12),vec3(.09,.31,.26),depth);}
  soil=mix(soil,vec3(.55,.49,.36),ridges*.28);
  soil*=.88+.32*detail+.08*fine;
  float snow=smoothstep(.72,.90,lat+(terrain-sea)*.9+.04*(detail-.5));
  if(family==2||family==3||family==5)snow*=.45;
  soil=mix(soil,vec3(.84,.88,.84),snow);
  col=mix(ocean,soil,land);
  col=mix(col,vec3(.82,.88,.89),smoothstep(.965,.99,lat+.018*(detail-.5))*.92);
  vec3 cloudp=p*1.9+warp(p*1.2)*1.6;
  float clouds=smoothstep(.56,.69,fbm(cloudp))*smoothstep(.08,.3,1.-lat);
  float wisps=smoothstep(.65,.79,ridge(p*5.+w*4.))*smoothstep(.54,.67,fbm(p*.8+17.));
  float coverage=family==0?.72:family==1?.48:family==2?.65:family==3?.38:family==4?.21:.55;
  col=mix(col,vec3(.85,.9,.92),clamp(clouds+wisps*.17,0.,.85)*coverage);
 }else if(family==6){
  float basin=fbm(p*1.5+w*2.4);
  col=mix3(vec3(.22,.13,.075),vec3(.55,.32,.15),vec3(.83,.65,.38),basin);
  float dunes=sin(q.y*190.+fbm(p*9.)*26.+q.x*60.);
  col*=.92+.08*dunes+.19*(detail-.5);
  float salt=smoothstep(.64,.69,terrain)*smoothstep(.4,.6,humidity);
  col=mix(col,vec3(.85,.76,.59),salt*.8);
  col=mix(col,vec3(.85,.70,.46),smoothstep(.58,.73,fbm(p*2.2+w*3.))*.17);
 }else if(family==7){
  float fractures=1.-smoothstep(.012,.055,abs(fbm(p*9.+w*4.)-.5));
  col=mix3(vec3(.15,.34,.43),vec3(.52,.70,.76),vec3(.90,.94,.93),terrain+.10);
  col=mix(col,vec3(.10,.24,.33),fractures*.44);
  col=mix(col,vec3(.87,.94,.94),pow(ridges,2.)*.35);
  col*=.93+.16*detail+.05*fine;
 }else if(family==8||family==9){
  float cr=0.;for(int k=0;k<62;k++)cr+=crater(q,float(k));
  vec3 low=family==8?vec3(.14,.12,.12):vec3(.065,.072,.085);
  vec3 mid=family==8?vec3(.36,.31,.26):vec3(.26,.27,.28);
  vec3 high=family==8?vec3(.58,.52,.44):vec3(.51,.49,.45);
  col=mix3(low,mid,high,terrain+.16*cr);
  col*=clamp(.89+.23*detail+cr,.48,1.34);
  col+=.04*(fine-.5);
  float ejecta=smoothstep(.64,.70,fbm(p*2.+w*4.));
  col=mix(col,high,ejecta*.22);
 }else if(family==10){
  float tectonic=abs(fbm(p*3.4+w*2.)-.51);
  float hot=1.-smoothstep(.002,.020,tectonic);
  float channels=pow(hot,3.)*smoothstep(.42,.56,fbm(p*.85+12.));
  col=mix(vec3(.045,.037,.045),vec3(.20,.12,.10),terrain);
  col*=.8+.5*detail;
  col=mix(col,vec3(.72,.12,.025),hot*.35);
  col=mix(col,vec3(1.,.38,.035),channels*.9);
  col=mix(col,vec3(1.,.70,.16),pow(channels,4.)*.65);
  float ash=smoothstep(.59,.73,fbm(p*1.5+w*2.));
  col=mix(col,vec3(.27,.20,.18),ash*.45);
 }else if(family==11){
  float flow=fbm(p*2.+warp(p*2.)*4.);
  col=mix3(vec3(.17,.18,.08),vec3(.49,.48,.16),vec3(.84,.74,.36),flow);
  float storms=smoothstep(.53,.69,fbm(p*2.8+warp(p*1.3)*4.));
  col=mix(col,vec3(.88,.80,.49),storms*.65);
  col*=.95+.14*(detail-.5);
  col=mix(col,vec3(.42,.24,.12),smoothstep(.66,.73,terrain)*.4);
 }else{
  float bandlat=q.y;
  // Longitude-dependent distortion fades at the poles; spherical noise keeps the seam closed.
  float turbulence=(fbm(p*3.4+w*2.)-.5)*.12*(1.-lat*lat);
  float bands=sin((bandlat+turbulence)*62.+fbm(p*2.)*3.);
  float bands2=sin((bandlat+turbulence)*155.+fbm(p*7.)*8.);
  vec3 deep=vec3(.10,.19,.28),cream=vec3(.76,.70,.53),ochre=vec3(.48,.31,.19);
  col=mix(deep,cream,smoothstep(-.75,.7,bands));
  col=mix(col,ochre,smoothstep(.3,.85,sin(bandlat*22.+.6))*.5);
  col*=.94+.06*bands2+.18*(detail-.5);
  // A bounded elliptical vortex in one hemisphere, expressed on the unit sphere.
  vec3 center=normalize(vec3(.88,-.24,.42));
  vec3 tangent=normalize(cross(vec3(0,1,0),center)),north=normalize(cross(center,tangent));
  vec2 v=vec2(dot(q-center,tangent)/.26,dot(q-center,north)/.11);
  float r=length(v),gate=smoothstep(.98,.80,r)*smoothstep(.75,.95,dot(q,center));
  float swirl=.5+.5*sin(atan(v.y,v.x)*2.+r*19.+fbm(p*10.)*5.);
  col=mix(col,mix(vec3(.42,.19,.12),vec3(.83,.57,.33),swirl),gate*.75);
 }
 fragColor=vec4(clamp(col,0.,1.),1.);
}
"""


def preview_sphere(texture, size=270):
    """QA-only sphere with a common light, not an exported texture layer."""
    yy, xx = np.mgrid[-1:1:complex(size), -1:1:complex(size)]
    mask = xx*xx+yy*yy <= 1
    z = np.sqrt(np.maximum(0, 1-xx*xx-yy*yy))
    lon = np.arctan2(z, xx)
    lat = np.arcsin(np.clip(-yy, -1, 1))
    u = ((.5-lon/(2*np.pi)) % 1)*(texture.width-1)
    v = (.5-lat/np.pi)*(texture.height-1)
    rgb = np.asarray(texture)[v.astype(int), u.astype(int)].astype(float)
    lighting = np.maximum(0, -.40*xx-.38*yy+.83*z)
    rgb *= (.10+.90*lighting)[..., None]
    out = np.full((size, size, 3), [6, 12, 23], dtype=np.uint8)
    out[mask] = np.clip(rgb[mask], 0, 255).astype(np.uint8)
    return Image.fromarray(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--families", nargs="*", choices=FAMILIES, default=FAMILIES)
    parser.add_argument("--contact-sheet", default=str(Path(tempfile.gettempdir())/"geostat-planet-families.jpg"))
    args = parser.parse_args()
    out = ROOT/"assets/space/families"
    out.mkdir(parents=True, exist_ok=True)
    ctx = moderngl.create_standalone_context(backend="egl", require=330)
    prog = ctx.program(vertex_shader="#version 330\nin vec2 aPosition;void main(){gl_Position=vec4(aPosition,0,1);}", fragment_shader=SHADER)
    vertices = np.array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1], dtype="f4")
    quad = ctx.simple_vertex_array(prog, ctx.buffer(vertices.tobytes()), "aPosition")
    fbo = ctx.simple_framebuffer((4096, 2048)); fbo.use()
    ctx.viewport = (0, 0, 4096, 2048)
    report = []
    for name in args.families:
        i = FAMILIES.index(name)
        prog["family"] = i; prog["seed"] = 23.7+i*17.13
        quad.render(moderngl.TRIANGLES)
        image = Image.frombytes("RGB", (4096,2048), fbo.read(components=3))
        high = out/f"{name}-4k.webp"; small = out/f"{name}.webp"
        image.save(high, quality=87, method=6)
        image.resize((2048,1024), Image.Resampling.LANCZOS).save(small, quality=85, method=6)
        report.append({"family":name,"4k_bytes":high.stat().st_size,"2k_bytes":small.stat().st_size,"sha256":hashlib.sha256(high.read_bytes()).hexdigest()})
        print(name, high.stat().st_size, small.stat().st_size, flush=True)
    sheet = Image.new("RGB", (4*320, 4*330), "#060c17")
    draw = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 23)
    except OSError: font = ImageFont.load_default()
    for i, name in enumerate(FAMILIES):
        path=out/f"{name}.webp"
        if not path.exists(): continue
        tile = preview_sphere(Image.open(path).convert("RGB"))
        x=(i%4)*320; y=(i//4)*330
        sheet.paste(tile, (x+25,y+10)); draw.text((x+28,y+290), name.upper(), fill="#c9dfed", font=font)
    sheet.save(args.contact_sheet, quality=93)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
