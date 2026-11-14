/* Recreate exactly one public teaching fixture intentionally excluded by its
   own .gitignore. Never load secrets or overwrite a different existing file. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const relative = 'risultati/R/M15_N17/repo_ignore/.env';
const target = path.join('materiali', relative);
const contents = Buffer.from('SEGNAPOSTO_NON_SEGRETO\n', 'utf8');
const manifest = fs
  .readFileSync('materiali/MANIFEST_SHA256.txt', 'utf8')
  .split('\n')
  .find(line => line.endsWith('  ' + relative));
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
if (!manifest || sha(contents) !== manifest.split('  ')[0])
  throw Error('Teaching fixture does not match the original course manifest.');
if (fs.existsSync(target)) {
  if (fs.lstatSync(target).isSymbolicLink() || sha(fs.readFileSync(target)) !== sha(contents))
    throw Error('Unexpected teaching fixture; inspect it without replacing its contents.');
} else {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, contents, { flag: 'wx' });
}
