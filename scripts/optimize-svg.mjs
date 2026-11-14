// Optional regeneration step: SVGO 4.0.0, eight-decimal coordinates and absolute paths.
// Existing PDFs, fonts and course sources are never changed.
import fs from 'node:fs';
import path from 'node:path';
const { optimize } = await import(process.env.SVGO_MODULE || 'svgo');
const options = {
  floatPrecision: 8,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          cleanupNumericValues: false,
          convertColors: false,
          convertTransform: false,
          convertPathData: {
            floatPrecision: 8,
            applyTransforms: false,
            makeArcs: false,
            straightCurves: false,
            convertToQ: false,
            forceAbsolutePath: true,
          },
          removeDesc: false,
        },
      },
    },
  ],
};
let count = 0,
  before = 0,
  after = 0;
for (const folder of ['assets/slides', 'assets/visuals'])
  for (const group of fs.readdirSync(folder))
    for (const file of fs.readdirSync(path.join(folder, group))) {
      if (!file.endsWith('.svg')) continue;
      const p = path.join(folder, group, file),
        source = fs.readFileSync(
          process.env.SVG_SOURCE_ROOT ? path.join(process.env.SVG_SOURCE_ROOT, p.replace(/^assets\//, '')) : p,
          'utf8',
        ),
        result = optimize(source, { ...options, path: p });
      before += Buffer.byteLength(source);
      after += Buffer.byteLength(result.data);
      fs.writeFileSync(p, result.data);
      count++;
      if (count % 100 === 0) console.log(count + ' SVG');
    }
console.log(JSON.stringify({ count, before, after, saved: before - after }));
