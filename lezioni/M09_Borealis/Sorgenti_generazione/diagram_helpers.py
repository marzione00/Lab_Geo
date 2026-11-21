from pathlib import Path
import csv, json, math, random, statistics
ROOT=Path(__file__).resolve().parent
MODULE=ROOT.parent if ROOT.name=='Sorgenti_generazione' else ROOT/'Borealis_M09'
def rows(name,calc=False):
    return list(csv.DictReader((MODULE/('Calcoli' if calc else 'Dati')/name).open()))
WK=rows('co2_settimanale_storica.csv')
MON=rows('co2_mensile_derivata.csv')
CO2=rows('co2_1985_2001.csv')
TEMP=rows('temperatura_simulata.csv')
for i,r in enumerate(TEMP): r['tempo0']=i
PROC=rows('processi_simulati.csv')
def val(s):
    try:return float(s)
    except (TypeError,ValueError):return math.nan
def it(x,d=2):return f'{float(x):.{d}f}'.replace('.','{,}')
def texnum(x):
    return format(float(x),'.5g').replace('.','{,}')
def tk(body,w=9.4,h=4.5):
    return r'\begin{tikzpicture}[x=1cm,y=1cm]'+f'\n\\path[use as bounding box](-.15,-.15) rectangle({w},{h});\n'+body+'\n'+r'\end{tikzpicture}'
def axes(xmin=0,xmax=10,ymin=0,ymax=10,xlabel='Tempo',ylabel='',w=9.2,h=4.4,xticks=None,yticks=None):
    ox=.92;oy=.68;iw=w-1.25;ih=h-1.13
    X=lambda x:ox+(float(x)-xmin)/(xmax-xmin)*iw
    Y=lambda y:oy+(float(y)-ymin)/(ymax-ymin)*ih
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]',rf'\path[use as bounding box](-.3,-.2) rectangle({w+.1},{h+.1});',
         rf'\draw[pAxis]({ox},{oy})--({ox+iw+.10},{oy});',rf'\draw[pAxis]({ox},{oy})--({ox},{oy+ih+.10});']
    if xticks is None:xticks=[xmin,(xmin+xmax)/2,xmax]
    if yticks is None:yticks=[ymin,(ymin+ymax)/2,ymax]
    for tick in xticks:
        t,label=tick if isinstance(tick,tuple) else (tick,'$'+texnum(tick)+'$')
        out.append(rf'\draw[Muted]({X(t):.4f},{oy-.05})--({X(t):.4f},{oy+.05});\node[pNote] at({X(t):.4f},{oy-.25}){{{label}}};')
    for tick in yticks:
        t,label=tick if isinstance(tick,tuple) else (tick,'$'+texnum(tick)+'$')
        out.append(rf'\draw[Muted]({ox-.05},{Y(t):.4f})--({ox+.05},{Y(t):.4f});\node[pNote,anchor=east] at({ox-.12},{Y(t):.4f}){{{label}}};')
    out.append(rf'\node[pNote] at({ox+iw/2},{oy-.59}){{{xlabel}}};')
    if ylabel:out.append(rf'\node[pNote,rotate=90] at(-.3,{oy+ih/2}){{{ylabel}}};')
    return out,X,Y
def line(out,X,Y,points,color='Classical',options='line width=1.0pt'):
    segments=[];seg=[]
    for x,y in points:
        if not math.isfinite(val(x)) or not math.isfinite(val(y)):
            if seg:segments.append(seg);seg=[]
        else:seg.append((float(x),float(y)))
    if seg:segments.append(seg)
    for seg in segments:
        out.append(r'\draw['+color+','+options+'] plot coordinates {'+' '.join(f'({X(x):.4f},{Y(y):.4f})' for x,y in seg)+'};')
def finish(out):return '\n'.join(out+[r'\end{tikzpicture}'])
def plot_series(data,columns,xcol=None,xlabel='Mese',ylabel='',colors=None,h=4.4,w=9.2,yrange=None,legend=True,xticks=None):
    colors=colors or ['GeoA','GeoB','GeoC','Muted']
    xx=[val(r[xcol]) if xcol else i+1 for i,r in enumerate(data)]
    yy=[val(r[c]) for r in data for c in columns if math.isfinite(val(r.get(c)))]
    lo,hi=yrange or (min(yy),max(yy))
    margin=(hi-lo)*.09 or .5
    out,X,Y=axes(min(xx),max(xx),lo-margin,hi+margin,xlabel,ylabel,w,h,xticks,[(lo,'$'+texnum(lo)+'$'),(hi,'$'+texnum(hi)+'$')])
    for k,c in enumerate(columns):
        line(out,X,Y,[(x,val(r.get(c))) for x,r in zip(xx,data)],colors[k%len(colors)])
    return finish(out)
def order_pair():
    a=[math.sin(i*.35)+i*.026 for i in range(36)]
    b=a.copy();random.Random(109).shuffle(b)
    body=''
    for q,v in enumerate([a,b]):
        x0=.4+q*4.7
        body+=rf'\node[pLabel] at({x0+2},4.0){{'+('Ordine temporale' if q==0 else 'Ordine rimescolato')+'};'
        body+=rf'\draw[pAxis]({x0},.8)--({x0+4},.8);'
        pts=' '.join(f'({x0+3.8*i/35:.3f},{1+2.3*(y-min(a))/(max(a)-min(a)):.3f})' for i,y in enumerate(v))
        body+=r'\draw['+('GeoA' if q==0 else 'GeoB')+r',line width=1.1pt] plot coordinates {'+pts+'};'
        body+=rf'\node[pNote] at({x0+2},.35){{'+('tempo' if q==0 else 'posizione nella permutazione')+'};'
    body+=r'\node[pNote] at(4.5,4.65){Gli stessi 36 valori, con la stessa media e lo stesso istogramma};'
    return tk(body,h=4.9)
def calendar(missing=True,compact=False):
    names=['gen','feb','mar','apr','mag','giu','lug','ago']
    body=''
    for j,n in enumerate(names):
        if compact and j==3:continue
        x=.65+(j-(1 if compact and j>3 else 0))*1.08
        fill='GeoB!12' if j==3 and missing else 'GeoA!10'
        body+=rf'\filldraw[fill={fill},draw=Rule,rounded corners=1mm]({x-.45},1.4)rectangle({x+.45},2.7);\node[pLabel] at({x},2.3){{{n}}};\node[pNote] at({x},1.8){{'+('NA' if j==3 and missing else str([5,7,6,8,9,7,6,4][j]))+'};'
    body+=r'\node[pNote] at(4.5,.6){'+('Eliminare aprile rende vicini marzo e maggio' if compact else 'Ogni mese conserva una posizione nella griglia')+'};'
    return tk(body,h=3.3)
def time_pairs():
    body=r'\draw[pAxis](.4,.8)--(9,.8);'
    for i,(x,label,v) in enumerate([(1,'1 marzo','8,2'),(3,'3 marzo','8,5'),(7,'7 marzo','9,1')]):
        body+=rf'\draw[GeoA]({x},.7)--({x},1.1);\fill[GeoA]({x},1.2)circle(3pt);\node[pLabel] at({x},1.75){{$x_{i+1}={v}$}};\node[pNote] at({x},.4){{{label}}};'
    body+=r'\draw[decorate,decoration={brace,amplitude=4pt},GeoB](1,2.7)--(3,2.7);\node[pNote] at(2,3.15){2 giorni};\draw[decorate,decoration={brace,amplitude=4pt},GeoB](3,2.7)--(7,2.7);\node[pNote] at(5,3.15){4 giorni};'
    return tk(body,h=3.8)
def provenance():
    body=''
    labels=[r'Osservatorio\\Mauna Loa',r'Archivio storico\\distribuito con statsmodels',r'Medie settimanali\\copia del corso',r'Medie mensili\\aggregazione locale']
    for i,l in enumerate(labels):
        x=2.3 if i%2==0 else 7.05;y=3.6 if i<2 else 1.45
        body+=rf'\node[pFlow,text width=3.7cm,minimum height=1.15cm] (p{i}) at({x},{y}){{{l}}};'
    body+=r'\draw[pEdge](p0.east)--(p1.west);\draw[pEdge](p1.south)--(7.05,2.5)--(2.3,2.5)--(p2.north);\draw[pEdge](p2.east)--(p3.west);'
    return tk(body,h=4.5)
def source_table(data,n=5,cols=None):
    cols=cols or ['data','co2_ppm','n_settimane']
    body=r'\node[pLabel,anchor=west] at(.3,3.8){Data};\node[pLabel] at(4.9,3.8){CO$_2$ (ppm)};\node[pLabel] at(7.8,3.8){Settimane};'
    for i,r in enumerate(data[:n]):
        y=3.15-.57*i
        body+=rf'\fill[GeoA!{5 if i%2 else 10}](.15,{y-.24}) rectangle(9.05,{y+.24});\node[pNote,anchor=west] at(.3,{y}){{{r[cols[0]]}}};\node[pNote,text=Ink] at(4.9,{y}){{$ {it(r[cols[1]],3)} $}};'
        if len(cols)>2:body+=rf'\node[pNote,text=Ink] at(7.8,{y}){{{r[cols[2]]}}};'
    return tk(body,h=4.2)
def columns_bars(values,labels,colors=None,ylabel='',h=4.4):
    colors=colors or ['GeoA']*len(values)
    top=max(values)*1.15 or 1
    out,X,Y=axes(0,len(values)+1,0,top,'',ylabel,h=h,xticks=[],yticks=[0,max(values)])
    for i,(v,l,c) in enumerate(zip(values,labels,colors)):
        x=X(i+1)
        out.append(rf'\fill[{c}!70]({x-.32},{Y(0):.4f})rectangle({x+.32},{Y(v):.4f});\node[pNote] at({x},{Y(v)+.22:.4f}){{$ {texnum(v)} $}};\node[pNote] at({x},.32){{{l}}};')
    return finish(out)
def coverage():
    counts={n:sum(int(r['n_settimane'])==n for r in MON) for n in range(6)}
    return columns_bars(list(counts.values()),[str(n) for n in counts],['GeoB' if n<3 else 'GeoA' for n in counts],ylabel='Numero di mesi')
def month_weights():
    body=''
    for g,n in enumerate([2,8]):
        x=.6+g*4.7
        body+=rf'\node[pLabel] at({x+1.8},4.1){{'+('Periodo A: 2 misure' if g==0 else 'Periodo B: 8 misure')+'};'
        for j in range(n):body+=rf'\fill[{"GeoA" if g==0 else "GeoB"}]({x+(j%4)*.8},{2.4+(j//4)*.7})circle(6pt);'
        body+=rf'\node[pLabel] at({x+1.7},1.5){{$\bar x_{"A" if g==0 else "B"}={10 if g==0 else 20}$}};'
    body+=r'\node[pNote] at(4.6,.55){Ogni punto pesa allo stesso modo nella media delle dieci misure};'
    return tk(body,h=4.5)
def interval_weights():
    body=''
    for j,(start,end,label,c) in enumerate([(0,1,'10','GeoA'),(1,4,'20','GeoB')]):
        x=.7+start*2
        level=1.9+j*.9
        body+=rf'\fill[{c}!14]({x},1.4)rectangle({.7+end*2},{level});\draw[{c},line width=2pt]({x},{level})--({.7+end*2},{level});\node[pLabel] at({.7+(start+end)},{level+.35}){{$x={label}$}};'
    body+=r'\draw[pAxis](.7,1.3)--(9,1.3);\node[pNote] at(.7,.9){0};\node[pNote] at(2.7,.9){1};\node[pNote] at(8.7,.9){4};\node[pNote] at(4.5,.35){Durata (ore), valori costanti entro ogni intervallo};'
    return tk(body,h=3.8)
def aliasing():
    out,X,Y=axes(0,6,-1.2,1.2,'Tempo (unità)','Segnale',h=4.4,xticks=list(range(7)),yticks=[-1,0,1])
    line(out,X,Y,[(i/40,math.cos(2*math.pi*i/40)) for i in range(241)],'GeoA')
    line(out,X,Y,[(0,1),(6,1)],'GeoB','dashed,line width=1.2pt')
    for i in range(7):out.append(rf'\fill[Ink]({X(i):.4f},{Y(1):.4f})circle(2.8pt);')
    out.append(r'\node[pNote,fill=Paper] at(4.9,1.1){Campioni interi: tutti uguali a 1};')
    return finish(out)
def aggregate_signal():
    a=[math.sin(2*math.pi*t/12)+.35*math.sin(2*math.pi*t/3) for t in range(1,49)]
    out,X,Y=axes(1,48,-1.5,1.5,'Mese','Segnale',h=4.3,xticks=[1,12,24,36,48],yticks=[-1,0,1])
    line(out,X,Y,enumerate(a,1),'Muted','line width=.65pt')
    for q,c in [(3,'GeoA'),(12,'GeoB')]:
        pts=[(i+(q+1)/2,sum(a[i:i+q])/q) for i in range(0,len(a),q)]
        line(out,X,Y,pts,c,'line width=1.5pt')
    out.append(r'\node[pNote,fill=Paper] at(5,3.9){Grigio: mensile. Blu: 3 mesi. Rame: 12 mesi.};')
    return finish(out)
def window_diagram(past=False,edges=False):
    body=''
    idx=list(range(-4,5))
    selected=range(-4,1) if past else range(-2,3)
    for j,k in enumerate(idx):
        x=.6+j*1.03;c='GeoB' if k>0 else 'GeoA'
        if k in selected:body+=rf'\fill[{c}!13]({x-.43},1.3)rectangle({x+.43},3.1);'
        body+=rf'\fill[{c}]({x},2.05)circle(3pt);\node[pNote] at({x},1){{$'+('t' if k==0 else 't'+('+' if k>0 else '')+str(k))+'$};'
        if k in selected:body+=rf'\node[pNote] at({x},2.65){{$1/5$}};'
    body+=r'\draw[Ink,dashed](4.72,.6)--(4.72,3.5);\node[pLabel] at(4.7,4){'+('Cinque valori già disponibili' if past else 'Due valori sono successivi a $t$')+'};'
    return tk(body,h=4.4)
def edge_window():
    body=''
    for j in range(9):
        x=.65+j
        present=j>=2
        body+=rf'\filldraw[fill={"GeoA!15" if present else "Paper"},draw={"GeoA" if present else "GeoB"},dashed]({x-.4},1.6)rectangle({x+.4},2.6);\node[pNote] at({x},2.1){{'+(str(j-1) if present else '?')+'};'
    body+=r'\draw[GeoB,line width=1.1pt,rounded corners=1mm](.2,1.4)rectangle(5.1,2.8);\node[pLabel] at(4.6,3.5){Finestra centrata sul primo valore};\node[pNote] at(4.5,.8){Due vicini precedenti sono fuori dall’archivio};'
    return tk(body,h=4.1)
def component_chart():
    out,X,Y=axes(0,59,-10,23,'Mese da gennaio 2000',r'Temperatura ($^\circ$C)',h=4.5,xticks=[0,12,24,36,48,59],yticks=[-8,0,12,20])
    for c,color in [('temperatura_C','Muted'),('trend_simulato','GeoB'),('stagione_simulata','GeoA')]:
        line(out,X,Y,[(i,val(r[c])) for i,r in enumerate(TEMP[:60])],color)
    out.append(r'\node[pNote,fill=Paper] at(4.9,4.4){Osservata (grigio), trend (rame), stagione (blu)};')
    return finish(out)
def seasonal_overlay():
    out,X,Y=axes(1,12,340,375,'Mese',r'CO$_2$ (ppm)',h=4.4,xticks=[1,4,7,10,12],yticks=[340,350,360,370])
    for year,color in [(1985,'GeoA'),(1992,'GeoB'),(2001,'GeoC')]:
        vals=[r for r in CO2 if r['data'].startswith(str(year))]
        line(out,X,Y,[(j+1,val(r['co2_ppm'])) for j,r in enumerate(vals)],color)
    out.append(r'\node[pNote,fill=Paper] at(4.9,4.05){1985: blu. 1992: rame. 2001: viola.};')
    return finish(out)
def local_fit():
    out,X,Y=axes(0,10,0,10,'Tempo','Valore',h=4.2,xticks=[0,5,10],yticks=[0,5,10])
    for j in range(41):
        t=j/4;y=.6*t+1.4+math.sin(j*1.89)*.7
        col='GeoA' if 3.5<=t<=6.5 else 'Rule'
        out.append(rf'\fill[{col}]({X(t):.3f},{Y(y):.3f})circle(2pt);')
    line(out,X,Y,[(3.5,3.5),(6.5,5.3)],'GeoB','line width=1.6pt')
    out.append(rf'\draw[GeoA,dashed]({X(5):.3f},{Y(0):.3f})--({X(5):.3f},{Y(6):.3f});')
    return finish(out)
def median_outlier():
    a=[0,.2,-.1,.1,6,-.1,.2,0,.1]
    b=[math.nan]+[statistics.mean(a[i-1:i+2]) for i in range(1,8)]+[math.nan]
    c=[a[0]]+[statistics.median(a[i-1:i+2]) for i in range(1,8)]+[a[-1]]
    out,X,Y=axes(1,9,-.5,6.5,'Posizione','Valore',h=4.4,xticks=[1,3,5,7,9],yticks=[0,3,6])
    line(out,X,Y,enumerate(a,1),'Muted');line(out,X,Y,enumerate(b,1),'GeoB');line(out,X,Y,enumerate(c,1),'GeoA')
    out.append(r'\node[pNote,fill=Paper] at(5,4.0){Finestra 3: media (rame), mediana (blu)};')
    return finish(out)
def anomaly_plot():
    baseline=[r for r in TEMP if '2000'<=r['data'][:4]<='2004']
    means={m:statistics.mean(val(r['temperatura_C']) for r in baseline if r['data'][5:7]==f'{m:02}') for m in range(1,13)}
    a=[{'i':i,'anom':val(r['temperatura_C'])-means[int(r['data'][5:7])]} for i,r in enumerate(TEMP)]
    return plot_series(a,['anom'],'i',xlabel='Mese da gennaio 2000',ylabel=r'Anomalia ($^\circ$C)',h=4.4)
def lag_pairs(k=1):
    body=''
    for row in range(2):
        for j in range(7):
            x=.55+j*1.28;y=3.0-row*1.75
            lab='t'+(f'+{j}' if j else '')+(f'-{k}' if row else '')
            body+=rf'\filldraw[fill={"GeoA" if row==0 else "GeoB"}!12,draw=Rule,rounded corners=1mm]({x-.42},{y-.36})rectangle({x+.42},{y+.36});\node[pNote] at({x},{y}){{$x_{{{lab}}}$}};'
            if row==0:body+=rf'\draw[pEdge]({x},{y-.48})--({x},{y-1.22});'
    body+=rf'\node[pNote] at(4.4,.42){{Ogni coppia confronta valori distanti {k} '+('passo' if k==1 else 'mesi')+'};'
    return tk(body,h=3.8)
def lag_scatter(k=1,col='ar1'):
    a=[val(r[col]) for r in PROC]
    hi=max(a);lo=min(a);d=(hi-lo)*.08
    out,X,Y=axes(lo-d,hi+d,lo-d,hi+d,rf'$x_{{t-{k}}}$',r'$x_t$',h=4.6,xticks=[round(lo),0,round(hi)],yticks=[round(lo),0,round(hi)])
    for u,v in zip(a[:-k],a[k:]):out.append(rf'\fill[GeoA,opacity=.65]({X(u):.4f},{Y(v):.4f})circle(1.5pt);')
    return finish(out)
def acf_values(a,maxlag=24):
    a=[val(v) for v in a];mu=statistics.mean(a);z=[x-mu for x in a];den=sum(x*x for x in z)
    return [sum(z[t]*z[t-k] for t in range(k,len(z)))/den for k in range(maxlag+1)]
def acf_chart(a=None,values=None,maxlag=24,bands=True,title=None,w=9.2,h=4.4,colors=None):
    values=values if values is not None else acf_values(a,maxlag)
    out,X,Y=axes(0,maxlag+.5,-1.05,1.08,'Ritardo (passi)',r'$\widehat\rho(k)$',w,h,xticks=[0,6,12,18,24] if maxlag==24 else list(range(0,maxlag+1,2)),yticks=[-1,0,1])
    line(out,X,Y,[(0,0),(maxlag+.2,0)],'Rule')
    if bands and a:
        band=1.96/math.sqrt(len(a))
        for s in [-1,1]:line(out,X,Y,[(0,s*band),(maxlag+.2,s*band)],'GeoB','dashed,line width=.6pt')
    for i,y in enumerate(values):
        color=(colors or {}).get(i,'GeoA')
        out.append(rf'\draw[{color},line width=1.6pt]({X(i):.4f},{Y(0):.4f})--({X(i):.4f},{Y(y):.4f});')
    if title:out.append(rf'\node[pNote,fill=Paper] at(5,{h-.1}){{{title}}};')
    return finish(out)
def covariance_products():
    a=[-2,-1,0,2,1];body=''
    for j,(x,z) in enumerate(zip(a[:-1],a[1:])):
        c='GeoA' if x*z>=0 else 'GeoB'
        body+=rf'\node[pFlow,draw={c},text width=1.65cm,minimum height=1.4cm] at({1.2+j*2.25},2.7){{$({x})({z})$\\[2mm]$={x*z}$}};'
    body+=r'\node[pLabel] at(4.7,.9){Somma al ritardo 1: $2+0+0+2=4$};'
    return tk(body,h=4)
def pacf_chain():
    body=r'\node[pFlow,text width=1.7cm](a)at(1.4,2.5){$X_{t-2}$};\node[pFlow,text width=1.7cm](b)at(4.7,2.5){$X_{t-1}$};\node[pFlow,text width=1.7cm](c)at(8,2.5){$X_t$};\draw[pEdge](a)--(b);\draw[pEdge](b)--(c);\node[pNote,text width=8cm]at(4.7,.9){La PACF a ritardo 2 considera la relazione rimasta dopo aver rimosso linearmente $X_{t-1}$ da entrambi gli estremi.};'
    return tk(body,h=4)
def transform_four():
    body=''
    labs=[('Livello','$X_t$','204'),('Differenza 1',r'$\Delta X_t$','203'),('Differenza 12',r'$\Delta_{12}X_t$','192'),('Combinata',r'$\Delta\Delta_{12}X_t$','191')]
    for i,(a,b,n) in enumerate(labs):
        x=2.3+4.7*(i%2);y=3.5-2.1*(i//2)
        body+=rf'\node[pFlow,text width=3.5cm,minimum height=1.35cm] at({x},{y}){{{a}\\[1mm]{b}\\[1mm]{n} mesi disponibili}};'
    return tk(body,h=4.5)

