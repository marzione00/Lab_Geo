// Lint gate for CI: ESLint and Stylelint must report no errors, Prettier must report no unformatted file,
// and the number of functions above the complexity threshold may only go down (qa/lint-baseline.json).
import fs from 'node:fs';
import { ESLint } from 'eslint';
import stylelint from 'stylelint';
import * as prettier from 'prettier';

const JS = ['src/**/*.js', 'scripts/**/*.mjs', 'tests/**/*.mjs', 'tests/**/*.js', 'tests/**/*.cjs'];
const CSS = ['src/*.css'];
const baseline = JSON.parse(fs.readFileSync('qa/lint-baseline.json', 'utf8'));

const eslintResults = await new ESLint().lintFiles(JS);
const errors = eslintResults.flatMap(r =>
  r.messages.filter(m => m.severity === 2).map(m => `${r.filePath}:${m.line} ${m.ruleId} ${m.message}`),
);
const complex = eslintResults.flatMap(r =>
  r.messages
    .filter(m => m.ruleId === 'complexity')
    .map(m => `${r.filePath.replace(process.cwd() + '/', '')}:${m.line} ${m.message.split(' has a complexity')[0]}`),
);
const otherWarnings = eslintResults.flatMap(r => r.messages.filter(m => m.severity === 1 && m.ruleId !== 'complexity'));

const style = await stylelint.lint({ files: CSS });
const styleProblems = style.results.flatMap(r => r.warnings.map(w => `${r.source}:${w.line} ${w.text}`));

const unformatted = [];
for (const pattern of [...JS, ...CSS]) {
  for (const file of fs.globSync(pattern)) {
    const text = fs.readFileSync(file, 'utf8');
    const options = { ...(await prettier.resolveConfig(file)), filepath: file };
    if (!(await prettier.check(text, options))) unformatted.push(file);
  }
}

const report = {
  complexity: complex.length,
  complexityLimit: baseline.complexity,
  functions: complex,
  errors,
  styleProblems,
  unformatted,
};
fs.writeFileSync('qa/lint.json', JSON.stringify(report, null, 2) + '\n');
const failures = [
  ...errors.map(e => 'ESLint: ' + e),
  ...otherWarnings.map(w => 'ESLint warning: ' + w.ruleId + ' ' + w.message),
  ...styleProblems.map(s => 'Stylelint: ' + s),
  ...unformatted.map(f => 'Prettier: not formatted ' + f),
];
if (complex.length > baseline.complexity)
  failures.push(
    `Complexity: ${complex.length} functions above 15, baseline ${baseline.complexity}. Simplify the new code or split it.`,
  );
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
const note =
  complex.length < baseline.complexity ? ` (baseline ${baseline.complexity}: lower qa/lint-baseline.json)` : '';
console.log(`Lint: ESLint, Stylelint and Prettier clean; ${complex.length} functions above complexity 15${note}.`);
