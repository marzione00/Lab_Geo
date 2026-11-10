/* Development server: read-only, loopback by default; not a public production host. */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {securityHeaders, workerCsp} from './security-policy.mjs';
const root = fs.realpathSync(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist'));
if (!fs.existsSync(path.join(root, 'index.html'))) throw Error('Eseguire prima npm run build.');
const port = Number(process.env.PORT || 4173), host = process.env.HOST || '127.0.0.1';
const types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.wasm':'application/wasm','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.pdf':'application/pdf','.json':'application/json; charset=utf-8','.otf':'font/otf','.woff2':'font/woff2','.R':'text/plain; charset=utf-8','.py':'text/plain; charset=utf-8','.tex':'text/plain; charset=utf-8','.md':'text/plain; charset=utf-8','.csv':'text/csv; charset=utf-8','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.zip':'application/zip','.gz':'application/gzip','.tgz':'application/gzip'};
const inside = target => target.startsWith(root + path.sep) || target === root;
const server = http.createServer((req, res) => {
  for (const [key, value] of Object.entries(securityHeaders)) res.setHeader(key, value);
  res.setHeader('Cache-Control', 'no-cache');
  const fail = (code, text) => {res.writeHead(code, {'Content-Type':'text/plain; charset=utf-8'}); res.end(text);};
  if (!['GET', 'HEAD'].includes(req.method)) {res.setHeader('Allow', 'GET, HEAD'); return fail(405, 'Metodo non consentito');}
  try {
    const actualPort = server.address().port;
    // Reject DNS rebinding against the loopback development server.
    const allowedHosts = new Set([`${host}:${actualPort}`, `127.0.0.1:${actualPort}`, `localhost:${actualPort}`, `[::1]:${actualPort}`]);
    if (!allowedHosts.has(req.headers.host)) return fail(403, 'Host non consentito');
    if (req.headers['sec-fetch-site'] === 'cross-site') return fail(403, 'Richiesta esterna non consentita');
    const raw = req.url.split('?')[0];
    if (!raw.startsWith('/') || raw.startsWith('//') || raw.length > 4096) return fail(400, 'Percorso non valido');
    const pathname = decodeURIComponent(raw);
    const segments = pathname.split('/');
    if(pathname.startsWith('/vendor/webr/'))res.setHeader('Content-Security-Policy',workerCsp);
    if (/[\x00-\x1f\x7f\\]/.test(pathname) || segments.some(s => s.startsWith('.') || s === '..')) return fail(403, 'Percorso non consentito');
    let target = path.resolve(root, '.' + pathname);
    if (!inside(target)) return fail(403, 'Accesso non consentito');
    target = fs.realpathSync(target);
    if (!inside(target)) return fail(403, 'Accesso non consentito');
    if (fs.statSync(target).isDirectory()) target = fs.realpathSync(path.join(target, 'index.html'));
    if (!inside(target) || !fs.statSync(target).isFile()) return fail(404, 'File non trovato');
    if(path.extname(target)==='.html'){
      const meta=fs.readFileSync(target,'utf8').match(/<meta http-equiv="Content-Security-Policy" content="([^"]+)"/i);
      if(meta)res.setHeader('Content-Security-Policy',meta[1]+"; frame-ancestors 'none'");
    }
    const fd = fs.openSync(target, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
    const size = fs.fstatSync(fd).size;
    res.writeHead(200, {'Content-Type':types[path.extname(target)] || 'application/octet-stream', 'Content-Length':size});
    if (req.method === 'HEAD') {fs.closeSync(fd); return res.end();}
    const stream = fs.createReadStream(target, {fd, autoClose:true});
    stream.on('error', () => res.destroy()); res.on('close', () => stream.destroy()); stream.pipe(res);
  } catch (err) {
    if (err instanceof URIError) return fail(400, 'Richiesta non valida');
    if (['ENOENT', 'ENOTDIR'].includes(err.code)) return fail(404, 'File non trovato');
    fail(403, 'Accesso non consentito');
  }
});
server.requestTimeout = 15000; server.headersTimeout = 10000; server.keepAliveTimeout = 5000; server.maxRequestsPerSocket = 100;
server.listen(port, host, () => console.log('GeoStat Lab: http://' + host + ':' + server.address().port + '/'));
