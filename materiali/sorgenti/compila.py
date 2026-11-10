"""Compilazione XeLaTeX nel template originale, con misure dei riquadri."""
from pathlib import Path
import json,re,subprocess,shutil,sys,csv
import fitz
P=Path(__file__).resolve().parents[1]
def esc(s):
 return s.replace('₀',r'\textsubscript{0}').replace('₂',r'\textsubscript{2}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('³',r'\textsuperscript{3}').replace('²',r'\textsuperscript{2}')
def prose(s):
 s=s.replace('₀',r'\textsubscript{0}').replace('₂',r'\textsubscript{2}')
 parts=re.split(r'(\\\(.*?\\\)|\\\[.*?\\\]|\$[^$]*\$)',s,flags=re.S)
 return ''.join(t if i%2 else re.sub(r'(?<!\\)([%_&#])',r'\\\1',t) for i,t in enumerate(parts))
def math(s):
 if not s:return ''
 s=re.sub(r'(?<=\d),(?=\d)',r'{,}',s)
 return r'\par\vspace{.28cm}{\centering\fontsize{13}{17}\selectfont\(\displaystyle\begin{gathered}'+s+r'\end{gathered}\)\par}'
def box(name,w,size,lead,s):return rf'\begin{{lrbox}}{{\{name}}}\begin{{minipage}}[t]{{{w}cm}}\raggedright\sloppy\color{{Ink}}\fontsize{{{size}}}{{{lead}}}\selectfont '+s+rf'\end{{minipage}}\end{{lrbox}}'+'\n'
def node(x,y,s,anchor='north west'):return rf'\node[anchor={anchor},inner sep=0] at ([xshift={x}cm,yshift=-{y}cm]current page.north west){{{s}}};'+'\n'
def compila(mod):
 data=json.loads((P/'sorgenti/contenuti'/f'{mod}.json').read_text());pages=data['pagine'];n=len(pages)+2
 pre=(P/'sorgenti/template/originale.tex').read_text().split(r'\begin{document}')[0]
 a=pre.index(r'\IfFontExistsTF{NimbusSans-Regular.otf}');b=pre.index(r'\usefonttheme{professionalfonts}')
 pre=pre[:a]+r'''\setsansfont{NimbusSans-Regular.otf}[Path=sorgenti/font/,BoldFont=NimbusSans-Bold.otf,ItalicFont=NimbusSans-Italic.otf]
\setmainfont{NimbusSans-Regular.otf}[Path=sorgenti/font/,BoldFont=NimbusSans-Bold.otf,ItalicFont=NimbusSans-Italic.otf]
\setmonofont{lmmono10-regular.otf}[Path=sorgenti/font/,Scale=.88]
'''+pre[b:]
 pre+=r'\usetikzlibrary{decorations.pathreplacing,fit,backgrounds,matrix}\hypersetup{pdftitle={'+esc(mod+' · '+data['titolo'])+r'},pdfsubject={Revisione integrale R6}}\begin{document}'+'\n'
 out=[pre,r'\begin{frame}[plain]\hypertarget{slide1}{}\begin{tikzpicture}[remember picture,overlay]']
 out+=[r'\fill[Night] (current page.south west) rectangle (current page.north east);',r'\draw[Mint,line width=2pt] ([xshift=1.05cm,yshift=-1.35cm]current page.north west)--([xshift=3cm,yshift=-1.35cm]current page.north west);']
 out.append(node(1.05,1.7,r'\color{Mint}\bfseries\fontsize{11}{14}\selectfont '+mod+' · REVISIONE R6'))
 out.append(node(1.05,2.65,r'\begin{minipage}{15.8cm}\raggedright\color{white}\bfseries\fontsize{31}{38}\selectfont '+esc(data['titolo'])+r'\end{minipage}'))
 out.append(node(1.05,6.4,r'\begin{minipage}{15.8cm}\raggedright\color{Lilac}\fontsize{15}{21}\selectfont '+esc(data['sottotitolo'])+r'\end{minipage}'))
 out.append(node(1.05,8.6,r'\begin{minipage}{16.5cm}\color{white}\fontsize{11}{15}\selectfont '+str(n)+r' slide · teoria, derivazioni, figure e applicazioni in R.\par\smallskip Provenienza dei dati e sorgenti nei materiali allegati.\end{minipage}'))
 out.append(node(18.95,11.35,r'\color{Lilac!45}\bfseries\fontsize{64}{68}\selectfont '+mod,anchor='south east'))
 out.append(r'\end{tikzpicture}\end{frame}'+'\n')
 sections=[]
 for i,s in enumerate(pages,3):
  if not sections or sections[-1][0]!=s['sezione']:sections.append((s['sezione'],i))
 assert len(sections)<=12,(mod,sections)
 out.append(r'\begin{frame}[plain]\hypertarget{slide2}{}\bookmark[level=0,page=2]{Indice}\begin{tikzpicture}[remember picture,overlay]')
 out.append(node(.95,.65,r'\color{Navy}\bfseries\fontsize{22}{27}\selectfont Percorso del modulo'))
 out.append(r'\draw[Classical,line width=1.3pt] ([xshift=.95cm,yshift=-1.68cm]current page.north west)--([xshift=2.25cm,yshift=-1.68cm]current page.north west);')
 half=(len(sections)+1)//2
 for j,(sec,pg) in enumerate(sections):
  x=.95+(j//half)*9.35;y=2.23+(j%half)*1.30
  out.append(node(x,y,rf'\color{{Classical}}\bfseries\fontsize{{13}}{{16}}\selectfont {pg}'))
  out.append(node(x+1.05,y,r'\begin{minipage}{7.25cm}\raggedright\color{Navy}\bfseries\fontsize{12.4}{15.5}\selectfont\hyperlink{slide'+str(pg)+'}{'+esc(sec)+r'}\end{minipage}'))
 out.append(node(.95,10.55,r'\begin{minipage}{18cm}\color{Muted}\fontsize{10}{13}\selectfont I numeri indicano le pagine iniziali; i titoli sono cliccabili. Codice, figure e verifiche sono inclusi nel progetto.\end{minipage}'))
 out.append(r'\end{tikzpicture}\end{frame}'+'\n')
 mapping=[];prev=None
 for i,s in enumerate(pages,3):
  left=prose(s['testo'])+math(s['formula']);right=prose(s['destra']);kind='Sviluppo e interpretazione'
  if s['figura']:
   kind='Evidenza grafica';right=r'\includegraphics[width=7.45cm]{figure/'+s['figura']+r'.pdf}'
  if s['tikz']:
   kind='Lettura del diagramma';right=r'\input{tikz/'+s['tikz']+'.tex}'
  if s['didascalia']:right+=r'\par\vspace{.16cm}{\fontsize{9.5}{12.6}\selectfont '+prose(s['didascalia'])+'}'
  right+=math(s['formula_destra'])
  if s['codice']:
   kind='Implementazione in R';right+=r'\par\vspace{.25cm}\lstinputlisting[language=R]{estratti/'+s['codice']+'.R}'
  out += [box('TitleBox',18.2,20.7,24,r'\bfseries\color{Navy}'+esc(s['titolo'])),box('BodyBox',10.25,12.4,16.4,left),box('SideBox',7.45,12.2,16.1,right),box('RecallBox',16.45,10.1,13.2,esc(s['richiamo']))]
  for nm in ['TitleBox','BodyBox','SideBox','RecallBox']:out.append(r'\MeasureBox{'+str(i)+'-'+nm+'}{\\'+nm+'}\n')
  out.append(r'\begin{frame}[plain]\hypertarget{slide'+str(i)+'}{}\n')
  if s['sezione']!=prev:out.append(r'\bookmark[level=0,page='+str(i)+']{'+esc(s['sezione'])+'}\n');prev=s['sezione']
  out.append(r'\bookmark[level=1,page='+str(i)+']{'+esc(s['titolo'])+'}\n')
  out.append(r'\begin{tikzpicture}[remember picture,overlay]')
  out.append(node(19.05,.16,r'\color{Classical}\fontsize{8}{10}\selectfont\hyperlink{slide2}{Indice}',anchor='north east'))
  out.append(node(.95,.62,r'\usebox{\TitleBox}'))
  out.append(r'\draw[Classical,line width=1.3pt] ([xshift=.95cm,yshift=-1.68cm]current page.north west)--([xshift=2.25cm,yshift=-1.68cm]current page.north west);')
  out.append(node(.95,2.12,r'\usebox{\BodyBox}'));out.append(node(11.6,2.1,r'\color{Quantum}\bfseries\fontsize{11.5}{14}\selectfont '+kind));out.append(node(11.6,2.75,r'\usebox{\SideBox}'))
  out.append(r'\draw[Rule,line width=.5pt] ([xshift=.95cm,yshift=-10.43cm]current page.north west)--([xshift=19.05cm,yshift=-10.43cm]current page.north west);')
  out.append(node(.95,10.66,r'\color{Classical}\bfseries\fontsize{9.4}{12}\selectfont Richiami'));out.append(node(2.6,10.64,r'\usebox{\RecallBox}'))
  out.append(r'\draw[Rule,line width=.35pt] ([xshift=.95cm,yshift=-11.92cm]current page.north west)--([xshift=19.05cm,yshift=-11.92cm]current page.north west);')
  out.append(node(.95,12.06,r'\color{Muted}\fontsize{7.7}{9.3}\selectfont '+mod+' · '+esc(data['titolo'][:53])));
  out.append(node(17.65,12.06,r'\color{Classical}\fontsize{7.3}{9.1}\selectfont '+esc(s['fonti']),anchor='north east'))
  out.append(node(19.05,12.06,rf'\color{{Muted}}\fontsize{{7.7}}{{9.3}}\selectfont {i}/{n}',anchor='north east'))
  out.append(r'\end{tikzpicture}\end{frame}'+'\n')
  mapping.append(dict(pagina=i,**s))
 out.append(r'\end{document}')
 tex=P/'sorgenti'/f'{mod}_R6.tex';tex.write_text(''.join(out))
 d=P/'verifiche'/mod;d.mkdir(exist_ok=True)
 for _ in range(2):
  q=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={d}',str(tex)],cwd=P,capture_output=True,text=True)
  (d/'console.txt').write_text(q.stdout+q.stderr)
  if q.returncode:raise RuntimeError(mod+'\n'+q.stdout[-3000:])
 log=(d/f'{mod}_R6.log').read_text(errors='replace');metrics=[]
 limits={'TitleBox':.98,'BodyBox':8.14,'SideBox':7.5,'RecallBox':1.05}
 for m in re.finditer(r'GEOBOX:(\d+)-(\w+):([\d.]+)pt:([\d.]+)pt:([\d.]+)pt',log):
  z=dict(pagina=int(m[1]),box=m[2],h_pt=float(m[4])+float(m[5]));z['ok']=z['h_pt']<=limits[z['box']]*28.45274;metrics.append(z)
 (d/'geometria.json').write_text(json.dumps(metrics,indent=2))
 bad=[x for x in metrics if not x['ok']]
 assert not bad,(mod,bad)
 assert 'Overfull' not in log and 'Missing character:' not in log,(mod,re.findall(r'(?:Overfull|Missing character:)[^\n]+',log))
 shutil.copyfile(d/f'{mod}_R6.pdf',P/'pdf'/f'{mod}_R6.pdf')
 pdf=fitz.open(P/'pdf'/f'{mod}_R6.pdf');assert len(pdf)==n
 (P/'documentazione'/f'mappa_{mod}.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2))
 print(mod,n,'pagine; nessun overflow')
if __name__=='__main__':
 for mod in sys.argv[1:]:compila(mod)
