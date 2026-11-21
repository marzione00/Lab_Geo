"""Diagrammi TikZ per processi, differenze e diagnostica di Borealis."""
import math

def tk(body,w=9.35,h=3.9):
    return r'\begin{tikzpicture}[x=1cm,y=1cm]'+f'\n\\path[use as bounding box](-.1,-.12) rectangle({w},{h});\n'+body+'\n'+r'\end{tikzpicture}'

def node(x,y,label,style='pLabel',extra=''):
    return rf'\node[{style}{","+extra if extra else ""}] at({x},{y}){{{label}}};'

def axis(xmin,xmax,ymin,ymax,w=9.2,h=3.8,xlabel='Ritardo $k$',ylabel='',xticks=None,yticks=None):
    X=lambda x:.9+(float(x)-xmin)/(xmax-xmin)*(w-1.45)
    Y=lambda y:.65+(float(y)-ymin)/(ymax-ymin)*(h-1.2)
    out=rf'\draw[pAxis](.9,.65)--({w-.35},.65);\draw[pAxis](.9,.65)--(.9,{h-.4});'
    for t in ([] if xticks is None else xticks):
        out+=rf'\draw[Muted]({X(t)},.6)--({X(t)},.7);'+node(X(t),.36,f'${t}$','pNote')
    for t in ([] if yticks is None else yticks):
        out+=rf'\draw[Muted](.85,{Y(t)})--(.95,{Y(t)});'+node(.76,Y(t),('$'+str(t).replace('.','{,}')+'$'),'pNote','anchor=east')
    out+=node(w/2,.0,xlabel,'pNote')
    if ylabel:out+=node(.05,(h+.1)/2,ylabel,'pNote','rotate=90')
    return out,X,Y

def line(X,Y,pts,color='GeoA',options='line width=1.2pt'):
    return r'\draw['+color+','+options+'] plot coordinates {'+' '.join(f'({X(x):.5f},{Y(y):.5f})' for x,y in pts)+'};'

def paths(kind='realizations'):
    out=''
    for j in range(3):
        oy=.7+j*.9
        pts=[(.65+i*.17,oy+.24*math.sin(.77*i+j*2)+.13*math.cos(2.2*i-j)) for i in range(49)]
        out+=r'\draw['+['GeoA','GeoB','GeoC'][j]+',line width=.8pt] plot coordinates {'+' '.join(f'({x:.3f},{y:.3f})' for x,y in pts)+'};'
        out+=node(.2,oy,f'${j+1}$','pNote')
    out+=r'\draw[Muted,dashed](5,.35)--(5,3.45);'+node(5,3.65,'Stesso istante, esiti diversi','pNote')
    out+=node(4.7,.08,'Tre traiettorie schematiche dello stesso processo','pNote')
    return tk(out,h=3.9)

def stationarity():
    out=''
    for j,x in enumerate([1.5,4.7,7.9]):
        out+=rf'\draw[GeoA,line width=1.1pt]({x},.8)--({x},2.9);\draw[GeoA]({x-.38},.8)--({x+.38},.8)({x-.38},2.9)--({x+.38},2.9);\fill[GeoA]({x},1.85) circle(3pt);'
        out+=node(x,.4,['$t$','$t+h$','$t+2h$'][j],'pLabel')
    out+=r'\draw[Muted,dashed](.6,1.85)--(8.8,1.85);'+node(4.7,3.55,r'Stessa media e stessa varianza','pLabel')
    out+=node(4.7,.02,r'Le barre rappresentano una scala di dispersione, non intervalli stimati','pNote')
    return tk(out,h=3.8)

def acf_theory(kind='white'):
    out,X,Y=axis(0,12,-.8,1.1,xlabel='Ritardo $k$',ylabel=r'$\rho(k)$',xticks=[0,1,4,8,12],yticks=[-.5,0,1])
    out+=line(X,Y,[(0,0),(12,0)],'Rule','line width=.7pt')
    if kind=='white':vals=[1]+[0]*12
    elif kind=='diff':vals=[1,-.5]+[0]*11
    else:vals=[float(kind)**k for k in range(13)]
    for k,v in enumerate(vals):
        out+=line(X,Y,[(k,0),(k,v)])+rf'\fill[GeoA]({X(k)},{Y(v)}) circle(2pt);'
    out+=node(7.2,3.55,'ACF teorica','pNote')
    return tk(out,h=3.85)

def dependence():
    out=''
    for x,label in [(1.5,r'$U_{t-1}$'),(4.6,r'$U_t$'),(7.7,r'$U_{t+1}$')]:
        out+=node(x,3.15,label,'pFlow','minimum width=1.5cm')
    out+=node(3,1.2,r'$E_t=U_{t-1}U_t$','pFlow','draw=GeoA,minimum width=3cm')
    out+=node(6.4,1.2,r'$E_{t+1}=U_tU_{t+1}$','pFlow','draw=GeoB,minimum width=3cm')
    for x,y in [(1.5,3),(4.6,3),(4.6,6.4),(7.7,6.4)]:out+=rf'\draw[pEdge]({x},2.56)--({y},1.78);'
    out+=node(4.7,.1,r'Il fattore condiviso crea dipendenza','pNote')
    return tk(out,h=3.8)

def ar_recursion():
    out=node(1.4,2.15,r'$X_{t-1}$','pFlow','minimum width=1.8cm')
    out+=node(4.2,2.15,r'$\phi\,X_{t-1}$','pFlow','minimum width=2cm')
    out+=node(7.55,2.15,r'$X_t$','pFlow','minimum width=1.8cm')
    out+=r'\draw[pEdge](2.3,2.15)--(3.18,2.15);\draw[pEdge](5.22,2.15)--(6.63,2.15);'
    out+=node(5.9,3.4,r'$\varepsilon_t$','pLabel')+r'\draw[pEdge,GeoB](5.9,3.05)--(5.9,2.18);'
    out+=node(4.7,.55,r'Parte ereditata dal passato e nuova innovazione','pNote')
    return tk(out,h=3.9)

def impulse(compare=False):
    out,X,Y=axis(0,12,-.1,1.1,xlabel='Passi dopo lo shock',ylabel='Effetto',xticks=[0,3,6,9,12],yticks=[0,1])
    out+=line(X,Y,[(i,.65**i) for i in range(13)])
    for i in range(13):out+=rf'\fill[GeoA]({X(i)},{Y(.65**i)}) circle(2pt);'
    out+=node(6.7,2.0,r'AR(1): $0{,}65^k$','pNote','text=GeoA')
    if compare:
        out+=line(X,Y,[(0,1),(12,1)],'GeoB')+node(6.8,3.5,'Random walk: 1','pNote','text=GeoB')
    return tk(out,h=3.85)

def variance_balance():
    out=node(4.7,3.2,r'$\gamma(0)$','pFlow','minimum width=2.5cm')
    out+=node(2.5,1.3,r'$\phi^2\gamma(0)$','pFlow','draw=GeoA,minimum width=3.1cm')
    out+=node(6.85,1.3,r'$\sigma_\varepsilon^2$','pFlow','draw=GeoB,minimum width=2.8cm')
    out+=r'\draw[pEdge](2.5,1.9)--(3.8,2.6);\draw[pEdge,GeoB](6.85,1.9)--(5.6,2.6);'
    out+=node(4.7,.15,'La varianza ereditata e quella nuova si sommano','pNote')
    return tk(out,h=3.9)

def ar_acfs():
    out,X,Y=axis(0,12,-.8,1.1,xlabel='Ritardo $k$',ylabel=r'$\rho(k)$',xticks=[0,4,8,12],yticks=[-.5,0,1])
    out+=line(X,Y,[(0,0),(12,0)],'Rule','line width=.7pt')
    for phi,col,yy in [(.65,'GeoA',3.5),(-.65,'GeoB',3.12),(.9,'GeoC',2.74)]:
        out+=line(X,Y,[(i,phi**i) for i in range(13)],col)
        out+=node(7.4,yy,r'$\phi='+str(phi).replace('.','{,}')+'$','pNote','text='+col)
    return tk(out,h=3.9)

def initial_variance():
    out,X,Y=axis(0,10,0,2,xlabel='Passi dall’inizializzazione',ylabel='Varianza',xticks=[0,2,6,10],yticks=[0,1,2])
    limit=1/(1-.65**2)
    out+=line(X,Y,[(0,limit),(10,limit)],'GeoB','dashed,line width=1pt')
    out+=line(X,Y,[(i,(1-.65**(2*i))/(1-.65**2)) for i in range(11)])
    out+=node(6.4,3.3,r'$\sigma_\varepsilon^2=1,\quad\phi=0{,}65$','pNote')
    out+=node(6.4,2.6,'Limite stazionario','pNote','text=GeoB')
    return tk(out,h=3.9)

def two_paths():
    e=[math.sin(i*2.4)+.6*math.sin(i*1.37) for i in range(50)]
    a=[0];b=[0]
    for v in e:a.append(.3*a[-1]+v);b.append(.9*b[-1]+v)
    out,X,Y=axis(0,50,-3,3,xlabel='Tempo $t$',ylabel='Valore',xticks=[0,25,50],yticks=[-3,0,3])
    out+=line(X,Y,list(enumerate(a)),'GeoA')+line(X,Y,list(enumerate(b)),'GeoB')
    out+=node(6.7,3.55,r'$\phi=0{,}3$ e $\phi=0{,}9$','pNote')
    return tk(out,h=3.9)

def accumulation():
    out=''
    for i,label in enumerate([r'$X_0$',r'$+\varepsilon_1$',r'$+\varepsilon_2$',r'$+\cdots$',r'$+\varepsilon_t$']):
        x=.9+i*1.85
        out+=node(x,2.2,label,'pFlow','minimum width=1.55cm,draw='+('GeoA' if i==0 else 'GeoB'))
    out+=r'\draw[decorate,decoration={brace,amplitude=5pt,mirror},Muted](.2,1.3)--(9,1.3);'
    out+=node(4.7,.63,r'Ogni innovazione rimane nei livelli successivi','pNote')
    return tk(out,h=3.6)

def rw_variance():
    out,X,Y=axis(0,100,-22,22,xlabel='Tempo $t$',ylabel=r'$X_t-X_0$',xticks=[0,25,50,100],yticks=[-20,0,20])
    pts=[(t,2*math.sqrt(t)) for t in range(101)]
    out+=line(X,Y,pts,'GeoB')+line(X,Y,[(t,-v) for t,v in pts],'GeoB')
    out+=line(X,Y,[(0,0),(100,0)],'Rule','dashed')
    out+=node(6.6,2.1,r'$\pm2\sqrt{t}\,\sigma_\varepsilon$','pLabel')
    return tk(out,h=3.9)

def ensemble():
    out=''
    for j,col in enumerate(['GeoA','GeoB','GeoC','Classical']):
        out+=r'\draw['+col+',line width=.8pt] plot coordinates {'+' '.join(f'({.65+i*.16:.3f},{1.9+.1*j+.45*math.sin(.33*i+j)+.2*math.cos(i*.8+j):.3f})' for i in range(48))+'};'
    out+=r'\draw[Muted,dashed](6.4,.4)--(6.4,3.4);'
    out+=node(6.4,3.7,r'Confronto tra repliche a $t$ fissato','pNote')
    out+=node(4.6,.08,'Schema: una linea del tempo per ciascuna replica','pNote')
    return tk(out,h=3.95)

def trend_comparison():
    out=''
    for j,label in enumerate(['Trend deterministico','Accumulo degli shock']):
        ox=.5+4.6*j
        out+=node(ox+2.05,3.75,label,'pLabel')
        out+=rf'\draw[pAxis]({ox},.6)--({ox+4.05},.6);'
        if j==0:
            pts=[(ox+i*.075,.85+i*.043+.22*math.sin(i*1.9)) for i in range(51)]
            out+=rf'\draw[GeoB,dashed]({ox},.85)--({ox+3.75},3);'
        else:
            x=1.6;pts=[]
            for i in range(51):
                x+=.115*math.sin(i*.38)+.09*math.cos(i*1.13);pts.append((ox+i*.075,x))
        out+=r'\draw[GeoA,line width=.9pt] plot coordinates {'+' '.join(f'({x:.3f},{y:.3f})' for x,y in pts)+'};'
    out+=node(4.7,.1,'Traiettorie schematiche: un andamento crescente non identifica il modello','pNote')
    return tk(out,h=4.0)

def detrending():
    out,X,Y=axis(0,12,-1,8,xlabel='Tempo $t$',ylabel='Valore',xticks=[0,6,12],yticks=[0,4,8])
    vals=[1+.45*i+.6*math.sin(i*1.7) for i in range(13)]
    out+=line(X,Y,list(enumerate(vals)),'GeoA')+line(X,Y,[(0,1),(12,6.4)],'GeoB')
    for i in [2,5,8,11]:out+=line(X,Y,[(i,1+.45*i),(i,vals[i])],'GeoC','line width=1.3pt')
    out+=node(6.3,3.6,'Schema: scarti rispetto alla retta','pNote')
    return tk(out,h=3.9)

def difference(lag=1,combined=False):
    if combined:
        vals=[(0,'$t-13$','+1','GeoA'),(3,'$t-12$','−1','GeoB'),(6,'$t-1$','−1','GeoB'),(9,'$t$','+1','GeoA')]
        out=''
        for x,label,c,col in vals:
            xx=.6+x*.88
            out+=node(xx,2.65,label,'pNote')+node(xx,1.65,c,'pFlow',f'draw={col},text={col},minimum width=1.4cm')
        out+=node(4.6,.45,'Quattro date, quattro coefficienti','pNote')
    else:
        out=''
        n=7 if lag==1 else 13
        for i in range(n):
            x=.55+i*8.1/(n-1)
            out+=rf'\fill[Rule]({x},1.55) circle(2pt);'
        x1=7.3 if lag==1 else .55;x2=8.65
        out+=rf'\draw[pEdge,GeoB]({x1},2.35)--({x2},2.35);'
        out+=node(x1,1.08,r'$X_{t-'+str(lag)+'}$','pLabel')+node(x2,1.08,r'$X_t$','pLabel')
        out+=node((x1+x2)/2,2.85,f'{lag} passo' if lag==1 else '12 mesi','pNote')
        out+=node(4.7,.2,'La differenza conserva il tempo del valore più recente','pNote')
    return tk(out,h=3.4)

def month_calendar(drop=1):
    out=''
    labs=['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic']
    for i in range(12):
        x=.45+i*.74
        col='GeoB' if i<drop else 'GeoA'
        out+=rf'\filldraw[fill={col}!13,draw={col}!55]({x},1.45) rectangle({x+.62},2.15);'
        out+=node(x+.31,1.8,str(i+1),'pNote')+node(x+.31,.95,labs[i],'pNote')
    out+=node(4.7,2.85,'Anno iniziale della serie','pLabel')
    out+=node(4.7,.2,'Le posizioni eliminate restano documentate nel calendario','pNote')
    return tk(out,h=3.5)

def lag_operator():
    out=node(1.5,2.2,r'$X_t$','pFlow','minimum width=2cm')
    out+=node(4.7,2.2,r'$B$','pFlow','draw=GeoB,minimum width=1.4cm')
    out+=node(7.9,2.2,r'$X_{t-1}$','pFlow','minimum width=2cm')
    out+=r'\draw[pEdge](2.55,2.2)--(3.95,2.2);\draw[pEdge](5.45,2.2)--(6.85,2.2);'
    out+=node(4.7,.7,r'$B^{12}X_t=X_{t-12}$','pLabel')
    return tk(out,h=3.5)

def losses():
    out=''
    for i,(label,loss,n,col) in enumerate([('Livelli',0,204,'GeoA'),('Differenza ordinaria',1,203,'GeoB'),('Differenza stagionale',12,192,'GeoC'),('Differenza combinata',13,191,'Classical')]):
        yy=3.25-i*.78
        out+=node(.2,yy,label,'pNote','anchor=west')
        out+=rf'\fill[{col}!25](4.15,{yy-.18}) rectangle({4.15+4.2*n/204},{yy+.18});'
        out+=node(8.75,yy,str(n),'pLabel')
    out+=node(4.7,.05,'Serie completa: gennaio 1985–dicembre 2001','pNote')
    return tk(out,h=3.8)

def reconstruction():
    out=node(1.8,2.5,r'Valore iniziale\\$X_1$','pFlow','minimum width=2.6cm')
    out+=node(5,2.5,r'Incrementi\\$\Delta X_2,\ldots,\Delta X_n$','pFlow','minimum width=3.2cm')
    out+=node(4.7,.7,r'Livelli ricostruiti: $X_t=X_1+\sum_{j=2}^t\Delta X_j$','pFlow','minimum width=8.5cm')
    out+=r'\draw[pEdge](1.8,1.85)--(3.4,1.3);\draw[pEdge](5,1.85)--(5,1.3);'
    return tk(out,h=3.6)

def shared_noise():
    out=''
    for x,l in [(1.5,r'$\varepsilon_{t-1}$'),(4.7,r'$\varepsilon_t$'),(7.9,r'$\varepsilon_{t+1}$')]:out+=node(x,3.1,l,'pFlow','minimum width=2cm')
    out+=node(2.8,1.2,r'$D_t=\varepsilon_t-\varepsilon_{t-1}$','pFlow','minimum width=3.6cm,draw=GeoA')
    out+=node(6.8,1.2,r'$D_{t+1}=\varepsilon_{t+1}-\varepsilon_t$','pFlow','minimum width=3.9cm,draw=GeoB')
    out+=r'\draw[pEdge,GeoA](4.5,2.5)--(3.5,1.8);\draw[pEdge,GeoB](4.9,2.5)--(6.1,1.8);'
    out+=node(3.6,2.4,'$+$','pLabel','text=GeoA')+node(5.9,2.4,'$-$','pLabel','text=GeoB')
    out+=node(4.7,.1,'La stessa innovazione compare con segni opposti','pNote')
    return tk(out,h=3.9)

def two_acfs():
    out,X,Y=axis(0,8,-.7,1.1,xlabel='Ritardo $k$',ylabel=r'$\rho(k)$',xticks=[0,1,4,8],yticks=[-.5,0,1])
    out+=line(X,Y,[(0,0),(8,0)],'Rule','line width=.7pt')
    for vals,col in [([1,-.5]+[0]*7,'GeoA'),([(-.5)**k for k in range(9)],'GeoB')]:
        out+=line(X,Y,list(enumerate(vals)),col)
        for k,v in enumerate(vals):out+=rf'\fill[{col}]({X(k)},{Y(v)}) circle(2pt);'
    out+=node(6.9,3.35,'Rumore differenziato','pNote','text=GeoA')+node(6.9,2.97,r'AR(1), $\phi=-0{,}5$','pNote','text=GeoB')
    return tk(out,h=3.9)

def register():
    out=''
    labs=[r'Originale\\date e unità',r'Trasformazione\\formula e parametri',r'Risultato\\date rimaste']
    for i,l in enumerate(labs):
        x=1.65+3.05*i;out+=node(x,2.55,l,'pFlow','text width=2.5cm,minimum height=1.25cm')
        if i<2:out+=rf'\draw[pEdge]({x+1.3},2.55)--({x+1.72},2.55);'
    out+=node(4.7,.7,r'Archivio originale e passaggi di calcolo restano disponibili','pNote')
    return tk(out,h=3.8)

def nulls():
    out=node(2.45,2.45,r'ADF\\$H_0$: radice unitaria','pFlow','text width=3.7cm,minimum height=1.5cm,draw=GeoA')
    out+=node(6.95,2.45,r'KPSS\\$H_0$: stazionarietà','pFlow','text width=3.7cm,minimum height=1.5cm,draw=GeoB')
    out+=node(4.7,.65,r'La specificazione determina il significato di ciascuna ipotesi','pNote')
    return tk(out,h=3.8)

def adf_design():
    out=''
    labs=[r'Livello passato\\$X_{t-1}$',r'Termini deterministici\\$1,\ t$',r'Differenze passate\\$\Delta X_{t-j}$']
    for i,l in enumerate(labs):out+=node(1.65+3.05*i,2.7,l,'pFlow','text width=2.5cm,minimum height=1.3cm')
    out+=node(4.7,.65,r'Risposta della regressione: $\Delta X_t$','pFlow','minimum width=6cm,draw=GeoB')
    for x in [1.65,4.7,7.75]:out+=rf'\draw[pEdge]({x},2.02)--(4.7,1.25);'
    return tk(out,h=3.8)

def deterministic_terms():
    out=''
    for j,label in enumerate(['Solo livello','Livello e trend']):
        ox=.4+j*4.65;out+=node(ox+2.05,3.25,label,'pLabel')
        pts=[]
        for i in range(35):pts.append((ox+i*.115,1.6+.18*math.sin(2*i)+(.034*i if j else 0)))
        out+=r'\draw[GeoA,line width=.8pt] plot coordinates {'+' '.join(f'({x:.3f},{y:.3f})' for x,y in pts)+'};'
        out+=rf'\draw[GeoB,dashed]({ox},1.6)--({ox+3.9},{2.75 if j else 1.6});'
    out+=node(4.7,.4,'Schema: cambia la componente rispetto a cui si studiano gli scarti','pNote')
    return tk(out,h=3.65)

def lag_regression():
    out=''
    for j,label in enumerate([r'$\Delta X_{t-1}$',r'$\Delta X_{t-2}$',r'$\cdots$',r'$\Delta X_{t-p}$']):
        out+=node(1.2+2.3*j,2.4,label,'pFlow','minimum width=1.85cm')
    out+=node(4.7,.7,r'Le differenze passate descrivono parte della dinamica di breve periodo','pNote')
    return tk(out,h=3.65)

def kpss_sums():
    out,X,Y=axis(0,40,-6,6,xlabel='Indice $t$',ylabel=r'$S_t=\sum_{j\leq t} e_j$',xticks=[0,20,40],yticks=[-5,0,5])
    es=[math.sin(i*.9)+.6*math.cos(i*.32) for i in range(1,41)];mean=sum(es)/len(es)
    sums=[0];
    for e in es:sums.append(sums[-1]+e-mean)
    out+=line(X,Y,list(enumerate(sums)),'GeoA')
    out+=line(X,Y,[(0,0),(40,0)],'Rule','dashed')
    out+=node(6.8,3.5,'Residui illustrativi','pNote')
    return tk(out,h=3.9)

def bartlett():
    out,X,Y=axis(0,5,0,1.1,xlabel='Ritardo $j$',ylabel='Peso',xticks=[0,1,2,3,4,5],yticks=[0,.5,1])
    for j in range(5):
        weight=1-j/5
        out+=line(X,Y,[(j,0),(j,weight)],'GeoA','line width=2pt')
        out+=rf'\fill[GeoA]({X(j)},{Y(weight)}) circle(2pt);'
    out+=node(6.4,3.45,r'$L=4,\quad w_j=1-j/(L+1)$','pNote')
    return tk(out,h=3.9)

def decisions():
    out=node(6,3.8,'KPSS','pLabel')+node(4.2,3.28,'Non rifiuta','pNote')+node(7.1,3.28,'Rifiuta','pNote')
    for x,yy,col in [(3,1.6,'GeoA'),(6,1.6,'GeoB'),(3,.2,'GeoC'),(6,.2,'Muted')]:out+=rf'\filldraw[fill={col}!9,draw=Rule]({x},{yy}) rectangle({x+2.85},{yy+1.3});'
    out+=node(1.35,2.25,'ADF rifiuta','pNote')+node(1.35,.85,'ADF non rifiuta','pNote')
    out+=node(4.4,2.25,r'Compatibile con\\stazionarietà','pNote')
    out+=node(7.4,2.25,r'Specificazione\\da riesaminare','pNote')
    out+=node(4.4,.85,r'Evidenza\\poco discriminante','pNote')
    out+=node(7.4,.85,r'Compatibile con\\radice unitaria','pNote')
    return tk(out,h=4.05)

def p_bounds():
    out=r'\draw[pAxis](1,1.4)--(8.7,1.4);'
    for x,label in [(1.7,'0,01'),(4.3666667,'0,05'),(7.7,'0,10')]:
        out+=rf'\draw[Muted]({x},1.3)--({x},1.5);'+node(x,1.0,label,'pNote')
    out+=r'\draw[pEdge,GeoA](1.7,2.25)--(.8,2.25);\draw[pEdge,GeoB](7.7,2.25)--(8.7,2.25);'
    out+=node(2.5,3.05,r'$p<0{,}01$ se segnalato','pLabel','text=GeoA')+node(6.7,3.05,r'$p>0{,}10$ se segnalato','pLabel','text=GeoB')
    out+=node(4.7,.35,'I limiti dipendono dalla tabella del test utilizzato','pNote')
    return tk(out,h=3.65)

def mc_reference():
    out=node(2.3,2.7,r'ADF semplificato\\riferimento: random walk','pFlow','text width=3.7cm,minimum height=1.5cm,draw=GeoA')
    out+=node(7,2.7,r'KPSS semplificato\\riferimento: rumore IID','pFlow','text width=3.7cm,minimum height=1.5cm,draw=GeoB')
    out+=node(4.7,.65,r'La simulazione dichiara un generatore nullo preciso','pNote')
    return tk(out,h=3.9)

def break_series():
    out,X,Y=axis(1,80,-2,4,xlabel='Tempo $t$',ylabel='Valore',xticks=[1,40,80],yticks=[-2,0,2,4])
    pts=[(i,.5*math.sin(i*1.83)+(.0 if i<=40 else 2.)) for i in range(1,81)]
    out+=line(X,Y,pts,'GeoA')+line(X,Y,[(40,-2),(40,4)],'GeoB','dashed')
    out+=node(3.0,3.5,'Prima della discontinuità','pNote')+node(7.1,3.5,'Dopo','pNote')
    return tk(out,h=3.9)

def evidence():
    out=''
    labs=[('Calendario',1.65,2.85),('Grafici e ACF',4.7,2.85),('Test dichiarati',7.75,2.85)]
    for label,x,yy in labs:
        out+=node(x,yy,label,'pFlow','text width=2.4cm')
        out+=rf'\draw[pEdge]({x},2.25)--(4.7,1.3);'
    out+=node(4.7,.7,r'Conclusione circoscritta ai dati e al modello','pFlow','minimum width=8.3cm,draw=GeoB')
    return tk(out,h=3.8)
