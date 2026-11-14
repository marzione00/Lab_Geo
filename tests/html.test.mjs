import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { load } from './source.mjs';
const context = vm.createContext({
  location: { href: 'https://geostat.test/#indice', origin: 'https://geostat.test' },
  URL,
});
load(context, 'html');
const H = context.GeoHTML;
test('escape covers the five HTML metacharacters and nullish values', () => {
  assert.equal(
    H.escape(`<a href="x" title='y'>&</a>`),
    '&lt;a href=&quot;x&quot; title=&#39;y&#39;&gt;&amp;&lt;/a&gt;',
  );
  assert.equal(H.escape(null), '');
  assert.equal(H.escape(undefined), '');
  assert.equal(H.escape(0), '0');
});
test('html escapes interpolations unless they are marked raw', () => {
  const name = '<img src=x onerror=alert(1)>';
  assert.equal(H.html`<p>${name}</p>`, '<p>&lt;img src=x onerror=alert(1)&gt;</p>');
  assert.equal(H.html`<p>${H.raw('<b>ok</b>')}</p>`, '<p><b>ok</b></p>');
  assert.equal(H.html`<p>${null}${undefined}${2}</p>`, '<p>2</p>');
});
test('the default policy rejects executable markup and accepts escaped text', () => {
  for (const bad of [
    '<script>x</script>',
    '<img src=x onerror=alert(1)>',
    '<svg><a href="javascript:alert(1)">x</a></svg>',
    '<div  ONCLICK = "x">',
  ])
    assert.throws(() => H.checkedHTML(bad), /executable content/);
  for (const ok of [
    H.escape('<script>alert(1)</script>'),
    '<p>R: fit <- lm(y ~ x, data = d); one = 1</p>',
    '<svg viewBox="0 0 1 1"><path d="M0 0"/></svg>',
    '<a href="#laboratorio/m05-estimandi">x</a>',
  ])
    assert.equal(H.checkedHTML(ok), ok);
});
test('script URLs must stay on the site', () => {
  assert.equal(H.checkedScriptURL('assets/content/M05.js'), 'assets/content/M05.js');
  assert.equal(H.checkedScriptURL('blob:https://geostat.test/123'), 'blob:https://geostat.test/123');
  assert.throws(() => H.checkedScriptURL('https://cdn.example.org/x.js'), /outside the site/);
});
