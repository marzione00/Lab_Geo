from pathlib import Path
import argparse, importlib.util, json, re, shutil

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent
OUT.mkdir(exist_ok=True)
for d in ('Codice','Dati','Risorse/Figure','R'):(OUT/d).mkdir(parents=True,exist_ok=True)
base=(ROOT/'template.tex').read_text()
preamble=base.split('\\begin{document}',1)[0]
preamble=preamble.replace('Iride: descrivere e visualizzare i dati','Gemina: confrontare gruppi e valutare ipotesi')
preamble=preamble.replace('Iride_M03_descrivere_visualizzare.tex','Gemina_M06_confronti_ipotesi.tex')
preamble=preamble.replace('80 slide','94 slide').replace('#3/80','#3/94')
preamble=preamble.replace('Modulo M03: distribuzioni, confronti e rappresentazioni','Modulo M05: modelli del caso e propagazione dell’incertezza')
if r'\newcommand{\PLab}' not in preamble:
    preamble+=r'''
\newcommand{\PLab}[2]{\par{\color{Classical}\bfseries\fontsize{9}{11}\selectfont
\href{#1}{\MakeUppercase{#2}}}\par\vspace{1.8mm}}
'''



SECTIONS=[(3,'Definire il confronto'),(20,'Interpretare l’evidenza'),(37,'Confrontare due gruppi'),(60,'Categorie e confronti multipli'),(78,'Applicazioni e verifica')]
cover=r'''
\begin{frame}[plain]\hypertarget{slide1}{}
\begin{tikzpicture}[remember picture,overlay]
\fill[Night] (current page.south west) rectangle (current page.north east);
\draw[Mint,line width=2pt] ([xshift=1.05cm,yshift=-1.35cm]current page.north west)--([xshift=3cm,yshift=-1.35cm]current page.north west);
\node[anchor=north west,inner sep=0] at ([xshift=1.05cm,yshift=-1.7cm]current page.north west){\color{Mint}\bfseries\fontsize{11}{14}\selectfont GEMINA · MODULO M06 · SCIENZE DELLA TERRA};
\node[anchor=north west,inner sep=0] at ([xshift=1.05cm,yshift=-2.75cm]current page.north west){\begin{minipage}{17cm}\raggedright\color{white}\bfseries\fontsize{31}{39}\selectfont Confrontare gruppi\\e valutare ipotesi\end{minipage}};
\node[anchor=north west,inner sep=0] at ([xshift=1.05cm,yshift=-6.65cm]current page.north west){\begin{minipage}{16cm}\color{Lilac}\fontsize{15}{21}\selectfont Contrasti, disegno ed evidenza statistica in R\end{minipage}};
\node[anchor=north west,inner sep=0] at ([xshift=1.05cm,yshift=-8.95cm]current page.north west){\begin{minipage}{16cm}\color{white}\fontsize{11.5}{16}\selectfont Marzio De Corato\\Materiale per la lezione e il laboratorio\end{minipage}};
\node[anchor=south east,inner sep=0] at ([xshift=18.95cm,yshift=-11.35cm]current page.north west){\color{Lilac!45}\bfseries\fontsize{64}{68}\selectfont R};
\end{tikzpicture}\end{frame}
'''
index=r'''\begin{frame}[plain]\hypertarget{slide2}{}\bookmark[level=0,page=2]{Indice}
\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north west,inner sep=0] at ([xshift=.95cm,yshift=-.65cm]current page.north west){\color{Navy}\bfseries\fontsize{22}{27}\selectfont Percorso di Gemina};
\draw[Classical,line width=1.3pt] ([xshift=.95cm,yshift=-1.68cm]current page.north west)--([xshift=2.25cm,yshift=-1.68cm]current page.north west);
'''
for i,(n,title) in enumerate(SECTIONS):
    y=2.45+1.05*i
    index+=rf'\node[anchor=north west,inner sep=0,text width=16.9cm] at ([xshift=1.1cm,yshift=-{y}cm]current page.north west){{\color{{Navy}}\fontsize{{14}}{{18}}\selectfont\hyperlink{{slide{n}}}{{{i+1}. {title}}}\hfill\color{{Muted}}\fontsize{{10}}{{13}}\selectfont {n}}};'+'\n'
index+=r'''
\node[anchor=north west,inner sep=0] at ([xshift=1cm,yshift=-8.7cm]current page.north west){\begin{minipage}{17.9cm}\color{Ink}\fontsize{11.3}{15}\selectfont Definire il contrasto, stimare l’effetto e motivare il riferimento del test. Undici esperimenti collegano formule, osservazioni e interpretazione dei risultati.\end{minipage}};
\node[anchor=north west,inner sep=0,text width=17.9cm] at ([xshift=1cm,yshift=-10.2cm]current page.north west){\color{Classical}\fontsize{11}{14.5}\selectfont Materiale operativo: dati CSV, frammenti R e quaderno di esercitazione nel progetto Gemina.};
\draw[Rule,line width=.35pt] ([xshift=.95cm,yshift=-11.92cm]current page.north west)--([xshift=19.05cm,yshift=-11.92cm]current page.north west);
\node[anchor=north west,inner sep=0] at ([xshift=.95cm,yshift=-12.06cm]current page.north west){\color{Muted}\fontsize{7.7}{9.3}\selectfont Gemina: confrontare gruppi e valutare ipotesi};
\node[anchor=north east,inner sep=0] at ([xshift=19.05cm,yshift=-12.06cm]current page.north west){\color{Muted}\fontsize{7.7}{9.3}\selectfont 2/94};
\end{tikzpicture}\end{frame}
'''

slides={};codes={}
for name in ('intro_slides','evidence_slides','methods_slides','closing_slides'):
    p=ROOT/(name+'.py')
    if not p.exists():continue
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    if slides.keys()&mod.SLIDES.keys():raise ValueError('Slide duplicate')
    if codes.keys()&mod.CODES.keys():raise ValueError('Codice duplicato')
    slides.update(mod.SLIDES);codes.update(mod.CODES)

def frame(n,d):
    box='';placement=''
    slots=[('W','FullWideBox',18.1,.96,'wide')] if 'wide' in d else [('L','PilotLeftBox',10.05,.96,'left'),('R','PilotRightBox',7.55,11.52,'right')]
    for side,save,width,x,key in slots:
        box+=rf'''\begin{{lrbox}}{{\{save}}}%
\begin{{minipage}}[t]{{{width}cm}}\raggedright\color{{Ink}}\fontsize{{11.3}}{{14.8}}\selectfont
{d[key]}
\end{{minipage}}% 
\end{{lrbox}}
\typeout{{FULLBOX:{n:03}:{side}:\the\ht\{save}:\the\dp\{save}}}
'''
        placement+=(r'\node[anchor=north west,inner sep=0] at ([xshift=@X@cm,yshift=-2.13cm]current page.north west) {\usebox{\@SAVE@}};'+'\n').replace('@X@',str(x)).replace('@SAVE@',save)
    return f"\n% SLIDE {n:03} | {d['title']}\n"+box+rf'''\begin{{frame}}[plain]\hypertarget{{slide{n}}}{{}}
\bookmark[level=1,page={n}]{{{d['title']}}}
\begin{{tikzpicture}}[remember picture,overlay]
\PilotChrome{{{d['title']}}}{{{d['section']}}}{{{n}}}{{{d['recall']}}}
{placement}
\end{{tikzpicture}}\end{{frame}}
'''

for name,code in codes.items():(OUT/'Codice'/name).write_text(code.strip()+'\n')
for f in (OUT/'Codice').glob('*.R'):
    if f.name not in codes:f.unlink()

if '--final' in __import__('sys').argv:
    assert set(slides)==set(range(3,95)), 'Contenuti mancanti o fuori intervallo'
tex=preamble+'\n\\begin{document}\n'+cover+index
for n in range(3,95):
    d=slides.get(n,dict(title=f'Bozza {n}',section='IN LAVORAZIONE',left='',right='',recall=''))
    tex+=frame(n,d)
tex+='\n\\end{document}\n'
(OUT/'Gemina_M06_confronti_ipotesi.tex').write_text(tex)
script='''# Gemina - Confrontare gruppi e valutare ipotesi
# Eseguire dalla cartella di Gemina_M06.Rproj.
# Per mostrare il codice: source("Lezione_Gemina.R", echo = TRUE)
source("setup.R", encoding = "UTF-8")
dir.create("Risultati", showWarnings = FALSE)
pdf("Risultati/Figure_lezione.pdf", width = 9, height = 5.5)
'''
for name,code in sorted(codes.items()):
    script+='\n\n# '+'='*54+'\n# '+name+'\n# '+'='*54+'\n'+code.strip()+'\n'
script+='\n\n# Chiudere il documento delle figure.\ndev.off()\n'
(OUT/'Lezione_Gemina.R').write_text(script)
(OUT/'Gemina_M06.Rproj').write_text('Version: 1.0\n\nRestoreWorkspace: No\nSaveWorkspace: No\nAlwaysSaveHistory: No\n\nEncoding: UTF-8\nUseSpacesForTab: Yes\nNumSpacesForTab: 2\nLaTeX: XeLaTeX\n')
manifest=dict(total_slides=94,revised_slides=sorted(slides),snippets=sorted(codes),tikz_diagrams=sum(sum(d.get(k,'').count('begin{tikzpicture}') for k in ('left','right','wide')) for d in slides.values()))
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(slides=len(slides)+2,snippets=len(codes),tikz=manifest['tikz_diagrams']),indent=2))
