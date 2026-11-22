"""Porta le figure delle slide (SVG chiari) sul pannello scuro delle tappe.

La palette delle presentazioni è unica per tutte le lezioni: i suoi colori passano ai token del sito con lo stesso
ruolo. Gli altri colori seguono il contesto in cui compaiono:
- testo e tratti restano chiari sul pannello, con la stessa tinta e luminosità ordinata;
- le campiture si invertono in modo monotono (le tinte leggere diventano superfici scure della stessa tinta, una
  scala di colori resta ordinata, rovesciata come la sua legenda);
- le figure con scale continue o superfici ombreggiate (più di 40 colori) cambiano soltanto sfondo, grigi e palette;
- i raster incorporati (maschere di trasparenza o dati su scala continua) restano intatti.
Il calcolo avviene in OKLab; la stessa funzione esiste in src/figure-tone.js per i grafici prodotti nel browser.
"""
import math
import re
import sys

MARK = ' data-tono="pannello"'


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def oklab(r, g, b):
    r, g, b = _lin(r), _lin(g), _lin(b)
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def srgb(L, a, b):
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    c = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
         -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
         -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    return tuple(min(1.0, max(0.0, _gam(min(1.0, max(0.0, x))))) for x in c)


def h2t(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def t2h(t):
    return '#%02X%02X%02X' % tuple(int(math.floor(x * 255 + 0.5)) for x in t)


PANEL = oklab(*h2t('0B192B'))
INK = oklab(*h2t('E3EEF5'))

# Palette delle presentazioni -> token del sito. Neutri: valgono in ogni contesto.
NEUTRAL = {'F8F6F1': '0B192B', 'F5F6F3': '0B192B', 'FFFFFF': '102739', 'F0F4F3': '12293B', 'D6DAD9': '35506A',
           '657180': 'A9C1D0', '253344': 'E3EEF5', '15283E': 'F2F8FB', '112236': 'E3EEF5', '000000': 'E3EEF5'}
# Colori della palette usati per testo e tratti; nelle campiture seguono la regola generale.
ACCENT = {'087C74': '5CC9B8', '72D8C8': '72D8C8', '1D7890': '62B8D2', 'C57E42': 'E5A46C', '7363AA': 'AE9FE6',
          '5146A5': 'A196EC', 'ABB5FF': 'ABB5FF'}
BACKGROUND = ('F8F6F1', 'F5F6F3')


def _neutral(L):
    """Grigi: luminosità invertita fra pannello e testo, tinta interpolata fra le due."""
    L2 = min(INK[0], max(PANEL[0], PANEL[0] + (1 - L) * (INK[0] - PANEL[0]) / 0.72))
    u = (L2 - PANEL[0]) / (INK[0] - PANEL[0])
    return srgb(L2, PANEL[1] + u * (INK[1] - PANEL[1]), PANEL[2] + u * (INK[2] - PANEL[2]))


def remap(rgb, role, safe=False):
    """rgb in [0, 1]; role: 'area' (campitura), 'box' (campitura sotto testo bianco), 'line' (tratto),
    'text' (glifi), 'label' (glifi bianchi su una campitura 'box')."""
    key = t2h(rgb)[1:]
    L, a, b = oklab(*rgb)
    C = math.hypot(a, b)
    if role == 'label' and key == 'FFFFFF':
        return h2t('F2F8FB')
    if role == 'box':
        # Intestazioni di tabella ed etichette su fondo scuro: superficie scura della stessa tinta, testo chiaro.
        L2 = 0.30 + 0.15 * L
        if C <= 0.02:
            u = (L2 - PANEL[0]) / (INK[0] - PANEL[0])
            return srgb(L2, PANEL[1] + u * (INK[1] - PANEL[1]), PANEL[2] + u * (INK[2] - PANEL[2]))
        k = min(1.0, 0.09 / C)
        return srgb(L2, a * k, b * k)
    if safe:
        # Scale continue e ombreggiature: soltanto sfondo, testo e assi grigi, palette nei tratti e nel testo.
        if key in BACKGROUND and role == 'area':
            return h2t(NEUTRAL[key])
        if key in NEUTRAL and key not in BACKGROUND and key != 'FFFFFF' and L < 0.75:
            return h2t(NEUTRAL[key])
        if role != 'area' and key in ACCENT:
            return h2t(ACCENT[key])
        if C <= 0.006 and L < 0.75:
            return _neutral(L)
        return rgb
    if key in NEUTRAL:
        return h2t(NEUTRAL[key])
    if role != 'area' and key in ACCENT:
        return h2t(ACCENT[key])
    if C <= (0.004 if role == 'area' and L > 0.85 else 0.02):
        return _neutral(L)
    if role == 'area' or L > 0.85:
        # Inversione monotona (anche per i tratti chiari, che nelle figure fanno da fasce e campiture): 0.97 -> 0.25, 0.53 -> 0.66; le tinte leggere guadagnano croma per restare leggibili.
        L2 = min(0.9, max(PANEL[0] + 0.02, 0.25 + (0.97 - L) * 0.932))
        k = max(1.0, min(4.0, 0.032 / C)) if L > 0.85 else 1.0
        return srgb(L2, a * k, b * k)
    # Testo e tratti: luminosità compressa in [0.70, 0.95], ordine conservato.
    L2 = 0.70 + 0.25 * min(1.0, max(0.0, (L - 0.25) / 0.65))
    return srgb(L2, a * 1.08, b * 1.08)


COLOR = r'rgb\(\s*([\d.]+)%\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*\)|#([0-9A-Fa-f]{6})(?![0-9A-Fa-f])'
PROP = re.compile(r'((?:fill|stroke|stop-color|flood-color)\s*(?:=\s*["\']\s*|:\s*))(' + COLOR + ')')
FILL = re.compile(r'((?<![\w-])fill\s*(?:=\s*["\']\s*|:\s*))(' + COLOR + ')')
TAG = re.compile(r'<([a-zA-Z][\w:-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>')
ANY = re.compile(COLOR)


def _parse(m):
    if m.group(1) is not None:
        return tuple(float(m.group(i)) / 100 for i in (1, 2, 3))
    return h2t(m.group(4))


def tone(svg):
    """SVG chiaro -> SVG per il pannello scuro. Rifiuta un SVG già trasformato."""
    head = re.search(r'<svg\b[^>]*>', svg)
    if not head:
        raise ValueError('SVG senza elemento radice')
    if MARK.strip() in head.group(0):
        raise ValueError('SVG già portato sul pannello')
    safe = len({m.group(0).replace(' ', '') for m in ANY.finditer(svg)}) > 40
    cache = {}

    def colour(rgb, role):
        k = (rgb, role)
        if k not in cache:
            cache[k] = t2h(remap(rgb, role, safe))
        return cache[k]

    tags = list(TAG.finditer(svg))
    kinds = []
    for i, t in enumerate(tags):
        nxt = tags[i + 1] if i + 1 < len(tags) else None
        glyphs = t.group(1) == 'g' and nxt is not None and nxt.group(1) == 'use' and '#glyph' in nxt.group(2)
        kinds.append(t.group(1) in ('text', 'tspan') or glyphs)
    # Testo bianco: la campitura che lo precede (non chiara) è il suo fondo. Un fondo scuro resta una superficie
    # scura con testo chiaro; un fondo di tono medio segue la regola generale e il testo prende il tono più leggibile.
    # Le campiture disegnate di seguito prima del testo (intestazioni affiancate) formano un gruppo.
    boxes, labels, run, after_text = set(), set(), [], False
    for i, t in enumerate(tags):
        m = FILL.search(t.group(2))
        if not m:
            continue
        rgb = _parse(re.match(COLOR, m.group(2)))
        if kinds[i]:
            after_text = True
            if t2h(rgb) == '#FFFFFF' and run and not safe:
                dark = [j for j, c in run if oklab(*c)[0] < 0.45]
                boxes.update(dark)
                if oklab(*run[-1][1])[0] < 0.45 or oklab(*remap(run[-1][1], 'area'))[0] < 0.59:
                    labels.add(i)
        elif oklab(*rgb)[0] <= 0.85:
            if after_text:
                run, after_text = [], False
            run.append((i, rgb))
    out, last = [], 0
    for i, t in enumerate(tags):
        name, attrs, text = t.group(1), t.group(2), kinds[i]

        def prop(m, i=i, text=text):
            p = m.group(1).split('=')[0].split(':')[0].strip()
            if p == 'stroke':
                role = 'line'
            elif text and p == 'fill':
                role = 'label' if i in labels else 'text'
            else:
                role = 'box' if i in boxes and p == 'fill' else 'area'
            return m.group(1) + colour(_parse(re.match(COLOR, m.group(2))), role)

        new = PROP.sub(prop, attrs)
        if name == 'svg' and t.start() == head.start():
            # Il nero implicito (testo senza fill, per esempio in svglite) diventa il colore del testo.
            new = new + ('' if re.search(r'(?<![\w-])fill\s*=', attrs) else ' fill="#E3EEF5"') + MARK
        out.append(svg[last:t.start(2)])
        out.append(new)
        last = t.end(2)
    out.append(svg[last:])
    res = ''.join(out)

    def css(m):
        def prop(n):
            role = 'line' if n.group(1).startswith('stroke') else 'area'
            return n.group(1) + colour(_parse(re.match(COLOR, n.group(2))), role)
        return m.group(1) + PROP.sub(prop, m.group(2)) + m.group(3)
    res = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', css, res, flags=re.S)
    left = [m.group(0) for m in ANY.finditer(res) if not _mapped(res, m)]
    if left:
        raise ValueError('colori fuori contesto: %s' % sorted(set(left))[:5])
    return res


def _mapped(res, m):
    """Un colore è stato trattato se compare come valore di fill, stroke o stop-color."""
    before = res[max(0, m.start() - 24):m.start()]
    return re.search(r'(?:fill|stroke|stop-color|flood-color)\s*(?:=\s*["\']\s*|:\s*)$', before) is not None


def main(paths):
    n = 0
    for p in paths:
        with open(p, encoding='utf-8') as f:
            svg = f.read()
        if MARK.strip() in svg[:2000]:
            continue
        with open(p, 'w', encoding='utf-8') as f:
            f.write(tone(svg))
        n += 1
    print('%d figure portate sul pannello, %d già trasformate' % (n, len(paths) - n))


def fixture(path):
    """Casi di prova condivisi con tests/figure-tone.test.mjs: stessi colori dalle due implementazioni."""
    import json
    pdftocairo = ('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="60" viewBox="0 0 100 60">'
                  '<defs><g id="glyph-0-0"><path d="M 0 0 L 1 1 Z"/></g>'
                  '<radialGradient id="r"><stop offset="0" stop-color="rgb(100%, 100%, 100%)"/>'
                  '<stop offset="1" stop-color="rgb(39.599609%, 44.299316%, 50.19989%)"/></radialGradient></defs>'
                  '<path fill="rgb(97.299194%, 96.499634%, 94.499207%)" d="M 0 0 L 100 0 L 100 60 Z"/>'
                  '<path fill="rgb(93.540955%, 96.389771%, 97.250366%)" d="M 1 1 L 9 9 Z"/>'
                  '<path fill="rgb(98.199463%, 95.448303%, 92.649841%)" d="M 1 1 L 9 9 Z"/>'
                  '<path fill="#61A0B1" d="M 1 1 L 9 9 Z"/><path fill="#EFB9BA" d="M 1 1 L 9 9 Z"/>'
                  '<path fill="none" stroke-width="1" stroke="rgb(3.137255%, 48.627451%, 45.490196%)" d="M 0 0 L 9 9"/>'
                  '<path fill="none" stroke="#7F7F7F" d="M 0 0 L 9 9"/><path fill="#15283E" d="M 0 0 L 9 9"/>'
                  '<g fill="rgb(14.509804%, 20%, 26.666667%)" fill-opacity="1"><use xlink:href="#glyph-0-0" x="1" y="2"/></g>'
                  '<g fill="rgb(77.254902%, 49.411765%, 25.882353%)"><use xlink:href="#glyph-0-0" x="1" y="2"/></g>'
                  '<g fill="rgb(100%, 100%, 100%)"><use xlink:href="#glyph-0-0" x="1" y="2"/></g></svg>')
    svglite = ("<svg xmlns='http://www.w3.org/2000/svg' class='svglite' width='648.00pt' height='396.00pt'>"
               "<defs><style type='text/css'><![CDATA[ .svglite line, .svglite polyline { fill: none; "
               "stroke: #000000; stroke-linecap: round; } ]]></style></defs>"
               "<rect width='100%' height='100%' style='stroke: none; fill: #F5F6F3;'/>"
               "<rect x='1' y='1' width='5' height='5' style='stroke-width: 1.07; stroke: #FFFFFF; fill: #EBEBEB;'/>"
               "<circle cx='3' cy='3' r='1.9' style='stroke-width: 0.71; stroke: #1B9E77; fill: #1B9E77;'/>"
               "<polyline points='1,1 2,2' style='stroke-width: 1.07; stroke: #D95F02;'/>"
               "<text x='1' y='2' style='font-size: 8.80px; fill: #4D4D4D; font-family: \"Liberation Sans\";'>a</text>"
               "<text x='1' y='2' style='font-size: 13.2px; fill: #000000;'>b</text>"
               "<rect x='1' y='1' width='5' height='5' style='fill: #C57E42;'/>"
               "<text x='2' y='3' style='font-size: 8.80px; fill: #FFFFFF;'>c</text>"
               "<rect x='1' y='1' width='5' height='5' style='fill: #9DC3E6;'/>"
               "<text x='2' y='3' style='font-size: 8.80px; fill: #FFFFFF;'>d</text></svg>")
    scale = ''.join('<rect x="%d" y="0" width="1" height="1" fill="#%02X%02XA0"/>' % (i, 120 + 2 * i, 230 - 2 * i)
                    for i in range(45))
    safe = ('<svg xmlns="http://www.w3.org/2000/svg" width="45" height="10" viewBox="0 0 45 10">'
            '<path fill="#F5F6F3" d="M 0 0 L 45 0 L 45 10 Z"/>' + scale +
            '<path fill="none" stroke="#4D4D4D" d="M 0 0 L 9 9"/><path fill="none" stroke="#FFFFFF" d="M 0 0 L 9 9"/>'
            '<text x="1" y="9" fill="#1D7890">c</text></svg>')
    cases = [{'name': n, 'input': v, 'expected': tone(v).replace(MARK, '')}
             for n, v in (('pdftocairo', pdftocairo), ('svglite', svglite), ('scala continua', safe))]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cases, f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    if sys.argv[1:2] == ['--fixture']:
        fixture(sys.argv[2])
    else:
        main(sys.argv[1:])
