/* HTTP contract required by ES modules and webR; no browser is launched. */
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import http from 'node:http';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const server = spawn(process.execPath, ['scripts/serve.mjs'], {
  env: { ...process.env, HOST: '127.0.0.1', PORT: '0' },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let output = '';
try {
  const base = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(Error('HTTP test server did not start: ' + output)), 10000);
    server.stdout.on('data', data => {
      output += data;
      const found = output.match(/http:\/\/127\.0\.0\.1:\d+\//);
      if (found) {
        clearTimeout(timer);
        resolve(found[0]);
      }
    });
    server.stderr.on('data', data => (output += data));
    server.once('error', err => {
      clearTimeout(timer);
      reject(err);
    });
    server.once('exit', code => {
      clearTimeout(timer);
      reject(Error('HTTP server exited: ' + code + ' ' + output));
    });
  });
  for (const [file, mime] of [
    ['vendor/webr/webr.mjs', 'text/javascript'],
    ['vendor/webr/R.wasm', 'application/wasm'],
    ['assets/lab-engine.js', 'text/javascript'],
  ]) {
    const response = await fetch(base + file, { method: 'HEAD' });
    assert.equal(response.status, 200, file);
    assert.equal(response.headers.get('content-type').split(';')[0], mime, file);
    assert.equal(response.headers.get('x-content-type-options'), 'nosniff');
  }
  const raw = (pathname, options = {}) =>
    new Promise((resolve, reject) => {
      const u = new URL(base);
      const req = http.request(
        {
          hostname: u.hostname,
          port: u.port,
          path: pathname,
          method: options.method || 'GET',
          headers: options.headers || {},
        },
        res => {
          res.resume();
          res.on('end', () => resolve({ status: res.statusCode, headers: res.headers }));
        },
      );
      req.on('error', reject);
      req.end();
    });
  for (const [pathname, status] of [
    ['/../package.json', 403],
    ['/%2e%2e/package.json', 403],
    ['/.git/config', 403],
    ['/assets/%00test', 403],
    ['/%5c../package.json', 403],
    ['/%xx', 400],
    ['//example.invalid/', 400],
  ])
    assert.equal((await raw(pathname)).status, status, pathname);
  assert.equal((await raw('/', { method: 'POST' })).status, 405);
  assert.equal((await raw('/', { headers: { host: 'attacker.invalid' } })).status, 403);
  assert.equal((await raw('/', { headers: { 'sec-fetch-site': 'cross-site' } })).status, 403);
  const worker = await raw('/vendor/webr/webr-worker.js');
  assert(worker.headers['content-security-policy'].includes("'unsafe-eval'"));
  assert(worker.headers['content-security-policy'].includes("connect-src 'self'"));
  const index = await raw('/');
  assert(!index.headers['content-security-policy'].includes(" 'unsafe-eval'"));
  assert.equal(index.status, 200);
  assert.equal(index.headers['x-frame-options'], 'DENY');
  assert.equal(index.headers['referrer-policy'], 'no-referrer');
  assert(index.headers['content-security-policy'].includes("frame-ancestors 'none'"));
  // A symlink inside the served tree must never expose repository files.
  const probe = 'dist/security-link-probe';
  try {
    fs.symlinkSync('../package.json', probe);
    assert.equal((await raw('/security-link-probe')).status, 403);
  } finally {
    fs.rmSync(probe, { force: true });
  }
  const courseIndex = await raw('/materiali/Indice_corso.html');
  assert.equal(courseIndex.status, 200);
  assert(courseIndex.headers['content-security-policy'].includes("'sha256-"));
  for (const file of [
    '/materiali/audit/Registro_slide_R6.html',
    '/materiali/audit/Rapporto_revisione_R6.pdf',
    '/materiali/Rapporto_revisione_R6.pdf',
  ])
    assert.equal((await raw(file)).status, 404, file);
  const missing = await fetch(base + 'missing-script.mjs', { method: 'HEAD' });
  assert.equal(missing.status, 404);
  console.log(
    'HTTP: MIME, security headers, traversal, malformed requests, symlinks, methods and DNS rebinding verified.',
  );
} finally {
  if (server.exitCode === null) {
    const closed = once(server, 'exit');
    server.kill();
    await closed;
  }
}
