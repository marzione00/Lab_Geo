import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

// Every text tone of the design tokens must reach WCAG AA (4.5:1) on every surface placed behind text.
const root = fs.readFileSync(new URL('../src/space.css', import.meta.url), 'utf8').match(/:root \{([\s\S]*?)\n\}/)[1];
const tokens = Object.fromEntries([...root.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m => [m[1], m[2].trim()]));
const resolve = name => {
  let v = tokens[name];
  for (let i = 0; i < 5 && v?.startsWith('var('); i++) v = tokens[v.slice(6, -1)];
  return v;
};
const rgba = hex => {
  const h = hex.slice(1);
  const n = [0, 2, 4, 6].map(i => (h.length >= i + 2 ? parseInt(h.slice(i, i + 2), 16) : 255));
  return { rgb: n.slice(0, 3), a: n[3] / 255 };
};
const over = (top, bottom) => top.rgb.map((c, i) => c * top.a + bottom[i] * (1 - top.a));
const luminance = rgb =>
  rgb
    .map(c => c / 255)
    .map(c => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4))
    .reduce((s, c, i) => s + c * [0.2126, 0.7152, 0.0722][i], 0);
const ratio = (a, b) => {
  const [x, y] = [luminance(a), luminance(b)].sort((p, q) => q - p);
  return (x + 0.05) / (y + 0.05);
};

const TEXT = [
  'ink-bright',
  'ink',
  'ink-soft',
  'muted',
  'teal',
  'gold-dim',
  'gold',
  'gold-pale',
  'alert',
  'action',
  'info',
];
const bg = rgba(resolve('bg')).rgb;
const SURFACES = {
  bg,
  surface: over(rgba(resolve('surface')), bg),
  'surface-raised': rgba(resolve('surface-raised')).rgb,
};

test('Toni del testo leggibili su ogni superficie (WCAG AA 4,5:1)', () => {
  for (const t of TEXT) {
    const value = resolve(t);
    assert.match(value ?? '', /^#[0-9a-f]{6}$/i, `token --${t} must resolve to an opaque colour`);
    for (const [name, surface] of Object.entries(SURFACES)) {
      const r = ratio(rgba(value).rgb, surface);
      assert.ok(r >= 4.5, `--${t} on --${name}: ${r.toFixed(2)}:1`);
    }
  }
});

test('Scala tipografica: sette gradini, il primo almeno 12 px', () => {
  const steps = Object.keys(tokens).filter(k => /^fs-\d$/.test(k));
  assert.equal(steps.length, 7);
  assert.equal(tokens['fs-1'], '0.75rem');
  const css = fs
    .readdirSync(new URL('../src/', import.meta.url))
    .filter(f => f.endsWith('.css'))
    .map(f => fs.readFileSync(new URL('../src/' + f, import.meta.url), 'utf8'))
    .join('\n');
  // No font size in pixels: sizes come from the scale (decorative glyphs use rem).
  assert.deepEqual(css.match(/font-size:\s*[\d.]+px/g) ?? [], []);
  assert.deepEqual(css.match(/font:\s*(?:[\w-]+\s+)*[\d.]+px/g) ?? [], []);
});
