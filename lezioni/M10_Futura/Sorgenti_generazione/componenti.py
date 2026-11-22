"""Elementi editoriali e diagrammi vettoriali originali di Futura M10."""
from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
SLIDES = []
SEZIONI = [(2, 'I · IL COMPITO PREVISIONALE'), (11, 'II · RIFERIMENTI'),
           (23, 'III · MEMORIA E INNOVAZIONI'), (40, 'IV · ARIMA E STAGIONE'),
           (58, 'V · DIAGNOSTICA'), (70, 'VI · VALIDAZIONE TEMPORALE'),
           (83, 'VII · ERRORI E INTERVALLI'), (94, 'VIII · SISTEMI MULTIVARIATI'),
           (102, 'IX · PROGETTO STATISTICO')]

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

def timeline(kind='split'):
    if kind=='split':
        return tikz(r'''\fill[GeoA!17](.4,1.7)rectangle(7.2,3.25);
\fill[GeoB!18](7.2,1.7)rectangle(9.4,3.25);
\node[pLabel]at(3.8,2.65){Addestramento: 168 mesi};
\node[pNote]at(3.8,2.05){gennaio 1985 -- dicembre 1998};
\node[pLabel]at(8.3,2.65){Test: 36};
\node[pNote]at(8.3,2.05){1999--2001};
\draw[Classical,line width=1pt](7.2,1.35)--(7.2,3.7);
\node[pLabel,anchor=east]at(7.0,3.7){Origine $T$};
\draw[pAxis](.4,1.2)--(9.5,1.2);
\node[pNote]at(.8,.65){passato};\node[pNote]at(8.5,.65){futuro storico};
\draw[decorate,decoration={brace,amplitude=4pt},GeoB](7.2,4.05)--(9.4,4.05);
\node[pNote]at(8.3,4.45){$h=1,\ldots,36$};''',4.8)
    return tikz(r'''\draw[pAxis](.4,1.7)--(9.5,1.7);
\fill[GeoA!12](.5,1.7)rectangle(5.8,2.7);
\node[pLabel]at(3.1,2.2){Informazione $\mathcal F_T$};
\draw[GeoB,line width=1.2pt](5.8,1.4)--(5.8,3.1);
\node[pLabel]at(5.8,3.55){$T$};
\fill[GeoB](8.45,1.7)circle(3pt);
\node[pLabel]at(8.45,2.55){$Y_{T+h}$};
\node[pNote]at(8.45,1.1){da prevedere};
\draw[decorate,decoration={brace,amplitude=4pt},Classical](5.8,3.0)--(8.45,3.0);
\node[pNote]at(7.1,3.5){orizzonte $h$};''',4.2)

def origins(dense=False):
    a=[]
    origins_=[120,132,144] if not dense else [120,132,144,156]
    for j,o in enumerate(origins_):
        y=4.2-j*.92;x=.5+8.5*(o/204);end=.5+8.5*((o+12)/204)
        a += [f'\\fill[GeoA!20](.5,{y-.24})rectangle({x:.3f},{y+.24});',
              f'\\fill[GeoB!40]({x:.3f},{y-.24})rectangle({end:.3f},{y+.24});',
              f'\\node[pNote,anchor=west]at({end+.16:.3f},{y})'+'{'+str(o)+'};']
    x=.5+8.5*168/204
    a += [f'\\draw[Muted,dashed]({x:.3f},.6)--({x:.3f},4.65);',
          '\\node[pNote]at(4,.25){train in verde · verifica interna in rame};',
          '\\node[pNote]at(8.8,4.4){test\\\\finale};']
    return tikz('\n'.join(a),4.9)

def seasons():
    a=[]
    for j,yr in enumerate([1998,1999,2000,2001]):
        y=4.0-j*1.0
        a.append(f'\\node[pLabel,anchor=east]at(1.1,{y})'+'{'+str(yr)+'};')
        for k in range(12):
            x=1.55+k*.62
            a.append(f'\\filldraw[fill={"GeoA" if j==0 else "GeoB"}!{18+int(12*math.sin(k/12*math.tau))},draw=Rule]({x},{y-.23})rectangle({x+.5},{y+.23});')
        a.append(f'\\node[pNote,anchor=west]at(9.0,{y})'+'{'+('noto' if j==0 else 'copia')+'};')
    a.append('\\draw[pEdge](8.72,3.65)--(8.72,1.2);')
    return tikz('\n'.join(a),4.65)

def memory(kind='AR'):
    if kind=='AR':
        return boxes([('a',1.4,3.5,r'$X_{t-2}$',2.1,'GeoA'),('b',4.8,3.5,r'$X_{t-1}$',2.1,'GeoA'),
                      ('c',8.2,3.5,r'$X_t$',2.1,'GeoB'),('u',8.2,1.15,r'$\varepsilon_t$',2.1,'GeoC')],
                     [('a','b',r'$\phi$'),('b','c',r'$\phi$'),('u','c','')],4.5)
    return boxes([('a',1.4,3.5,r'$\varepsilon_{t-1}$',2.1,'GeoC'),('b',5.0,3.5,r'$\varepsilon_t$',2.1,'GeoC'),
                  ('c',8.2,1.1,r'$X_t$',2.1,'GeoB')], [('a','c',r'$\theta$'),('b','c','1')],4.5)

def roots(which='AR'):
    # Explicit example, not fitted data: AR polynomial 1-.6z or MA 1+.6z.
    rx=1/.6 if which=='AR' else -1/.6
    body=r'''\draw[pAxis](1,2.5)--(8.5,2.5)node[right,pNote]{Re};
\draw[pAxis](4.7,.35)--(4.7,4.7)node[above,pNote]{Im};
\draw[Classical,line width=1pt](4.7,2.5)circle(1.55);
\node[pNote]at(5.6,3.85){$|z|=1$};'''
    x=4.7+rx*1.55
    body+=f'\\fill[GeoB]({x:.3f},2.5)circle(3.2pt);'
    body+=f'\\node[pLabel]at({x:.3f},1.85)'+'{$z='+('1/0{,}6' if rx>0 else '-1/0{,}6')+'$};'
    return tikz(body,5.1)

def distribution():
    pts=[]
    for j in range(101):
        z=-3.2+j*6.4/100
        pts.append(f'({4.8+z*1.22:.4f},{.8+3.0*math.exp(-z*z/2):.4f})')
    return tikz(r'\draw[pAxis](.5,.8)--(9.3,.8);'+
                r'\fill[GeoA!10](2.408,.8)--'+ ' -- '.join(pt for j,pt in enumerate(pts) if 20<=j<=80)+r'--(7.192,.8)--cycle;'+
                r'\draw[GeoA,line width=1.2pt]plot coordinates{'+ ' '.join(pts)+r'};'+
                r'\draw[GeoB,dashed](4.8,.8)--(4.8,4.0);\node[pLabel]at(4.8,4.4){distribuzione futura};'+
                r'\node[pNote]at(4.8,.3){centro e dispersione sono informazioni diverse};',4.8)

def var_network():
    return tikz(r'''\node[pFlow,text width=2.8cm,fill=GeoA!8](xp)at(2,3.6){$X_{t-1}$};
\node[pFlow,text width=2.8cm,fill=GeoB!8](yp)at(2,1.1){$Y_{t-1}$};
\node[pFlow,text width=2.8cm,fill=GeoA!8](x)at(7.6,3.6){$X_t$};
\node[pFlow,text width=2.8cm,fill=GeoB!8](y)at(7.6,1.1){$Y_t$};
\draw[pEdge](xp)--node[above,pNote]{$a_{11}$}(x);
\draw[pEdge](yp)--node[below,pNote]{$a_{22}$}(y);
\draw[pEdge,GeoC](xp)--node[pos=.25,below,pNote]{$a_{21}$}(y);
\draw[pEdge,GeoC](yp)--node[pos=.25,above,pNote]{$a_{12}$}(x);''',4.6)

def loss():
    a=[r'\draw[pAxis](.5,.7)--(9.2,.7);\draw[pAxis](4.8,.5)--(4.8,4.5);']
    for kind,c in [('abs','GeoA'),('square','GeoB')]:
        pts=[]
        for j in range(81):
            e=-2+j*.05;v=abs(e) if kind=='abs' else e*e
            pts.append(f'({4.8+e*2:.3f},{.7+.8*v:.3f})')
        a.append('\\draw['+c+',line width=1.2pt]plot coordinates{'+' '.join(pts)+'};')
    a += [r'\node[pNote,text=GeoA]at(8,2.0){$|e|$};\node[pNote,text=GeoB]at(8.4,4.1){$e^2$};',
          r'\node[pNote]at(4.8,.15){errore $e$};']
    return tikz('\n'.join(a),4.8)

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
