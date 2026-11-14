/* Procedural nebula from the approved preview. Generated once per viewport, off the UI thread. */
'use strict';
let seed = 14783;
function random() {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return seed / 4294967296;
}
// Preserve the preview noise seed after its stellar catalogue.
for (let i = 0; i < 2100 * 6 + 30 * 6 + 12000 * 8; i++) random();
const noiseTable = new Float32Array(256 * 256);
for (let i = 0; i < noiseTable.length; i++) noiseTable[i] = random();
function valueNoise(x, y) {
  const ix = Math.floor(x),
    iy = Math.floor(y),
    fx = x - ix,
    fy = y - iy,
    u = fx * fx * (3 - 2 * fx),
    v = fy * fy * (3 - 2 * fy);
  const a = noiseTable[((iy & 255) << 8) + (ix & 255)],
    b = noiseTable[((iy & 255) << 8) + ((ix + 1) & 255)],
    c = noiseTable[(((iy + 1) & 255) << 8) + (ix & 255)],
    d = noiseTable[(((iy + 1) & 255) << 8) + ((ix + 1) & 255)];
  return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v;
}
function fractal(x, y) {
  let value = 0,
    a = 0.5;
  for (let i = 0; i < 6; i++) {
    value += a * valueNoise(x, y);
    const next = (0.8 * x + 0.6 * y) * 2.03 + 7.9;
    y = (-0.6 * x + 0.8 * y) * 2.03 + 3.2;
    x = next;
    a *= 0.5;
  }
  return value;
}
function smooth(a, b, x) {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
}
function buildCloudTexture(width, height) {
  const cloudAspect = width / height,
    cloudTexture = { width, height };
  const data = new Uint8ClampedArray(width * height * 4);
  for (let y = 0; y < cloudTexture.height; y++)
    for (let x = 0; x < cloudTexture.width; x++) {
      const p = (x / cloudTexture.width - 0.5) * cloudAspect,
        t = 0.5 - y / cloudTexture.height;
      const qx = fractal(p * 2.3 + 8.3, t * 2.3 + 1.7),
        qy = fractal(p * 2.3 + 2.1, t * 2.3 + 9.2);
      const wx = fractal(p * 4.1 + qx * 2.9 + 4.1, t * 4.1 + qy * 2.9 + 7.2),
        wy = fractal(p * 4.1 + qx * 2.9 + 8.2, t * 4.1 + qy * 2.9 + 2.3);
      const n = fractal(p * 7.8 + wx * 3.4, t * 7.8 + wy * 3.4),
        fine = fractal(p * 31 + wx * 6, t * 31 + wy * 6);
      const leftPath = -cloudAspect * 0.39 + 0.14 * Math.sin(t * 5.5 + 1.6) + 0.1 * (qx - 0.5),
        rightPath = cloudAspect * 0.46 + 0.17 * Math.sin(t * 5.2 + 2.6) + 0.1 * (qy - 0.5);
      const cloudWidth = 0.16 + cloudAspect * 0.07;
      const left = Math.exp(-Math.pow((p - leftPath) / cloudWidth, 2)),
        right = Math.exp(-Math.pow((p - rightPath) / cloudWidth, 2)),
        field = Math.min(1, left + right);
      const gas = Math.pow(Math.max(0, n - 0.27) * 2.3, 1.6) * field;
      const lace = Math.pow(Math.max(0, 1 - Math.abs(n - 0.5) * 12), 3) * field;
      const dust = smooth(0.44, 0.68, fractal(p * 6.5 + qx * 3.2 + 14, t * 6.5 + qy * 3.2 + 2));
      const threads = Math.pow(Math.max(0, 1 - Math.abs(fine - 0.52) * 9), 4);
      const warm = smooth(0.28, 0.65, fractal(p * 2.7 + 32, t * 2.7 + 17)) * 0.82;
      const violet = smooth(-0.05, cloudAspect * 0.6, p);
      const cold = [0.1 + violet * 0.16, 0.36 - violet * 0.18, 0.55 - violet * 0.17];
      const hue = cold.map((v, i) => v * (1 - warm) + [0.65, 0.36, 0.17][i] * warm);
      const base = [0.008, 0.014, 0.028],
        light = [0.18, 0.42, 0.53],
        amber = [0.75, 0.49, 0.27];
      const calm = 0.56 + 0.44 * smooth(0.05, 0.38, Math.abs(p) / Math.max(0.7, cloudAspect));
      const k = (y * cloudTexture.width + x) * 4;
      for (let j = 0; j < 3; j++) {
        const filament = light[j] * (1 - warm) + amber[j] * warm;
        const emission = hue[j] * gas * 1.8 + filament * lace * 0.17 + filament * threads * gas * 0.65;
        const color = (base[j] + emission * (1 - dust * 0.93)) * calm;
        data[k + j] = Math.min(255, Math.max(0, color * 255));
      }
      data[k + 3] = 255;
    }
  return data;
}

self.onmessage = ({ data: q }) => {
  if (
    !q ||
    !Number.isInteger(q.width) ||
    !Number.isInteger(q.height) ||
    q.width < 1 ||
    q.height < 1 ||
    q.width > 1600 ||
    q.height > 1200
  )
    return;
  const pixels = buildCloudTexture(q.width, q.height);
  self.postMessage({ id: q.id, width: q.width, height: q.height, pixels: pixels.buffer }, [pixels.buffer]);
};
