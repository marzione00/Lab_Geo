/* Repository guardrails. This is not a CVE scanner or a penetration test. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const walk = dir => fs.readdirSync(dir, {withFileTypes:true}).flatMap(d => {
 const p = path.join(dir,d.name); assert(!d.isSymbolicLink(), 'Symbolic link not allowed: '+p);
 return d.isDirectory() ? walk(p) : [p];
});
const inventory = JSON.parse(fs.readFileSync('security/vendor-integrity.json')).files;
assert.deepEqual(walk('vendor').sort(), inventory.map(f=>f.path).sort(), 'Vendor inventory changed; review the update.');
for (const f of inventory) assert.equal(sha(f.path), f.sha256, 'Vendor checksum: '+f.path);
const upstream = JSON.parse(fs.readFileSync('vendor/webr-provenance.json'));
for (const f of upstream.files) assert.equal(sha('vendor/webr/'+f.file), f.sha256, 'Upstream webR checksum: '+f.file);
for (const p of JSON.parse(fs.readFileSync('vendor/r-packages-lock.json'))) assert.equal(sha('vendor/r-repo/bin/emscripten/contrib/4.6/'+p.file),p.sha256,'R package checksum: '+p.package);
for (const f of walk('.github/workflows')) {
 const s = fs.readFileSync(f,'utf8');
 assert(!/pull_request_target|write-all|continue-on-error\s*:\s*true/.test(s), 'Unsafe workflow: '+f);
 for (const m of s.matchAll(/uses:\s*([^\s#]+)/g)) assert(/^[\w./-]+@[a-f0-9]{40}$/.test(m[1]),'Action must use full commit SHA: '+m[1]);
 assert(s.includes('persist-credentials: false'), 'Checkout credentials must not persist.');
 assert(!/runs-on:\s*ubuntu-latest/.test(s), 'Runner must be pinned.');
}
const index = fs.readFileSync('dist/index.html','utf8');
assert(index.includes("script-src-attr 'none'")); assert(index.includes("base-uri 'none'")); assert(index.includes("form-action 'none'"));
assert(!index.includes(" 'unsafe-eval'")); assert(!/script-src[^;]*'unsafe-inline'/.test(index));
for (const tag of index.match(/<(?:script|link)\b[^>]*>/g) || []) {
 const file = tag.match(/(?:src|href)="([^"]+\.(?:js|css))"/); if (!file) continue;
 const integrity = tag.match(/integrity="sha384-([^"]+)"/); assert(integrity, 'Missing SRI: '+file[1]);
 assert.equal(integrity[1],crypto.createHash('sha384').update(fs.readFileSync('dist/'+file[1])).digest('base64'));
}
const lock=JSON.parse(fs.readFileSync('package-lock.json'));
for(const [name,p] of Object.entries(lock.packages)) if(name){assert(p.integrity&&p.resolved,'Unlocked npm dependency: '+name);assert.equal(new URL(p.resolved).origin,'https://registry.npmjs.org','Unexpected registry');}
const secretPatterns = [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, /gh[pousr]_[A-Za-z0-9]{36,}/, /github_pat_[A-Za-z0-9_]{60,}/, /AKIA[A-Z0-9]{16}/, /sk-(?:proj-)?[A-Za-z0-9_-]{40,}/];
const roots=['src','config','scripts','tests','docs','.github','content','R','moduli'];
let scanned=0;
for(const file of roots.flatMap(walk).filter(f=>/\.(?:[cm]?js|json|html|md|ya?ml|R|py|txt|css)$/.test(f))){const text=fs.readFileSync(file,'utf8');for(const p of secretPatterns)assert(!p.test(text),'Potential secret in '+file);scanned++;}
const report={date:new Date().toISOString(),status:'passed',vendorFiles:inventory.length,upstreamWebR:upstream.files.length,rPackages:JSON.parse(fs.readFileSync('vendor/r-packages-lock.json')).length,sourceFilesScanned:scanned,checks:['vendor-sha256','upstream-sha256','workflow-pins','least-privilege-guardrails','CSP','SRI','npm-lock-integrity','secret-patterns'],limits:'Pattern matching is not exhaustive. CVE scanning of npm is separate; R/WASM and browser security require upstream monitoring. GitHub-hosted workflows are not executed by this command.'};
fs.writeFileSync('qa/security.json',JSON.stringify(report,null,2)+'\n');
console.log('Security guardrails passed: '+inventory.length+' vendored files, CSP/SRI, workflow pins and '+scanned+' source files.');
