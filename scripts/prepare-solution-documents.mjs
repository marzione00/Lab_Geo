import fs from 'node:fs';
import vm from 'node:vm';
import { pathToFileURL } from 'node:url';
const scope = {};
vm.runInNewContext(fs.readFileSync('src/html.js', 'utf8'), scope);
vm.runInNewContext(fs.readFileSync('src/solution-terminal.js', 'utf8'), scope);
export function solutionDocument(a, g) {
  const bodyBlocks = a.code.trim().split(/\n\s*\n/);
  const indices = g.stages.flatMap(s => s.blocks);
  if (indices.length !== bodyBlocks.length || indices.some((n, i) => n !== i))
    throw Error('Incomplete solution: ' + a.id);
  const text = [
    a.title,
    'GeoStat Lab · Marzio De Corato',
    '',
    g.introduction,
    '',
    'SUGGERIMENTI',
    ...g.hints.map((s, i) => i + 1 + '. ' + s),
    '',
    'SOLUZIONE GUIDATA',
    ...g.stages.flatMap((s, i) => [
      i + 1 + '. ' + s.title,
      s.explanation,
      '',
      scope.GeoSolutions.stageCode(a, g, i),
      '',
      s.observe,
      '',
    ]),
    'INTERPRETAZIONE',
    ...g.interpretation,
    '',
    ...g.alternatives,
    '',
    'LIMITI E CONTROLLI',
    ...g.pitfalls,
  ].join('\n\n');
  return text + '\n';
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const guides = JSON.parse(fs.readFileSync('content/solution-guides-research.json'));
  const cases = [];
  for (const [id, g] of Object.entries(guides)) {
    const a = JSON.parse(fs.readFileSync('content/research-' + id + '.json'));
    fs.writeFileSync('assets/research/' + id + '/SOLUZIONE.txt', solutionDocument(a, g));
    cases.push({
      id,
      parameters: Object.fromEntries(a.controls.map(c => [c.key, c.value])),
      programs: g.stages.map((s, i) => scope.GeoSolutions.partialProgram(a, g, i)),
    });
  }
  if (process.argv[2]) fs.writeFileSync(process.argv[2], JSON.stringify(cases));
  console.log('Five downloadable worked solutions prepared.');
}
