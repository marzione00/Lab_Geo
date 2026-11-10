import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
const policy = JSON.parse(fs.readFileSync(fileURLToPath(new URL('../config/security.json', import.meta.url)), 'utf8'));
export const csp = policy.csp;
export const securityHeaders = Object.freeze({...policy.headers, 'Content-Security-Policy': csp + "; frame-ancestors 'none'"});

// Emscripten dynamic linking requires JS evaluation inside the dedicated worker.
// This exception never applies to the application document.
export const workerCsp = "default-src 'none'; script-src 'self' 'unsafe-eval' 'wasm-unsafe-eval'; connect-src 'self'; worker-src 'none'; object-src 'none'; base-uri 'none'";
