/* Clio: a comet on an eccentric orbit. In the orbital view every dust grain leaves the nucleus at its emission
   time and then moves under the gravity of the star reduced by radiation pressure, (1 - beta) GM, integrated
   in the vertex shader: the dust tail curves behind the orbit, the ion tail follows the solar wind away from the
   star. The close view shows the nucleus as a dense textured mesh with jets from its sunlit active areas.
   Units: AU and years in the orbital views, kilometres and seconds in the close view. */
(function (root) {
  'use strict';
  const O = root.GeoObjects,
    K = root.GeoObjectKit;
  const COUNTS = {
    high: { dust: 1400000, ions: 700000, coma: 900000 },
    medium: { dust: 520000, ions: 260000, coma: 340000 },
    low: { dust: 90000, ions: 50000, coma: 60000 },
  };
  const SPRITE = { high: 1.3, medium: 1.7, low: 2.2 };
  // The passage within 1.4 years of perihelion repeats every 48 s on screen.
  const WINDOW = 1.4,
    LOOP = 48;
  const ORBIT = `
    uniform float uA,uE,uTime,uPeriod;
    const float TAU=6.2831853,PI=3.14159265,GM=39.478418;
    // Position and velocity (AU, AU/yr) on the orbit of the nucleus, t in years from perihelion. Perihelion on +x.
    void orbit(float t,out vec3 x,out vec3 v){
      float M=TAU*t/uPeriod;M=mod(M+PI,TAU)-PI;
      float E=M+.85*uE*sign(sin(M)+1e-6);
      for(int i=0;i<14;i++)E-=(E-uE*sin(E)-M)/(1.-uE*cos(E));
      float b=uA*sqrt(1.-uE*uE),k=sqrt(GM/uA)/(1.-uE*cos(E));
      x=vec3(uA*(cos(E)-uE),0.,-b*sin(E));v=vec3(-k*sin(E),0.,-k*sqrt(1.-uE*uE)*cos(E));}`;
  const TAIL = `#version 300 es
    precision highp float;precision highp int;
    ${K.NOISE}
    ${ORBIT}
    uniform mat4 uVP;uniform vec3 uEye,uOrigin;uniform float uGain,uSize,uActive,uAge;uniform int uKind;
    out vec3 vColor;
    vec3 acc(vec3 p,float s){float r=length(p);return -s*GM*p/(r*r*r);}
    void main(){
      uint id=uint(gl_VertexID);
      float age=uAge*pow(rnd(id,1u),uKind==0?1.5:1.1);
      float te=uTime-age;vec3 x,v;orbit(te,x,v);
      float r=length(x),activity=r<uActive?pow(1./r,2.)*(1.-smoothstep(uActive*.75,uActive,r)):0.;
      vec3 sun=x/r;vec3 col;float b;
      if(uKind==0){
        // Dust: beta from 0.005 to 1 (smaller grains, larger beta), ejected mostly toward the sunlit side.
        float beta=.02+.98*pow(rnd(id,2u),1.4);
        vec3 dir=normalize(vec3(gauss(id,3u),gauss(id,4u),gauss(id,5u))-1.2*sun);
        v+=dir*.12*sqrt(beta);
        float s=1.-beta,h=age/10.;
        for(int i=0;i<10;i++){
          vec3 k1=v,a1=acc(x,s),k2=v+.5*h*a1,a2=acc(x+.5*h*k1,s),k3=v+.5*h*a2,a3=acc(x+.5*h*k2,s),k4=v+h*a3,a4=acc(x+h*k3,s);
          x+=h/6.*(k1+2.*k2+2.*k3+k4);v+=h/6.*(a1+2.*a2+2.*a3+a4);}
        col=mix(vec3(1.,.86,.62),vec3(.95,.92,.86),beta);
        b=activity*(.55+.45*beta)/(dot(x,x));
      }else{
        // Ions: picked up by the solar wind (about 400 km/s, 84 AU/yr) along the aberrated anti-solar direction.
        vec3 wind=normalize(sun*84.-v);float ray=floor(rnd(id,6u)*9.);
        vec3 side=normalize(cross(wind,vec3(0,1,0)));vec3 up=cross(side,wind);
        float sp=age*84.;
        float wave=.008*sin(sp*14.+ray*2.1+uTime*20.)*sp;
        x+=v*age*.2+wind*sp+(side*(rnd(uint(ray),7u)-.5)*.05*sp+up*(rnd(uint(ray),8u)-.5)*.035*sp)
          +side*wave+.004*sp*vec3(gauss(id,9u),gauss(id,10u),gauss(id,11u));
        col=vec3(.32,.58,1.);b=activity*1.6*(1.-age/uAge);
      }
      vColor=col*b*uGain;gl_Position=uVP*vec4(x-uOrigin,1.);gl_PointSize=uSize;}`;
  // Close view: gas and dust leaving the sunlit active areas of the rotating nucleus, pushed away from the star.
  const COMA = `#version 300 es
    precision highp float;precision highp int;
    ${K.NOISE}
    uniform mat4 uVP,uBody;uniform vec3 uSun;uniform float uTime,uGain,uSize,uRadius;uniform int uSpots;
    out vec3 vColor;
    void main(){
      uint id=uint(gl_VertexID);uint spot=id%uint(uSpots);bool jet=rnd(id,1u)<.55;
      float age=fract(rnd(id,2u)+uTime*.02*(.6+.8*rnd(id,3u)));
      vec3 n=normalize(vec3(gauss(spot,4u),gauss(spot,5u),gauss(spot,6u)));
      if(!jet)n=normalize(vec3(gauss(id,7u),gauss(id,8u),gauss(id,9u)));
      // Emission point and direction rotate with the nucleus; the sunlit side is more active.
      vec3 base=normalize(mat3(uBody)*n)*uRadius;vec3 dir=normalize(mat3(uBody)*n+(jet?.18:.6)*vec3(gauss(id,10u),gauss(id,11u),gauss(id,12u)));
      float light=max(0.,dot(normalize(base),uSun));
      float d=age*uRadius*14.;
      vec3 x=base+dir*d-uSun*age*age*uRadius*9.;
      float b=(jet?2.2:1.)*(.15+light)*(1.-age)*(1.-age)/(1.+d*d/(uRadius*uRadius));
      vColor=mix(vec3(.95,.9,.82),vec3(.6,.75,1.),rnd(id,13u)*.5)*b*uGain;
      gl_Position=uVP*vec4(x,1.);gl_PointSize=uSize;}`;
  const POINT_FRAGMENT = `#version 300 es
    precision highp float;in vec3 vColor;out vec4 o;
    void main(){vec2 q=gl_PointCoord*2.-1.;float d=dot(q,q);if(d>1.)discard;o=vec4(vColor*exp(-3.*d),1.);}`;

  function create(engine, ui) {
    const gl = engine.gl,
      model = O.byId.cometa.model,
      kit = K.kit(engine),
      labels = K.labels(ui.chart),
      counts = { ...COUNTS[engine.tier] };
    const tail = engine.program(TAIL, POINT_FRAGMENT, 'clio-tails'),
      coma = engine.program(COMA, POINT_FRAGMENT, 'clio-coma');
    const crust = engine.imageTexture(
      'assets/space/objects/' + (engine.tier === 'high' ? 'nucleo-4k' : 'nucleo') + '.webp',
    );
    const options = { dust: true, ions: true, orbit: true };
    let view = 'orbit',
      nucleus = null,
      shadow = null;
    ui.status?.('Costruzione del nucleo…');
    engine
      .work('smallBody', {
        seed: 5,
        level: engine.tier === 'low' ? 6 : 7,
        axes: [1.45, 0.86, 0.8],
        lobes: 1,
        craterCount: 1600,
        rough: 0.03,
        largest: 0.22,
      })
      .then(m => {
        nucleus = engine.mesh(m);
        shadow = engine.shadowMap(engine.tier === 'low' ? 1024 : 2048);
        ui.status?.('');
        engine.invalidate();
      });
    labels.set('star', 'Stella', 'body');
    labels.set('peri', 'Perielio', 'resonance');
    labels.set('comet', 'Clio', 'body');
    labels.set('active', 'Limite di attività (3 UA)', 'group');
    // Orbit polyline of the inner passage (r < 6 AU) for the overlay.
    const orbitLine = (() => {
      const pts = [];
      for (let i = -400; i <= 400; i++) {
        const st = O.cometState(model, (i / 400) * 7.5);
        if (st.r < 6.5) pts.push(st.x, 0, -st.y);
      }
      return new Float32Array(pts);
    })();
    const yearsAt = time => (((time / LOOP) % 1) * 2 - 1) * WINDOW;
    function state(t) {
      const s = O.cometState(model, t);
      return { x: [s.x, 0, -s.y], r: s.r };
    }
    function drawTails(frame, origin) {
      const t = yearsAt(frame.time);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE);
      gl.depthMask(false);
      gl.useProgram(tail);
      engine.set(tail, 'uVP', frame.camera.vp);
      engine.set(tail, 'uOrigin', origin);
      engine.set(tail, 'uA', model.a);
      engine.set(tail, 'uE', model.eccentricity);
      engine.set(tail, 'uPeriod', model.period);
      engine.set(tail, 'uTime', t);
      engine.set(tail, 'uActive', model.active);
      const size = Math.max(1, SPRITE[engine.tier] * frame.pixelRatio),
        density = (frame.width * frame.height) / 1e6 / Math.max(1, 0.9 * (size / 2) ** 2);
      engine.set(tail, 'uSize', size);
      if (options.dust) {
        engine.set(tail, 'uKind', 0, 'int');
        engine.set(tail, 'uAge', 0.16);
        engine.set(tail, 'uGain', (0.05 * density * 1.4e6) / counts.dust);
        engine.points(counts.dust);
      }
      if (options.ions) {
        engine.set(tail, 'uKind', 1, 'int');
        engine.set(tail, 'uAge', 0.008);
        engine.set(tail, 'uGain', (0.11 * density * 7e5) / counts.ions);
        engine.points(counts.ions);
      }
      gl.depthMask(true);
      gl.disable(gl.BLEND);
      return t;
    }
    function drawOrbitView(frame) {
      engine.sky(frame, 0.18);
      const t = yearsAt(frame.time),
        c = state(t);
      if (view === 'tail') engine.camera.target = c.x.slice();
      gl.enable(gl.DEPTH_TEST);
      kit.drawStar(frame, { position: [0, 0, 0], radius: 0.07, color: O.blackbody(5772), intensity: 26, grain: 7 });
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
      gl.depthMask(false);
      if (options.orbit) {
        kit.drawLine(frame, 'orbit', orbitLine, [0.6, 0.85, 1, 0.3]);
        kit.drawLine(frame, 'active', K.circle(model.active, 512), [0.95, 0.78, 0.5, 0.14]);
      }
      gl.depthMask(true);
      drawTails(frame, [0, 0, 0]);
      const activity = c.r < model.active ? Math.min(1.5, 1 / (c.r * c.r)) : 0;
      kit.drawGlow(frame, {
        position: c.x,
        size: 0.05 + 0.18 * activity,
        color: [0.5 + activity, 0.6 + activity, 0.7 + activity * 1.2],
        falloff: 9,
      });
      kit.drawGlow(frame, { position: [0, 0, 0], size: 1.2, color: [2, 1.75, 1.4], falloff: 9 });
      labels.hideAll();
      labels.place('star', engine.project([0, 0.1, 0]));
      labels.place('peri', engine.project([model.perihelion, -0.05, 0]), options.orbit);
      labels.place('comet', engine.project([c.x[0], c.x[1] + 0.08, c.x[2]]));
      labels.place('active', engine.project([0, 0, -model.active]), options.orbit);
      ui.status?.(
        'Giorni dal perielio: ' +
          Math.round(t * 365.25) +
          ' · distanza dalla stella ' +
          c.r.toFixed(2).replace('.', ',') +
          ' UA',
      );
    }
    function drawNucleus(frame) {
      const t = yearsAt(frame.time),
        c = state(t),
        sun = c.x.map(v => -v / c.r);
      engine.sky(frame, 0.35);
      if (!nucleus) return;
      const spin = frame.time * 0.21,
        radius = 2.1,
        body = engine.model(
          [0, 0, 0],
          radius,
          [0.15, 1, 0.2].map(v => v / Math.hypot(0.15, 1, 0.2)),
          spin,
        );
      gl.enable(gl.DEPTH_TEST);
      const lightVP = kit.renderShadow(shadow, frame, sun, [0, 0, 0], 4.5, [[nucleus, body]]);
      kit.drawRock(frame, nucleus, {
        matrix: body,
        albedo: crust,
        lightDir: sun,
        power: 2.4 / (c.r * c.r),
        scale: 2.2,
        bump: 0.035,
        tint: [1, 1, 1],
        albedoScale: 0.6,
        shadow,
        lightVP,
        ambient: 0.004,
      });
      const active = c.r < model.active ? 1 / (c.r * c.r) : 0;
      if (active > 0) {
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.ONE, gl.ONE);
        gl.depthMask(false);
        gl.useProgram(coma);
        engine.set(coma, 'uVP', frame.camera.vp);
        engine.set(coma, 'uBody', body);
        engine.set(coma, 'uSun', sun);
        engine.set(coma, 'uTime', frame.time);
        engine.set(coma, 'uRadius', radius * 1.05);
        engine.set(coma, 'uSpots', 7, 'int');
        const size = Math.max(1, SPRITE[engine.tier] * frame.pixelRatio),
          density = (frame.width * frame.height) / 1e6 / Math.max(1, 0.9 * (size / 2) ** 2);
        engine.set(coma, 'uSize', size);
        engine.set(coma, 'uGain', (0.3 * Math.min(2.5, active) * density * 9e5) / counts.coma);
        engine.points(counts.coma);
        gl.depthMask(true);
        gl.disable(gl.BLEND);
      }
      labels.hideAll();
      ui.status?.(
        'Distanza dalla stella ' + c.r.toFixed(2).replace('.', ',') + ' UA' + (active ? '' : ' · nucleo inattivo'),
      );
    }
    function draw(frame) {
      if (view === 'nucleus') drawNucleus(frame);
      else drawOrbitView(frame);
    }
    function setView(next) {
      view = next;
      if (next === 'nucleus') {
        // Camera on the day side, about 50 degrees from the direction of the star.
        const c = state(yearsAt(engine.time())),
          sun = c.x.map(v => -v / c.r);
        Object.assign(engine.camera, { minDistance: 5, maxDistance: 120 });
        engine.moveTo(
          { azimuth: Math.atan2(sun[0], sun[2]) + 0.9, elevation: 0.3, distance: 11, target: [0, 0, 0] },
          0,
        );
      } else if (next === 'tail') {
        Object.assign(engine.camera, { minDistance: 0.15, maxDistance: 8 });
        engine.moveTo({ azimuth: 1.1, elevation: 0.45, distance: 1.1 }, 0);
      } else {
        Object.assign(engine.camera, { minDistance: 1, maxDistance: 30 });
        engine.moveTo({ azimuth: 0.4, elevation: 0.85, distance: 5, target: [0.4, 0, 0] }, 0);
      }
      ui.status?.('');
    }
    return {
      draw,
      view: setView,
      near: d => d * 0.004,
      far: d => d * 40,
      options,
      setOption(key, value) {
        options[key] = value;
        engine.invalidate();
      },
      reduce() {
        if (counts.dust < 120000) return engine.reduceResolution();
        for (const k of Object.keys(counts)) counts[k] = Math.round(counts[k] * 0.7);
        return true;
      },
      debug: () => ({
        object: 'cometa',
        view,
        particles: counts.dust + counts.ions,
        mesh: nucleus ? nucleus.count / 3 : 0,
        options: { ...options },
      }),
      dispose() {
        kit.dispose();
        labels.dispose();
      },
    };
  }
  root.GeoObjectScenes = root.GeoObjectScenes || {};
  root.GeoObjectScenes.cometa = {
    create,
    exposure: 1,
    camera: {
      azimuth: 0.4,
      elevation: 0.85,
      distance: 5,
      target: [0.4, 0, 0],
      minDistance: 1,
      maxDistance: 30,
      fov: (40 * Math.PI) / 180,
      startTime: LOOP * 0.42,
    },
  };
})(globalThis);
