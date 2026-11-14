// Loads front-end sources into a vm context or a jsdom window under their file URL, so that
// `npm run coverage` attributes executed lines to src/*.js.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export function load(target, ...names) {
  for (const name of names) {
    const file = path.join(root, 'src', name + '.js');
    const code = fs.readFileSync(file, 'utf8'),
      url = pathToFileURL(file).href;
    if (typeof target.eval === 'function' && target.document) target.eval(code + '\n//# sourceURL=' + url);
    else vm.runInContext(code, vm.isContext(target) ? target : vm.createContext(target), { filename: url });
  }
  return target;
}
