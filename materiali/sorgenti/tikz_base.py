from pathlib import Path
P=Path(__file__).resolve().parents[1]
def scrivi(mod,id,body):
 d=P/'tikz'/mod;d.mkdir(exist_ok=True)
 pre=r'\begin{tikzpicture}[x=1cm,y=-.87cm,every node/.style={font=\fontsize{12.2}{15}\selectfont,text=Ink},arr/.style={-{Stealth[length=2mm]},line width=.8pt,draw=Classical}]\path[use as bounding box] (0,0) rectangle (7.45,6.2);'
 (d/f'{id}.tex').write_text(pre+'\n'+body+'\n'+r'\end{tikzpicture}')
 return f'{mod}/{id}'
def n(x,y,text,w=None,color='Ink',size=12.2,anchor='center'):
 opts=f'anchor={anchor},text={color},font=\\fontsize{{{size}}}{{15}}\\selectfont'
 if w:opts+=f',text width={w}cm,align=center'
 return rf'\node[{opts}] at ({x},{y}) {{{text}}};'+'\n'
def a(x1,y1,x2,y2,col='Classical'):
 return rf'\draw[arr,draw={col}] ({x1},{y1})--({x2},{y2});'+'\n'
def rect(x1,y1,x2,y2,col='Classical',fill=8):
 return rf'\draw[draw={col},fill={col}!{fill},rounded corners=2pt,line width=.7pt] ({x1},{y1}) rectangle ({x2},{y2});'+'\n'
def linea(x1,y1,x2,y2,col='Rule'):
 return rf'\draw[{col},line width=.8pt] ({x1},{y1})--({x2},{y2});'+'\n'
