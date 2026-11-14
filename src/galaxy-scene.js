/* The home is one perspective scene: volumetric particles, triangle-mesh
   spheres and annular meshes. No background image or external runtime. */
(function (root) {
  'use strict';
  const M = root.GeoGalaxyModel,
    TAU = Math.PI * 2;
  const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255);
  const pointVertex = `attribute vec3 aPosition;attribute vec4 aColor;attribute float aSize;
    uniform mat4 uVP,uModel;uniform float uScale;varying vec4 vColor;
    void main(){vec4 p=uVP*uModel*vec4(aPosition,1.);gl_Position=p;
    gl_PointSize=clamp(aSize*uScale/max(.1,p.w),1.,100.);vColor=aColor;}`;
  const pointFragment = `precision mediump float;varying vec4 vColor;
    void main(){float d=length(gl_PointCoord*2.-1.);if(d>1.)discard;
    gl_FragColor=vec4(vColor.rgb,vColor.a*exp(-d*d*5.5)*(1.-smoothstep(.7,1.,d)));}`;
  const meshVertex = `attribute vec3 aPosition;attribute vec2 aUV;uniform mat4 uVP,uModel;
    varying vec3 vPosition,vNormal;varying vec2 vUV;
    void main(){vec4 w=uModel*vec4(aPosition,1.);vPosition=w.xyz;
    vNormal=normalize(mat3(uModel)*aPosition);vUV=aUV;gl_Position=uVP*w;}`;
  const meshFragment = `precision mediump float;varying vec3 vPosition,vNormal;varying vec2 vUV;
    uniform sampler2D uTexture;uniform vec3 uEye,uColor,uAtmosphere,uLight;
    uniform float uSpin,uMode,uVolcanic,uTextured;
    void main(){vec3 n=normalize(vNormal),v=normalize(uEye-vPosition);
      if(uMode>2.5){float grain=sin(vUV.x*560.+uSpin*8.)*sin(vUV.y*410.+sin(vUV.x*75.)*3.);
        float limb=.48+.52*sqrt(max(0.,dot(n,v)));gl_FragColor=vec4(uColor*(.86+.14*grain)*limb,1.);return;}
      if(uMode>1.5){float rim=pow(1.-abs(dot(n,v)),3.5);
        gl_FragColor=vec4(uAtmosphere,rim*.37);return;}
      if(uMode>.5){float r=vUV.y;float band=.55+.25*sin(r*140.)+.17*sin(r*310.);
        float gap=smoothstep(.57,.61,r)*(1.-smoothstep(.66,.70,r));
        gl_FragColor=vec4(uColor*(.68+.32*band),(.48+.36*band)*(1.-gap*.95));return;}
      vec3 tex=mix(uColor,texture2D(uTexture,vec2(fract(vUV.x+uSpin),vUV.y)).rgb,uTextured);
      vec3 light=normalize(uLight-vPosition);float diffuse=max(0.,dot(n,light));
      vec3 c=tex*(.12+diffuse*1.1);
      if(uVolcanic>.5)c+=tex*max(0.,tex.r-tex.g*1.5)*1.8;
      float rim=pow(1.-max(0.,dot(n,v)),4.);
      c+=uAtmosphere*rim*(.06+diffuse*.38);gl_FragColor=vec4(c,1.);}`;
  const lineVertex = `attribute vec3 aPosition;uniform mat4 uVP,uModel;
    void main(){gl_Position=uVP*uModel*vec4(aPosition,1.);}`;
  const lineFragment = `precision mediump float;uniform vec4 uColor;void main(){gl_FragColor=uColor;}`;

  function sphere() {
    const v = [],
      ix = [],
      u = 96,
      t = 64;
    for (let j = 0; j <= t; j++)
      for (let i = 0; i <= u; i++) {
        const p = (j / t) * Math.PI,
          a = (i / u) * TAU;
        v.push(Math.sin(p) * Math.cos(a), Math.cos(p), Math.sin(p) * Math.sin(a), i / u, j / t);
      }
    for (let j = 0; j < t; j++)
      for (let i = 0; i < u; i++) {
        const a = j * (u + 1) + i,
          b = a + u + 1;
        ix.push(a, b, a + 1, b, b + 1, a + 1);
      }
    return { v, ix };
  }
  function annulus() {
    const v = [],
      ix = [];
    for (let i = 0; i <= 128; i++)
      for (let k = 0; k < 2; k++) {
        const a = (i / 128) * TAU,
          r = k ? 1.94 : 1.22;
        v.push(r * Math.cos(a), 0, r * Math.sin(a), i / 128, k);
        if (i < 128 && k === 0) {
          const n = i * 2;
          ix.push(n, n + 1, n + 2, n + 1, n + 3, n + 2);
        }
      }
    return { v, ix };
  }

  function webgl(canvas, data, worlds, invalidate) {
    if (root.GeoCore?.softwareRendering?.()) throw Error('WebGL software');
    const gl = canvas.getContext('webgl', {
      alpha: true,
      antialias: true,
      depth: true,
      premultipliedAlpha: false,
      powerPreference: 'low-power',
    });
    if (!gl || typeof gl.getParameter(gl.MAX_TEXTURE_SIZE) !== 'number') throw Error('WebGL unavailable');
    const resources = [],
      textures = new Map(),
      images = [];
    const blank = gl.createTexture();
    resources.push(['deleteTexture', blank]);
    gl.bindTexture(gl.TEXTURE_2D, blank);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([255, 255, 255, 255]));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    function program(v, f) {
      const p = gl.createProgram();
      for (const [type, text] of [
        [gl.VERTEX_SHADER, v],
        [gl.FRAGMENT_SHADER, f],
      ]) {
        const s = gl.createShader(type);
        gl.shaderSource(s, text);
        gl.compileShader(s);
        if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
          const reason = gl.getShaderInfoLog(s);
          gl.deleteShader(s);
          throw Error(reason);
        }
        gl.attachShader(p, s);
        gl.deleteShader(s);
      }
      gl.linkProgram(p);
      if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw Error(gl.getProgramInfoLog(p));
      resources.push(['deleteProgram', p]);
      return p;
    }
    function buffer(arr, element = false) {
      const b = gl.createBuffer();
      gl.bindBuffer(element ? gl.ELEMENT_ARRAY_BUFFER : gl.ARRAY_BUFFER, b);
      gl.bufferData(
        element ? gl.ELEMENT_ARRAY_BUFFER : gl.ARRAY_BUFFER,
        element ? new Uint16Array(arr) : new Float32Array(arr),
        gl.STATIC_DRAW,
      );
      resources.push(['deleteBuffer', b]);
      return b;
    }
    function matrix(p, key, val) {
      gl.uniformMatrix4fv(gl.getUniformLocation(p, key), false, val);
    }
    function one(p, key, v) {
      gl.uniform1f(gl.getUniformLocation(p, key), v);
    }
    function three(p, key, v) {
      gl.uniform3fv(gl.getUniformLocation(p, key), v);
    }
    function attribute(p, name, n, stride, offset) {
      const l = gl.getAttribLocation(p, name);
      if (l < 0) return;
      gl.enableVertexAttribArray(l);
      gl.vertexAttribPointer(l, n, gl.FLOAT, false, stride, offset);
    }
    const points = program(pointVertex, pointFragment),
      mesh = program(meshVertex, meshFragment),
      lines = program(lineVertex, lineFragment);
    const flatten = rows => rows.flatMap(p => [...p.p, ...p.c, p.a, p.size]);
    const starBuffer = buffer(flatten(data.stars)),
      dustBuffer = buffer(flatten(data.dust));
    const ball = sphere(),
      ring = annulus(),
      ballBuffer = buffer(ball.v),
      ballIndex = buffer(ball.ix, true),
      ringBuffer = buffer(ring.v),
      ringIndex = buffer(ring.ix, true);
    const orbit = [];
    for (let i = 0; i <= 120; i++) orbit.push(Math.cos((i / 120) * TAU) * 1.45, 0, Math.sin((i / 120) * TAU) * 1.45);
    const orbitBuffer = buffer(orbit);
    let disposed = false;
    for (const p of worlds) {
      if (p.marker || p.emissive) continue;
      const t = gl.createTexture();
      resources.push(['deleteTexture', t]);
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(
        gl.TEXTURE_2D,
        0,
        gl.RGBA,
        1,
        1,
        0,
        gl.RGBA,
        gl.UNSIGNED_BYTE,
        new Uint8Array([...rgb(p.land).map(v => v * 255), 255]),
      );
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      const entry = { t, ready: false };
      textures.set(p.id, entry);
      const im = new Image();
      images.push(im);
      im.onload = () => {
        if (disposed) return;
        gl.bindTexture(gl.TEXTURE_2D, t);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
        if ((im.width & (im.width - 1)) === 0 && (im.height & (im.height - 1)) === 0) {
          gl.generateMipmap(gl.TEXTURE_2D);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
        }
        entry.ready = true;
        invalidate();
      };
      im.onerror = () => invalidate();
      im.src = root.GeoFamilies
        ? root.GeoFamilies.texture(p)
        : 'assets/space/' + ((p.textureId || p.id) === 'M01' ? 'day' : 'p-' + (p.textureId || p.id)) + '.webp';
    }
    const canDetail = gl.getParameter(gl.MAX_TEXTURE_SIZE) >= 4096;
    function detailTexture(p, state) {
      const entry = textures.get(p.id);
      if (
        !canDetail ||
        state.width < 760 ||
        p.screen?.radius < 90 ||
        !p.familyId ||
        !entry?.ready ||
        entry.detailRequested
      )
        return;
      entry.detailRequested = true;
      const im = new Image();
      images.push(im);
      im.onload = () => {
        if (disposed) return;
        gl.bindTexture(gl.TEXTURE_2D, entry.t);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
        gl.generateMipmap(gl.TEXTURE_2D);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
        invalidate();
      };
      im.onerror = () => {};
      im.src = root.GeoFamilies.texture(p, true);
    }
    function pointPass(buffer, count, state) {
      gl.useProgram(points);
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      attribute(points, 'aPosition', 3, 32, 0);
      attribute(points, 'aColor', 4, 32, 12);
      attribute(points, 'aSize', 1, 32, 28);
      matrix(points, 'uVP', state.camera.vp);
      matrix(points, 'uModel', M.rotation(state.angle));
      one(points, 'uScale', canvas.height * state.camera.f);
      gl.drawArrays(gl.POINTS, 0, count);
    }
    function linePass(b, count, model, color, state, mode = gl.LINE_STRIP) {
      gl.useProgram(lines);
      gl.bindBuffer(gl.ARRAY_BUFFER, b);
      attribute(lines, 'aPosition', 3, 12, 0);
      matrix(lines, 'uVP', state.camera.vp);
      matrix(lines, 'uModel', model);
      gl.uniform4fv(gl.getUniformLocation(lines, 'uColor'), color);
      gl.drawArrays(mode, 0, count);
    }
    function planetPass(p, state, mode = 0) {
      gl.useProgram(mesh);
      gl.bindBuffer(gl.ARRAY_BUFFER, mode === 1 ? ringBuffer : ballBuffer);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, mode === 1 ? ringIndex : ballIndex);
      attribute(mesh, 'aPosition', 3, 20, 0);
      attribute(mesh, 'aUV', 2, 20, 12);
      matrix(mesh, 'uVP', state.camera.vp);
      matrix(mesh, 'uModel', M.model(p.position, p.radius * (mode === 2 ? 1.09 : 1), p.tilt));
      three(mesh, 'uLight', state.light || [-30, 50, 40]);
      three(mesh, 'uEye', state.camera.eye);
      three(mesh, 'uColor', rgb(mode === 1 ? p.high : p.land));
      three(mesh, 'uAtmosphere', rgb(p.atmosphere));
      one(mesh, 'uMode', p.emissive ? 3 : mode);
      one(mesh, 'uVolcanic', p.kind === 14 ? 1 : 0);
      one(mesh, 'uSpin', p.phase / TAU - (state.time * p.speed) / TAU);
      one(mesh, 'uTextured', textures.get(p.id)?.ready ? 1 : 0);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, textures.get(p.id)?.t || blank);
      gl.uniform1i(gl.getUniformLocation(mesh, 'uTexture'), 0);
      gl.drawElements(gl.TRIANGLES, mode === 1 ? ring.ix.length : ball.ix.length, gl.UNSIGNED_SHORT, 0);
    }
    return {
      kind: 'webgl',
      draw(state) {
        gl.viewport(0, 0, canvas.width, canvas.height);
        gl.clearColor(0, 0, 0, 0);
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        gl.enable(gl.DEPTH_TEST);
        gl.depthMask(true);
        gl.disable(gl.BLEND);
        for (const p of state.worlds)
          if (!p.marker) {
            if (p.id === state.selected) detailTexture(p, state);
            planetPass(p, state);
          }
        gl.depthMask(false);
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        for (const p of state.worlds) if (p.rings && !p.marker) planetPass(p, state, 1);
        const p = state.worlds.find(x => x.id === state.selected);
        if (p && !p.marker && !p.emissive && !state.light)
          linePass(orbitBuffer, 121, M.model(p.position, p.radius * 1.3), [0.93, 0.7, 0.37, 0.65], state);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
        pointPass(dustBuffer, data.dust.length, state);
        pointPass(starBuffer, data.stars.length, state);
        for (const p of state.worlds) if (!p.marker && !p.emissive) planetPass(p, state, 2);
        gl.depthMask(true);
      },
      dispose() {
        disposed = true;
        for (const im of images) {
          im.onload = null;
          im.onerror = null;
        }
        for (const [method, value] of resources) gl[method](value);
      },
      textureCount: () => [...textures.values()].filter(t => t.ready).length,
    };
  }

  function software(canvas, data, invalidate) {
    const ctx = canvas.getContext('2d');
    if (!ctx) throw Error('Canvas unavailable');
    const sprites = new Map();
    function sprite(color) {
      const key = color.map(v => Math.round(v * 8)).join('-');
      if (sprites.has(key)) return sprites.get(key);
      const c = document.createElement('canvas');
      c.width = c.height = 32;
      const x = c.getContext('2d'),
        g = x.createRadialGradient(16, 16, 0, 16, 16, 16);
      const col = color.map(v => Math.round(v * 255));
      g.addColorStop(0, 'rgba(' + col + ',1)');
      g.addColorStop(0.25, 'rgba(' + col + ',.45)');
      g.addColorStop(1, 'rgba(' + col + ',0)');
      x.fillStyle = g;
      x.fillRect(0, 0, 32, 32);
      sprites.set(key, c);
      return c;
    }
    const rows = M.softwareParticles(data).map(p => ({ ...p, image: sprite(p.c) }));
    const off = document.createElement('canvas'),
      cpu = root.GeoCPU.create(off, invalidate);
    let disposed = false;
    cpu.ready
      .then(() => {
        if (!disposed) invalidate();
      })
      .catch(() => {});
    // The star field is the costly part of a CPU frame; it is drawn into a layer that is reused until the
    // camera or the canvas size changes, so a selection or a hover repaints only the worlds.
    const layer = document.createElement('canvas');
    let layerKey = '';
    function starField(state, vp, scale) {
      const key = canvas.width + 'x' + canvas.height + ':' + vp.map(v => v.toFixed(5)).join(',');
      if (key === layerKey) return;
      layer.width = canvas.width;
      layer.height = canvas.height;
      const l = layer.getContext('2d');
      l.setTransform(scale, 0, 0, scale, 0, 0);
      l.globalCompositeOperation = 'lighter';
      for (const p of rows) {
        const q = M.project(p.p, vp, state.width, state.height);
        if (!q.visible) continue;
        const size = M.clamp((p.size * state.height * state.camera.f) / q.depth, 1.2, 70);
        l.globalAlpha = M.clamp(p.a * (p.size < 0.3 ? 2.2 : 2.6), 0, 1);
        l.drawImage(p.image, q.x - size / 2, q.y - size / 2, size, size);
      }
      layerKey = key;
    }
    return {
      kind: 'canvas',
      draw(state) {
        const scale = canvas.width / state.width;
        const vp = M.multiply(state.camera.vp, M.rotation(state.angle));
        starField(state, vp, scale);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(layer, 0, 0);
        ctx.setTransform(scale, 0, 0, scale, 0, 0);
        ctx.globalAlpha = 1;
        ctx.globalCompositeOperation = 'source-over';
        const selected = state.worlds.find(p => p.id === state.selected);
        if (selected && !selected.marker && !selected.emissive && !state.light) {
          ctx.beginPath();
          for (let i = 0; i <= 80; i++) {
            const a = (i / 80) * TAU,
              r = selected.radius * 1.85,
              q = M.project(
                [selected.position[0] + Math.cos(a) * r, selected.position[1], selected.position[2] + Math.sin(a) * r],
                state.camera.vp,
                state.width,
                state.height,
              );
            if (i === 0) ctx.moveTo(q.x, q.y);
            else ctx.lineTo(q.x, q.y);
          }
          ctx.strokeStyle = 'rgba(230,185,119,.65)';
          ctx.stroke();
        }
        const sorted = [...state.worlds].sort((a, b) => b.screen.depth - a.screen.depth);
        off.width = canvas.width;
        off.height = canvas.height;
        cpu.clear(off.width, off.height, scale);
        for (const p of sorted) {
          if (!p.screen.visible || p.marker) continue;
          if (p.emissive) {
            const { x, y, radius: r } = p.screen,
              g = ctx.createRadialGradient(x, y, 0, x, y, r * 2.8);
            g.addColorStop(0, p.land);
            g.addColorStop(0.25, p.land);
            g.addColorStop(0.37, p.land + 'c0');
            g.addColorStop(0.6, p.land + '18');
            g.addColorStop(1, p.land + '00');
            ctx.fillStyle = g;
            ctx.fillRect(x - r * 2.8, y - r * 2.8, r * 5.6, r * 5.6);
            ctx.save();
            ctx.beginPath();
            ctx.arc(x, y, r, 0, TAU);
            ctx.clip();
            const photosphere = ctx.createRadialGradient(x - r * 0.2, y - r * 0.22, 0, x, y, r);
            photosphere.addColorStop(0, '#fff5df');
            photosphere.addColorStop(0.6, p.land);
            photosphere.addColorStop(1, p.deep);
            ctx.fillStyle = photosphere;
            ctx.fillRect(x - r, y - r, r * 2, r * 2);
            ctx.globalAlpha = 0.12;
            ctx.fillStyle = p.deep;
            for (let i = 0; i < 180; i++) {
              const u = Math.sin(i * 71.3 + state.time * 0.04),
                v = Math.cos(i * 19.7);
              ctx.beginPath();
              ctx.arc(x + u * r, y + v * r, 1 + Math.abs(u) * r * 0.025, 0, TAU);
              ctx.fill();
            }
            ctx.restore();
            continue;
          }
          let light;
          if (state.light) {
            const v = state.light.map((v, i) => v - p.position[i]),
              m = state.camera.view;
            light = [
              m[0] * v[0] + m[4] * v[1] + m[8] * v[2],
              m[1] * v[0] + m[5] * v[1] + m[9] * v[2],
              m[2] * v[0] + m[6] * v[1] + m[10] * v[2],
            ];
          }
          cpu.paint(p, { x: p.screen.x, y: p.screen.y, r: p.screen.radius, hero: 0, light }, state.time, 1);
        }
        ctx.drawImage(off, 0, 0, state.width, state.height);
      },
      dispose() {
        disposed = true;
        cpu.dispose();
        sprites.clear();
      },
      textureCount: () => cpu.textureCount(),
    };
  }

  function create(chart, onSelect, onOpen = onSelect) {
    let canvas = chart.querySelector('canvas'),
      renderer,
      raf = 0,
      last = 0,
      time = 0,
      angle = 0,
      selected = 'M01',
      disposed = false,
      hovering = false,
      dragging = false,
      visible = true;
    let width = 1,
      height = 1,
      azimuth = 0,
      elevation = 0.66,
      distance = 34,
      target = [0, 0, 0],
      flight = null,
      flightTimer = 0;
    const worlds = root.GeoAstro.systems.map(s => ({
      ...root.GeoPlanets.byId[s.id],
      name: s.name,
      land: s.star.color,
      marker: true,
      radius: 0.025,
    }));
    const data = M.particles(window.innerWidth < 600 ? 60000 : 120000),
      buttons = [...chart.querySelectorAll('[data-destination]')],
      listeners = [];
    const leaders = new Map(
      [...chart.querySelectorAll('[data-leader]')].map(g => [
        g.dataset.leader,
        {
          group: g,
          line: g.querySelector('path'),
          pin: g.querySelector('.leader-pin'),
          target: g.querySelector('.leader-target'),
        },
      ]),
    );
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    const paused = () => Boolean(root.GeoSpace?.debug().paused ?? reduced.matches);
    const state = { width, height, time, angle, selected, worlds, camera: null };
    const listen = (el, event, fn, options) => {
      el.addEventListener(event, fn, options);
      listeners.push(() => el.removeEventListener(event, fn, options));
    };
    const invalidate = () => {
      if (!disposed && !raf) raf = requestAnimationFrame(tick);
    };
    function initialize() {
      try {
        renderer = webgl(canvas, data, worlds, invalidate);
      } catch (_) {
        const next = canvas.cloneNode(false);
        canvas.replaceWith(next);
        canvas = next;
        try {
          renderer = software(canvas, data, invalidate);
        } catch (_) {
          renderer = null;
          chart.dataset.renderer = 'essential';
          return;
        }
      }
      chart.dataset.renderer = renderer.kind;
      chart.classList.add('scene-ready');
    }
    initialize();
    function resize() {
      const r = chart.getBoundingClientRect();
      width = Math.max(1, r.width);
      height = Math.max(1, r.height);
      chart.dataset.compact = String(width < 580);
      // The CPU renderer paints at one device pixel per CSS pixel: its cost grows with the pixel count.
      const dpr = Math.min(window.devicePixelRatio || 1, renderer?.kind === 'canvas' ? 1 : 1.5, 1600 / width);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      invalidate();
    }
    function layout(now) {
      const fitDistance = M.fitDistance(width, height, distance);
      if (flight) {
        const t = M.clamp((now - flight.started) / 1350, 0, 1),
          e = t * t * (3 - 2 * t);
        target = flight.target.map((v, i) => flight.fromTarget[i] + (v - flight.fromTarget[i]) * e);
        distance = flight.distance + (5.6 - flight.distance) * e;
        if (t === 1) {
          finish();
          return false;
        }
      }
      state.width = width;
      state.height = height;
      state.time = time;
      state.angle = angle;
      state.selected = selected;
      state.camera = M.camera(azimuth, elevation, flight ? distance : fitDistance, target, width / height);
      for (const p of worlds) {
        p.position = M.destination(p.id, angle);
        p.screen = M.project(p.position, state.camera.vp, width, height);
        p.screen.radius = (p.radius * height * state.camera.f) / (2 * p.screen.depth);
      }
      const labelLayout = M.labels(worlds, width, height);
      chart.querySelector('.galaxy-leaders').setAttribute('viewBox', `0 0 ${width} ${height}`);
      for (const b of buttons) {
        const p = worlds.find(p => p.id === b.dataset.destination),
          s = p.screen,
          l = labelLayout.find(l => l.id === p.id),
          hidden = !s.visible || Boolean(flight);
        b.style.left = l.x + 'px';
        b.style.top = l.y + 'px';
        b.style.width = l.width + 'px';
        b.style.height = l.height + 'px';
        b.dataset.side = l.side;
        b.classList.toggle('off-view', hidden);
        const g = leaders.get(p.id),
          endX = l.x + (l.side === 'left' ? l.width : 0),
          endY = l.y + l.height / 2;
        const dx = endX - s.x,
          dy = endY - s.y,
          d = Math.hypot(dx, dy) || 1,
          rad = 0,
          startX = s.x + (dx / d) * rad,
          startY = s.y + (dy / d) * rad;
        const elbowX = endX + (l.side === 'left' ? 24 : -24);
        g.line.setAttribute(
          'd',
          `M${startX.toFixed(1)},${startY.toFixed(1)} L${elbowX.toFixed(1)},${endY.toFixed(1)} L${endX.toFixed(1)},${endY.toFixed(1)}`,
        );
        g.pin.setAttribute('cx', startX);
        g.pin.setAttribute('cy', startY);
        g.target.setAttribute('cx', s.x);
        g.target.setAttribute('cy', s.y);
        g.target.setAttribute('r', p.id === selected ? 12 : 5);
        g.group.classList.toggle('selected', p.id === selected);
        g.group.style.display = hidden ? 'none' : '';
      }
      return true;
    }
    function tick(now) {
      raf = 0;
      if (disposed || !chart.isConnected || !renderer || document.hidden || !visible) {
        last = 0;
        return;
      }
      if (renderer.kind === 'canvas' && last && now - last < 32 && !paused() && !flight) {
        raf = requestAnimationFrame(tick);
        return;
      }
      const dt = last ? Math.min((now - last) / 1000, 0.1) : 0;
      last = now;
      // The CPU renderer draws on demand (selection, drag, flight): a frame costs it a long task, and with the
      // chart in the first screen a continuous rotation would keep the main thread busy.
      const continuous = !paused() && renderer.kind !== 'canvas';
      if (continuous) {
        time += dt;
        if (!hovering && !dragging && !flight) angle += dt * 0.018;
      }
      if (layout(now)) renderer.draw(state);
      if (continuous || flight) raf = requestAnimationFrame(tick);
      else last = 0;
    }
    function finish() {
      if (!flight) return;
      const done = flight.done;
      flight = null;
      clearTimeout(flightTimer);
      chart.classList.remove('is-travelling');
      done();
    }
    function pick(x, y) {
      return worlds
        .filter(
          p => p.screen?.visible && Math.hypot(x - p.screen.x, y - p.screen.y) < Math.max(20, p.screen.radius * 1.6),
        )
        .sort((a, b) => a.screen.depth - b.screen.depth)[0];
    }
    const pointers = new Map();
    let start = null,
      pinch = 0,
      hoverPick = null,
      pickTimer = 0;
    function clearPick() {
      clearTimeout(pickTimer);
      hoverPick = null;
    }
    listen(canvas, 'pointerdown', e => {
      if (flight) return;
      clearPick();
      pointers.set(e.pointerId, [e.clientX, e.clientY]);
      start = { x: e.clientX, y: e.clientY, moved: false };
      dragging = true;
      canvas.setPointerCapture(e.pointerId);
      if (pointers.size === 2) {
        const q = [...pointers.values()];
        pinch = Math.hypot(q[0][0] - q[1][0], q[0][1] - q[1][1]);
      }
    });
    listen(canvas, 'pointermove', e => {
      if (flight) return;
      const r = canvas.getBoundingClientRect();
      if (pointers.has(e.pointerId)) {
        const prev = pointers.get(e.pointerId);
        pointers.set(e.pointerId, [e.clientX, e.clientY]);
        if (pointers.size === 2) {
          const q = [...pointers.values()],
            next = Math.hypot(q[0][0] - q[1][0], q[0][1] - q[1][1]);
          if (pinch > 0) distance = M.clamp((distance * pinch) / Math.max(10, next), 22, 58);
          pinch = next;
        } else {
          azimuth -= (e.clientX - prev[0]) * 0.006;
          elevation = M.clamp(elevation + (e.clientY - prev[1]) * 0.004, 0.25, 1.36);
        }
        if (start && Math.hypot(e.clientX - start.x, e.clientY - start.y) > 5) start.moved = true;
        invalidate();
      } else {
        const p = pick(e.clientX - r.left, e.clientY - r.top);
        hovering = Boolean(p);
        canvas.style.cursor = p ? 'pointer' : 'grab';
        if (p?.id !== hoverPick) {
          clearPick();
          if (p && p.id !== selected) {
            hoverPick = p.id;
            pickTimer = setTimeout(() => {
              if (!disposed && !flight && hoverPick === p.id) onSelect(p.id);
            }, 220);
          }
        }
      }
    });
    function up(e) {
      const r = canvas.getBoundingClientRect();
      if (start && !start.moved && !flight) {
        const p = pick(e.clientX - r.left, e.clientY - r.top);
        if (p) onOpen(p.id);
      }
      pointers.delete(e.pointerId);
      if (!pointers.size) {
        dragging = false;
        start = null;
        pinch = 0;
      }
      invalidate();
    }
    listen(canvas, 'pointerup', up);
    listen(canvas, 'pointercancel', () => {
      pointers.clear();
      start = null;
      dragging = false;
      pinch = 0;
      invalidate();
    });
    listen(canvas, 'pointerleave', () => {
      clearPick();
      hovering = false;
      invalidate();
    });
    listen(
      canvas,
      'wheel',
      e => {
        if (flight) return;
        e.preventDefault();
        distance = M.clamp(distance * Math.exp(e.deltaY * 0.001), 22, 58);
        invalidate();
      },
      { passive: false },
    );
    listen(canvas, 'keydown', e => {
      if (flight) return;
      const keys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', '+', '-', 'Home'];
      if (!keys.includes(e.key)) return;
      e.preventDefault();
      if (e.key === 'ArrowLeft') azimuth += 0.12;
      if (e.key === 'ArrowRight') azimuth -= 0.12;
      if (e.key === 'ArrowUp') elevation = M.clamp(elevation + 0.1, 0.25, 1.36);
      if (e.key === 'ArrowDown') elevation = M.clamp(elevation - 0.1, 0.25, 1.36);
      if (e.key === '+') distance = M.clamp(distance - 3, 22, 58);
      if (e.key === '-') distance = M.clamp(distance + 3, 22, 58);
      if (e.key === 'Home') reset();
      invalidate();
    });
    function reset() {
      if (flight) finish();
      azimuth = 0;
      elevation = 0.66;
      distance = 34;
      target = [0, 0, 0];
      angle = 0;
      invalidate();
    }
    for (const b of buttons) {
      listen(b, 'pointerenter', () => {
        hovering = true;
      });
      listen(b, 'pointerleave', () => {
        hovering = false;
        invalidate();
      });
      listen(b, 'focus', () => {
        hovering = true;
      });
      listen(b, 'blur', () => {
        hovering = false;
        invalidate();
      });
    }
    for (const b of chart.querySelectorAll('[data-camera]'))
      listen(b, 'click', () => {
        if (flight) return;
        if (b.dataset.camera === 'reset') reset();
        else distance = M.clamp(distance + (b.dataset.camera === 'in' ? -4 : 4), 22, 58);
        invalidate();
      });
    listen(chart.querySelector('.galaxy-skip'), 'click', finish);
    listen(document, 'keydown', e => {
      if (e.key === 'Escape' && flight) {
        e.preventDefault();
        finish();
      }
    });
    listen(document, 'visibilitychange', () => {
      if (document.hidden && flight) finish();
      last = 0;
      invalidate();
    });
    listen(document, 'geospace:pause', () => {
      last = 0;
      invalidate();
    });
    listen(window, 'resize', resize);
    let observer = null;
    if (window.IntersectionObserver) {
      observer = new IntersectionObserver(entries => {
        visible = entries[0].isIntersecting;
        last = 0;
        invalidate();
      });
      observer.observe(chart);
    }
    listen(canvas, 'webglcontextlost', e => {
      e.preventDefault();
      if (disposed) return;
      renderer?.dispose();
      renderer = null;
      chart.classList.remove('scene-ready');
      chart.dataset.renderer = 'essential';
      if (flight) finish();
    });
    listen(canvas, 'webglcontextrestored', () => {
      if (disposed) return;
      try {
        renderer = webgl(canvas, data, worlds, invalidate);
        chart.dataset.renderer = 'webgl';
        chart.classList.add('scene-ready');
        resize();
      } catch (_) {
        chart.dataset.renderer = 'essential';
      }
    });
    resize();
    // Place the system buttons before the first paint: the chart is in the first screen, and waiting for
    // the visibility observer would move them after they are drawn (layout shift).
    if (renderer) layout(performance.now());
    return {
      select(id) {
        clearPick();
        selected = id;
        invalidate();
      },
      travel(id, done) {
        if (!renderer || paused() || reduced.matches) {
          done();
          return;
        }
        if (flight) return;
        selected = id;
        flight = {
          started: performance.now(),
          fromTarget: [...target],
          target: M.destination(id, angle),
          distance: M.fitDistance(width, height, distance),
          done,
        };
        chart.querySelector('.galaxy-flight-name').textContent = root.GeoAstro.byId[id].name;
        chart.classList.add('is-travelling');
        chart.querySelector('.galaxy-skip').focus({ preventScroll: true });
        flightTimer = setTimeout(finish, 1500);
        invalidate();
      },
      dispose() {
        disposed = true;
        clearPick();
        cancelAnimationFrame(raf);
        clearTimeout(flightTimer);
        observer?.disconnect();
        for (const remove of listeners) remove();
        renderer?.dispose();
        renderer = null;
      },
      debug: () => ({
        renderer: renderer?.kind || 'essential',
        stars: data.stars.length,
        dust: data.dust.length,
        angle,
        time,
        azimuth,
        elevation,
        distance,
        selected,
        flight: Boolean(flight),
        textures: renderer?.textureCount() || 0,
        worlds: worlds.map(p => ({ id: p.id, position: p.position, screen: p.screen })),
      }),
    };
  }
  root.GeoGalaxyScene = Object.freeze({ create, webgl, software });
})(globalThis);
