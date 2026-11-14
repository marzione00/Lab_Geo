import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { csp, securityHeaders, workerCsp } from './security-policy.mjs';
export function hardenBuild(out) {
  const hash = file =>
    'sha384-' +
    crypto
      .createHash('sha384')
      .update(fs.readFileSync(path.join(out, file)))
      .digest('base64');
  const dynamic = [
    'vendor/mathjax/tex-svg.js',
    'assets/experiments-details.js',
    'assets/solution-data.js',
    'assets/briefing.js',
    'assets/briefing.css',
    'assets/audio.js',
    ...fs.readdirSync(path.join(out, 'assets/content')).map(f => 'assets/content/' + f),
  ];
  fs.writeFileSync(
    path.join(out, 'assets/integrity.js'),
    'window.GEO_INTEGRITY=' + JSON.stringify(Object.fromEntries(dynamic.map(f => [f, hash(f)]))) + ';\n',
  );
  let html = fs.readFileSync(path.join(out, 'index.html'), 'utf8').replace('{{CSP}}', csp);
  html = html.replace(/<(script|link)\b[^>]*>/g, tag => {
    const match = tag.match(/(?:src|href)="([^"#]+)"/);
    if (!match || !/^(assets|vendor)\//.test(match[1]) || !/\.(js|css)$/.test(match[1])) return tag;
    return tag.replace(/>$/, ' integrity="' + hash(match[1]) + '" crossorigin="anonymous">');
  });
  fs.writeFileSync(path.join(out, 'index.html'), html);
  // Preserve the original HTML sources and filters; add CSP to derived pages.
  const htmlPolicies = {};
  const visit = dir => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) visit(file);
      else if (entry.name.endsWith('.html')) {
        const relative = path.relative(out, file).split(path.sep).join('/');
        if (relative === 'index.html') continue;
        let source = fs.readFileSync(file, 'utf8');
        const hashes = [...source.matchAll(/<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(
          m => "'sha256-" + crypto.createHash('sha256').update(m[1]).digest('base64') + "'",
        );
        const policy = csp
          .replace("; require-trusted-types-for 'script'", '')
          .replace(
            "script-src 'self' 'wasm-unsafe-eval'",
            "script-src 'self'" + (hashes.length ? ' ' + hashes.join(' ') : ''),
          );
        const meta =
          '<meta http-equiv="Content-Security-Policy" content="' +
          policy +
          '"><meta name="referrer" content="no-referrer">';
        source = source.replace(/(<meta\b[^>]*charset[^>]*>)/i, '$1' + meta);
        fs.writeFileSync(file, source);
        htmlPolicies[relative] = policy;
      }
    }
  };
  visit(path.join(out, 'materiali'));
  visit(path.join(out, 'percorso'));
  const headers = { ...securityHeaders, 'Strict-Transport-Security': 'max-age=31536000' };
  delete headers['Content-Security-Policy'];
  fs.writeFileSync(
    path.join(out, '_headers'),
    '/*\n' +
      Object.entries(headers)
        .map(([k, v]) => '  ' + k + ': ' + v)
        .join('\n') +
      '\n/\n  Content-Security-Policy: ' +
      csp +
      "; frame-ancestors 'none'\n/index.html\n  Content-Security-Policy: " +
      csp +
      "; frame-ancestors 'none'\n/vendor/webr/*\n  Content-Security-Policy: " +
      workerCsp +
      '\n' +
      Object.entries(htmlPolicies)
        .map(([file, policy]) => '/' + file + '\n  Content-Security-Policy: ' + policy + "; frame-ancestors 'none'")
        .join('\n') +
      '\n',
  );
}
