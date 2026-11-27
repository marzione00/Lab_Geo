/* Shared pieces of the object scenes: GLSL noise, emissive stars, lit planets, orbit lines, rocky bodies with
   shadows and the labels placed over the canvas. */
(function (root) {
  'use strict';
  const TAU = Math.PI * 2;
  // Integer hash and 3D gradient-free value noise with quintic interpolation.
  const NOISE = `
    uint hash(uint x){x^=x>>16;x*=0x7feb352dU;x^=x>>15;x*=0x846ca68bU;x^=x>>16;return x;}
    float rnd(uint id,uint k){return float(hash(id*0x9E3779B9U+k*0x85EBCA6BU+0x632BE5ABU))*2.3283064e-10;}
    float gauss(uint id,uint k){return sqrt(-2.*log(max(1e-7,rnd(id,k))))*cos(6.2831853*rnd(id,k+101u));}
    float h3(vec3 p){p=fract(p*.1031);p+=dot(p,p.zyx+31.32);return fract((p.x+p.y)*p.z);}
    float noise(vec3 p){vec3 i=floor(p),f=fract(p);vec3 u=f*f*f*(f*(f*6.-15.)+10.);
      return mix(mix(mix(h3(i),h3(i+vec3(1,0,0)),u.x),mix(h3(i+vec3(0,1,0)),h3(i+vec3(1,1,0)),u.x),u.y),
        mix(mix(h3(i+vec3(0,0,1)),h3(i+vec3(1,0,1)),u.x),mix(h3(i+vec3(0,1,1)),h3(i+vec3(1,1,1)),u.x),u.y),u.z)*2.-1.;}
    float fbm(vec3 p){float s=0.,a=.5;for(int i=0;i<6;i++){s+=a*noise(p);p=p*2.03+17.1;a*=.5;}return s;}`;
  const MESH_VERTEX = `#version 300 es
    precision highp float;
    layout(location=0) in vec3 aPosition;layout(location=1) in vec3 aNormal;layout(location=2) in vec2 aUV;
    uniform mat4 uVP,uModel;out vec3 vWorld,vNormal,vLocal;out vec2 vUV;
    void main(){vec4 w=uModel*vec4(aPosition,1.);vWorld=w.xyz;vLocal=aPosition;
      vNormal=normalize(mat3(uModel)*aNormal);vUV=aUV;gl_Position=uVP*w;}`;
  // Emissive photosphere: granulation, limb darkening and colour of the effective temperature.
  const STAR_FRAGMENT = `#version 300 es
    precision highp float;in vec3 vWorld,vNormal,vLocal;in vec2 vUV;out vec4 o;
    uniform vec3 uEye,uColor;uniform float uTime,uIntensity,uGrain;
    ${NOISE}
    void main(){vec3 n=normalize(vNormal),v=normalize(uEye-vWorld);float mu=max(0.,dot(n,v));
      vec3 p=normalize(vLocal)*uGrain;
      float cells=fbm(p+vec3(0,uTime*.03,0))*.5+noise(p*4.+uTime*.05)*.35;
      float spots=smoothstep(.55,.75,fbm(p*.35+11.));
      float limb=1.-.6*(1.-mu)-.25*(1.-mu)*(1.-mu);
      o=vec4(uColor*uIntensity*limb*(1.+.22*cells)*(1.-.55*spots),1.);}`;
  // Planet with an equirectangular albedo, lit by a point source, with a thin scattering rim.
  const PLANET_FRAGMENT = `#version 300 es
    precision highp float;in vec3 vWorld,vNormal,vLocal;in vec2 vUV;out vec4 o;
    uniform sampler2D uAlbedo;uniform vec3 uEye,uLight,uRim;uniform float uLightPower,uSpin;
    void main(){vec3 n=normalize(vNormal),v=normalize(uEye-vWorld),l=normalize(uLight-vWorld);
      vec3 a=texture(uAlbedo,vec2(fract(vUV.x+uSpin),vUV.y)).rgb;
      float d=max(0.,dot(n,l));float rim=pow(1.-max(0.,dot(n,v)),4.)*smoothstep(-.2,.4,dot(n,l));
      o=vec4(a*d*uLightPower+uRim*rim*uLightPower*.5+a*.004,1.);}`;
  const LINE_VERTEX = `#version 300 es
    precision highp float;layout(location=0) in vec3 aPosition;uniform mat4 uVP,uModel;
    void main(){gl_Position=uVP*uModel*vec4(aPosition,1.);}`;
  const LINE_FRAGMENT = `#version 300 es
    precision highp float;uniform vec4 uColor;out vec4 o;void main(){o=uColor;}`;
  // Rocky body: triplanar regolith texture with relief from its height channel, Lommel-Seeliger and Lambert
  // reflectance, percentage-closer shadows from the star.
  const ROCK_FRAGMENT = `#version 300 es
    precision highp float;precision highp sampler2DShadow;
    in vec3 vWorld,vNormal,vLocal;in vec2 vUV;out vec4 o;
    uniform sampler2D uAlbedo;uniform sampler2DShadow uShadow;uniform mat4 uLightVP;
    uniform vec3 uEye,uLightDir,uTint;uniform float uLightPower,uScale,uBump,uAlbedoScale,uShadowOn,uAmbient;
    vec4 tri(vec3 p,vec3 w){return texture(uAlbedo,p.yz)*w.x+texture(uAlbedo,p.zx)*w.y+texture(uAlbedo,p.xy)*w.z;}
    float height(vec3 p,vec3 w){return tri(p,w).a;}
    void main(){vec3 n=normalize(vNormal);vec3 w=pow(abs(n),vec3(4.));w/=dot(w,vec3(1));
      vec3 p=vLocal*uScale;vec4 t=tri(p,w);
      // Relief: gradient of the height channel in the three projection planes.
      float e=.0025;float h0=t.a;
      vec3 g=vec3(height(p+vec3(e,0,0),w)-h0,height(p+vec3(0,e,0),w)-h0,height(p+vec3(0,0,e),w)-h0)/e;
      n=normalize(n-uBump*(g-dot(g,n)*n));
      vec3 l=uLightDir,v=normalize(uEye-vWorld);
      float mu0=max(0.,dot(n,l)),mu=max(.05,dot(n,v));
      float ls=mu0/(mu0+mu),lam=mu0;float phase=dot(l,v);
      float shade=mix(ls*2.,lam,.35)*(1.+.25*pow(max(0.,phase),20.));
      float lit=1.;
      if(uShadowOn>.5){vec4 s=uLightVP*vec4(vWorld,1.);s.xyz=s.xyz/s.w*.5+.5;
        float bias=.0015+.007*(1.-max(0.,dot(normalize(vNormal),l)));lit=0.;
        vec2 texel=vec2(1./2048.);
        for(int i=-2;i<=2;i++)for(int j=-2;j<=2;j++)lit+=texture(uShadow,vec3(s.xy+vec2(i,j)*texel,s.z-bias));
        lit/=25.;}
      vec3 albedo=t.rgb*uTint*uAlbedoScale;
      o=vec4(albedo*(shade*lit*uLightPower+uAmbient),1.);}`;
  const DEPTH_VERTEX = `#version 300 es
    precision highp float;layout(location=0) in vec3 aPosition;uniform mat4 uVP,uModel;
    void main(){gl_Position=uVP*uModel*vec4(aPosition,1.);}`;
  const DEPTH_FRAGMENT = `#version 300 es
    precision highp float;void main(){}`;
  // Soft glow around a bright source, drawn as a screen-facing quad.
  const GLOW_VERTEX = `#version 300 es
    precision highp float;uniform mat4 uVP;uniform vec3 uCenter,uRight,uUp;uniform float uSize;out vec2 vQ;
    void main(){vec2 q=vec2(float(gl_VertexID&1),float((gl_VertexID>>1)&1))*2.-1.;vQ=q;
      gl_Position=uVP*vec4(uCenter+(uRight*q.x+uUp*q.y)*uSize,1.);}`;
  const GLOW_FRAGMENT = `#version 300 es
    precision highp float;in vec2 vQ;uniform vec3 uColor;uniform float uFalloff;out vec4 o;
    void main(){float r=length(vQ);if(r>1.)discard;o=vec4(uColor*(exp(-r*uFalloff)-exp(-uFalloff))/(1.-exp(-uFalloff)),1.);}`;

  // UV sphere with a duplicated seam column, so that the equirectangular texture has no seam.
  function uvSphere(lat = 128, lon = 256) {
    const positions = [],
      uvs = [],
      indices = [];
    for (let j = 0; j <= lat; j++)
      for (let i = 0; i <= lon; i++) {
        const t = (j / lat) * Math.PI,
          p = (i / lon) * TAU;
        positions.push(Math.sin(t) * Math.cos(p), Math.cos(t), -Math.sin(t) * Math.sin(p));
        uvs.push(i / lon, j / lat);
      }
    for (let j = 0; j < lat; j++)
      for (let i = 0; i < lon; i++) {
        const a = j * (lon + 1) + i,
          b = a + lon + 1;
        indices.push(a, b, a + 1, b, b + 1, a + 1);
      }
    const pos = new Float32Array(positions);
    return {
      positions: pos,
      normals: pos.slice(),
      indices: new Uint32Array(indices),
      extra: new Float32Array(uvs),
      extraSize: 2,
    };
  }
  function circle(radius, segments = 512, y = 0) {
    const out = new Float32Array((segments + 1) * 3);
    for (let i = 0; i <= segments; i++) {
      const a = (i / segments) * TAU;
      out.set([Math.cos(a) * radius, y, Math.sin(a) * radius], i * 3);
    }
    return out;
  }
  function kit(engine) {
    const gl = engine.gl;
    let star, planet, line, rock, depth, glow, sphere;
    const lineBuffers = new Map();
    function sphereMesh() {
      sphere ||= engine.mesh(uvSphere());
      return sphere;
    }
    function drawStar(
      frame,
      { position, radius, color, intensity = 20, grain = 9, time = frame.time, mesh = null, matrix = null },
    ) {
      star ||= engine.program(MESH_VERTEX, STAR_FRAGMENT, 'star');
      gl.useProgram(star);
      engine.set(star, 'uVP', frame.camera.vp);
      engine.set(star, 'uModel', matrix || engine.model(position, radius));
      engine.set(star, 'uEye', frame.camera.eye);
      engine.set(star, 'uColor', color);
      engine.set(star, 'uTime', time);
      engine.set(star, 'uIntensity', intensity);
      engine.set(star, 'uGrain', grain);
      (mesh || sphereMesh()).draw();
    }
    function drawPlanet(
      frame,
      { position, radius, albedo, light = [0, 0, 0], power = 1, spin = 0, rim = [0.4, 0.55, 0.8], tilt = 0.05 },
    ) {
      planet ||= engine.program(MESH_VERTEX, PLANET_FRAGMENT, 'planet');
      gl.useProgram(planet);
      engine.set(planet, 'uVP', frame.camera.vp);
      engine.set(planet, 'uModel', engine.model(position, radius, [0, 0, 1], tilt));
      engine.set(planet, 'uEye', frame.camera.eye);
      engine.set(planet, 'uLight', light);
      engine.set(planet, 'uLightPower', power);
      engine.set(planet, 'uSpin', spin);
      engine.set(planet, 'uRim', rim);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, albedo.texture);
      engine.set(planet, 'uAlbedo', 0, 'int');
      sphereMesh().draw();
    }
    function drawLine(frame, key, points, color, matrix = engine.model(), mode = gl.LINE_STRIP) {
      line ||= engine.program(LINE_VERTEX, LINE_FRAGMENT, 'line');
      let entry = lineBuffers.get(key);
      if (!entry) {
        const vao = gl.createVertexArray(),
          buffer = gl.createBuffer();
        gl.bindVertexArray(vao);
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, points, gl.DYNAMIC_DRAW);
        gl.enableVertexAttribArray(0);
        gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
        gl.bindVertexArray(null);
        entry = { vao, buffer, count: points.length / 3 };
        lineBuffers.set(key, entry);
      }
      gl.useProgram(line);
      engine.set(line, 'uVP', frame.camera.vp);
      engine.set(line, 'uModel', matrix);
      engine.set(line, 'uColor', color);
      gl.bindVertexArray(entry.vao);
      gl.drawArrays(mode, 0, entry.count);
      gl.bindVertexArray(null);
    }
    function updateLine(key, points) {
      const entry = lineBuffers.get(key);
      if (!entry) return;
      gl.bindBuffer(gl.ARRAY_BUFFER, entry.buffer);
      gl.bufferData(gl.ARRAY_BUFFER, points, gl.DYNAMIC_DRAW);
      entry.count = points.length / 3;
    }
    function drawGlow(frame, { position, size, color, falloff = 6 }) {
      glow ||= engine.program(GLOW_VERTEX, GLOW_FRAGMENT, 'glow');
      gl.useProgram(glow);
      engine.set(glow, 'uVP', frame.camera.vp);
      engine.set(glow, 'uCenter', position);
      engine.set(glow, 'uRight', frame.camera.right);
      engine.set(glow, 'uUp', frame.camera.up);
      engine.set(glow, 'uSize', size);
      engine.set(glow, 'uColor', color);
      engine.set(glow, 'uFalloff', falloff);
      // The glow is light scattered around a bright source: it is added over the bodies in front of it.
      const depth = gl.isEnabled(gl.DEPTH_TEST);
      gl.disable(gl.DEPTH_TEST);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE);
      gl.depthMask(false);
      engine.fullscreenQuad();
      gl.depthMask(true);
      gl.disable(gl.BLEND);
      if (depth) gl.enable(gl.DEPTH_TEST);
    }
    // Rocky body with optional shadow map: light is a direction (star far away compared with the body).
    function drawRock(
      frame,
      mesh,
      {
        matrix,
        albedo,
        lightDir,
        power = 1,
        scale = 0.06,
        bump = 0.6,
        tint = [1, 1, 1],
        albedoScale = 1,
        shadow = null,
        lightVP = null,
        ambient = 0.004,
      },
    ) {
      rock ||= engine.program(MESH_VERTEX, ROCK_FRAGMENT, 'rock');
      gl.useProgram(rock);
      engine.set(rock, 'uVP', frame.camera.vp);
      engine.set(rock, 'uModel', matrix);
      engine.set(rock, 'uEye', frame.camera.eye);
      engine.set(rock, 'uLightDir', lightDir);
      engine.set(rock, 'uLightPower', power);
      engine.set(rock, 'uScale', scale);
      engine.set(rock, 'uBump', bump);
      engine.set(rock, 'uTint', tint);
      engine.set(rock, 'uAlbedoScale', albedoScale);
      engine.set(rock, 'uAmbient', ambient);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, albedo.texture);
      engine.set(rock, 'uAlbedo', 0, 'int');
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, shadow?.depth || null);
      engine.set(rock, 'uShadow', 1, 'int');
      engine.set(rock, 'uShadowOn', shadow ? 1 : 0);
      if (lightVP) engine.set(rock, 'uLightVP', lightVP);
      mesh.draw();
    }
    // Depth from the light for a set of meshes; returns the light view-projection matrix.
    function renderShadow(shadow, frame, lightDir, center, radius, items) {
      depth ||= engine.program(DEPTH_VERTEX, DEPTH_FRAGMENT, 'depth');
      const eye = center.map((c, i) => c + lightDir[i] * radius * 3),
        up = Math.abs(lightDir[1]) > 0.9 ? [1, 0, 0] : [0, 1, 0];
      const view = engine.cameraMatrices(eye, center, up, 1, 0.5, 0.1, 10).view;
      const r = radius * 1.05,
        n = radius * 1.5,
        f = radius * 4.6;
      const ortho = new Float32Array([
        1 / r,
        0,
        0,
        0,
        0,
        1 / r,
        0,
        0,
        0,
        0,
        -2 / (f - n),
        0,
        0,
        0,
        -(f + n) / (f - n),
        1,
      ]);
      const vp = engine.multiply(ortho, view);
      gl.bindFramebuffer(gl.FRAMEBUFFER, shadow.fb);
      gl.viewport(0, 0, shadow.size, shadow.size);
      gl.clearDepth(1);
      gl.clear(gl.DEPTH_BUFFER_BIT);
      gl.enable(gl.DEPTH_TEST);
      gl.depthMask(true);
      gl.enable(gl.POLYGON_OFFSET_FILL);
      gl.polygonOffset(1.5, 3);
      gl.useProgram(depth);
      engine.set(depth, 'uVP', vp);
      for (const [mesh, matrix] of items) {
        engine.set(depth, 'uModel', matrix);
        mesh.draw();
      }
      gl.disable(gl.POLYGON_OFFSET_FILL);
      gl.bindFramebuffer(gl.FRAMEBUFFER, frame.output);
      gl.viewport(0, 0, frame.width, frame.height);
      return vp;
    }
    function dispose() {
      for (const e of lineBuffers.values()) {
        gl.deleteBuffer(e.buffer);
        gl.deleteVertexArray(e.vao);
      }
      lineBuffers.clear();
    }
    return { drawStar, drawPlanet, drawLine, updateLine, drawGlow, drawRock, renderShadow, sphereMesh, dispose };
  }
  // Text labels over the canvas, kept on the projected position of a 3D point.
  function labels(chart) {
    const layer = document.createElement('div');
    layer.className = 'object-labels';
    layer.setAttribute('aria-hidden', 'true');
    chart.append(layer);
    const items = new Map();
    return {
      set(key, text, kind = '') {
        if (items.has(key)) return items.get(key);
        const el = document.createElement('span');
        el.className = 'object-label ' + kind;
        el.textContent = text;
        layer.append(el);
        items.set(key, el);
        return el;
      },
      place(key, q, visible = true) {
        const el = items.get(key);
        if (!el) return;
        const show =
          visible &&
          q &&
          q.visible &&
          q.x > 8 &&
          q.y > 8 &&
          q.x < chart.clientWidth - 8 &&
          q.y < chart.clientHeight - 8;
        el.hidden = !show;
        if (show) el.style.transform = `translate(${q.x.toFixed(1)}px, ${q.y.toFixed(1)}px)`;
      },
      hideAll() {
        for (const el of items.values()) el.hidden = true;
      },
      dispose() {
        layer.remove();
        items.clear();
      },
    };
  }
  root.GeoObjectKit = Object.freeze({ NOISE, MESH_VERTEX, uvSphere, circle, kit, labels });
})(globalThis);
