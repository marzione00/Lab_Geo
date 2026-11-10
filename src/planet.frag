precision highp float;
uniform vec2 uResolution;
uniform vec2 uCenter;
uniform float uRadius;
uniform float uAngle;
uniform float uTime;
uniform float uKind;
uniform float uSeed;
uniform float uTilt;
uniform float uRings;
uniform float uOpacity;
uniform float uHero;
uniform vec3 uLand;
uniform vec3 uDeep;
uniform vec3 uHigh;
uniform vec3 uAtmosphere;
uniform sampler2D uDay;
uniform sampler2D uSurface;
uniform sampler2D uNight;
const float PI=3.14159265359;
float hash(vec3 p){return fract(sin(dot(p,vec3(127.1,311.7,74.7)))*43758.5453123);}
float noise(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fbm(vec3 p){float a=.5,s=0.;for(int i=0;i<5;i++){s+=a*noise(p);p=p*2.03+vec3(1.7,9.2,3.1);a*=.49;}return s;}
vec3 rx(vec3 p,float a){float c=cos(a),s=sin(a);return vec3(p.x,c*p.y-s*p.z,s*p.y+c*p.z);}
vec3 ry(vec3 p,float a){float c=cos(a),s=sin(a);return vec3(c*p.x+s*p.z,p.y,-s*p.x+c*p.z);}
vec3 rz(vec3 p,float a){float c=cos(a),s=sin(a);return vec3(c*p.x-s*p.y,s*p.x+c*p.y,p.z);}
vec3 local(vec3 n,float a){return ry(rx(rz(n,-uTilt),-.24),a);}
vec2 earthUV(vec3 q){return vec2(.5-atan(q.z,q.x)/(2.*PI),.5-asin(clamp(q.y,-1.,1.))/PI);}
void main(){
 vec2 xy=vec2(gl_FragCoord.x,uResolution.y-gl_FragCoord.y);
 vec2 p=(xy-uCenter)/uRadius;
 float d=length(p);
 vec3 L=normalize(mix(vec3(-.6,.65,.8),vec3(-.42,.84,-.36),uHero));
 vec2 sunDir=normalize(vec2(L.x,-L.y));
 vec3 col=vec3(0.);float alpha=0.;
 float zSphere=d<1.?sqrt(max(0.,1.-d*d)):-5.;
 // Inclined ring plane, with front/back occlusion against the sphere.
 vec3 ringNormal=normalize(vec3(.23,.78,.51));
 float ringZ=-(ringNormal.x*p.x-ringNormal.y*p.y)/ringNormal.z;
 vec3 rp=vec3(p.x,-p.y,ringZ);float rd=length(rp);
 float ringMask=smoothstep(1.2,1.23,rd)*(1.-smoothstep(1.94,1.98,rd))*uRings;
 if(ringMask>.001&&(d>1.||ringZ>zSphere)){
   float grooves=.5+.5*sin(rd*160.+noise(vec3(rd*44.,uSeed,1.))*4.);
   float gap=1.-smoothstep(.012,.024,abs(rd-1.62));
   col=mix(uLand,uHigh,.35+.45*grooves)*(.5+.28*grooves)*(1.-gap*.8);
   float shadow=smoothstep(.1,.3,length(rp-L*max(dot(rp,L),0.))-.82);
   col*=mix(.15,1.,shadow);alpha=ringMask*(.32+.42*grooves);
 }
 if(d<=1.&&!(ringMask>.001&&ringZ>zSphere)){
  vec3 n=vec3(p.x,-p.y,zSphere),q=local(n,uAngle);
  float diffuse=dot(n,L),sunlight=max(diffuse,0.);
  float water=0.,cloudAlpha=0.,emission=0.;
  vec3 surface;
  if(uKind<.5){
   vec2 uv=earthUV(q);
   vec3 day=pow(texture2D(uDay,uv).rgb,vec3(2.2));
   water=1.-texture2D(uSurface,uv).g;
   vec3 cloudN=vec3(p/1.004*vec2(1.,-1.),sqrt(max(0.,1.-dot(p/1.004,p/1.004))));
   vec2 cuv=earthUV(local(cloudN,uAngle*1.012+.04));
   float clouds=texture2D(uSurface,cuv).b;
   float shadow=texture2D(uSurface,cuv+vec2(.0018,-.001)).b;
   cloudAlpha=smoothstep(.2,.92,clouds)*.88;
   surface=day*vec3(1.,.94,.85)*(sunlight*1.65+.012)*(1.-shadow*.42);
   surface+=day*vec3(.07,.13,.24)*.16;
   surface+=pow(texture2D(uNight,uv).rgb,vec3(1.7))*(1.-smoothstep(-.12,.12,diffuse))*.9;
  }else{
   vec3 pos=q*3.3+uSeed;
   float terrain=fbm(pos),detail=fbm(pos*9.);
   vec3 albedo=mix(uDeep,uLand,smoothstep(.27,.64,terrain));
   if(abs(uKind-4.)<.5||abs(uKind-10.)<.5){
    vec3 flowing=ry(q,uTime*.004*q.y);
    float latitude=flowing.y+(.09+uKind*.002)*(fbm(flowing*7.+uSeed)-.5);
    float bands=sin(latitude*24.+fbm(flowing*14.+uSeed)*2.3);
    float fine=sin(latitude*180.+noise(flowing*60.)*5.);
    albedo=mix(uDeep,uLand,smoothstep(-.9,.8,bands));
    albedo=mix(albedo,uHigh,smoothstep(.45,.95,bands)*.65);
    albedo*=.88+.07*fine+.13*detail;
    vec3 spot=normalize(vec3(.9,-.22,.28));
    float cyclone=exp(-pow(length((q-spot)*vec3(1.,2.,1.))*5.,2.));
    albedo=mix(albedo,uDeep,cyclone*(.65+.2*sin(length(q-spot)*150.+uTime*.08)));
   }else if(abs(uKind-14.)<.5){
    float cracks=abs(fbm(pos*1.6)-.47);
    emission=(1.-smoothstep(.008,.032,cracks))*smoothstep(.29,.65,terrain);
    albedo=mix(uDeep,uLand,detail)*(.75+detail*.5);
   }else if(abs(uKind-9.)<.5){
    float cracks=abs(fbm(pos*2.)-.48);
    albedo=mix(uDeep,uHigh,smoothstep(.009,.043,cracks));
    albedo=mix(albedo,uLand,detail*.5);
   }else if(abs(uKind-5.)<.5||abs(uKind-6.)<.5||abs(uKind-8.)<.5){
    float limit=abs(uKind-5.)<.5?.57:.49;
    water=1.-smoothstep(limit-.01,limit+.01,terrain);
    albedo=mix(mix(uLand,uHigh,smoothstep(.58,.76,terrain)),uDeep,water);
    float cloud=fbm(local(n,uAngle*1.022+.2)*8.+uSeed);
    cloudAlpha=smoothstep(.52,.72,cloud)*.7;
   }else if(abs(uKind-13.)<.5){
    float strata=sin(q.y*57.+terrain*19.+detail*2.);
    albedo=mix(uLand,uHigh,smoothstep(-.7,.7,strata));
    albedo=mix(uDeep,albedo,smoothstep(.22,.54,terrain));
   }else if(abs(uKind-3.)<.5||abs(uKind-16.)<.5){
    albedo=mix(uDeep,uLand,smoothstep(.35,.48,terrain));
    albedo=mix(albedo,uHigh,smoothstep(.54,.61,terrain));
    albedo*=.6+detail*.8;
   }else if(abs(uKind-2.)<.5){
    float faults=abs(fbm(pos*1.8)-.49);
    albedo=mix(uDeep,mix(uLand,uHigh,detail),smoothstep(.012,.055,faults));
   }else{
    albedo=mix(albedo,uHigh,smoothstep(.51,.72,terrain));
    albedo*=.6+detail*.8;
    float crater=abs(noise(q*24.+uSeed)-.45);
    albedo*=.72+.28*smoothstep(.01,.12,crater);
   }
   surface=pow(albedo,vec3(2.2))*(vec3(1.,.93,.86)*sunlight*1.65+vec3(.027,.038,.055));
   surface+=vec3(1.,.16,.014)*emission*(1.3-sunlight*.3);
   if(abs(uKind-15.)<.5){float stations=step(.91,noise(q*120.));surface+=vec3(.22,.68,1.)*stations*.1*(1.-sunlight);}
  }
  float spec=pow(max(dot(n,normalize(L+vec3(0,0,1))),0.),105.)*water*(1.-cloudAlpha);
  surface+=vec3(.7,.85,1.)*spec*.5;
  surface=mix(surface,vec3(.74,.85,1.)*(.035+sunlight*1.24),cloudAlpha);
  float rim=pow(1.-n.z,4.2),rimLit=smoothstep(-.2,.8,diffuse);
  surface+=pow(uAtmosphere,vec3(2.2))*rim*(.05+rimLit*.75);
  if(uRings>.5){
   float travel=-dot(n,ringNormal)/dot(L,ringNormal);
   float shadowRadius=length(n+L*travel);
   float shadow=smoothstep(1.2,1.25,shadowRadius)*(1.-smoothstep(1.94,2.,shadowRadius))*step(0.,travel);
   surface*=1.-shadow*.6;
  }
  col=surface;alpha=1.;
 }else if(d>1.){
  float edge=d-1.;float facing=max(dot(normalize(p),sunDir),0.);
  float halo=(exp(-edge*160.)*.55+exp(-edge*32.)*.04)*(.12+.88*facing);
  vec3 atmosphere=pow(uAtmosphere,vec3(2.2));
  col+=atmosphere*halo;alpha=max(alpha,min(halo*2.,.9));
  if(uHero>.5){
   vec2 sun=p-sunDir*1.012;float sunDist=length(sun);
   float flare=exp(-sunDist*sunDist*17000.)*2.7+exp(-sunDist*32.)*.12;
   col+=vec3(1.,.67,.39)*flare;alpha=max(alpha,min(1.,flare));
  }
 }
 if(alpha<.001)discard;
 col=col/(col+vec3(.8));
 gl_FragColor=vec4(pow(max(col,vec3(0)),vec3(1./2.2)),alpha*uOpacity);
}
