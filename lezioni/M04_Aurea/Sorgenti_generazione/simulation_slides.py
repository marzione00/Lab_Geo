"""Aurea M04, slide 50-76. Figure TikZ e calcoli riproducibili."""
from pathlib import Path
import csv
import math

SLIDES = {}
CODES = {}
POS = "VARIABILITÀ MOLTIPLICATIVA"
MC = "MONTE CARLO"
UNC = "PROPAGAZIONE DELL'INCERTEZZA"
ROOT = Path(__file__).resolve().parent

def add(n, title, left, right, recall, section):
    SLIDES[n] = dict(title=title, section=section, left=left,
                     right=right, recall=recall)

def nden(x, mu=0, sd=1):
    return math.exp(-.5*((x-mu)/sd)**2)/(sd*math.sqrt(2*math.pi))

def lden(x, mu=0, sd=.6):
    return nden(math.log(x),mu,sd)/x if x>0 else 0

def coords(fun, a, b, count=151):
    return [(a+(b-a)*i/(count-1), fun(a+(b-a)*i/(count-1)))
            for i in range(count)]

def chart(series, xmin, xmax, ymax, xticks, yticks, xlabel,
          ylabel="Densità", height=2.8, marks=None, label=True, ymin=0):
    x0,y0,w=.72,.58,8.15
    sx=lambda x:x0+(x-xmin)/(xmax-xmin)*w
    sy=lambda y:y0+(y-ymin)/(ymax-ymin)*height
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for y,lab in yticks:
        out += [rf'\draw[Rule] ({x0},{sy(y):.4f})--({x0+w},{sy(y):.4f});',
                rf'\node[pNote,anchor=east] at ({x0-.12},{sy(y):.4f}) {{{lab}}};']
    out += [rf'\draw[pAxis] ({x0},{y0})--({x0+w+.2},{y0});',
            rf'\draw[pAxis] ({x0},{y0})--({x0},{y0+height+.15});']
    for x,lab in xticks:
        out += [rf'\draw[Muted] ({sx(x):.4f},{y0})--({sx(x):.4f},{y0-.1});',
                rf'\node[pNote,below] at ({sx(x):.4f},{y0-.12}) {{{lab}}};']
    for color,pts in series:
        out += [rf'\draw[{color},line width=1.1pt] plot coordinates {{'+
                ' '.join(f'({sx(x):.5f},{sy(y):.5f})' for x,y in pts)+'};']
    if marks:
        for x,lab,color,yy in marks:
            out += [rf'\draw[{color},dashed] ({sx(x):.5f},{y0})--({sx(x):.5f},{sy(yy):.5f});',
                    rf'\node[pNote,text={color},anchor=south] at ({sx(x):.5f},{sy(yy)+.03:.5f}) {{{lab}}};']
    if label:
        out += [rf'\node[pNote,anchor=west] at ({x0},{y0+height+.4}) {{{ylabel}}};',
                rf'\node[pNote] at ({x0+w/2},-.25) {{{xlabel}}};']
    return '\n'.join(out+[r'\end{tikzpicture}'])

def table(headers, rows, widths, colors=None):
    xedges=[0]
    for w in widths:xedges.append(xedges[-1]+w)
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for j,row in enumerate([headers]+rows):
        y=-j*.62
        fill="Navy" if j==0 else ("white" if j%2 else "GeoTint")
        fg="white" if j==0 else "Ink"
        out.append(rf'\fill[{fill}] (0,{y}) rectangle ({xedges[-1]},{y+.62});')
        for k,txt in enumerate(row):
            out.append(rf'\node[pLabel,text={fg}] at ({(xedges[k]+xedges[k+1])/2},{y+.31}) {{{txt}}};')
    return '\n'.join(out+[r'\end{tikzpicture}'])

add(50,"Variazioni che si moltiplicano",r'''
\PLabel{Rapporti uguali, incrementi diversi}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis] (.4,2.8)--(9.2,2.8);
\foreach \xx/\lab in {.8/{1/4},2.8/{1/2},4.8/{1},6.8/{2},8.8/{4}}{
  \fill[GeoA] (\xx,2.8) circle(2.5pt);
  \node[pLabel,above] at(\xx,2.93){$\lab$};
}
\foreach \xx in {.8,2.8,4.8,6.8}{
  \draw[pEdge] (\xx,2.2)--node[pNote,below] {$\times2$} ++(2,0);
}
\node[pNote] at(4.8,1.15){Scala di $\log(X/x_0)$: passi uguali per rapporti uguali};
\end{tikzpicture}
\[
X=x_0\prod_{j=1}^{k}F_j
\quad\Longrightarrow\quad
\log(X/x_0)=\sum_{j=1}^{k}\log F_j.
\]
\PSmall{$x_0>0$: riferimento nella stessa unità di $X$; i fattori $F_j>0$ sono adimensionali. Il logaritmo è naturale.}
''',r'''
\PCode{R · prodotto e somma dei log}{50_prodotti.R}
\PBody{I logaritmi rendono additivi i contributi moltiplicativi di crescita o riduzione.}
\PInfo{Logaritmi normali indipendenti hanno somma normale. In altri casi l'approssimazione va giustificata.}
''',"Un modello moltiplicativo richiede fattori positivi e un riferimento che renda adimensionale il logaritmo.",POS)
CODES["50_prodotti.R"]='''# Fattori positivi adimensionali
f50 <- c(1.2, .8, 1.1)
prod(f50)       # Prodotto: 1.056
exp(sum(log(f50)))
# Stesso risultato entro precisione
all.equal(log(prod(f50)),
          sum(log(f50)))
'''

add(51,"La lognormale nasce sulla scala dei log",r'''
\PLabel{Una trasformazione con supporto positivo}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (z) at(2.1,2.75)
  {$Z=\log(X/x_0)$\\$Z\sim\mathcal N(\mu_\ell,s^2)$};
\node[pFlow,text width=3.7cm] (x) at(7.1,2.75)
  {$X=x_0e^Z$\\$X>0$};
\draw[pEdge] (z.east)--node[pNote,above] {$\exp$} (x.west);
\node[pFlow,text width=3.7cm,fill=GeoTint] at(2.1,.9)
  {Scarti additivi\\sulla scala logaritmica};
\node[pFlow,text width=3.7cm,fill=GeoTint] at(7.1,.9)
  {Rapporti moltiplicativi\\sulla scala originale};
\end{tikzpicture}
\PBody{In R, \texttt{meanlog} e \texttt{sdlog} descrivono il logaritmo dei valori numerici. Non sono la media e la deviazione standard di $X$.}
\PSmall{Nel caso adimensionale $x_0=1$, \texttt{rlnorm(500,0,.6)} estrae 500 valori con $\mu_\ell=0$ e $s=0{,}6$.}
''',r'''
\PCode{R · generare valori positivi}{51_lognormale.R}
\PSmall{La densità di \texttt{log(x51)} è riferita alla variabile trasformata. Cambiare soltanto la scala dell'asse lascia diversa la quantità rappresentata.}
''',"Una variabile lognormale ha logaritmo normale; i parametri di rlnorm appartengono alla scala logaritmica.",POS)
CODES["51_lognormale.R"]='''# X adimensionale, 500 estrazioni
set.seed(17)
x51 <- rlnorm(500, 0, .6)
range(x51)
hist(log(x51), probability = TRUE,
     main = "Logaritmo di X",
     xlab = "log(X)", col = "#E0ECEA")
curve(dnorm(x, 0, .6), add = TRUE,
      col = "#087C74", lwd = 2)
'''

add(52,"Mediana e media della lognormale",r'''
\PLabel{Caso adimensionale: $\mu_\ell=0$, $s=0{,}6$}
'''+chart([("GeoA",coords(lden,.015,4))],0,4,.95,
           [(0,"0"),(1,"1"),(2,"2"),(3,"3"),(4,"4")],
           [(0,"0"),(.4,"0,4"),(.8,"0,8")],"$X$",
           marks=[(1,"mediana", "Classical",.30),(math.exp(.18),"media","GeoB",.96)])+r'''
\[
\operatorname{med}(X)=e^{\mu_\ell}=1,\qquad
E[X]=e^{\mu_\ell+s^2/2}\simeq1{,}197.
\]
\PSmall{La coda destra sposta la media. Le formule riguardano il modello; una simulazione finita produce stime variabili.}
''',r'''
\PCode{R · teoria e simulazione}{52_media_mediana.R}
\PSmall{\texttt{median()} e \texttt{mean()} operano sui 500 valori estratti. La mediana teorica resta 1 quando cambia soltanto $s$.}
\PInfo{La media geometrica teorica è $e^{E[\log X]}=1$. Corrisponde alla mediana in questo modello lognormale.}
''',"Per una lognormale non degenere, la media supera la mediana; entrambe dipendono dai parametri sulla scala dei log.",POS)
CODES["52_media_mediana.R"]='''set.seed(17)
x52 <- rlnorm(500, 0, .6)
c(mediana_teoria = 1,
  mediana_sim = median(x52),
  media_teoria = exp(.6^2/2),
  media_sim = mean(x52))
'''

add(53,"La dispersione relativa cambia scala",r'''
\PLabel{Due quantità vicine solo per piccoli valori di $s$}
\[
\mathrm{CV}_X=\frac{\operatorname{SD}(X)}{E[X]}
            =\sqrt{e^{s^2}-1}.
\]
'''+table([r"$s=\operatorname{SD}(\log X)$",r"$\mathrm{CV}_X$","CV in percentuale"],
          [["0,10","0,1003","10,03%"],["0,30","0,3069","30,69%"],["0,60","0,6583","65,83%"]],
          [3.6,2.4,3.4]).replace("%",r"\%")+r'''
\vspace{2mm}
\PBody{L'approssimazione $\mathrm{CV}_X\simeq s$ deriva da $e^{s^2}-1\simeq s^2$. L'errore cresce con $s$.}
\PSmall{Per calcolare $e^a-1$ con $a$ piccolo, R mette a disposizione \texttt{expm1(a)}.}
''',r'''
\PCode{R · SD dei log e CV originale}{53_cv.R}
\PInfo{Nel laboratorio sulla propagazione il nome interno \texttt{cv} indica $s$. Il controllo dell'interfaccia lo descrive come SD dei logaritmi.}
\PSmall{I simboli della lezione esplicitano la scala: $s$ per la SD logaritmica, $\mathrm{CV}_X$ per il rapporto SD/media originale.}
''',"La SD dei logaritmi e il coefficiente di variazione originale sono legati da una formula, ma hanno valori diversi.",POS)
CODES["53_cv.R"]='''# X lognormale: formula esatta
s53 <- c(.1, .3, .6)
cv53 <- sqrt(expm1(s53^2))
data.frame(sdlog = s53, CV = cv53,
           percento = 100*cv53)
'''

mix=lambda x:.65*nden(x,2,.7)+.35*nden(x,6,1)
add(54,"Mescolare popolazioni cambia la distribuzione",r'''
\PLabel{Esempio costruito con due componenti normali}
'''+chart([("Navy",coords(mix,-.5,9)),
           ("GeoA,dashed",coords(lambda x:.65*nden(x,2,.7),-.5,9)),
           ("GeoB,dashed",coords(lambda x:.35*nden(x,6,1),-.5,9))],
          -.5,9,.42,[(0,"0"),(2,"2"),(4,"4"),(6,"6"),(8,"8")],
          [(0,"0"),(.2,"0,2"),(.4,"0,4")],"$X$ adimensionale")+r'''
\[
f_X(x)=0{,}65\,f_1(x)+0{,}35\,f_2(x).
\]
\PSmall{Blu: componente $N(2,0{,}7^2)$ pesata; ocra: $N(6,1)$ pesata; scuro: somma. I pesi descrivono le quote del modello.}
''',r'''
\PCode{R · scegliere gruppo e valore}{54_miscela.R}
\PSmall{Si estrae il gruppo, poi il valore. \texttt{ifelse()} assegna i parametri di ciascuna estrazione.}
\PInfo{Più componenti possono produrre un solo picco. I picchi non contano le popolazioni.}
''',"Una miscela conserva il meccanismo di appartenenza ai gruppi; una singola famiglia può non descriverne la forma.",POS)
CODES["54_miscela.R"]='''# Due popolazioni adimensionali
set.seed(17)
g54 <- rbinom(500, 1, .65)
mu54 <- ifelse(g54 == 1, 2, 6)
sd54 <- ifelse(g54 == 1, .7, 1)
x54 <- rnorm(500, mu54, sd54)
hist(x54, probability = TRUE,
     main = "Miscela di due gruppi",
     xlab = "X", col = "#E0ECEA")
'''

add(55,"Scegliere un modello coerente con la misura",r'''
\PLabel{Supporto, meccanismo e forma osservata}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.6cm] at(1.5,3.0){\textbf{Normale}\\valori reali};
\node[pFlow,text width=2.6cm] at(4.7,3.0){\textbf{Lognormale}\\valori positivi};
\node[pFlow,text width=2.6cm] at(7.9,3.0){\textbf{Miscela}\\componenti dichiarate};
\node[pNote,text width=2.6cm] at(1.5,1.45){Effetti additivi,\\simmetria plausibile};
\node[pNote,text width=2.6cm] at(4.7,1.45){Effetti moltiplicativi,\\coda destra plausibile};
\node[pNote,text width=2.6cm] at(7.9,1.45){Eterogeneità fra\\popolazioni};
\draw[Rule](3.1,.7)--(3.1,3.7);
\draw[Rule](6.3,.7)--(6.3,3.7);
\end{tikzpicture}
\PBody{Un modello assegna probabilità anche fuori dall'intervallo osservato. Il suo supporto deve essere compatibile con il significato delle misure.}
\PSmall{Un'approssimazione normale può essere utile per valori positivi se la probabilità di valori impossibili è trascurabile rispetto allo scopo.}
''',r'''
\PCode{R · controllare il supporto}{55_supporto_modello.R}
\PSmall{La prima probabilità riguarda una normale con media 1 e SD 0,6. La seconda riguarda una lognormale: il suo supporto è strettamente positivo.}
\PInfo{Eliminare a posteriori le estrazioni negative cambia il modello in una distribuzione condizionata. Tale scelta deve essere dichiarata.}
''',"La scelta di una distribuzione richiede il controllo del supporto e delle ipotesi, oltre all'aspetto del grafico.",POS)
CODES["55_supporto_modello.R"]='''# Esempio adimensionale costruito
pnorm(0, mean = 1, sd = .6)
# Probabilita' circa 0.048
plnorm(0, meanlog = 0, sdlog = .6)
# Qui P(X <= 0) = 0
'''

add(56,"Laboratorio: allargare la distribuzione dei log",r'''
\PLabel{Esperimento m04-moltiplicazione}
'''+chart([("GeoA",coords(lambda x:lden(x,0,.3),.02,4)),
           ("GeoB",coords(lambda x:lden(x,0,.8),.02,4))],
          0,4,1.5,[(0,"0"),(1,"1"),(2,"2"),(3,"3"),(4,"4")],
          [(0,"0"),(.5,"0,5"),(1,"1,0"),(1.5,"1,5")],"$X$")+r'''
\PSmall{Curve teoriche: blu $s=0{,}3$, ocra $s=0{,}8$; $\mu_\ell=0$. Nel browser ciascun istogramma usa 500 estrazioni.}
\PBody{Confrontare mediana teorica, media teorica e media simulata. Spiegare quale cambia quando aumenta $s$.}
''',r'''
\PCode{R · confrontare due ampiezze}{56_lab_lognormale.R}
\PSmall{Con lo stesso seme, il confronto mantiene la stessa sequenza normale sottostante. La mediana teorica è 1 in entrambi i casi.}
\PInfo{\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-moltiplicazione}{Apri l'esperimento sul sito}. Annotare $s$, seme, media teorica e media simulata.}
''',"A mediana fissata, aumentare la dispersione dei logaritmi allunga la coda destra e aumenta la media teorica.",POS)
CODES["56_lab_lognormale.R"]='''# Due esperimenti, ciascuno con B=500
a56 <- lab_moltiplicazione(
  sdlog = .3, seed = 17)
b56 <- lab_moltiplicazione(
  sdlog = .8, seed = 17)
a56$indicatori
b56$indicatori
'''

add(57,"Monte Carlo: ripetere un procedimento definito",r'''
\PLabel{Una quantità del modello diventa una media simulata}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.3cm] (x) at(1.9,3.0){\textbf{Generare}\\$X_b$ dal modello};
\node[pFlow,text width=3.3cm] (g) at(7.3,3.0){\textbf{Calcolare}\\$Y_b=g(X_b)$};
\node[pFlow,text width=4.9cm,fill=GeoTint] (m) at(4.6,.95){\textbf{Riassumere $B$ repliche}\\$\widehat\theta_B=B^{-1}\sum_{b=1}^B Y_b$};
\draw[pEdge] (x)--(g);
\draw[pEdge] (g.south)--++(0,-.65)-|(m.north);
\end{tikzpicture}
\PBody{La quantità cercata è $\theta=E[g(X)]$. Ogni replica completa comprende tutti gli ingressi richiesti da $g$.}
\PSmall{Qui si usano repliche indipendenti e identicamente distribuite. Le proprietà dell'errore dipendono da questa ipotesi e dai momenti esistenti.}
''',r'''
\PCode{R · media di una funzione}{57_monte_carlo.R}
\PSmall{Con $X\sim N(0,1)$ e $g(X)=X^2$, il valore teorico è $E[X^2]=1$. Le 5000 estrazioni costituiscono $B=5000$ repliche.}
\PInfo{Il metodo calcola conseguenze del modello scelto. La qualità del modello richiede controlli separati.}
''',"Ogni replica applica l'intero procedimento a nuovi ingressi; la media delle repliche approssima un valore atteso.",MC)
CODES["57_monte_carlo.R"]='''# E[X^2] per X normale standard
set.seed(17)
B57 <- 5000
x57 <- rnorm(B57)
y57 <- x57^2
c(stima = mean(y57), teoria = 1)
'''

add(58,"Prove in una replica e numero di repliche",r'''
\PLabel{Obiettivo: $P(K\geq8)$ con $K\sim\mathrm{Bin}(20,0{,}3)$}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\lab in {3.2/1,2.0/2,.8/B}{
 \node[pNote,anchor=east] at(.55,\yy){$\lab$};
 \node[pFlow,text width=2.6cm] (a\lab) at(2.2,\yy){20 prove Bernoulli};
 \node[pFlow,text width=1.8cm] (k\lab) at(5,\yy){$K_{\lab}$ successi};
 \node[pFlow,text width=1.9cm,fill=GeoTint] (i\lab) at(8,\yy){$I_{\lab}=\mathbf1_{\{K_{\lab}\geq8\}}$};
 \draw[pEdge](a\lab)--(k\lab);
 \draw[pEdge](k\lab)--(i\lab);
}
\end{tikzpicture}
\[
\widehat p_B=\frac1B\sum_{b=1}^B I_b,\qquad I_b\in\{0,1\}.
\]
\PSmall{$n=20$ definisce l'esperimento binomiale; $B=10000$ definisce la precisione della simulazione.}
''',r'''
\PCode{R · stimare una probabilità}{58_replica_completa.R}
\PSmall{\texttt{rbinom()} genera direttamente il conteggio di ogni replica. Il confronto \texttt{k58 >= 8} produce un vettore logico, la cui media è una frequenza.}
\PInfo{La coda esatta usa \texttt{pbinom(7,...,lower.tail=FALSE)}: l'evento è $K>7$.}
''',"Aumentare B ripete più volte lo stesso esperimento; aumentare n cambia l'esperimento e la probabilità cercata.",MC)
CODES["58_replica_completa.R"]='''set.seed(17)
B58 <- 10000
k58 <- rbinom(B58, 20, .3)
i58 <- k58 >= 8
c(stima = mean(i58),
  esatta = pbinom(7, 20, .3,
    lower.tail = FALSE))
'''

add(59,r"L'errore numerico diminuisce come $1/\sqrt{B}$",r'''
\PLabel{Repliche Bernoulli indipendenti con probabilità $p$}
\[
E[\widehat p_B]=p,\qquad
\operatorname{SE}_{MC}(\widehat p_B)
   =\sqrt{\frac{p(1-p)}{B}}.
\]
'''+table(["Repliche $B$","SE per $p=0{,}1$","Confronto"],
          [["200","0,0212","riferimento"],["800","0,0106","metà SE"],["3200","0,0053","un quarto di SE"]],
          [2.8,3.3,3.2])+r'''
\vspace{2mm}
\PBody{Quadruplicare $B$ dimezza la deviazione standard della stima fra simulazioni ripetute. Il valore di una singola stima può comunque oscillare.}
''',r'''
\PCode{R · precisione teorica}{59_errore_mc.R}
\PSmall{Questa formula riguarda l'errore numerico nella stima di $p$. Il modello della Bernoulli e la probabilità assegnata restano gli stessi.}
\PInfo{Per eventi rari, zero successi simulati non dimostra che $p=0$. La stima di SE ottenuta sostituendo $\widehat p=0$ può essere fuorviante.}
''',"Quattro volte le repliche dimezzano l'errore standard Monte Carlo, senza modificare la variabilità descritta dal modello.",MC)
CODES["59_errore_mc.R"]='''# p e' noto in questo esempio
B59 <- c(200, 800, 3200)
p59 <- .1
se59 <- sqrt(p59*(1-p59)/B59)
data.frame(B = B59, SE_MC = se59)
'''

with (ROOT/"simulation_proof/coordinate/mc_progressivo.csv").open() as f:
    mc_rows=list(csv.DictReader(f))
mc_plot=[(float(r["x"]),float(r["y"])) for r in mc_rows if float(r["x"])>=20]
add(60,"La convergenza non segue una linea regolare",r'''
\PLabel{Una sequenza simulata: $p=0{,}1$, seme 17}
'''+chart([("GeoA",mc_plot),
           ("GeoB",[(20,.1),(2000,.1)])],
          0,2000,.21,[(0,"0"),(500,"500"),(1000,"1000"),(1500,"1500"),(2000,"2000")],
          [(0,"0"),(.1,"0,1"),(.2,"0,2")],"$B$ repliche","Frequenza cumulativa")+r'''
\PBody{La linea blu usa i prefissi della stessa sequenza, dal ventesimo esito. La linea ocra indica la probabilità del modello.}
\PSmall{L'aumento di $B$ riduce la dispersione attesa della stima. Non impone che ogni passo sia più vicino a $p$ del precedente.}
''',r'''
\PCode{R · una frequenza progressiva}{60_convergenza.R}
\PSmall{\texttt{cumsum()} accumula i successi. Il denominatore cresce da 1 a 2000; il grafico mostra come cambia la stima durante una sola esecuzione.}
''',"La stabilizzazione è una proprietà del procedimento; singole oscillazioni restano compatibili con la convergenza.",MC)
CODES["60_convergenza.R"]='''set.seed(17)
B60 <- 2000
i60 <- rbinom(B60, 1, .1)
b60 <- seq_len(B60)
p60 <- cumsum(i60)/b60
plot(b60, p60, type = "l",
     xlab = "Repliche B",
     ylab = "Frequenza cumulativa")
abline(h = .1, col = "#C57E42")
'''

add(61,"Quante repliche servono?",r'''
\PLabel{Fissare un obiettivo per l'errore standard}
\[
\operatorname{SE}_{MC}\leq\varepsilon
\quad\Longrightarrow\quad
B\geq\frac{p(1-p)}{\varepsilon^2}.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] at(2.2,2.35){$p=0{,}1$ noto\\$\varepsilon=0{,}01$\\$B\geq900$};
\node[pFlow,text width=3.8cm,fill=GeoTint] at(7.1,2.35){Qualsiasi $p$\\$p(1-p)\leq1/4$\\$B\geq2500$};
\end{tikzpicture}
\PBody{Il limite riguarda una deviazione standard. Non garantisce che l'errore assoluto di ogni esecuzione sia inferiore a $\varepsilon$.}
\PSmall{Se $p$ è ignoto, un esperimento preliminare può orientare $B$; il limite $1/(4\varepsilon^2)$ evita di usare una stima iniziale troppo ottimistica.}
''',r'''
\PCode{R · progettare B}{61_numero_repliche.R}
\PSmall{\texttt{ceiling()} arrotonda all'intero superiore. Il numero di repliche è una scelta di precisione numerica, da dichiarare con il risultato.}
\PInfo{La formula vale per una probabilità stimata tramite indicatori indipendenti. Altre quantità richiedono una diversa valutazione dell'errore.}
''',"Scegliere B richiede una quantità obiettivo e una precisione numerica esplicita.",MC)
CODES["61_numero_repliche.R"]='''# Obiettivo: SE_MC <= 0.01
eps61 <- .01; p61 <- .1
B61 <- ceiling((p61/eps61) *
               ((1-p61)/eps61))
Bmax61 <- ceiling(1/(4*eps61^2))
c(con_p_noto = B61,
  limite_generale = Bmax61)
'''

add(62,"Il seme rende ripetibile una sequenza",r'''
\PLabel{Ripetibilità nello stesso ambiente di calcolo}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.6cm] (s) at(1.5,3.0){Seme\\\texttt{17}};
\node[pFlow,text width=2.6cm] (g) at(4.7,3.0){Generatore\\e versione di R};
\node[pFlow,text width=2.6cm] (c) at(7.9,3.0){Codice\\e ordine delle chiamate};
\node[pFlow,text width=5.4cm,fill=GeoTint] (r) at(4.7,.9){Stessa sequenza pseudocasuale\\e stessi risultati};
\draw[pEdge](s.south)--++(0,-.5)-|(r.north);
\draw[pEdge](g.south)--(r.north);
\draw[pEdge](c.south)--++(0,-.5)-|(r.north);
\end{tikzpicture}
\PBody{Impostare il seme una volta all'inizio dell'esperimento. Ripristinarlo dentro ogni replica riprodurrebbe sempre la stessa estrazione iniziale.}
''',r'''
\PCode{R · verificare la ripetibilità}{62_seme.R}
\PSmall{\texttt{identical()} deve restituire \texttt{TRUE}. Per condividere un'analisi conservare anche script, parametri, versione di R e tipo di generatore.}
\PInfo{Un seme fissato facilita il confronto e la diagnosi degli errori. Non rende più corretto il modello scelto.}
''',"Il seme identifica una sequenza nel suo ambiente: riproducibilità e validità del modello richiedono controlli distinti.",MC)
CODES["62_seme.R"]='''set.seed(17)
a62 <- rnorm(5)
set.seed(17)
b62 <- rnorm(5)
identical(a62, b62)
RNGkind()
R.version.string
'''

add(63,"Dispersione dell'uscita ed errore della media",r'''
\PLabel{Due domande diverse sugli stessi valori simulati}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=8.3cm] (v) at(4.7,3.1){Valori simulati $Y_1,\ldots,Y_B$};
\node[pFlow,text width=3.8cm] (s) at(2.2,1.15){\textbf{Quanto varia $Y$?}\\$s_Y=\operatorname{sd}(Y_1,\ldots,Y_B)$};
\node[pFlow,text width=3.8cm,fill=GeoTint] (e) at(7.15,1.15){\textbf{Quanto è precisa $\bar Y$?}\\$\widehat{\operatorname{SE}}_{MC}=s_Y/\sqrt B$};
\draw[pEdge](v.south)--++(0,-.3)-|(s.north);
\draw[pEdge](v.south)--++(0,-.3)-|(e.north);
\end{tikzpicture}
\PBody{La prima quantità descrive la distribuzione dell'uscita. La seconda descrive la precisione numerica della sua media stimata.}
\PSmall{La formula del SE richiede repliche indipendenti e varianza finita; non è la formula dell'errore di un quantile.}
''',r'''
\PCode{R · due deviazioni da distinguere}{63_due_errori.R}
\PSmall{Con più repliche, la SD simulata tende alla SD del modello. L'errore Monte Carlo della media diminuisce come $1/\sqrt B$.}
\PInfo{Nella propagazione dell'incertezza, $s_Y$ può rappresentare l'incertezza standard dell'uscita; dividere per $\sqrt B$ ne cambierebbe il significato.}
''',"La SD delle uscite misura la dispersione del modello; la SD della loro media misura la precisione numerica.",MC)
CODES["63_due_errori.R"]='''set.seed(17)
B63 <- 2000
y63 <- rlnorm(B63, 0, .6)
s63 <- sd(y63)
c(SD_uscita = s63,
  SE_media_MC = s63/sqrt(B63))
'''

add(64,"Aumentare B non corregge un errore sistematico",r'''
\PLabel{Esempio: scostamento noto nella misura di massa}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm] (m) at(2.1,3){Massa del provino\\$m_0=106$ g};
\node[pFlow,text width=3.6cm] (b) at(7.1,3){Massa registrata\\$E[M]=108$ g};
\draw[pEdge](m)--node[pNote,above] {$+2$ g} (b);
\node[pFlow,text width=3.6cm,fill=GeoTint] at(2.1,1){$m_0/V_0=2{,}65$\\g/cm$^3$};
\node[pFlow,text width=3.6cm,fill=GeoTint] at(7.1,1){$E[M]/V_0=2{,}70$\\g/cm$^3$};
\end{tikzpicture}
\[
V_0=40\ \mathrm{cm^3}\ \text{fissato},\qquad
\Delta d=\frac{2\ \mathrm g}{40\ \mathrm{cm^3}}=0{,}05\ \mathrm{g/cm^3}.
\]
\PSmall{Lo scostamento è imposto per l'esempio. In un'analisi reale la correzione richiede informazioni di taratura e la sua incertezza.}
''',r'''
\PCode{R · simulare il centro sbagliato}{64_bias.R}
\PSmall{Le due serie usano la stessa massa simulata; nella seconda viene sottratto lo scostamento di 2 g, qui assunto noto esattamente.}
\PInfo{Aumentare le repliche rende più precisa la media del modello impostato, compreso un eventuale centro sbagliato.}
''',"Una simulazione più lunga riduce l'errore numerico; uno scostamento sistematico richiede una correzione fondata su informazioni esterne.",MC)
CODES["64_bias.R"]='''# V fissato; scostamento di 2 g noto
set.seed(17)
m64 <- rnorm(20000, 108, 1)
d64 <- m64/40
dc64 <- (m64-2)/40
c(senza_correzione = mean(d64),
  con_correzione = mean(dc64))
'''

add(65,"Laboratorio: raddoppiare la precisione numerica",r'''
\PLabel{Esperimento m04-monte-carlo}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm] (a) at(2.1,2.9){$p=0{,}1$\\$B=200$\\$\operatorname{SE}_{MC}\simeq0{,}0212$};
\node[pFlow,text width=3.6cm,fill=GeoTint] (b) at(7.1,2.9){$p=0{,}1$\\$B=800$\\$\operatorname{SE}_{MC}\simeq0{,}0106$};
\draw[pEdge](a)--node[pNote,above] {$B\times4$} (b);
\node[pNote,text width=8.6cm] at(4.6,.85){Probabilità, modello e seme restano fissati.\\Cambiano lunghezza della sequenza e precisione attesa.};
\end{tikzpicture}
\PBody{Confrontare la stima finale e il SE teorico. Poi cambiare solo il seme: il SE resta uguale, mentre la stima può cambiare.}
''',r'''
\PCode{R · stesso modello, più repliche}{65_lab_mc.R}
\PSmall{Il rapporto fra i due SE deve essere 2. Il rapporto fra i due errori assoluti osservati non è fissato.}
\PInfo{\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-monte-carlo}{Apri l'esperimento sul sito}. Annotare $B$, $p$, seme, stima e SE prima di trarre una conclusione.}
''',"Una singola esecuzione può migliorare o peggiorare; la precisione attesa si confronta attraverso l'errore standard.",MC)
CODES["65_lab_mc.R"]='''a65 <- lab_monte_carlo(
  B = 200, prob = .1, seed = 17)
b65 <- lab_monte_carlo(
  B = 800, prob = .1, seed = 17)
a65$indicatori
b65$indicatori
a65$indicatori["se_mc_teorico"] /
  b65$indicatori["se_mc_teorico"]
'''

add(66,"La densità dipende da due misure incerte",r'''
\PLabel{Caso guida fisico · massa e volume di un provino}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] (m) at(2.2,3.0){Massa $M$\\$m_0=106$ g,\quad $u_m=1$ g};
\node[pFlow,text width=3.8cm] (v) at(7.1,3.0){Volume $V$\\$V_0=40$ cm$^3$,\quad $u_V=0{,}6$ cm$^3$};
\node[pFlow,text width=5.1cm,fill=GeoTint] (d) at(4.65,1.0){Densità $D=M/V$\\valore di riferimento $d_0=2{,}65$ g/cm$^3$};
\draw[pEdge](m.south)--++(0,-.4)-|(d.north);
\draw[pEdge](v.south)--++(0,-.4)-|(d.north);
\end{tikzpicture}
\PBody{$m_0,V_0$ sono le medie assegnate agli ingressi; $u_m,u_V$ le rispettive deviazioni standard. Il rapporto dei valori centrali è $d_0=m_0/V_0$.}
\PSmall{La lettera $D$ evita di confondere la densità fisica con il parametro di correlazione \texttt{rho} del browser.}
''',r'''
\PCode{R · quantità e unità}{66_densita.R}
\PSmall{L'incertezza è attribuita alla conoscenza di questo provino. Una distribuzione fra provini diversi descriverebbe un'altra fonte di variabilità.}
\PInfo{Per propagare l'incertezza servono distribuzioni degli ingressi e loro dipendenza. Le sole medie non bastano.}
''',"La distribuzione della densità dipende dalle distribuzioni congiunte di massa e volume, oltre che dalla formula del rapporto.",UNC)
CODES["66_densita.R"]='''# Unita': g, cm^3 e g/cm^3
m0 <- 106
V0 <- 40
um <- 1
uV <- .6
d0 <- m0/V0
c(densita = d0, CV_m = um/m0,
  CV_V = uV/V0)
'''

add(67,"Attribuire agli ingressi un modello positivo",r'''
\PLabel{Parametrizzare la lognormale con media e SD originali}
\[
s_\ell^2=\log\!\left[1+(u/\mu)^2\right],\qquad
\mu_\ell=\log\mu-\frac{s_\ell^2}{2}.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (a) at(2.1,2.25){Valori originali\\media $\mu>0$ e SD $u$};
\node[pFlow,text width=3.5cm,fill=GeoTint] (b) at(7.1,2.25){Parametri R\\\texttt{meanlog} $=\mu_\ell$\\\texttt{sdlog} $=s_\ell$};
\draw[pEdge](a)--(b);
\end{tikzpicture}
\PBody{Le formule riproducono esattamente media $\mu$ e SD $u$ del modello lognormale. I valori simulati sono positivi.}
\PSmall{In R si usano valori numerici nelle unità dichiarate: massa in g, volume in cm$^3$. Formalmente i logaritmi sono di rapporti con 1 g o 1 cm$^3$.}
''',r'''
\PCode{R · una funzione riutilizzabile}{67_rpos.R}
\PSmall{\texttt{rpos()} è inclusa nel progetto; qui ne è mostrata la definizione. \texttt{log1p(a)} calcola $\log(1+a)$ con buona precisione per $a$ piccolo.}
\PInfo{La positività è una proprietà del modello. La scelta lognormale resta un'ipotesi didattica da motivare per misure reali.}
''',"Parametrizzare correttamente un generatore richiede distinguere media e SD originali dai parametri della scala logaritmica.",UNC)
CODES["67_rpos.R"]='''# mu e s: media e SD originali
rpos <- function(n, mu, s) {
  v <- log1p((s/mu)^2)
  rlnorm(n, log(mu)-v/2, sqrt(v))
}
set.seed(17)
head(rpos(6, mu = 106, s = 1))
'''

def physical_hist():
    with (ROOT/"simulation_proof/coordinate/densita_fisica_hist.csv").open() as f:
        rows=list(csv.DictReader(f))
    x0,y0,w,h=.72,.58,8.15,2.8
    sx=lambda x:x0+(x-2.4)/.55*w
    sy=lambda y:y0+y/9.5*h
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for y,lab in [(0,"0"),(4,"4"),(8,"8")]:
        out += [rf'\draw[Rule] ({x0},{sy(y):.4f})--({x0+w},{sy(y):.4f});',
                rf'\node[pNote,anchor=east] at ({x0-.12},{sy(y):.4f}) {{{lab}}};']
    for r in rows:
        if float(r['count'])>0:
            out.append(rf'\filldraw[fill=GeoA!32,draw=Paper] ({sx(float(r["left"])):.5f},{y0}) rectangle ({sx(float(r["right"])):.5f},{sy(float(r["density"])):.5f});')
    for x,lab in [(2.4,"2,4"),(2.5,"2,5"),(2.6,"2,6"),(2.7,"2,7"),(2.8,"2,8"),(2.9,"2,9")]:
        out.append(rf'\node[pNote,below] at ({sx(x):.4f},{y0-.12}) {{{lab}}};')
    out += [rf'\draw[pAxis] ({x0},{y0})--({x0+w+.15},{y0});',
            rf'\draw[pAxis] ({x0},{y0})--({x0},{y0+h+.15});',
            rf'\draw[GeoB,dashed,line width=1pt] ({sx(2.65):.5f},{y0})--({sx(2.65):.5f},{y0+h});',
            rf'\node[pNote,anchor=west] at ({x0},{y0+h+.4}) {{Densità di probabilità}};',
            rf'\node[pNote] at ({x0+w/2},-.25) {{$D$ [g/cm$^3$]}};',
            r'\end{tikzpicture}']
    return '\n'.join(out)

add(68,"Propagare le due misure con Monte Carlo",r'''
\PLabel{20000 coppie indipendenti · seme 17}
'''+physical_hist()+r'''
\PSmall{Istogramma di $D_b=M_b/V_b$, classi di 0,02 g/cm$^3$. La linea ocra indica $d_0=2{,}65$ g/cm$^3$.}
\PBody{Risultati simulati: media $2{,}6510$, SD $0{,}0470$ e quantili 2,5\%--97,5\% pari a $[2{,}5606;\,2{,}7442]$ g/cm$^3$.}
''',r'''
\PCode{R · una coppia per replica}{68_simula_densita.R}
\PSmall{\texttt{m68} e \texttt{v68} hanno la stessa lunghezza: la divisione calcola un rapporto per riga. L'indipendenza è una scelta esplicita del caso iniziale.}
\PInfo{I quantili delimitano un intervallo centrale del modello propagato. Non descrivono l'errore Monte Carlo della media.}
''',"La simulazione deve propagare coppie complete di ingressi e conservare le dipendenze previste dal modello.",UNC)
CODES["68_simula_densita.R"]='''# Ingressi indipendenti, positivi
set.seed(17)
B68 <- 20000
m68 <- rpos(B68, 106, 1)
v68 <- rpos(B68, 40, .6)
d68 <- m68/v68
c(media = mean(d68), SD = sd(d68))
quantile(d68, c(.025, .975))
'''

add(69,"La sensibilità locale del rapporto",r'''
\PLabel{Variare il volume vicino a 40 cm$^3$, con massa 106 g}
'''+chart([("GeoA",coords(lambda x:106/x,36,44)),
           ("GeoB",coords(lambda x:2.65-106/40**2*(x-40),36,44))],
          36,44,3.0,[(36,"36"),(40,"40"),(44,"44")],
          [(2.4,"2,4"),(2.65,"2,65"),(2.9,"2,9")],"$V$ [cm$^3$]",
          "$D$ [g/cm$^3$] · asse verticale ingrandito",height=2.1,ymin=2.35)+r'''
\[
\Delta D\simeq\frac{1}{V_0}\Delta M
               -\frac{m_0}{V_0^2}\Delta V.
\]
\PSmall{Blu: rapporto esatto; ocra: retta tangente. Un aumento di massa fa crescere $D$; un aumento di volume la riduce.}
''',r'''
\PCode{R · coefficienti di sensibilità}{69_sensibilita.R}
\PSmall{Le derivate sono valutate in $(m_0,V_0)$. I coefficienti moltiplicano scarti con unità g e cm$^3$, producendo scarti in g/cm$^3$.}
\PInfo{L'approssimazione è locale: occorre che la curvatura conti poco nell'intervallo di valori plausibili degli ingressi.}
''',"Le derivate traducono piccoli scarti degli ingressi in variazioni dell'uscita; il segno è essenziale per la dipendenza.",UNC)
CODES["69_sensibilita.R"]='''m0 <- 106; V0 <- 40
cm69 <- 1/V0
cV69 <- -m0/V0^2
c(sensibilita_massa = cm69,
  sensibilita_volume = cV69)
# Effetto di +1 g e di +0.6 cm^3
c(cm69*1, cV69*.6)
'''

add(70,"Somma dei contributi per ingressi indipendenti",r'''
\PLabel{Approssimazione lineare nel caso guida}
\[
u_D^2\simeq
\left(\frac{u_m}{V_0}\right)^2+
\left(\frac{m_0u_V}{V_0^2}\right)^2.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA] (.45,1.6) rectangle (2.97,2.55);
\fill[GeoB] (2.97,1.6) rectangle (9.35,2.55);
\node[pLabel,text=white] at(1.71,2.08){28,3\%};
\node[pLabel,text=white] at(6.16,2.08){71,7\%};
\node[pNote] at(1.71,1.1){Massa};
\node[pNote] at(6.16,1.1){Volume};
\node[pNote] at(4.9,3.0){Quote della varianza approssimata $u_D^2$};
\end{tikzpicture}
\PBody{$u_D\simeq0{,}04696$ g/cm$^3$. Nel caso indipendente, il volume fornisce il contributo maggiore alla varianza propagata.}
\PSmall{Le quote si riferiscono alla varianza, non alla deviazione standard.}
''',r'''
\PCode{R · contributi e totale}{70_contributi.R}
\PSmall{La radice si applica dopo aver sommato i contributi quadratici. Sommare direttamente le SD darebbe un'altra quantità.}
\PInfo{Il risultato approssimato è vicino alla SD simulata, $0{,}04697$ g/cm$^3$, per le piccole incertezze scelte qui.}
''',"Per ingressi indipendenti la propagazione lineare somma contributi alla varianza, pesati dalle sensibilità.",UNC)
CODES["70_contributi.R"]='''# Contributi in (g/cm^3)^2
q70 <- c(massa = (1/40)^2,
         volume = (106*.6/40^2)^2)
u70 <- sqrt(sum(q70))
c(SD_approssimata = u70)
100*q70/sum(q70)
'''

def correlations():
    out=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for j,c in enumerate([-.7,0,.7]):
        x0=.4+j*3.15
        with (ROOT/f"simulation_proof/coordinate/correlazione_{c if c else 0}.csv").open() as f:
            rows=list(csv.DictReader(f))
        out += [rf'\draw[pAxis] ({x0},.4)--({x0+2.75},.4);',
                rf'\draw[pAxis] ({x0},.4)--({x0},2.6);',
                rf'\node[pNote] at ({x0+1.3},2.96) {{$c={str(c).replace(".",",")}$}};']
        for r in rows:
            x=float(r['x']); y=float(r['y'])
            out.append(rf'\fill[GeoA,opacity=.6] ({x0+(x+3)/6*2.6:.5f},{.4+(y+3)/6*2:.5f}) circle(1.1pt);')
    return '\n'.join(out+[r'\end{tikzpicture}'])

add(71,"La dipendenza modifica l'incertezza del rapporto",r'''
\PLabel{Tre esempi di dipendenza · coordinate standardizzate}
'''+correlations()+r'''
\[
\frac{u_D}{d_0}\simeq
\sqrt{\alpha^2+\beta^2-2c\alpha\beta},
\quad \alpha=\frac{u_m}{m_0},\quad \beta=\frac{u_V}{V_0}.
\]
\PSmall{$c=\operatorname{Corr}(M,V)$ sulla scala originale. La covarianza è $c\,u_m u_V$. Le nubi gaussiane illustrano solo la direzione della dipendenza.}
''',r'''
\PCode{R · cambiare la correlazione}{71_covarianza.R}
\PSmall{Nel rapporto, sensibilità di massa e volume hanno segni opposti. Una correlazione positiva riduce l'incertezza lineare, a marginali fissate.}
\PInfo{La correlazione deve essere stimata o motivata dalle condizioni di misura. Porla uguale a zero è un'ipotesi da esplicitare.}
''',"Nella propagazione di un rapporto, covarianza e segni delle sensibilità determinano quanto gli scarti si compensano.",UNC)
CODES["71_covarianza.R"]='''# c: correlazione sulla scala fisica
c71 <- c(-.7, 0, .7)
a71 <- 1/106
b71 <- .6/40
u71 <- 2.65*sqrt(a71^2+b71^2 -
                 2*c71*a71*b71)
data.frame(c = c71, SD = u71)
'''

add(72,"Generare due ingressi positivi dipendenti",r'''
\PLabel{Il modello adimensionale del laboratorio}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.2cm] (u) at(1.9,3.0){$U,Z$ normali standard\\indipendenti};
\node[pFlow,text width=4.4cm] (v) at(7,3.0){$W=c_\ell U+\sqrt{1-c_\ell^2}\,Z$\\$\operatorname{Corr}(U,W)=c_\ell$};
\node[pFlow,text width=3.3cm,fill=GeoTint] (x) at(1.9,1){$X=10\,e^{sU}$};
\node[pFlow,text width=3.3cm,fill=GeoTint] (y) at(7,1){$Y=5\,e^{sW}$};
\draw[pEdge](u)--(v);
\draw[pEdge](u.south)--(x.north);
\draw[pEdge](v.south)--(y.north);
\end{tikzpicture}
\PBody{Le mediane degli ingressi sono 10 e 5. Il parametro $s$ è la SD dei logaritmi; $c_\ell$ è la loro correlazione.}
\PSmall{È un caso adimensionale distinto dal provino fisico. Il codice usa $B=2000$ coppie e $c_\ell=0{,}7$.}
''',r'''
\PCode{R · mantenere la dipendenza}{72_ingressi_correlati.R}
\PSmall{Ogni riga di \texttt{z72} fornisce due normali indipendenti. La stessa componente \texttt{u72} entra in entrambi gli ingressi e ne crea la dipendenza.}
''',"Un modello congiunto specifica sia le distribuzioni marginali sia il modo in cui gli ingressi variano insieme.",UNC)
CODES["72_ingressi_correlati.R"]='''set.seed(17)
s72 <- .1; c72 <- .7
z72 <- matrix(rnorm(4000), ncol = 2)
u72 <- z72[, 1]
v72 <- c72*u72 +
  sqrt(1-c72^2)*z72[, 2]
x72 <- exp(log(10)+s72*u72)
y72 <- exp(log(5)+s72*v72)
r72 <- x72/y72
sd(r72)
'''

add(73,"Il rapporto lognormale si può calcolare esattamente",r'''
\PLabel{Rapporto $R=X/Y$ nel modello del laboratorio}
\[
\log R=\log2+s(U-W),\qquad
\tau^2=2s^2(1-c_\ell).
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (l) at(2.15,2.1){$\log R\sim N(\log2,\tau^2)$\\varianza dei log nota};
\node[pFlow,text width=3.7cm,fill=GeoTint] (r) at(7.1,2.1){$R$ lognormale\\mediana $=2$};
\draw[pEdge](l)--node[pNote,above] {$\exp$}(r);
\end{tikzpicture}
\[
E[R]=2e^{\tau^2/2},\qquad
u_R=2\sqrt{(e^{\tau^2}-1)e^{\tau^2}}.
\]
\PSmall{Il valore esatto fornisce un riferimento con cui verificare simulazione e approssimazione differenziale.}
''',r'''
\PCode{R · momenti esatti del rapporto}{73_rapporto_esatto.R}
\PSmall{Per $s=0{,}1$ e $c_\ell=0{,}7$, $\tau^2=0{,}006$. La mediana è 2; la media è leggermente maggiore.}
\PInfo{Per $c_\ell=1$ gli stessi fattori moltiplicano $X$ e $Y$: il rapporto è sempre 2 e la sua SD è zero.}
''',"La differenza di logaritmi normali congiunti permette di ricavare la distribuzione esatta del rapporto positivo.",UNC)
CODES["73_rapporto_esatto.R"]='''s73 <- .1; c73 <- .7
t273 <- 2*s73^2*(1-c73)
c(mediana = 2,
  media = 2*exp(t273/2),
  SD = 2*sqrt(expm1(t273) *
                 exp(t273)))
'''

add(74,"Leggere i parametri sulla scala corretta",r'''
\PLabel{Nomi del codice e significato matematico}
'''+table(["Nel codice del sito","Nella lezione","Significato"],
          [[r"\texttt{cv}","$s$","SD dei log"],
           [r"\texttt{rho}","$c_\\ell$","correlazione dei log"]],
          [3.5,2.3,3.6])+r'''
\[
\mathrm{CV}_X=\sqrt{e^{s^2}-1},\qquad
\operatorname{Corr}(X,Y)=
\frac{e^{c_\ell s^2}-1}{e^{s^2}-1}\quad(s>0).
\]
\PBody{Per $s=0{,}3$ e $c_\ell=0{,}7$, le quantità sulla scala originale si ottengono dalle formule. Le due coppie di parametri sono distinte.}
\PSmall{La formula della correlazione vale per il modello con la stessa SD logaritmica $s$ in entrambi gli ingressi.}
''',r'''
\PCode{R · convertire i parametri}{74_scale_parametri.R}
\PSmall{L'interfaccia del laboratorio indica già SD e correlazione dei logaritmi. I nomi interni \texttt{cv} e \texttt{rho} vanno letti con questa definizione.}
\PInfo{La formula lineare della slide 71 usa correlazione e SD sulla scala originale. Inserire direttamente $c_\ell$ introdurrebbe un'approssimazione aggiuntiva.}
''',"La scala fa parte della definizione di un parametro; correlazione e dispersione cambiano sotto trasformazioni non lineari.",UNC)
CODES["74_scale_parametri.R"]='''s74 <- .3; cl74 <- .7
CV74 <- sqrt(expm1(s74^2))
c74 <- expm1(cl74*s74^2) /
       expm1(s74^2)
c(SD_log = s74, CV_originale = CV74,
  cor_log = cl74, cor_originale = c74)
'''

add(75,"Quando la linearizzazione perde precisione",r'''
\PLabel{Rapporto del laboratorio con $c_\ell=0$}
'''+chart([("GeoA",coords(lambda s:2*math.sqrt(math.expm1(2*s*s)*math.exp(2*s*s)),0,.3)),
           ("GeoB",coords(lambda s:2*s*math.sqrt(2),0,.3))],
          0,.3,1,[(0,"0"),(.1,"0,1"),(.2,"0,2"),(.3,"0,3")],
          [(0,"0"),(.5,"0,5"),(1,"1")],"$s$: SD dei log","SD del rapporto",height=2.4)+r'''
\[
u_{R,\mathrm{lin}}\simeq2s\sqrt{2(1-c_\ell)}.
\]
\PSmall{Blu: SD esatta; ocra: approssimazione differenziale sui log. Lo scarto cresce con la dispersione degli ingressi.}
''',r'''
\PCode{R · confrontare i due calcoli}{75_confronto_approssimazione.R}
\PSmall{Nel browser questo confronto usa $s$ fra 0,02 e 0,30. La simulazione aggiunge errore numerico a una SD esatta che qui è disponibile.}
\PInfo{Un accordo fra due metodi con ingressi identici verifica il calcolo; non convalida da solo le distribuzioni assegnate agli ingressi.}
''',"La linearizzazione deve essere confrontata con la curvatura del modello e con l'ampiezza degli ingressi plausibili.",UNC)
CODES["75_confronto_approssimazione.R"]='''# Correlazione dei log uguale a 0
s75 <- c(.02, .1, .2, .3)
t275 <- 2*s75^2
a75 <- 2*sqrt(t275)
e75 <- 2*sqrt(expm1(t275)*exp(t275))
data.frame(sdlog = s75,
  approssimata = a75, esatta = e75,
  scarto_percento = 100*(e75-a75)/e75)
'''

add(76,"Laboratorio: dipendenza e incertezza del rapporto",r'''
\PLabel{Esperimento m04-propagazione · 2000 coppie}
'''+table(["Scenario","$s$","$c_\\ell$","Che cosa cambia"],
          [["A","0,10","0","riferimento"],
           ["B","0,10","0,70","dipendenza"],
           ["C","0,30","0","dispersione"]],
          [1.7,1.4,1.4,4.8])+r'''
\vspace{3mm}
\PBody{Confrontare SD simulata, SD differenziale sui log e SD esatta. Motivare il verso del cambiamento prima di eseguire il calcolo.}
\PSmall{A/B modifica solo la dipendenza; A/C modifica solo la dispersione. Il seme rimane 17. Cambiare poi il seme distingue lo scarto numerico da quello dell'approssimazione.}
''',r'''
\PCode{R · tre scenari confrontabili}{76_lab_propagazione.R}
\PSmall{Il primo argomento nominato è la correlazione dei log; \texttt{cv} è la loro SD. Le mediane restano 10 e 5.}
\PInfo{\href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-propagazione}{Apri l'esperimento sul sito}. Il rapporto è adimensionale; non usare le unità del caso fisico.}
''',"Un confronto informativo cambia un parametro alla volta e distingue errore Monte Carlo, approssimazione e ipotesi del modello.",UNC)
CODES["76_lab_propagazione.R"]='''a76 <- lab_propagazione(
  rho = 0, cv = .1, seed = 17)
b76 <- lab_propagazione(
  rho = .7, cv = .1, seed = 17)
c76 <- lab_propagazione(
  rho = 0, cv = .3, seed = 17)
rbind(A = a76$indicatori,
      B = b76$indicatori,
      C = c76$indicatori)
'''
