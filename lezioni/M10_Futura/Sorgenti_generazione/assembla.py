#!/usr/bin/env python3
"""Genera TeX, cataloghi editoriali e 48 frammenti R dalle sorgenti del modulo.
Non richiede librerie Python esterne. Non rigenera né sostituisce risultati R.
"""
from pathlib import Path
import csv, json, re
from contenuti import SLIDES, SEZIONI, ROOT

def plain(s):
    return s.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')

def bodybox(name,text,width,n):
    return ('\\begin{lrbox}{\\'+name+'}\n'+r'\begin{minipage}[t]{'+str(width)+'cm}'+
       r'\raggedright\color{Ink}\fontsize{11.3}{14.8}\selectfont'+'\n'+text+'\n'+
       r'\end{minipage}\end{lrbox}'+'\n'+
       r'\typeout{FULLBOX:'+f'{n:03}:'+name+':'+'\\the\\ht\\'+name+':'+'\\the\\dp\\'+name+'}\n')

def page(s):
    n=s['page'];o=[r'\begin{frame}[plain]\hypertarget{slide'+str(n)+'}{}']
    if n in [i for i,t in SEZIONI]:o.append(r'\bookmark[level=0,page='+str(n)+']{'+plain(s['section'])+'}')
    o.append(r'\bookmark[level=1,page='+str(n)+']{'+plain(s['title'])+'}')
    # A separate measurement makes title and recall bounds auditable.
    o.append(bodybox('TitleBox',r'\color{Navy}\bfseries\fontsize{20.6}{24.5}\selectfont '+plain(s['title']),17.7,n))
    o.append(bodybox('RecallBox',r'\fontsize{10.3}{13.8}\selectfont '+s['recall'],14.3,n))
    if s.get('layout')=='panorama':
        o.append(bodybox('FullWideBox',r'\centering\includegraphics[width=18.05cm,height=5.8cm,keepaspectratio]{Risultati/Figure/'+s['figure']+'.pdf}',18.1,n))
        o.append(bodybox('PilotRightBox',r'\PBody{'+s['caption']+'}',18.1,n))
    else:
        right=s['right']
        if s['snippet']:
            right+=r'\PCode{'+plain(s['snippet']['title'])+'}{'+s['code_file']+'}'
        o.append(bodybox('PilotLeftBox',s['left'],10.05,n))
        o.append(bodybox('PilotRightBox',right,7.55,n))
    o.append(r'\begin{tikzpicture}[remember picture,overlay]')
    o.append(r'\PilotChrome{'+plain(s['title'])+'}{'+plain(s['section'])+'}{'+str(n)+'}{'+s['recall']+'}')
    if s.get('layout')=='panorama':
        o.append(r'\node[anchor=north west,inner sep=0] at([xshift=.96cm,yshift=-2.13cm]current page.north west){\usebox{\FullWideBox}};')
        o.append(r'\node[anchor=north west,inner sep=0] at([xshift=.96cm,yshift=-8.25cm]current page.north west){\usebox{\PilotRightBox}};')
    else:
        o.append(r'\node[anchor=north west,inner sep=0] at([xshift=.96cm,yshift=-2.13cm]current page.north west){\usebox{\PilotLeftBox}};')
        o.append(r'\node[anchor=north west,inner sep=0] at([xshift=11.52cm,yshift=-2.13cm]current page.north west){\usebox{\PilotRightBox}};')
    if s['notebook']:
        nb=f'M10_N{s["notebook"]:02}'
        o.append(r'\node[anchor=north east,inner sep=0] at([xshift=17.65cm,yshift=-12.06cm]current page.north west){\color{Classical}\fontsize{7.7}{9.2}\selectfont\href{../../03_Notebook_svolti/M10_Futura/'+nb+'.html}{'+plain(nb)+' · notebook svolto}};')
    o += [r'\end{tikzpicture}\end{frame}', '']
    return '\n'.join(o)

COVER=r'''
\begin{frame}[plain]\hypertarget{slide1}{}\bookmark[level=0,page=1]{Futura}
\begin{tikzpicture}[remember picture,overlay]
\fill[Night](current page.south west) rectangle(current page.north east);
\IfFileExists{Risorse/Copertine/M10_Futura.jpg}{\node[inner sep=0] at(current page.center){\includegraphics[width=20cm,height=12.5cm]{Risorse/Copertine/M10_Futura.jpg}};}{}
\node[anchor=north west,inner sep=0] at([xshift=1.05cm,yshift=-1.10cm]current page.north west){\color{Mint}\bfseries\fontsize{23}{28}\selectfont FUTURA};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-2.16cm]current page.north west){\color{white}\fontsize{9}{12}\selectfont MODULO M10 · SCIENZE DELLA TERRA};
\draw[Mint,line width=1.5pt]([xshift=1.07cm,yshift=-2.78cm]current page.north west)--([xshift=2.6cm,yshift=-2.78cm]current page.north west);
\node[anchor=north west,inner sep=0] at([xshift=1.05cm,yshift=-3.35cm]current page.north west){\begin{minipage}{9.2cm}\raggedright\color{white}\bfseries\fontsize{30}{36}\selectfont Previsione\\e progetto\\statistico\end{minipage}};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-7.88cm]current page.north west){\begin{minipage}{8.9cm}\raggedright\color{Lilac}\fontsize{12.2}{17}\selectfont Modelli temporali, valutazione\\e argomentazione scientifica\end{minipage}};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-10.52cm]current page.north west){\color{white}\fontsize{11.5}{15}\selectfont Marzio De Corato};
\node[anchor=north west,inner sep=0] at([xshift=1.07cm,yshift=-11.17cm]current page.north west){\color{Mint}\fontsize{8.8}{11}\selectfont\href{https://creativecommons.org/licenses/by-nc-sa/4.0/}{© 2026 · CC BY-NC-SA 4.0}};
\end{tikzpicture}\end{frame}
'''

def main():
    (ROOT/'Codice').mkdir(exist_ok=True)
    for s in SLIDES:
        if s['snippet']:
            s['code_file']=f'{s["page"]:03}_esempio.R'
            (ROOT/'Codice'/s['code_file']).write_text(s['snippet']['text'],encoding='utf-8')
    pre=(Path(__file__).parent/'preambolo.tex').read_text()
    tex=pre+'\n\\begin{document}\n'+COVER+'\n'.join(page(s) for s in SLIDES)+'\n\\end{document}\n'
    dest=ROOT/'Futura_M10_previsione_progetto.tex';dest.write_text(tex,encoding='utf-8')
    (ROOT/'Metadati').mkdir(exist_ok=True)
    (ROOT/'Metadati/slide_contenuti.json').write_text(json.dumps(SLIDES,ensure_ascii=False,indent=2))
    with (ROOT/'Metadati/indice_slide.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['pagina','sezione','titolo','notebook'])
        w.writerow([1,'Apertura','Futura — Previsione e progetto statistico',''])
        for s in SLIDES:w.writerow([s['page'],s['section'],s['title'],f'M10_N{s["notebook"]:02}' if s['notebook'] else ''])
    # The script audit runs in a single teaching session after loading canonical state.
    r=['# Esecuzione sequenziale dei frammenti mostrati nelle slide.','source("R/stato_lezione.R",encoding="UTF-8")','verifica_codice <- list()']
    for s in SLIDES:
        if s['snippet']:
            path='Codice/'+s['code_file']
            r += [f'cat("\\nSLIDE {s["page"]:03}\\n")',f'source("{path}",echo=TRUE,encoding="UTF-8")',f'verifica_codice[["{s["page"]:03}"]] <- "PASS"']
    r += ['write.csv(data.frame(slide=names(verifica_codice),esito=unlist(verifica_codice)),"Verifiche/frammenti_slide.csv",row.names=FALSE)','cat("Tutti i frammenti delle slide sono stati eseguiti.\\n")']
    (ROOT/'Codice/esegui_frammenti.R').write_text('\n'.join(r)+'\n')
    print(f'Creati {len(SLIDES)+1} frame e {sum(bool(x["snippet"]) for x in SLIDES)} frammenti R: {dest}')

if __name__=='__main__':main()
