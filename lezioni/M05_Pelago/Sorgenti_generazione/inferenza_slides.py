"""Pelago M05, slide 26–59: distribuzioni, errore standard e intervalli.

Grafici TikZ nativi. Coordinate delle simulazioni in inferenza_proof/coordinate;
calcoli R riproducibili in inferenza_proof/calcoli_figure.R.
"""
from pathlib import Path
import csv, math

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "inferenza_proof/coordinate"
SLIDES, CODES = {}, {}
D = "DISTRIBUZIONI CAMPIONARIE"
E = "ERRORE STANDARD"
I = "INTERVALLI DI CONFIDENZA"

def S(n,title,section,left,right,recall):
    SLIDES[n]=dict(title=title,section=section,left=left,right=right,recall=recall)

def code(n,name,s):
    CODES[f"{n:03}_{name}.R"]=s.strip()+"\n"

def rows(name):
    return list(csv.DictReader((FIG/(name+".csv")).open()))

def fmt(v,d=3):
    return f"{v:.{d}f}".replace(".", "{,}")

def coords(p):
    return " ".join(f"({x:.5f},{y:.5f})" for x,y in p)

def axes(xmin,xmax,ymax,xticks,yticks,xlab,ylab,h=2.5):
    xx=lambda v:.75+8.05*(v-xmin)/(xmax-xmin)
    yy=lambda v:h*v/ymax
    o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for v in yticks:
        o += [rf"\draw[Rule](.75,{yy(v):.4f})--(8.8,{yy(v):.4f});",
              rf"\node[pNote,anchor=east] at(.60,{yy(v):.4f}){{$ {v:g} $}};"]
    o += [rf"\draw[pAxis](.75,0)--(9,0);",
          rf"\draw[pAxis](.75,0)--(.75,{h+.15});"]
    for v in xticks:
        o += [rf"\draw[Muted]({xx(v):.4f},0)--({xx(v):.4f},-.07);",
              rf"\node[pNote,below] at({xx(v):.4f},-.09){{$ {v:g} $}};"]
    o += [rf"\node[pNote] at(4.8,-.61){{{xlab}}};",
          rf"\node[pNote,rotate=90] at(-.18,{h/2}){{{ylab}}};"]
    return o,xx,yy

def line(o,p,xx,yy,color="GeoA",extra=""):
    o.append(rf"\draw[{color},line width=1.1pt,{extra}] plot coordinates{{"+
             coords([(xx(x),yy(y)) for x,y in p])+r"};")

def end(o):
    return "\n".join(o+[r"\end{tikzpicture}"])

def table(headers,rs,widths,h=.65):
    o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    w=sum(widths)
    o.append(rf"\fill[GeoTint](0,0) rectangle({w},{h});")
    for j,row in enumerate([headers]+rs):
        a=0
        for t,cw in zip(row,widths):
            o.append(rf"\node[pLabel,anchor=west] at({a+.10},{h/2-j*h}){{{t}}};")
            a+=cw
        o.append(rf"\draw[Rule](0,{-j*h})--({w},{-j*h});")
    return end(o)

ST={r["nome"]:float(r["valore"]) for r in rows("riepilogo_fossili")}

code(26,"campioni","""
set.seed(17)
# Ogni colonna e' un campione.
c26 <- replicate(4, rexp(6))
round(c26, 2)
m26 <- colMeans(c26)
round(m26, 2)  # Quattro medie
""")
S(26,"Una media per ciascun campione",D,r"""
\PLabel{La ripetizione riguarda l'intero campionamento}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.05cm] (p) at(1.3,2.0){Popolazione\\$F$};
\foreach \y/\lab in {3.4/1,2.0/2,.6/3}{
\node[pFlow,text width=2.6cm] (c\lab) at(5,\y){Campione $\lab$\\$X_1^{(\lab)},\ldots,X_n^{(\lab)}$};
\node[pFlow,text width=1.25cm,fill=GeoA!10] (m\lab) at(8.35,\y){$\bar X^{(\lab)}$};
\draw[pEdge](p.east)--++(.4,0)|-(c\lab.west);
\draw[pEdge](c\lab)--(m\lab);}
\node[pNote] at(5,-.13){$n$ osservazioni per campione};
\end{tikzpicture}
\PBody{La distribuzione campionaria descrive le medie ottenibili ripetendo lo stesso disegno, con popolazione e numerosità fissate.}
""",r"""
\PCode{R · quattro campioni esponenziali}{026_campioni.R}
\PBody{\texttt{replicate()} ripete un'espressione. \texttt{colMeans()} restituisce una media per colonna.}
\PInfo{Prima dell'osservazione, $\bar X$ è una variabile aleatoria. Dopo l'osservazione, $\bar x$ è il valore calcolato nel campione.}
""","Ogni punto della distribuzione campionaria corrisponde a una statistica calcolata su un intero campione.")

o,xx,yy=axes(-2,4.5,1.1,[-2,0,1,3],[0,.5,1],"$x$: osservazione individuale","densità")
rr=rows("popolazioni")
line(o,[(float(r["x"]),float(r["normale"])) for r in rr],xx,yy)
line(o,[(float(r["x"]),float(r["esponenziale"])) for r in rr if float(r["x"])>=0],xx,yy,"GeoB")
o += [r"\node[pNote,text=GeoA,anchor=west] at(4.9,2.35){Normale $\mathcal N(1,1)$};",
      r"\node[pNote,text=GeoB,anchor=west] at(4.9,1.91){Esponenziale $\mathrm{Exp}(1)$};"]
code(27,"popolazioni","""
# Due modelli con media e varianza 1
set.seed(17)
a27 <- rnorm(200, mean = 1, sd = 1)
b27 <- rexp(200, rate = 1)
c(mean(a27), var(a27))
c(mean(b27), var(b27))
""")
S(27,"Stessi momenti, forme diverse",D,r"""
\PLabel{Le due popolazioni offerte nel laboratorio}
"""+end(o)+r"""
\[
\mathbb E(X)=1,\qquad \operatorname{Var}(X)=1.
\]
\PSmall{La normale ammette anche valori negativi. Qui confrontiamo modelli matematici adimensionali, senza attribuire loro una grandezza fisica positiva.}
""",r"""
\PCode{R · due generatori}{027_popolazioni.R}
\PBody{I valori osservati di media e varianza oscillano. I parametri delle due popolazioni restano uguali a uno.}
\PInfo{La forma della distribuzione dei dati può influire sulla distribuzione della media quando il campione è piccolo.}
""","La media e la varianza della popolazione non ne determinano da sole la forma.")

code(28,"valore_atteso","""
# Medie note, anche differenti
mu28 <- c(2, 4, 9)
mean(mu28)  # E della media: 5
# Se tutte le medie valgono mu
mu28 <- rep(5, 3)
sum(mu28) / length(mu28)
""")
S(28,"Il valore atteso della media",D,r"""
\PLabel{La linearità dell'aspettazione}
\[
\begin{aligned}
\mathbb E(\bar X)
&=\mathbb E\!\left(\frac1n\sum_{i=1}^n X_i\right)\\
&=\frac1n\sum_{i=1}^n\mathbb E(X_i)
=\frac{n\mu}{n}=\mu.
\end{aligned}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.2cm] (a) at(1.9,1){Ogni osservazione\\ha media $\mu$};
\node[pFlow,text width=3.6cm,fill=GeoA!10] (b) at(7.1,1){Anche $\bar X$\\ha media $\mu$};
\draw[pEdge](a)--node[pNote,above]{media}(b);
\end{tikzpicture}
\PSmall{Sono sufficienti valori attesi finiti e uguali. Questa derivazione non usa l'indipendenza.}
""",r"""
\PCode{R · medie attese dei contributi}{028_valore_atteso.R}
\PBody{Con medie differenti $\mu_i$, il risultato diventa $\mathbb E(\bar X)=n^{-1}\sum_i\mu_i$.}
\PInfo{La non distorsione riguarda il valore atteso dello stimatore. Una singola media campionaria può trovarsi sopra o sotto il parametro.}
""","La media è non distorta per una media comune finita, anche quando le osservazioni sono dipendenti.")

o,xx,yy=axes(-.2,2.2,3.4,[0,.5,1,1.5,2],[0,1,2,3],r"$\bar x$: media di un campione","densità")
for n,col in [(12,"GeoB"),(60,"GeoA")]:
    pp=[(-.2+2.4*k/240) for k in range(241)]
    line(o,[(x,math.exp(-.5*n*(x-1)**2)*math.sqrt(n/(2*math.pi))) for x in pp],xx,yy,col)
o += [r"\node[pNote,text=GeoB] at(7.5,2.25){$n=12$};",
      r"\node[pNote,text=GeoA] at(7.5,1.82){$n=60$};"]
code(29,"media_normale","""
# Media di n osservazioni N(1,1)
n29 <- 60
se29 <- 1 / sqrt(n29)
# Probabilita' di media fra .8 e 1.2
pnorm(1.2, 1, se29) -
  pnorm(.8, 1, se29)
""")
S(29,"Da dati normali a medie normali",D,r"""
\PLabel{Un risultato esatto sotto indipendenza}
"""+end(o)+r"""
\[
X_i\overset{\mathrm{iid}}\sim\mathcal N(\mu,\sigma^2)
\quad\Longrightarrow\quad
\bar X\sim\mathcal N\!\left(\mu,\frac{\sigma^2}{n}\right).
\]
\PSmall{Nel grafico $\mu=\sigma=1$. La media mantiene il centro e ha dispersione minore.}
""",r"""
\PCode{R · probabilità per una media}{029_media_normale.R}
\PBody{\texttt{pnorm()} richiede la deviazione standard. Per $\bar X$ usiamo $1/\sqrt n$, con $\sigma=1$.}
\PInfo{Il risultato vale per ogni $n$ nel modello normale indipendente. Non richiede un'approssimazione asintotica.}
""","La normale della media ha varianza σ²/n quando i dati sono normali e indipendenti.")

o,xx,yy=axes(0,2.3,3.4,[0,.5,1,1.5,2],[0,1,2,3],r"$\bar x$: media di un campione","densità")
rr=rows("medie_esponenziali")
for key,col in [("n12","GeoB"),("n60","GeoA")]:
    line(o,[(float(r["x"]),float(r[key])) for r in rr],xx,yy,col)
o += [r"\node[pNote,text=GeoB] at(7.4,2.25){$n=12$};",
      r"\node[pNote,text=GeoA] at(7.4,1.82){$n=60$};"]
code(30,"medie_esponenziali","""
set.seed(17)
# Una nuova media a ogni replica
m30 <- replicate(200,
  mean(rexp(60, rate = 1)))
hist(m30, main = "200 medie",
     xlab = "Media campionaria")
sd(m30)
1 / sqrt(60)  # SE teorico
""")
S(30,"Le medie di dati asimmetrici",D,r"""
\PLabel{Esponenziale di media e varianza unitarie}
"""+end(o)+r"""
\[
\bar X_n\sim\operatorname{Gamma}(\text{forma}=n,\ \text{tasso}=n).
\]
\PSmall{Le curve sono densità teoriche. Per $n$ finito resta un'asimmetria, più evidente con $n=12$. La varianza è $1/n$.}
""",r"""
\PCode{R · simulare la distribuzione}{030_medie_esponenziali.R}
\PSmall{L'istogramma contiene 200 medie. Ogni media deriva da 60 nuove osservazioni indipendenti.}
\PInfo{$n$ controlla la precisione della media. $B$ controlla quante medie simulate descrivono la distribuzione.}
""","Aumentare n concentra le medie. Aumentare B migliora la descrizione numerica della loro distribuzione.")

code(31,"chebyshev","""
n31 <- c(25, 100, 400)
eps31 <- .2  # Tolleranza
# Varianza della popolazione = 1
lim31 <- pmin(1, 1/(n31*eps31^2))
data.frame(n = n31, limite = lim31)
""")
S(31,"Perché la media si concentra",D,r"""
\PLabel{Una dimostrazione sufficiente della legge dei grandi numeri}
\[
\Pr\{|\bar X_n-\mu|\ge\varepsilon\}
\le \frac{\operatorname{Var}(\bar X_n)}{\varepsilon^2}
=\frac{\sigma^2}{n\varepsilon^2}
\longrightarrow0.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.4,.5)--(9,.5);
\fill[GeoA!12](3,.05) rectangle(6.6,1.8);
\draw[GeoA,line width=1pt](4.8,.1)--(4.8,1.9);
\foreach \x/\t in {3/{\mu-\varepsilon},4.8/\mu,6.6/{\mu+\varepsilon}}{
\draw[Muted](\x,.42)--(\x,.6);\node[pLabel,below] at(\x,.05){$\t$};}
\node[pNote] at(4.8,1.4){fascia di tolleranza};
\end{tikzpicture}
\PSmall{Ipotesi: osservazioni IID, media $\mu$ e varianza finita $\sigma^2$. La tolleranza $\varepsilon>0$ resta fissata.}
""",r"""
\PCode{R · il limite di Chebyshev}{031_chebyshev.R}
\PBody{Il limite superiore può essere largo. Se supera uno, resta valido il limite banale di probabilità pari a uno.}
\PInfo{La conclusione è la convergenza in probabilità: $\bar X_n\xrightarrow{p}\mu$. Ogni singolo passo della sequenza può ancora allontanarsi da $\mu$.}
""","La legge dei grandi numeri controlla la probabilità di uno scarto oltre una tolleranza fissata.")

rr=rows("media_cumulativa")
o,xx,yy=axes(1,200,1.65,[1,50,100,150,200],[0,.5,1,1.5],"$n$: osservazioni accumulate","media cumulativa",2.45)
line(o,[(int(r["n"]),float(r["media"])) for r in rr],xx,yy)
o += [rf"\draw[GeoB,dashed]({xx(1):.4f},{yy(1):.4f})--({xx(200):.4f},{yy(1):.4f});",
      rf"\node[pNote,anchor=west,text=GeoB] at(6.8,{yy(1)+.28:.4f}){{$\mu=1$}};"]
code(32,"media_cumulativa","""
set.seed(17)
x32 <- rexp(200)
n32 <- seq_along(x32)
mc32 <- cumsum(x32) / n32
plot(n32, mc32, type = "l",
  xlab = "n", ylab = "Media")
abline(h = 1, lty = 2)
""")
S(32,"Una sequenza di medie cumulative",D,r"""
\PLabel{Una realizzazione esponenziale con seme 17}
"""+end(o)+r"""
\[
\bar x_n=\frac{x_1+\cdots+x_n}{n}.
\]
\PSmall{Le medie successive condividono le osservazioni precedenti. I punti della curva sono quindi dipendenti fra loro.}
""",r"""
\PCode{R · seguire il campione che cresce}{032_media_cumulativa.R}
\PBody{\texttt{cumsum()} calcola somme progressive. Il denominatore conta quante osservazioni entrano in ciascuna media.}
\PInfo{Questa curva segue un solo campione crescente. La distribuzione campionaria richiede invece molte repliche dello stesso disegno.}
""","Una traiettoria cumulativa può oscillare mentre il comportamento probabilistico della media si concentra.")

o,xx,yy=axes(-3.5,4,.48,[-3,-1,0,1,3],[0,.2,.4],"$z$: errore standardizzato","densità",2.4)
rr=rows("standardizzate")
for key,col,style in [("normale","Muted","dashed"),("n12","GeoB",""),("n60","GeoA","")]:
    line(o,[(float(r["z"]),float(r[key])) for r in rr],xx,yy,col,style)
o += [r"\node[pNote,text=GeoB] at(7.75,2.15){$n=12$};",
      r"\node[pNote,text=GeoA] at(7.75,1.75){$n=60$};",
      r"\node[pNote] at(7.65,1.35){$\mathcal N(0,1)$};"]
code(33,"standardizzazione","""
set.seed(17)
n33 <- 60
m33 <- replicate(1000,
  mean(rexp(n33)))
z33 <- sqrt(n33) * (m33 - 1)
c(media = mean(z33), sd = sd(z33))
""")
S(33,"La forma dell'errore standardizzato",D,r"""
\PLabel{Teorema del limite centrale per osservazioni IID}
"""+end(o)+r"""
\[
Z_n=\frac{\sqrt n(\bar X_n-\mu)}{\sigma}
\xrightarrow{d}\mathcal N(0,1).
\]
\PSmall{Richiediamo $0<\sigma^2<\infty$. Le curve esponenziali standardizzate si confrontano con la normale tratteggiata.}
""",r"""
\PCode{R · centrare e riscalare}{033_standardizzazione.R}
\PBody{Sottraiamo il centro $\mu=1$ e dividiamo per il SE teorico $1/\sqrt n$. Il risultato è adimensionale.}
\PInfo{Il teorema descrive una distribuzione limite. Non stabilisce un valore di $n$ valido per ogni popolazione.}
""","La standardizzazione rende confrontabile la forma dell'errore mentre la sua scala originale diminuisce.")

code(34,"dipendenza_totale","""
set.seed(17)
z34 <- rnorm(1)
x34 <- rep(z34, 100)
mean(x34)  # Identico a z34
# Aggiungere copie lascia la media
# uguale alla stessa osservazione.
""")
S(34,"Le condizioni che sostengono il risultato",D,r"""
\PLabel{Un caso limite rende visibile il ruolo della dipendenza}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=1.7cm,fill=GeoB!12] (z) at(1.35,2){$Z$};
\foreach \y/\i in {3.1/1,2/2,.9/n}{
\node[pFlow,text width=2.4cm] (x\i) at(5,\y){$X_{\i}=Z$};
\draw[pEdge](z.east)--++(.4,0)|-(x\i.west);}
\node[pFlow,text width=1.7cm] (m) at(8.25,2){$\bar X=Z$};
\foreach \i in {1,2,n}{\draw[pEdge](x\i.east)--(m.west);}
\end{tikzpicture}
\[
\operatorname{Var}(\bar X)=\operatorname{Var}(Z).
\]
\PSmall{Tutte le osservazioni condividono la stessa variabile. La loro media conserva la variabilità di $Z$ anche con $n$ grande.}
""",r"""
\PCode{R · cento copie di un valore}{034_dipendenza_totale.R}
\PBody{Anche code molto pesanti richiedono attenzione: il limite centrale classico qui usato assume varianza finita.}
\PInfo{La quantità di informazione dipende dal disegno e dal modello di dipendenza, oltre che dal numero di righe.}
""","L'indipendenza e i momenti finiti sono ipotesi da motivare nel problema analizzato.")

code(35,"lab_distribuzioni","""
# n: osservazioni; B: campioni
a35 <- lab_distribuzioni(
  n = 12, B = 1000,
  population = "exp", seed = 17)
b35 <- lab_distribuzioni(
  n = 60, B = 1000,
  population = "exp", seed = 17)
a35$indicatori
b35$indicatori
""")
S(35,"Laboratorio: forma e precisione delle medie",D,r"""
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-distribuzioni}{Esperimento · distribuzione campionaria}
"""+table(["Varia","Resta fisso","Lettura"],
 [["$n=12,60$","$B=1000$, Exp(1)","forma e SE"],
  ["$B=200,1000$","$n=60$, Exp(1)","stabilità numerica"],
  ["popolazione","$n=12$, $B=1000$","asimmetria"]],
 [2.75,3.35,3.35],.85)+r"""
\PBody{Per ogni scenario, confrontare la SD delle medie con $1/\sqrt n$. Annotare quale parametro cambia e che cosa rappresenta ciascun punto dell'istogramma.}
\PInfo{Nel sito: $12\le n\le300$, $40\le B\le1000$. Entrambe le popolazioni hanno media e varianza unitarie.}
""",r"""
\PCode{R · due scenari riproducibili}{035_lab_distribuzioni.R}
\PSmall{Le funzioni \texttt{lab\_distribuzioni()} sono nel progetto. Gli argomenti corrispondono ai controlli del sito.}
""","Per interpretare una simulazione occorre distinguere la dimensione del campione dal numero delle repliche.")

code(36,"varianza","""
x36 <- c(4, 5, 6, 9)
sc36 <- x36 - mean(x36)
sum(sc36)  # Scarti vincolati
sum(sc36^2)/(length(x36)-1)
var(x36)   # Stesso denominatore
sd(x36)^2
""")
S(36,"La varianza campionaria usa n meno uno",E,r"""
\PLabel{Gli scarti dipendono dalla media stimata}
\[
\sum_i(X_i-\bar X)^2
=\sum_i(X_i-\mu)^2-n(\bar X-\mu)^2.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.1,1.6){$\mathbb E\sum_i(X_i-\mu)^2$\\$n\sigma^2$};
\node[pFlow,text width=3.5cm] (b) at(7.4,1.6){$\mathbb E[n(\bar X-\mu)^2]$\\$\sigma^2$};
\node[pLabel] at(4.8,1.6){$-$};
\node[pNote] at(4.8,.35){rimane $(n-1)\sigma^2$};
\end{tikzpicture}
\[
S^2=\frac{\sum_i(X_i-\bar X)^2}{n-1},
\qquad \mathbb E(S^2)=\sigma^2.
\]
\PSmall{L'ultimo risultato richiede osservazioni IID con varianza finita.}
""",r"""
\PCode{R · la somma dei quadrati}{036_varianza.R}
\PBody{Gli scarti dalla media sommano a zero. Dopo averne fissati $n-1$, l'ultimo è determinato.}
\PInfo{\texttt{var()} e \texttt{sd()} usano il denominatore $n-1$. La correzione rende non distorta $S^2$ nel modello IID.}
""","Il denominatore n meno uno corregge la stima della varianza quando la media è stimata dallo stesso campione.")

code(37,"sd_se","""
f37 <- read.csv(
  "Dati/fossili_simulati.csv")
p37 <- subset(f37,
              morfotipo == "Rounded")
x37 <- p37$diametro_tot_um
n37 <- length(x37)
s37 <- sd(x37)
c(SD = s37, SE = s37/sqrt(n37))
""")
S(37,"Dispersione dei dati e precisione della media",E,r"""
\PLabel{Diametri sintetici del gruppo Rounded}
"""+table(["Oggetto","Quantità","Valore"],
 [["singoli fossili","$s$","$1{,}000\\ \\mu\\mathrm m$"],
  ["media di 80 fossili","$s/\\sqrt{80}$","$0{,}112\\ \\mu\\mathrm m$"]],
 [4.1,2.35,2.9],.95)+r"""
\[
\widehat{\operatorname{SE}}(\bar X)=\frac{S}{\sqrt n}.
\]
\PBody{La SD riassume le differenze fra individui. Il SE stima la dispersione che avrebbe la media in campioni indipendenti della stessa dimensione.}
\PSmall{La formula richiede un disegno compatibile con osservazioni indipendenti e identicamente distribuite.}
""",r"""
\PCode{R · due misure, stessa unità}{037_sd_se.R}
\PBody{Entrambi i numeri sono espressi in micrometri. Per interpretarli occorre indicare quale oggetto varia.}
\PInfo{I 160 fossili del progetto sono sintetici. Il gruppo Rounded comprende 80 individui.}
""","La deviazione standard descrive le osservazioni. L'errore standard descrive la variabilità dello stimatore.")

code(38,"covarianze","""
# Quattro osservazioni, varianza 1
S38 <- matrix(.2, 4, 4)
diag(S38) <- 1
w38 <- rep(1/4, 4)
# Varianza della loro media
drop(t(w38) %*% S38 %*% w38)
sum(S38) / 4^2
""")
S(38,"Nella varianza entrano anche le covarianze",E,r"""
\PLabel{La formula generale della media}
\[
\operatorname{Var}(\bar X)=\frac1{n^2}
\left[\sum_i\sigma_i^2+
2\sum_{i<j}\operatorname{Cov}(X_i,X_j)\right].
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \i in {0,...,3}{\foreach \j in {0,...,3}{
\ifnum\i=\j\fill[GeoA!70](.8+\j*.58,2.32-\i*.58) rectangle++(.53,-.53);
\else\fill[GeoB!38](.8+\j*.58,2.32-\i*.58) rectangle++(.53,-.53);\fi}}
\node[pLabel] at(1.95,-.45){$\Sigma$};
\node[pDotA] at(4.1,1.95){};
\node[pLabel,anchor=west] at(4.4,1.95){diagonale: varianze};
\node[pDotB] at(4.1,1.25){};
\node[pLabel,anchor=west] at(4.4,1.25){altre celle: covarianze};
\node[pLabel] at(6.2,.25){$\operatorname{Var}(\bar X)=w^\top\Sigma w$};
\end{tikzpicture}
\PSmall{Per la media semplice, $w_i=1/n$. Covarianze positive aumentano la varianza a parità di varianze individuali.}
""",r"""
\PCode{R · sommare la matrice}{038_covarianze.R}
\PBody{\texttt{diag()} imposta le varianze. Le altre celle contengono covarianze pari a $0{,}2$.}
\PInfo{Con covarianze nulle e varianza comune $\sigma^2$, la formula si riduce a $\operatorname{Var}(\bar X)=\sigma^2/n$.}
""","L'errore standard dipende dalla struttura congiunta delle osservazioni.")

code(39,"equicorrelazione","""
n39 <- 60
rho39 <- .2
deff39 <- 1 + (n39-1)*rho39
c(SE = sqrt(deff39/n39),
  n_eff = n39/deff39)
# Varianza marginale fissata a 1
""")
S(39,"Una componente comune a tutte le misure",E,r"""
\PLabel{Il modello equicorrelato del laboratorio}
\[
X_i=\sqrt\rho\,U+\sqrt{1-\rho}\,\varepsilon_i,
\quad U,\varepsilon_1,\ldots,\varepsilon_n
\overset{\mathrm{iid}}\sim\mathcal N(0,1).
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=1.5cm,fill=GeoB!10] (u) at(4.7,2.05){$U$};
\foreach \x/\i in {1.3/1,4.7/2,8.1/n}{
\node[pFlow,text width=1.8cm] (x\i) at(\x,.15){$X_{\i}$};
\draw[pEdge](u)--(x\i);}
\node[pNote,anchor=west] at(6.05,2.05){effetto comune};
\end{tikzpicture}
\[
\operatorname{Var}(\bar X)=\frac{1+(n-1)\rho}{n},
\qquad n_{\mathrm{eff}}=\frac{n}{1+(n-1)\rho}.
\]
\PSmall{Ogni misura ha varianza uno. Ogni coppia ha correlazione comune $0\le\rho\le1$.}
""",r"""
\PCode{R · l'effetto della dipendenza}{039_equicorrelazione.R}
\PBody{Con $n=60$ e $\rho=0{,}2$: $\mathrm{SE}=0{,}462$ e $n_{\mathrm{eff}}=4{,}6875$.}
\PInfo{Qui $n_{\mathrm{eff}}$ è la numerosità indipendente equivalente per il SE, con varianza uno. Dipende da questo specifico modello.}
""","Un effetto condiviso da tutte le misure può mantenere elevata l'incertezza della media.")

o,xx,yy=axes(-1.8,1.8,1.35,[-1.5,-.5,0,.5,1.5],[0,.5,1],r"$\bar x$: media della campagna","densità",2.45)
for r in rows("dipendenza"):
    a,b,y=float(r["sinistra"]),float(r["destra"]),float(r["densita"])
    o.append(rf"\fill[GeoA!40]({xx(a):.4f},0) rectangle({xx(b):.4f},{yy(y):.4f});")
for a in [-1.96/math.sqrt(60),1.96/math.sqrt(60)]:
    o.append(rf"\draw[GeoB,dashed,line width=1pt]({xx(a):.4f},0)--({xx(a):.4f},{yy(1.3):.4f});")
o += [r"\node[pNote,text=GeoB,anchor=west] at(6.3,2.35){$\pm1{,}96/\sqrt{60}$};"]
code(40,"lab_dipendenza","""
a40 <- lab_dipendenza(
  n = 60, B = 200,
  rho = 0, seed = 17)
b40 <- lab_dipendenza(
  n = 60, B = 200,
  rho = .2, seed = 17)
a40$indicatori
b40$indicatori
""")
S(40,"Laboratorio: la dispersione sottostimata",E,r"""
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-dipendenza}{Esperimento · errore standard e dipendenza}
"""+end(o)+r"""
\PSmall{Figura: $n=60$, $B=200$, $\rho=0{,}2$, seme 17. Le linee delimitano il riferimento centrale che assumerebbe indipendenza e varianza nota.}
\PInfo{Per $\rho>0$ fissata, $\operatorname{Var}(\bar X)\to\rho$. Aggiungere misure nella stessa campagna lascia una componente di incertezza comune.}
""",r"""
\PCode{R · isolare il ruolo di rho}{040_lab_dipendenza.R}
\PSmall{Le campagne sono indipendenti fra loro. All'interno di ciascuna campagna, tutte le misure condividono un nuovo valore di $U$.}
""","Il riferimento che ignora la correlazione può essere molto più stretto della distribuzione effettiva delle medie.")

code(41,"stazioni","""
G41 <- 6   # Stazioni indipendenti
m41 <- 4   # Provini per stazione
rho41 <- .6
deff41 <- 1 + (m41-1)*rho41
n41 <- G41*m41
c(DEFF = deff41, n_eff = n41/deff41)
""")
S(41,"Stazioni indipendenti, provini correlati",E,r"""
\PLabel{La componente comune riguarda ciascuna stazione}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \i in {0,...,5}{\foreach \j in {0,...,5}{
\pgfmathtruncatemacro{\gi}{floor(\i/3)}
\pgfmathtruncatemacro{\gj}{floor(\j/3)}
\ifnum\i=\j\fill[GeoA!75](.65+\j*.4,2.45-\i*.4) rectangle++(.36,-.36);
\else\ifnum\gi=\gj\fill[GeoB!45](.65+\j*.4,2.45-\i*.4) rectangle++(.36,-.36);
\else\draw[Rule](.65+\j*.4,2.45-\i*.4) rectangle++(.36,-.36);\fi\fi}}
\node[pNote] at(1.8,-.25){schema: 2 stazioni, 3 provini};
\node[pLabel,text width=5.2cm,align=left] at(6.4,1.6){Covarianze entro stazione.\\Covarianze nulle fra stazioni.};
\end{tikzpicture}
\[
\operatorname{Var}(\bar X)=
\frac{\sigma^2}{Gm}\,[1+(m-1)\rho].
\]
\PSmall{$G$ stazioni indipendenti, $m$ provini per stazione, varianza comune $\sigma^2$ e correlazione interna comune $\rho$.}
""",r"""
\PCode{R · un disegno bilanciato}{041_stazioni.R}
\PBody{Con $G=6$, $m=4$ e $\rho=0{,}6$: $\mathrm{DEFF}=2{,}8$, $n_{\mathrm{eff}}=8{,}57$.}
\PInfo{Il moltiplicatore contiene $m-1$. Nel modello della slide precedente tutte le $n$ misure appartenevano alla stessa componente comune.}
""","Nel campionamento per stazioni, la correlazione interna e il numero di stazioni determinano la precisione.")

o,xx,yy=axes(4,100,.55,[4,25,50,100],[0,.1,.3,.5],"$n$: unità indipendenti","SE della media",2.5)
line(o,[(n,1/math.sqrt(n)) for n in range(4,101)],xx,yy)
for n in [25,100]:
    o.append(rf"\fill[GeoB]({xx(n):.4f},{yy(1/math.sqrt(n)):.4f}) circle(2.7pt);")
o += [r"\node[pNote,text=GeoB] at(3.15,1.4){$25:\ 0{,}20$};",
      r"\node[pNote,text=GeoB,anchor=east] at(8.85,.95){$100:\ 0{,}10$};"]
code(42,"radice_n","""
n42 <- c(4, 25, 100)
se42 <- 1/sqrt(n42)
data.frame(n = n42, SE = se42)
# Rapporto: da 25 a 100
sqrt(25/100)
""")
S(42,"Il costo di dimezzare l'errore standard",E,r"""
\PLabel{Varianza individuale costante e unità indipendenti}
"""+end(o)+r"""
\[
\frac{\operatorname{SE}_{n_2}}{\operatorname{SE}_{n_1}}
=\sqrt{\frac{n_1}{n_2}},
\qquad n_2=4n_1\ \Longrightarrow\
\operatorname{SE}_{n_2}=\tfrac12\operatorname{SE}_{n_1}.
\]
\PSmall{Il grafico assume $\sigma=1$. I guadagni assoluti diminuiscono quando $n$ è già elevato.}
""",r"""
\PCode{R · la legge della radice}{042_radice_n.R}
\PBody{Passare da 25 a 100 unità indipendenti riduce il SE da $0{,}20$ a $0{,}10$.}
\PInfo{La pianificazione deve contare le unità che forniscono informazione indipendente. Più provini nello stesso sito possono avere un rendimento diverso.}
""","Con varianza costante e indipendenza, dimezzare il SE richiede di quadruplicare la numerosità.")

code(43,"proporzione","""
evento43 <- c(rep(1, 18), rep(0, 42))
n43 <- length(evento43)
p43 <- mean(evento43)
sqrt(p43*(1-p43)/n43)
# Con zero eventi la stima e' zero:
# non implica certezza su p.
""")
o,xx,yy=axes(0,1,.07,[0,.25,.5,.75,1],[0,.02,.04,.06],"$p$: probabilità dell'evento","SE teorico",2.4)
o=[s.replace("at(-.18","at(-.45") for s in o]
line(o,[(p/100,math.sqrt((p/100)*(1-p/100)/60)) for p in range(101)],xx,yy)
o.append(r"\node[pNote] at(7.55,2.1){$n=60$};")
S(43,"L'errore standard di una proporzione",E,r"""
\PLabel{La proporzione è una media di indicatori}
"""+end(o)+r"""
\[
\hat p=\frac1n\sum_iY_i,\qquad
\operatorname{SE}(\hat p)=\sqrt{\frac{p(1-p)}n}.
\]
\PSmall{$Y_i$ sono Bernoulli indipendenti con la stessa probabilità $p$. Il SE è adimensionale.}
""",r"""
\PCode{R · proporzione osservata}{043_proporzione.R}
\PBody{Sostituire $p$ con $\hat p$ fornisce una stima semplice del SE. Ai bordi può essere inadeguata.}
\PInfo{Zero eventi osservati lascia incertezza su $p$. Gli intervalli per proporzioni devono tenerne conto.}
""","La formula di una proporzione deriva dalla varianza della media di variabili Bernoulli indipendenti.")

code(44,"popolazione_finita","""
pop44 <- c(2, 4, 6, 8, 10)
m44 <- colMeans(combn(pop44, 2))
# Varianza esatta sui 10 campioni
mean((m44-mean(pop44))^2)
# Formula senza reinserimento
(1-2/length(pop44))*var(pop44)/2
""")
S(44,"Campionare senza reinserimento",E,r"""
\PLabel{Popolazione finita e campione casuale semplice}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \x/\v in {1/2,2.8/4,4.6/6,6.4/8,8.2/10}{
\node[pFlow,minimum width=1cm,fill=white] at(\x,1.7){$\v$};}
\draw[GeoB,line width=1.2pt,rounded corners=2mm](.35,.95) rectangle(1.65,2.45);
\draw[GeoB,line width=1.2pt,rounded corners=2mm](5.75,.95) rectangle(7.05,2.45);
\node[pNote] at(4.6,.35){esempio di campione: $\{2,8\}$, media $5$};
\end{tikzpicture}
\[
\operatorname{Var}_d(\bar Y_s)
=\left(1-\frac{n}{N_U}\right)\frac{S_U^2}{n}.
\]
\PSmall{$N_U$ è la popolazione finita. $S_U^2$ usa il denominatore $N_U-1$. Tutti i campioni di $n$ unità hanno la stessa probabilità.}
""",r"""
\PCode{R · enumerare tutti i campioni}{044_popolazione_finita.R}
\PBody{Qui $N_U=5$ e $n=2$. Le dieci medie possibili hanno varianza $3$, come la formula.}
\PInfo{Con $n=N_U$ l'incertezza di campionamento è zero. Possono restare errori di misura o altre fonti di incertezza.}
""","La correzione per popolazione finita dipende dal campionamento casuale semplice senza reinserimento.")

code(45,"strati","""
f45 <- read.csv(
  "Dati/fossili_simulati.csv")
g45 <- split(f45$diametro_tot_um,
             f45$morfotipo)
w45 <- c(Rounded = .5, Spiky = .5)
se45 <- sqrt(sum(w45^2 *
  sapply(g45, var)/lengths(g45)))
se45
""")
S(45,"Pesi fissati e campioni stratificati",E,r"""
\PLabel{La varianza di una somma pesata}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.1cm] (a) at(1.8,2.3){Rounded\\$\bar X_R,\ n_R=80$};
\node[pFlow,text width=3.1cm] (b) at(7.5,2.3){Spiky\\$\bar X_S,\ n_S=80$};
\node[pFlow,text width=3.8cm,fill=GeoA!10] (m) at(4.65,.4){$\hat\mu_{\mathrm{str}}=\tfrac12\bar X_R+\tfrac12\bar X_S$};
\draw[pEdge](a)--node[pNote,left]{$W_R=\tfrac12$}(m);
\draw[pEdge](b)--node[pNote,right]{$W_S=\tfrac12$}(m);
\end{tikzpicture}
\[
\operatorname{Var}(\hat\mu_{\mathrm{str}})
=\sum_h W_h^2\frac{\sigma_h^2}{n_h}.
\]
\PSmall{Osservazioni IID entro strato e campioni indipendenti fra strati. Pesi fissati con $\sum_h W_h=1$. La formula non include la correzione per popolazione finita.}
""",r"""
\PCode{R · contributi alla varianza}{045_strati.R}
\PBody{Ogni varianza entra con il peso al quadrato. Il SE è la radice della somma.}
\PInfo{I pesi devono rappresentare l'estimando. Quote campionarie e pesi della popolazione possono essere differenti.}
""","Per campioni stratificati indipendenti si sommano le varianze interne moltiplicate per i pesi al quadrato.")

code(46,"pianificazione","""
sigma46 <- 1  # SD pilota, micrometri
E46 <- .1     # Semiampiezza voluta
z46 <- qnorm(.975)
n46 <- ceiling((z46*sigma46/E46)^2)
n46
z46*sigma46/sqrt(n46)
""")
S(46,"Una numerosità orientata alla precisione",E,r"""
\PLabel{Semiampiezza desiderata di un intervallo normale}
\[
z_{1-\alpha/2}\frac{\sigma_0}{\sqrt n}\le E
\quad\Longrightarrow\quad
n\ge\left(\frac{z_{1-\alpha/2}\sigma_0}{E}\right)^2.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.4cm] (s) at(1.4,2.1){SD pilota\\$\sigma_0=1\ \mu\mathrm m$};
\node[pFlow,text width=2.4cm] (e) at(5,2.1){Tolleranza\\$E=0{,}1\ \mu\mathrm m$};
\node[pFlow,text width=2.1cm,fill=GeoA!10] (n) at(8.3,.5){$n=385$};
\draw[pEdge](s.south)--++(0,-1.6)--(n.west);
\draw[pEdge](e.south)--++(0,-.8)--(n.north);
\end{tikzpicture}
\PSmall{Livello nominale 95\%, unità indipendenti, varianza pilota pertinente. L'arrotondamento va all'intero superiore.}
""",r"""
\PCode{R · dalla precisione a n}{046_pianificazione.R}
\PBody{\texttt{ceiling()} arrotonda per eccesso. Il valore è una prima pianificazione basata su un'approssimazione normale.}
\PInfo{Dipendenza, perdite di campioni e incertezza della SD pilota richiedono un riesame della numerosità prevista.}
""","La precisione desiderata deve essere espressa nelle unità della quantità stimata e riferita al disegno previsto.")

o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
xx=lambda v:2.1+6.9*(v-4.8)/(7.4-4.8)
for y,a,label,col in [(2.5,ST["sd_R"],r"$\bar x\pm s$","GeoB"),(1.5,ST["se_R"],r"$\bar x\pm\widehat{\mathrm{SE}}$","GeoA"),(.5,ST["q_R"]*ST["se_R"],r"IC 95\%","GeoC")]:
    x=ST["media_R"]
    o += [rf"\node[pLabel,anchor=east] at(1.9,{y}){{{label}}};",
          rf"\draw[{col},line width=1.7pt]({xx(x-a):.4f},{y})--({xx(x+a):.4f},{y});",
          rf"\fill[{col}]({xx(x):.4f},{y}) circle(2.5pt);"]
    for edge in [x-a,x+a]:
        o.append(rf"\draw[{col},line width=1pt]({xx(edge):.4f},{y-.12})--({xx(edge):.4f},{y+.12});")
o.append(r"\draw[pAxis](2.1,-.1)--(9.15,-.1);")
for val in [5,6,7]:
    o.append(rf"\node[pNote,below] at({xx(val):.4f},-.14){{$ {val} $}};")
o.append(r"\node[pNote] at(5.55,-.7){diametro ($\mu\mathrm m$)};")
code(47,"barre","""
f47 <- read.csv(
  "Dati/fossili_simulati.csv")
p47 <- subset(f47,
              morfotipo == "Rounded")
x47 <- p47$diametro_tot_um
s47 <- sd(x47); n47 <- length(x47)
c(SD = s47, SE = s47/sqrt(n47),
  IC95 = qt(.975,n47-1)*s47/sqrt(n47))
""")
S(47,"Tre significati delle barre",E,r"""
\PLabel{Stessa media, quantità rappresentate differenti}
"""+end(o)+r"""
\PBody{La prima barra descrive dispersione individuale. La seconda mostra un SE. La terza è un intervallo per la media costruito con il quantile di Student.}
\PSmall{Dati sintetici Rounded, $n=80$. La barra $\bar x\pm s$ non assegna una copertura individuale prefissata.}
""",r"""
\PCode{R · le tre semiampiezze}{047_barre.R}
\PInfo{Una didascalia completa dichiara: quantità rappresentata, livello quando presente, unità e numero di unità indipendenti.}
""","L'ampiezza di una barra si interpreta solo dopo averne identificato la definizione.")

o,xx,yy=axes(-4,4,.43,[-4,-2,0,2,4],[0,.2,.4],"$t$: perno di Student","densità",2.4)
rr=rows("student")
q19=2.093024054408263
shade=[(float(r["t"]),float(r["t19"])) for r in rr if -q19<=float(r["t"])<=q19]
o.append(r"\fill[GeoA!20] "+f"({xx(-q19):.5f},0)--"+
         "--".join(f"({xx(x):.5f},{yy(y):.5f})" for x,y in shade)+
         f"--({xx(q19):.5f},0)--cycle;")
line(o,[(float(r["t"]),float(r["t19"])) for r in rr],xx,yy)
for q in [-q19,q19]:
    o.append(rf"\draw[GeoB,dashed]({xx(q):.4f},0)--({xx(q):.4f},1.2);")
o.append(r"\node[pLabel] at(4.8,1.25){area $0{,}95$};")
code(48,"student","""
n48 <- 20
q48 <- qt(.975, df = n48-1)
q48  # Circa 2.093
# Area centrale della Student
pt(q48, n48-1) - pt(-q48, n48-1)
""")
S(48,"Il perno di Student",I,r"""
\PLabel{Campione normale indipendente, varianza ignota}
"""+end(o)+r"""
\[
T=\frac{\bar X-\mu}{S/\sqrt n}\sim t_{n-1}.
\]
\PSmall{Per $n=20$ i gradi di libertà sono 19. Un perno ha distribuzione che non dipende dai parametri ignoti del modello.}
""",r"""
\PCode{R · il quantile critico}{048_student.R}
\PSmall{La normalità IID rende indipendenti $Z=\sqrt n(\bar X-\mu)/\sigma$ e $U=(n-1)S^2/\sigma^2$.}
\PInfo{$Z\sim\mathcal N(0,1)$, $U\sim\chi^2_{n-1}$ e $T=Z/\sqrt{U/(n-1)}$. Da qui nasce la distribuzione di Student.}
""","L'intervallo di Student ha copertura esatta nel modello normale IID con varianza positiva.")

code(49,"intervallo_t","""
# Esempio costruito, n = 6
x49 <- c(4.2, 5.1, 5.4, 6, 6.3, 7)
n49 <- length(x49)
se49 <- sd(x49)/sqrt(n49)
q49 <- qt(.975, n49-1)
mean(x49) + c(-1,1)*q49*se49
""")
S(49,"Dal perno agli estremi dell'intervallo",I,r"""
\PLabel{Lo stesso evento scritto in funzione del parametro}
\[
\Pr\!\left\{-q\le
\frac{\bar X-\mu}{S/\sqrt n}\le q\right\}=1-\alpha,
\qquad q=t_{n-1;\,1-\alpha/2}.
\]
\[
-q\frac{S}{\sqrt n}\le \bar X-\mu
\le q\frac{S}{\sqrt n}.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\path[use as bounding box](0,.2) rectangle(9.4,1.05);
\draw[pEdge](4.7,1)--(4.7,.25);
\node[pNote,anchor=west] at(5.1,.6){isoliamo $\mu$};
\end{tikzpicture}
\[
\bar X-q\frac{S}{\sqrt n}
\le\mu\le
\bar X+q\frac{S}{\sqrt n}.
\]
\PSmall{Moltiplichiamo per $S/\sqrt n>0$, quindi isoliamo $\mu$. Gli estremi dipendono dal campione.}
""",r"""
\PCode{R · centro e semiampiezza}{049_intervallo_t.R}
\PBody{\texttt{c(-1,1)} costruisce i due estremi: sottrae e somma la stessa semiampiezza alla media.}
\PInfo{Prima dell'osservazione, l'intervallo è casuale e $\mu$ è fissato. Dopo l'osservazione, gli estremi diventano numeri.}
""","L'intervallo nasce dall'inversione di un evento del perno, sotto le ipotesi del modello.")

code(50,"livelli","""
liv50 <- c(.80, .90, .95, .99)
q50 <- qt((1+liv50)/2, df = 19)
data.frame(livello = liv50,
           quantile = q50)
# La semiampiezza e' quantile * SE.
""")
o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
for j,(lev,q,col) in enumerate([("80",1.327728209,"Muted"),("90",1.729132812,"GeoA"),("95",q19,"GeoB"),("99",2.860934606,"GeoC")]):
    y=3.1-j*.85
    o += [rf"\node[pLabel,anchor=east] at(1.55,{y}){{{lev}\%}};",
          rf"\draw[{col},line width=1.4pt]({5.3-q:.4f},{y})--({5.3+q:.4f},{y});",
          rf"\fill[{col}](5.3,{y}) circle(2.4pt);",
          rf"\node[pNote,anchor=west] at(8.4,{y}){{$q={fmt(q,3)}$}};"]
o += [r"\draw[Rule,dashed](5.3,.05)--(5.3,3.55);",
      r"\node[pNote] at(5.3,-.35){stesso centro e stesso SE};"]
S(50,"Più confidenza richiede un intervallo più ampio",I,r"""
\PLabel{Student con 19 gradi di libertà}
"""+end(o)+r"""
\[
|C(\mathbf X)|=2\,t_{n-1;\,1-\alpha/2}\frac{S}{\sqrt n}.
\]
\PSmall{Le lunghezze sono proporzionali al quantile $q$. Dati e numerosità rimangono fissati.}
""",r"""
\PCode{R · quattro livelli nominali}{050_livelli.R}
\PBody{Il quantile dipende dal livello richiesto e dai gradi di libertà.}
\PInfo{Con pochi gradi di libertà, le code della Student sono più pesanti di quelle normali. Il moltiplicatore $1{,}96$ non è universale.}
""","L'ampiezza dell'intervallo dipende dalla dispersione dei dati, dalla numerosità e dal livello nominale.")

code(51,"ic_fossili","""
f51 <- read.csv(
  "Dati/fossili_simulati.csv")
p51 <- subset(f51,
              morfotipo == "Rounded")
x51 <- p51$diametro_tot_um
n51 <- length(x51)
q51 <- qt(.975, n51-1)
se51 <- sd(x51)/sqrt(n51)
mean(x51) + c(-1,1)*q51*se51
t.test(x51)$conf.int
""")
o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
xx=lambda v:.6+8.25*(v-5.7)/.7
o.append(r"\draw[pAxis](.6,.7)--(9.1,.7);")
o.append(rf"\draw[GeoA,line width=2pt]({xx(ST['ic_inf']):.4f},1.6)--({xx(ST['ic_sup']):.4f},1.6);")
o.append(rf"\fill[GeoA]({xx(ST['media_R']):.4f},1.6) circle(3pt);")
for key in ["ic_inf","ic_sup"]:
    v=ST[key]
    o.append(rf"\draw[GeoA,line width=1.2pt]({xx(v):.4f},1.42)--({xx(v):.4f},1.78);")
    o.append(rf"\node[pLabel] at({xx(v):.4f},1.02){{$ {fmt(v)} $}};")
o.append(rf"\node[pLabel] at({xx(ST['media_R']):.4f},2.2){{$\bar x={fmt(ST['media_R'])}$}};")
o.append(r"\node[pNote] at(4.7,.2){diametro ($\mu\mathrm m$)};")
S(51,"Un intervallo per la media dei diametri",I,r"""
\PLabel{Ottanta fossili sintetici Rounded}
"""+end(o)+r"""
\[
\begin{aligned}
\bar x&=6{,}064\ \mu\mathrm m,\quad
s=1{,}000\ \mu\mathrm m,\\
q&=1{,}990,\quad
\widehat{\mathrm{SE}}=0{,}112\ \mu\mathrm m.
\end{aligned}
\]
\PBody{L'intervallo al 95\% è $[5{,}841;\,6{,}286]\ \mu\mathrm m$. I numeri riassumono questo campione sintetico entro le ipotesi adottate.}
""",r"""
\PCode{R · calcolo esplicito e funzione}{051_ic_fossili.R}
\PSmall{\texttt{\$conf.int} estrae l'intervallo restituito dalla funzione.}
\PInfo{L'inferenza richiede un campionamento e un modello compatibili con l'intervallo.}
""","Un risultato completo riporta stima, intervallo, unità, numerosità e condizioni della procedura.")

o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
xx=lambda v:.8+8.0*(v-9.1)/1.9
for r in rows("copertura_indipendente")[:40]:
    k=int(r["replica"]);y=.15+(40-k)*.083
    col="GeoA" if r["copre"]=="TRUE" else "GeoB"
    o.append(rf"\draw[{col},line width=.7pt]({xx(float(r['inferiore'])):.4f},{y:.4f})--({xx(float(r['superiore'])):.4f},{y:.4f});")
    o.append(rf"\fill[{col}]({xx(float(r['media'])):.4f},{y:.4f}) circle(.75pt);")
o += [rf"\draw[Muted,dashed]({xx(10):.4f},0)--({xx(10):.4f},3.58);",
      r"\draw[pAxis](.8,0)--(9,0);"]
for v in [9.2,9.6,10,10.4,10.8]:
    o.append(rf"\node[pNote,below] at({xx(v):.4f},-.08){{$ {v:g} $}};")
for k in [1,10,20,30,40]:
    o.append(rf"\node[pNote,anchor=east] at(.67,{.15+(40-k)*.083:.4f}){{$ {k} $}};")
o += [r"\node[pNote,rotate=90] at(-.15,1.8){replica};",
      r"\node[pNote] at(4.8,-.62){media e intervallo};",
      r"\node[pNote,anchor=west] at(.8,3.75){Prime 40 repliche: normale IID, $n=30$};"]
code(52,"copertura","""
a52 <- lab_intervalli(
  n = 30, B = 200, rho = 0,
  level = .95, seed = 17)
sum(a52$dati$copre)  # 187 su 200
mean(a52$dati$copre)
a52$indicatori
""")
S(52,"La copertura riguarda le ripetizioni",I,r"""
\PLabel{La media della popolazione rimane fissata a 10}
"""+end(o)+r"""
\PSmall{Figura: prime 40 delle 200 repliche. Gli intervalli arancioni escludono $\mu=10$. La copertura usa tutte le 200 repliche e vale $0{,}935$ in questa esecuzione.}
""",r"""
\PCode{R · contare gli intervalli che coprono}{052_copertura.R}
\[
\hat c=\frac1B\sum_{b=1}^B
\mathbf1_{\{\mu\in C_b\}}.
\]
\PInfo{Il livello nominale è $0{,}95$. La frequenza simulata oscilla e non deve coincidere esattamente con quel valore.}
""","Il 95 per cento descrive la copertura della procedura in ripetizioni compatibili con il modello.")

code(53,"lab_intervalli","""
b53 <- lab_intervalli(
  n = 30, B = 200, rho = .2,
  level = .95, seed = 17)
b53$indicatori
c53 <- mean(b53$dati$copre)
# SE Monte Carlo della copertura
sqrt(c53*(1-c53)/200)
""")
S(53,"Laboratorio: copertura e modello di dipendenza",I,r"""
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-intervalli}{Esperimento · copertura degli intervalli}
"""+table(["Correlazione","Copertura osservata","SE Monte Carlo"],
 [["$\\rho=0$","$0{,}935$","$0{,}017$"],
  ["$\\rho=0{,}2$","$0{,}490$","$0{,}035$"]],
 [2.55,3.55,3.3],.9)+r"""
\PBody{Il generatore introduce una componente comune. La formula dell'intervallo continua a usare $s/\sqrt n$, che assume indipendenza.}
\PInfo{Scenari: $n=30$, $B=200$, seme 17, livello 95\%. Nel sito il grafico mostra le prime 80 repliche, mentre il riepilogo usa tutte le $B$.}
""",r"""
\PCode{R · una formula fuori dalle ipotesi}{053_lab_intervalli.R}
\[
\widehat{\mathrm{SE}}_{\mathrm{MC}}(\hat c)
=\sqrt{\frac{\hat c(1-\hat c)}B}.
\]
\PSmall{Aumentare $B$ stabilizza la misura della copertura. La correlazione fra le osservazioni rimane.}
""","Una copertura scorretta può essere stimata con grande precisione numerica.")

o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
xx=lambda v:1.9+7.1*(v-3.8)/4.5
for y,keys,lab,col in [(1.8,["ic_inf","ic_sup"],r"media $\mu$","GeoA"),(.7,["ip_inf","ip_sup"],r"$X_{\mathrm{nuovo}}$","GeoB")]:
    a,b=ST[keys[0]],ST[keys[1]]
    o += [rf"\node[pLabel,anchor=east] at(1.7,{y}){{{lab}}};",
          rf"\draw[{col},line width=1.6pt]({xx(a):.4f},{y})--({xx(b):.4f},{y});",
          rf"\fill[{col}]({xx(ST['media_R']):.4f},{y}) circle(2.5pt);"]
o.append(r"\draw[pAxis](1.9,0)--(9.1,0);")
for v in [4,5,6,7,8]:
    o.append(rf"\node[pNote,below] at({xx(v):.4f},-.09){{$ {v} $}};")
o.append(r"\node[pNote] at(5.5,-.6){diametro ($\mu\mathrm m$)};")
code(54,"previsione","""
# x51: diametri Rounded
n54 <- length(x51)
q54 <- qt(.975, n54-1)
mean(x51) + c(-1,1)*q54 *
  sd(x51)*sqrt(1+1/n54)
# Include la variabilita' futura.
""")
S(54,"Media della popolazione e nuova osservazione",I,r"""
\PLabel{Due domande nel modello normale IID}
"""+end(o)+r"""
\[
\begin{aligned}
C_\mu&=\bar X\pm q\,S/\sqrt n,\\
I_{\mathrm{pred}}&=\bar X\pm q\,S\sqrt{1+1/n}.
\end{aligned}
\]
\PSmall{Per il nuovo individuo si aggiunge la varianza $\sigma^2$: $\operatorname{Var}(X_{\mathrm{nuovo}}-\bar X)=\sigma^2(1+1/n)$.}
""",r"""
\PCode{R · intervallo predittivo al 95\%}{054_previsione.R}
\PBody{Nel caso Rounded, l'intervallo predittivo è $[4{,}060;\,8{,}067]\ \mu\mathrm m$.}
\PInfo{Il nuovo individuo deve essere indipendente dal campione e provenire dalla stessa popolazione normale.}
""","La previsione individuale include la variabilità del nuovo individuo oltre all'incertezza sulla media.")

code(55,"contrasto","""
f55 <- read.csv(
  "Dati/fossili_simulati.csv")
g55 <- split(f55$diametro_tot_um,
             f55$morfotipo)
S55 <- g55$Spiky; R55 <- g55$Rounded
mean(S55) - mean(R55)
t.test(S55, R55,
       var.equal = FALSE)$conf.int
""")
S(55,"Un intervallo per due medie indipendenti",I,r"""
\PLabel{Orientamento fissato: Spiky meno Rounded}
\[
\hat\Delta=\bar X_S-\bar X_R,\qquad
a=\frac{S_S^2}{n_S},\quad b=\frac{S_R^2}{n_R}.
\]
\[
\widehat{\mathrm{SE}}(\hat\Delta)=\sqrt{a+b},
\quad
\nu=\frac{(a+b)^2}
{a^2/(n_S-1)+b^2/(n_R-1)}.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,.6)--(9,.6);
\draw[Muted,dashed](.9,.25)--(.9,1.8);
\draw[GeoA,line width=2pt](3.14,1.1)--(7.95,1.1);
\fill[GeoA](5.55,1.1) circle(3pt);
\node[pNote] at(.9,.05){$0$};
\node[pNote] at(3.14,.05){$0{,}282$};
\node[pNote] at(7.95,.05){$0{,}882$};
\node[pLabel] at(5.55,1.7){$\hat\Delta=0{,}582\ \mu\mathrm m$};
\end{tikzpicture}
\PSmall{Intervallo di Welch: $\hat\Delta\pm t_{\nu;\,0{,}975}\sqrt{a+b}$. Gruppi indipendenti, varianze stimate separatamente. Normalità entro gruppo o approssimazione adeguata per le medie.}
""",r"""
\PCode{R · il contrasto e il suo intervallo}{055_contrasto.R}
\PSmall{I due gruppi sintetici hanno 80 individui ciascuno. L'approssimazione di Welch fornisce qui $\nu\simeq156{,}89$.}
\PInfo{Il segno dipende dall'ordine degli argomenti. M06 svilupperà il rapporto fra effetto, intervallo e test.}
""","Un contrasto richiede un ordine esplicito dei gruppi e un errore standard coerente con il disegno.")

code(56,"differenze","""
# Tre coppie costruite, micrometri
tot56 <- c(7.2, 5.8, 6.4)
int56 <- c(6.3, 5.0, 5.3)
d56 <- tot56 - int56
d56
sd(d56)/sqrt(length(d56))
# Il numero di coppie e' 3.
""")
S(56,"Due misure sullo stesso individuo",I,r"""
\PLabel{Il legame tra le colonne appartiene al dato}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \y/\id/\a/\b/\d in {2.9/1/{7{,}2}/{6{,}3}/{0{,}9},1.5/2/{5{,}8}/{5{,}0}/{0{,}8},.1/3/{6{,}4}/{5{,}3}/{1{,}1}}{
\draw[pGroup](.15,\y-.5) rectangle(5.9,\y+.5);
\node[pNote,anchor=west] at(.35,\y){fossile \id};
\node[pLabel] at(2.6,\y){$\a$};
\node[pLabel] at(4.65,\y){$\b$};
\node[pFlow,text width=1.65cm,minimum height=.7cm,fill=GeoA!10] (d\id) at(8.1,\y){$D_{\id}=\d$};
\draw[pEdge](6.05,\y)--(d\id);}
\node[pNote] at(2.6,3.65){totale};
\node[pNote] at(4.65,3.65){interno};
\end{tikzpicture}
\[
\operatorname{Var}(D)=\sigma_{\mathrm{tot}}^2+\sigma_{\mathrm{int}}^2
-2\operatorname{Cov}(X_{\mathrm{tot}},X_{\mathrm{int}}).
\]
\PSmall{Ogni fossile produce una differenza $D_i=X_{i,\mathrm{tot}}-X_{i,\mathrm{int}}$.}
""",r"""
\PCode{R · sottrarre entro la coppia}{056_differenze.R}
\PBody{La covarianza interna può ridurre la variabilità delle differenze. Occorre conservare l'associazione corretta fra le due misure.}
\PInfo{L'indipendenza richiesta riguarda gli individui. Il numero di coppie determina la numerosità.}
""","L'appaiamento va conservato sia nel calcolo delle differenze sia nel ricampionamento.")

o=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
yy=lambda v:.3+3.1*(v-3.7)/4.0
o += [r"\draw[pAxis](1,.3)--(1,3.65);"]
for v in [4,5,6,7]:
    o += [rf"\node[pNote,anchor=east] at(.85,{yy(v):.4f}){{$ {v} $}};",
          rf"\draw[Rule](1,{yy(v):.4f})--(8.4,{yy(v):.4f});"]
for j,r in enumerate(rows("coppie")):
    a,b=float(r["diametro_tot_um"]),float(r["diametro_int_um"])
    col="GeoB" if j==0 else "GeoA"
    o += [rf"\draw[{col},line width=.85pt](2.1,{yy(a):.4f})--(7.2,{yy(b):.4f});",
          rf"\fill[{col}](2.1,{yy(a):.4f}) circle(1.6pt);",
          rf"\fill[{col}](7.2,{yy(b):.4f}) circle(1.6pt);"]
o += [r"\node[pLabel] at(2.1,-.1){totale};",
      r"\node[pLabel] at(7.2,-.1){interno};",
      r"\node[pNote,rotate=90] at(-.05,2){diametro ($\mu\mathrm m$)};"]
code(57,"ic_appaiato","""
f57 <- read.csv(
  "Dati/fossili_simulati.csv")
p57 <- subset(f57,
              morfotipo == "Rounded")
d57 <- p57$diametro_tot_um -
       p57$diametro_int_um
c(media = mean(d57), n = length(d57))
t.test(d57)$conf.int
""")
S(57,"L'intervallo si calcola sulle differenze",I,r"""
\PLabel{Il grafico mostra otto coppie del gruppo Rounded}
"""+end(o)+r"""
\[
C_{\mu_D}=\bar D\pm t_{n-1;\,0{,}975}\frac{S_D}{\sqrt n}.
\]
\PSmall{Il calcolo usa tutte le 80 coppie: media $0{,}857\ \mu\mathrm m$, intervallo $[0{,}802;\,0{,}912]\ \mu\mathrm m$.}
""",r"""
\PCode{R · una media di differenze}{057_ic_appaiato.R}
\PBody{La normalità delle differenze rende esatto l'intervallo t. L'indipendenza riguarda le differenze di individui distinti.}
\PInfo{Separare casualmente le due colonne distruggerebbe la struttura dell'appaiamento.}
""","Il confronto appaiato si riconduce all'analisi di una variabile: la differenza entro individuo.")

code(58,"sensibilita","""
# Esempio costruito
x58 <- c(4.1,4.7,5,5.2,5.4,5.6,5.8,6)
z58 <- x58
z58[8] <- 12  # Un valore cambiato
rbind(prima = c(mean(x58), sd(x58)),
      dopo = c(mean(z58), sd(z58)))
rbind(t.test(x58)$conf.int,
      t.test(z58)$conf.int)
""")
S(58,"La formula va confrontata con i dati",I,r"""
\PLabel{Un valore influente modifica centro e dispersione}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.8,.45)--(9,.45);
\foreach \x in {1.31,1.91,2.21,2.41,2.61,2.81,3.01,3.21}{
\fill[GeoA](\x,1.6) circle(2.4pt);}
\foreach \x in {1.31,1.91,2.21,2.41,2.61,2.81,3.01}{
\fill[GeoB](\x,.8) circle(2.4pt);}
\fill[GeoB](8.55,.8) circle(2.4pt);
\draw[pEdge,draw=GeoB](3.21,1.35)--(8.55,1.05);
\node[pNote,anchor=west] at(.8,2.3){un solo valore passa da 6 a 12};
\node[pNote] at(1.31,.06){$4{,}1$};
\node[pNote] at(3.21,.06){$6$};
\node[pNote] at(8.55,.06){$12$};
\end{tikzpicture}
\PBody{L'analisi deve esaminare il disegno, la forma della distribuzione e i valori influenti. La scelta di un metodo richiede una motivazione riferita alla stessa quantità d'interesse.}
\PSmall{Il grafico è schematico. Il codice conserva gli otto valori originali e la variante costruita.}
""",r"""
\PCode{R · un controllo di sensibilità}{058_sensibilita.R}
\PInfo{Un valore insolito richiede un controllo della provenienza. La sola distanza dalla media non giustifica l'eliminazione.}
""","La stabilità del risultato e la pertinenza del disegno vanno valutate insieme alle formule inferenziali.")

S(59,"Una conclusione completa sulla stima",I,r"""
\PLabel{Dal calcolo a una frase verificabile}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=4cm] at(2.35,3.35){\textbf{Quantità d'interesse}\\media del diametro Rounded};
\node[pFlow,text width=4cm] at(7.15,3.35){\textbf{Campione}\\80 individui sintetici};
\node[pFlow,text width=4cm,fill=GeoA!8] at(2.35,1.3){\textbf{Risultato}\\$6{,}064\ \mu\mathrm m$\\IC 95\%: $[5{,}841;\,6{,}286]$};
\node[pFlow,text width=4cm,fill=GeoB!8] at(7.15,1.3){\textbf{Condizioni}\\campionamento indipendente\\modello della media pertinente};
\end{tikzpicture}
\PBody{L'intervallo quantifica l'incertezza entro il procedimento dichiarato. La selezione del campione resta parte della giustificazione scientifica.}
""",r"""
\PLabel{Domande prima del ricampionamento}
\PBody{Quale unità può essere trattata come indipendente?}
\vspace{2.8mm}
\PBody{Quale statistica stima il parametro scelto?}
\vspace{2.8mm}
\PBody{Quali legami fra osservazioni devono essere conservati?}
\vspace{2.8mm}
\PInfo{Il bootstrap costruirà repliche a partire dai dati osservati. La scelta delle unità da ricampionare dovrà rispettare queste risposte.}
""","La stima, il suo intervallo e le condizioni del campionamento devono riferirsi alla stessa domanda.")
