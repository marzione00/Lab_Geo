/* Erebo: Schwarzschild black hole seen by a static observer. The sky behind the hole is deflected along null
   geodesics; the accretion disk, the hot corona and the relativistic jets are millions of particles, each drawn
   at its primary, secondary and tertiary image with gravitational and Doppler shift. Units G = c = M = 1. */
(function (root) {
  'use strict';
  const O = root.GeoObjects;
  const R_MIN = 3.05,
    R_MAX = 320,
    N_R = 256,
    N_PSI = 1024,
    PSI_MAX = 3 * Math.PI + 0.2,
    LEVELS = 12,
    NEAR = 42,
    FAR = 260,
    SKY = 2048,
    DISK_IN = 6,
    DISK_OUT = 34;
  const SPRITE = { high: 1.5, medium: 2, low: 2.6 };
  const COUNTS = {
    high: { disk: 3200000, corona: 420000, jets: 900000, photons: 700000 },
    medium: { disk: 1100000, corona: 150000, jets: 320000, photons: 260000 },
    low: { disk: 180000, corona: 30000, jets: 60000, photons: 50000 },
  };
  // GLSL shared by the particle and sky passes: hashing and the lens tables.
  const COMMON = `
    const float PI=3.14159265,TAU=6.2831853;
    uniform highp sampler2DArray uLens;uniform highp sampler2D uBB;
    uniform vec3 uCam;uniform float uRc,uLevel;
    uint hash(uint x){x^=x>>16;x*=0x7feb352dU;x^=x>>15;x*=0x846ca68bU;x^=x>>16;return x;}
    float rnd(uint id,uint k){return float(hash(id*0x9E3779B9U+k*0x85EBCA6BU+0x632BE5ABU))*2.3283064e-10;}
    float gauss(uint id,uint k){return sqrt(-2.*log(max(1e-7,rnd(id,k))))*cos(TAU*rnd(id,k+101u));}
    // Bilinear value of eta = alpha rc, with its derivatives per column (sweep) and per row (log radius).
    vec3 cell(int layer,float row,float col){
      int r0=clamp(int(floor(row)),0,${N_R - 2}),c0=clamp(int(floor(col)),0,${N_PSI - 2});
      float fr=clamp(row-float(r0),0.,1.),fc=clamp(col-float(c0),0.,1.);
      float a=texelFetch(uLens,ivec3(c0,r0,layer),0).r,b=texelFetch(uLens,ivec3(c0+1,r0,layer),0).r;
      float c=texelFetch(uLens,ivec3(c0,r0+1,layer),0).r,d=texelFetch(uLens,ivec3(c0+1,r0+1,layer),0).r;
      if(min(min(a,b),min(c,d))<0.)return vec3(-1.);
      return vec3(mix(mix(a,b,fc),mix(c,d,fc),fr),mix(b-a,d-c,fr),mix(c-a,d-b,fc));}
    // Apparent angle alpha of the ray reaching radius r after sweep psi, with d alpha / d psi and d alpha / d r.
    vec3 lens(float r,float psi){
      float row=log(r/${R_MIN.toFixed(4)})/${Math.log(R_MAX / R_MIN).toFixed(6)}*${(N_R - 1).toFixed(1)};
      float col=psi/${PSI_MAX.toFixed(6)}*${(N_PSI - 1).toFixed(1)};
      if(row<0.||row>${(N_R - 1).toFixed(1)}||col>${(N_PSI - 1).toFixed(1)})return vec3(-1.);
      int l0=int(floor(uLevel));int l1=min(l0+1,${LEVELS - 1});float w=uLevel-float(l0);
      vec3 a=cell(l0,row,col),b=cell(l1,row,col);
      if(a.x<0.||b.x<0.)return vec3(-1.);
      vec3 e=mix(a,b,w)/uRc;
      return vec3(e.x,e.y*${((N_PSI - 1) / PSI_MAX).toFixed(6)},e.z*${((N_R - 1) / Math.log(R_MAX / R_MIN)).toFixed(6)}/r);}
    vec3 blackbody(float T){float i=clamp(log(T/1000.)/log(40.)*255.,0.,255.);int k=int(floor(i));
      return mix(texelFetch(uBB,ivec2(k,0),0).rgb,texelFetch(uBB,ivec2(min(k+1,255),0),0).rgb,fract(i));}`;
  const PARTICLES = `#version 300 es
    precision highp float;precision highp int;precision highp sampler2DArray;
    ${COMMON}
    uniform highp sampler2D uRadius;
    uniform int uImage,uKind;uniform uint uStride,uOffset;
    uniform float uTime,uGain,uSize,uDoppler,uTpeak,uFpeak,uJetLength;
    uniform mat4 uVP;
    out vec3 vColor;
    float diskFlux(float r){float y=sqrt(r),y0=2.4494897;
      float l=log((y-1.7320508)/(y+1.7320508))-log((y0-1.7320508)/(y0+1.7320508));
      return .1193662*(y-y0-.8660254*l)/(pow(y,5.)*(y*y-3.));}
    float radiusOf(float u){float i=u*1023.;int k=int(floor(i));
      return mix(texelFetch(uRadius,ivec2(k,0),0).r,texelFetch(uRadius,ivec2(min(k+1,1023),0),0).r,fract(i));}
    // Emitter position, local emission (rgb = colour times weight) and redshift data for each kind of particle.
    struct E{vec3 x;vec3 rgb;float omega;vec3 vel;float speed;};
    E disk(uint id){
      uint clump=id>>6u;bool diffuse=rnd(id,1u)<.32;
      float r=diffuse?radiusOf(rnd(id,2u)):radiusOf(rnd(clump,3u))*(1.+.035*gauss(id,4u));
      r=max(r,${DISK_IN}.02);
      float phi=diffuse?rnd(id,5u)*TAU:rnd(clump,6u)*TAU+.16*gauss(id,7u)+.05*gauss(clump,8u);
      // Spiral density wave: the azimuth is drawn toward two arms that wind with radius.
      phi+=.22*sin(2.*(phi-2.6*log(r)));
      float om=pow(r,-1.5);phi+=om*uTime;
      float z=(.010*r+.035)*gauss(id,9u);
      float f=diskFlux(r)/uFpeak;
      E e;e.x=vec3(r*cos(phi),z,r*sin(phi));e.omega=om;e.speed=0.;e.vel=vec3(0);
      float T=uTpeak*pow(max(f,1e-6),.25);e.rgb=vec3(T,sqrt(f),0.);return e;}
    E corona(uint id){
      float r=4.2+10.*pow(rnd(id,11u),1.8);float ct=gauss(id,12u)*.35;ct=clamp(ct,-.95,.95);
      float st=sqrt(1.-ct*ct);float om=.8*pow(r,-1.5);float phi=rnd(id,13u)*TAU+om*uTime;
      E e;e.x=r*vec3(st*cos(phi),ct,st*sin(phi));e.omega=0.;e.speed=0.;e.vel=vec3(0);
      e.rgb=vec3(uTpeak*1.9,.22*pow(6./r,1.2),0.);return e;}
    E jet(uint id){
      float side=(id&1u)==1u?1.:-1.;uint knot=id>>9u;
      // Knots are launched at random times and move outward; each particle follows its knot with some spread.
      float s=fract(rnd(knot,21u)+uTime*.0035+.02*gauss(id,22u));
      float d=5.+uJetLength*s*s;float rho=.5+.16*pow(d,.86)*(.75+.5*rnd(knot,26u));
      float th=rnd(id,23u)*TAU+d*.05+side*uTime*.015;float rr=rho*pow(rnd(id,24u),.6);
      E e;e.x=vec3(rr*cos(th),side*d,rr*sin(th));e.omega=0.;e.vel=vec3(0,side,0);e.speed=.92;
      float fade=smoothstep(5.,24.,d)*(1.-smoothstep(.65,1.,s));
      e.rgb=vec3(uTpeak*2.6,fade*pow(12./d,1.1)*(.4+1.2*rnd(knot,25u)),0.);return e;}
    void main(){
      uint id=uint(gl_VertexID)*uStride+uOffset;
      E e;if(uKind==0)e=disk(id);else if(uKind==1)e=corona(id);else e=jet(id);
      vec3 x=e.x;float re=length(x);vec3 ex=x/re,c=uCam/uRc;
      float gamma=acos(clamp(dot(ex,c),-1.,1.));
      vec3 n=cross(ex,c);float sn=length(n);
      n=sn>1e-7?n/sn:normalize(cross(c,abs(c.y)<.9?vec3(0,1,0):vec3(1,0,0)));
      float psi=uImage==0?gamma:uImage==1?TAU-gamma:TAU+gamma;float s=uImage==1?-1.:1.;
      vec3 L=lens(re,psi);
      if(L.x<0.){gl_Position=vec4(2.,2.,2.,1.);gl_PointSize=0.;vColor=vec3(0);return;}
      float alpha=L.x;vec3 axis=s*n,t=cross(axis,c);
      vec3 dir=-cos(alpha)*c-sin(alpha)*t;
      vec4 p=uVP*vec4(dir,0.);
      if(p.w<=0.){gl_Position=vec4(2.,2.,2.,1.);gl_PointSize=0.;vColor=vec3(0);return;}
      p.z=p.w*.99999;gl_Position=p;
      // Redshift: circular orbits (disk), static gas (corona) or outflow at speed beta (jets).
      float obs=sqrt(1.-2./uRc),b=uRc*sin(alpha)/obs,g;
      if(uKind==0){float lambda=-b*axis.y;g=sqrt(1.-3./re)/(obs*(1.-e.omega*lambda));}
      else if(uKind==1)g=sqrt(1.-2./re)/obs;
      else{vec3 los=normalize(uCam-x);float gam=1./sqrt(1.-e.speed*e.speed);
        g=sqrt(1.-2./re)/(obs*gam*(1.-e.speed*dot(e.vel,los)));}
      g=mix(1.,g,uDoppler);
      // Brightness of a point image: flux = 1 / D_A^2, with D_A^2 = w r sin(gamma) / sin(alpha), where w is the
      // width of the ray bundle at the emitter per unit alpha. w = r cos(chi) / |d alpha/d psi| or
      // sin(chi) / |d alpha/d r|: the better-conditioned form is used (chi: angle of the ray from the radial).
      float schi=min(1.,b*sqrt(1.-2./re)/re),cchi=sqrt(1.-schi*schi);
      float width=cchi>schi?re*cchi/max(abs(L.y),1e-6):schi/max(abs(L.z),1e-6);
      float mag=min(uRc*uRc*sin(alpha)/(width*re*max(sin(gamma),.002)),40.);
      float boost=uKind==2?pow(g,3.):pow(g,4.);
      float weight=e.rgb.y*mag*boost*uGain*(uImage==2?4.:1.);
      vColor=blackbody(e.rgb.x*g)*weight;
      gl_PointSize=uSize;}`;
  const POINT_FRAGMENT = `#version 300 es
    precision highp float;in vec3 vColor;out vec4 o;
    void main(){vec2 q=gl_PointCoord*2.-1.;float d=dot(q,q);if(d>1.)discard;o=vec4(vColor*exp(-3.2*d),1.);}`;
  const SKY_VERTEX = `#version 300 es
    out vec2 vUV;void main(){vec2 p=vec2(float((gl_VertexID<<1)&2),float(gl_VertexID&2));vUV=p;gl_Position=vec4(p*2.-1.,0.,1.);}`;
  const SKY_FRAGMENT = `#version 300 es
    precision highp float;precision highp int;precision highp sampler2DArray;
    ${COMMON}
    in vec2 vUV;out vec4 o;uniform mat4 uInvVP;uniform samplerCube uSky;uniform highp sampler2D uSweep;
    uniform float uLensing,uSkyGain;
    float sweep(int layer,float t){float i=t*${SKY - 1}.;int k=int(floor(i));
      float a=texelFetch(uSweep,ivec2(k,layer),0).r,b=texelFetch(uSweep,ivec2(min(k+1,${SKY - 1}),layer),0).r;
      return min(a,b)<0.?-1.:mix(a,b,fract(i));}
    void main(){
      vec4 q=uInvVP*vec4(vUV*2.-1.,1.,1.);vec3 d=normalize(q.xyz/q.w-uCam),c=uCam/uRc;
      float alpha=acos(clamp(-dot(d,c),-1.,1.));
      float ac=asin(min(1.,5.1961524*sqrt(1.-2./uRc)/uRc));
      vec3 dir=d;
      if(uLensing>.5){
        if(alpha<ac){o=vec4(0,0,0,1);return;}
        float t=sqrt((alpha-ac)/(PI-ac));int l0=int(floor(uLevel));int l1=min(l0+1,${LEVELS - 1});
        float a=sweep(l0,t),b=sweep(l1,t);
        if(a<0.||b<0.){o=vec4(0,0,0,1);return;}
        float S=mix(a,b,uLevel-float(l0));
        vec3 tg=d+dot(d,c)*(-c);tg=normalize(d-dot(d,c)*c);
        dir=cos(S)*c+sin(S)*tg;}
      o=vec4(texture(uSky,dir).rgb*uSkyGain,1.);}`;
  const PHOTON_VERTEX = `#version 300 es
    precision highp float;precision highp int;
    uniform highp sampler2D uPaths;uniform mat4 uVP;uniform float uTime,uGain,uSize;uniform int uCount,uSamples;
    out vec3 vColor;
    uint hash(uint x){x^=x>>16;x*=0x7feb352dU;x^=x>>15;x*=0x846ca68bU;x^=x>>16;return x;}
    float rnd(uint id,uint k){return float(hash(id*0x9E3779B9U+k*0x85EBCA6BU+0x632BE5ABU))*2.3283064e-10;}
    void main(){
      uint id=uint(gl_VertexID);uint beam=id>>11u;
      int path=int(rnd(beam,1u)*float(uCount));
      // Plane of the path: incoming direction and a perpendicular, both random on the sphere.
      float z=rnd(beam,2u)*2.-1.,a=rnd(beam,3u)*6.2831853;vec3 e1=vec3(sqrt(1.-z*z)*cos(a),z,sqrt(1.-z*z)*sin(a));
      vec3 h=abs(e1.y)<.9?vec3(0,1,0):vec3(1,0,0);vec3 p1=normalize(cross(e1,h)),p2=cross(e1,p1);
      float b=rnd(beam,4u)*6.2831853;vec3 e2=cos(b)*p1+sin(b)*p2;
      // Points cover the whole path; pulses of light run along it.
      float u=rnd(id,5u),s=u*float(uSamples-1);int k=int(floor(s));
      vec4 A=texelFetch(uPaths,ivec2(k,path),0),B=texelFetch(uPaths,ivec2(min(k+1,uSamples-1),path),0);
      vec4 P=mix(A,B,fract(s));
      vec3 x=P.x*e1+P.y*e2;
      gl_Position=uVP*vec4(x,1.);gl_PointSize=uSize;
      float alive=min(A.z,B.z),pulse=.18+.82*pow(.5+.5*cos(6.2831853*(u*4.-uTime*.22-rnd(beam,6u))),8.);
      vColor=mix(vec3(1.,.36,.12),vec3(.55,.72,1.),P.w*P.w)*uGain*alive*pulse*(.4+.6*P.w);}`;

  // Inverse cumulative distribution of disk radii for a density proportional to r sqrt(F(r)).
  function radiusTable(n = 1024) {
    const grid = 8192,
      cdf = new Float64Array(grid + 1),
      r = i => DISK_IN + ((DISK_OUT - DISK_IN) * i) / grid;
    for (let i = 1; i <= grid; i++) {
      const x = r(i - 0.5);
      cdf[i] = cdf[i - 1] + x * Math.sqrt(O.diskFluxGeo(x) / O.diskPeak.flux) * (0.55 + 0.45 * Math.exp(-x / 22));
    }
    const out = new Float32Array(n);
    let j = 0;
    for (let k = 0; k < n; k++) {
      const target = (k / (n - 1)) * cdf[grid];
      while (j < grid - 1 && cdf[j + 1] < target) j++;
      const f = (target - cdf[j]) / (cdf[j + 1] - cdf[j] || 1);
      out[k] = r(j + f);
    }
    return out;
  }

  function create(engine, ui) {
    const gl = engine.gl,
      model = O.byId['buco-nero'].model,
      counts = { ...COUNTS[engine.tier] };
    const particles = engine.program(PARTICLES, POINT_FRAGMENT, 'erebo-particles'),
      skyPass = engine.program(SKY_VERTEX, SKY_FRAGMENT, 'erebo-sky'),
      photons = engine.program(PHOTON_VERTEX, POINT_FRAGMENT, 'erebo-photons');
    const radius = engine.dataTexture(radiusTable(), 1024, 1, 1),
      bb = engine.dataTexture(O.blackbodyTable(256), 256, 1, 4),
      lensData = new Float32Array(N_PSI * N_R * LEVELS).fill(-1),
      sweepData = new Float32Array(SKY * LEVELS).fill(-1);
    let lensTex = engine.dataArray(lensData, N_PSI, N_R, LEVELS),
      sweepTex = engine.dataTexture(sweepData, SKY, LEVELS, 1),
      pathTex = null,
      pathInfo = null,
      cube = null,
      radii = null,
      ready = new Set(),
      busy = true;
    const options = { doppler: true, images: true, jets: true, photons: false, ...ui?.initial };
    const gains = { disk: 0.22, corona: 0.05, jets: 0.6, photons: 0.035, sky: 0.8, ...ui?.gains };
    const status = text => ui?.status?.(text);
    status('Calcolo delle geodetiche della luce…');
    const radiiAll = Array.from({ length: LEVELS }, (_, i) => NEAR * (FAR / NEAR) ** (i / (LEVELS - 1)));
    engine
      .work('lens', {
        near: NEAR,
        far: FAR,
        count: LEVELS,
        first: engine.camera.distance,
        rays: engine.tier === 'low' ? 1536 : 3072,
        onPartial(level) {
          lensData.set(level.lens, level.index * N_PSI * N_R);
          sweepData.set(level.sky, level.index * SKY);
          ready.add(level.index);
          gl.bindTexture(gl.TEXTURE_2D_ARRAY, lensTex);
          gl.texSubImage3D(gl.TEXTURE_2D_ARRAY, 0, 0, 0, level.index, N_PSI, N_R, 1, gl.RED, gl.FLOAT, level.lens);
          gl.bindTexture(gl.TEXTURE_2D, sweepTex);
          gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, level.index, SKY, 1, gl.RED, gl.FLOAT, level.sky);
          status(ready.size < LEVELS ? 'Geodetiche: ' + ready.size + ' livelli su ' + LEVELS : '');
          engine.invalidate();
        },
      })
      .then(result => {
        radii = result.radii;
        busy = false;
        status('');
        engine.invalidate();
      })
      .catch(err => status('Calcolo non riuscito: ' + err.message));
    engine.work('photons', { count: 256, samples: 512 }).then(r => {
      pathTex = engine.dataTexture(r.paths, r.samples, r.count, 4);
      pathInfo = r;
      engine.invalidate();
    });
    // Fractional level for the camera radius, restricted to levels already computed.
    function level(rc) {
      const all = radii || radiiAll,
        x = Math.log(rc / all[0]) / Math.log(all[1] / all[0]),
        l = Math.min(LEVELS - 1.0001, Math.max(0, x));
      const l0 = Math.floor(l);
      if (ready.has(l0) && ready.has(l0 + 1)) return l;
      let best = -1;
      for (const i of ready) if (best < 0 || Math.abs(i - l) < Math.abs(best - l)) best = i;
      return best < 0 ? -1 : Math.min(best, LEVELS - 1.0001);
    }
    function common(p, frame, lv, rc) {
      gl.useProgram(p);
      engine.set(p, 'uCam', frame.camera.eye);
      engine.set(p, 'uRc', rc);
      engine.set(p, 'uLevel', lv);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D_ARRAY, lensTex);
      engine.set(p, 'uLens', 0, 'int');
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, bb);
      engine.set(p, 'uBB', 1, 'int');
    }
    function drawSky(frame, lv, rc) {
      cube ||= engine.skyCube(engine.tier === 'high' ? 2048 : engine.tier === 'medium' ? 1024 : 512, 1);
      gl.bindFramebuffer(gl.FRAMEBUFFER, frame.output);
      gl.viewport(0, 0, frame.width, frame.height);
      common(skyPass, frame, Math.max(0, lv), rc);
      engine.set(skyPass, 'uInvVP', engine.invert(frame.camera.vp));
      gl.activeTexture(gl.TEXTURE2);
      gl.bindTexture(gl.TEXTURE_CUBE_MAP, cube);
      engine.set(skyPass, 'uSky', 2, 'int');
      gl.activeTexture(gl.TEXTURE3);
      gl.bindTexture(gl.TEXTURE_2D, sweepTex);
      engine.set(skyPass, 'uSweep', 3, 'int');
      engine.set(skyPass, 'uLensing', lv >= 0 ? 1 : 0);
      engine.set(skyPass, 'uSkyGain', gains.sky);
      gl.disable(gl.DEPTH_TEST);
      gl.disable(gl.BLEND);
      engine.fullscreen();
    }
    function drawKind(frame, kind, count, gain) {
      const images = options.images ? 3 : 1;
      engine.set(particles, 'uKind', kind, 'int');
      for (let image = 0; image < images; image++) {
        const stride = image === 2 ? 4 : 1;
        engine.set(particles, 'uImage', image, 'int');
        gl.uniform1ui(gl.getUniformLocation(particles, 'uStride'), stride);
        gl.uniform1ui(gl.getUniformLocation(particles, 'uOffset'), image === 2 ? 1 : 0);
        engine.set(particles, 'uGain', gain);
        engine.points(Math.floor(count / stride));
      }
    }
    function draw(frame) {
      const rc = Math.hypot(...frame.camera.eye),
        lv = level(rc),
        t = 600 + frame.time * 11;
      drawSky(frame, lv, rc);
      if (lv < 0) return;
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE);
      gl.disable(gl.DEPTH_TEST);
      gl.depthMask(false);
      common(particles, frame, lv, rc);
      gl.activeTexture(gl.TEXTURE2);
      gl.bindTexture(gl.TEXTURE_2D, radius);
      engine.set(particles, 'uRadius', 2, 'int');
      engine.set(particles, 'uVP', frame.camera.vp);
      const size = Math.max(1, SPRITE[engine.tier] * frame.pixelRatio);
      engine.set(particles, 'uTime', t);
      engine.set(particles, 'uSize', size);
      engine.set(particles, 'uDoppler', options.doppler ? 1 : 0);
      engine.set(particles, 'uTpeak', model.displayPeak);
      engine.set(particles, 'uFpeak', O.diskPeak.flux);
      engine.set(particles, 'uJetLength', 150);
      // Gains keep the brightness per pixel independent of particle count, resolution and sprite size.
      const sprite = Math.max(1, 0.94 * (size / 2) ** 2),
        area = (frame.width * frame.height) / 1.0e6 / sprite;
      drawKind(frame, 0, counts.disk, (gains.disk * area * 3.2e6) / counts.disk);
      drawKind(frame, 1, counts.corona, (gains.corona * area * 4.2e5) / counts.corona);
      if (options.jets) drawKind(frame, 2, counts.jets, (gains.jets * area * 9e5) / counts.jets);
      if (options.photons && pathTex) {
        gl.useProgram(photons);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, pathTex);
        engine.set(photons, 'uPaths', 0, 'int');
        engine.set(photons, 'uVP', frame.camera.vp);
        engine.set(photons, 'uTime', frame.time);
        engine.set(photons, 'uGain', (gains.photons * area * 7e5) / counts.photons);
        engine.set(photons, 'uSize', Math.max(1, 1.4 * frame.pixelRatio));
        engine.set(photons, 'uCount', pathInfo.count, 'int');
        engine.set(photons, 'uSamples', pathInfo.samples, 'int');
        engine.points(counts.photons);
      }
      gl.disable(gl.BLEND);
      gl.depthMask(true);
    }
    return {
      draw,
      busy: () => busy,
      near: d => d * 0.01,
      far: d => d * 20,
      options,
      gains,
      setOption(key, value) {
        options[key] = value;
        engine.invalidate();
      },
      reduce() {
        if (counts.disk < 300000) return engine.reduceResolution();
        for (const k of Object.keys(counts)) counts[k] = Math.round(counts[k] * 0.7);
        return true;
      },
      debug: () => ({
        object: 'buco-nero',
        levels: ready.size,
        particles: counts.disk + counts.corona + (options.jets ? counts.jets : 0),
        images: options.images ? 3 : 1,
        counts: { ...counts },
        options: { ...options },
      }),
      dispose() {
        ready.clear();
      },
    };
  }
  root.GeoObjectScenes = root.GeoObjectScenes || {};
  root.GeoObjectScenes['buco-nero'] = {
    create,
    exposure: 0.55,
    camera: {
      azimuth: 0.4,
      elevation: 0.17,
      distance: 72,
      minDistance: NEAR + 1,
      maxDistance: FAR - 1,
      minElevation: -1.3,
      maxElevation: 1.3,
      fov: (38 * Math.PI) / 180,
    },
    radiusTable,
  };
})(globalThis);
