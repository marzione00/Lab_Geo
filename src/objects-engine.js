/* WebGL2 engine of the notable objects: HDR rendering with physically based bloom and tone mapping, an orbital
   camera with pointer, wheel, pinch and keyboard controls, a geometry worker and the shared sky of the atlas.
   Each object scene draws into the HDR target; the engine owns the frame loop and every GPU resource. */
(function (root) {
  'use strict';
  const TAU = Math.PI * 2;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const FULLSCREEN = `#version 300 es
    out vec2 vUV;
    void main(){vec2 p=vec2(float((gl_VertexID<<1)&2),float(gl_VertexID&2));vUV=p;gl_Position=vec4(p*2.-1.,0.,1.);}`;
  // Bloom after Jimenez (2014): 13-tap downsampling with a Karis average on the first level, tent upsampling.
  const DOWN = `#version 300 es
    precision highp float;in vec2 vUV;uniform sampler2D uSource;uniform vec2 uTexel;uniform float uKaris;out vec4 o;
    vec3 t(vec2 d){return texture(uSource,vUV+d*uTexel).rgb;}
    float w(vec3 c){return 1./(1.+dot(c,vec3(.2126,.7152,.0722))*uKaris);}
    void main(){
      vec3 a=t(vec2(-2,2)),b=t(vec2(0,2)),c=t(vec2(2,2)),d=t(vec2(-2,0)),e=t(vec2(0)),f=t(vec2(2,0));
      vec3 g=t(vec2(-2,-2)),h=t(vec2(0,-2)),i=t(vec2(2,-2)),j=t(vec2(-1,1)),k=t(vec2(1,1)),l=t(vec2(-1,-1)),m=t(vec2(1,-1));
      vec3 g0=(j+k+l+m)*.25,g1=(a+b+d+e)*.25,g2=(b+c+e+f)*.25,g3=(d+e+g+h)*.25,g4=(e+f+h+i)*.25;
      float w0=w(g0),w1=w(g1),w2=w(g2),w3=w(g3),w4=w(g4);
      vec3 s=g0*w0*.5+(g1*w1+g2*w2+g3*w3+g4*w4)*.125;
      float ws=w0*.5+(w1+w2+w3+w4)*.125;o=vec4(s/ws,1.);}`;
  const UP = `#version 300 es
    precision highp float;in vec2 vUV;uniform sampler2D uSource;uniform vec2 uTexel;uniform float uRadius;out vec4 o;
    vec3 t(vec2 d){return texture(uSource,vUV+d*uTexel*uRadius).rgb;}
    void main(){vec3 s=t(vec2(-1,1))+t(vec2(1,1))+t(vec2(-1,-1))+t(vec2(1,-1))
      +2.*(t(vec2(0,1))+t(vec2(0,-1))+t(vec2(-1,0))+t(vec2(1,0)))+4.*t(vec2(0));o=vec4(s/16.,1.);}`;
  // ACES filmic curve (Hill's fit of the RRT and ODT), sRGB transfer, vignette and triangular dithering.
  const FINAL = `#version 300 es
    precision highp float;in vec2 vUV;uniform sampler2D uScene,uBloom;uniform float uExposure,uBloomStrength,uSeed;
    out vec4 o;
    const mat3 I=mat3(.59719,.07600,.02840,.35458,.90834,.13383,.04823,.01566,.83777);
    const mat3 O=mat3(1.60475,-.10208,-.00327,-.53108,1.10813,-.07276,-.07367,-.00605,1.07602);
    vec3 rrt(vec3 v){vec3 a=v*(v+.0245786)-.000090537;vec3 b=v*(.983729*v+.4329510)+.238081;return a/b;}
    vec3 srgb(vec3 c){return mix(c*12.92,1.055*pow(c,vec3(1./2.4))-.055,step(.0031308,c));}
    float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233))+uSeed)*43758.5453);}
    void main(){vec3 c=texture(uScene,vUV).rgb+texture(uBloom,vUV).rgb*uBloomStrength;
      c=clamp(O*rrt(I*(c*uExposure)),0.,1.);
      vec2 q=vUV-.5;c*=1.-dot(q,q)*.38;
      c=srgb(c)+(h(gl_FragCoord.xy)+h(gl_FragCoord.yx+3.1)-1.)/255.;o=vec4(c,1.);}`;

  // Column-major perspective camera with configurable clipping planes (camera at eye, looking at target).
  function cameraMatrices(eye, target, up, aspect, fov, near, far) {
    const sub = (a, b) => a.map((x, i) => x - b[i]),
      norm = v => {
        const l = Math.hypot(...v) || 1;
        return v.map(x => x / l);
      },
      cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]],
      dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    const z = norm(sub(eye, target)),
      x = norm(cross(up, z)),
      y = cross(z, x);
    const view = new Float32Array([
      x[0],
      y[0],
      z[0],
      0,
      x[1],
      y[1],
      z[1],
      0,
      x[2],
      y[2],
      z[2],
      0,
      -dot(x, eye),
      -dot(y, eye),
      -dot(z, eye),
      1,
    ]);
    const f = 1 / Math.tan(fov / 2);
    const proj = new Float32Array([
      f / aspect,
      0,
      0,
      0,
      0,
      f,
      0,
      0,
      0,
      0,
      (far + near) / (near - far),
      -1,
      0,
      0,
      (2 * far * near) / (near - far),
      0,
    ]);
    return { view, proj, vp: multiply(proj, view), eye, target, f, near, far, aspect, right: x, up: y, back: z };
  }
  function multiply(a, b) {
    const o = new Float32Array(16);
    for (let c = 0; c < 4; c++)
      for (let r = 0; r < 4; r++) {
        let s = 0;
        for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k];
        o[c * 4 + r] = s;
      }
    return o;
  }
  function invert(m) {
    const inv = new Float32Array(16),
      a = m;
    inv[0] =
      a[5] * a[10] * a[15] -
      a[5] * a[11] * a[14] -
      a[9] * a[6] * a[15] +
      a[9] * a[7] * a[14] +
      a[13] * a[6] * a[11] -
      a[13] * a[7] * a[10];
    inv[4] =
      -a[4] * a[10] * a[15] +
      a[4] * a[11] * a[14] +
      a[8] * a[6] * a[15] -
      a[8] * a[7] * a[14] -
      a[12] * a[6] * a[11] +
      a[12] * a[7] * a[10];
    inv[8] =
      a[4] * a[9] * a[15] -
      a[4] * a[11] * a[13] -
      a[8] * a[5] * a[15] +
      a[8] * a[7] * a[13] +
      a[12] * a[5] * a[11] -
      a[12] * a[7] * a[9];
    inv[12] =
      -a[4] * a[9] * a[14] +
      a[4] * a[10] * a[13] +
      a[8] * a[5] * a[14] -
      a[8] * a[6] * a[13] -
      a[12] * a[5] * a[10] +
      a[12] * a[6] * a[9];
    inv[1] =
      -a[1] * a[10] * a[15] +
      a[1] * a[11] * a[14] +
      a[9] * a[2] * a[15] -
      a[9] * a[3] * a[14] -
      a[13] * a[2] * a[11] +
      a[13] * a[3] * a[10];
    inv[5] =
      a[0] * a[10] * a[15] -
      a[0] * a[11] * a[14] -
      a[8] * a[2] * a[15] +
      a[8] * a[3] * a[14] +
      a[12] * a[2] * a[11] -
      a[12] * a[3] * a[10];
    inv[9] =
      -a[0] * a[9] * a[15] +
      a[0] * a[11] * a[13] +
      a[8] * a[1] * a[15] -
      a[8] * a[3] * a[13] -
      a[12] * a[1] * a[11] +
      a[12] * a[3] * a[9];
    inv[13] =
      a[0] * a[9] * a[14] -
      a[0] * a[10] * a[13] -
      a[8] * a[1] * a[14] +
      a[8] * a[2] * a[13] +
      a[12] * a[1] * a[10] -
      a[12] * a[2] * a[9];
    inv[2] =
      a[1] * a[6] * a[15] -
      a[1] * a[7] * a[14] -
      a[5] * a[2] * a[15] +
      a[5] * a[3] * a[14] +
      a[13] * a[2] * a[7] -
      a[13] * a[3] * a[6];
    inv[6] =
      -a[0] * a[6] * a[15] +
      a[0] * a[7] * a[14] +
      a[4] * a[2] * a[15] -
      a[4] * a[3] * a[14] -
      a[12] * a[2] * a[7] +
      a[12] * a[3] * a[6];
    inv[10] =
      a[0] * a[5] * a[15] -
      a[0] * a[7] * a[13] -
      a[4] * a[1] * a[15] +
      a[4] * a[3] * a[13] +
      a[12] * a[1] * a[7] -
      a[12] * a[3] * a[5];
    inv[14] =
      -a[0] * a[5] * a[14] +
      a[0] * a[6] * a[13] +
      a[4] * a[1] * a[14] -
      a[4] * a[2] * a[13] -
      a[12] * a[1] * a[6] +
      a[12] * a[2] * a[5];
    inv[3] =
      -a[1] * a[6] * a[11] +
      a[1] * a[7] * a[10] +
      a[5] * a[2] * a[11] -
      a[5] * a[3] * a[10] -
      a[9] * a[2] * a[7] +
      a[9] * a[3] * a[6];
    inv[7] =
      a[0] * a[6] * a[11] -
      a[0] * a[7] * a[10] -
      a[4] * a[2] * a[11] +
      a[4] * a[3] * a[10] +
      a[8] * a[2] * a[7] -
      a[8] * a[3] * a[6];
    inv[11] =
      -a[0] * a[5] * a[11] +
      a[0] * a[7] * a[9] +
      a[4] * a[1] * a[11] -
      a[4] * a[3] * a[9] -
      a[8] * a[1] * a[7] +
      a[8] * a[3] * a[5];
    inv[15] =
      a[0] * a[5] * a[10] -
      a[0] * a[6] * a[9] -
      a[4] * a[1] * a[10] +
      a[4] * a[2] * a[9] +
      a[8] * a[1] * a[6] -
      a[8] * a[2] * a[5];
    const det = a[0] * inv[0] + a[1] * inv[4] + a[2] * inv[8] + a[3] * inv[12];
    for (let i = 0; i < 16; i++) inv[i] /= det || 1;
    return inv;
  }
  // Model matrix: translation, uniform scale and rotation about an axis.
  function model(position = [0, 0, 0], scale = 1, axis = [0, 1, 0], angle = 0) {
    const [x, y, z] = axis,
      c = Math.cos(angle),
      s = Math.sin(angle),
      t = 1 - c;
    const sx = Array.isArray(scale) ? scale : [scale, scale, scale];
    return new Float32Array([
      (t * x * x + c) * sx[0],
      (t * x * y + s * z) * sx[0],
      (t * x * z - s * y) * sx[0],
      0,
      (t * x * y - s * z) * sx[1],
      (t * y * y + c) * sx[1],
      (t * y * z + s * x) * sx[1],
      0,
      (t * x * z + s * y) * sx[2],
      (t * y * z - s * x) * sx[2],
      (t * z * z + c) * sx[2],
      0,
      position[0],
      position[1],
      position[2],
      1,
    ]);
  }
  // Rendering tier from the rasteriser and the device: counts and resolution scale with it.
  function tierOf(gl) {
    const info = gl.getExtension('WEBGL_debug_renderer_info'),
      name = String(gl.getParameter(info ? info.UNMASKED_RENDERER_WEBGL : gl.RENDERER) || '');
    if (/swiftshader|llvmpipe|softpipe|software rasterizer|basic render driver/i.test(name)) return 'low';
    const coarse = root.matchMedia?.('(pointer: coarse)').matches && !root.matchMedia?.('(pointer: fine)').matches;
    if (coarse || gl.getParameter(gl.MAX_TEXTURE_SIZE) < 8192) return 'medium';
    return 'high';
  }

  // A tier stored by the browser checks (geostat:objects-tier) fixes counts and resolution for comparisons.
  function storedTier() {
    try {
      const t = root.localStorage?.getItem('geostat:objects-tier');
      return ['high', 'medium', 'low'].includes(t) ? t : null;
    } catch {
      return null;
    }
  }
  // Orbital camera of a scene, with the limits declared by the scene.
  function cameraState(o) {
    return {
      azimuth: o.azimuth ?? 0.6,
      elevation: o.elevation ?? 0.35,
      distance: o.distance ?? 10,
      minDistance: o.minDistance ?? 1,
      maxDistance: o.maxDistance ?? 100,
      minElevation: o.minElevation ?? -1.45,
      maxElevation: o.maxElevation ?? 1.45,
      target: o.target?.slice() ?? [0, 0, 0],
      fov: o.fov ?? (40 * Math.PI) / 180,
      transition: null,
    };
  }
  function settings(o, tier) {
    return {
      time: o.startTime ?? 0,
      exposure: o.exposure ?? 1,
      bloom: o.bloom ?? 0.06,
      scale: { high: 1, medium: 0.85, low: 0.6 }[tier],
    };
  }

  // Half-float HDR target with 4x multisampling where the device renders to float buffers.
  function formats(gl, floatTarget, tier) {
    return {
      hdrInternal: floatTarget ? gl.RGBA16F : gl.RGBA8,
      hdrType: floatTarget ? gl.HALF_FLOAT : gl.UNSIGNED_BYTE,
      samples: floatTarget && tier !== 'low' ? Math.min(4, gl.getParameter(gl.MAX_SAMPLES)) : 0,
    };
  }
  function create(chart, options = {}) {
    let canvas = chart.querySelector('canvas');
    const gl = canvas.getContext('webgl2', {
      alpha: false,
      antialias: false,
      depth: false,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: false,
    });
    if (!gl) throw Error('WebGL2 non disponibile');
    const floatTarget = Boolean(
      gl.getExtension('EXT_color_buffer_float') || gl.getExtension('EXT_color_buffer_half_float'),
    );
    gl.getExtension('EXT_float_blend');
    const anisotropy = gl.getExtension('EXT_texture_filter_anisotropic');
    const forced = storedTier(),
      fixed = Boolean(forced),
      tier = options.tier || forced || tierOf(gl);
    const resources = [],
      listeners = [],
      programs = new Map();
    const own = (kind, obj) => {
      resources.push([kind, obj]);
      return obj;
    };
    const listen = (el, ev, fn, opt) => {
      el.addEventListener(ev, fn, opt);
      listeners.push(() => el.removeEventListener(ev, fn, opt));
    };
    // ------------------------------------------------------------ GPU helpers
    function program(vs, fs, name = 'program') {
      const p = gl.createProgram();
      for (const [type, src] of [
        [gl.VERTEX_SHADER, vs],
        [gl.FRAGMENT_SHADER, fs],
      ]) {
        const s = gl.createShader(type);
        gl.shaderSource(s, src);
        gl.compileShader(s);
        if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
          const log = gl.getShaderInfoLog(s);
          gl.deleteShader(s);
          throw Error(name + ': ' + log);
        }
        gl.attachShader(p, s);
        gl.deleteShader(s);
      }
      gl.linkProgram(p);
      if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw Error(name + ': ' + gl.getProgramInfoLog(p));
      programs.set(p, new Map());
      return own('deleteProgram', p);
    }
    // Uniform setter with cached locations; the value type selects the call.
    function set(p, name, value, kind) {
      const cache = programs.get(p);
      if (!cache.has(name)) cache.set(name, gl.getUniformLocation(p, name));
      const l = cache.get(name);
      if (l === null) return;
      if (kind === 'int') gl.uniform1i(l, value);
      else if (typeof value === 'number') gl.uniform1f(l, value);
      else if (value.length === 16) gl.uniformMatrix4fv(l, false, value);
      else if (value.length === 9 && kind === 'mat3') gl.uniformMatrix3fv(l, false, value);
      else if (value.length === 2) gl.uniform2fv(l, value);
      else if (value.length === 3) gl.uniform3fv(l, value);
      else if (value.length === 4) gl.uniform4fv(l, value);
    }
    function texture2D({
      width,
      height,
      internal,
      format,
      type,
      data = null,
      filter = gl.LINEAR,
      wrap = gl.CLAMP_TO_EDGE,
    }) {
      const t = own('deleteTexture', gl.createTexture());
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, internal, width, height, 0, format, type, data);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, filter);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, filter === gl.NEAREST ? gl.NEAREST : gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, wrap);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, wrap);
      return t;
    }
    // Float data texture read with texelFetch (no filtering needed or assumed).
    function dataTexture(data, width, height, channels = 1) {
      const fmt = [null, [gl.R32F, gl.RED], [gl.RG32F, gl.RG], [gl.RGB32F, gl.RGB], [gl.RGBA32F, gl.RGBA]][channels];
      gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1);
      return texture2D({ width, height, internal: fmt[0], format: fmt[1], type: gl.FLOAT, data, filter: gl.NEAREST });
    }
    function dataArray(data, width, height, layers) {
      const t = own('deleteTexture', gl.createTexture());
      gl.bindTexture(gl.TEXTURE_2D_ARRAY, t);
      gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1);
      gl.texImage3D(gl.TEXTURE_2D_ARRAY, 0, gl.R32F, width, height, layers, 0, gl.RED, gl.FLOAT, data);
      for (const k of [gl.TEXTURE_MIN_FILTER, gl.TEXTURE_MAG_FILTER])
        gl.texParameteri(gl.TEXTURE_2D_ARRAY, k, gl.NEAREST);
      for (const k of [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T])
        gl.texParameteri(gl.TEXTURE_2D_ARRAY, k, gl.CLAMP_TO_EDGE);
      return t;
    }
    // Albedo image in sRGB space with mipmaps and anisotropic filtering; resolves when uploaded.
    const images = [];
    function imageTexture(url, { wrap = gl.REPEAT, srgb = true } = {}) {
      const t = own('deleteTexture', gl.createTexture());
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
        new Uint8Array([128, 120, 112, 255]),
      );
      const entry = { texture: t, ready: false };
      entry.promise = new Promise(resolve => {
        const im = new Image();
        images.push(im);
        im.decoding = 'async';
        im.onload = () => {
          if (disposed) return resolve(entry);
          gl.bindTexture(gl.TEXTURE_2D, t);
          gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
          gl.texImage2D(gl.TEXTURE_2D, 0, srgb ? gl.SRGB8_ALPHA8 : gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE, im);
          gl.generateMipmap(gl.TEXTURE_2D);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, wrap);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, wrap === gl.REPEAT ? gl.REPEAT : gl.CLAMP_TO_EDGE);
          if (anisotropy)
            gl.texParameterf(
              gl.TEXTURE_2D,
              anisotropy.TEXTURE_MAX_ANISOTROPY_EXT,
              gl.getParameter(anisotropy.MAX_TEXTURE_MAX_ANISOTROPY_EXT),
            );
          entry.ready = true;
          invalidate();
          resolve(entry);
        };
        im.onerror = () => resolve(entry);
        im.src = url;
      });
      return entry;
    }
    // Indexed triangle mesh (32-bit indices) with positions, normals and optional extra attribute.
    function mesh({ positions, normals, indices, extra = null, extraSize = 0 }) {
      const vao = own('deleteVertexArray', gl.createVertexArray());
      gl.bindVertexArray(vao);
      const attribute = (loc, data, size) => {
        const b = own('deleteBuffer', gl.createBuffer());
        gl.bindBuffer(gl.ARRAY_BUFFER, b);
        gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
        gl.enableVertexAttribArray(loc);
        gl.vertexAttribPointer(loc, size, gl.FLOAT, false, 0, 0);
      };
      attribute(0, positions, 3);
      attribute(1, normals, 3);
      if (extra) attribute(2, extra, extraSize);
      const ib = own('deleteBuffer', gl.createBuffer());
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib);
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);
      gl.bindVertexArray(null);
      return {
        vao,
        count: indices.length,
        draw() {
          gl.bindVertexArray(vao);
          gl.drawElements(gl.TRIANGLES, this.count, gl.UNSIGNED_INT, 0);
          gl.bindVertexArray(null);
        },
      };
    }
    const emptyVAO = own('deleteVertexArray', gl.createVertexArray());
    // Points without attributes: every property derives from gl_VertexID in the shader.
    function points(count, first = 0) {
      gl.bindVertexArray(emptyVAO);
      gl.drawArrays(gl.POINTS, first, count);
      gl.bindVertexArray(null);
    }
    function fullscreen() {
      gl.bindVertexArray(emptyVAO);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.bindVertexArray(null);
    }
    // Four vertices as a strip: billboards built in the vertex shader from gl_VertexID.
    function fullscreenQuad() {
      gl.bindVertexArray(emptyVAO);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      gl.bindVertexArray(null);
    }
    // Shadow map: depth texture rendered from the light, compared in hardware.
    function shadowMap(size = 2048) {
      const depth = texture2D({
        width: size,
        height: size,
        internal: gl.DEPTH_COMPONENT24,
        format: gl.DEPTH_COMPONENT,
        type: gl.UNSIGNED_INT,
        filter: gl.LINEAR,
      });
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_COMPARE_MODE, gl.COMPARE_REF_TO_TEXTURE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_COMPARE_FUNC, gl.LEQUAL);
      const fb = own('deleteFramebuffer', gl.createFramebuffer());
      gl.bindFramebuffer(gl.FRAMEBUFFER, fb);
      gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.TEXTURE_2D, depth, 0);
      gl.drawBuffers([gl.NONE]);
      gl.readBuffer(gl.NONE);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      return { depth, fb, size };
    }

    // ------------------------------------------------------------ sky of the atlas
    // The 52,000 stars and the volumetric nebulae of GeoUniverse, drawn into the HDR target or a cube map.
    let environment = null;
    function sky(frame, strength = 1) {
      if (!root.GeoUniverse) return;
      environment ||= root.GeoUniverse.create(gl);
      gl.bindVertexArray(null);
      environment.draw(frame.camera, frame.width, frame.height, strength, frame.output);
      gl.bindFramebuffer(gl.FRAMEBUFFER, frame.output);
      gl.viewport(0, 0, frame.width, frame.height);
      gl.disable(gl.BLEND);
    }
    // Cube map of the same sky, seen from the origin: the black-hole scene deflects its rays and samples it.
    function skyCube(size = 1024, strength = 1) {
      const cube = own('deleteTexture', gl.createTexture());
      gl.bindTexture(gl.TEXTURE_CUBE_MAP, cube);
      for (let f = 0; f < 6; f++)
        gl.texImage2D(gl.TEXTURE_CUBE_MAP_POSITIVE_X + f, 0, hdrInternal, size, size, 0, gl.RGBA, hdrType, null);
      gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      for (const k of [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T, gl.TEXTURE_WRAP_R])
        gl.texParameteri(gl.TEXTURE_CUBE_MAP, k, gl.CLAMP_TO_EDGE);
      if (!root.GeoUniverse) return cube;
      environment ||= root.GeoUniverse.create(gl);
      const faces = [
        [
          [1, 0, 0],
          [0, -1, 0],
        ],
        [
          [-1, 0, 0],
          [0, -1, 0],
        ],
        [
          [0, 1, 0],
          [0, 0, 1],
        ],
        [
          [0, -1, 0],
          [0, 0, -1],
        ],
        [
          [0, 0, 1],
          [0, -1, 0],
        ],
        [
          [0, 0, -1],
          [0, -1, 0],
        ],
      ];
      const fb = gl.createFramebuffer();
      gl.bindVertexArray(null);
      faces.forEach(([dir, upv], f) => {
        gl.bindFramebuffer(gl.FRAMEBUFFER, fb);
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_CUBE_MAP_POSITIVE_X + f, cube, 0);
        gl.viewport(0, 0, size, size);
        gl.clearColor(0, 0, 0, 1);
        gl.clear(gl.COLOR_BUFFER_BIT);
        const camera = cameraMatrices([0, 0, 0], dir, upv, 1, Math.PI / 2, 0.1, 100);
        environment.draw(camera, size, size, strength, fb);
      });
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.deleteFramebuffer(fb);
      gl.disable(gl.BLEND);
      return cube;
    }

    // ------------------------------------------------------------ HDR target and bloom
    const down = program(FULLSCREEN, DOWN, 'bloom-down'),
      up = program(FULLSCREEN, UP, 'bloom-up'),
      final = program(FULLSCREEN, FINAL, 'tonemap');
    const { hdrInternal, hdrType, samples } = formats(gl, floatTarget, tier);
    let target = null;
    function freeTarget() {
      if (!target) return;
      for (const t of target.textures) gl.deleteTexture(t);
      for (const f of target.framebuffers) gl.deleteFramebuffer(f);
      for (const r of target.renderbuffers) gl.deleteRenderbuffer(r);
      target = null;
    }
    function colorTexture(w, h) {
      const t = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, hdrInternal, w, h, 0, gl.RGBA, hdrType, null);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      return t;
    }
    function buildTarget(w, h) {
      freeTarget();
      target = { w, h, textures: [], framebuffers: [], renderbuffers: [], mips: [] };
      const color = colorTexture(w, h),
        resolve = gl.createFramebuffer(),
        depthRB = gl.createRenderbuffer();
      target.textures.push(color);
      target.framebuffers.push(resolve);
      target.renderbuffers.push(depthRB);
      gl.bindFramebuffer(gl.FRAMEBUFFER, resolve);
      gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, color, 0);
      gl.bindRenderbuffer(gl.RENDERBUFFER, depthRB);
      gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT24, w, h);
      gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, depthRB);
      target.color = color;
      target.resolve = resolve;
      target.scene = resolve;
      if (samples) {
        const ms = gl.createFramebuffer(),
          msColor = gl.createRenderbuffer(),
          msDepth = gl.createRenderbuffer();
        target.framebuffers.push(ms);
        target.renderbuffers.push(msColor, msDepth);
        gl.bindFramebuffer(gl.FRAMEBUFFER, ms);
        gl.bindRenderbuffer(gl.RENDERBUFFER, msColor);
        gl.renderbufferStorageMultisample(gl.RENDERBUFFER, samples, hdrInternal, w, h);
        gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.RENDERBUFFER, msColor);
        gl.bindRenderbuffer(gl.RENDERBUFFER, msDepth);
        gl.renderbufferStorageMultisample(gl.RENDERBUFFER, samples, gl.DEPTH_COMPONENT24, w, h);
        gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, msDepth);
        if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) === gl.FRAMEBUFFER_COMPLETE) target.scene = ms;
      }
      let mw = w,
        mh = h;
      for (let i = 0; i < 7 && mw > 8 && mh > 8; i++) {
        mw = Math.max(1, mw >> 1);
        mh = Math.max(1, mh >> 1);
        const t = colorTexture(mw, mh),
          fb = gl.createFramebuffer();
        gl.bindFramebuffer(gl.FRAMEBUFFER, fb);
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
        target.textures.push(t);
        target.framebuffers.push(fb);
        target.mips.push({ t, fb, w: mw, h: mh });
      }
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    }
    function bloom() {
      gl.disable(gl.DEPTH_TEST);
      gl.disable(gl.BLEND);
      gl.useProgram(down);
      let source = target.color,
        sw = target.w,
        sh = target.h;
      target.mips.forEach((m, i) => {
        gl.bindFramebuffer(gl.FRAMEBUFFER, m.fb);
        gl.viewport(0, 0, m.w, m.h);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, source);
        set(down, 'uSource', 0, 'int');
        set(down, 'uTexel', [1 / sw, 1 / sh]);
        set(down, 'uKaris', i === 0 ? 1 : 0);
        fullscreen();
        source = m.t;
        sw = m.w;
        sh = m.h;
      });
      gl.useProgram(up);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE);
      for (let i = target.mips.length - 1; i > 0; i--) {
        const from = target.mips[i],
          to = target.mips[i - 1];
        gl.bindFramebuffer(gl.FRAMEBUFFER, to.fb);
        gl.viewport(0, 0, to.w, to.h);
        gl.bindTexture(gl.TEXTURE_2D, from.t);
        set(up, 'uSource', 0, 'int');
        set(up, 'uTexel', [1 / from.w, 1 / from.h]);
        set(up, 'uRadius', 1);
        fullscreen();
      }
      gl.disable(gl.BLEND);
    }

    // ------------------------------------------------------------ camera and controls
    const cam = cameraState(options);
    const home = { ...cam, target: cam.target.slice() };
    const initial = settings(options, tier);
    let width = 1,
      height = 1,
      pixelRatio = 1,
      raf = 0,
      last = 0,
      time = initial.time,
      disposed = false,
      visible = true,
      scale = initial.scale,
      exposure = initial.exposure,
      bloomStrength = initial.bloom,
      scene = null,
      frames = 0;
    const reduced = root.matchMedia?.('(prefers-reduced-motion: reduce)');
    const paused = () => Boolean(root.GeoSpace?.debug().paused ?? reduced?.matches);
    const slowFrames = root.GeoCore?.frameWatch?.(55, 10) || (() => false);
    function invalidate() {
      if (!disposed && !raf) raf = requestAnimationFrame(tick);
    }
    function resize() {
      const r = chart.getBoundingClientRect();
      width = Math.max(1, r.width);
      height = Math.max(1, r.height);
      pixelRatio = Math.min(root.devicePixelRatio || 1, tier === 'high' ? 2 : 1.5) * scale;
      const w = Math.max(1, Math.round(width * pixelRatio)),
        h = Math.max(1, Math.round(height * pixelRatio));
      if (canvas.width !== w || canvas.height !== h || !target) {
        canvas.width = w;
        canvas.height = h;
        buildTarget(w, h);
      }
      invalidate();
    }
    function pose(now) {
      let { azimuth, elevation, distance, target: t } = cam;
      if (cam.transition) {
        const tr = cam.transition,
          k = clamp((now - tr.start) / tr.duration, 0, 1),
          e = k * k * (3 - 2 * k);
        const lerp = (a, b) => a + (b - a) * e;
        azimuth = lerp(tr.from.azimuth, cam.azimuth);
        elevation = lerp(tr.from.elevation, cam.elevation);
        distance = Math.exp(lerp(Math.log(tr.from.distance), Math.log(cam.distance)));
        t = tr.from.target.map((v, i) => lerp(v, cam.target[i]));
        if (k === 1) cam.transition = null;
      }
      const eye = [
        t[0] + distance * Math.cos(elevation) * Math.sin(azimuth),
        t[1] + distance * Math.sin(elevation),
        t[2] + distance * Math.cos(elevation) * Math.cos(azimuth),
      ];
      const near = scene?.near?.(distance) ?? distance * 0.002,
        far = scene?.far?.(distance) ?? distance * 60;
      return { ...cameraMatrices(eye, t, [0, 1, 0], width / height, cam.fov, near, far), distance };
    }
    function moveTo(next, duration = 900) {
      cam.transition =
        paused() || reduced?.matches
          ? null
          : {
              start: performance.now(),
              duration,
              from: { ...cam, target: (lastCamera?.target || cam.target).slice() },
            };
      if (lastCamera && cam.transition) {
        cam.transition.from.distance = Math.hypot(...lastCamera.eye.map((v, i) => v - lastCamera.target[i]));
      }
      Object.assign(cam, next);
      if (next.target) cam.target = next.target.slice();
      invalidate();
    }
    function resetCamera() {
      moveTo({ ...home, target: home.target.slice() }, 700);
    }
    const pointers = new Map();
    let drag = null,
      pinch = 0;
    listen(canvas, 'pointerdown', e => {
      pointers.set(e.pointerId, [e.clientX, e.clientY]);
      drag = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY, moved: false };
      canvas.setPointerCapture(e.pointerId);
      if (pointers.size === 2) {
        const q = [...pointers.values()];
        pinch = Math.hypot(q[0][0] - q[1][0], q[0][1] - q[1][1]);
      }
    });
    listen(canvas, 'pointermove', e => {
      if (!pointers.has(e.pointerId)) return;
      const prev = pointers.get(e.pointerId);
      pointers.set(e.pointerId, [e.clientX, e.clientY]);
      cam.transition = null;
      if (pointers.size === 2) {
        const q = [...pointers.values()],
          next = Math.hypot(q[0][0] - q[1][0], q[0][1] - q[1][1]);
        if (pinch > 0) zoom(pinch / Math.max(10, next));
        pinch = next;
      } else {
        cam.azimuth -= (e.clientX - prev[0]) * 0.0055;
        cam.elevation = clamp(cam.elevation + (e.clientY - prev[1]) * 0.0045, cam.minElevation, cam.maxElevation);
      }
      if (drag && Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy) > 5) drag.moved = true;
      invalidate();
    });
    const release = e => {
      pointers.delete(e.pointerId);
      if (!pointers.size) {
        if (drag && !drag.moved && e.type === 'pointerup') {
          const r = canvas.getBoundingClientRect();
          scene?.pick?.(e.clientX - r.left, e.clientY - r.top);
        }
        drag = null;
        pinch = 0;
      }
    };
    listen(canvas, 'pointerup', release);
    listen(canvas, 'pointercancel', release);
    function zoom(factor) {
      cam.transition = null;
      cam.distance = clamp(cam.distance * factor, cam.minDistance, cam.maxDistance);
      invalidate();
    }
    listen(
      canvas,
      'wheel',
      e => {
        e.preventDefault();
        zoom(Math.exp(clamp(e.deltaY, -120, 120) * 0.0016));
      },
      { passive: false },
    );
    listen(canvas, 'keydown', e => {
      const keys = { ArrowLeft: 1, ArrowRight: 1, ArrowUp: 1, ArrowDown: 1, '+': 1, '-': 1, Home: 1 };
      if (!keys[e.key]) return;
      e.preventDefault();
      cam.transition = null;
      if (e.key === 'ArrowLeft') cam.azimuth += 0.12;
      if (e.key === 'ArrowRight') cam.azimuth -= 0.12;
      if (e.key === 'ArrowUp') cam.elevation = clamp(cam.elevation + 0.08, cam.minElevation, cam.maxElevation);
      if (e.key === 'ArrowDown') cam.elevation = clamp(cam.elevation - 0.08, cam.minElevation, cam.maxElevation);
      if (e.key === '+') zoom(0.85);
      if (e.key === '-') zoom(1 / 0.85);
      if (e.key === 'Home') resetCamera();
      invalidate();
    });
    for (const b of chart.querySelectorAll('[data-object-camera]'))
      listen(b, 'click', () => {
        const k = b.dataset.objectCamera;
        if (k === 'reset') resetCamera();
        else zoom(k === 'in' ? 0.8 : 1.25);
      });
    listen(document, 'geospace:pause', () => {
      last = 0;
      invalidate();
    });
    listen(document, 'visibilitychange', () => {
      last = 0;
      invalidate();
    });
    listen(root, 'resize', resize);
    let observer = null;
    if (root.IntersectionObserver) {
      observer = new IntersectionObserver(entries => {
        visible = entries[0].isIntersecting;
        last = 0;
        invalidate();
      });
      observer.observe(chart);
    }
    listen(canvas, 'webglcontextlost', e => {
      e.preventDefault();
      disposed = true;
      chart.dataset.renderer = 'essential';
      chart.classList.remove('scene-ready');
      options.onLost?.();
    });

    // ------------------------------------------------------------ worker
    let worker = null,
      jobs = 0;
    const waiting = new Map();
    function work(task, payload = {}) {
      if (!worker) {
        worker = new Worker(new URL('objects-worker.js', options.base || root.location.href));
        worker.onmessage = ({ data }) => {
          const w = waiting.get(data.id);
          if (!w) return;
          if (data.partial) return w.partial?.(data.result);
          waiting.delete(data.id);
          if (data.error) w.reject(Error(data.error));
          else w.resolve(data.result);
        };
        worker.onerror = e => {
          for (const w of waiting.values()) w.reject(Error(e.message || 'Worker non disponibile'));
          waiting.clear();
        };
      }
      const id = ++jobs;
      return new Promise((resolve, reject) => {
        waiting.set(id, { resolve, reject, partial: payload.onPartial });
        const { onPartial: _onPartial, ...message } = payload;
        worker.postMessage({ id, task, ...message });
      });
    }

    // ------------------------------------------------------------ frame loop
    let lastCamera = null;
    function frameDue() {
      if (disposed || !chart.isConnected || document.hidden || !visible || !target) {
        last = 0;
        return false;
      }
      return true;
    }
    // Multisampled scene to texture, bloom chain, then tone mapping onto the canvas.
    function present(frame) {
      if (target.scene !== target.resolve) {
        gl.bindFramebuffer(gl.READ_FRAMEBUFFER, target.scene);
        gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, target.resolve);
        gl.blitFramebuffer(0, 0, target.w, target.h, 0, 0, target.w, target.h, gl.COLOR_BUFFER_BIT, gl.NEAREST);
      }
      bloom();
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.useProgram(final);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, target.color);
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, target.mips[0]?.t || target.color);
      set(final, 'uScene', 0, 'int');
      set(final, 'uBloom', 1, 'int');
      set(final, 'uExposure', exposure * (scene?.exposure?.() ?? 1));
      set(final, 'uBloomStrength', bloomStrength);
      set(final, 'uSeed', (frames++ % 64) * 0.37);
      fullscreen();
      scene?.overlay?.(frame);
    }
    // Interval since the previous frame (s); slow frames reduce the scene unless the tier is fixed.
    function watch(now) {
      const dt = last ? Math.min(0.1, (now - last) / 1000) : 0;
      if (!fixed && last && slowFrames(now - last) && scene?.reduce?.()) chart.dataset.reduced = 'true';
      last = now;
      return dt;
    }
    function tick(now) {
      raf = 0;
      if (!frameDue()) return;
      const dt = watch(now);
      const moving = !paused();
      if (moving) time += dt;
      const camera = pose(now);
      lastCamera = camera;
      const frame = {
        gl,
        time,
        dt: moving ? dt : 0,
        camera,
        width: target.w,
        height: target.h,
        pixelRatio,
        tier,
        output: target.scene,
      };
      gl.bindFramebuffer(gl.FRAMEBUFFER, target.scene);
      gl.viewport(0, 0, target.w, target.h);
      gl.clearColor(0, 0, 0, 1);
      gl.clearDepth(1);
      gl.depthMask(true);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      scene?.draw(frame);
      gl.bindVertexArray(null);
      present(frame);
      if (moving || cam.transition || scene?.busy?.()) raf = requestAnimationFrame(tick);
      else last = 0;
    }
    function dispose() {
      disposed = true;
      cancelAnimationFrame(raf);
      observer?.disconnect();
      listeners.forEach(f => f());
      worker?.terminate();
      waiting.clear();
      for (const im of images) {
        im.onload = null;
        im.onerror = null;
      }
      try {
        scene?.dispose?.();
      } catch {
        /* the scene keeps no resource outside the engine */
      }
      freeTarget();
      environment?.dispose();
      for (const [method, obj] of resources) gl[method](obj);
      gl.getExtension('WEBGL_lose_context')?.loseContext();
    }
    resize();
    return {
      gl,
      tier,
      floatTarget,
      program,
      set,
      texture2D,
      dataTexture,
      dataArray,
      imageTexture,
      mesh,
      points,
      fullscreen,
      fullscreenQuad,
      shadowMap,
      sky,
      skyCube,
      cameraMatrices,
      multiply,
      invert,
      model,
      work,
      invalidate,
      moveTo,
      resetCamera,
      camera: cam,
      setHome(next) {
        Object.assign(home, next);
        if (next.target) home.target = next.target.slice();
      },
      lastCamera: () => lastCamera,
      setScene(s) {
        scene = s;
        invalidate();
      },
      setExposure(v) {
        exposure = v;
        invalidate();
      },
      setBloom(v) {
        bloomStrength = v;
        invalidate();
      },
      reduceResolution() {
        if (scale <= 0.5) return false;
        scale = Math.max(0.5, scale * 0.8);
        resize();
        return true;
      },
      project(p, camera = lastCamera) {
        if (!camera) return null;
        const m = camera.vp,
          x = m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
          y = m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
          w = m[3] * p[0] + m[7] * p[1] + m[11] * p[2] + m[15];
        return { x: ((x / w + 1) * width) / 2, y: ((1 - y / w) * height) / 2, depth: w, visible: w > 0 };
      },
      time: () => time,
      debug: () => ({ tier, floatTarget, samples, width: target?.w, height: target?.h, scale, ...scene?.debug?.() }),
      dispose,
      TAU,
    };
  }
  root.GeoObjectEngine = Object.freeze({ create, cameraMatrices, multiply, invert, model, tierOf });
})(globalThis);
