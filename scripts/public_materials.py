"""Publish teaching materials while retaining editorial records in source only."""
from pathlib import Path
import argparse
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
TRANSIENT = {'.aux', '.log', '.nav', '.snm', '.toc', '.out', '.pyc'}


def public_path(relative):
    path = Path(relative)
    if path.parts[0] == 'audit':
        return False
    if path.parts[0] == 'verifiche' and path.as_posix() != 'verifiche/versioni_R.csv':
        return False
    if path.stem in {'Rapporto_revisione_R6', 'Registro_slide_R6', 'revisione_R6', 'CONSEGNA_R6'}:
        return False
    return (not any(p.startswith('.') or p == '__pycache__' for p in path.parts)
            and path.suffix not in TRANSIENT
            and path.suffix.lower() not in {'.key', '.p12', '.pfx'})


def public_bytes(relative):
    path = ROOT / 'materiali' / relative
    if path.is_symlink():
        raise ValueError(f'Symbolic link in publication: {path}')
    data = path.read_bytes()
    if str(relative) == 'Indice_corso.html':
        text = data.decode()
        text, count = re.subn(r'<p><a href="audit/Rapporto_revisione_R6\.pdf">.*?</p>', '', text)
        if count != 1:
            raise ValueError('The original index changed: review its public projection')
        return text.replace('Revisione R6', 'Edizione R6').encode()
    if str(relative) == 'LEGGIMI.txt':
        text = data.decode()
        if text.count('\nRILETTURA R6\n') != 1:
            raise ValueError('The original guide changed: review its public projection')
        text = text.split('\nRILETTURA R6\n')[0]
        return text.replace('REVISIONE R6', 'EDIZIONE R6').replace('struttura, revisione e ricostruzione', 'struttura e ricostruzione').encode()
    return data


def checksum_manifest(files):
    return ''.join(hashlib.sha256(data).hexdigest() + '  ' + name + '\n'
                   for name, data in sorted(files.items())).encode()


def publish(output):
    files = {}
    for path in sorted((ROOT / 'materiali').rglob('*')):
        relative = path.relative_to(ROOT / 'materiali').as_posix()
        if not public_path(relative):
            continue
        if path.is_symlink():
            raise ValueError(f'Symbolic link in publication: {path}')
        if path.is_file() and relative != 'MANIFEST_SHA256.txt':
            files[relative] = public_bytes(relative)
    for relative, data in files.items():
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def write_manifest(output):
    files = {path.relative_to(output).as_posix(): path.read_bytes()
             for path in output.rglob('*')
             if path.is_file() and path.name != 'MANIFEST_SHA256.txt'}
    (output / 'MANIFEST_SHA256.txt').write_bytes(checksum_manifest(files))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manifest-only', action='store_true')
    args = parser.parse_args()
    if args.manifest_only:
        write_manifest(args.output)
    else:
        publish(args.output)
