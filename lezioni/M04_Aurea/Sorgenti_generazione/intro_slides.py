from pathlib import Path
import csv, math

SLIDES = {}
CODES = {}
ROOT = Path(__file__).resolve().parent

def S(n, title, section, left, right, recall):
    SLIDES[n] = dict(title=title, section=section, left=left, right=right, recall=recall)

def table(headers, rows, widths):
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    w=sum(widths); h=.62; centers=[]; a=0
    for cw in widths: centers.append(a+cw/2); a+=cw
    out += [rf'\fill[Navy](0,0) rectangle({w},{h});']
    for x,t in zip(centers,headers):
        out += [rf'\node[font=\bfseries\fontsize{{9.5}}{{12}}\selectfont,text=white] at({x},{h/2}){{{t}}};']
    for j,row in enumerate(rows):
        y=-(j+1)*h
        out += [rf'\fill[{"white" if j%2==0 else "GeoTint"}](0,{y}) rectangle({w},{y+h});']
        for x,t in zip(centers,row):
            out += [rf'\node[pLabel] at({x},{y+h/2}){{{t}}};']
    return '\n'.join(out+[r'\end{tikzpicture}'])

def coords(points):
    return ' '.join(f'({x:.5f},{y:.5f})' for x,y in points)

def code(n,name,text):
    key=f'{n:02}_{name}.R'; CODES[key]=text
    return key

code(3,'avvio','''# Aprire Aurea_M04.Rproj.
source("setup.R", encoding = "UTF-8")
# Parametri del caso fisico finale
parametri_densita
# Guida alle distribuzioni in R
help("Distributions")
''')
S(3,'Un modello per le ripetizioni possibili','EVENTI E PROBABILITÀ',r'''
\PLabel{Dalla domanda alle conseguenze del modello}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (p) at(2,3.3){\textbf{Protocollo}\\che cosa osserviamo?};
\node[pFlow,text width=3.5cm] (m) at(7.1,3.3){\textbf{Modello}\\quali esiti e probabilità?};
\node[pFlow,text width=3.5cm] (d) at(2,1.25){\textbf{Dati}\\una realizzazione};
\node[pFlow,text width=3.5cm] (r) at(7.1,1.25){\textbf{Repliche simulate}\\altre realizzazioni};
\draw[pEdge](p)--(m);\draw[pEdge](p)--(d);\draw[pEdge](m)--(r);
\draw[pEdge](d)--node[pNote,above]{confronto}(r);
\end{tikzpicture}
\PBody{Iride ha descritto le osservazioni. In Aurea assegniamo probabilità agli esiti e calcoliamo ciò che il modello prevede.}
''',r'''
\PCode{R · progetto della lezione}{03_avvio.R}
\PSmall{\texttt{setup.R} definisce le funzioni dei laboratori e legge i parametri di massa e volume. Non avvia simulazioni.}
\PInfo{Prerequisiti: vettori, selezioni logiche, media, deviazione standard e lettura dei grafici. Il codice completo è in \texttt{Lezione\_Aurea.R}.}
''','Un modello probabilistico rende espliciti gli esiti, le probabilità assegnate e le condizioni delle ripetizioni.')

SLIDES[4]=dict(title='Tre origini diverse della variabilità',section='EVENTI E PROBABILITÀ',wide=r'''
\PLabel{Che cosa varia e che cosa possiamo modificare}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\lab/\desc/\act in {
5/{Fenomeno}/{Provini diversi hanno proprietà diverse.}/{Cambiare popolazione o supporto cambia la variabilità.},
3/{Misura}/{Le informazioni su una quantità sono limitate.}/{Misure e tarature migliori possono ridurre l'incertezza.},
1/{Calcolo Monte Carlo}/{Un numero finito di repliche dà una stima numerica.}/{Più repliche riducono l'errore numerico.}}{
\node[pFlow,text width=3.1cm,fill=GeoTint] (a\yy) at(1.8,\yy){\textbf{\lab}};
\node[pLabel,text width=6.1cm,align=left] (b\yy) at(7,\yy){\desc};
\node[pLabel,text width=5.4cm,align=left] (c\yy) at(14.4,\yy){\act};
\draw[pEdge](a\yy)--(b\yy);
\draw[Rule](10.45,\yy-.65)--(10.45,\yy+.65);
}
\end{tikzpicture}
\PSmall{Il numero di repliche del computer non migliora da solo una misura, la rappresentatività dei dati o la scelta del modello.}
''',recall='Prima di parlare di precisione, occorre identificare la quantità che varia e la fonte di quella variazione.')

code(5,'eventi','''# Un prelievo uniforme fra 6 provini
m05 <- c(104,106,108,110,112,114)
tipo05 <- c("F","M","F","M","F","M")
A05 <- m05 >= 110   # massa in g
B05 <- tipo05 == "M"
mean(A05)           # P(A) = 3/6
which(A05)          # provini 4,5,6
''')
S(5,'Esiti ed eventi in un insieme finito','EVENTI E PROBABILITÀ',r'''
\PLabel{Un provino scelto con probabilità uniforme}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pGroup](.2,0) rectangle(9.2,3.5);
\node[pLabel,anchor=west] at(.5,3.1){$\Omega=\{1,2,3,4,5,6\}$};
\foreach \x/\lab/\mass in {1/1/104,2.5/2/106,4/3/108,5.5/4/110,7/5/112,8.5/6/114}{
\node[pFlow,minimum width=1.1cm,minimum height=.9cm] at(\x,1.9){\lab};
\node[pNote] at(\x,1.05){\mass\,g};}
\draw[Classical,line width=1.3pt](4.85,.55) rectangle(9.05,2.55);
\node[pNote,text=Classical] at(7,-.35){$A=\{m\ge110\ \mathrm{g}\}=\{4,5,6\}$};
\end{tikzpicture}
\PBody{Un esito è il provino estratto. Un evento è un insieme di esiti che soddisfano una regola. Ogni provino ha probabilità $1/6$.}
\PSmall{La scelta uniforme è un'ipotesi esplicita di questo esempio costruito.}
''',r'''
\PCode{R · un evento come condizione}{05_eventi.R}
\PSmall{\texttt{A05} contiene valori \texttt{TRUE}/\texttt{FALSE}. La media conta i veri e divide per sei. Qui coincide con la probabilità perché tutti gli esiti sono equiprobabili.}
\PInfo{$0\le P(A)\le1,\quad P(\Omega)=1.$\\Il modello deve assegnare probabilità anche quando gli esiti hanno pesi diversi.}
''','La probabilità per conteggio richiede esiti equiprobabili e un evento definito senza ambiguità.')

code(6,'operazioni','''# A: massa >=110 g; B: tipo M
mean(A05 & B05)  # entrambi: 2/6
mean(A05 | B05)  # almeno uno: 4/6
mean(!A05)       # complemento: 3/6
# Controllo della formula dell'unione
mean(A05) + mean(B05) -
  mean(A05 & B05)
''')
S(6,'Unione, intersezione e complemento','EVENTI E PROBABILITÀ',r'''
\PLabel{Le operazioni sugli eventi}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pGroup](.2,.1) rectangle(9.2,3.4);
\fill[GeoA!12](3.4,1.75) ellipse(2.1cm and 1.2cm);
\fill[GeoB!15](5.8,1.75) ellipse(2.1cm and 1.2cm);
\draw[GeoA,line width=.8pt](3.4,1.75) ellipse(2.1cm and 1.2cm);
\draw[GeoB,line width=.8pt](5.8,1.75) ellipse(2.1cm and 1.2cm);
\node[pLabel] at(2.6,1.75){$5$};
\node[pLabel] at(4.6,1.75){$4,6$};
\node[pLabel] at(6.6,1.75){$2$};
\node[pLabel] at(8.5,.55){$1,3$};
\node[pLabel,text=GeoA] at(2.4,3){$A$};
\node[pLabel,text=GeoB] at(6.8,3){$B$};
\end{tikzpicture}
\[
P(A\cup B)=P(A)+P(B)-P(A\cap B)
\]
\PSmall{L'intersezione compare in entrambi i conteggi e va sottratta una volta. Il disegno rappresenta appartenenze, senza proporzionalità fra aree e probabilità.}
''',r'''
\PCode{R · operatori logici}{06_operazioni.R}
\PBody{\texttt{\&} richiede entrambe le condizioni. \texttt{|} richiede almeno una delle due. \texttt{!} inverte la condizione.}
\PInfo{Per il complemento:\\$P(A^c)=1-P(A)$.\\In questo esempio $P(A^c)=3/6$.}
''','Per l’unione si sottrae l’intersezione; per il complemento si sottrae la probabilità a uno.')

code(7,'frequenza','''set.seed(17)  # sequenza riproducibile
x07 <- rbinom(200, 1, prob = .3)
k07 <- seq_along(x07)
f07 <- cumsum(x07) / k07
plot(k07, f07, type = "l",
  ylim = c(0, 1), xlab = "Prove",
  ylab = "Frequenza cumulativa")
abline(h = .3, lty = 2)
''')
freq=list(csv.DictReader((ROOT/'root_proof/frequenze_07.csv').open()))
freqpts=[(.5+float(r['k'])/200*8.1,.2+float(r['frequenza'])*2.9) for r in freq]
S(7,'Probabilità e frequenza osservata','EVENTI E PROBABILITÀ',r'''
\PLabel{Prove indipendenti con probabilità costante $p=0{,}3$}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,.2)--(8.9,.2);\draw[pAxis](.5,.2)--(.5,3.3);
\foreach \y/\lab in {.2/0,1.07/{0{,}3},3.1/1}{\node[pNote,anchor=east] at(.35,\y){$\lab$};}
\foreach \x/\lab in {.54/1,4.55/100,8.6/200}{\node[pNote] at(\x,-.1){\lab};}
\draw[GeoB,dashed,line width=.8pt](.5,1.07)--(8.6,1.07);
\draw[GeoA,line width=.9pt] plot coordinates{'''+coords(freqpts)+r'''};
\node[pNote,anchor=west,text=GeoB] at(6.7,1.4){$p=0{,}3$};
\node[pNote] at(4.5,-.5){numero di prove $n$};
\end{tikzpicture}
\[
\widehat p_n=\frac1n\sum_{i=1}^{n} I_i,\qquad I_i=\mathbf1_{\{A\text{ alla prova }i\}}.
\]
\PSmall{Le oscillazioni possono aumentare temporaneamente lo scarto da $p$.}
''',r'''
\PCode{R · frequenza cumulativa}{07_frequenza.R}
\PSmall{\texttt{rbinom(200,1,.3)} genera 200 esiti 0/1. \texttt{cumsum()} conta progressivamente gli eventi. Il denominatore cresce a ogni prova.}
\PInfo{$p$ resta fisso. La frequenza cambia con la sequenza e il numero di prove.}
''','La probabilità è un parametro del modello; la frequenza è una quantità calcolata da una realizzazione.')

code(8,'atteso','''# Modello costruito per un conteggio
k08 <- 0:2
p08 <- c(.2, .5, .3)
sum(p08)           # normalizzazione
sum(k08 * p08)     # E(K) = 1.1
set.seed(17)
x08 <- sample(k08, 1000,
  replace = TRUE, prob = p08)
mean(x08)          # media simulata
''')
S(8,'Il valore atteso di un conteggio','EVENTI E PROBABILITÀ',r'''
\PLabel{Un modello con tre esiti numerici}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.4,.2)--(8.8,.2);\draw[pAxis](.4,.2)--(.4,3.5);
\foreach \x/\y/\lab in {1.5/1.4/{0{,}2},4.2/3.2/{0{,}5},6.9/2/{0{,}3}}{
\draw[GeoA,line width=8pt](\x,.2)--(\x,\y);\node[pNote] at(\x,\y+.35){$\lab$};}
\foreach \x/\lab in {1.5/0,4.2/1,6.9/2}{\node[pNote] at(\x,-.1){\lab};}
\draw[GeoB,dashed,line width=.9pt](4.47,.2)--(4.47,3.7);
\node[pNote,text=GeoB,anchor=west] at(4.7,3.65){$\mathbb E[K]=1{,}1$};
\node[pNote] at(8,-.1){$k$};
\end{tikzpicture}
\[
\mathbb E[K]=\sum_k kP(K=k)
=0\cdot0{,}2+1\cdot0{,}5+2\cdot0{,}3=1{,}1.
\]
\PSmall{L'atteso può essere diverso da tutti i valori ammessi per una singola osservazione.}
''',r'''
\PCode{R · media del modello}{08_atteso.R}
\PSmall{\texttt{sample()} estrae i valori $0,1,2$ con i pesi specificati. \texttt{replace=TRUE} permette estrazioni ripetute dallo stesso insieme.}
\PInfo{L'atteso descrive il centro delle ripetizioni. Il conteggio effettivo rimane un intero.}
''','Il valore atteso è una media pesata delle possibilità del modello; la singola prova conserva i propri esiti ammessi.')

code(9,'lab_eventi','''a09 <- lab_eventi(prob=.3, n=200)
b09 <- lab_eventi(prob=.3, n=800)
a09$indicatori
b09$indicatori
# Cambia la sequenza, lascia fisso p
c09 <- lab_eventi(prob=.3,
  n=800, seed=21)
c09$indicatori
''')
S(9,'Laboratorio: frequenze nelle ripetizioni','LABORATORIO · EVENTI',r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-eventi}{Esperimento m04-eventi}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.1,3.3){$p=0{,}3$, $n=200$\\seme 17};
\node[pFlow,text width=3.7cm] (b) at(7.2,3.3){$p=0{,}3$, $n=800$\\seme 17};
\node[pFlow,text width=3.7cm] (c) at(7.2,1.25){$p=0{,}3$, $n=800$\\seme 21};
\draw[pEdge](a)--node[pNote,above]{più prove}(b);
\draw[pEdge](b)--node[pNote,left]{altra sequenza}(c);
\end{tikzpicture}
\PBody{Registrare la frequenza finale e il suo scarto da $p$. Cercare anche un tratto in cui lo scarto aumenta.}
\PSmall{Il sito consente da 20 a 2000 prove. L'esperimento mantiene indipendenza e probabilità costante.}
''',r'''
\PCode{R · confronti controllati}{09_lab_eventi.R}
\PSmall{Le funzioni del progetto riproducono i dati e gli indicatori degli esperimenti. \texttt{\$indicatori} estrae il riepilogo restituito dalla funzione.}
\PInfo{Domanda: una frequenza finale più vicina a $p$ dimostra che la convergenza è sempre monotona? Motivare dalla curva.}
''','Il numero di prove e il seme modificano la realizzazione; il parametro p definisce la probabilità dell’evento.')

code(10,'condizionata','''# Numeri attesi per 100 casi
t10 <- matrix(c(32,12,8,48), nrow=2,
  dimnames=list(c("B","nonB"),
                c("A","nonA")))
t10
t10["B","A"] / sum(t10["B",])
# Fra tutti i casi: P(A)=44/100
sum(t10[,"A"]) / sum(t10)
''')
S(10,'Condizionare cambia il denominatore','CONDIZIONAMENTO',r'''
\PLabel{Modello di un segnale A e di un tipo B}
'''+table(['Casi attesi','Segnale $A$','$A^c$','Totale'],[['Tipo $B$','32','8','40'],['Altri $B^c$','12','48','60'],['Totale','44','56','100']],[2.7,2.2,2,2.3])+r'''
\vspace{2mm}
\[
P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{32}{40}=0{,}8.
\]
\PSmall{I conteggi sono attesi, costruiti da probabilità assegnate. La popolazione di riferimento comprende entrambi i tipi.}
\PBody{Conoscere $B$ restringe l'insieme di riferimento alla prima riga.}
''',r'''
\PCode{R · selezionare il denominatore}{10_condizionata.R}
\PSmall{Le righe distinguono i tipi, le colonne il segnale. \texttt{sum(t10["B",])} conta tutti i casi del gruppo $B$.}
\PInfo{La definizione richiede $P(B)>0$. Una condizione impossibile non fornisce un denominatore utilizzabile.}
''','Una probabilità condizionata deve sempre dichiarare il gruppo entro cui si calcola la quota.')

code(11,'totale','''prior11 <- .4    # P(B)
pa11 <- .8       # P(A dato B)
pb11 <- .2       # P(A dato nonB)
joint11 <- c(prior11 * pa11,
  (1-prior11) * pb11)
joint11         # .32 e .12
sum(joint11)    # P(A) = .44
''')
S(11,'Probabilità congiunte e probabilità totale','CONDIZIONAMENTO',r'''
\PLabel{Prodotti lungo i percorsi, somme fra percorsi alternativi}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,minimum width=.9cm] (o) at(.7,2.1){$\Omega$};
\node[pFlow,minimum width=1cm] (b) at(3.4,3.3){$B$};
\node[pFlow,minimum width=1cm] (c) at(3.4,.9){$B^c$};
\node[pLabel,anchor=west] (a) at(6.2,4){$A:\ 0{,}32$};
\node[pLabel,anchor=west] (aa) at(6.2,2.6){$A^c:\ 0{,}08$};
\node[pLabel,anchor=west] (ac) at(6.2,1.6){$A:\ 0{,}12$};
\node[pLabel,anchor=west] (cc) at(6.2,.2){$A^c:\ 0{,}48$};
\draw[pEdge](o)--node[pNote,above]{$0{,}4$}(b);
\draw[pEdge](o)--node[pNote,below]{$0{,}6$}(c);
\draw[pEdge](b)--node[pNote,above]{$0{,}8$}(a);
\draw[pEdge](b)--node[pNote,below]{$0{,}2$}(aa);
\draw[pEdge](c)--node[pNote,above]{$0{,}2$}(ac);
\draw[pEdge](c)--node[pNote,below]{$0{,}8$}(cc);
\end{tikzpicture}
\[
P(A)=P(A\mid B)P(B)+P(A\mid B^c)P(B^c).
\]
\PSmall{$B$ e $B^c$ sono disgiunti e ricoprono tutti gli esiti.}
''',r'''
\PCode{R · sommare i contributi}{11_totale.R}
\PBody{Il primo contributo è $0{,}8\cdot0{,}4=0{,}32$. Il secondo è $0{,}2\cdot0{,}6=0{,}12$. La somma dà $P(A)=0{,}44$.}
\PInfo{La formula del prodotto $P(A\cap B)=P(A\mid B)P(B)$ vale anche quando gli eventi dipendono l'uno dall'altro.}
''','La probabilità totale combina le probabilità interne ai gruppi usando i pesi dei gruppi.')

code(12,'indipendenza','''# Esempio indipendente
pA12 <- .4; pB12 <- .5
pAB12 <- .2
pAB12 / pB12       # .4 = P(A)
isTRUE(all.equal(pAB12, pA12*pB12))
# Incompatibili: P(A e B)=0
0 == pA12*pB12     # FALSE
''')
S(12,'Indipendenza e incompatibilità','CONDIZIONAMENTO',r'''
\PLabel{Due relazioni con condizioni diverse}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=4cm,fill=GeoA!8] at(2.2,3.2){\textbf{Indipendenza}\\conoscere $B$ lascia invariata $P(A)$};
\node[pFlow,text width=4cm,fill=GeoB!8] at(7.15,3.2){\textbf{Incompatibilità}\\$A$ e $B$ non possono verificarsi insieme};
\node[pLabel,text width=4.2cm] at(2.2,1.6){$P(A\cap B)=P(A)P(B)$};
\node[pLabel,text width=4.2cm] at(7.15,1.6){$P(A\cap B)=0$};
\node[pNote,text width=9cm] at(4.7,.3){Se $P(A)>0$ e $P(B)>0$, l'incompatibilità esclude l'indipendenza.};
\end{tikzpicture}
\PBody{L'indipendenza è una proprietà del modello. Distanza fisica o assenza di una correlazione osservata non bastano a giustificarla.}
''',r'''
\PCode{R · una verifica numerica}{12_indipendenza.R}
\PSmall{\texttt{all.equal()} confronta valori numerici con tolleranza. \texttt{isTRUE()} converte l'esito della verifica in un singolo valore logico.}
\PInfo{Nel modello della pagina precedente, $P(A\mid B)=0{,}8$ e $P(A)=0{,}44$: gli eventi sono dipendenti.}
''','L’indipendenza conserva la probabilità dopo il condizionamento; l’incompatibilità vieta il verificarsi congiunto.')

code(13,'bayes','''prior13 <- .4
pa13 <- .8; pb13 <- .2
pA13 <- pa13*prior13 +
  pb13*(1-prior13)
post13 <- pa13*prior13 / pA13
c(P_A = pA13, P_B_dato_A = post13)
# .44 e circa .72727
''')
S(13,'La probabilità inversa con Bayes','CONDIZIONAMENTO',r'''
\PLabel{Fra i casi con segnale A}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!75](.4,1.3) rectangle(6.8,2.7);
\fill[GeoB!85](6.8,1.3) rectangle(9.2,2.7);
\node[pLabel,text=white] at(3.6,2){32 del tipo $B$};
\node[pLabel,text=white] at(8,2){12 di $B^c$};
\draw[decorate,decoration={brace,amplitude=5pt}](.4,2.9)--(9.2,2.9)
 node[midway,above=6pt,pLabel]{44 segnali attesi};
\node[pNote,text width=8.6cm] at(4.8,.55){Il denominatore raccoglie tutti i segnali, da entrambi i gruppi.};
\end{tikzpicture}
\[
P(B\mid A)=\frac{P(A\mid B)P(B)}{P(A)}
=\frac{0{,}32}{0{,}44}\simeq0{,}727.
\]
\PSmall{$P(A)>0$. La probabilità inversa usa la composizione iniziale oltre alle probabilità di segnale nei due gruppi.}
''',r'''
\PCode{R · invertire la condizione}{13_bayes.R}
\PBody{La quota di $B$ fra i segnali è circa il 72,7\%. La probabilità di segnale nel gruppo $B$ rimane 80\%.}
\PInfo{Le domande hanno denominatori diversi:\\$P(B\mid A)$ considera i segnali.\\$P(A\mid B)$ considera il tipo $B$.}
''','Per invertire una condizione servono la probabilità del segnale nei gruppi e la composizione della popolazione.')

code(14,'prevalenza','''prior14 <- c(.1, .4, .8)
pa14 <- .8; pb14 <- .2
pA14 <- pa14*prior14 +
  pb14*(1-prior14)
post14 <- pa14*prior14/pA14
data.frame(prior14, post14)
''')
bayespts=[(.6+8*i/100,.2+3.6*(.8*(i/100)/(.8*(i/100)+.2*(1-i/100)))) for i in range(101)]
S(14,'La composizione iniziale cambia il risultato','CONDIZIONAMENTO',r'''
\PLabel{$P(A\mid B)=0{,}8$ e $P(A\mid B^c)=0{,}2$ restano fisse}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,.2)--(8.9,.2);\draw[pAxis](.6,.2)--(.6,4.05);
\draw[GeoA,line width=1.2pt] plot coordinates{'''+coords(bayespts)+r'''};
\foreach \x/\y/\lab in {1.4/1.30769/{0{,}1},3.8/2.81818/{0{,}4},7/3.58824/{0{,}8}}{
\fill[GeoB](\x,\y) circle(2.3pt);
\draw[GeoB!65,dashed](\x,.2)--(\x,\y);
\node[pNote] at(\x,-.1){$\lab$};}
\node[pNote,anchor=east] at(.4,.2){0};
\node[pNote,anchor=east] at(.4,3.8){1};
\node[pNote] at(4.8,-.6){prevalenza iniziale $P(B)$};
\node[pNote,anchor=west] at(.8,4.1){$P(B\mid A)$};
\end{tikzpicture}
\PSmall{La curva deriva direttamente da Bayes. I tre punti corrispondono ai valori calcolati nel codice.}
''',r'''
\PCode{R · modificare un solo parametro}{14_prevalenza.R}
\PBody{La quota $P(B\mid A)$ vale circa 0,308, 0,727 e 0,941 nei tre scenari.}
\PInfo{Trasferire un criterio di riconoscimento a un altro contesto richiede di riesaminare la composizione iniziale e la validità dei tassi condizionati.}
''','A parità di probabilità condizionate, la quota del tipo B fra i segnali cambia con la prevalenza iniziale.')

code(15,'mille_casi','''# Nuovo esempio: tipo T e segnale S
N15 <- 1000
nT15 <- N15 * .10
segnali15 <- c(T = nT15*.90,
  altri = (N15-nT15)*.05)
segnali15           # 90 e 45
segnali15["T"] / sum(segnali15)
# Due terzi dei segnali attesi
''')
S(15,'Un classificatore su mille campioni','CONDIZIONAMENTO',r'''
\PLabel{Un secondo esempio costruito}
'''+table(['Gruppo','Campioni','Segnali attesi'],[['Tipo $T$','100','$100\\cdot0{,}90=90$'],['Altri tipi','900','$900\\cdot0{,}05=45$'],['Totale','1000','135']],[3.1,2.5,3.6])+r'''
\vspace{4mm}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm] (a) at(2.05,.7){Fra i campioni $T$\\$P(S\mid T)=0{,}90$};
\node[pFlow,text width=4.5cm,fill=GeoTint] (b) at(6.95,.7){Fra i segnali\\$P(T\mid S)=90/135=2/3$};
\draw[pEdge](a)--(b);
\end{tikzpicture}
\PSmall{Il tipo $T$ e il segnale $S$ appartengono a questo nuovo scenario. I parametri differiscono da quelli predefiniti nel browser.}
''',r'''
\PCode{R · contare i segnali attesi}{15_mille_casi.R}
\PBody{Gli altri tipi sono nove volte più numerosi. La probabilità del 5\% produce 45 segnali attesi.}
\PInfo{I conteggi sono attesi. Un campione osservato può produrre numeri diversi.}
''','Il significato di un segnale dipende anche dalla numerosità dei gruppi che possono produrlo.')

code(16,'lab_condizionamento','''a16 <- lab_condizionamento(
  prior=.4, pa=.8, pb=.2)
b16 <- lab_condizionamento(
  prior=.1, pa=.8, pb=.2)
a16$indicatori
b16$indicatori
# Uguale probabilita' nei due gruppi
c16 <- lab_condizionamento(
  prior=.4, pa=.2, pb=.2)
c16$indicatori
''')
S(16,'Laboratorio: marginali e condizionate','LABORATORIO · CONDIZIONAMENTO',r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-condizionamento}{Esperimento m04-condizionamento}
'''+table(['Parametro','Significato','Default'],[[r'\texttt{prior}','$P(B)$','0,4'],[r'\texttt{pa}','$P(A\\mid B)$','0,8'],[r'\texttt{pb}','$P(A\\mid B^c)$','0,2']],[2.4,4.5,2.3])+r'''
\vspace{4mm}
\PBody{Prima diminuire \texttt{prior} mantenendo fissi gli altri parametri. Poi impostare \texttt{pa=pb} e controllare l'indipendenza.}
\PInfo{Annotare $P(A)$ e $P(B\mid A)$, spiegando perché rispondono in modo diverso al cambiamento dei parametri.}
''',r'''
\PCode{R · due confronti}{16_lab_condizionamento.R}
\PSmall{Il risultato è deterministico: deriva dalle formule. Il seme presente nell'interfaccia non modifica questo esperimento.}
''','La marginale combina i gruppi; la probabilità inversa ripesa i gruppi fra i casi che soddisfano la condizione.')

code(17,'dominio','''# Formula esplicita e denominatore
bayes17 <- function(prior, pa, pb) {
  pA <- pa*prior + pb*(1-prior)
  if (pA == 0) return(NA_real_)
  pa*prior/pA
}
bayes17(.4, .8, .2)
bayes17(.4, 0, 0)  # condizione nulla
''')
S(17,'Le condizioni della formula di Bayes','CONDIZIONAMENTO',r'''
\PLabel{Il calcolo richiede un modello coerente}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=4cm] (a) at(2.2,3.3){Probabilità in $[0,1]$\\gruppi $B$ e $B^c$};
\node[pFlow,text width=4cm] (b) at(7.1,3.3){Tassi condizionati\\validi per quel contesto};
\node[pFlow,text width=4cm,fill=GeoTint] (c) at(2.2,1.1){$P(A)>0$\\denominatore definito};
\node[pFlow,text width=4cm,fill=GeoTint] (d) at(7.1,1.1){$P(B\mid A)$\\quota entro i casi $A$};
\draw[pEdge](a)--(c);\draw[pEdge](b)--(d);\draw[pEdge](c)--(d);
\end{tikzpicture}
\PBody{Se $A$ ha probabilità nulla, il rapporto usato qui non definisce $P(B\mid A)$. In R restituiamo \texttt{NA} per rendere visibile il problema.}
''',r'''
\PCode{R · una condizione non definita}{17_dominio.R}
\PSmall{La funzione è un esempio didattico con argomenti già validi in $[0,1]$. \texttt{NA\_real\_} rappresenta un valore numerico mancante.}
\PInfo{Il laboratorio limita i parametri a valori interni a $(0,1)$. Il caso con probabilità nulla serve a chiarire il dominio della formula.}
''','Il valore numerico ha significato solo insieme al denominatore e alle ipotesi che definiscono il modello.')

