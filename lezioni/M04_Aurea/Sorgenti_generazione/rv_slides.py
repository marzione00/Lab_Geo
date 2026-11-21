from pathlib import Path
import csv
SLIDES={}; CODES={}
ROOT=Path(__file__).resolve().parent

def S(n,title,left,right,recall,section='VARIABILI E DISTRIBUZIONI'):
    SLIDES[n]=dict(title=title,section=section,left=left,right=right,recall=recall)
def coords(points):
    return ' '.join(f'({x:.5f},{y:.5f})' for x,y in points)

CODES['18_variabile.R']='''# Due prove indipendenti, p=.3
esiti18 <- c("00","01","10","11")
x18 <- c(0, 1, 1, 2)  # successi
p18 <- c(.49, .21, .21, .09)
# Somma i pesi per lo stesso X
tapply(p18, x18, sum)
'''
S(18,'Una variabile assegna numeri agli esiti',r'''
\PLabel{$X:\Omega\longrightarrow\mathbb R$}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \y/\lab/\p in {4/00/{0{,}49},3/01/{0{,}21},2/10/{0{,}21},1/11/{0{,}09}}{
\node[pFlow,minimum height=.7cm,text width=2.7cm] (s\lab) at(1.9,\y){$\lab\quad P=\p$};}
\node[pFlow,text width=2.5cm] (z) at(7.1,4){$X=0$};
\node[pFlow,text width=2.5cm] (u) at(7.1,2.5){$X=1$};
\node[pFlow,text width=2.5cm] (d) at(7.1,1){$X=2$};
\draw[pEdge](s00)--(z);\draw[pEdge](s01)--(u);\draw[pEdge](s10)--(u);\draw[pEdge](s11)--(d);
\node[pNote] at(1.9,.25){sequenza delle prove};
\node[pNote] at(7.1,.25){numero di successi};
\end{tikzpicture}
\PBody{Esiti diversi possono produrre lo stesso numero. La distribuzione di $X$ somma le probabilità degli esiti che portano a quel valore.}
''',r'''
\PCode{R · raggruppare gli esiti}{18_variabile.R}
\PSmall{Con prove indipendenti e $p=0{,}3$, la sequenza 01 pesa $0{,}7\cdot0{,}3=0{,}21$. Anche 10 pesa 0,21.}
\PInfo{Quindi $P(X=1)=0{,}21+0{,}21=0{,}42$. Il conteggio perde l'ordine delle due prove.}
''','Una variabile casuale associa un numero a ciascun esito; la sua distribuzione trasferisce a quei numeri le probabilità.')

CODES['19_massa.R']='''k19 <- 0:2
p19 <- c(.49, .42, .09)
sum(p19)             # 1
sum(p19[k19 >= 1])    # .51
sum(k19 * p19)        # atteso .6
barplot(p19, names.arg=k19,
  xlab="Successi", ylab="Probabilita'")
'''
S(19,'La massa di probabilità discreta',r'''
\PLabel{$p_X(k)=P(X=k)$}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.4,.2)--(8.8,.2);\draw[pAxis](.4,.2)--(.4,3.1);
\foreach \x/\y/\p/\k in {1.6/2.65/{0{,}49}/0,4.3/2.3/{0{,}42}/1,7/.65/{0{,}09}/2}{
\draw[GeoA,line width=10pt](\x,.2)--(\x,\y);
\node[pNote] at(\x,\y+.3){$\p$};\node[pNote] at(\x,-.1){$\k$};}
\draw[GeoB,line width=1pt](3.6,-.55)--(7.7,-.55);
\node[pNote,text=GeoB] at(5.65,-.8){$P(X\ge1)=0{,}42+0{,}09=0{,}51$};
\end{tikzpicture}
\[
p_X(k)\ge0,\qquad \sum_k p_X(k)=1.
\]
\PSmall{Le barre rappresentano le masse sui valori possibili. Le probabilità degli eventi si ottengono sommando.}
''',r'''
\PCode{R · sommare le masse}{19_massa.R}
\PSmall{\texttt{k19>=1} seleziona i valori inclusi nell'evento. Le masse sono pesi del modello e sommano a uno.}
\PInfo{La media teorica vale 0,6 successi. Una singola osservazione di $X$ può valere solo 0, 1 o 2.}
''','Per una variabile discreta, le probabilità dei singoli valori sono masse che si sommano.')

CODES['20_densita.R']='''# Modello uniforme fra 0 e 2
dunif(.75, min=0, max=2)   # .5
# Probabilita' tra .5 e 1
punif(1, 0, 2) - punif(.5, 0, 2)
# .25: altezza .5 per larghezza .5
'''
S(20,'La probabilità continua è un’area',r'''
\PLabel{Una variabile uniforme su $[0,2]$, adimensionale}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!12](1,.3) rectangle(8,3.1);
\fill[Classical!75](2.75,.3) rectangle(4.5,3.1);
\draw[GeoA,line width=1pt](1,.3)--(1,3.1)--(8,3.1)--(8,.3);
\draw[pAxis](.5,.3)--(9,.3);\draw[pAxis](1,.3)--(1,3.6);
\foreach \x/\lab in {1/0,2.75/{0{,}5},4.5/1,8/2}{\node[pNote] at(\x,-.1){$\lab$};}
\node[pNote,anchor=east] at(.8,3.1){$0{,}5$};
\node[pLabel,text=white,rotate=90] at(3.625,1.7){area $0{,}25$};
\node[pNote] at(6.3,1.7){$f(x)=1/2$};
\end{tikzpicture}
\[
P(0{,}5<X\le1)=\int_{0{,}5}^{1}\tfrac12\,dx=0{,}25.
\]
\PSmall{La larghezza dell'intervallo è 0,5. L'altezza della densità è 0,5. Il prodotto restituisce la probabilità.}
''',r'''
\PCode{R · densità e cumulata}{20_densita.R}
\PSmall{\texttt{dunif()} restituisce l'altezza. \texttt{punif()} restituisce la probabilità cumulata fino alla soglia.}
\PInfo{Per una distribuzione con densità, $P(X=x)=0$ per ogni singolo punto. Le probabilità riguardano intervalli o insiemi di valori.}
''','L’altezza della densità e la probabilità hanno significati diversi: la probabilità continua si calcola integrando.')

CODES['21_altezza.R']='''# X uniforme [0, .2], adimensionale
dunif(.1, 0, .2)        # densita' 5
punif(.15, 0, .2) -
  punif(.05, 0, .2)     # area .5
# Il punto singolo ha area zero
punif(.1, 0, .2) - punif(.1, 0, .2)
'''
S(21,'Una densità può superare uno',r'''
\PLabel{Uniforme su un intervallo più stretto}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!15](1,.3) rectangle(8,3.6);
\fill[Classical!65](2.75,.3) rectangle(6.25,3.6);
\draw[GeoA,line width=1pt](1,.3)--(1,3.6)--(8,3.6)--(8,.3);
\draw[pAxis](.5,.3)--(9,.3);\draw[pAxis](1,.3)--(1,4);
\foreach \x/\lab in {1/0,2.75/{0{,}05},6.25/{0{,}15},8/{0{,}2}}{\node[pNote] at(\x,-.1){$\lab$};}
\node[pNote,anchor=east] at(.8,3.6){$5$};
\node[pLabel,text=white] at(4.5,2){area $=5\cdot0{,}1=0{,}5$};
\end{tikzpicture}
\[
\int_0^{0{,}2}5\,dx=1.
\]
\PSmall{Il vincolo $[0,1]$ riguarda la probabilità. Se $X$ ha un'unità fisica, la densità ha l'unità inversa.}
''',r'''
\PCode{R · un’altezza pari a cinque}{21_altezza.R}
\PBody{Accorciare il supporto dell'uniforme aumenta l'altezza necessaria a conservare area totale uno.}
\PInfo{Il valore letto su un asse di densità richiede anche la scala e l'unità della variabile. La probabilità resta adimensionale.}
''','Una densità alta è compatibile con una probabilità totale pari a uno quando il supporto è sufficientemente stretto.')

CODES['22_cumulativa.R']='''k22 <- 0:2
p22 <- c(.49, .42, .09)
cumsum(p22)           # .49,.91,1
# Caso continuo: uniforme [0,2]
punif(c(0,.5,1,2), 0, 2)
# .00, .25, .50, 1.00
'''
S(22,'La funzione di distribuzione cumulativa',r'''
\PLabel{$F_X(x)=P(X\le x)$}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,.2)--(9,.2);\draw[pAxis](.5,.2)--(.5,3.9);
\draw[GeoA,line width=1.1pt](.5,.2)--(1.5,.2);
\draw[GeoA,line width=1.1pt](1.5,1.866)--(4.2,1.866);
\draw[GeoA,line width=1.1pt](4.2,3.294)--(6.9,3.294);
\draw[GeoA,line width=1.1pt](6.9,3.6)--(8.7,3.6);
\foreach \x/\y in {1.5/1.866,4.2/3.294,6.9/3.6}{\fill[GeoA](\x,\y) circle(2.3pt);}
\foreach \x/\y in {1.5/.2,4.2/1.866,6.9/3.294}{\draw[GeoA,fill=Paper](\x,\y) circle(2.3pt);}
\foreach \x/\lab in {1.5/0,4.2/1,6.9/2}{\node[pNote] at(\x,-.1){\lab};}
\foreach \y/\lab in {1.866/{0{,}49},3.294/{0{,}91},3.6/1}{\node[pNote,anchor=east] at(.3,\y){$\lab$};}
\node[pNote] at(4.8,-.55){soglia $x$};
\end{tikzpicture}
\PSmall{Nel modello discreto, il salto in $k$ ha ampiezza $P(X=k)$. La cumulativa è non decrescente e comprende il valore alla soglia.}
\[
P(a<X\le b)=F_X(b)-F_X(a).
\]
''',r'''
\PCode{R · accumulare le probabilità}{22_cumulativa.R}
\PSmall{Per la variabile discreta delle pagine precedenti, $F(1)=0{,}49+0{,}42=0{,}91$.}
\PInfo{La differenza di cumulative vale anche nel continuo. Nel discreto occorre leggere con attenzione gli estremi inclusi ed esclusi.}
''','La cumulativa raccoglie tutta la probabilità fino alla soglia, compresa la massa eventualmente presente sulla soglia.')

CODES['23_momenti.R']='''k23 <- 0:2
p23 <- c(.49, .42, .09)
mu23 <- sum(k23*p23)
v23 <- sum((k23-mu23)^2*p23)
c(media=mu23, varianza=v23,
  sd=sqrt(v23))
# .6, .42, circa .6481
'''
S(23,'Media e varianza del modello',r'''
\PLabel{Il centro e gli scarti pesati dalle probabilità}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,1.2)--(9,1.2);
\foreach \x/\k/\sz in {1.3/0/6,4.4/1/5.555,7.5/2/2.5714}{
\fill[GeoA](\x,1.2) circle(\sz pt);\node[pNote] at(\x,.7){$\k$};}
\draw[GeoB,line width=1pt](3.16,.9)--(3.16,3);
\node[pNote,text=GeoB] at(3.16,3.3){$\mu=0{,}6$};
\draw[pEdge](3.16,2.5)--(1.3,2.5);
\draw[pEdge](3.16,2.0)--(4.4,2.0);
\draw[pEdge](3.16,1.6)--(7.5,1.6);
\node[pNote] at(6.8,3.1){area dei punti $\propto p_X(k)$};
\end{tikzpicture}
\[
\mu=\mathbb E[X],\qquad
\sigma^2=\mathbb E[(X-\mu)^2],\qquad
\sigma=\sqrt{\sigma^2}.
\]
\PSmall{Nel continuo, le somme pesate diventano integrali contro la densità. Queste quantità richiedono momenti finiti.}
''',r'''
\PCode{R · momenti teorici}{23_momenti.R}
\PSmall{I pesi sommano a uno. La formula è quella del modello e non usa il divisore campionario $n-1$.}
\PInfo{Se $X$ è una lunghezza in mm, $\sigma$ è in mm e $\sigma^2$ in mm$^2$. Media e deviazione standard conservano l'unità originale.}
''','Media e varianza del modello usano le probabilità; le statistiche campionarie usano le osservazioni disponibili.')

CODES['24_quantile.R']='''# Uniforme [0,2]: F(q)=.75
qunif(.75, min=0, max=2)  # 1.5
# Caso discreto delle pagine 18-23
k24 <- 0:2
F24 <- cumsum(c(.49,.42,.09))
k24[which(F24 >= .75)[1]] # 1
# F(1)=.91: il salto supera .75
'''
S(24,'Il quantile inverte la cumulativa',r'''
\PLabel{La soglia che raggiunge una probabilità assegnata}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.3)--(9,.3);\draw[pAxis](.7,.3)--(.7,4);
\draw[GeoA,line width=1.1pt](.7,.3)--(8.3,3.7);
\draw[GeoB,dashed,line width=.9pt](.7,2.85)--(6.4,2.85)--(6.4,.3);
\node[pNote,anchor=east] at(.5,2.85){$0{,}75$};
\node[pNote] at(6.4,-.05){$q_{0{,}75}=1{,}5$};
\node[pNote] at(8.3,-.05){2};
\node[pNote,anchor=east] at(.5,3.7){1};
\node[pLabel] at(3.5,3.8){$X\sim U(0,2)$};
\fill[GeoB](6.4,2.85) circle(2.4pt);
\end{tikzpicture}
\[
q_\alpha=\inf\{x:F_X(x)\ge\alpha\},\quad0<\alpha<1.
\]
\PSmall{Per il discreto, il quantile è il primo valore che raggiunge o supera $\alpha$. L'uguaglianza $F(q_\alpha)=\alpha$ può fallire.}
''',r'''
\PCode{R · dal livello alla soglia}{24_quantile.R}
\PSmall{\texttt{qunif()} lavora sul modello uniforme. \texttt{quantile(x)} calcola invece quantili da un vettore di dati, con una convenzione di interpolazione.}
\PInfo{Nel caso discreto, $q_{0{,}75}=1$ perché $F(0)=0{,}49<0{,}75$ e $F(1)=0{,}91\ge0{,}75$.}
''','Il quantile risponde alla domanda inversa: quale soglia raccoglie almeno la probabilità richiesta?')

CODES['25_lab_distribuzione.R']='''a25 <- lab_distribuzione(cut=1)
a25$indicatori
# Probabilita' esatte della normale
pnorm(1)              # circa .8413
pnorm(1, lower.tail=FALSE)
b25 <- lab_distribuzione(cut=0)
b25$indicatori        # .5 e .5
'''
normal=list(csv.DictReader((ROOT/'root_proof/normale_25.csv').open()))
npts=[(.6+(float(r['z'])+4),.2+float(r['densita'])*8) for r in normal]
nshade=[p for p,r in zip(npts,normal) if float(r['z'])<=1]
S(25,'Laboratorio: soglia, area e cumulata',r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-distribuzione}{Esperimento m04-distribuzione}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[Classical!25](.6,.2)--'''+ ' -- '.join(f'({x:.5f},{y:.5f})' for x,y in nshade)+r'''--(5.6,.2)--cycle;
\draw[pAxis](.4,.2)--(9,.2);
\draw[GeoA,line width=1.1pt] plot coordinates{'''+coords(npts)+r'''};
\draw[GeoB,dashed](5.6,.2)--(5.6,3.6);
\foreach \x/\lab in {.6/{-4},4.6/0,5.6/1,8.6/4}{\node[pNote] at(\x,-.1){$\lab$};}
\node[pLabel] at(3.8,1.3){$F(1)\simeq0{,}8413$};
\node[pNote] at(4.7,-.55){soglia standardizzata $z$};
\end{tikzpicture}
\PBody{Spostare la soglia modifica l'area cumulata, mentre la curva della normale standard rimane la stessa.}
\PSmall{Il disegno mostra $[-4,4]$. Gli indicatori usano \texttt{pnorm()} sull'intera distribuzione, comprese le code esterne al grafico.}
''',r'''
\PCode{R · cumulata e superamento}{25_lab_distribuzione.R}
\PSmall{\texttt{lower.tail=FALSE} restituisce $P(Z>z)$. La cumulata e il superamento sommano a uno.}
\PInfo{Il calcolo è deterministico. La normale standard sarà studiata nel blocco dedicato a posizione, scala e quantili.}
''','La soglia determina una probabilità cumulata; il taglio grafico delle code non cambia il calcolo analitico.',
section='LABORATORIO · DISTRIBUZIONE')

