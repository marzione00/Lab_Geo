import fs from 'node:fs';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';
const projects = fs
  .readdirSync('content')
  .filter(f => /^research-.*\.json$/.test(f))
  .map(f => JSON.parse(fs.readFileSync('content/' + f)));
const scope = { GEO_RESEARCH: projects, GEO_LABS: { common: fs.readFileSync('R/lab-common.R', 'utf8') } };
for (const name of ['html', 'code-terminal', 'research-projects'])
  vm.runInNewContext(fs.readFileSync('src/' + name + '.js', 'utf8'), scope);
for (const p of projects) {
  const path = 'assets/research/' + p.id + '/';
  if (p.code.trimEnd() !== fs.readFileSync(path + 'source.R', 'utf8').trimEnd()) throw Error('Drift R body: ' + p.id);
  const script = scope.GeoResearch.script(p, Object.fromEntries(p.controls.map(c => [c.key, c.value])));
  fs.writeFileSync(path + p.id + '.R', script);
  fs.writeFileSync(
    path + 'README.txt',
    `${p.title}\nGeoStat Lab · Marzio De Corato\n\n1. Estrarre l’intero archivio in una cartella.\n2. Aprire R/RStudio e impostare quella cartella come directory di lavoro.\n3. Installare ggplot2 se necessario: install.packages("ggplot2").\n4. Consultare SOLUZIONE.txt per indizi, spiegazione dei passaggi e interpretazione.\n5. Eseguire ${p.id}.R. Le figure PDF e risultati.csv vengono scritti nella cartella.\n\nLa copia data.csv è il campione effettivamente utilizzato. provenance.json documenta fonti, data di acquisizione, trasformazioni, unità e limiti. I file raw conservano la risposta originale del fornitore. preview.json riporta l’ambiente R nativo e i parametri iniziali verificati.\n\nDomanda: ${p.question}\n\n${p.limitations.join('\n\n')}\n\nIl mondo dell’atlante è immaginario; il dataset contiene osservazioni reali documentate. Il campione non si aggiorna automaticamente.\n`,
  );
  execFileSync('python3', [
    '-c',
    `import pathlib,zipfile\np=pathlib.Path(${JSON.stringify(path)})\nwith zipfile.ZipFile(p/'project.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:\n for f in sorted(p.rglob('*')):\n  if f.is_file() and f.name!='project.zip':\n   info=zipfile.ZipInfo(f.relative_to(p).as_posix(),date_time=(2000,1,1,0,0,0))\n   info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16\n   z.writestr(info,f.read_bytes(),compresslevel=9)\n`,
  ]);
}
console.log('Packaged ' + projects.length + ' observed-data investigations.');
