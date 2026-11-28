"""Genera il sorgente Beamer di una lezione M17-M21 a partire dalla sua specifica (spec_<id>.py).

Uso, dalla radice del repository:  python3 -I lezioni/Edizione_M17-M21/genera.py M17
Scrive lezioni/<id>_<Pianeta>/<id>_<Pianeta>.tex e Indice.csv. Preambolo, cornici, colonne e riquadri sono quelli
delle lezioni planetarie T00 e M13-M16 (impaginazione da Tessera); le pagine si numerano da sole, l'indice dei
capitoli e i segnalibri seguono i capitoli della specifica. I risultati dei frammenti R vengono letti da
Codice/risultati-capitoli.json.

Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
"""
import importlib.util
import json
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
LEZIONI = QUI.parent
SITO = 'https://marzione00.github.io/Lab_Geo/'
SX = r'\node[anchor=north west,inner sep=0] at([xshift=.96cm,yshift=-2.12cm]current page.north west){\Colonna{9.40cm}{'
DX = r'\node[anchor=north west,inner sep=0] at([xshift=10.85cm,yshift=-2.12cm]current page.north west){\Colonna{8.16cm}{'
CODICE = (r'\begin{tcolorbox}[enhanced,arc=1.7mm,boxrule=.6pt,colback=white,colframe=Classical!60!Navy,'
          r'colbacktitle=Navy,coltitle=white,fonttitle=\bfseries\small,title={R · calcolo riproducibile},left=1.7mm,'
          r'right=1.3mm,top=1.1mm,bottom=1.1mm,before skip=1mm,after skip=1.0mm]\lstinputlisting[style=GeoR,'
          r'language=R]{Codice/%s}\end{tcolorbox}')
TABELLA = (r'{\fontsize{10.2}{12.8}\selectfont\begin{tabular}{@{}>{\raggedright\arraybackslash}p{0.48\linewidth}'
           r'@{\hspace{.13cm}}>{\raggedright\arraybackslash}p{0.224\linewidth}@{\hspace{.13cm}}>{\raggedright'
           r'\arraybackslash}p{0.224\linewidth}@{}}\toprule Grandezza & A & B\\[2.3pt]' + '\n' + r'\midrule ')


def carica(lid):
    spec = importlib.util.spec_from_file_location('spec', QUI / ('spec_' + lid + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LEZIONE


def tt(riga):
    """Una riga di uscita di R in un riquadro a spaziatura fissa."""
    out = ''
    for ch in riga.rstrip():
        out += {' ': r'\ ', '_': r'\_', '$': r'\$', '%': r'\%', '&': r'\&', '#': r'\#', '{': r'\{', '}': r'\}',
                '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '\\': r'\textbackslash{}'}.get(ch, ch)
    return r'\mbox{' + out + '}'


def uscita(testo):
    righe = [tt(r) for r in testo.split('\n')]
    return (r'\PLabel{Risultato in R}' + '\n' + r'\begin{tcolorbox}[colback=GeoTint,colframe=Rule,boxrule=.5pt,'
            r'arc=1.4mm,left=2mm,right=1mm,top=1mm,bottom=1mm]{\fontsize{8.6}{11.4}\selectfont\ttfamily '
            + r'\\'.join(righe) + '}\\end{tcolorbox}')


def formula(f):
    return r'\par\smallskip{\centering\adjustbox{max width=.98\linewidth}{$\displaystyle ' + f + r'$}\par\smallskip}'


def blocchi(p, chiavi=('body', 'formula', 'symbols')):
    s = ''
    if p.get('label'):
        s += r'\PLabel{' + p['label'] + '}\n'
    if p.get('body'):
        s += r'\PBody{' + p['body'] + '}\n'
    if p.get('formula'):
        s += formula(p['formula']) + '\n'
    if p.get('symbols'):
        s += r'\PSmall{' + p['symbols'] + '}\n'
    return s


def immagine(p):
    if p.get('fig'):
        return (r'{\centering\includegraphics[width=\linewidth,height=' + p.get('h', '6.15cm') + r',keepaspectratio]{'
                + p['fig'] + r'}\par}' + '\n')
    return r'{\centering\resizebox{' + p.get('scala', '0.94') + r'\linewidth}{!}{\input{' + p['diag'] + r'}}\par}' + '\n'


def lab(eid, testo='Apri il laboratorio'):
    return (r'\node[anchor=north east,inner sep=0] at([xshift=17.1cm,yshift=-12.04cm]current page.north west)'
            r'{\fontsize{7.7}{9}\selectfont \href{' + SITO + r'\#laboratorio/' + eid + r'}{\color{Classical}\bfseries '
            + testo + ' · ' + eid + '}};\n')


def titolo(t):
    return t if len(t) <= 52 else r'{\fontsize{15.3}{19}\selectfont ' + t + '}'


def num(x):
    return str(x).replace('.', '{,}') if isinstance(x, (int, float)) else x


def genera(lid):
    L = carica(lid)
    cartella = LEZIONI / (lid + '_' + L['planet'])
    risultati = json.loads((cartella / 'Codice' / 'risultati-capitoli.json').read_text())
    pagine = [{'tipo': 'copertina'}, {'tipo': 'indice'}, dict(L['caso'], tipo='caso')]
    capitoli = []
    for cap in L['capitoli']:
        capitoli.append((cap['titolo'], len(pagine) + 1))
        for i, p in enumerate(cap['pagine']):
            pagine.append(dict(p, sezione=cap['titolo'].upper(), apre=cap['titolo'] if i == 0 else None))
    pagine.append(dict(L['sintesi'], tipo='sintesi', sezione='SINTESI', apre='Sintesi'))
    pagine.append(dict(L['riferimenti'], tipo='riferimenti', sezione='RIFERIMENTI', apre='Riferimenti'))
    n = len(pagine)
    pre = (LEZIONI / 'M16_Prisma' / 'M16_Prisma.tex').read_text().split(r'\begin{document}')[0]
    for a, b in [('Prisma · Classificazione e validazione', L['planet'] + ' · ' + L['title']),
                 ('M16_Prisma.tex', lid + '_' + L['planet'] + '.tex'), ('62 slide.', str(n) + ' slide.'),
                 ('GeoStat Lab · M16', 'GeoStat Lab · ' + lid), ('#3/62', '#3/' + str(n))]:
        assert a in pre, a
        pre = pre.replace(a, b)
    out = [pre + r'\begin{document}' + '\n']
    indice = []
    for k, p in enumerate(pagine, start=1):
        t = p['tipo']
        if t == 'copertina':
            c = L['copertina']
            out.append(r'''
\begin{frame}[plain]\hypertarget{slide1}{}\bookmark[level=0,page=1]{%(P)s}
\begin{tikzpicture}[remember picture,overlay]
\fill[Night](current page.south west) rectangle(current page.north east);
\IfFileExists{Scena/copertina.jpg}{\node[inner sep=0] at(current page.center){\includegraphics[width=20cm,height=12.5cm]{Scena/copertina.jpg}};}{}
\node[anchor=north west,inner sep=0] at([xshift=1.05cm,yshift=-1.10cm]current page.north west){\color{Mint}\bfseries\fontsize{23}{28}\selectfont %(PU)s};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-2.16cm]current page.north west){\color{white}\fontsize{9}{12}\selectfont MODULO %(ID)s · SCIENZE DELLA TERRA};
\draw[Mint,line width=1.5pt]([xshift=1.07cm,yshift=-2.78cm]current page.north west)--([xshift=2.6cm,yshift=-2.78cm]current page.north west);
\node[anchor=north west,inner sep=0] at([xshift=1.05cm,yshift=-3.35cm]current page.north west){\begin{minipage}{9.2cm}\raggedright\color{white}\bfseries\fontsize{28.5}{34.5}\selectfont %(T)s\end{minipage}};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-7.88cm]current page.north west){\begin{minipage}{8.9cm}\raggedright\color{Lilac}\fontsize{12.2}{17}\selectfont %(S1)s\end{minipage}};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-8.70cm]current page.north west){\begin{minipage}{8.9cm}\raggedright\color{white!75}\fontsize{10.3}{14.5}\selectfont %(S2)s\end{minipage}};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-10.52cm]current page.north west){\color{white}\fontsize{10.5}{14}\selectfont GeoStat Lab · corso di Marzio De Corato};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-11.17cm]current page.north west){\color{Mint}\fontsize{8.8}{11}\selectfont\href{https://creativecommons.org/licenses/by-nc-sa/4.0/}{Impaginazione da Tessera · CC BY-NC-SA 4.0}};
\end{tikzpicture}\end{frame}
''' % dict(P=L['planet'], PU=L['planet'].upper(), ID=lid, T=c['titolo'], S1=c['sottotitolo'], S2=c['riga']))
            indice.append((1, 'COPERTINA', L['title']))
            continue
        if t == 'indice':
            titolo_p, sez, ric = 'Indice della presentazione', 'PERCORSO', ('I titoli dell’indice aprono i capitoli. Il nome '
                                                                         'del capitolo in alto riporta a questa pagina.')
        elif t == 'caso':
            titolo_p, sez, ric = p['domanda'], 'IL CASO GUIDA', p['ricorda']
        else:
            titolo_p, sez, ric = p['titolo'], p['sezione'], p['ricorda']
        out.append('\n' + r'\begin{frame}[plain]\hypertarget{slide%d}{}' % k + '\n')
        if p.get('apre'):
            out.append(r'\bookmark[level=0,page=%d]{%s}' % (k, p['apre']) + '\n')
        out.append(r'\bookmark[level=1,page=%d]{%s}' % (k, titolo_p) + '\n')
        out.append(r'\begin{tikzpicture}[remember picture,overlay]' + '\n')
        out.append(r'\PilotChrome{%s}{%s}{%d}{%s}' % (titolo(titolo_p), sez, k, ric) + '\n')
        indice.append((k, sez, titolo_p))
        if t == 'indice':
            voci = ''.join(r'{\fontsize{10.7}{13.5}\selectfont\hyperlink{slide%d}{%s\hfill %d}\par}\vspace{.16cm}' % (pg, ti, pg)
                           + '\n' for ti, pg in capitoli)
            out.append(SX + r'\PLabel{Capitoli}' + '\n' + voci + '}};\n')
            out.append(DX + r'\PLabel{Percorso di lettura}' + '\n' + r'\PBody{' + L['percorso'] + '}\n'
                       + r'\PInfo{Le pagine Scenario A e Confronto riprendono gli esperimenti nel browser. I valori di '
                       r'partenza del simulatore possono differire dal caso guida.}' + '\n'
                       + r'\href{' + SITO + r'\#modulo-' + lid + r'}{\color{Classical}\bfseries Apri gli esperimenti di '
                       + L['planet'] + '}}};\n')
        elif t == 'caso':
            out.append(SX + immagine({'diag': 'Diagrammi/apertura.tex', 'scala': '.97'}) + '}};\n')
            out.append(DX + r'\PLabel{Il caso}' + '\n' + r'\PBody{' + p['body'] + '}\n' + r'\PInfo{' + p['info'] + '}\n}};\n')
        elif t in ('figura', 'schema'):
            out.append(SX + immagine(p) + (r'\PSmall{' + p['didascalia'] + '}\n' if p.get('didascalia') else '') + '}};\n')
            out.append(DX + blocchi(p) + '}};\n')
        elif t == 'domanda':
            out.append(SX + r'\PLabel{Domanda}' + '\n' + r'\PBody{' + p['domanda_testo'] + '}\n' + r'\vspace{.35cm}'
                       + r'\PLabel{Interpretazione}' + '\n' + r'\PBody{' + p['interpretazione'] + '}\n}};\n')
            out.append(DX + CODICE % p['codice'] + '\n' + uscita(risultati[p['codice']]) + '}};\n')
        elif t == 'codice':
            out.append(SX + blocchi(p) + '}};\n')
            out.append(DX + CODICE % p['codice'] + '\n' + uscita(risultati[p['codice']]) + '}};\n')
        elif t == 'testo':
            out.append(SX + blocchi(p['sinistra']) + '}};\n')
            out.append(DX + blocchi(p['destra']) + '}};\n')
        elif t == 'scenario':
            e = p['esperimento']
            out.append(SX + immagine({'fig': 'Esperimenti/' + e + '-A.pdf', 'h': '6.0cm'}) + r'\PSmall{' + p['didascalia']
                       + '}\n}};\n')
            out.append(DX + r'\PLabel{Scenario A · simulazione}' + '\n' + blocchi(p) + '}};\n' + lab(e))
        elif t == 'confronto':
            e = p['esperimento']
            dati = json.loads((cartella / 'Esperimenti' / (e + '.json')).read_text())
            va = {m['grandezza']: m['valore'] for m in dati[0]['metrics']}
            vb = {m['grandezza']: m['valore'] for m in dati[1]['metrics']}
            righe = ''.join('%s & %s & %s\\\\[2.3pt]\n' % (r[0], num(va[r[1]].strip().replace('.', '{,}')),
                                                           num(vb[r[1]].strip().replace('.', '{,}'))) for r in p['righe'])
            out.append(SX + immagine({'fig': 'Esperimenti/' + e + '-B.pdf', 'h': '5.6cm'}) + r'\PSmall{' + p['didascalia']
                       + '}\n}};\n')
            out.append(DX + r'\PLabel{Confronto fra gli scenari}' + '\n' + TABELLA + '\n' + righe
                       + r'\bottomrule\end{tabular}\par}' + '\n' + r'\vspace{.25cm}\PBody{' + p['body'] + '}\n}};\n' + lab(e))
        elif t == 'sintesi':
            out.append(SX + r'\PLabel{Domanda di partenza}' + '\n' + r'\PBody{' + L['caso']['domanda'] + '}\n'
                       + r'\PLabel{Risultato da discutere}' + '\n' + r'\PBody{' + p['risultato'] + '}\n}};\n')
            out.append(DX + r'\PLabel{Limiti della conclusione}' + '\n' + r'\PBody{' + p['limiti'] + '}\n'
                       + r'\vspace{.4cm}\href{' + SITO + r'\#modulo-' + lid + r'}{\color{Classical}\bfseries Torna agli '
                       r'esperimenti di ' + L['planet'] + '}\n}};\n')
        elif t == 'riferimenti':
            out.append(SX + r'\PLabel{Fonti}' + '\n' + r'{\fontsize{9.4}{12.2}\selectfont ' + p['fonti'] + '\\par}\n}};\n')
            out.append(DX + r'\PLabel{Dati e codice}' + '\n' + r'\PBody{' + p['dati'] + '}\n'
                       + r'\vspace{.3cm}\href{' + SITO + r'\#lezione-' + lid + r'}{\color{Classical}\bfseries Apri le tappe '
                       r'di ' + L['planet'] + ' su GeoStat Lab}\n}};\n')
        else:
            raise ValueError(t)
        out.append(r'\end{tikzpicture}\end{frame}' + '\n')
    out.append(r'\end{document}' + '\n')
    (cartella / (lid + '_' + L['planet'] + '.tex')).write_text(''.join(out))
    righe = ['Pagina,Titolo', '1,Copertina'] + ['%d,"%s"' % (k, ti.replace('"', '""')) for k, _, ti in indice[1:]]
    (cartella / 'Indice.csv').write_text('\n'.join(righe) + '\n')
    print(lid, n, 'pagine;', len(capitoli), 'capitoli')


if __name__ == '__main__':
    for lid in sys.argv[1:]:
        genera(lid)
