/* Procedural world-space environment. No image assets, skybox or canvas textures.
 * The nebula pass integrates emission and absorption through 3D density fields.
 * Only this expensive pass uses a reduced resolution; stars stay full resolution. */
(function (root) {
  'use strict';
  const volumeVertex = `attribute vec2 aPosition;varying vec2 vUV;
    void main(){vUV=aPosition*.5+.5;gl_Position=vec4(aPosition,0.,1.);}`;
  const volumeFragment = `precision highp float;varying vec2 vUV;
    uniform mat3 uBasis;uniform vec3 uOrigin;uniform vec2 uSize;uniform float uF,uStrength,uSteps;
    float hash(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
    float noise3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
      return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
      mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);}
    float fbm(vec3 p){return .55*noise3(p)+.27*noise3(p*2.03+7.1)+.13*noise3(p*4.11+17.3)+.05*noise3(p*8.21);}
    void main(){vec2 uv=vUV*2.-1.;uv.x*=uSize.x/uSize.y;
      vec3 rd=normalize(uBasis*vec3(uv/uF,-1.));vec3 ro=uOrigin;
      vec3 sum=vec3(0.);float trans=1.;
      float jitter=.5;
      for(int i=0;i<56;i++){
        if(float(i)>=uSteps)break;
        float stride=308./uSteps;
        float t=35.+(float(i)+jitter)*stride;vec3 p=ro+rd*t;
        vec3 q=(p-vec3(-75.,-105.,-145.))/vec3(135.,90.,115.);
        vec3 r=(p-vec3(115.,-100.,-120.))/vec3(100.,95.,115.);
        vec3 s=(p-vec3(-40.,-80.,170.))/vec3(135.,85.,100.);
        float envelope=exp(-dot(q,q)*2.)+exp(-dot(r,r)*2.)*.78+exp(-dot(s,s)*2.)*.65;
        if(envelope<.012)continue;
        vec3 warp=vec3(fbm(p*.014),fbm(p*.014+23.),fbm(p*.014+49.));
        float n=fbm(p*.067+warp*4.8),fine=noise3(p*.19+warp*4.);
        float filaments=pow(max(0.,1.-abs(n-.51)*11.),4.);
        float gas=pow(smoothstep(.30,.72,n),1.65)*envelope;
        float dust=smoothstep(.48,.73,fbm(p*.031+71.))*envelope;
        float opacity=(gas*.14+dust*.24)*uStrength*stride/5.5;
        float warm=smoothstep(.43,.69,fbm(p*.009+110.));
        vec3 cold=mix(vec3(.045,.22,.43),vec3(.23,.065,.29),smoothstep(-50.,90.,p.x));
        vec3 color=mix(cold,vec3(.62,.28,.1),warm);
        vec3 emission=color*(gas*(.5+fine)*1.9+filaments*envelope*.45);
        sum+=trans*emission*opacity;trans*=exp(-opacity);
        if(trans<.025)break;
      }
      vec3 c=sum*1.9;gl_FragColor=vec4(c,1.-trans);
    }`;
  const copyFragment = `precision mediump float;varying vec2 vUV;uniform sampler2D uMap;
    void main(){gl_FragColor=texture2D(uMap,vUV);}`;
  const skyVertex = `attribute vec3 aPosition;attribute vec4 aColor;attribute float aSize;
    uniform mat3 uView;uniform float uF,uAspect,uScale;varying vec4 vColor;
    void main(){vec3 p=uView*aPosition;float z=-p.z;
      gl_Position=vec4(p.x*uF/uAspect,p.y*uF,z*.999,z);
      gl_PointSize=clamp(aSize*uScale,1.,8.);vColor=aColor;}`;
  const skyFragment = `precision mediump float;varying vec4 vColor;
    void main(){float r=length(gl_PointCoord*2.-1.);if(r>1.)discard;
      gl_FragColor=vec4(vColor.rgb,vColor.a*exp(-r*r*4.)*(1.-smoothstep(.7,1.,r)));}`;
  let catalogue;
  function skyData() {
    if (catalogue) return catalogue;
    const rng = root.GeoGalaxyModel.random(64173),
      count = 52000;
    const data = new Float32Array(count * 8),
      tau = Math.PI * 2;
    for (let i = 0; i < count; i++) {
      const a = rng() * tau,
        z = rng() * 2 - 1,
        r = Math.sqrt(1 - z * z);
      let p = [r * Math.cos(a), z, r * Math.sin(a)],
        color = [0.67, 0.8, 1];
      let size = 0.6 + Math.pow(rng(), 10) * 3.7,
        alpha = 0.19 + rng() * 0.5;
      if (i < 23000) {
        const lat = (rng() + rng() + rng() - 1.5) * 0.095;
        p = [Math.cos(a), lat + Math.sin(a) * 0.85 - Math.cos(a) * 0.15, Math.sin(a)];
        alpha *= 0.45;
        size = 0.7;
      } else if (i > 44000) {
        const g = i % 3,
          radius = Math.pow(rng(), 0.65),
          theta = radius * 8 + (i % 2) * Math.PI + (rng() - 0.5) * 0.35;
        const centers = [
          [-0.66, -0.68, -1],
          [0.82, -0.82, -1],
          [-0.5, -0.4, 1],
        ];
        p = [
          centers[g][0] + Math.cos(theta) * radius * 0.085,
          centers[g][1] + Math.sin(theta) * radius * 0.026,
          centers[g][2] + (rng() - 0.5) * 0.012,
        ];
        color = radius < 0.2 ? [1, 0.83, 0.52] : [0.4, 0.65, 1];
        alpha = 0.25;
        size = 0.8;
      } else if (rng() < 0.18) color = [1, 0.77, 0.51];
      data.set([...p, ...color, alpha, size], i * 8);
    }
    catalogue = data;
    return data;
  }
  function program(gl, vertex, fragment) {
    const p = gl.createProgram();
    for (const [type, code] of [
      [gl.VERTEX_SHADER, vertex],
      [gl.FRAGMENT_SHADER, fragment],
    ]) {
      const s = gl.createShader(type);
      gl.shaderSource(s, code);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
        const reason = gl.getShaderInfoLog(s);
        gl.deleteShader(s);
        gl.deleteProgram(p);
        throw Error(reason);
      }
      gl.attachShader(p, s);
      gl.deleteShader(s);
    }
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      const reason = gl.getProgramInfoLog(p);
      gl.deleteProgram(p);
      throw Error(reason);
    }
    return p;
  }
  function create(gl) {
    // Detect the actual rasteriser even when the application forces its WebGL path.
    // CPU WebGL still renders the 3D volume, with a bounded sample budget.
    const info = gl.getExtension('WEBGL_debug_renderer_info');
    const software = /swiftshader|llvmpipe|softpipe|software rasterizer|basic render driver/i.test(
      info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
    );
    const volume = program(gl, volumeVertex, volumeFragment),
      copy = program(gl, volumeVertex, copyFragment),
      sky = program(gl, skyVertex, skyFragment);
    const quad = gl.createBuffer(),
      stars = gl.createBuffer(),
      texture = gl.createTexture(),
      target = gl.createFramebuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quad);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, stars);
    gl.bufferData(gl.ARRAY_BUFFER, skyData(), gl.STATIC_DRAW);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    let tw = 0,
      th = 0,
      lastKey = '',
      detail = software ? 64 : 640,
      steps = software ? 16 : 56;
    const location = new Map();
    function loc(p, name) {
      if (!location.has(p)) location.set(p, new Map());
      const cache = location.get(p);
      if (!cache.has(name)) cache.set(name, gl.getUniformLocation(p, name));
      return cache.get(name);
    }
    function attribute(p, name, n, stride, offset) {
      const a = gl.getAttribLocation(p, name);
      gl.enableVertexAttribArray(a);
      gl.vertexAttribPointer(a, n, gl.FLOAT, false, stride, offset);
    }
    function screen(p) {
      gl.useProgram(p);
      gl.bindBuffer(gl.ARRAY_BUFFER, quad);
      attribute(p, 'aPosition', 2, 0, 0);
    }
    function draw(camera, width, height, strength = 1) {
      const m = camera.view,
        basis = new Float32Array([m[0], m[4], m[8], m[1], m[5], m[9], m[2], m[6], m[10]]);
      const view = new Float32Array([m[0], m[1], m[2], m[4], m[5], m[6], m[8], m[9], m[10]]);
      const scale = Math.min(1, detail / Math.max(width, height));
      const w = Math.max(1, Math.round(width * scale)),
        h = Math.max(1, Math.round(height * scale));
      const origin = camera.eye.map(x => x * 0.025);
      const key = [...basis, ...origin, width, height, strength, detail].map(x => Math.round(x * 10000)).join(',');
      gl.disable(gl.DEPTH_TEST);
      gl.depthMask(false);
      gl.disable(gl.BLEND);
      if (key !== lastKey) {
        gl.bindTexture(gl.TEXTURE_2D, texture);
        if (w !== tw || h !== th) {
          tw = w;
          th = h;
          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
        }
        gl.bindFramebuffer(gl.FRAMEBUFFER, target);
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0);
        if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) !== gl.FRAMEBUFFER_COMPLETE)
          throw Error('Nebula framebuffer unavailable');
        gl.viewport(0, 0, w, h);
        screen(volume);
        gl.uniformMatrix3fv(loc(volume, 'uBasis'), false, basis);
        gl.uniform3fv(loc(volume, 'uOrigin'), origin);
        gl.uniform2f(loc(volume, 'uSize'), width, height);
        gl.uniform1f(loc(volume, 'uF'), camera.f);
        gl.uniform1f(loc(volume, 'uStrength'), strength);
        gl.uniform1f(loc(volume, 'uSteps'), steps);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        lastKey = key;
      }
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.viewport(0, 0, width, height);
      gl.useProgram(sky);
      gl.bindBuffer(gl.ARRAY_BUFFER, stars);
      attribute(sky, 'aPosition', 3, 32, 0);
      attribute(sky, 'aColor', 4, 32, 12);
      attribute(sky, 'aSize', 1, 32, 28);
      gl.uniformMatrix3fv(loc(sky, 'uView'), false, view);
      gl.uniform1f(loc(sky, 'uF'), camera.f);
      gl.uniform1f(loc(sky, 'uAspect'), width / height);
      gl.uniform1f(loc(sky, 'uScale'), Math.min(1.8, width / 1000));
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
      gl.drawArrays(gl.POINTS, 0, skyData().length / 8);
      screen(copy);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, texture);
      gl.uniform1i(loc(copy, 'uMap'), 0);
      gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      gl.disable(gl.BLEND);
      gl.depthMask(true);
      gl.enable(gl.DEPTH_TEST);
    }
    return {
      draw,
      reduce: () => {
        detail = Math.min(detail, 160);
        steps = Math.min(steps, 24);
      },
      debug: () => ({ stars: 52000, nebulaSteps: steps, nebulaWidth: tw, software }),
      dispose() {
        for (const p of [volume, copy, sky]) gl.deleteProgram(p);
        gl.deleteBuffer(quad);
        gl.deleteBuffer(stars);
        gl.deleteTexture(texture);
        gl.deleteFramebuffer(target);
      },
    };
  }
  root.GeoUniverse = Object.freeze({
    create,
    skyData,
    shaders: { volumeVertex, volumeFragment, skyVertex, skyFragment, copyFragment },
  });
})(globalThis);
