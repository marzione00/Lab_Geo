from pathlib import Path
import importlib, json, shutil, sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent if ROOT.name=='Sorgenti_generazione' else ROOT/'Polychroma_M08'
OUT.mkdir(exist_ok=True)
for d in ['Codice','R','Risorse/Copertine','Dati','Calcoli']:(OUT/d).mkdir(parents=True,exist_ok=True)
modules=[importlib.import_module(n) for n in ['intro_slides','pca_slides','clustering_slides','robustness_slides']]
slides={};codes={}
for m in modules:
    assert not slides.keys()&m.SLIDES.keys()
    assert not codes.keys()&m.CODES.keys()
    slides.update(m.SLIDES);codes.update(m.CODES)
assert set(slides)==set(range(2,109))
for name,text in codes.items():(OUT/'Codice'/name).write_text(text)

preamble=(ROOT/'template.tex').read_text().split('\\begin{document}')[0]
cover=r'''
\begin{frame}[plain]\hypertarget{slide1}{}\bookmark[level=0,page=1]{Polychroma}
\begin{tikzpicture}[remember picture,overlay]
\fill[Night](current page.south west) rectangle(current page.north east);
\IfFileExists{Risorse/Copertine/M08_Polychroma.jpg}{\node[inner sep=0] at(current page.center){\includegraphics[width=20cm,height=12.5cm]{Risorse/Copertine/M08_Polychroma.jpg}};}{}
\node[anchor=north west,inner sep=0] at([xshift=1.05cm,yshift=-1.10cm]current page.north west){\color{Mint}\bfseries\fontsize{23}{28}\selectfont POLYCHROMA};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-2.16cm]current page.north west){\color{white}\fontsize{9}{12}\selectfont MODULO M08 · SCIENZE DELLA TERRA};
\draw[Mint,line width=1.5pt]([xshift=1.07cm,yshift=-2.78cm]current page.north west)--([xshift=2.6cm,yshift=-2.78cm]current page.north west);
\node[anchor=north west,inner sep=0] at([xshift=1.05cm,yshift=-3.35cm]current page.north west){\begin{minipage}{9.2cm}\raggedright\color{white}\bfseries\fontsize{30}{36}\selectfont Analisi\\multivariata\\dei campioni\end{minipage}};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-7.88cm]current page.north west){\begin{minipage}{8.9cm}\raggedright\color{Lilac}\fontsize{12.2}{17}\selectfont Geometria della PCA,\\partizioni e interpretazione geologica\end{minipage}};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-10.52cm]current page.north west){\color{white}\fontsize{11.5}{15}\selectfont Marzio De Corato};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-11.17cm]current page.north west){\color{Mint}\fontsize{8.8}{11}\selectfont\href{https://creativecommons.org/licenses/by-nc-sa/4.0/}{© 2026 · CC BY-NC-SA 4.0}};
\end{tikzpicture}\end{frame}
'''
sections={2:'Campioni, scale e distanze',15:'Ridondanza e composizioni',27:'Geometria della PCA',45:'Interpretare le componenti',58:'K-means',73:'Numero dei gruppi e silhouette',83:'Gerarchie di Ward',94:'Stabilità e interpretazione',104:'Un’analisi completa'}

def frame(n,d):
    # The boxes belong to the frame. This keeps a clean rebuild independent
    # of changes to frame boundaries in editorial scripts.
    s=rf'\begin{{frame}}[plain]\hypertarget{{slide{n}}}{{}}'+'\n'
    if n in sections:s+=rf'\bookmark[level=0,page={n}]{{{sections[n]}}}'+'\n'
    s+=rf'\bookmark[level=1,page={n}]{{{d["title"]}}}'+'\n'
    placements=[]
    slots=[('W','FullWideBox',18.1,.96,'wide')] if 'wide' in d else [('L','PilotLeftBox',10.05,.96,'left'),('R','PilotRightBox',7.55,11.52,'right')]
    for side,box,width,x,key in slots:
        s+=rf'''\begin{{lrbox}}{{\{box}}}%
\begin{{minipage}}[t]{{{width}cm}}\raggedright\color{{Ink}}\fontsize{{11.3}}{{14.8}}\selectfont
{d[key]}
\end{{minipage}}%
\end{{lrbox}}
\typeout{{FULLBOX:{n:03}:{side}:\the\ht\{box}:\the\dp\{box}}}
'''
        placements.append(rf'\node[anchor=north west,inner sep=0] at([xshift={x}cm,yshift=-2.13cm]current page.north west){{\usebox{{\{box}}}}};')
    s+=r'\begin{tikzpicture}[remember picture,overlay]'+'\n'
    s+=rf'\PilotChrome{{{d["title"]}}}{{{d["section"]}}}{{{n}}}{{{d["recall"]}}}'+'\n'+'\n'.join(placements)
    return s+'\n'+r'\end{tikzpicture}\end{frame}'+'\n'

tex=preamble+'\n\\begin{document}\n'+cover+'\n'.join(frame(n,slides[n]) for n in range(2,109))+'\n\\end{document}\n'
(OUT/'Polychroma_M08_multivariata.tex').write_text(tex)
lesson='# Polychroma M08: frammenti eseguibili nell’ordine della presentazione.\n# Aprire Polychroma_M08.Rproj e lanciare source("Lezione_Polychroma.R", echo=TRUE).\nsource("setup.R", encoding="UTF-8")\ndir.create("Risultati", showWarnings=FALSE)\npdf("Risultati/Figure_lezione.pdf", width=9, height=5.5)\n'
for name,s in sorted(codes.items()):lesson+='\n# '+name+'\n'+s
lesson+='\ndev.off()\n'
(OUT/'Lezione_Polychroma.R').write_text(lesson)
(OUT/'Polychroma_M08.Rproj').write_text('Version: 1.0\n\nRestoreWorkspace: No\nSaveWorkspace: No\nAlwaysSaveHistory: No\n\nEncoding: UTF-8\nUseSpacesForTab: Yes\nNumSpacesForTab: 2\nLaTeX: XeLaTeX\n')
manifest={'slides':108,'snippets':len(codes),'tikz_diagrams':sum(d.get(k,'').count(r'\begin{tikzpicture}') for d in slides.values() for k in ['left','right','wide']),'slide_titles':{str(n):d['title'] for n,d in sorted(slides.items())},'codes':sorted(codes)}
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in manifest.items() if k not in ['slide_titles','codes']}))
