from pathlib import Path
import csv, math
SLIDES={}; CODES={}
ROOT=Path(__file__).resolve().parent
def S(n,title,left,right,recall):
    SLIDES[n]=dict(title=title,section='APPLICAZIONI E CONSEGNA',left=left,right=right,recall=recall)
def table(headers,rows,widths):
    w=sum(widths); h=.68; a=0; cx=[]
    for v in widths: cx.append(a+v/2);a+=v
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for j,row in enumerate([headers]+rows):
        y=-j*h
        out+=[rf'\fill[{"Navy" if j==0 else ("white" if j%2 else "GeoTint")}](0,{y}) rectangle({w},{y+h});']
        for x,t in zip(cx,row):
            out+=[rf'\node[pLabel,text={"white" if j==0 else "Ink"}] at({x},{y+h/2}){{{t}}};']
    return '\n'.join(out+[r'\end{tikzpicture}'])

S(77,'La scelta del modello parte dal processo',r'''
\PLabel{Domande diverse richiedono variabili diverse}
'''+table(['Situazione','Modello candidato'],[['Esito binario','Bernoulli'],['Successi su $n$ prove','Binomiale'],['Eventi per esposizione','Poisson'],['Scarti additivi simmetrici','Normale'],['Fattori positivi moltiplicativi','Lognormale']],[5.45,4])+r'''
\vspace{3mm}
\PSmall{Il modello candidato va confrontato con dominio, protocollo, dipendenza e variabilità osservata. La forma di un istogramma da sola non decide.}
''',r'''
\PLabel{Controlli prima del calcolo}
\PBody{Le prove sono indipendenti? La probabilità resta costante? Le esposizioni sono confrontabili? I valori devono essere positivi?}
\vspace{3mm}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3cm] (a) at(1.8,2.7){Ipotesi\\sul processo};
\node[pFlow,text width=2.8cm] (b) at(5.5,2.7){Conseguenze\\calcolabili};
\node[pFlow,text width=5.8cm,fill=GeoTint] (c) at(3.6,.8){Confronto con dati e protocollo\\eventuale revisione del modello};
\draw[pEdge](a)--(b);
\draw[pEdge](b.south)--++(0,-.25)-|(c.north);
\draw[pEdge](c.west)-|(-.15,2.7)--(a.west);
\end{tikzpicture}
''','La scelta di una distribuzione deve riflettere il processo e le sue condizioni, oltre alla forma dei dati.')

CODES['78_strumenti.R']='''# Densita': 106 g / 40 cm^3
u78 <- function(um, uV) {
  2.65*sqrt((um/106)^2+(uV/40)^2)
}
u78(1, .6)    # situazione iniziale
u78(.5, .6)   # migliora la massa
u78(1, .3)    # migliora il volume
# Incertezze in g/cm^3; c=0
'''
vals=list(csv.DictReader((ROOT/'root_proof/strumenti_78.csv').open()))
bars=''
for y,lab,row in zip([3.2,2.1,1],['Iniziale','Massa: $u_m/2$','Volume: $u_V/2$'],vals):
    v=float(row['u_densita']);x=3+5.1*v/.05
    bars+=rf'\fill[{"GeoB" if lab=="Iniziale" else "GeoA"}](3,{y-.27}) rectangle({x},{y+.27});'+'\n'
    bars+=rf'\node[pLabel,anchor=east] at(2.8,{y}){{{lab}}};'+'\n'
    bars+=rf'\node[pNote,anchor=west] at({x+.1},{y}){{{v:.4f}}};'+'\n'
S(78,'Quale strumento conviene migliorare?',r'''
\PLabel{Confronto a parità di quantità centrali e indipendenza}
\begin{tikzpicture}[x=1cm,y=1cm]
'''+bars+r'''
\draw[pAxis](3,.4)--(8.9,.4);
\node[pNote] at(5.8,0){incertezza standard della densità [g/cm$^3$]};
\end{tikzpicture}
\[
u_{\rho_m}\simeq2{,}65
\sqrt{\left(\frac{u_m}{106}\right)^2+
      \left(\frac{u_V}{40}\right)^2}.
\]
\PSmall{$u_m=1$ g e $u_V=0{,}6$ cm$^3$ all'inizio. Dimezzare $u_V$ riduce maggiormente l'incertezza del rapporto in questo caso.}
''',r'''
\PCode{R · confronto dei contributi}{78_strumenti.R}
\PBody{La massa contribuisce per circa il 28,3\% alla varianza linearizzata; il volume per il 71,7\%.}
\PInfo{La scelta strumentale richiede anche una valutazione di costi, taratura e bias.}
''','Il contributo relativo alla varianza indica quale miglioramento strumentale può ridurre maggiormente l’incertezza del risultato.')

SLIDES[79]=dict(title='I nove esperimenti e i loro prerequisiti',section='APPLICAZIONI E CONSEGNA',wide=r'''
\PLabel{Collegamenti fra lezione e laboratorio}
'''+table(['Esperimento del sito','Domanda di lavoro','Slide'],[
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-eventi}{Eventi}','Probabilità e frequenza cumulativa','5–9'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-condizionamento}{Condizionamento}','Marginali, gruppi e Bayes','10–17'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-distribuzione}{Distribuzione}','Densità, cumulata e soglia','18–25'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-binomiale}{Binomiale}','Prove, conteggi e ripetizioni','26–33'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-poisson}{Poisson}','Tasso ed esposizione','34–41'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-normale}{Normale}','Standardizzazione e quantili','42–49'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-moltiplicazione}{Moltiplicazione}','Scala logaritmica e asimmetria','50–56'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-monte-carlo}{Monte Carlo}','Stima e precisione numerica','57–65'],
[r'\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-propagazione}{Propagazione}','Dipendenza e rapporto positivo','66–76']
],[5.3,9.8,2.5])+r'''
\PSmall{Il quaderno segue questi nove esperimenti. La mappa nel progetto collega separatamente i venti laboratori R del modulo.}
''',recall='Ogni esperimento richiede una previsione, un confronto fra scenari e una spiegazione del risultato.')

CODES['80_consegna.R']='''# Caso fisico: input indipendenti
set.seed(17)
B80 <- 20000
m80 <- rpos(B80, 106, 1)
v80 <- rpos(B80, 40, .6)
d80 <- m80/v80
dir.create("Risultati",
           showWarnings=FALSE)
write.csv(data.frame(densita=d80),
  "Risultati/densita.csv",
  row.names=FALSE)
'''
S(80,'Consegna: una relazione riproducibile',r'''
\PLabel{Il caso della densità come esercizio conclusivo}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=4cm] (a) at(2.2,3.3){\textbf{Modello}\\input positivi, unità e dipendenza};
\node[pFlow,text width=4cm] (b) at(7.1,3.3){\textbf{Calcolo}\\simulazione e approssimazione};
\node[pFlow,text width=4cm] (c) at(2.2,1.2){\textbf{Risultato}\\distribuzione, intervallo e precisione};
\node[pFlow,text width=4cm] (d) at(7.1,1.2){\textbf{Discussione}\\sensibilità e miglioramento strumentale};
\draw[pEdge](a)--(b);\draw[pEdge](a)--(c);\draw[pEdge](b)--(d);\draw[pEdge](c)--(d);
\end{tikzpicture}
\PBody{Consegnare uno script R eseguibile e una relazione di due pagine con due figure. Indicare seme, numero di repliche e parametri.}
\PSmall{Confrontare lo scenario iniziale con un volume misurato meglio. Spiegare quali risultati cambiano se aumenta soltanto $B$.}
''',r'''
\PCode{R · salvare le repliche}{80_consegna.R}
\PSmall{\texttt{rpos()} usa media e SD originali. Il modello mantiene gli input positivi.}

''','Un risultato riproducibile richiede modello dichiarato, codice eseguibile, unità e una lettura corretta della variabilità.')

S(81,'Domande per controllare la comprensione',r'''
\PLabel{Quattro situazioni da spiegare}
'''+table(['Situazione','Controllo necessario'],[
['Densità pari a 5','Area e unità della variabile'],
['Nessun evento simulato','Probabilità e repliche'],
['Media uguale, SD diversa','Parametri di scala'],
['Rapporto meno variabile','Dipendenza degli ingressi']
],[4.7,4.8])+r'''
\vspace{3mm}
\PBody{Per ogni situazione scrivere una spiegazione e un controllo in R. Una risposta deve indicare quale quantità si sta calcolando.}
''',r'''
\PLabel{Tre risultati da tenere distinti}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=6.3cm] at(3.6,4.3){$\operatorname{sd}(Y_1,\ldots,Y_B)$\\dispersione dell'output simulato};
\node[pFlow,text width=6.3cm] at(3.6,2.6){$[q_{0,025},q_{0,975}]$\\intervallo centrale del modello};
\node[pFlow,text width=6.3cm,fill=GeoTint] at(3.6,.9){$\operatorname{sd}(Y)/\sqrt B$\\stima dell’errore standard MC della media};
\end{tikzpicture}
\PSmall{L'ultima espressione richiede repliche indipendenti e varianza finita. I tre risultati rispondono a domande diverse.}
''','Il nome della quantità, le ipotesi e l’unità devono accompagnare ogni numero riportato.')

S(82,'Fonti e materiali per il laboratorio',r'''
\PLabel{Il percorso del corso}
\PBody{\href{https://marzione00.github.io/Lab_Geo/}{Lab\_Geo, modulo M04}\\Probabilità, variabilità e simulazione.}
\vspace{2mm}
\PSmall{Materiali del modulo: nove esperimenti nel browser e venti laboratori R. Collegamenti e corrispondenze sono nei sorgenti.}
\vspace{4mm}
\PLabel{Documentazione R}
\PBody{\href{https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Distributions.html}{R Core Team, distribuzioni nel pacchetto stats}.}
\PSmall{\texttt{Binomial}, \texttt{Poisson}, \texttt{Normal}, \texttt{Lognormal}, \texttt{Uniform} e documentazione dei generatori casuali.}
\vspace{4mm}
\PLabel{Propagazione delle distribuzioni}
\PSmall{\href{https://www.bipm.org/documents/20126/2071204/JCGM_101_2008_E.pdf}{JCGM 101:2008, Supplement 1 to the GUM}. Principi di propagazione delle distribuzioni mediante Monte Carlo.}
''',r'''
\PLabel{Nel progetto Aurea}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=6.1cm] at(3.4,4.5){\textbf{Lezione}\\PDF, sorgente LaTeX e frammenti R};
\node[pFlow,text width=6.1cm] at(3.4,2.8){\textbf{Esercitazioni}\\quaderno, nove script e dati};
\node[pFlow,text width=6.1cm] at(3.4,1.1){\textbf{Approfondimento}\\note docente e mappa dei venti esercizi};
\end{tikzpicture}
\PSmall{I dati didattici e le simulazioni non rappresentano una campagna di misura reale. Parametri e provenienza sono dichiarati nei materiali.}
''','Le formule e il codice sono strumenti per rendere controllabili il modello, i calcoli e l’interpretazione.')

