from pathlib import Path
import csv, json, math

ROOT=Path(__file__).resolve().parent
MODULE=ROOT.parent if ROOT.name=='Sorgenti_generazione' else ROOT/'Annula_M07'
DATA=list(csv.DictReader((MODULE/'Dati/fossili_simulati.csv').open()))
VALUES=json.loads((MODULE/'Calcoli/slides_values.json').read_text())
V=VALUES['valori']

def it(x,d=3): return f'{float(x):.{d}f}'.replace('.','{,}')

def axes(xmin=3,xmax=9,ymin=2,ymax=8,xlabel=r'Diametro totale ($\mu$m)',ylabel=r'Diametro interno ($\mu$m)',w=9,h=4.5,xticks=None,yticks=None):
    X=lambda x: .65+(float(x)-xmin)/(xmax-xmin)*(w-1.15)
    Y=lambda y: .65+(float(y)-ymin)/(ymax-ymin)*(h-.9)
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]',rf'\path[use as bounding box](-.25,-.4) rectangle({w+.15},{h+.2});',rf'\draw[pAxis](.65,.65)--({w},.65);',rf'\draw[pAxis](.65,.65)--(.65,{h});']
    if xticks is None:xticks=range(math.ceil(xmin),math.floor(xmax)+1)
    if yticks is None:yticks=range(math.ceil(ymin),math.floor(ymax)+1,2)
    for t in xticks:out.append(rf'\draw[Muted]({X(t):.4f},.59)--({X(t):.4f},.71);\node[pNote] at({X(t):.4f},.31){{$ {it(t,0)} $}};')
    for t in yticks:out.append(rf'\draw[Muted](.59,{Y(t):.4f})--(.71,{Y(t):.4f});\node[pNote,anchor=east] at(.5,{Y(t):.4f}){{$ {it(t,0)} $}};')
    out.append(rf'\node[pNote] at({w/2+.4},-.15){{{xlabel}}};')
    out.append(rf'\node[pNote,rotate=90] at(-.14,{h/2+.3}){{{ylabel}}};')
    return out,X,Y

def line(out,X,Y,points,color='Classical',options='line width=1.1pt'):
    out.append(r'\draw['+color+','+options+'] plot coordinates {'+' '.join(f'({X(x):.4f},{Y(y):.4f})' for x,y in points)+'};')

def scatter(fit=False,band=False,means=False):
    out,X,Y=axes()
    if band:
        for lo,hi,col in [('ip_lwr','ip_upr','GeoA!13'),('ic_lwr','ic_upr','Classical!35')]:
            rows=VALUES['intervalli_griglia']
            pts=[(float(r['x']),float(r[lo])) for r in rows]+[(float(r['x']),float(r[hi])) for r in rows[::-1]]
            out.append(r'\fill['+col+'] '+'--'.join(f'({X(x):.4f},{Y(y):.4f})' for x,y in pts)+'--cycle;')
    for r in DATA:
        col='GeoA' if r['morfotipo']=='Rounded' else 'GeoB'
        out.append(rf'\fill[{col},opacity=.68]({X(r["diametro_tot_um"]):.4f},{Y(r["diametro_int_um"]):.4f}) circle(1.25pt);')
    if fit:
        a=V['intercetta.(Intercept)'];b=V['pendenza.diametro_tot_um']
        line(out,X,Y,[(3.7,a+b*3.7),(8.62,a+b*8.62)],'Navy')
    if means:
        xx=X(V['xmedio']);yy=Y(V['ymedio'])
        out += [rf'\draw[Muted,dashed]({xx:.4f},.65)--({xx:.4f},{yy:.4f})--(.65,{yy:.4f});',rf'\draw[white,line width=1pt,fill=Classical]({xx:.4f},{yy:.4f}) circle(3.2pt);',rf'\node[pLabel,anchor=north west] at({xx+.2:.4f},{yy-.2:.4f}){{$ (\bar x,\bar y) $}};']
    out += [r'\node[pNote,text=GeoA,anchor=west] at(1.0,4.45){Rounded};\node[pNote,text=GeoB,anchor=west] at(3.1,4.45){Spiky};',r'\end{tikzpicture}']
    return '\n'.join(out)

def schematic(kind='linear'):
    out,X,Y=axes(0,5,0,7,xlabel='$x$',ylabel='$y$',xticks=[0,1,2,3,4,5],yticks=[0,2,4,6])
    xs=[.3+i*.19 for i in range(24)]
    for i,x in enumerate(xs):
        if kind=='u':y=.55+.8*(x-2.5)**2
        elif kind=='monotonic':y=.2+.22*x*x
        elif kind=='residual':y=1+.9*x+.5*math.sin(2.3*i)
        else:y=1+.9*x+.7*math.sin(2.3*i)
        out.append(rf'\fill[GeoA]({X(x):.4f},{Y(y):.4f}) circle(1.7pt);')
        if kind=='residual':out.append(rf'\draw[GeoB,line width=.8pt]({X(x):.4f},{Y(y):.4f})--({X(x):.4f},{Y(1+.9*x):.4f});')
    if kind in ['linear','residual']:line(out,X,Y,[(0,1),(5,5.5)])
    if kind=='u':line(out,X,Y,[(0,2.3),(5,2.3)],'GeoB','dashed,line width=1pt')
    out.append(r'\end{tikzpicture}')
    return '\n'.join(out)

def bars(labels,vals,maxval=1.1,unit=r'RMSE ($\mu$m)'):
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]',r'\path[use as bounding box](0,-.2) rectangle(9.5,4.8);',r'\draw[pAxis](2.7,.55)--(9,.55);']
    for i,(label,val) in enumerate(zip(labels,vals)):
        y=3.8-i*1.15;x=2.7+5.7*val/maxval
        col=['GeoB','GeoA','Classical'][i%3]
        out.append(rf'\node[pLabel,anchor=east,text width=2.35cm] at(2.45,{y}){{{label}}};')
        out.append(rf'\fill[{col}!65](2.7,{y-.25}) rectangle({x:.4f},{y+.25});')
        out.append(rf'\node[pNote,anchor=west] at({x+.12:.4f},{y}){{$ {it(val)} $}};')
    out.append(rf'\node[pNote] at(5.7,.1){{{unit}}};\end{{tikzpicture}}')
    return '\n'.join(out)
