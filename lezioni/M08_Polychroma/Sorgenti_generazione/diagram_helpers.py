from pathlib import Path
import csv, json, math
ROOT=Path(__file__).resolve().parent
MODULE=ROOT.parent if ROOT.name=='Sorgenti_generazione' else ROOT/'Polychroma_M08'
DATA=list(csv.DictReader((MODULE/'Dati/rocce_simulate.csv').open()))
VARIABLES=['SiO2','CaO','MgO','FeO','densita','grana_mm','colore','fossili']
LABELS={'SiO2':r'SiO$_2$','CaO':'CaO','MgO':'MgO','FeO':'FeO','densita':'Densità','grana_mm':'Grana','colore':'Colore','fossili':'Fossili'}
COLORS=['GeoA','GeoB','GeoC']
def table(name):
 return list(csv.DictReader((MODULE/'Calcoli'/name).open()))
def metrics():return json.loads((MODULE/'Calcoli/metrics.json').read_text())
def it(x,d=3):return f'{float(x):.{d}f}'.replace('.','{,}')
def tk(body,w=9.4,h=4.5):
 return r'\begin{tikzpicture}[x=1cm,y=1cm]'+f'\n\\path[use as bounding box](-.15,-.15) rectangle({w},{h});\n'+body+'\n'+r'\end{tikzpicture}'
def axes(xmin=-3,xmax=3,ymin=-3,ymax=3,xlabel='$z_1$',ylabel='$z_2$',w=9,h=4.5,xticks=None,yticks=None,equal=False):
 iw=w-1.25;ih=h-1.15
 if equal:
  scale=min(iw/(xmax-xmin),ih/(ymax-ymin));iw=scale*(xmax-xmin);ih=scale*(ymax-ymin)
 ox=.8+(w-1.25-iw)/2;oy=.7+(h-1.15-ih)/2
 X=lambda x:ox+(float(x)-xmin)/(xmax-xmin)*iw
 Y=lambda y:oy+(float(y)-ymin)/(ymax-ymin)*ih
 out=[r'\begin{tikzpicture}[x=1cm,y=1cm]',rf'\path[use as bounding box](-.15,-.2) rectangle({w+.1},{h+.15});',rf'\draw[pAxis]({ox},{oy})--({ox+iw+.12},{oy});',rf'\draw[pAxis]({ox},{oy})--({ox},{oy+ih+.12});']
 if xticks is None:xticks=[xmin,(xmin+xmax)/2,xmax]
 if yticks is None:yticks=[ymin,(ymin+ymax)/2,ymax]
 for t in xticks:out.append(rf'\draw[Muted]({X(t):.4f},{oy-.05})--({X(t):.4f},{oy+.05});\node[pNote] at({X(t):.4f},{oy-.25}){{$ {format(float(t),".4g").replace(".", "{,}")} $}};')
 for t in yticks:out.append(rf'\draw[Muted]({ox-.05},{Y(t):.4f})--({ox+.05},{Y(t):.4f});\node[pNote,anchor=east] at({ox-.1},{Y(t):.4f}){{$ {format(float(t),".4g").replace(".", "{,}")} $}};')
 out.append(rf'\node[pNote] at({ox+iw/2},{oy-.58}){{{xlabel}}};')
 out.append(rf'\node[pNote,rotate=90] at({max(-.05,ox-.65)},{oy+ih/2}){{{ylabel}}};')
 return out,X,Y
def line(out,X,Y,points,color='Classical',options='line width=1.1pt'):
 out.append(r'\draw['+color+','+options+'] plot coordinates {'+' '.join(f'({X(x):.4f},{Y(y):.4f})' for x,y in points)+'};')
def pca_plot(color='none',dim1='PC1',dim2='PC2',w=9,h=4.7):
 rows=table('pca_scores.csv');assign={r['id']:r for r in table('assignments.csv')}
 xs=[float(r[dim1]) for r in rows];ys=[float(r[dim2]) for r in rows]
 xmin=math.floor(min(xs))-.2;xmax=math.ceil(max(xs))+.2;ymin=math.floor(min(ys))-.2;ymax=math.ceil(max(ys))+.2
 var=table('variance.csv');q={(r['PC'] if r['PC'].startswith('PC') else 'PC'+r['PC']):float(r['quota']) for r in var}
 out,X,Y=axes(xmin,xmax,ymin,ymax,xlabel=rf'{dim1} ({it(100*q[dim1],1)}\%)',ylabel=rf'{dim2} ({it(100*q[dim2],1)}\%)',w=w,h=h,xticks=[],yticks=[],equal=True)
 if xmin<0<xmax:line(out,X,Y,[(0,ymin),(0,ymax)],'Rule','dashed')
 if ymin<0<ymax:line(out,X,Y,[(xmin,0),(xmax,0)],'Rule','dashed')
 lith={r['id']:r['litologia_generatrice'] for r in DATA}
 for r in rows:
  if color=='litologia':c=COLORS[['Basalto','Arenaria','Calcare'].index(lith[r['id']])]
  elif color in ['kmeans','ward']:c=COLORS[(int(float(assign[r['id']][color]))-1)%3]
  else:c='GeoA'
  out.append(rf'\fill[{c},opacity=.75]({X(r[dim1]):.4f},{Y(r[dim2]):.4f}) circle(1.6pt);')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
