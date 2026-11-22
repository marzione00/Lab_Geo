import test from 'node:test';
import { execFileSync } from 'node:child_process';

test('Gli archivi respingono file mancanti, duplicati, aggiunti o alterati', () => {
  execFileSync(
    'python3',
    [
      '-c',
      `
import runpy, tempfile, zipfile, warnings
from pathlib import Path
check = runpy.run_path('scripts/labs/package-downloads.py')['verify_archive']
expected = {'a.R': b'original', 'LEGGIMI.txt': b'guide'}
with tempfile.TemporaryDirectory() as tmp:
    file = Path(tmp) / 'case.zip'
    cases = [list(expected.items())[:1], list(expected.items()) + [('a.R', b'original')],
             list(expected.items()) + [('extra.R', b'new')], [('a.R', b'changed'), ('LEGGIMI.txt', b'guide')]]
    for members in cases:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(file, 'w') as z:
                for name, data in members: z.writestr(name, data)
        try: check(file, expected)
        except ValueError: pass
        else: raise AssertionError('Invalid archive accepted')
    with zipfile.ZipFile(file, 'w') as z:
        for name, data in expected.items(): z.writestr(name, data)
    assert check(file, expected) == 2
`,
    ],
    { stdio: 'pipe' },
  );
});

test('Il download didattico esclude rapporti e richiami alla lavorazione editoriale', () => {
  execFileSync(
    'python3',
    [
      '-c',
      `
import runpy
archives,_ = runpy.run_path('scripts/labs/package-downloads.py')['payloads']()
members = archives['GeoStatLab_codice_dati.zip']
assert not any('/audit/' in p or 'Rapporto_revisione_R6' in p or 'revisione_R6' in p or 'CONSEGNA_R6' in p for p in members)
for p in ['materiali/LEGGIMI.txt', 'materiali/MANIFEST_SHA256.txt']:
    assert b'audit/' not in members[p] and b'Rapporto_revisione_R6' not in members[p]
# The modules keep their laboratories; slides, sources and figure programs of the earlier edition are gone.
# The programs of the expeditions travel with the R project of each lesson.
assert 'materiali/laboratori/M01/M01_N01.R' in members
assert not any(p.startswith(('materiali/pdf/', 'materiali/sorgenti/', 'materiali/tikz/', 'materiali/estratti/',
                             'materiali/figure/'))
               or p.endswith('_figure.R') or p in ('materiali/Guida_corso_R6.pdf', 'materiali/Indice_corso.html')
               for p in members)
`,
    ],
    { stdio: 'pipe' },
  );
});
