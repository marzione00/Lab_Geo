"""Elementi editoriali e diagrammi vettoriali originali di Locus M11."""
from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
SLIDES = []
SEZIONI = [(2,'I · DATO E SUPPORTO'), (17,'II · COORDINATE E DISTANZE'),
 (32,'III · CARTE E APPARTENENZE'), (44,'IV · VICINATI E PESI'),
 (56,'V · ASSOCIAZIONE SPAZIALE'), (71,'VI · SEMIVARIANZA'),
 (82,'VII · COPERTURA DEL CAMPIONE'), (92,'VIII · PREVISIONE SPAZIALE'),
 (106,'IX · CONSEGNA E STUDIO')]

def p(s): return '\\PBody{' + s + '}\n\\vspace{2.5mm}\n'
def sm(s): return '\\PSmall{' + s + '}\n'
def lab(s): return '\\PLabel{' + s + '}\n'
def info(s): return '\\PInfo{' + s + '}\n'
def eq(s): return '\\[' + s + '\\]\n'
def fig(name, caption='', height=5.25):
    return ('\\includegraphics[width=9.85cm,height=' + str(height) +
            'cm,keepaspectratio]{Risultati/Figure/' + name + '.pdf}\n' +
            ('\\vspace{1.5mm}\n' + sm(caption) if caption else ''))

def table(headers, rows, widths=None):
    n = len(headers)
    if widths is None: widths = [(9.6-0.422*(n-1))/n] * n
    cols = '@{}' + ''.join('p{'+str(w)+'cm}' for w in widths) + '@{}'
    return ('{\\fontsize{10.2}{13.1}\\selectfont\\renewcommand{\\arraystretch}{1.45}' +
            '\\begin{tabular}{' + cols + '}\\toprule\n' +
            ' & '.join('\\textbf{'+h+'}' for h in headers) + '\\\\\\midrule\n' +
            '\n'.join(' & '.join(str(c) for c in r) + '\\\\' for r in rows) +
            '\n\\bottomrule\\end{tabular}}\n')

def code(text, title='R · calcolo riproducibile'):
    # Code is written to a dedicated UTF-8 .R file by the assembler.
    return {'text': text.strip()+'\n', 'title': title}

def slide(n, title, left, right, recall, snippet=None, notebook=None, source=None):
    assert n == len(SLIDES)+2, (n, len(SLIDES)+2)
    section = [s for k,s in SEZIONI if k<=n][-1]
    SLIDES.append(dict(page=n,title=title,section=section,left=left,right=right,
                       recall=recall,snippet=snippet,notebook=notebook,source=source or []))

def tikz(body, h=4.6):
    return ('\\begin{tikzpicture}[x=1cm,y=1cm]\n'
            '\\path[use as bounding box](-.1,-.15) rectangle(9.7,'+str(h)+');\n'+body+
            '\n\\end{tikzpicture}\n')

def boxes(items, edges=(), h=4.8):
    """items = (id, x, y, label, width, color)."""
    a=[]
    for ident,x,y,label,w,color in items:
        a.append(f'\\node[pFlow,text width={w}cm,fill={color}!7] ({ident}) at({x},{y})'+'{'+label+'};')
    for a0,b0,label in edges:
        a.append('\\draw[pEdge] ('+a0+') -- '+('node[pNote,fill=Paper,inner sep=1pt]{'+label+'} ' if label else '')+'('+b0+');')
    return tikz('\n'.join(a),h)

def read_rows(name):
    with (ROOT/'Calcoli'/(name+'.csv')).open() as f:return list(csv.DictReader(f))

def fmt(x,d=3):
    x=float(x)
    if 0<abs(x)<10**(-d):return ('%.2g'%x).replace('.',',')
    return f'{x:.{d}f}'.replace('.',',')

def metric_table(name,keys,labels,digits=3):
    rows=read_rows(name)
    return table(labels,[[r[k] if i==0 else fmt(r[k],digits) for i,k in enumerate(keys)] for r in rows])

def value(section,key,d=3):
    j=json.loads((ROOT/'Calcoli/riassunto.json').read_text())
    return fmt(j[section][key],d)

def internal_link(page,title):return '\\hyperlink{slide'+str(page)+'}{'+title+'}'

def experiment(ident,title):
    return r'\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m11-'+ident+'}{'+title+'}\n'

def grid(kind='points'):
    """Geometria didattica: griglia 4x4 con connessioni e supporti dichiarati."""
    a=[r'\draw[pAxis](1,.4)--(8.7,.4)node[right,pNote]{$x$};',
       r'\draw[pAxis](1,.4)--(1,5.0)node[above,pNote]{$y$};']
    if kind=='support':
        a += [r'\filldraw[fill=GeoA!10,draw=GeoA](2.2,1.15)rectangle(5.8,3.75);',
              r'\node[pLabel,anchor=west]at(6.1,3.6){supporto $B$};']
    if kind=='split':
        a += [r'\fill[GeoA!8](1.2,.6)rectangle(5.7,4.8);',
              r'\fill[GeoB!12](5.7,.6)rectangle(8.4,4.8);',
              r'\draw[GeoB,dashed](5.7,.55)--(5.7,4.9);']
    for iy in range(4):
        for ix in range(4):
            x=1.7+ix*2.0;y=.9+iy*1.1
            col='GeoB' if kind=='split' and ix>=2 else 'GeoA'
            if kind in ('neighbors','weights'):
                if ix<3:a.append(f'\\draw[Rule,line width=1pt]({x},{y})--({x+2},{y});')
                if iy<3:a.append(f'\\draw[Rule,line width=1pt]({x},{y})--({x},{y+1.1});')
            a.append(f'\\fill[{col}]({x},{y})circle(2.7pt);')
    if kind in ('neighbors','weights'):
        a += [r'\fill[GeoB](3.7,2)circle(4pt);',
              r'\node[pNote]at(5,4.9){connessioni locali dichiarate};']
    return tikz('\n'.join(a),5.25)

def supports():
    return tikz(r'''\filldraw[fill=GeoA!10,draw=GeoA](.7,1.0)rectangle(4.2,4.2);
\fill[GeoB](2.45,2.6)circle(3.5pt);
\node[pLabel]at(2.45,4.65){campione puntuale};
\node[pLabel]at(2.45,.45){$Z(s_i)$};
\filldraw[fill=GeoA!16,draw=GeoA](5.2,1.0)rectangle(8.7,4.2);
\foreach \x in {5.55,6.25,6.95,7.65,8.35}
 \foreach \y in {1.35,2.0,2.65,3.3,3.95}{\fill[GeoA](\x,\y)circle(1.4pt);}
\node[pLabel]at(6.95,4.65){media sul supporto};
\node[pLabel]at(6.95,.45){$Z(B)=|B|^{-1}\int_B Z(s)\,ds$};''',5.2)

def coordinates():
    return boxes([('a',2.3,3.8,'Numeri nelle colonne',3.7,'GeoA'),
                  ('b',7.1,3.8,'CRS e ordine degli assi',3.7,'GeoC'),
                  ('c',2.3,1.15,'Posizioni interpretabili',3.7,'GeoA'),
                  ('d',7.1,1.15,'Distanze e unità',3.7,'GeoB')],
                 [('a','c',''),('b','d',''),('c','d','')],4.8)

def projection():
    return boxes([('a',2.1,3.8,r'$(\lambda,\varphi)$\\gradi, CRS noto',3.6,'GeoA'),
                  ('b',7.3,3.8,r'$(E,N)$\\metri, UTM 32N',3.6,'GeoB'),
                  ('c',2.1,1.15,'Stessa posizione sulla Terra',3.6,'GeoA'),
                  ('d',7.3,1.15,'Coordinate numericamente diverse',3.6,'GeoB')],
                 [('a','b',''),('a','c',''),('b','d','')],4.8)

def sphere():
    return tikz(r'''\shade[ball color=GeoA!22,opacity=.75](4.6,2.6)circle(2.1);
\draw[GeoA!45](4.6,2.6)ellipse(2.1 and .6);
\draw[GeoA!45](4.6,2.6)ellipse(.75 and 2.1);
\fill[GeoB](3.35,2.8)circle(3pt);
\fill[GeoB](5.85,3.25)circle(3pt);
\draw[GeoB,line width=1.5pt](3.35,2.8)to[bend left=22](5.85,3.25);
\draw[Muted,dashed](3.35,2.8)--(5.85,3.25);
\node[pLabel,anchor=east]at(2.8,3.15){$s_1$};
\node[pLabel,anchor=west]at(6.2,3.5){$s_2$};
\node[pNote]at(4.6,.1){arco sulla sfera e corda nello spazio};''',5.1)

def membership():
    return tikz(r'''\filldraw[fill=GeoA!10,draw=GeoA](.6,1.1)rectangle(5.8,4.2);
\filldraw[fill=GeoB!14,draw=GeoB](3.6,1.1)rectangle(8.8,4.2);
\node[pLabel]at(2,3.7){regione A};
\node[pLabel]at(7.3,3.7){regione B};
\fill[GeoC](4.7,2.3)circle(4pt);
\node[pLabel]at(4.7,.5){un sito, due appartenenze};
\draw[pEdge](4.7,2.3)--(2.5,2.3);
\draw[pEdge](4.7,2.3)--(6.9,2.3);''',4.8)

def weightstar():
    return tikz(r'''\node[pFlow,fill=GeoB!10,text width=1.6cm](s)at(4.7,2.6){$s_i$};
\node[pFlow,fill=GeoA!8,text width=1.6cm](a)at(1.1,2.6){$s_1$};
\node[pFlow,fill=GeoA!8,text width=1.6cm](b)at(8.3,2.6){$s_2$};
\node[pFlow,fill=GeoA!8,text width=1.6cm](c)at(4.7,4.65){$s_3$};
\node[pFlow,fill=GeoA!8,text width=1.6cm](d)at(4.7,.6){$s_4$};
\draw[pEdge](a)--node[above,pNote]{$1/4$}(s);
\draw[pEdge](b)--node[above,pNote]{$1/4$}(s);
\draw[pEdge](c)--node[right,pNote]{$1/4$}(s);
\draw[pEdge](d)--node[right,pNote]{$1/4$}(s);''',5.3)

def permutation():
    return boxes([('a',2.2,3.8,'Coordinate e pesi restano fissi',3.7,'GeoA'),
                  ('b',7.2,3.8,'Valori osservati vengono permutati',3.7,'GeoB'),
                  ('c',2.2,1.15,r'Statistica osservata\\$I_{\mathrm{obs}}$',3.7,'GeoA'),
                  ('d',7.2,1.15,r'Riferimento nullo\\$I^{(1)},\ldots,I^{(B)}$',3.7,'GeoC')],
                 [('a','c',''),('b','d',''),('c','d','rango')],4.8)

def bufferedge():
    return tikz(r'''\fill[GeoB!10](2.2,2.6)circle(1.6);
\filldraw[fill=GeoA!5,draw=GeoA](2.2,.7)rectangle(8.8,4.6);
\begin{scope}
\clip(2.2,.7)rectangle(8.8,4.6);
\fill[GeoB!15](2.2,2.6)circle(1.6);
\end{scope}
\draw[GeoB,dashed,line width=1pt](2.2,2.6)circle(1.6);
\foreach \x in {2.8,4.4,6,7.6}
 \foreach \y in {1.2,2.4,3.6}{\fill[GeoA](\x,\y)circle(2.3pt);}
\draw[GeoB,line width=1pt](2.08,2.6)--(2.32,2.6);
\draw[GeoB,line width=1pt](2.2,2.48)--(2.2,2.72);
\node[pLabel]at(5.7,5.0){dominio campionato};
\node[pNote]at(1.2,.35){fuori dominio};
\node[pNote]at(5.8,.35){campioni disponibili};
''',5.3)

def pairs():
    return tikz(r'''\fill[GeoA](1.2,1.2)circle(4pt);
\fill[GeoB](7.9,3.8)circle(4pt);
\draw[GeoC,line width=1.2pt](1.2,1.2)--node[above,sloped,pLabel]{$h_{ij}=\|s_i-s_j\|$}(7.9,3.8);
\node[pLabel]at(1.3,.55){$z_i$};
\node[pLabel]at(7.9,4.4){$z_j$};
\node[pLabel]at(5.0,.8){contributo: $\tfrac12(z_i-z_j)^2$};''',5.1)

def validation_flow():
    return boxes([('a',2.1,3.8,'40 siti Ovest: stima e scelte',3.7,'GeoA'),
                  ('b',7.3,3.8,'Procedura fissata prima del test',3.7,'GeoC'),
                  ('c',2.1,1.15,'24 siti Est: valori tenuti fuori',3.7,'GeoB'),
                  ('d',7.3,1.15,'Errori e limiti del trasferimento',3.7,'GeoB')],
                 [('a','b',''),('b','d',''),('c','d','')],4.8)

def panorama(n,title,name,caption,recall,notebook=None,source=None):
    slide(n,title,'','',recall,notebook=notebook,source=source)
    SLIDES[-1].update(layout='panorama',figure=name,caption=caption)
