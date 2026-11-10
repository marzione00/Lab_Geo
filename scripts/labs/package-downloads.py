"""Build or verify both public downloads from their canonical sources."""
from pathlib import Path
import csv
import io
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from public_materials import public_path, public_bytes, checksum_manifest
OUT = ROOT / 'assets/downloads'
R6_DIRS = ('R', 'dati', 'documentazione', 'estratti', 'laboratori',
           'laboratori_python', 'sorgenti', 'strumenti', 'tikz')


def payloads():
    catalogue = json.loads((ROOT / 'content/experiments.json').read_text())
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['modulo', 'sezione', 'titolo_sezione', 'funzione', 'esperimenti'])
    for item in catalogue['coverage']:
        writer.writerow([item.get('module'), item.get('section'),
                         item.get('title', item.get('sectionTitle', '')),
                         item['role'], ';'.join(item['activities'])])
    source = [p for directory in R6_DIRS for p in (ROOT / 'materiali' / directory).rglob('*')]
    source += list((ROOT / 'materiali').iterdir())
    r6 = {str(p.relative_to(ROOT)): public_bytes(p.relative_to(ROOT / 'materiali').as_posix()) for p in source
          if p.is_file() and public_path(p.relative_to(ROOT / 'materiali'))
          and p.name != 'MANIFEST_SHA256.txt'}
    r6['materiali/MANIFEST_SHA256.txt'] = checksum_manifest({k.removeprefix('materiali/'): v for k, v in r6.items()})
    files = list((ROOT / 'R').rglob('*.R')) + [ROOT / p for p in (
        'content/experiments.json', 'vendor/r-packages-lock.json',
        'docs/LABORATORI_INTERATTIVI.md', 'scripts/labs/check-r.R',
        'scripts/labs/check-invariants.R')]
    labs = {str(p.relative_to(ROOT)): p.read_bytes() for p in files}
    count = len(catalogue['activities'])
    labs['LEGGIMI.txt'] = (
        f'GeoStat Lab · {count} esperimenti R\n\n'
        'Ogni file in R/experiments è autonomo e include funzioni e parametri.\n'
        'Installare ggplot2 e jsonlite; svglite serve per esportare figure SVG.\n'
        'Eseguire con Rscript R/experiments/NOME.R oppure aprire il file in RStudio.\n'
        'Il browser usa R 4.6.0 e ggplot2 4.0.3; il collaudo nativo usa R 4.5.0 e ggplot2 3.5.1.\n'
        'I dati sono sintetici: generatore, ipotesi e seme sono dichiarati nel codice.\n'
        'Vedere docs/LABORATORI_INTERATTIVI.md per copertura e limiti.\n'
    ).encode()
    return {'GeoStatLab_codice_dati_R6.zip': r6, 'GeoStatLab_esperimenti_R.zip': labs}, stream.getvalue().encode('utf-8-sig')


def verify_archive(file, expected):
    with zipfile.ZipFile(file) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError(f'Duplicate member in {file}')
        if set(names) != set(expected):
            raise ValueError(f'Archive membership differs in {file}: missing={set(expected)-set(names)}, extra={set(names)-set(expected)}')
        for name in names:
            if archive.read(name) != expected[name]:
                raise ValueError(f'Stale archive member: {file} / {name}')
    return len(expected)


def main():
    archives, csv_bytes = payloads()
    if sys.argv[1:] == ['--check']:
        count = sum(verify_archive(OUT / name, members) for name, members in archives.items())
        if (OUT / 'GeoStatLab_mappa_esperimenti.csv').read_bytes() != csv_bytes:
            raise ValueError('Stale section/experiment CSV')
        print(json.dumps({'archiveMembersCompared': count, 'archives': len(archives), 'csv': 'passed'}))
    elif not sys.argv[1:]:
        OUT.mkdir(exist_ok=True)
        for name, members in archives.items():
            with zipfile.ZipFile(OUT / name, 'w', zipfile.ZIP_DEFLATED) as archive:
                for member, data in sorted(members.items()):
                    info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o644 << 16
                    archive.writestr(info, data)
        (OUT / 'GeoStatLab_mappa_esperimenti.csv').write_bytes(csv_bytes)
        print('Entrambi gli archivi e la mappa CSV aggiornati dai sorgenti.')
    else:
        raise SystemExit('Usage: package-downloads.py [--check]')


if __name__ == '__main__':
    main()
