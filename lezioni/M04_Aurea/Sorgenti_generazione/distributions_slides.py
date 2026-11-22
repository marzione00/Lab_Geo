"""Aurea M04, slide 26–49: Bernoulli, binomiale, Poisson, normale.

Coordinate teoriche calcolate con le formule esplicite; frequenze della
slide 32 calcolate da R (seed 17) in distributions_proof/calcoli_figure.R.
"""
from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parent
FIG = ROOT / 'distributions_proof/figure_data'
SLIDES, CODES = {}, {}
BIN = 'BERNOULLI E BINOMIALE'
POI = 'POISSON ED ESPOSIZIONE'
NOR = 'DISTRIBUZIONE NORMALE'

def S(n, title, section, left, right, recall):
    SLIDES[n] = dict(title=title, section=section, left=left, right=right, recall=recall)

def fmt(x, d=2):
    return f'{x:.{d}f}'.rstrip('0').rstrip('.').replace('.', '{,}')

def binom(k, n=20, p=.3):
    return math.comb(n, k)*p**k*(1-p)**(n-k) if 0 <= k <= n else 0

def pois(k, mu=6):
    return math.exp(-mu)*mu**k/math.factorial(k)

def normal(x, mu=10, sd=2):
    return math.exp(-.5*((x-mu)/sd)**2)/(sd*math.sqrt(2*math.pi))

def axes(xmin, xmax, ymax, xticks, yticks, xlab, ylab, h=2.45):
    xx = lambda v: .85 + 8*(v-xmin)/(xmax-xmin)
    yy = lambda v: h*v/ymax
    o = [r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for v in yticks:
        o += [fr'\draw[Rule] (.85,{yy(v):.4f})--(8.85,{yy(v):.4f});',
              fr'\node[pNote,anchor=east] at (.7,{yy(v):.4f}) {{{fmt(v)}}};']
    o += [fr'\draw[pAxis] (.85,0)--(9.05,0);',
          fr'\draw[pAxis] (.85,0)--(.85,{h+.18});']
    for v in xticks:
        o.append(fr'\draw[Muted] ({xx(v):.4f},0)--({xx(v):.4f},-.08);\node[pNote,below] at ({xx(v):.4f},-.1) {{{fmt(v)}}};')
    o += [fr'\node[pNote] at (4.85,-.65) {{{xlab}}};',
          fr'\node[pNote,rotate=90] at (-.18,{h/2}) {{{ylab}}};']
    return o, xx, yy

def finish(o):
    return '\n'.join(o+[r'\end{tikzpicture}'])

def curve(o, values, xx, yy, color='GeoA', extra=''):
    o.append(fr'\draw[{color},line width=1.15pt,{extra}] plot coordinates {{'+
             ' '.join(f'({xx(x):.4f},{yy(y):.4f})' for x,y in values)+'};')

def stem_chart(probs, xmax=20, highlight=None, label=None, second=None,
               xmax_plot=None, ymax=.22, xticks=None, h=2.45):
    xmax_plot = xmax if xmax_plot is None else xmax_plot
    xticks = xticks or list(range(0,xmax_plot+1,5))
    o, xx, yy = axes(-.6, xmax_plot+.6, ymax, xticks,
                    [0,.1,.2] if ymax>.2 else [0,.05,.1,.15],
                    '$k$: numero di eventi', '$P(K=k)$', h)
    for k,p in enumerate(probs):
        col = 'GeoB' if highlight and highlight(k) else 'GeoA'
        o.append(fr'\draw[{col},line width=2pt] ({xx(k):.4f},0)--({xx(k):.4f},{yy(p):.4f});')
    if second is not None:
        for k,p in enumerate(second):
            o.append(fr'\fill[GeoB] ({xx(k):.4f},{yy(p):.4f}) circle(2.3pt);')
    if label:
        o.append(fr'\node[pNote,anchor=north east] at (8.9,{h+.05}) {{{label}}};')
    return finish(o)

def norm_chart(mu=10, sd=2, xmin=2, xmax=18, shade=None,
               xticks=(2,6,10,14,18), color='GeoA', h=2.45,
               marks=(), label=None, ymax=None):
    ymax = ymax or 1/(sd*math.sqrt(2*math.pi))*1.15
    o, xx, yy = axes(xmin,xmax,ymax,xticks,[], '$x$', '$f_X(x)$',h)
    if shade is not None:
        a,b = max(xmin,shade[0]), min(xmax,shade[1])
        xs = [a+(b-a)*i/100 for i in range(101)]
        path = [f'({xx(a):.4f},0)']+[f'({xx(x):.4f},{yy(normal(x,mu,sd)):.4f})' for x in xs]+[f'({xx(b):.4f},0)']
        o.append(fr'\fill[{color}!22] '+' -- '.join(path)+' -- cycle;')
    xs = [xmin+(xmax-xmin)*i/200 for i in range(201)]
    curve(o, [(x,normal(x,mu,sd)) for x in xs],xx,yy,color)
    for x,lab in marks:
        o.append(fr'\draw[GeoB,dashed] ({xx(x):.4f},0)--({xx(x):.4f},{yy(normal(x,mu,sd)):.4f});')
        o.append(fr'\node[pNote,anchor=south] at ({xx(x):.4f},{yy(normal(x,mu,sd))+.08:.4f}) {{{lab}}};')
    if label:
        o.append(fr'\node[pNote,anchor=north east] at (8.9,{h+.05}) {{{label}}};')
    return finish(o)

def table(headers,rows,widths):
    o=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    w=sum(widths); h=.68
    o.append(fr'\fill[GeoTint] (0,0) rectangle ({w},{h});')
    for j,row in enumerate([headers]+rows):
        a=0
        for text,cw in zip(row,widths):
            o.append(fr'\node[font=\fontsize{{9.8}}{{12.1}}\selectfont,text=Ink,anchor=west] at ({a+.12},{h/2-j*h}) {{{text}}};')
            a+=cw
        o.append(fr'\draw[Rule] (0,{-j*h})--({w},{-j*h});')
    return finish(o)


CODES['26_bernoulli.R'] = '''# Una prova: evento presente = 1
set.seed(17)
x26 <- rbinom(12, size = 1,
             prob = .3)
x26
mean(x26)  # Frequenza osservata
# Media e varianza del modello
c(media = .3, varianza = .3*.7)
'''
S(26,'Una prova, due esiti: Bernoulli',BIN,r'''
\PLabel{Un indicatore assegna 1 all'evento e 0 al complemento}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.6cm] (a) at(1.6,1.65){Una prova\\evento $A$?};
\node[pFlow,text width=3.3cm,fill=GeoA!10] (b) at(7,2.75){$X=1$\\probabilità $p$};
\node[pFlow,text width=3.3cm,fill=GeoB!10] (c) at(7,.55){$X=0$\\probabilità $1-p$};
\draw[pEdge](a.east)--++(.9,0)|-(b.west);
\draw[pEdge](a.east)--++(.9,0)|-(c.west);
\end{tikzpicture}
\[
X\sim\operatorname{Bern}(p),\quad
\operatorname E[X]=p,\quad
\operatorname{Var}(X)=p(1-p).
\]
\PSmall{$0\le p\le1$. Un esempio: rilevare una frattura in un provino secondo un criterio fissato prima dell'osservazione.}
''',r'''
\PCode{R · simulare indicatori}{26_bernoulli.R}
\PSmall{In \texttt{rbinom()}, \texttt{size=1} indica una sola prova per valore. Il primo argomento chiede 12 valori simulati.}
\PInfo{La media del modello è $p$. La frequenza ottenuta in una breve simulazione può discostarsene.}
''','Bernoulli descrive un singolo evento binario. Il parametro p è la probabilità assegnata all’esito 1.')

CODES['27_somma_prove.R'] = '''# Una sequenza costruita di 20 prove
x27 <- c(1,0,0,1,0, 0,1,0,0,0,
         1,0,0,0,1, 0,0,1,0,0)
length(x27)  # Numero di prove n
sum(x27)     # Numero di successi K
mean(x27)    # Proporzione K/n
'''
S(27,'Dalle prove al numero di successi',BIN,r'''
\PLabel{Esempio costruito: 20 provini, 6 positivi}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \i/\v in {0/1,1/0,2/0,3/1,4/0,5/0,6/1,7/0,8/0,9/0,
10/1,11/0,12/0,13/0,14/1,15/0,16/0,17/1,18/0,19/0}{
\pgfmathtruncatemacro{\row}{int(\i/10)}
\pgfmathtruncatemacro{\col}{mod(\i,10)}
\ifnum\v=1\relax
\node[draw=GeoA,fill=GeoA!16,minimum size=.65cm,pLabel] at(.5+.9*\col,2.3-1.0*\row){\v};
\else
\node[draw=Rule,fill=white,minimum size=.65cm,pLabel] at(.5+.9*\col,2.3-1.0*\row){\v};
\fi
}
\node[pNote] at(4.55,.35){Ogni casella è una prova; ogni 1 contribuisce al conteggio.};
\end{tikzpicture}
\[
K=\sum_{i=1}^{n}X_i,\qquad K\in\{0,1,\ldots,n\}.
\]
\PBody{Con $n$ prove indipendenti e la stessa probabilità $p$, il conteggio $K$ segue una distribuzione binomiale.}
''',r'''
\PCode{R · prove, conteggio, proporzione}{27_somma_prove.R}
\PInfo{Tre quantità: $n=20$ prove; $K=6$ successi nella sequenza; $K/n=0{,}30$ come proporzione osservata.}
\PSmall{Il numero di prove si fissa prima. Un campionamento senza reinserimento da una piccola popolazione richiede un modello diverso.}
''','La binomiale conta i successi in un numero fissato di prove indipendenti con probabilità comune.')

CODES['28_probabilita_binomiale.R'] = '''# Esattamente 2 successi su 3
p28 <- .3
choose(3, 2) * p28^2 * (1-p28)
dbinom(2, size = 3, prob = p28)
# Esattamente 8 su 20
dbinom(8, size = 20, prob = .3)
'''
S(28,'La formula conta tutte le sequenze possibili',BIN,r'''
\PLabel{Tre modi per ottenere due successi su tre prove}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \y/\a/\b/\c in {2.65/1/1/0,1.65/1/0/1,.65/0/1/1}{
\node[pFlow,minimum width=.8cm,minimum height=.65cm] at(.8,\y){\a};
\node[pFlow,minimum width=.8cm,minimum height=.65cm] at(2.1,\y){\b};
\node[pFlow,minimum width=.8cm,minimum height=.65cm] at(3.4,\y){\c};
\draw[pEdge](4,\y)--(5.2,\y);
\node[pLabel,anchor=west] at(5.4,\y){probabilità $p^2(1-p)$};
}
\end{tikzpicture}
\[
P(K=k)=\binom nk p^k(1-p)^{n-k}.
\]
\PSmall{$\binom nk$ conta le posizioni dei $k$ successi. L'indipendenza consente di moltiplicare le probabilità delle singole prove.}
''',r'''
\PCode{R · formula e funzione}{28_probabilita_binomiale.R}
\PSmall{\texttt{choose(n,k)} calcola il coefficiente binomiale. \texttt{dbinom()} restituisce la probabilità del singolo conteggio indicato.}
\PInfo{Per $n=20$, $p=0{,}3$: $P(K=8)\simeq0{,}1144$. La probabilità di \emph{almeno} 8 comprende altri conteggi.}
''','La probabilità di un conteggio somma quelle di tutte le sequenze che producono lo stesso numero di successi.')

CODES['29_centro_dispersione.R'] = '''# Parametri del modello
n29 <- 20
p29 <- .3
c(media = n29*p29,
  varianza = n29*p29*(1-p29))
k29 <- 0:n29
sum(k29 * dbinom(k29, n29, p29))
sqrt(n29*p29*(1-p29))  # SD
'''
S(29,'Media e dispersione del conteggio',BIN,r'''
\PLabel{Distribuzione teorica: $n=20$, $p=0{,}3$}
'''+stem_chart([binom(k) for k in range(21)],label=r'$E[K]=6$')+r'''
\[
\operatorname E[K]=np=6,\qquad
\operatorname{Var}(K)=np(1-p)=4{,}2.
\]
\PSmall{La deviazione standard è $\sqrt{4{,}2}\simeq2{,}05$ successi. La media teorica può essere non intera anche se ogni conteggio è intero.}
''',r'''
\PCode{R · momenti del modello}{29_centro_dispersione.R}
\PSmall{Il prodotto \texttt{k29 * dbinom(...)} pesa ogni conteggio con la sua probabilità. La somma ricostruisce la media teorica.}
''','Per la binomiale la media vale np e la varianza np(1−p). Descrivono la distribuzione dei conteggi.')

CODES['30_coda_binomiale.R'] = '''# Almeno 8: sommare k = 8,...,20
sum(dbinom(8:20, 20, .3))
# lower.tail=FALSE calcola P(K>q)
pbinom(7, size = 20, prob = .3,
       lower.tail = FALSE)
# P(K=8) e' una sola probabilita
dbinom(8, 20, .3)
'''
S(30,'«Almeno 8» comprende 8, 9, 10, …',BIN,r'''
\PLabel{La coda discreta inizia dal valore incluso}
'''+stem_chart([binom(k) for k in range(21)],
              highlight=lambda k:k>=8,label=r'arancio: $K\ge8$')+r'''
\[
P(K\ge8)=1-P(K\le7)\simeq0{,}2277.
\]
\PBody{Con conteggi interi, $K\ge8$ equivale a $K>7$. Scrivere prima l'evento evita di spostare la soglia di una unità.}
''',r'''
\PCode{R · due calcoli equivalenti}{30_coda_binomiale.R}
\PInfo{\texttt{pbinom(8,...,lower.tail=FALSE)} calcolerebbe $P(K>8)$, escludendo il caso $K=8$.}
\PSmall{Le barre rappresentano masse di probabilità su valori interi; la probabilità di un insieme è la loro somma.}
''','Le disuguaglianze strette e inclusive producono risultati diversi per una variabile discreta.')

CODES['31_quattro_funzioni.R'] = '''# d: probabilita del valore
dbinom(8, 20, .3)
# p: probabilita cumulata
pbinom(8, 20, .3)
# q: primo k con F(k) >= .95
qbinom(.95, 20, .3)
# r: cinque conteggi simulati
set.seed(17)
rbinom(5, size = 20, prob = .3)
'''
S(31,'Quattro prefissi, quattro domande',BIN,r'''
\PLabel{Stessi prefissi nelle diverse distribuzioni}
'''+table(['Prefisso','Domanda','Risultato'],[
    [r'\texttt{d}',r'$P(K=8)$','una probabilità'],
    [r'\texttt{p}',r'$P(K\le8)$','una cumulata'],
    [r'\texttt{q}',r'quale soglia per $0{,}95$?','un conteggio'],
    [r'\texttt{r}',r'quali esiti simulati?','un vettore'],
],[1.6,4.7,3.1])+r'''
\vspace{3mm}
\[
q_\alpha=\min\{k:F_K(k)\ge\alpha\}.
\]
\PSmall{Per $K\sim\operatorname{Bin}(20,0{,}3)$, $q_{0,95}=9$. La cumulata a 9 supera $0{,}95$: i salti discreti impediscono di ottenere ogni livello esatto.}
''',r'''
\PCode{R · d, p, q, r}{31_quattro_funzioni.R}
\PSmall{In \texttt{rbinom(5,size=20,...)}, 5 è il numero di conteggi richiesti; ogni conteggio deriva da 20 prove.}
''','d restituisce una massa o densità, p una cumulata, q una soglia e r valori simulati.')

bin32 = list(csv.DictReader((FIG/'binomiale_400.csv').open()))
CODES['32_teoria_simulazione.R'] = '''# 400 repliche, 20 prove ciascuna
set.seed(17)
s32 <- rbinom(400, size=20, prob=.3)
f32 <- tabulate(s32+1, nbins=21)/400
plot(0:20, dbinom(0:20,20,.3),
     type="h", xlab="k", ylab="P")
points(0:20, f32, col="orange",pch=16)
mean(s32)  # 5.9375; teoria: 6
'''
S(32,'400 repliche approssimano la distribuzione',BIN,r'''
\PLabel{Stesso modello, frequenze ottenute con seme 17}
'''+stem_chart([float(r['probabilita']) for r in bin32],
              second=[float(r['frequenza']) for r in bin32],
              label=r'barre: teoria\\punti: frequenze')+r'''
\PBody{Ogni replica genera un conteggio su $n=20$ prove. Le $B=400$ repliche costruiscono la distribuzione empirica dei conteggi.}
\PSmall{Con questo seme la media simulata è $5{,}9375$; quella teorica è 6. Le differenze dipendono dalla simulazione finita.}
''',r'''
\PCode{R · teoria e frequenze}{32_teoria_simulazione.R}
\PSmall{\texttt{tabulate(s32+1)} conta gli esiti: lo spostamento di 1 permette di includere il conteggio zero nella prima posizione.}
''','n indica le prove di una replica; B indica quante volte si ripete l’esperimento completo.')

CODES['33_lab_binomiale.R'] = '''# Esperimento m04-binomiale
a33 <- lab_binomiale(n=20, prob=.3)
b33 <- lab_binomiale(n=40, prob=.3)
a33$indicatori
b33$indicatori
# Il sito usa 400 repliche
length(a33$simulazioni)
'''
S(33,'Laboratorio: aumentare il numero di prove',BIN,r'''
\PLabel{Esperimento m04-binomiale}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.75cm] (a) at(2.2,2.5){$n=20,\ p=0{,}3$\\$E[K]=6$\\$\operatorname{Var}(K)=4{,}2$};
\node[pFlow,text width=3.75cm] (b) at(7.2,2.5){$n=40,\ p=0{,}3$\\$E[K]=12$\\$\operatorname{Var}(K)=8{,}4$};
\draw[pEdge](a)--node[pNote,above] {$n\times2$}(b);
\node[pLabel,text width=8.6cm] at(4.7,.55){Per la proporzione: $\operatorname{Var}(K/n)=p(1-p)/n$.};
\end{tikzpicture}
\PBody{Confrontare posizione e dispersione dei conteggi. Poi ripetere il confronto sulla proporzione $K/n$.}
\PSmall{Nel sito il numero di repliche rimane 400. \href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-binomiale}{Aprire l'esperimento}.}
''',r'''
\PCode{R · due valori di n}{33_lab_binomiale.R}
\PInfo{Prima di eseguire: prevedere che cosa accade a media e deviazione standard di $K$, poi a quelle di $K/n$.}
\PSmall{Registrare parametri, previsione e risultato. Uno scarto della media simulata dalla teoria è atteso con repliche finite.}
''','Aumentare n amplia i conteggi possibili e riduce la dispersione della proporzione K/n, a p fissata.')


CODES['34_tasso_esposizione.R'] = '''# Esempio: fratture lungo una linea
rate34 <- 2  # Eventi per metro
L34 <- 3     # Metri osservati
mu34 <- rate34 * L34
mu34         # Conteggio atteso: 6
dpois(0, lambda = mu34)
'''
S(34,'Poisson: tasso ed esposizione',POI,r'''
\PLabel{Esempio dichiarato: eventi lungo una linea}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[GeoA,line width=2pt](.7,2.6)--(8.5,2.6);
\foreach \x/\lab in {.7/0,3.3/1,5.9/2,8.5/3}{
\draw[GeoA](\x,2.35)--(\x,2.85);
\node[pNote,above] at(\x,2.9){\lab\ m};}
\draw[decorate,decoration={brace,mirror,amplitude=5pt},Classical](.7,2.1)--(8.5,2.1);
\node[pLabel] at(4.6,1.55){Esposizione $L=3$ m};
\node[pFlow,text width=7.5cm] at(4.6,.35){Tasso $\lambda=2$ eventi/m $\quad\Rightarrow\quad\mu=\lambda L=6$};
\end{tikzpicture}
\[
K\sim\operatorname{Pois}(\mu),\qquad \mu=\lambda L.
\]
\PSmall{$\lambda$ è un tasso per unità di esposizione; $\mu$ è il conteggio atteso sull'intero supporto. L'esposizione può essere lunghezza, area o tempo.}
''',r'''
\PCode{R · costruire la media attesa}{34_tasso_esposizione.R}
\PInfo{In \texttt{dpois()}, l'argomento chiamato \texttt{lambda} è la media $\mu$ del conteggio, già moltiplicata per l'esposizione.}
\PSmall{Il modello omogeneo assume tasso costante e conteggi indipendenti in porzioni disgiunte del supporto.}
''','Per ottenere il conteggio atteso si moltiplica il tasso per l’esposizione, con unità coerenti.')

CODES['35_poisson_distribuzione.R'] = '''# Media del conteggio: 6
k35 <- 0:qpois(.999, lambda=6)
pr35 <- dpois(k35, lambda=6)
sum(pr35)  # Quasi 1: coda esclusa
c(media=6, varianza=6, sd=sqrt(6))
'''
S(35,'La distribuzione di Poisson',POI,r'''
\PLabel{Conteggi non negativi: $\mu=6$}
'''+stem_chart([pois(k) for k in range(16)],xmax=15,ymax=.18,xticks=[0,3,6,9,12,15])+r'''
\[
P(K=k)=e^{-\mu}\frac{\mu^k}{k!},\qquad k=0,1,\ldots
\]
\PSmall{$E[K]=\operatorname{Var}(K)=\mu$; $\operatorname{SD}(K)=\sqrt{\mu}$. L'uguaglianza fra media e varianza è una proprietà del modello.}
''',r'''
\PCode{R · masse di probabilità}{35_poisson_distribuzione.R}
\PSmall{Il grafico termina al quantile $0{,}999$, qui 15. La distribuzione continua oltre: la somma delle barre mostrate è lievemente inferiore a 1.}
\PInfo{La varianza di un campione finito non coincide necessariamente con la media, anche quando il modello di generazione è Poisson.}
''','Nella Poisson media e varianza teoriche coincidono. Il supporto comprende tutti gli interi non negativi.')

CODES['36_esposizioni.R'] = '''# Stesso tasso: esposizione doppia
L36 <- c(3, 6)
mu36 <- 2 * L36
data.frame(esposizione=L36,
           media=mu36,
           sd=sqrt(mu36),
           cv=1/sqrt(mu36))
'''
o,xx,yy=axes(-.6,23.6,.18,[0,6,12,18,24],[0,.05,.10,.15],
             '$k$: conteggio su ciascuna esposizione','$P(K=k)$')
for mu,col in [(6,'GeoA'),(12,'GeoB')]:
    curve(o,[(k,pois(k,mu)) for k in range(25)],xx,yy,col)
    for k in range(25):
        o.append(fr'\fill[{col}] ({xx(k):.4f},{yy(pois(k,mu)):.4f}) circle(1.7pt);')
o.append(r'\node[pNote,anchor=north east] at(8.9,2.5){blu: $L=3$ m\\arancio: $L=6$ m};')
S(36,'Più esposizione, più eventi attesi',POI,r'''
\PLabel{Tasso costante: $\lambda=2$ eventi/m}
'''+finish(o)+r'''
\[
E[K]=\lambda L,\qquad
\frac{\operatorname{SD}(K)}{E[K]}=\frac{1}{\sqrt{\lambda L}}.
\]
\PSmall{Raddoppiare $L$ raddoppia la media e moltiplica la deviazione standard per $\sqrt2$. La dispersione relativa diminuisce. Le linee uniscono masse discrete.}
''',r'''
\PCode{R · conteggi e dispersione relativa}{36_esposizioni.R}
\PInfo{Confrontare solo i conteggi di supporti diversi confonde tasso ed esposizione. Riportare sempre quanto spazio o tempo è stato osservato.}
''','Nel modello omogeneo l’esposizione determina la media del conteggio e la sua dispersione relativa.')

CODES['37_coda_poisson.R'] = '''# Almeno 10 eventi, media 6
ppois(9, lambda=6,
      lower.tail=FALSE)
# Primo conteggio con cumulata >= .95
qpois(.95, lambda=6)
ppois(10, lambda=6)
'''
S(37,'Code e soglie per i conteggi Poisson',POI,r'''
\PLabel{Un evento raro è definito rispetto a una soglia}
'''+stem_chart([pois(k) for k in range(16)],xmax=15,ymax=.18,
              xticks=[0,3,6,9,12,15],highlight=lambda k:k>=10,
              label=r'arancio: $K\ge10$')+r'''
\[
P(K\ge10)=P(K>9)\simeq0{,}0839.
\]
\PSmall{Il quantile $q_{0,95}=10$ è una domanda diversa: cerca il primo conteggio con probabilità cumulata almeno $0{,}95$.}
''',r'''
\PCode{R · probabilità e quantile}{37_coda_poisson.R}
\PSmall{\texttt{lower.tail=FALSE} calcola direttamente la coda superiore e migliora la precisione per probabilità molto piccole.}
\PInfo{Prima di scegliere una funzione, scrivere se si cerca una probabilità a soglia fissata o una soglia a probabilità fissata.}
''','Una funzione di probabilità riceve una soglia; una funzione quantile riceve una probabilità.')

CODES['38_eventi_rari.R'] = '''# Molte prove, p piccolo: n*p=6
k38 <- 0:25
b38 <- dbinom(k38, 200, .03)
p38 <- dpois(k38, 6)
max(abs(b38-p38))
c(var_bin=200*.03*.97, var_pois=6)
'''
S(38,'Eventi rari: dalla binomiale alla Poisson',POI,r'''
\PLabel{Confronto: $\operatorname{Bin}(200,0{,}03)$ e $\operatorname{Pois}(6)$}
'''+stem_chart([binom(k,200,.03) for k in range(21)],
              second=[pois(k) for k in range(21)],xmax=20,ymax=.18,
              label=r'barre: binomiale\\punti: Poisson')+r'''
\[
n\to\infty,\quad p\to0,\quad np\to\mu
\quad\Longrightarrow\quad
\operatorname{Bin}(n,p)\ \to\ \operatorname{Pois}(\mu).
\]
\PSmall{Qui le varianze sono $5{,}82$ e 6. L'approssimazione va valutata per la probabilità richiesta, soprattutto nelle code.}
''',r'''
\PCode{R · confrontare le masse}{38_eventi_rari.R}
\PSmall{La massima differenza fra le masse controllate, da 0 a 25, è circa $0{,}00246$. Questa quantità non è l'errore relativo di una coda.}
\PInfo{Con $n=20$ e $p=0{,}3$, $np$ vale ancora 6 ma la varianza binomiale è $4{,}2$: conoscere soltanto la media non basta.}
''','La Poisson approssima una binomiale quando le prove sono molte e la probabilità per prova è piccola.')

CODES['39_somma_poisson.R'] = '''# Due conteggi indipendenti
set.seed(17)
a39 <- rpois(10000, lambda=2)
b39 <- rpois(10000, lambda=4)
s39 <- a39 + b39
c(media=mean(s39), varianza=var(s39))
# La distribuzione esatta e' Pois(6)
'''
S(39,'Sommare conteggi su supporti disgiunti',POI,r'''
\PLabel{L'indipendenza è un'ipotesi del risultato}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (a) at(2.1,3){$K_1\sim\operatorname{Pois}(2)$\\primo supporto};
\node[pFlow,text width=3.5cm] (b) at(7.1,3){$K_2\sim\operatorname{Pois}(4)$\\secondo supporto};
\node[pFlow,text width=5.6cm,fill=GeoTint] (c) at(4.6,1){$K_1+K_2\sim\operatorname{Pois}(6)$\\supporto complessivo};
\draw[pEdge](a.south)--++(0,-.35)-|(c.north);
\draw[pEdge](b.south)--++(0,-.35)-|(c.north);
\end{tikzpicture}
\[
\mu_{\mathrm{tot}}=\mu_1+\mu_2,\qquad
\operatorname{Var}(K_1+K_2)=\mu_1+\mu_2.
\]
\PSmall{L'additività delle medie vale sempre. La forma Poisson della somma qui richiede componenti Poisson indipendenti.}
''',r'''
\PCode{R · generare componenti indipendenti}{39_somma_poisson.R}
\PSmall{Ogni posizione dei due vettori forma una replica completa. La somma elemento per elemento produce 10\,000 conteggi totali.}
\PInfo{Un fattore comune che aumenta entrambi i conteggi introduce dipendenza e può cambiare la dispersione della somma.}
''','La somma di conteggi Poisson indipendenti è Poisson, con media uguale alla somma delle medie.')

CODES['40_eterogeneita.R'] = '''# Due regimi con uguale probabilita
set.seed(17)
mu40 <- sample(c(2,10), 10000,
               replace=TRUE)
k40 <- rpois(10000, lambda=mu40)
c(media=mean(k40), varianza=var(k40))
# Teoria: media 6, varianza 6+16=22
'''
S(40,'L’eterogeneità può aumentare la dispersione',POI,r'''
\PLabel{Stessa media 6: Poisson e miscela di due regimi}
'''+stem_chart([pois(k) for k in range(23)],xmax=22,ymax=.18,
              second=[.5*pois(k,2)+.5*pois(k,10) for k in range(23)],
              label=r'barre: Poisson(6)\\punti: miscela')+r'''
\[
\operatorname{Var}(K)=E[\Lambda]+\operatorname{Var}(\Lambda)
=6+16=22.
\]
\PSmall{Nella miscela costruita, $\Lambda=2$ o 10 con probabilità $1/2$; dato $\Lambda$, $K$ è Poisson. I regimi aumentano la varianza totale.}
''',r'''
\PCode{R · una Poisson con media variabile}{40_eterogeneita.R}
\PSmall{\texttt{sample()} sceglie un regime per replica. \texttt{rpois()} usa il corrispondente valore del vettore \texttt{mu40}.}
\PInfo{Una dispersione maggiore della media invita a esaminare esposizioni, gruppi e dipendenza. Da sola non identifica la causa.}
''','L’uguaglianza fra media e varianza può fallire quando si mescolano conteggi con medie diverse.')

CODES['41_lab_poisson.R'] = '''# Stessa media, tassi differenti
a41 <- lab_poisson(rate=2,
                  exposure=3)
b41 <- lab_poisson(rate=1,
                  exposure=6)
a41$indicatori
b41$indicatori
all.equal(a41$dati, b41$dati)
'''
S(41,'Laboratorio: due combinazioni, stessa media',POI,r'''
\PLabel{Esperimento m04-poisson}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.9cm] (a) at(2.25,3){Tasso 2\\esposizione 3};
\node[pFlow,text width=3.9cm] (b) at(7.15,3){Tasso 1\\esposizione 6};
\node[pFlow,text width=6cm,fill=GeoTint] (c) at(4.7,1){$\mu=6$ in entrambi i casi\\stessa distribuzione dei conteggi};
\draw[pEdge](a.south)--++(0,-.25)-|(c.north);
\draw[pEdge](b.south)--++(0,-.25)-|(c.north);
\end{tikzpicture}
\PBody{Verificare che le barre coincidano. Poi mantenere fisso il tasso e raddoppiare l'esposizione: prevedere media e deviazione standard.}
\PSmall{Il sito mostra probabilità teoriche. \href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-poisson}{Aprire l'esperimento}.}
''',r'''
\PCode{R · separare tasso ed esposizione}{41_lab_poisson.R}
\PInfo{Il tasso cambia; le probabilità del conteggio dipendono dal prodotto fra tasso ed esposizione.}
\PSmall{In questo esperimento il seme non modifica il risultato: non viene generato un campione casuale.}
''','Uguali conteggi attesi possono derivare da tassi diversi se cambiano le esposizioni.')


CODES['42_normale.R'] = '''# Modello continuo: media 10, SD 2
x42 <- seq(2, 18, length.out=201)
d42 <- dnorm(x42, mean=10, sd=2)
plot(x42, d42, type="l",
     xlab="x", ylab="Densita")
# dnorm restituisce una densita
dnorm(10, mean=10, sd=2)
'''
S(42,'La normale: posizione e scala',NOR,r'''
\PLabel{Modello continuo: $X\sim\mathcal N(10,2^2)$}
'''+norm_chart(label=r'$\mu=10,\ \sigma=2$')+r'''
\[
f_X(x)=\frac{1}{\sigma\sqrt{2\pi}}\,
e^{-\frac12((x-\mu)/\sigma)^2},\qquad \sigma>0.
\]
\PSmall{$\mu=E[X]$ fissa il centro; $\sigma$ è la deviazione standard. Il secondo parametro della notazione $\mathcal N(\mu,\sigma^2)$ è la varianza.}
''',r'''
\PCode{R · disegnare una densità}{42_normale.R}
\PSmall{In R l'argomento \texttt{sd=2} riceve la deviazione standard. Per questa curva la varianza vale $2^2=4$.}
\PInfo{La probabilità corrisponde a un'area sotto la curva. Il valore restituito da \texttt{dnorm()} è un'altezza di densità.}
''','Nella normale μ indica la media e σ la deviazione standard; in R sd riceve σ.')

CODES['43_posizione_scala.R'] = '''# Stessa variabile, tre modelli
x43 <- seq(2, 20, length.out=201)
a43 <- dnorm(x43, 10, 1)
b43 <- dnorm(x43, 10, 2)
c43 <- dnorm(x43, 14, 2)
matplot(x43, cbind(a43,b43,c43),
        type="l", lty=1,
        xlab="x", ylab="Densita")
'''
o,xx,yy=axes(2,20,.46,[2,6,10,14,18],[],'$x$','$f_X(x)$',2.5)
for mu,sd,col in [(10,1,'GeoA'),(10,2,'GeoB'),(14,2,'GeoC')]:
    curve(o,[(2+18*i/220,normal(2+18*i/220,mu,sd)) for i in range(221)],xx,yy,col)
o.append(r'\node[pNote,text=GeoA,anchor=north west] at(.9,2.6){$\mu=10,\ \sigma=1$};')
o.append(r'\node[pNote,text=GeoB,anchor=north west] at(.9,2.15){$\mu=10,\ \sigma=2$};')
o.append(r'\node[pNote,text=GeoC,anchor=north west] at(.9,1.7){$\mu=14,\ \sigma=2$};')
S(43,'Spostare il centro o cambiare la dispersione',NOR,r'''
\PLabel{Tre densità, ciascuna con area totale 1}
'''+finish(o)+r'''
\[
Z\sim\mathcal N(0,1)\quad\Rightarrow\quad X=\mu+\sigma Z.
\]
\PBody{Aumentare $\mu$ trasla la distribuzione. Aumentare $\sigma$ dilata la scala e abbassa il picco, conservando l'area totale.}
''',r'''
\PCode{R · confrontare tre densità}{43_posizione_scala.R}
\PSmall{\texttt{cbind()} riunisce le tre colonne; \texttt{matplot()} le rappresenta sullo stesso asse orizzontale.}
\PInfo{La posizione del picco e la sua altezza descrivono aspetti differenti. Una curva più alta può semplicemente essere meno dispersa.}
''','La media trasla la normale; la deviazione standard ne cambia la larghezza.')

CODES['44_standardizzare.R'] = '''# Valore 14 nel modello N(10, 2^2)
z44 <- (14 - 10) / 2
z44  # Due deviazioni sopra la media
pnorm(14, mean=10, sd=2)
pnorm(z44)  # Stessa probabilita
'''
S(44,'Standardizzare rende confrontabili le distanze',NOR,r'''
\PLabel{Un cambiamento di origine e unità}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.55,3.15)--(9,3.15);
\draw[pAxis](.55,.9)--(9,.9);
\foreach \x/\v in {1/6,3/8,5/10,7/12,9/14}{
\draw[GeoA](\x,3.03)--(\x,3.27);
\node[pLabel,above] at(\x,3.3){\v};
}
\foreach \x/\z in {1/-2,3/-1,5/0,7/1,9/2}{
\draw[GeoC](\x,.78)--(\x,1.02);
\node[pLabel,below] at(\x,.75){\z};
\draw[pEdge,draw=Rule](\x,2.8)--(\x,1.25);
}
\node[pNote,anchor=west] at(.6,4){Scala originale $X$: $\mu=10,\ \sigma=2$};
\node[pNote,anchor=west] at(.6,-.05){Scala standard $Z$: media 0, deviazione standard 1};
\end{tikzpicture}
\[
Z=\frac{X-\mu}{\sigma},\qquad
P(X\le x)=\Phi\!\left(\frac{x-\mu}{\sigma}\right).
\]
''',r'''
\PCode{R · la stessa area su due scale}{44_standardizzare.R}
\PSmall{$\Phi$ è la cumulata della normale standard. Il valore $z=2$ significa due deviazioni standard sopra la media.}
\PInfo{Questa equivalenza usa l'ipotesi normale. Standardizzare un insieme di dati ne cambia la scala, conservandone la forma.}
''','Lo z-score misura la distanza dalla media in unità di deviazione standard.')

CODES['45_probabilita_intervallo.R'] = '''# Probabilita fra 8 e 12
pnorm(12, mean=10, sd=2) -
  pnorm(8, mean=10, sd=2)
# Stesso intervallo: -1 < Z < 1
pnorm(1) - pnorm(-1)
'''
S(45,'La probabilità di un intervallo è un’area',NOR,r'''
\PLabel{Intervallo $[8,12]$ nel modello $\mathcal N(10,2^2)$}
'''+norm_chart(shade=(8,12),marks=[(8,'8'),(12,'12')],
              label=r'area $\simeq0{,}6827$')+r'''
\[
P(a<X\le b)=F_X(b)-F_X(a).
\]
\PSmall{Per una variabile continua, includere o escludere i singoli estremi non cambia la probabilità. Qui l'intervallo corrisponde a $\mu\pm\sigma$.}
''',r'''
\PCode{R · sottrarre due cumulate}{45_probabilita_intervallo.R}
\PBody{Circa il $68{,}27\%$ della probabilità del modello cade entro una deviazione standard dalla media.}
\PInfo{La percentuale descrive la distribuzione assunta. Non garantisce che un piccolo campione mostri esattamente la stessa quota.}
''','La probabilità fra due soglie si calcola come differenza delle rispettive probabilità cumulate.')

CODES['46_quantile_normale.R'] = '''# Soglia con il 95% a sinistra
q46 <- qnorm(.95, mean=10, sd=2)
q46  # 13.28971
qnorm(.95)  # 1.644854
pnorm(q46, mean=10, sd=2)
'''
S(46,'Un quantile trasforma una probabilità in soglia',NOR,r'''
\PLabel{Quantile $0{,}95$: una coda destra del $5\%$}
'''+norm_chart(shade=(2,13.2897072539),
              marks=[(13.2897072539,r'$q_{0,95}$')],
              label=r'$P(X\le q_{0,95})=0{,}95$')+r'''
\[
q_\alpha=\mu+\sigma\,\Phi^{-1}(\alpha).
\]
\PSmall{Con $\mu=10$ e $\sigma=2$, $q_{0,95}=10+2(1{,}64485)\simeq13{,}2897$. I valori sotto la soglia hanno probabilità totale $0{,}95$.}
''',r'''
\PCode{R · calcolare e verificare la soglia}{46_quantile_normale.R}
\PSmall{\texttt{qnorm()} trova la soglia. Applicare \texttt{pnorm()} a quel valore restituisce la probabilità richiesta, entro l'errore numerico.}
\PInfo{Il livello $0{,}95$ in questa chiamata è una probabilità cumulata da sinistra.}
''',r'Il quantile 0,95 lascia il 95\% della probabilità a sinistra e il 5\% a destra.')

CODES['47_intervallo_centrale.R'] = '''# Due code del 2.5% ciascuna
i47 <- qnorm(c(.025,.975), 10, 2)
i47  # 6.080072, 13.919928
diff(pnorm(i47, mean=10, sd=2))
# Quantile unilaterale: altra soglia
qnorm(.95, mean=10, sd=2)
'''
def two_normal_intervals():
    o=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    xx=lambda z:.8+8.0*(z+4)/8
    for y,a,b,lab in [(2.5,-4,1.64485362695,r'95\% a sinistra'),
                      (.35,-1.95996398454,1.95996398454,r'95\% centrale')]:
        yy=lambda z:y+1.05*math.exp(-z*z/2)
        o.append(fr'\draw[pAxis](.8,{y})--(9,{y});')
        xs=[a+(b-a)*i/100 for i in range(101)]
        path=[f'({xx(a):.4f},{y})']+[f'({xx(z):.4f},{yy(z):.4f})' for z in xs]+[f'({xx(b):.4f},{y})']
        o.append(r'\fill[GeoA!22] '+' -- '.join(path)+' -- cycle;')
        o.append(r'\draw[GeoA,line width=1pt] plot coordinates {'+
                 ' '.join(f'({xx(-4+8*i/160):.4f},{yy(-4+8*i/160):.4f})' for i in range(161))+'};')
        o.append(fr'\node[pNote,anchor=west] at(.8,{y+1.25}) {{{lab}}};')
        for z,text in (([(0,'0'),(1.64485362695,'1{,}645')] if y>1 else
                       [(-1.95996398454,'-1{,}960'),(0,'0'),(1.95996398454,'1{,}960')])):
            o.append(fr'\draw[Muted]({xx(z):.4f},{y})--({xx(z):.4f},{y-.07});')
            o.append(fr'\node[pNote,below] at({xx(z):.4f},{y-.08}) {{$ {text} $}};')
    o.append(r'\node[pNote,anchor=west] at(.8,-.4){Asse orizzontale: $z=(x-\mu)/\sigma$};')
    return finish(o)

S(47,r'Il 95\% centrale lascia due code uguali',NOR,r'''
\PLabel{Due richieste di probabilità, due geometrie}
'''+two_normal_intervals()+r'''
\[
P\!\left(\mu-1{,}96\sigma\le X\le\mu+1{,}96\sigma\right)
\simeq0{,}95.
\]
\PSmall{I due estremi sono i quantili $0{,}025$ e $0{,}975$. Il quantile $0{,}95$ da solo definisce una soglia unilaterale.}
''',r'''
\PCode{R · due quantili per un intervallo}{47_intervallo_centrale.R}
\PInfo{Questo è un intervallo centrale dei valori del modello con $\mu$ e $\sigma$ fissati. Un intervallo di confidenza per un parametro richiede un problema di inferenza.}
''',r'Un intervallo centrale al 95\% usa i quantili 0,025 e 0,975; il quantile 0,95 è una soglia unilaterale.')

CODES['48_limite_normale.R'] = '''# Concentrazione [mg/L], modello
# normale con media 1 e SD 0.8
pnorm(0, mean=1, sd=.8)
# Probabilita negativa: circa 10.6%
# Con media 10 e SD 2 e' molto minore
pnorm(0, mean=10, sd=2)
'''
S(48,'Controllare il dominio fisico del modello',NOR,r'''
\PLabel{Esempio: concentrazione non negativa, in mg/L}
'''+norm_chart(mu=1,sd=.8,xmin=-2,xmax=4,xticks=[-2,-1,0,1,2,3,4],
              shade=(-2,0),color='GeoB',label=r'$P(X<0)\simeq0{,}106$')+r'''
\PBody{Una normale con media 1 e deviazione standard $0{,}8$ assegna circa il $10{,}6\%$ della probabilità a concentrazioni negative.}
\PSmall{Il supporto della normale è tutta la retta reale. Vicino a un limite fisico, occorre valutare un modello coerente con quel limite.}
''',r'''
\PCode{R · probabilità fuori dal dominio}{48_limite_normale.R}
\PInfo{La lognormale, introdotta nel blocco successivo, ha supporto positivo. La scelta richiede anche una spiegazione plausibile del processo e della variabilità.}
\PSmall{Eliminare dopo la simulazione i valori negativi cambia il modello: si ottiene una distribuzione condizionata, da dichiarare.}
''','La scelta di una distribuzione deve rispettare il significato della variabile e le probabilità assegnate fuori dal suo dominio.')

CODES['49_lab_normale.R'] = '''# Stesso livello, scale differenti
a49 <- lab_normale(mu=10, sd=2,
                  q=.95)
b49 <- lab_normale(mu=20, sd=4,
                  q=.95)
a49$indicatori
b49$indicatori
'''
S(49,'Laboratorio: il quantile segue la scala',NOR,r'''
\PLabel{Esperimento m04-normale}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.75cm] (a) at(2.2,3){$\mu=10,\ \sigma=2$\\$q_{0,95}=13{,}2897$};
\node[pFlow,text width=3.75cm] (b) at(7.2,3){$\mu=20,\ \sigma=4$\\$q_{0,95}=26{,}5794$};
\node[pFlow,text width=6.2cm,fill=GeoTint] (c) at(4.7,.9){Distanza standard uguale\\$(q_{0,95}-\mu)/\sigma=1{,}64485$};
\draw[pEdge](a.south)--++(0,-.35)-|(c.north);
\draw[pEdge](b.south)--++(0,-.35)-|(c.north);
\end{tikzpicture}
\PBody{Prevedere il quantile prima di muovere i controlli. Variare poi il livello $q$: che cosa accade alla soglia?}
\PSmall{Il sito calcola una curva teorica. \href{https://marzione00.github.io/Lab_Geo/\#laboratorio/m04-normale}{Aprire l'esperimento}.}
''',r'''
\PCode{R · confrontare quantili}{49_lab_normale.R}
\PInfo{A livello fissato, il quantile standard rimane uguale. Cambia il quantile espresso sulla scala originale.}
\PSmall{Il seme non modifica questa curva. Separare nei commenti il livello $q$, il quantile originale e quello standard.}
''','Il quantile normale sulla scala originale si ricava da μ + σz; il livello determina z.')
