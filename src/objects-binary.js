/* Diade: a cataclysmic binary. A red dwarf fills its Roche lobe and loses gas through the inner Lagrange point;
   the ballistic stream hits the accretion disk around the white dwarf at a hot spot. The donor surface is the
   critical equipotential of the Roche potential. Units: the separation of the two stars is 10 scene units;
   one orbit lasts 40 s on screen. */
(function (root) {
  'use strict';
  const O = root.GeoObjects,
    K = root.GeoObjectKit,
    TAU = Math.PI * 2;
  const COUNTS = {
    high: { disk: 1500000, stream: 260000 },
    medium: { disk: 560000, stream: 100000 },
    low: { disk: 100000, stream: 24000 },
  };
  const SPRITE = { high: 1.3, medium: 1.7, low: 2.2 };
  const SCALE = 10,
    SHOWN_ORBIT = 40;
  const DISK = `#version 300 es
    precision highp float;precision highp int;precision highp sampler2D;
    ${K.NOISE}
    uniform mat4 uVP;uniform highp sampler2D uBB,uStream;
    uniform float uTime,uPhase,uGM1,uRin,uRout,uGain,uSize,uScale,uTmax;uniform vec3 uWD,uImpact;uniform int uKind,uSamples;
    out vec3 vColor;
    const float TAU=6.2831853;
    vec3 bb(float T){float i=clamp(log(T/1000.)/log(40.)*255.,0.,255.);int k=int(floor(i));
      return mix(texelFetch(uBB,ivec2(k,0),0).rgb,texelFetch(uBB,ivec2(min(k+1,255),0),0).rgb,fract(i));}
    // Corotating frame (x toward the donor) to the inertial frame of the scene.
    vec3 rot(vec3 p){float c=cos(uPhase),s=sin(uPhase);return vec3(c*p.x+s*p.z,p.y,-s*p.x+c*p.z);}
    void main(){
      uint id=uint(gl_VertexID);vec3 x;float T,b;
      if(uKind==0){
        // Keplerian disk around the white dwarf, surface density rising inward, two tidal spiral arms
        // fixed in the corotating frame, and the hot spot where the stream reaches the rim.
        float u=rnd(id,1u);float r=uRin*pow(uRout/uRin,pow(u,.8));
        float phi=rnd(id,2u)*TAU+uTime*sqrt(uGM1/(r*r*r));
        float arm=pow(.5+.5*cos(2.*(phi-uPhase)-5.*log(r/uRout)),6.)*smoothstep(.45*uRout,uRout,r);
        float z=.03*r*gauss(id,3u);
        x=uWD+vec3(r*cos(phi),z,-r*sin(phi));
        T=uTmax*pow(uRin/r,.75)*(1.+.35*arm);b=pow(uRin/r,.35)*(1.+2.5*arm);
        // Hot spot: the stream impact on the rim, fixed in the corotating frame, heated to about 12000 K by the shock.
        vec3 rel=x-uWD;float c=cos(-uPhase),sn=sin(-uPhase);vec3 co=vec3(c*rel.x+sn*rel.z,rel.y,-sn*rel.x+c*rel.z);
        float hs=exp(-dot(co-uImpact,co-uImpact)/(.09*uRout*uRout));T=mix(T,12000.,hs);b*=1.+18.*hs;
      }else{
        // Stream particles along the ballistic path from L1, in the corotating frame.
        float s=fract(rnd(id,4u)+uTime*.35);float i=s*float(uSamples-1);int k=int(floor(i));
        vec2 A=texelFetch(uStream,ivec2(k,0),0).xy,B=texelFetch(uStream,ivec2(min(k+1,uSamples-1),0),0).xy;
        vec2 p=mix(A,B,fract(i));float w=.008+.02*s;
        vec3 q=vec3(p.x,0.,-p.y)*uScale+w*uScale*vec3(gauss(id,5u),gauss(id,6u)*.6,gauss(id,7u));
        x=rot(q);T=3600.+9000.*s*s;b=.5+3.*s*s;
      }
      vColor=bb(T)*b*uGain;gl_Position=uVP*vec4(x,1.);gl_PointSize=uSize;}`;
  const POINT_FRAGMENT = `#version 300 es
    precision highp float;in vec3 vColor;out vec4 o;
    void main(){vec2 q=gl_PointCoord*2.-1.;float d=dot(q,q);if(d>1.)discard;o=vec4(vColor*exp(-3.*d),1.);}`;
  // Donor: convective red dwarf with limb darkening, gravity darkening toward L1 and the face heated by the
  // white dwarf and the disk.
  const DONOR = `#version 300 es
    precision highp float;in vec3 vWorld,vNormal,vLocal;in vec2 vUV;out vec4 o;
    uniform vec3 uEye,uCool,uHot,uWD;uniform float uTime,uIntensity,uL1;
    ${K.NOISE}
    void main(){vec3 n=normalize(vNormal),v=normalize(uEye-vWorld);float mu=max(0.,dot(n,v));
      float cells=fbm(normalize(vLocal)*14.+vec3(0,uTime*.02,0));
      float toward=max(0.,dot(n,normalize(uWD-vWorld)));
      float neck=smoothstep(.55,1.,-vLocal.x/uL1);
      vec3 c=mix(uCool,uHot,toward*toward*.65)*(1.+.18*cells)*(1.-.45*neck);
      float limb=1.-.7*(1.-mu);o=vec4(c*uIntensity*limb,1.);}`;

  function create(engine, ui) {
    const gl = engine.gl,
      model = O.byId.binaria.model,
      kit = K.kit(engine),
      labels = K.labels(ui.chart),
      counts = { ...COUNTS[engine.tier] };
    const disk = engine.program(DISK, POINT_FRAGMENT, 'diade-disk'),
      donorProgram = engine.program(K.MESH_VERTEX, DONOR, 'diade-donor');
    const bb = engine.dataTexture(O.blackbodyTable(256), 256, 1, 4);
    const mu = model.mu,
      wdLocal = [-mu * SCALE, 0, 0],
      donorLocal = [(1 - mu) * SCALE, 0, 0],
      l1 = (model.l1 - mu) * SCALE;
    const rIn = 0.018 * SCALE,
      rOut = model.diskRadius * SCALE,
      wdRadius = ((0.0102 * O.SI.Rsun) / model.a) * SCALE;
    const options = { disk: true, stream: true, lobes: true };
    let donor = null,
      stream = null,
      samples = 0,
      impact = null,
      lastFigure = 0;
    engine.work('donor', { mu, potential: model.l1Potential, level: engine.tier === 'low' ? 6 : 7 }).then(m => {
      donor = engine.mesh(m);
      engine.invalidate();
    });
    engine.work('stream', { mu, l1: model.l1 - mu, radius: model.diskRadius }).then(({ path }) => {
      samples = path.length;
      // Impact on the rim, relative to the white dwarf, in corotating scene coordinates.
      const end = path[path.length - 1];
      impact = { scene: [(end[0] + mu) * SCALE, 0, -end[1] * SCALE] };
      const data = new Float32Array(samples * 2);
      path.forEach((p, i) => data.set([p[0], p[1]], i * 2));
      stream = engine.dataTexture(data, samples, 1, 2);
      engine.invalidate();
    });
    // Roche lobe outlines in the orbital plane: the critical equipotential through L1, traced around each star.
    const lobe = center => {
      const pts = [],
        target = model.l1Potential * 1.0004;
      for (let i = 0; i <= 360; i++) {
        const a = (i / 360) * TAU,
          at = s => O.roche(mu, center + s * Math.cos(a), s * Math.sin(a), 0);
        // First exit from the lobe along the ray, then bisection.
        let lo = 0.01,
          hi = 0.02;
        while (hi < 1.2 && at(hi) < target) {
          lo = hi;
          hi += 0.01;
        }
        for (let k = 0; k < 40; k++) {
          const s = (lo + hi) / 2;
          if (at(s) < target) lo = s;
          else hi = s;
        }
        const s = (lo + hi) / 2;
        pts.push((center + s * Math.cos(a)) * SCALE, 0, -s * Math.sin(a) * SCALE);
      }
      return new Float32Array(pts);
    };
    const lobes = [lobe(-mu), lobe(1 - mu)];
    labels.set('wd', 'Nana bianca', 'body');
    labels.set('donor', 'Nana rossa', 'body');
    labels.set('l1', 'L1', 'resonance');
    labels.set('spot', 'Punto caldo', 'group');
    const phaseAt = time => (TAU * time) / SHOWN_ORBIT;
    const rotate = (p, a) => [Math.cos(a) * p[0] + Math.sin(a) * p[2], p[1], -Math.sin(a) * p[0] + Math.cos(a) * p[2]];
    function draw(frame) {
      engine.sky(frame, 0.3);
      const phase = phaseAt(frame.time),
        wd = rotate(wdLocal, phase),
        donorPos = rotate(donorLocal, phase);
      gl.enable(gl.DEPTH_TEST);
      if (donor) {
        gl.useProgram(donorProgram);
        engine.set(donorProgram, 'uVP', frame.camera.vp);
        engine.set(donorProgram, 'uModel', engine.model(donorPos, SCALE, [0, 1, 0], phase));
        engine.set(donorProgram, 'uEye', frame.camera.eye);
        engine.set(donorProgram, 'uCool', O.blackbody(3100));
        engine.set(donorProgram, 'uHot', O.blackbody(5200));
        engine.set(donorProgram, 'uWD', wd);
        engine.set(donorProgram, 'uTime', frame.time);
        engine.set(donorProgram, 'uIntensity', 1.6);
        engine.set(donorProgram, 'uL1', (1 - model.l1) * 1);
        donor.draw();
      }
      kit.drawStar(frame, { position: wd, radius: wdRadius, color: O.blackbody(25000), intensity: 30, grain: 4 });
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE);
      gl.depthMask(false);
      gl.useProgram(disk);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, bb);
      engine.set(disk, 'uBB', 0, 'int');
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, stream);
      engine.set(disk, 'uStream', 1, 'int');
      engine.set(disk, 'uVP', frame.camera.vp);
      engine.set(disk, 'uTime', frame.time * (TAU / SHOWN_ORBIT));
      engine.set(disk, 'uPhase', phase);
      engine.set(disk, 'uGM1', (1 - mu) * SCALE ** 3);
      engine.set(disk, 'uRin', rIn);
      engine.set(disk, 'uRout', rOut);
      engine.set(disk, 'uScale', SCALE);
      engine.set(disk, 'uWD', wd);
      engine.set(disk, 'uImpact', impact?.scene || [rOut, 0, 0]);
      engine.set(disk, 'uTmax', 9000);
      engine.set(disk, 'uSamples', samples, 'int');
      const size = Math.max(1, SPRITE[engine.tier] * frame.pixelRatio),
        density = (frame.width * frame.height) / 1e6 / Math.max(1, 0.9 * (size / 2) ** 2);
      engine.set(disk, 'uSize', size);
      if (options.disk) {
        engine.set(disk, 'uKind', 0, 'int');
        engine.set(disk, 'uGain', (0.05 * density * 1.5e6) / counts.disk);
        engine.points(counts.disk);
      }
      if (options.stream && stream) {
        engine.set(disk, 'uKind', 1, 'int');
        engine.set(disk, 'uGain', (0.06 * density * 2.6e5) / counts.stream);
        engine.points(counts.stream);
      }
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
      if (options.lobes)
        lobes.forEach((l, i) =>
          kit.drawLine(frame, 'lobe' + i, l, [0.75, 0.7, 1, 0.3], engine.model([0, 0, 0], 1, [0, 1, 0], phase)),
        );
      gl.depthMask(true);
      gl.disable(gl.BLEND);
      kit.drawGlow(frame, { position: wd, size: 0.6, color: [1.2, 1.4, 2], falloff: 8 });
      labels.hideAll();
      labels.place('wd', engine.project([wd[0], 1.3, wd[2]]));
      labels.place('donor', engine.project([donorPos[0], 3.4, donorPos[2]]));
      labels.place('l1', engine.project(rotate([l1, 0, 0], phase)), options.lobes);
      if (impact)
        labels.place(
          'spot',
          engine.project(rotate([wdLocal[0] + impact.scene[0], -0.9, impact.scene[2]], phase)),
          options.stream,
        );
      // Orbital phase seen from the camera: 0 when the donor passes in front of the white dwarf.
      if (performance.now() - lastFigure > 250) {
        lastFigure = performance.now();
        const eye = frame.camera.eye,
          inclination = Math.acos(Math.abs(eye[1]) / Math.hypot(...eye)),
          seen = ((((Math.atan2(-donorPos[2], donorPos[0]) - Math.atan2(-eye[2], eye[0])) / TAU) % 1) + 1) % 1;
        ui.figure?.({ inclination, phase: seen });
      }
    }
    return {
      draw,
      near: d => d * 0.004,
      far: d => d * 30,
      options,
      setOption(key, value) {
        options[key] = value;
        engine.invalidate();
      },
      reduce() {
        if (counts.disk < 120000) return engine.reduceResolution();
        for (const k of Object.keys(counts)) counts[k] = Math.round(counts[k] * 0.7);
        return true;
      },
      debug: () => ({
        object: 'binaria',
        particles: counts.disk + counts.stream,
        donor: donor ? donor.count / 3 : 0,
        streamSamples: samples,
        options: { ...options },
      }),
      dispose() {
        kit.dispose();
        labels.dispose();
      },
    };
  }
  root.GeoObjectScenes = root.GeoObjectScenes || {};
  root.GeoObjectScenes.binaria = {
    create,
    exposure: 1,
    camera: { azimuth: 0.3, elevation: 0.42, distance: 26, minDistance: 3, maxDistance: 90, fov: (40 * Math.PI) / 180 },
  };
})(globalThis);
