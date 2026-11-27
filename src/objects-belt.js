/* Lapis: a main-sequence star, a giant planet and an asteroid belt of Keplerian orbits. The Kirkwood gaps are
   carved in the distribution of semimajor axes; Hildas follow the 3:2 resonance and Trojans share the orbit of
   the giant 60 degrees ahead and behind. A close view shows one asteroid as a dense textured mesh with shadows.
   Units: astronomical units and years in the belt view, kilometres in the close view. */
(function (root) {
  'use strict';
  const O = root.GeoObjects,
    K = root.GeoObjectKit,
    TAU = Math.PI * 2;
  const COUNTS = { high: 1600000, medium: 600000, low: 120000 };
  const SPRITE = { high: 1.3, medium: 1.7, low: 2.2 };
  const YEARS_PER_SECOND = 0.08,
    GIANT_PHASE = 1.1;
  const BELT_VERTEX = `#version 300 es
    precision highp float;precision highp int;
    ${K.NOISE}
    uniform highp sampler2D uAxis;uniform mat4 uVP;uniform vec3 uEye,uOrigin;
    uniform float uTime,uGiant,uGiantPhase,uGain,uSize,uEcc,uGroups,uSkyMode;
    out vec3 vColor;
    const float TAU=6.2831853,PI=3.14159265;
    float axisOf(float u){float i=u*1023.;int k=int(floor(i));
      return mix(texelFetch(uAxis,ivec2(k,0),0).r,texelFetch(uAxis,ivec2(min(k+1,1023),0),0).r,fract(i));}
    // Position on a Keplerian orbit (star of one solar mass, a in AU, t in years). World y is the ecliptic pole.
    vec3 kepler(float a,float e,float inc,float node,float peri,float M){
      float E=M;for(int i=0;i<6;i++)E-=(E-e*sin(E)-M)/(1.-e*cos(E));
      float x=a*(cos(E)-e),y=a*sqrt(1.-e*e)*sin(E);
      float cw=cos(peri),sw=sin(peri),cn=cos(node),sn=sin(node),ci=cos(inc),si=sin(inc);
      float X=(cw*cn-sw*sn*ci)*x+(-sw*cn-cw*sn*ci)*y;
      float Y=(cw*sn+sw*cn*ci)*x+(-sw*sn+cw*cn*ci)*y;
      float Z=(sw*si)*x+(cw*si)*y;return vec3(X,Z,-Y);}
    void main(){
      uint id=uint(gl_VertexID);float g=rnd(id,1u);
      float node=rnd(id,2u)*TAU,peri=rnd(id,3u)*TAU,a,e,inc,M,albedo;
      float lambdaJ=uGiantPhase+TAU*uTime/pow(uGiant,1.5);
      if(g<.06*uGroups){
        // Trojans: mean longitude 60 degrees ahead (L4) or behind (L5) the giant, with a libration spread.
        a=uGiant*(1.+.008*gauss(id,4u));e=.06*abs(gauss(id,5u));inc=.22*abs(gauss(id,6u));
        float lam=lambdaJ+(rnd(id,7u)<.55?PI/3.:-PI/3.)+.32*gauss(id,8u);M=lam-node-peri;albedo=.06;
      }else if(g<.09*uGroups){
        // Hildas in the 3:2 resonance: the longitude of perihelion stays at lambda_J0 - 2 M0 / 3.
        a=uGiant*pow(2./3.,2./3.)*(1.+.006*gauss(id,9u));e=.17+.05*rnd(id,10u);inc=.1*abs(gauss(id,11u));
        float M0=rnd(id,12u)*TAU;float varpi=uGiantPhase-2.*M0/3.+.25*gauss(id,13u);
        peri=varpi-node;M=M0+TAU*uTime/pow(a,1.5);albedo=.05;
      }else{
        a=axisOf(rnd(id,14u));e=min(.3,.09*abs(gauss(id,15u))+.02);inc=.12*abs(gauss(id,16u));
        M=rnd(id,17u)*TAU+TAU*uTime/pow(a,1.5);
        float carbon=smoothstep(2.3,3.3,a)*.75+.1;albedo=rnd(id,18u)<carbon?.06:.22;
      }
      vec3 x=kepler(a,e*uEcc,inc,node,peri,M);
      // Reflected light: albedo, size, distance from the star and from the camera, Lambert phase function.
      float r=length(x);vec3 toStar=-x/r,toEye=normalize(uEye-x);
      float ph=acos(clamp(dot(toStar,toEye),-1.,1.));float phase=((PI-ph)*cos(ph)+sin(ph))/PI;
      float size=pow(max(rnd(id,19u),1e-4),-.55);
      float d=length(uEye-x);
      vec3 tint=albedo>.1?vec3(1.,.82,.64):vec3(.78,.76,.74);
      float dist=uSkyMode>.5?1./(d*d+.02):1./(1.+d*d*.002);
      float boost=g<.09*uGroups?3.:1.;
      vColor=tint*albedo*boost*min(size,40.)*phase/(r*r)*uGain*dist;
      // Seen from inside the belt the asteroids are directions on the sky, beyond every mesh of the scene.
      if(uSkyMode>.5){vec4 q=uVP*vec4(normalize(x-uOrigin),0.);q.z=q.w*.9999;gl_Position=q;}
      else gl_Position=uVP*vec4(x-uOrigin,1.);
      gl_PointSize=uSize;}`;
  const POINT_FRAGMENT = `#version 300 es
    precision highp float;in vec3 vColor;out vec4 o;
    void main(){vec2 q=gl_PointCoord*2.-1.;float d=dot(q,q);if(d>1.)discard;o=vec4(vColor*exp(-3.*d),1.);}`;

  function axisTable(model, n = 1024) {
    const lo = 1.9,
      hi = 3.6,
      grid = 8192,
      cdf = new Float64Array(grid + 1),
      a = i => lo + ((hi - lo) * i) / grid,
      hilda = model.resonances.find(r => r.label === '3:2').a;
    for (let i = 1; i <= grid; i++) {
      const x = a(i - 0.5);
      // The Hilda group is drawn separately, on its resonant orbits.
      cdf[i] = cdf[i - 1] + Math.max(0, O.beltDensity(x, model) - 0.11 * Math.exp(-(((x - hilda) / 0.05) ** 2)));
    }
    const out = new Float32Array(n);
    let j = 0;
    for (let k = 0; k < n; k++) {
      const target = (k / (n - 1)) * cdf[grid];
      while (j < grid - 1 && cdf[j + 1] < target) j++;
      out[k] = a(j + (target - cdf[j]) / (cdf[j + 1] - cdf[j] || 1));
    }
    return out;
  }
  function create(engine, ui) {
    const gl = engine.gl,
      model = O.byId.asteroidi.model,
      kit = K.kit(engine),
      labels = K.labels(ui.chart),
      count = { value: COUNTS[engine.tier] };
    const belt = engine.program(BELT_VERTEX, POINT_FRAGMENT, 'lapis-belt'),
      axis = engine.dataTexture(axisTable(model), 1024, 1, 1);
    const big = engine.tier === 'high',
      gas = engine.imageTexture('assets/space/families/' + (big ? 'gas-4k' : 'gas') + '.webp', {
        wrap: gl.CLAMP_TO_EDGE,
      }),
      regolith = engine.imageTexture('assets/space/objects/' + (big ? 'regolite-4k' : 'regolite') + '.webp');
    const options = { giant: true, groups: true, axes: false, resonances: true };
    let view = 'belt',
      hero = null,
      moon = null,
      shadow = null;
    const heroOrbit = { a: 2.74, e: 0.08, inc: 0.09, node: 0.6, peri: 1.9, M0: 2.2 };
    const status = text => ui.status?.(text);
    status('Costruzione della superficie dell’asteroide…');
    const level = engine.tier === 'low' ? 6 : 7;
    Promise.all([
      engine.work('smallBody', {
        seed: 31,
        level,
        axes: [1.32, 0.88, 0.76],
        craterCount: engine.tier === 'low' ? 1200 : 3200,
      }),
      engine.work('smallBody', {
        seed: 77,
        level: level - 2,
        axes: [1.05, 0.92, 0.84],
        craterCount: 300,
        rough: 0.04,
        largest: 0.3,
      }),
    ])
      .then(([a, b]) => {
        hero = engine.mesh(a);
        moon = engine.mesh(b);
        shadow = engine.shadowMap(engine.tier === 'low' ? 1024 : 2048);
        status('');
        engine.invalidate();
      })
      .catch(err => status('Superficie non disponibile: ' + err.message));
    for (const r of model.resonances) labels.set('res-' + r.label, r.label, 'resonance');
    labels.set('giant', 'Gigante', 'body');
    labels.set('star', 'Lapis', 'body');
    labels.set('L4', 'Troiani L4', 'group');
    labels.set('L5', 'Troiani L5', 'group');
    labels.set('hero', 'Asteroide osservato', 'body');
    const years = frame => 40 + frame.time * YEARS_PER_SECOND;
    function heroPosition(t) {
      const n = TAU / heroOrbit.a ** 1.5,
        E = O.keplerE((((heroOrbit.M0 + n * t) % TAU) + TAU) % TAU, heroOrbit.e),
        x = heroOrbit.a * (Math.cos(E) - heroOrbit.e),
        y = heroOrbit.a * Math.sqrt(1 - heroOrbit.e ** 2) * Math.sin(E);
      const [cw, sw, cn, sn, ci, si] = [
        heroOrbit.peri,
        heroOrbit.peri,
        heroOrbit.node,
        heroOrbit.node,
        heroOrbit.inc,
        heroOrbit.inc,
      ].map((v, i) => (i % 2 ? Math.sin(v) : Math.cos(v)));
      const X = (cw * cn - sw * sn * ci) * x + (-sw * cn - cw * sn * ci) * y,
        Y = (cw * sn + sw * cn * ci) * x + (-sw * sn + cw * cn * ci) * y,
        Z = sw * si * x + cw * si * y;
      return [X, Z, -Y];
    }
    const giantAt = t => {
      const l = GIANT_PHASE + (TAU * t) / model.giant ** 1.5;
      return [Math.cos(l) * model.giant, 0, -Math.sin(l) * model.giant];
    };
    function drawBelt(frame, origin, sky) {
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE);
      gl.depthMask(false);
      gl.useProgram(belt);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, axis);
      engine.set(belt, 'uAxis', 0, 'int');
      engine.set(belt, 'uVP', frame.camera.vp);
      engine.set(belt, 'uEye', sky ? origin : frame.camera.eye);
      engine.set(belt, 'uOrigin', origin);
      engine.set(belt, 'uTime', years(frame));
      engine.set(belt, 'uGiant', model.giant);
      engine.set(belt, 'uGiantPhase', GIANT_PHASE);
      engine.set(belt, 'uEcc', options.axes ? 0 : 1);
      engine.set(belt, 'uGroups', options.groups ? 1 : 0);
      engine.set(belt, 'uSkyMode', sky ? 1 : 0);
      const size = Math.max(1, SPRITE[engine.tier] * frame.pixelRatio),
        density = (frame.width * frame.height) / 1e6 / Math.max(1, 0.9 * (size / 2) ** 2);
      engine.set(belt, 'uSize', size);
      engine.set(belt, 'uGain', ((sky ? 0.05 : 2.4) * density * 1.6e6) / count.value);
      engine.points(count.value);
      gl.depthMask(true);
      gl.disable(gl.BLEND);
    }
    function drawOverview(frame) {
      engine.sky(frame, 0.3);
      const t = years(frame),
        giant = giantAt(t);
      gl.enable(gl.DEPTH_TEST);
      kit.drawStar(frame, { position: [0, 0, 0], radius: 0.09, color: O.blackbody(5772), intensity: 26, grain: 7 });
      if (options.giant)
        kit.drawPlanet(frame, {
          position: giant,
          radius: 0.17,
          albedo: gas,
          light: [0, 0, 0],
          power: 1.4,
          spin: frame.time * 0.02,
          rim: [0.5, 0.6, 0.8],
        });
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
      gl.depthMask(false);
      if (options.giant) kit.drawLine(frame, 'giant-orbit', K.circle(model.giant, 720), [0.75, 0.62, 0.4, 0.35]);
      if (options.resonances)
        for (const r of model.resonances.slice(1, 5))
          kit.drawLine(frame, 'res-' + r.label, K.circle(r.a, 720), [0.95, 0.78, 0.5, 0.16]);
      kit.drawLine(frame, 'hero-orbit', heroOrbitPoints(), [0.55, 0.85, 1, 0.3]);
      gl.depthMask(true);
      gl.disable(gl.BLEND);
      drawBelt(frame, [0, 0, 0], false);
      kit.drawGlow(frame, { position: [0, 0, 0], size: 1.6, color: [2.2, 1.9, 1.5], falloff: 9 });
      placeOverviewLabels(giant, t);
    }
    function heroOrbitPoints() {
      const pts = new Float32Array(721 * 3),
        P = heroOrbit.a ** 1.5;
      for (let i = 0; i <= 720; i++) pts.set(heroPosition((i / 720) * P), i * 3);
      return pts;
    }
    function placeOverviewLabels(giant, t) {
      labels.hideAll();
      const show = (key, p, on = true) => labels.place(key, engine.project(p), on);
      show('star', [0, 0.12, 0]);
      show('giant', [giant[0], 0.2, giant[2]], options.giant);
      if (options.groups) {
        const l = Math.atan2(-giant[2], giant[0]);
        show('L4', [Math.cos(l + Math.PI / 3) * model.giant, 0.3, -Math.sin(l + Math.PI / 3) * model.giant]);
        show('L5', [Math.cos(l - Math.PI / 3) * model.giant, 0.3, -Math.sin(l - Math.PI / 3) * model.giant]);
      }
      if (options.resonances)
        model.resonances.slice(1, 5).forEach((r, i) => {
          const a = -0.35 - i * 0.3;
          show('res-' + r.label, [Math.cos(a) * r.a, 0.02, -Math.sin(a) * r.a]);
        });
      const h = heroPosition(t);
      show('hero', [h[0], h[1] + 0.08, h[2]]);
    }
    // Close view: the asteroid in kilometres; the belt, the star and the giant are drawn as the sky seen from it.
    function drawClose(frame) {
      const t = years(frame),
        where = heroPosition(t),
        r = Math.hypot(...where),
        sun = where.map(v => -v / r),
        spin = frame.time * 0.16;
      engine.sky(frame, 0.45);
      const skyCamera = { ...frame.camera, vp: engine.multiply(frame.camera.proj, viewRotation(frame.camera.view)) };
      drawBelt({ ...frame, camera: skyCamera }, where, true);
      gl.enable(gl.DEPTH_TEST);
      kit.drawGlow(
        { ...frame, camera: skyCamera },
        { position: sun.map(v => v * 50), size: 0.55, color: [9, 8.2, 7], falloff: 22 },
      );
      if (!hero) return;
      const scale = 24,
        matrix = engine.model(
          [0, 0, 0],
          scale,
          [0.2, 1, 0.1].map(v => v / Math.hypot(0.2, 1, 0.1)),
          spin,
        );
      const moonAngle = frame.time * 0.05,
        moonPos = [Math.cos(moonAngle) * 78, Math.sin(moonAngle) * 9, -Math.sin(moonAngle) * 78],
        moonMatrix = engine.model(moonPos, 3.4, [0, 1, 0], frame.time * 0.3);
      const lightVP = kit.renderShadow(shadow, frame, sun, [0, 0, 0], 90, [
        [hero, matrix],
        [moon, moonMatrix],
      ]);
      const power = 3.2 / (r * r);
      for (const [mesh, m] of [
        [hero, matrix],
        [moon, moonMatrix],
      ])
        kit.drawRock(frame, mesh, {
          matrix: m,
          albedo: regolith,
          lightDir: sun,
          power: power * 2.4,
          scale: 2.5,
          bump: 0.03,
          tint: [1, 0.97, 0.93],
          shadow,
          lightVP,
          ambient: 0.006,
        });
      labels.hideAll();
    }
    function viewRotation(m) {
      const r = new Float32Array(m);
      r[12] = r[13] = r[14] = 0;
      return r;
    }
    function draw(frame) {
      if (view === 'belt') drawOverview(frame);
      else drawClose(frame);
    }
    function setView(next) {
      view = next;
      if (next === 'asteroid') {
        // Camera on the day side, about 45 degrees from the direction of the star.
        const where = heroPosition(40 + engine.time() * YEARS_PER_SECOND),
          sun = where.map(v => -v / Math.hypot(...where));
        Object.assign(engine.camera, { minDistance: 45, maxDistance: 600 });
        engine.moveTo(
          { azimuth: Math.atan2(sun[0], sun[2]) + 0.8, elevation: 0.32, distance: 130, target: [0, 0, 0] },
          0,
        );
      } else {
        Object.assign(engine.camera, { minDistance: 1.5, maxDistance: 34 });
        engine.moveTo({ azimuth: 0.5, elevation: 0.62, distance: 13, target: [0, 0, 0] }, 0);
      }
      ui.status?.('');
      engine.invalidate();
    }
    return {
      draw,
      view: setView,
      near: d => (view === 'belt' ? d * 0.005 : d * 0.02),
      far: d => (view === 'belt' ? d * 30 : d * 40),
      options,
      setOption(key, value) {
        options[key] = value;
        engine.invalidate();
      },
      reduce() {
        if (count.value < 200000) return engine.reduceResolution();
        count.value = Math.round(count.value * 0.7);
        return true;
      },
      debug: () => ({
        object: 'asteroidi',
        view,
        particles: count.value,
        mesh: hero ? hero.count / 3 : 0,
        options: { ...options },
      }),
      dispose() {
        kit.dispose();
        labels.dispose();
      },
    };
  }
  root.GeoObjectScenes = root.GeoObjectScenes || {};
  root.GeoObjectScenes.asteroidi = {
    create,
    exposure: 1,
    camera: {
      azimuth: 0.5,
      elevation: 0.62,
      distance: 13,
      minDistance: 1.5,
      maxDistance: 34,
      minElevation: -1.4,
      maxElevation: 1.45,
      fov: (40 * Math.PI) / 180,
    },
  };
})(globalThis);
