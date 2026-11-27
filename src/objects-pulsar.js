/* Faro: a young pulsar. The neutron star rotates about the vertical axis with its magnetic dipole inclined by
   chi; plasma flows along the closed field lines inside the light cylinder, the radio beams leave the magnetic
   poles as hollow cones, and beyond the light cylinder the current sheet of the striped wind waves with the
   rotation. Units: radius of the neutron star (12 km). The rotation is shown slowed down. */
(function (root) {
  'use strict';
  const O = root.GeoObjects,
    K = root.GeoObjectKit,
    TAU = Math.PI * 2;
  const COUNTS = {
    high: { field: 1400000, beams: 700000, wind: 1300000 },
    medium: { field: 500000, beams: 260000, wind: 480000 },
    low: { field: 90000, beams: 50000, wind: 80000 },
  };
  const SPRITE = { high: 1.4, medium: 1.8, low: 2.3 };
  // One turn every 2.5 s on screen: the real period of 0.04 s is slowed down 62.5 times.
  const SHOWN_PERIOD = 2.5;
  const PARTICLES = `#version 300 es
    precision highp float;precision highp int;
    ${K.NOISE}
    uniform mat4 uVP;uniform float uTime,uSpin,uChi,uLC,uGain,uSize;uniform int uKind;
    out vec3 vColor;
    const float TAU=6.2831853,PI=3.14159265;
    // Rotation about the vertical spin axis, then the magnetic frame tilted by chi about x.
    vec3 spin(vec3 p){float c=cos(uSpin),s=sin(uSpin);return vec3(c*p.x+s*p.z,p.y,-s*p.x+c*p.z);}
    vec3 magnetic(vec3 p){float c=cos(uChi),s=sin(uChi);return spin(vec3(p.x,c*p.y-s*p.z,s*p.y+c*p.z));}
    void main(){
      uint id=uint(gl_VertexID);vec3 x;vec3 col;float b;
      if(uKind==0){
        // Closed dipole field lines r = L sin^2(theta), from one footpoint on the surface to the other.
        uint line=id>>8u;float L=exp(mix(log(1.6),log(uLC*.98),pow(rnd(line,1u),1.7)));
        float tmin=asin(sqrt(1./L));float phim=rnd(line,2u)*TAU;
        float s=fract(rnd(id,3u)+uTime*(.06+.5/L)*(rnd(line,4u)<.5?1.:-1.));
        float th=mix(tmin,PI-tmin,s);float r=L*sin(th)*sin(th);
        x=magnetic(vec3(r*sin(th)*cos(phim),r*cos(th),r*sin(th)*sin(phim)));
        col=mix(vec3(.35,.75,1.),vec3(.75,.55,1.),smoothstep(10.,uLC,L));
        b=pow(9./(r+6.),.85)*(.6+.4*rnd(line,5u));
      }else if(uKind==1){
        // Hollow-cone beams above the two magnetic poles, moving outward at the speed of light.
        float pole=(id&1u)==1u?1.:-1.;float s=fract(rnd(id,6u)+uTime*.35);
        float d=1.2+uLC*.95*s;float rho=(.17+.05*rnd(id,7u))*(.25+.75*smoothstep(1.,25.,d));
        float az=rnd(id,8u)*TAU;
        x=magnetic(d*vec3(sin(rho)*cos(az),pole*cos(rho),sin(rho)*sin(az)));
        col=vec3(.92,.86,1.);b=3.2*(1.-s)*(1.-s)*(.5+rnd(id,9u));
      }else{
        // Current sheet of the striped wind: latitude oscillates with amplitude chi and phase phi - Omega (t - r/c).
        float s=fract(rnd(id,10u)+uTime*.05);float r=uLC*(1.+2.6*s);float ph=rnd(id,11u)*TAU;
        float lat=atan(tan(uChi)*sin(ph-uSpin+r/uLC))+.03*gauss(id,12u);
        x=vec3(r*cos(lat)*cos(ph),r*sin(lat),r*cos(lat)*sin(ph));
        col=mix(vec3(1.,.45,.75),vec3(.55,.5,1.),rnd(id,13u));b=.55*(1.-s)*smoothstep(0.,.06,s);
      }
      vColor=col*b*uGain;gl_Position=uVP*vec4(x,1.);gl_PointSize=uSize;}`;
  const POINT_FRAGMENT = `#version 300 es
    precision highp float;in vec3 vColor;out vec4 o;
    void main(){vec2 q=gl_PointCoord*2.-1.;float d=dot(q,q);if(d>1.)discard;o=vec4(vColor*exp(-3.*d),1.);}`;
  // Neutron star surface: thermal glow with a mottled crust and hot polar caps around the magnetic poles.
  const SURFACE = `#version 300 es
    precision highp float;in vec3 vWorld,vNormal,vLocal;in vec2 vUV;out vec4 o;
    uniform vec3 uEye,uPole,uBase,uCap;uniform float uCapAngle,uIntensity;
    ${K.NOISE}
    void main(){vec3 n=normalize(vNormal),v=normalize(uEye-vWorld);float mu=max(0.,dot(n,v));
      float crust=fbm(normalize(vLocal)*7.)*.5+.5;
      float cap=max(smoothstep(cos(uCapAngle*2.2),cos(uCapAngle),dot(n,uPole)),smoothstep(cos(uCapAngle*2.2),cos(uCapAngle),-dot(n,uPole)));
      vec3 c=mix(uBase*(.75+.5*crust),uCap*3.,cap)*(.55+.45*mu);
      o=vec4(c*uIntensity,1.);}`;

  function create(engine, ui) {
    const gl = engine.gl,
      model = O.byId.pulsar.model,
      kit = K.kit(engine),
      labels = K.labels(ui.chart),
      counts = { ...COUNTS[engine.tier] };
    const LC = model.lightCylinder / model.radius,
      chi = (model.inclination * Math.PI) / 180,
      capAngle = Math.asin(Math.sqrt(model.radius / model.lightCylinder));
    const particles = engine.program(PARTICLES, POINT_FRAGMENT, 'faro-particles'),
      surface = engine.program(K.MESH_VERTEX, SURFACE, 'faro-surface');
    const options = { field: true, beams: true, wind: true, cylinder: true };
    let star = null;
    engine.work('sphere', { level: engine.tier === 'low' ? 5 : 7 }).then(m => {
      star = engine.mesh(m);
      engine.invalidate();
    });
    labels.set('lc', 'Cilindro di luce', 'group');
    labels.set('spin', 'Asse di rotazione', 'body');
    labels.set('pole', 'Polo magnetico', 'resonance');
    const spinAngle = t => (TAU * t) / SHOWN_PERIOD;
    const magneticAxis = s => {
      const p = [0, Math.cos(chi), Math.sin(chi)];
      return [Math.cos(s) * p[0] + Math.sin(s) * p[2], p[1], -Math.sin(s) * p[0] + Math.cos(s) * p[2]];
    };
    const cylinder = [];
    for (const y of [-0.62, 0.62]) cylinder.push(K.circle(LC, 360, y * LC));
    const verticals = new Float32Array(16 * 2 * 3);
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * TAU;
      verticals.set(
        [Math.cos(a) * LC, -0.62 * LC, Math.sin(a) * LC, Math.cos(a) * LC, 0.62 * LC, Math.sin(a) * LC],
        i * 6,
      );
    }
    let lastFigure = 0;
    function draw(frame) {
      engine.sky(frame, 0.35);
      const s = spinAngle(frame.time),
        m = magneticAxis(s);
      gl.enable(gl.DEPTH_TEST);
      if (star) {
        gl.useProgram(surface);
        engine.set(surface, 'uVP', frame.camera.vp);
        engine.set(surface, 'uModel', engine.model([0, 0, 0], 1, [0, 1, 0], s));
        engine.set(surface, 'uEye', frame.camera.eye);
        engine.set(surface, 'uPole', m);
        engine.set(surface, 'uBase', O.blackbody(16000));
        engine.set(surface, 'uCap', O.blackbody(32000));
        engine.set(surface, 'uCapAngle', capAngle * 3);
        engine.set(surface, 'uIntensity', 1.1);
        star.draw();
      }
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
      gl.depthMask(false);
      if (options.cylinder) {
        cylinder.forEach((c, i) => kit.drawLine(frame, 'lc' + i, c, [0.55, 0.8, 1, 0.22]));
        kit.drawLine(frame, 'lcv', verticals, [0.55, 0.8, 1, 0.1], engine.model(), gl.LINES);
      }
      kit.drawLine(
        frame,
        'spin',
        new Float32Array([0, -LC * 1.4, 0, 0, LC * 1.4, 0]),
        [0.9, 0.85, 0.6, 0.35],
        engine.model(),
        gl.LINES,
      );
      const axis = new Float32Array([...m.map(v => -v * LC), ...m.map(v => v * LC)]);
      kit.updateLine('magnetic', axis);
      kit.drawLine(frame, 'magnetic', axis, [1, 0.75, 0.45, 0.4], engine.model(), gl.LINES);
      gl.blendFunc(gl.ONE, gl.ONE);
      gl.useProgram(particles);
      engine.set(particles, 'uVP', frame.camera.vp);
      engine.set(particles, 'uTime', frame.time);
      engine.set(particles, 'uSpin', s);
      engine.set(particles, 'uChi', chi);
      engine.set(particles, 'uLC', LC);
      const size = Math.max(1, SPRITE[engine.tier] * frame.pixelRatio),
        density = (frame.width * frame.height) / 1e6 / Math.max(1, 0.9 * (size / 2) ** 2);
      engine.set(particles, 'uSize', size);
      const pass = (kind, n, gain) => {
        engine.set(particles, 'uKind', kind, 'int');
        engine.set(particles, 'uGain', gain * density);
        engine.points(n);
      };
      if (options.field) pass(0, counts.field, (1.6 * 1.4e6) / counts.field);
      if (options.beams) pass(1, counts.beams, (0.3 * 7e5) / counts.beams);
      if (options.wind) pass(2, counts.wind, (0.5 * 1.3e6) / counts.wind);
      gl.depthMask(true);
      gl.disable(gl.BLEND);
      // Far away the star is smaller than a pixel: a glow keeps its position visible.
      const far = Math.min(1, Math.max(0, (frame.camera.distance - 25) / 80));
      if (far > 0)
        kit.drawGlow(frame, { position: [0, 0, 0], size: 6, color: [0.9 * far, 0.95 * far, 1.4 * far], falloff: 8 });
      labels.hideAll();
      labels.place('lc', engine.project([LC * 0.7, 0.62 * LC, -LC * 0.7]), options.cylinder);
      labels.place('spin', engine.project([0, LC * 1.25, 0]));
      labels.place('pole', engine.project(m.map(v => v * Math.min(LC * 0.8, frame.camera.distance * 0.25 + 3))));
      // Pulse profile seen from the current direction of the camera, refreshed a few times per second.
      const eye = frame.camera.eye,
        zeta = Math.acos(eye[1] / Math.hypot(...eye));
      if (performance.now() - lastFigure > 250) {
        lastFigure = performance.now();
        ui.figure?.({ chi, zeta, phase: (s / TAU) % 1 });
      }
    }
    return {
      draw,
      view(next) {
        if (next === 'surface') engine.moveTo({ distance: 5.5, elevation: 0.35, target: [0, 0, 0] }, 0);
        else engine.moveTo({ distance: 520, elevation: 0.32, target: [0, 0, 0] }, 0);
      },
      near: d => d * 0.004,
      far: d => d * 30,
      options,
      setOption(key, value) {
        options[key] = value;
        engine.invalidate();
      },
      reduce() {
        if (counts.field < 150000) return engine.reduceResolution();
        for (const k of Object.keys(counts)) counts[k] = Math.round(counts[k] * 0.7);
        return true;
      },
      debug: () => ({
        object: 'pulsar',
        particles: counts.field + counts.beams + counts.wind,
        lightCylinder: LC,
        options: { ...options },
      }),
      dispose() {
        kit.dispose();
        labels.dispose();
      },
    };
  }
  root.GeoObjectScenes = root.GeoObjectScenes || {};
  root.GeoObjectScenes.pulsar = {
    create,
    exposure: 1,
    bloom: 0.08,
    camera: {
      azimuth: 0.7,
      elevation: 0.32,
      distance: 520,
      minDistance: 3.2,
      maxDistance: 1500,
      fov: (40 * Math.PI) / 180,
    },
  };
})(globalThis);
