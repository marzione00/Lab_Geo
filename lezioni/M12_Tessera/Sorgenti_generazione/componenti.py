"""Elementi editoriali e diagrammi vettoriali originali di Tessera M12."""
from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
SLIDES = []
FIGURES = {
 'dem_quota':'01_dem',
 'orientamento_angoli':'02_orientamento',
 'maschera':'04_maschera_nodata',
 'medie_maschera':'05_effetto_zero',
 'dominio_crop':'06_ritaglio',
 'aggregazione_2x2':'08_aggregazione',
 'statistiche_aggregazione':'09_perdita_estremi',
 'ricampionamento_continuo':'12_ricampionamento_continuo',
 'ricampionamento_categorie':'13_ricampionamento_classi',
 'allineamento_mezzo_pixel':'14_origini_15m',
 'sensibilita_risoluzione':'10_risoluzioni_analitiche'
}
SEZIONI = [(2,'I · TERRITORIO E GRIGLIA'),(6,'II · GEOMETRIA RASTER'),(20,'III · MASCHERE E DOMINIO'),(33,'IV · RISOLUZIONE E ALLINEAMENTO'),(49,'V · MORFOMETRIA'),(67,'VI · LUCE E RILIEVO'),(77,'VII · BANDE E INDICI'),(91,'VIII · SINTESI TERRITORIALI'),(103,'IX · CONSEGNA E VERIFICA')]

def p(s): return '\\PBody{' + s + '}\n\\vspace{2.5mm}\n'
def sm(s): return '\\PSmall{' + s + '}\n'
def lab(s): return '\\PLabel{' + s + '}\n'
def info(s): return '\\PInfo{' + s + '}\n'
def eq(s): return '\\[' + s + '\\]\n'
def fig(name, caption='', height=5.25):
    name=FIGURES.get(name,name)
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
    return r'\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m12-'+ident+'}{'+title+'}\n'

def panorama(n,title,name,caption,recall,notebook=None,source=None):
    slide(n,title,'','',recall,notebook=notebook,source=source)
    SLIDES[-1].update(layout='panorama',figure=FIGURES.get(name,name),caption=caption)

def raster_grid(mode='centres'):
    a=[r'\draw[pAxis](.8,.4)--(8.7,.4)node[right,pNote]{$x$};',
       r'\draw[pAxis](.8,.4)--(.8,5.0)node[above,pNote]{$y$};']
    for i in range(4):
        for j in range(6):
            x=1.3+j*1.1;y=.85+i*.9
            col='GeoA!12'
            if mode=='mask' and 1<=i<=2 and 2<=j<=3:col='GeoC!25'
            if mode=='zone':col='GeoA!14' if j<3 else 'GeoB!18'
            a.append(f'\\filldraw[fill={col},draw=white,line width=1pt]({x},{y})rectangle({x+1.1},{y+.9});')
            if mode=='centres':a.append(f'\\fill[GeoA]({x+.55},{y+.45})circle(1.6pt);')
    a.append(r'\node[pNote]at(4.6,4.8){schema: sei colonne, quattro righe};')
    return tikz('\n'.join(a),5.25)

def corner_centre():
    return tikz(r'''\filldraw[fill=GeoA!10,draw=GeoA,line width=1pt](1.3,.9)rectangle(5.3,4.5);
\fill[GeoB](1.3,4.5)circle(3.4pt);
\fill[GeoA](3.3,2.7)circle(3.4pt);
\draw[GeoA,dashed](3.3,.9)--(3.3,4.5);
\draw[GeoA,dashed](1.3,2.7)--(5.3,2.7);
\draw[<->,draw=Muted](1.3,.55)--node[below,pNote]{$\Delta x$}(5.3,.55);
\draw[<->,draw=Muted](.9,.9)--node[left,pNote]{$\Delta y$}(.9,4.5);
\node[pLabel,anchor=west]at(5.65,4.1){angolo superiore sinistro};
\node[pNote,anchor=west]at(5.65,3.55){$(x_{\min},y_{\max})$};
\node[pLabel,anchor=west]at(5.65,2.55){centro della cella};
\node[pNote,anchor=west,text width=3.6cm]at(5.65,1.8){mezzo passo verso Est\\mezzo passo verso Sud};''',5.15)

def orientation():
    a=[]
    for panel,x0 in enumerate([.6,5.5]):
        a.append(f'\\node[pLabel]at({x0+1.8},4.6)'+'{'+('matrice locale' if panel==0 else 'matrice GeoTIFF')+'};')
        for row in range(3):
            for col in range(3):
                v=(row if panel==0 else 2-row)*3+col+1
                x=x0+col*1.2;y=.9+(2-row)*1.05
                a.append(f'\\filldraw[fill=GeoA!{10+v*3},draw=white]({x},{y})rectangle({x+1.2},{y+1.05});')
                a.append(f'\\node[pLabel]at({x+.6},{y+.525})'+'{'+str(v)+'};')
        a.append(f'\\node[pNote]at({x0+1.8},.4)'+'{'+('riga 1: Sud' if panel==0 else 'riga 1: Nord')+'};')
    a.append(r'\draw[pEdge](4.4,2.4)--(5.15,2.4);')
    return tikz('\n'.join(a),5.15)

def bilinear():
    return tikz(r'''\draw[GeoA,line width=1pt](1.2,1)rectangle(7.8,4.3);
\foreach \x/\y in {1.2/1,7.8/1,1.2/4.3,7.8/4.3}{\fill[GeoA](\x,\y)circle(3.2pt);}
\fill[GeoB](3.8,2.2)circle(3.8pt);
\draw[GeoB,dashed](3.8,1)--(3.8,4.3);
\draw[GeoB,dashed](1.2,2.2)--(7.8,2.2);
\node[pNote]at(1.2,.45){$(1-u)(1-v)$};
\node[pNote]at(7.8,.45){$u(1-v)$};
\node[pNote]at(1.2,4.8){$(1-u)v$};
\node[pNote]at(7.8,4.8){$uv$};
\node[pLabel,anchor=west]at(4.1,2.55){bersaglio $(u,v)$};
\node[pNote]at(4.7,5.35){schema bilineare fra quattro centri};''',5.65)

def stencil():
    a=[]
    for i in range(3):
        for j in range(3):
            x=2.1+j*1.55;y=.6+i*1.4
            fill='GeoB!18' if i==1 and j==1 else 'GeoA!9'
            a.append(f'\\filldraw[fill={fill},draw=Rule]({x},{y})rectangle({x+1.55},{y+1.4});')
    for x,y,label in [(4.425,2.7,r'z_{ij}'),(5.975,2.7,r'z_{i,j+1}'),(2.875,2.7,r'z_{i,j-1}'),(4.425,4.1,r'z_{i+1,j}'),(4.425,1.3,r'z_{i-1,j}')]:
        a.append(f'\\node[pLabel]at({x},{y})'+'{$'+label+'$};')
    a += [r'\draw[pEdge](7.1,1)--(7.1,4.6)node[above,pNote]{Nord};',
          r'\draw[<->,Muted](2.875,.2)--node[below,pNote]{$2\Delta x$}(5.975,.2);']
    return tikz('\n'.join(a),5.3)

def azimuth():
    return tikz(r'''\draw[Rule,line width=1pt](4.7,2.7)circle(1.8);
\draw[pAxis](2.4,2.7)--(7,2.7);
\draw[pAxis](4.7,.4)--(4.7,5);
\node[pLabel]at(4.7,5.3){N: $0^\circ$};
\node[pLabel]at(7.8,2.7){E: $90^\circ$};
\node[pLabel]at(4.7,.05){S: $180^\circ$};
\node[pLabel]at(1.5,2.7){O: $270^\circ$};
\draw[-{Latex},GeoA,line width=1.6pt](4.7,2.7)--(5.95,3.95);
\draw[-{Latex},GeoB,line width=1.6pt](4.7,2.7)--(3.45,1.45);
\node[pNote,anchor=west]at(6.05,4.1){salita: $\nabla z$};
\node[pNote,anchor=east]at(3.35,1.25){discesa: $-\nabla z$};''',5.65)

def halo():
    a=[]
    for i in range(8):
        for j in range(10):
            x=1.0+j*.65;y=.65+i*.53
            inside=1<=i<=6 and 1<=j<=8
            color='GeoA!17' if inside else 'GeoB!23'
            a.append(f'\\filldraw[fill={color},draw=white]({x},{y})rectangle({x+.65},{y+.53});')
    a += [r'\draw[GeoA,line width=1pt](1.65,1.18)rectangle(6.85,4.36);',
          r'\node[pLabel]at(4.3,5.35){leggere anche i vicini della finestra};',
          r'\node[pNote,anchor=west]at(7.9,3.7){nucleo\\48 celle};',
          r'\node[pNote,anchor=west]at(7.9,1.7){bordo\\32 celle};']
    return tikz('\n'.join(a),5.7)

def layers():
    return tikz(r'''\filldraw[fill=GeoA!13,draw=GeoA](.8,1.05)--(5.8,1.05)--(8,2.45)--(3,2.45)--cycle;
\filldraw[fill=GeoB!15,draw=GeoB](.8,2.2)--(5.8,2.2)--(8,3.6)--(3,3.6)--cycle;
\filldraw[fill=GeoC!14,draw=GeoC](.8,3.35)--(5.8,3.35)--(8,4.75)--(3,4.75)--cycle;
\draw[Muted,dashed](3,2.45)--(3,4.75);
\draw[Muted,dashed](5.8,1.05)--(5.8,3.35);
\node[pNote,anchor=west]at(8.1,4.7){banda 3};
\node[pNote,anchor=west]at(8.1,3.55){banda 2};
\node[pNote,anchor=west]at(8.1,2.4){banda 1};
\node[pLabel]at(4.7,.35){stessa geometria, valori e metadati distinti};''',5.35)

