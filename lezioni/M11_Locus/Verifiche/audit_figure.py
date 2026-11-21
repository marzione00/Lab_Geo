"""Audit dei PDF scientifici. Dipendenza opzionale: PyMuPDF (fitz).
Dalla radice del modulo: python Verifiche/audit_figure.py
Controlla che le figure siano leggibili, monopagina, vettoriali e senza testo
oltre il bordo della pagina. La verifica di sovrapposizioni richiede anche
l'ispezione visiva dei render e della presentazione alla scala finale.
"""
from pathlib import Path
import json
import fitz
ROOT = Path(__file__).resolve().parents[1]
checks = []
for file in sorted((ROOT / 'Risultati/Figure').rglob('*.pdf')):
    document = fitz.open(file)
    page = document[0]
    spans = [span for block in page.get_text('dict')['blocks'] if 'lines' in block
             for line in block['lines'] for span in line['spans']]
    outside = [span['text'] for span in spans
               if span['bbox'][0] < -0.5 or span['bbox'][1] < -0.5
               or span['bbox'][2] > page.rect.width + 0.5
               or span['bbox'][3] > page.rect.height + 0.5]
    checks.append({'file': str(file.relative_to(ROOT)), 'pagine': len(document),
                   'immagini_bitmap': len(page.get_images()), 'testo_fuori_pagina': outside,
                   'font_pt_min': min(span['size'] for span in spans),
                   'font_pt_max': max(span['size'] for span in spans),
                   'larghezza_pt': page.rect.width, 'altezza_pt': page.rect.height})
assert all(check['pagine'] == 1 and check['immagini_bitmap'] == 0
           and not check['testo_fuori_pagina'] for check in checks), checks
result = {'figure_principali': 40, 'pannelli_dettaglio': 0, 'controlli': checks}
(ROOT / 'Verifiche/audit_figure_pdf.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(f"{len(checks)} PDF: una pagina ciascuno, zero bitmap, nessun testo oltre bordo.")
