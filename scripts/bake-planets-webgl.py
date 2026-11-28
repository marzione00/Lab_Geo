"""Bake procedural albedo textures with WebGL in headless Chromium (Playwright, Pillow, numpy).

Same shader and output as scripts/bake-planets.py, for machines without an EGL context for moderngl: the albedo
program is built from src/planet.frag exactly as there and rendered at 2048x1024 by WebGL 1. Only the planets
named on the command line are written, so the committed textures of the other worlds stay untouched.

Uso: python3 -I scripts/bake-planets-webgl.py M17 [M18 ...]
Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
data = json.loads(subprocess.check_output(['node', '--input-type=module', '-e', "await import('./src/planets.js');"
                                           "console.log(JSON.stringify(Object.values(globalThis.GeoPlanets.byId)))"],
                                          cwd=root))
original = (root / 'src/planet.frag').read_text()
helpers = original[original.index('const float PI'):original.index('void main()')]
body = original[original.index('   vec3 pos=q*3.3'):original.index('   surface=pow(albedo')]
frag = '''precision highp float;
uniform float uKind,uSeed,uTilt,uAngle,uTime;
uniform vec3 uLand,uDeep,uHigh;
''' + helpers + '''void main(){
vec2 uv=gl_FragCoord.xy/vec2(2048,1024);
float lat=(.5-uv.y)*PI,lon=(.5-uv.x)*2.*PI;
vec3 q=vec3(cos(lat)*cos(lon),sin(lat),cos(lat)*sin(lon)),n=q;
float emission=0.,water=0.,cloudAlpha=0.;
''' + body + '''albedo=mix(albedo,vec3(1.,.31,.035),min(1.,emission));
albedo=mix(albedo,vec3(.88,.94,1.),cloudAlpha);
gl_FragColor=vec4(albedo,1.);
}'''
PAGE = '''<canvas id="c" width="2048" height="1024"></canvas><script>
function bake(frag, u) {
  const gl = document.getElementById('c').getContext('webgl', {preserveDrawingBuffer: true, antialias: false});
  const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o);
    if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw Error(gl.getShaderInfoLog(o)); return o; };
  const p = gl.createProgram();
  gl.attachShader(p, sh(gl.VERTEX_SHADER, 'attribute vec2 a;void main(){gl_Position=vec4(a,0,1);}'));
  gl.attachShader(p, sh(gl.FRAGMENT_SHADER, frag)); gl.linkProgram(p); gl.useProgram(p);
  const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]), gl.STATIC_DRAW);
  const a = gl.getAttribLocation(p, 'a'); gl.enableVertexAttribArray(a); gl.vertexAttribPointer(a, 2, gl.FLOAT, false, 0, 0);
  for (const [k, v] of Object.entries(u)) { const l = gl.getUniformLocation(p, k); if (!l) continue;
    if (Array.isArray(v)) gl.uniform3fv(l, v); else gl.uniform1f(l, v); }
  gl.viewport(0, 0, 2048, 1024); gl.drawArrays(gl.TRIANGLES, 0, 6);
  const px = new Uint8Array(2048 * 1024 * 4); gl.readPixels(0, 0, 2048, 1024, gl.RGBA, gl.UNSIGNED_BYTE, px);
  let s = ''; for (let i = 0; i < px.length; i += 32768) s += String.fromCharCode.apply(null, px.subarray(i, i + 32768));
  return btoa(s);
}
</script>'''


def rgb(s):
    return [int(s[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def main(ids):
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        page = b.new_page()
        page.set_content(PAGE)
        for p in data:
            if p['id'] not in ids:
                continue
            u = {'uKind': p['kind'], 'uSeed': p['seed'], 'uTilt': p['tilt'], 'uAngle': 0, 'uTime': 0,
                 'uLand': rgb(p['land']), 'uDeep': rgb(p['deep']), 'uHigh': rgb(p['high'])}
            raw = base64.b64decode(page.evaluate('([f, u]) => bake(f, u)', [frag, u]))
            rgba = np.frombuffer(raw, dtype=np.uint8).reshape(1024, 2048, 4)
            # readPixels parte dalla riga inferiore, come fbo.read di moderngl in bake-planets.py.
            im = Image.fromarray(np.ascontiguousarray(rgba[:, :, :3]), 'RGB')
            im.save(root / 'assets/space' / ('p-' + p['id'] + '.webp'), quality=87, method=6)
            print('Baked', p['id'])
        b.close()


if __name__ == '__main__':
    main(set(sys.argv[1:]))
