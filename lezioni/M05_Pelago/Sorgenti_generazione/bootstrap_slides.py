"""Pelago M05, slide 60–102: bootstrap, disegno e precisione numerica.

Grafici da bootstrap_proof/calcoli_figure.R; schema e coordinate in TikZ.
I dati dei fossili e dei provini sono sintetici e provengono dal corso.
"""
from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "bootstrap_proof/coordinate"
SLIDES, CODES = {}, {}
MET = {r["indicatore"]: float(r["valore"])
       for r in csv.DictReader((FIG / "metriche.csv").open())}
BOOT = "BOOTSTRAP ELEMENTARE"
STR = "DISEGNO DEL RICAMPIONAMENTO"
BLO = "BOOTSTRAP A BLOCCHI"
MC = "PRECISIONE NUMERICA"

def add(n, title, left, right, recall, section=None):
    section = section or (BOOT if n < 72 else STR if n < 88
                          else BLO if n < 96 else MC)
    SLIDES[n] = dict(title=title, section=section, left=left,
                     right=right, recall=recall)

def code(n, name, body):
    key = f"{n:03}_{name}.R"
    CODES[key] = body.strip() + "\n"
    return key

def fmt(x, digits=3):
    return f"{x:.{digits}f}".replace(".", "{,}")

def rows(name):
    return list(csv.DictReader((FIG / f"{name}.csv").open()))

def table(headers, data, widths, h=.62):
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    width = sum(widths)
    for j, row in enumerate([headers] + data):
        yy = -j*h
        fill = "Navy" if j == 0 else "white" if j % 2 else "GeoTint"
        text = "white" if j == 0 else "Ink"
        out.append(rf"\fill[{fill}](0,{yy}) rectangle({width},{yy+h});")
        a = 0
        for cell, w in zip(row, widths):
            out.append(rf"\node[pLabel,text={text}] at({a+w/2},{yy+h/2}){{{cell}}};")
            a += w
    return "\n".join(out + [r"\end{tikzpicture}"])

def histplot(names, colors, labels, xmin, xmax, xticks, xlab, marks=(), h=2.55):
    allrows = [rows(n) for n in names]
    ymax = max(float(r["densita"]) for data in allrows for r in data)*1.12
    sx = lambda x: .85 + 8*(x-xmin)/(xmax-xmin)
    sy = lambda y: h*y/ymax
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for y in [0, ymax/2, ymax]:
        out.append(rf"\draw[Rule](.85,{sy(y)})--(8.85,{sy(y)});")
        out.append(rf"\node[pNote,anchor=east] at(.7,{sy(y)}){{$ {fmt(y,1)} $}};")
    for data, color in zip(allrows, colors):
        for r in data:
            a,b,d = map(float,(r["sx"],r["dx"],r["densita"]))
            if b >= xmin and a <= xmax:
                a,b = max(a,xmin),min(b,xmax)
                out.append(rf"\filldraw[fill={color},fill opacity=.18,draw={color},line width=.45pt]({sx(a):.5f},0) rectangle({sx(b):.5f},{sy(d):.5f});")
    out.extend([rf"\draw[pAxis](.85,0)--(9.05,0);",
                rf"\draw[pAxis](.85,0)--(.85,{h+.15});"])
    for x in xticks:
        out.append(rf"\node[pNote,below] at({sx(x):.5f},-.08){{$ {fmt(x,1)} $}};")
    for value, lab, color in marks:
        out.append(rf"\draw[{color},dashed,line width=.9pt]({sx(value):.5f},0)--({sx(value):.5f},{h});")
    for k,(lab,col) in enumerate(zip(labels,colors)):
        xx=.85 + 4.1*k
        out.append(rf"\draw[{col},line width=2pt]({xx},{h+.45})--++(.45,0);")
        out.append(rf"\node[pNote,anchor=west,text={col}] at({xx+.52},{h+.45}){{{lab}}};")
    out.append(rf"\node[pNote] at(4.85,-.65){{{xlab}}};")
    out.append(rf"\node[pNote,rotate=90] at(-.15,{h/2}){{densità}};")
    return "\n".join(out+[r"\end{tikzpicture}"])

def lineplot(points, xmin, xmax, ymin, ymax, xticks, yticks, xlab, ylab,
             color="GeoA", height=2.65, reference=None):
    sx=lambda x:.85+8*(x-xmin)/(xmax-xmin)
    sy=lambda y:height*(y-ymin)/(ymax-ymin)
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    ydigits = 2 if len(yticks)>1 and min(abs(b-a) for a,b in zip(yticks,yticks[1:])) < .099 else 1
    for y in yticks:
        out.extend([rf"\draw[Rule](.85,{sy(y):.5f})--(8.85,{sy(y):.5f});",
                    rf"\node[pNote,anchor=east] at(.7,{sy(y):.5f}){{$ {fmt(y,ydigits)} $}};"])
    out.extend([rf"\draw[pAxis](.85,0)--(9.05,0);",
                rf"\draw[pAxis](.85,0)--(.85,{height+.15});"])
    if reference is not None:
        out.append(rf"\draw[GeoB,dashed](.85,{sy(reference):.5f})--(8.85,{sy(reference):.5f});")
    out.append(rf"\draw[{color},line width=.85pt] plot coordinates{{"+
               " ".join(f"({sx(x):.5f},{sy(y):.5f})" for x,y in points)+"};")
    for x in xticks:
        out.append(rf"\node[pNote,below] at({sx(x):.5f},-.08){{$ {fmt(x,0)} $}};")
    out.append(rf"\node[pNote] at(4.85,-.65){{{xlab}}};")
    out.append(rf"\node[pNote,rotate=90] at(-.18,{height/2}){{{ylab}}};")
    return "\n".join(out+[r"\end{tikzpicture}"])

code(60,"distribuzione_empirica",'''
# Quattro osservazioni adimensionali
x60 <- c(4, 5, 7, 8)
F60 <- ecdf(x60)  # Frazione <= t
F60(c(4, 6, 8))  # .25, .50, 1
plot(F60, main = "CDF empirica",
     xlab = "t", ylab = "F_n(t)")
''')
add(60,"Il campione diventa una distribuzione",r'''
\PLabel{Dal modello ignoto ai valori osservati}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (f) at(2.1,3.3){Popolazione $F$\\non osservata per intero};
\node[pFlow,text width=3.7cm] (x) at(7.1,3.3){Campione osservato\\$\mathbf x=(x_1,\ldots,x_n)$};
\node[pFlow,text width=3.7cm,fill=GeoTint] (fn) at(7.1,1.4){Distribuzione empirica\\massa $1/n$ per osservazione};
\node[pFlow,text width=3.7cm,fill=GeoTint] (bs) at(2.1,1.4){Repliche bootstrap\\estrazioni da $\widehat F_n$};
\draw[pEdge](f)--node[pNote,above=.6cm]{campionamento}(x);
\draw[pEdge](x)--node[pNote,right]{costruzione}(fn);
\draw[pEdge](fn)--node[pNote,below=.6cm]{ricampionamento}(bs);
\end{tikzpicture}
\[
\widehat F_n(t)=\frac1n\sum_{i=1}^{n}\mathbf1_{\{x_i\le t\}}.
\]
\PSmall{I dati restano fissati. La casualità delle repliche riguarda la selezione delle osservazioni disponibili.}
''',r'''
\PCode{R · la distribuzione empirica}{060_distribuzione_empirica.R}
\PBody{La funzione \texttt{ecdf()} restituisce la frazione di osservazioni minori o uguali a ciascun valore richiesto.}
\PInfo{Unità iid: indipendenti, con distribuzione comune. La statistica deve ammettere un'approssimazione bootstrap adeguata.}
''',"La distribuzione bootstrap è condizionata al campione osservato e allo schema scelto per ricampionarlo.")

code(61,"masse",'''
x61 <- c(4, 5, 7, 8)
p61 <- rep(1/4, 4)
sum(p61)       # Probabilita totale
sum(x61*p61)   # Media empirica: 6
# Ogni posizione ha probabilita 1/4
data.frame(valore = x61, p = p61)
''')
add(61,"Quattro valori con lo stesso peso",r'''
\PLabel{Campione illustrativo $x=(4,5,7,8)$}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.65,.25)--(9,.25);
\draw[pAxis](.65,.25)--(.65,3);
\foreach \xx/\v in {1.3/4,3/5,6.4/7,8.1/8}{
\draw[GeoA,line width=5pt](\xx,.25)--(\xx,2.45);
\node[pLabel,below] at(\xx,.15){$\v$};
\node[pNote,above] at(\xx,2.5){$1/4$};}
\draw[GeoB,dashed](4.7,.25)--(4.7,2.95);
\node[pNote,text=GeoB] at(4.7,3.35){$\bar x=6$};
\node[pNote,rotate=90] at(-.05,1.55){probabilità empirica};
\end{tikzpicture}
\[
E_*(X^*)=\sum_{i=1}^{4}\tfrac14x_i=6.
\]
\PSmall{L'asterisco indica una nuova estrazione. Il pedice $*$ indica probabilità e momenti condizionati a questi quattro valori.}
''',r'''
\PCode{R · valori e probabilità}{061_masse.R}
\PBody{Osservazioni con lo stesso valore sommano le loro masse. La selezione continua a riguardare gli indici.}
\PInfo{Quattro valori permettono di seguire i calcoli a mano, ma rappresentano poche caratteristiche della popolazione.}
''',"L'empirica assegna uguale probabilità a ogni osservazione; valori ripetuti raccolgono la probabilità di più osservazioni.")

code(62,"indici",'''
x62 <- c(4, 5, 7, 8)
# Replica scelta per il diagramma
j62 <- c(3, 3, 1, 4)
x62[j62]        # 7, 7, 4, 8
mean(x62[j62])  # 6.5
# Una replica estratta casualmente
set.seed(17)
sample.int(4, 4, replace = TRUE)
''')
add(62,"Una replica osservata negli indici",r'''
\PLabel{Quattro estrazioni con reinserimento}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pNote,anchor=west] at(.15,4.1){campione};
\foreach \xx/\i/\v in {1/1/4,3.2/2/5,5.4/3/7,7.6/4/8}{
\node[pFlow,minimum width=1.4cm] (x\i) at(\xx,3.1){$x_{\i}=\v$};}
\foreach \xx/\k/\j/\v in {1/1/3/7,3.2/2/3/7,5.4/3/1/4,7.6/4/4/8}{
\node[pFlow,minimum width=1.4cm,fill=GeoTint] (r\k) at(\xx,.8){$x_{\j}=\v$};
\node[pNote] at(\xx,-.1){$J_{\k}=\j$};}
\draw[pEdge](x3.south)--(r1.north);
\draw[pEdge](x3.south)--(r2.north);
\draw[pEdge](x1.south)--(r3.north);
\draw[pEdge](x4.south)--(r4.north);
\end{tikzpicture}
\[
\bar x^*=(7+7+4+8)/4=6{,}5.
\]
\PSmall{L'indice 3 compare due volte. L'indice 2 non compare. La replica conserva quattro posizioni.}
''',r'''
\PCode{R · indici prima dei valori}{062_indici.R}
\PSmall{\texttt{sample.int(4,4,replace=TRUE)} estrae quattro indici fra 1 e 4. \texttt{x[j]} recupera i valori corrispondenti.}
\PInfo{La sequenza $(3,3,1,4)$ è illustrativa. Il seme 17 genera un'altra replica.}
''',"Il reinserimento consente che alcune osservazioni compaiano più volte e altre restino escluse dalla replica.")

code(63,"molteplicita",'''
x63 <- c(4, 5, 7, 8)
j63 <- c(3, 3, 1, 4)
N63 <- tabulate(j63, nbins = 4)
N63              # 1, 0, 2, 1
sum(N63)         # 4 estrazioni
sum(N63*x63)/4   # Media: 6.5
mean(x63[j63])   # Stesso valore
''')
add(63,"Le molteplicità diventano pesi",r'''
\PLabel{Due descrizioni della stessa replica}
'''+table(["Osservazione",r"$x_i$",r"$N_i^*$",r"$N_i^*x_i$"],
          [["1","4","1","4"],["2","5","0","0"],["3","7","2","14"],["4","8","1","8"]],
          [2.8,1.9,2.1,2.5])+r'''
\[
\bar X^*=\frac1n\sum_iN_i^*x_i,\qquad \sum_iN_i^*=n.
\]
\PSmall{Per estrazioni indipendenti con reinserimento, il vettore dei conteggi segue una multinomiale con $n$ prove e probabilità $1/n$.}
''',r'''
\PCode{R · conteggiare gli indici}{063_molteplicita.R}
\PBody{\texttt{tabulate()} conta quante volte compare ciascun indice. Il valore 5 riceve peso zero e il valore 7 riceve peso due.}
\PInfo{L'ordine della replica cambia alcune statistiche, ma lascia invariata la media quando le molteplicità restano uguali.}
''',"Per la media, estrarre valori con reinserimento equivale ad assegnare loro pesi interi casuali che sommano a n.")

exact = rows("esatto")
exact_pic = [r"\begin{tikzpicture}[x=1cm,y=1cm]",
             r"\draw[pAxis](.75,0)--(9,0);\draw[pAxis](.75,0)--(.75,3);"]
for r in exact:
    x,p=float(r["media"]),float(r["probabilita"])
    xx=.75+(x-4)*2
    exact_pic.append(rf"\draw[GeoA,line width=2pt]({xx:.5f},0)--({xx:.5f},{p*23:.5f});")
for x in range(4,9):
    exact_pic.append(rf"\node[pNote,below] at({.75+(x-4)*2},-.08){{$ {x} $}};")
for p in [0,.05,.1]:
    exact_pic.append(rf"\node[pNote,anchor=east] at(.6,{p*23}){{$ {fmt(p,2)} $}};")
exact_pic.extend([r"\node[pNote,rotate=90] at(-.2,1.5){probabilità};",
                  r"\node[pNote] at(4.75,-.65){media di una replica $\bar X^*$};",
                  r"\end{tikzpicture}"])
code(64,"enumerazione",'''
x64 <- c(4, 5, 7, 8)
# Tutte le 4^4 sequenze ordinate
j64 <- as.matrix(expand.grid(
  rep(list(1:4), 4)))
m64 <- apply(j64, 1,
  function(j) mean(x64[j]))
length(m64)               # 256
mean(m64)                 # 6
mean((m64-mean(m64))^2)    # .625
''')
add(64,"Tutte le 256 repliche possibili",r'''
\PLabel{Enumerazione esatta, senza errore Monte Carlo}
'''+ "\n".join(exact_pic)+r'''
\[
4^4=256,\qquad E_*(\bar X^*)=6,\qquad
\operatorname{Var}_*(\bar X^*)=0{,}625.
\]
\PSmall{Le sequenze ordinate sono equiprobabili. Le medie possibili hanno probabilità diverse, perché più sequenze producono la stessa media.}
''',r'''
\PCode{R · enumerare gli indici}{064_enumerazione.R}
\PSmall{\texttt{expand.grid()} elenca tutte le combinazioni. \texttt{apply(...,1,...)} calcola una media per riga.}
\PInfo{La varianza esatta usa il divisore 256: tutte le sequenze equiprobabili partecipano al calcolo.}
''',"Enumerare tutte le sequenze separa la distribuzione bootstrap dalla sua approssimazione ottenuta con B repliche casuali.")

code(65,"varianza_condizionata",'''
x65 <- c(4, 5, 7, 8)
n65 <- length(x65)
s265 <- var(x65)        # 10/3
v65 <- (n65-1)/n65^2*s265
v65                    # .625
sqrt(v65)              # SE esatto
# Varianza di una sola estrazione
mean((x65-mean(x65))^2)  # 2.5
''')
add(65,"La varianza della media bootstrap",r'''
\PLabel{I dati sono fissati e le estrazioni sono indipendenti}
\[
\begin{aligned}
\operatorname{Var}_*(X_j^*)
 &=\frac1n\sum_i(x_i-\bar x)^2\\
 &=\frac{n-1}{n}s^2,\\[1mm]
\operatorname{Var}_*(\bar X^*)
 &=\frac1n\operatorname{Var}_*(X_j^*)
 =\frac{n-1}{n^2}s^2.
\end{aligned}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (a) at(2,1){Una estrazione\\varianza $2{,}5$};
\node[pFlow,text width=3.5cm,fill=GeoTint] (b) at(7,1){Media di quattro\\varianza $0{,}625$};
\draw[pEdge](a)--node[pNote,above]{$\div4$}(b);
\end{tikzpicture}
\PSmall{$s^2$ usa il divisore $n-1$. La varianza empirica usa $n$.}
''',r'''
\PCode{R · controllo analitico}{065_varianza_condizionata.R}
\PBody{La formula fornisce un controllo del codice: la dispersione simulata deve avvicinarsi a $\sqrt{0{,}625}\simeq0{,}791$.}
\PInfo{Il fattore $(n-1)/n$ distingue la varianza bootstrap della media dalla stima $s^2/n$.}
''',"La varianza bootstrap condizionata della media è esatta per l'empirica e vale (n−1)s²/n².")

code(66,"molte_repliche",'''
x66 <- c(4, 5, 7, 8)
n66 <- length(x66)
B66 <- 2000
set.seed(17)
b66 <- replicate(B66, {
  j <- sample.int(n66, n66,
                  replace = TRUE)
  mean(x66[j])
})
length(b66)  # Una media per replica
''')
add(66,"Ogni replica produce una statistica",r'''
\PLabel{$n$ estrazioni per riga, $B$ righe simulate}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\r/\vals/\m in {3.6/1/{7,7,4,8}/{6{,}5},2.2/2/{5,4,5,8}/{5{,}5},.8/3/{4,8,8,8}/{7}}{
\node[pNote,anchor=east] at(.7,\yy){$\r$};
\foreach \v[count=\j] in \vals {
\node[pFlow,minimum width=1cm,minimum height=.7cm] at({.4+1.3*\j},\yy){$\v$};}
\node[pFlow,text width=2.2cm,minimum height=.8cm,fill=GeoTint] (m\r) at(8,\yy){$\bar x^{*(\r)}=\m$};
\draw[pEdge](6.1,\yy)--(m\r.west);}
\node[pNote] at(3.6,-.1){quattro posizioni per replica};
\end{tikzpicture}
\PSmall{Tre repliche illustrative. Il comando R genera $B=2000$ medie dallo stesso vettore di quattro valori.}
''',r'''
\PCode{R · ripetere il ricampionamento}{066_molte_repliche.R}
\PSmall{\texttt{replicate(B,\{...\})} esegue il blocco $B$ volte e raccoglie ogni risultato. Le quattro osservazioni iniziali restano invariate.}
''',"n definisce la dimensione di ogni campione bootstrap; B definisce quante statistiche simulate usiamo per descriverne la distribuzione.")

code(67,"errore_standard_boot",'''
# b66 contiene 2000 medie bootstrap
sd(b66)      # SE bootstrap: circa .783
# Errore MC della media delle repliche
sd(b66)/sqrt(length(b66))  # .0175
# Dispersione delle quattro misure
sd(x66)      # Circa 1.826
''')
add(67,"Tre deviazioni standard con significati diversi",r'''
\PLabel{Stesso esempio, quantità differenti}
'''+table(["Quantità","Che cosa varia","Valore"],
          [["SD dei dati","singoli valori","1,826"],
           ["SE bootstrap","medie ricampionate","0,783"],
           ["SE Monte Carlo","media di 2000 repliche","0,0175"]],
          [3.1,4.0,2.2],h=.85)+r'''
\[
\widehat{\mathrm{SE}}_*=
\sqrt{\frac1{B-1}\sum_{b=1}^B
(\widehat\theta^{*(b)}-\overline\theta^*)^2}.
\]
\PSmall{$\overline\theta^*$ è la media delle $B$ statistiche bootstrap. I numeri derivano dal seme 17 e da $B=2000$.}
''',r'''
\PCode{R · identificare la dispersione}{067_errore_standard_boot.R}
\PBody{\texttt{sd(b66)} stima l'incertezza della statistica tramite il bootstrap. Dividere per $\sqrt B$ descrive la precisione numerica della media delle repliche.}
\PInfo{L'errore standard bootstrap conserva la stessa unità della statistica.}
''',"Prima di interpretare una deviazione standard, occorre identificare gli oggetti su cui viene calcolata.")

code(68,"bias_bootstrap",'''
# Media delle repliche meno stima
mean(b66) - mean(x66)  # .00225
# Il valore condizionato esatto e 0
sum(x66/length(x66)) - mean(x66)
# Una selezione distorta del campione
# richiede informazioni sul disegno.
''')
add(68,"Il bias bootstrap riguarda l'empirica",r'''
\PLabel{Per la media il bias condizionato è nullo}
\[
\operatorname{bias}_*=
E_*(\widehat\theta^*)-\widehat\theta,
\qquad E_*(\bar X^*)-\bar x=0.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,1)--(9.1,1);
\draw[GeoA,line width=1.4pt](4.6,.55)--(4.6,1.55);
\node[pLabel,text=GeoA] at(4.6,2.15){$\bar x=E_*(\bar X^*)=6$};
\node[pFlow,text width=7.6cm,fill=GeoTint] at(4.6,-.35)
{Media di 2000 repliche: $6{,}00225$\\scarto Monte Carlo: $0{,}00225$};
\end{tikzpicture}
\PSmall{Il confronto avviene entro la distribuzione empirica. La relazione del campione con la popolazione dipende dalla selezione delle unità.}
''',r'''
\PCode{R · bias condizionato stimato}{068_bias_bootstrap.R}
\PBody{Un campione raccolto solo nei siti accessibili può avere una media distorta per il territorio. Ricampionarlo mantiene quelle stesse osservazioni.}
\PInfo{Per altre statistiche il bias bootstrap può essere diverso da zero. La sua utilità dipende dall'accuratezza dell'approssimazione.}
''',"Un bias bootstrap nullo della media non fornisce informazioni sufficienti per escludere una distorsione di selezione.")

code(69,"quantile_tipo7",'''
# Esempio di 20 statistiche ordinate
v69 <- seq(1, 2.9, by = .1)
p69 <- .975
h69 <- 1 + (length(v69)-1)*p69
j69 <- floor(h69)
g69 <- h69-j69
(1-g69)*v69[j69] + g69*v69[j69+1]
quantile(v69, p69, type = 7)
''')
add(69,"I percentili richiedono un ordinamento",r'''
\PLabel{Intervallo percentile al livello nominale $1-\alpha$}
\[
C^*_{1-\alpha}=
[q^*_{\alpha/2},q^*_{1-\alpha/2}].
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.4,1.6)--(9,1.6);
\fill[GeoA](1.6,1.6) circle(3pt);
\fill[GeoA](7.5,1.6) circle(3pt);
\fill[GeoB](4.6975,1.6) circle(3pt);
\node[pLabel,above] at(1.6,1.8){$v_{(19)}=2{,}8$};
\node[pLabel,above] at(7.5,1.8){$v_{(20)}=2{,}9$};
\node[pNote,below,text=GeoB] at(4.6975,1.4){$q_{0{,}975}=2{,}8525$};
\node[pNote] at(4.7,.25){$h=1+19(0{,}975)=19{,}525$};
\end{tikzpicture}
\[
q_p=(1-\gamma)v_{(j)}+\gamma v_{(j+1)},
\quad j=\lfloor h\rfloor,\quad\gamma=h-j.
\]
\PSmall{Esempio costruito per \texttt{type=7}, con $0<p<1$. Gli estremi $p=0,1$ restituiscono minimo e massimo.}
''',r'''
\PCode{R · interpolazione del quantile}{069_quantile_tipo7.R}
\PSmall{Le parentesi in $v_{(j)}$ indicano l'ordine crescente. Il quantile può cadere fra due statistiche osservate.}
\PInfo{Un intervallo percentile ha copertura approssimata. Piccoli campioni, bias e forme irregolari richiedono una valutazione specifica.}
''',"Il livello nominale e la convenzione dei quantili devono accompagnare i limiti dell'intervallo percentile.")

code(70,"bootstrap_mediana",'''
set.seed(17)
x70 <- rlnorm(30, 0, .6)
set.seed(17)
m70 <- replicate(2000,
  median(sample(x70, replace = TRUE)))
median(x70)
quantile(m70, c(.025, .975),
         type = 7)
''')
add(70,"La statistica può essere una mediana",r'''
\PLabel{Stesso campione del laboratorio, statistica diversa}
'''+histplot(["mediana"],["GeoC"],["2000 mediane bootstrap"],
             .8,1.9,[.8,1,1.2,1.4,1.6,1.8],r"mediana ricampionata (adimensionale)")+r'''
\[
\widehat m^*=\operatorname{mediana}(x_{J_1},\ldots,x_{J_n}).
\]
\PSmall{Mediana osservata $1{,}207$. Limiti percentili $[1{,}020;\,1{,}505]$ con il seme e il numero di repliche indicati.}
''',r'''
\PCode{R · cambiare la statistica}{070_bootstrap_mediana.R}
\PSmall{Il campionamento degli indici resta identico. Il comando interno diventa \texttt{median()}.}
\PInfo{La discrezione è visibile nel grafico. Le giustificazioni usuali richiedono regolarità della popolazione vicino alla mediana.}
''',"La scelta della statistica modifica la distribuzione bootstrap e le condizioni necessarie per interpretarla.")

code(71,"laboratorio_bootstrap",'''
r71 <- lab_bootstrap(
  n = 30, B = 200, seed = 17)
r71$indicatori
# La distribuzione e condizionata
# ai 30 valori del campione.
hist(r71$dati$media,
     xlab = "Media bootstrap",
     main = "Ricampionamento")
''')
add(71,"Laboratorio: ricampionare i 30 valori",r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-bootstrap}{Esperimento · bootstrap}
'''+histplot(["browser_bootstrap"],["GeoA"],["200 medie bootstrap"],
             .9,1.85,[1,1.2,1.4,1.6,1.8],
             r"media ricampionata (adimensionale)",
             marks=[(MET["browser_boot_low"],"", "GeoB"),(MET["browser_boot_high"],"","GeoB")])+r'''
\PSmall{Il generatore usa \texttt{rlnorm(30,0,.6)}. Media osservata $1{,}364$, SE bootstrap $0{,}124$, percentile $[1{,}129;\,1{,}604]$.}
\PBody{Aumentare $B$ da 200 a 1000, lasciando $n$ e il seme invariati. Confrontare SE e limiti.}
''',r'''
\PCode{R · riprodurre il caso iniziale}{071_laboratorio_bootstrap.R}
\PInfo{Il campione resta identico cambiando solo $B$. Il controllo $n$, da 12 a 300, modifica le osservazioni disponibili.}
''',"Ogni risultato bootstrap va riferito al campione fissato, al numero di repliche, al seme e alla statistica calcolata.")

code(72,"struttura_dati",'''
# Dati sintetici letti da setup.R
table(fossili$morfotipo)
table(provini$stazione)
# Una riga del fossile contiene
# due misure della stessa unita.
head(fossili[c("id",
  "diametro_tot_um", "diametro_int_um")])
''')
add(72,"L'unità di ricampionamento segue il disegno",r'''
\PLabel{Quali informazioni devono restare insieme?}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\tit/\txt/\col [count=\idx] in {
4.5/{Fossile}/{Diametro totale e interno}/{GeoA},
2.8/{Stazione}/{Tutti i provini del sito}/{GeoB},
1.1/{Tratto temporale}/{Osservazioni consecutive}/{GeoC}}{
\node[pFlow,text width=2.6cm,draw=\col] (a\idx) at(1.65,\yy){\tit};
\node[pFlow,text width=5.2cm,fill=\col!8,draw=\col] (b\idx) at(6.5,\yy){\txt};
\draw[pEdge,draw=\col](a\idx)--(b\idx);}
\end{tikzpicture}
\PSmall{Le relazioni fra misure fanno parte del dato. Lo schema deve conservare quelle rilevanti per la statistica e per il disegno.}
''',r'''
\PCode{R · leggere le unità del progetto}{072_struttura_dati.R}
\PInfo{Fossili: 80 Rounded e 80 Spiky. Provini: 24 righe da sei stazioni, quattro per sito. Tutti i dati sono sintetici.}
\PBody{L'estimando guida la scelta dell'unità di ricampionamento.}
''',"L'unità osservata, l'unità indipendente e l'unità ricampionata devono essere collegate al disegno dell'analisi.")

code(73,"quote_pooled",'''
# Indici del campione riunito
g73 <- fossili$morfotipo
set.seed(17)
j73 <- sample.int(length(g73),
  length(g73), replace = TRUE)
table(g73[j73])
# N_R varia fra repliche.
length(j73)  # Totale sempre 160
''')
add(73,"Il campione riunito ha quote casuali",r'''
\PLabel{Ricampionamento pooled dei 160 fossili}
\begin{tikzpicture}[x=1cm,y=.9cm]
\node[pFlow,text width=7.8cm] (src) at(4.65,4.5){Campione osservato: 80 Rounded e 80 Spiky};
\foreach \yy/\nr/\ns in {2.8/76/84,1.5/85/75,.2/80/80}{
\fill[GeoA!25](.6,\yy-.35) rectangle({.6+8.1*\nr/160},\yy+.35);
\fill[GeoB!25]({.6+8.1*\nr/160},\yy-.35) rectangle(8.7,\yy+.35);
\node[pNote,text=GeoA] at(2.7,\yy){$\nr$ Rounded};
\node[pNote,text=GeoB] at(6.8,\yy){$\ns$ Spiky};}
\draw[pEdge](src.south)--(4.65,3.35);
\end{tikzpicture}
\[
N_R^*\sim\operatorname{Bin}(160,1/2),\qquad E_*N_R^*=80.
\]
\PSmall{Tre composizioni illustrative. Il totale è fisso, la quota dei due gruppi cambia.}
''',r'''
\PCode{R · contare le quote estratte}{073_quote_pooled.R}
\PBody{Il pooled tratta i fossili come un campione da una popolazione mescolata. La composizione varia fra le repliche.}
\PInfo{Ogni fossile conserva tutte le proprie misure.}
''',"Nel bootstrap pooled le quote dei gruppi cambiano, anche quando il campione osservato contiene due gruppi della stessa dimensione.")

code(74,"stratificato",'''
g74 <- split(fossili$diametro_tot_um,
             fossili$morfotipo)
rb74 <- function(v)
  mean(sample(v, replace = TRUE))
set.seed(17)
b74 <- replicate(2000,
  .5*rb74(g74$Rounded) +
  .5*rb74(g74$Spiky))
sd(b74)
''')
add(74,"Il bootstrap stratificato conserva le quote",r'''
\PLabel{Due campioni indipendenti, pesi dichiarati}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm,draw=GeoA] (r) at(2.1,4){80 Rounded};
\node[pFlow,text width=3.7cm,draw=GeoB] (s) at(7.1,4){80 Spiky};
\node[pFlow,text width=3.7cm,fill=GeoA!8] (rb) at(2.1,2){80 estrazioni\\entro Rounded};
\node[pFlow,text width=3.7cm,fill=GeoB!8] (sb) at(7.1,2){80 estrazioni\\entro Spiky};
\draw[pEdge,draw=GeoA](r)--(rb);
\draw[pEdge,draw=GeoB](s)--(sb);
\node[pFlow,text width=6.2cm] (m) at(4.6,.15){$\widehat\mu^*=\tfrac12\bar X_R^*+\tfrac12\bar X_S^*$};
\draw[pEdge](rb.south)--(m.north west);
\draw[pEdge](sb.south)--(m.north east);
\end{tikzpicture}
\PSmall{I pesi $1/2$ appartengono alla definizione dell'obiettivo: una media che assegna la stessa importanza ai due morfotipi.}
''',r'''
\PCode{R · estrarre entro ogni gruppo}{074_stratificato.R}
\PSmall{\texttt{rb74()} ricampiona un vettore e ne restituisce la media, mantenendo la numerosità.}
\PInfo{I pesi della popolazione vanno dichiarati. Le quote osservate non li determinano.}
''',"Il bootstrap stratificato mantiene le numerosità dei gruppi e ricalcola la combinazione definita dai pesi dell'estimando.")

code(75,"pooled_stratificato",'''
z75 <- fossili$diametro_tot_um
set.seed(17)
bp75 <- replicate(2000,
  mean(sample(z75, replace = TRUE)))
# b74 usa quote fissate a 80 e 80
c(pooled = sd(bp75),
  stratificato = sd(b74))
mean(z75)  # Media osservata comune
''')
add(75,"Stessa media osservata, variabilità diversa",r'''
\PLabel{Confronto sui 160 fossili sintetici}
'''+histplot(["fossili_pooled","fossili_strat"],["GeoA","GeoB"],
             ["pooled","stratificato"],
             6.0,6.72,[6,6.2,6.4,6.6],r"diametro medio ($\mu$m)")+r'''
\PSmall{Media osservata comune $6{,}355\,\mu$m. Con $B=2000$ e seme 17, SE pooled $0{,}081\,\mu$m e SE stratificato $0{,}076\,\mu$m.}
\PBody{Il metodo pooled aggiunge la variabilità dovuta alle quote casuali. Le due procedure rappresentano ripetizioni diverse.}
''',r'''
\PCode{R · confrontare i due schemi}{075_pooled_stratificato.R}
\[
\operatorname{Var}_*(\widehat\mu^*_{\mathrm{str}})
=\frac14\frac{79}{80^2}(s_R^2+s_S^2).
\]
\PSmall{La formula assume ricampionamenti indipendenti entro i gruppi e pesi $1/2$ fissati. Il risultato simulato oscilla attorno al valore condizionato esatto.}
''',"L'uguaglianza delle stime osservate non rende equivalenti i disegni di ricampionamento o le loro distribuzioni.")

code(76,"contrasto_gruppi",'''
# Contrasto Spiky meno Rounded
set.seed(17)
delta76 <- replicate(2000,
  rb74(g74$Spiky) - rb74(g74$Rounded))
mean(g74$Spiky) - mean(g74$Rounded)
quantile(delta76, c(.025, .975),
         type = 7)
''')
add(76,"Il contrasto conserva un segno preciso",r'''
\PLabel{Diametro totale: Spiky meno Rounded}
'''+histplot(["contrasto"],["GeoC"],["2000 differenze bootstrap"],
             0,1.15,[0,.3,.6,.9],r"$\bar X_S^*-\bar X_R^*$ ($\mu$m)",
             marks=[(MET["contrasto_low"],"","GeoB"),(MET["contrasto_high"],"","GeoB")])+r'''
\[
\Delta=\mu_S-\mu_R,\qquad
\widehat\Delta^*=\bar X_S^*-\bar X_R^*.
\]
\PSmall{Differenza osservata $0{,}582\,\mu$m. Percentile $[0{,}273;\,0{,}888]\,\mu$m per questa esecuzione.}
''',r'''
\PCode{R · sottrarre le due medie}{076_contrasto_gruppi.R}
\PBody{Ogni replica seleziona individui entro il proprio gruppo. Le etichette Rounded e Spiky restano associate ai dati.}
\PInfo{Il modulo successivo costruirà distribuzioni di riferimento sotto ipotesi nulle. Qui stimiamo l'incertezza del contrasto osservato.}
''',"L'orientamento del contrasto deve rimanere uguale nella formula, nel codice, nel grafico e nella conclusione.")

code(77,"coppie",'''
r77 <- subset(fossili,
               morfotipo == "Rounded")
d77 <- with(r77,
  diametro_tot_um - diametro_int_um)
set.seed(17)
bd77 <- replicate(2000,
  mean(sample(d77, replace = TRUE)))
c(differenza = mean(d77),
  SE = sd(bd77))
''')
add(77,"Le due misure del fossile restano appaiate",r'''
\PLabel{Totale e interno appartengono allo stesso individuo}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\i/\a/\b in {4/1/7.2/6.4,2.5/2/5.8/5.0,1/3/6.6/5.6}{
\node[pFlow,minimum width=1.25cm] (id\i) at(.9,\yy){ID \i};
\node[pFlow,text width=3cm,fill=GeoTint] (p\i) at(3.8,\yy){$(a_{\i},b_{\i})$};
\node[pFlow,text width=2.8cm] (d\i) at(7.8,\yy){$d_{\i}=a_{\i}-b_{\i}$};
\draw[pEdge](id\i)--(p\i);\draw[pEdge](p\i)--(d\i);}
\end{tikzpicture}
\[
\bar D^*=\frac1n\sum_j(a_{J_j}-b_{J_j}).
\]
\PSmall{Ricampionare le differenze equivale a estrarre gli stessi indici nelle due colonne.}
''',r'''
\PCode{R · ricampionare le differenze}{077_coppie.R}
\PBody{Per Rounded: differenza media $0{,}857\,\mu$m, SE bootstrap $0{,}028\,\mu$m.}
\PInfo{Ricampionare separatamente le colonne altera la covarianza fra le misure.}
''',"Le coppie complete conservano la relazione fra le due misure; gli stessi indici devono selezionare entrambe le colonne.")

code(78,"medie_stazione",'''
# Densita in g/cm^3, 4 provini/sito
st78 <- aggregate(densita ~ stazione,
                  provini, mean)
st78
mean(provini$densita)
mean(st78$densita)  # Stesso valore
table(provini$stazione)
''')
add(78,"I 24 provini appartengono a sei stazioni",r'''
\PLabel{Dati sintetici del corso, due affioramenti}
\begin{tikzpicture}[x=1cm,y=.88cm]
\foreach \xx/\aff/\col in {2.3/A/GeoA,7.1/B/GeoB}{
\node[pLabel,text=\col] at(\xx,4.8){Affioramento \aff};
\foreach \j in {1,2,3}{
\node[pGroup,minimum width=1.1cm,minimum height=2.8cm] at({\xx+1.35*(\j-2)},2.8){};
\node[pNote,text=\col] at({\xx+1.35*(\j-2)},4){\aff\j};
\foreach \k in {1,2,3,4}
\fill[\col]({\xx+1.35*(\j-2)},{1.2+.6*\k}) circle(3.2pt);}
\node[pNote] at(\xx,.6){3 stazioni, 12 provini};}
\end{tikzpicture}
\[
\rho_{gi}=\frac{m_{gi}}{V_{gi}},\qquad
\bar\rho_g=\frac14\sum_{i=1}^{4}\rho_{gi}.
\]
\PSmall{La densità è in $\mathrm{g\,cm^{-3}}$. Il pedice $g$ identifica la stazione e $i$ il provino.}
''',r'''
\PCode{R · aggregare entro stazione}{078_medie_stazione.R}
\PBody{Con quattro provini per sito, la media delle 24 densità coincide con la media delle sei medie locali: $2{,}599\,\mathrm{g\,cm^{-3}}$.}
\PInfo{L'identità delle medie dipende dal bilanciamento. L'incertezza dipende anche dalla relazione fra i provini di ogni sito.}
''',"Quattro provini nello stesso sito condividono un contesto; la loro indipendenza richiede una giustificazione.")

code(79,"stazioni_intere",'''
v79 <- split(provini$densita,
              provini$stazione)
# Sei indici illustrativi
j79 <- c(2, 2, 6, 4, 1, 3)
mean(unlist(v79[j79]))
mean(sapply(v79[j79], mean))
# Identici: 4 provini per stazione
''')
add(79,"Una stazione viene selezionata per intero",r'''
\PLabel{Schema ridotto a tre stazioni illustrative}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\j/\col in {1.4/1/GeoA,4.6/2/GeoB,7.8/3/GeoC}{
\node[pGroup,minimum width=2.3cm,minimum height=1.5cm] (a\j) at(\xx,3.8){};
\node[pNote,text=\col] at(\xx,4.3){stazione \j};
\foreach \dx in {-.6,-.2,.2,.6}\fill[\col]({\xx+\dx},3.5) circle(3pt);}
\foreach \xx/\j/\k/\col in {1.4/1/2/GeoB,4.6/2/2/GeoB,7.8/3/1/GeoA}{
\node[pGroup,minimum width=2.3cm,minimum height=1.5cm,fill=GeoTint] (b\j) at(\xx,1.2){};
\node[pNote,text=\col] at(\xx,1.7){stazione \k};
\foreach \dx in {-.6,-.2,.2,.6}\fill[\col]({\xx+\dx},.9) circle(3pt);}
\draw[pEdge](a2.south)--(b1.north);
\draw[pEdge](a2.south)--(b2.north);
\draw[pEdge](a1.south)--(b3.north);
\end{tikzpicture}
\[
\widehat\theta_G^*=\frac1G\sum_{j=1}^{G}\bar\rho_{J_j},
\quad J_j\overset{\mathrm{iid}}{\sim}\operatorname{Unif}\{1,\ldots,G\}.
\]
''',r'''
\PCode{R · tenere insieme i provini}{079_stazioni_intere.R}
\PSmall{Il codice usa le sei stazioni del corso, assunte indipendenti e trattate come un campione unico.}
\PInfo{Con numerosità uguali, aggregare i provini delle stazioni estratte equivale a fare la media delle medie locali.}
''',"Il ricampionamento delle stazioni conserva le relazioni interne ai siti e rappresenta l'incertezza fra unità primarie.")

code(80,"gruppi_diseguali",'''
# Due stazioni illustrative
n80 <- c(2, 8)
medie80 <- c(2.4, 2.8)  # g/cm^3
mean(medie80)           # 2.60
weighted.mean(medie80, n80) # 2.72
# L'aggregazione definisce i pesi.
''')
add(80,"Gruppi diseguali richiedono pesi espliciti",r'''
\PLabel{Esempio illustrativo con due stazioni}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pGroup,minimum width=3cm,minimum height=2.2cm] at(2,2.5){};
\node[pGroup,minimum width=4.8cm,minimum height=2.2cm] at(6.8,2.5){};
\node[pLabel] at(2,3.25){$\bar\rho_1=2{,}4$};
\node[pLabel] at(6.8,3.25){$\bar\rho_2=2{,}8$};
\foreach \xx in {1.5,2.5}\fill[GeoA](\xx,2.2) circle(4pt);
\foreach \xx in {5.2,6.2,7.2,8.2}
\foreach \yy in {1.9,2.45}\fill[GeoB](\xx,\yy) circle(4pt);
\end{tikzpicture}
\[
\widehat\theta_{\mathrm{siti}}=\frac{2{,}4+2{,}8}{2}=2{,}60,
\]
\[
\widehat\theta_{\mathrm{provini}}
=\frac{2(2{,}4)+8(2{,}8)}{10}=2{,}72.
\]
\PSmall{Entrambe sono densità in $\mathrm{g\,cm^{-3}}$, riferite a pesi diversi.}
''',r'''
\PCode{R · due aggregazioni}{080_gruppi_diseguali.R}
\PBody{Nelle repliche, una media di medie assegna uguale peso ai siti estratti. La media di tutti i provini assegna peso proporzionale alla numerosità.}
\PInfo{Il ricampionamento di gruppi interi va accompagnato dalla formula della statistica che si ricalcola.}
''',"Conservare i gruppi mantiene la dipendenza interna; la regola di aggregazione determina il peso attribuito a ogni gruppo.")

code(81,"righe_stazioni",'''
set.seed(17)
br81 <- replicate(2000,
  mean(sample(provini$densita,
              replace = TRUE)))
set.seed(17)
bs81 <- replicate(2000,
  mean(sample(stazioni$densita,
              replace = TRUE)))
c(righe = sd(br81), siti = sd(bs81))
''')
add(81,"Le righe e le stazioni danno SE diversi",r'''
\PLabel{Stesse osservazioni, due unità di ricampionamento}
'''+histplot(["stazioni_righe","stazioni_intere"],["GeoA","GeoB"],
             ["24 provini","6 stazioni"],
             2.50,2.70,[2.5,2.6,2.7],
             r"densità media ($\mathrm{g\,cm^{-3}}$)")+r'''
\PSmall{Con $B=2000$ e seme 17: SE per righe $0{,}014$, per stazioni $0{,}024\,\mathrm{g\,cm^{-3}}$.}
\PBody{La scelta dello schema deriva dal disegno e dalle ipotesi di indipendenza. I sei siti restano una base piccola.}
''',r'''
\PCode{R · ricampionare a due livelli}{081_righe_stazioni.R}
\PInfo{Nel campione, la dispersione per stazioni è maggiore. Altre realizzazioni possono dare un ordinamento diverso.}
''',"La dispersione delle medie ricampionate dipende dall'unità che viene trattata come indipendente.")

code(82,"affioramenti",'''
a82 <- split(stazioni$densita,
              stazioni$affioramento)
set.seed(17)
ab82 <- replicate(2000,
  rb74(a82$A) - rb74(a82$B))
mean(a82$A) - mean(a82$B)
quantile(ab82, c(.025, .975),
         type = 7)
''')
add(82,"Gli affioramenti restano separati",r'''
\PLabel{Contrasto A meno B, tre siti per affioramento}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm,draw=GeoA] (a) at(2.1,4){A1, A2, A3};
\node[pFlow,text width=3.7cm,draw=GeoB] (b) at(7.1,4){B1, B2, B3};
\node[pFlow,text width=3.7cm,fill=GeoA!8] (aa) at(2.1,2){Tre siti estratti entro A\\media delle medie};
\node[pFlow,text width=3.7cm,fill=GeoB!8] (bb) at(7.1,2){Tre siti estratti entro B\\media delle medie};
\draw[pEdge,draw=GeoA](a)--(aa);\draw[pEdge,draw=GeoB](b)--(bb);
\node[pLabel] at(4.6,.2){$\widehat\Delta_{AB}^*=\overline\rho_A^*-\overline\rho_B^*$};
\end{tikzpicture}
\PSmall{Differenza osservata $0{,}097\,\mathrm{g\,cm^{-3}}$. Percentile $[0{,}042;\,0{,}150]\,\mathrm{g\,cm^{-3}}$ per $B=2000$ e seme 17.}
''',r'''
\PCode{R · siti entro affioramento}{082_affioramenti.R}
\PBody{Le repliche conservano tre stazioni per ogni affioramento.}
\PInfo{Tre siti per gruppo limitano l'informazione. L'associazione geologica non dimostra un effetto causale.}
''',"Quando gli affioramenti sono strati del disegno, il ricampionamento deve rispettarne l'appartenenza e i pesi.")

smallg_pic=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
            r"\draw[pAxis](.8,.4)--(9,.4);"]
for y,key1,key2,label,col in [(2.9,"densita_low","densita_high","Percentile","GeoA"),
                           (1.4,"densita_t_low","densita_t_high","Student","GeoB")]:
    xx=lambda v:.8+(v-2.5)/.2*8
    a,b,c=xx(MET[key1]),xx(MET[key2]),xx(MET["densita_media"])
    smallg_pic.extend([rf"\draw[{col},line width=1.4pt]({a:.5f},{y})--({b:.5f},{y});",
                       rf"\fill[{col}]({c:.5f},{y}) circle(3pt);",
                       rf"\node[pNote,text={col},above] at({c:.5f},{y+.2}){{{label}}};",
                       rf"\node[pNote,below] at({a:.5f},{y-.15}){{$ {fmt(MET[key1])} $}};",
                       rf"\node[pNote,below] at({b:.5f},{y-.15}){{$ {fmt(MET[key2])} $}};"])
smallg_pic.extend([r"\node[pNote] at(4.8,-.3){densità media delle stazioni ($\mathrm{g\,cm^{-3}}$)};",
                   r"\end{tikzpicture}"])
code(83,"pochi_siti",'''
# Sei medie locali indipendenti
quantile(bs81, c(.025, .975),
         type = 7)
# Student assume normalita delle
# medie di stazione, oltre a iid.
t.test(stazioni$densita)$conf.int
length(stazioni$densita)  # 6
''')
add(83,"Sei siti lasciano molta incertezza",r'''
\PLabel{Confronto fra due procedure sullo stesso campione}
'''+"\n".join(smallg_pic)+r'''
\PBody{Il percentile usa la distribuzione empirica delle sei medie. Student aggiunge un modello normale iid per le medie di stazione.}
\PSmall{Entrambi i confronti aggregano i sei siti senza trattare gli affioramenti come strati. Le ipotesi vanno dichiarate.}
''',r'''
\PCode{R · confrontare le assunzioni}{083_pochi_siti.R}
\PInfo{Più repliche descrivono meglio le possibilità costruite da sei siti. Nuovi siti indipendenti possono aggiungere informazioni sulla variabilità territoriale.}
\PBody{La conclusione deve riportare selezione dei siti e sensibilità al metodo.}
''',"Un grande numero di repliche calcolate non aumenta il numero di siti osservati né la copertura territoriale.")

code(84,"modello_stazioni",'''
G84 <- 12
m84 <- 6
tau84 <- 2     # SD fra stazioni
rho84 <- tau84^2/(tau84^2+1)
se84 <- sqrt(tau84^2/G84 +
             1/(G84*m84))
c(rho_intra = rho84, SE = se84)
''')
add(84,"Nel laboratorio ogni sito ha un effetto comune",r'''
\PLabel{Dodici stazioni con sei misure ciascuna}
\[
X_{gi}=10+U_g+\varepsilon_{gi},\qquad
U_g\sim\mathcal N(0,\tau^2),\quad
\varepsilon_{gi}\sim\mathcal N(0,1).
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.2cm] (u) at(1.5,2.2){$U_g$\\effetto del sito};
\foreach \yy/\i in {3.5/1,2.2/2,.9/6}{
\node[pFlow,text width=3.1cm,fill=GeoTint] (x\i) at(7,\yy){$X_{g\i}=10+U_g+\varepsilon_{g\i}$};
\draw[pEdge](u.east)--(x\i.west);}
\node[pNote] at(4.1,.2){schema di una stazione};
\end{tikzpicture}
\PSmall{Tutti gli $U_g$ e gli errori $\varepsilon_{gi}$ sono indipendenti. Le misure nello stesso sito condividono $U_g$. Valori adimensionali.}
''',r'''
\PCode{R · precisione del modello}{084_modello_stazioni.R}
\[
\rho_{\mathrm{intra}}=\frac{\tau^2}{\tau^2+1},
\qquad
\mathrm{SE}(\bar X)=
\sqrt{\frac{\tau^2}{G}+\frac1{Gm}}.
\]
\PSmall{Per $\tau=2$: correlazione $0{,}8$, SE teorico $0{,}589$. I siti indipendenti sono $G=12$.}
''',"La componente condivisa entro stazione contribuisce alla varianza della media attraverso le covarianze.")

code(85,"laboratorio_stazioni",'''
r85 <- lab_ricampionamento(
  tau = 2, B = 200, seed = 17)
r85$indicatori
# Variante: componente comune nulla
r85b <- lab_ricampionamento(
  tau = 0, B = 200, seed = 17)
r85b$indicatori
''')
add(85,"Laboratorio: misure o stazioni intere",r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-ricampionamento}{Esperimento · ricampionamento per stazioni}
'''+histplot(["browser_righe","browser_stazioni"],["GeoA","GeoB"],
             ["singole misure","stazioni intere"],8.5,12.7,
             [9,10,11,12],r"media ricampionata (adimensionale)")+r'''
\PSmall{Default $\tau=2$, $B=200$, seme 17. SE delle singole misure $0{,}239$, delle stazioni $0{,}494$.}
\PBody{Ripetere con $\tau=0$. Interpretare la differenza tra il modello generatore e il risultato di un singolo campione.}
''',r'''
\PCode{R · confrontare i due schemi}{085_laboratorio_stazioni.R}
\PInfo{A $\tau=0$ manca la componente comune del modello. Le stime dei due SE possono comunque differire in una realizzazione con dodici siti.}
\PSmall{La media delle repliche può oscillare. Il riferimento teorico $0{,}589$ riguarda campagne nuove generate con $\tau=2$.}
''',"La struttura del generatore chiarisce quali misure condividono variabilità e quale livello deve essere ricampionato.")

add(86,"Un secondo stadio richiede una giustificazione",r'''
\PLabel{Siti selezionati e provini selezionati entro sito}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=7.7cm] (p) at(4.65,4.3){Popolazione di stazioni};
\node[pFlow,text width=3.6cm] (a) at(2.1,2.5){Primo stadio\\selezione delle stazioni};
\node[pFlow,text width=3.6cm] (b) at(7.1,2.5){Secondo stadio\\selezione dei provini};
\draw[pEdge](p.south)--(a.north);
\draw[pEdge](a)--(b);
\node[pFlow,text width=7.7cm,fill=GeoTint] at(4.65,.6)
{La replica deve rappresentare le fonti di casualità\\previste dal disegno e dall'estimando.};
\end{tikzpicture}
\PSmall{Aggiungere un ricampionamento interno ai siti introduce ulteriore variabilità. La scelta richiede pesi, frazioni di campionamento e unità chiaramente definiti.}
''',r'''
\PLabel{Scomposizione della varianza}
\[
\begin{aligned}
\operatorname{Var}(T)
={}&\operatorname{Var}\!\left(E[T\mid S]\right)\\
 &+E\!\left[\operatorname{Var}(T\mid S)\right].
\end{aligned}
\]
\PBody{$S$ rappresenta le unità selezionate al primo stadio. La prima parte descrive la variabilità fra selezioni di siti, la seconda quella residua entro la selezione.}
\PInfo{La formula descrive il modello. Un algoritmo bootstrap deve riprodurre correttamente questi contributi, evitando di contarli due volte.}
''',"Un disegno a più stadi richiede una procedura di ricampionamento motivata per ciascun livello casuale.")

SLIDES[87]=dict(title="Quattro domande per scegliere lo schema",
    section=STR,wide=r'''
\PLabel{Estimando, unità indipendente, relazioni da conservare, statistica}
'''+table(["Caso","Unità estratta","Vincolo conservato","Statistica"],
          [["Due gruppi indipendenti","individuo entro gruppo","numerosità e pesi","differenza di medie"],
           ["Due misure appaiate","coppia completa","associazione entro individuo","media delle differenze"],
           ["Provini per sito","stazione","tutti i provini del sito","media definita dai pesi"],
           ["Serie temporale","blocco contiguo","vicinanze entro blocco","media della serie"]],
          [4.5,4.1,5.1,4.0],h=1.02)+r'''
\vspace{4mm}
\PBody{Esercizio: 120 misure provengono da dieci stazioni indipendenti, con dipendenza entro sito. La domanda riguarda la media delle stazioni. Scrivere l'unità da estrarre e la formula da ricalcolare.}
\PSmall{La risposta deve includere il criterio di selezione delle dieci stazioni e l'eventuale presenza di strati.}
''',recall="La procedura va scelta in base alla domanda scientifica e al disegno, prima di confrontare l'ampiezza degli intervalli.")

code(88,"serie_temporale",'''
r88 <- lab_blocchi(length = 8,
  rho = .7, B = 200, seed = 17)
x88 <- r88$campione
plot(x88, type = "l",
     xlab = "Tempo",
     ylab = "Valore adimensionale")
abline(h = 0, lty = 2)
''')
add(88,"La serie conserva memoria del valore precedente",r'''
\PLabel{Il generatore AR(1) del laboratorio}
'''+lineplot([(float(r["tempo"]),float(r["valore"])) for r in rows("serie")],
              1,120,-4,3,[1,40,80,120],[-3,0,3],
              "tempo", "valore", reference=0)+r'''
\[
X_t=\rho X_{t-1}+\sqrt{1-\rho^2}\,Z_t,
\quad Z_t\overset{\mathrm{iid}}{\sim}\mathcal N(0,1).
\]
\PSmall{$X_1\sim\mathcal N(0,1)$ è indipendente dagli $Z_t$. Con $\rho=0{,}7$, il modello è stazionario con media zero e varianza uno.}
''',r'''
\PCode{R · la serie di 120 valori}{088_serie_temporale.R}
\PBody{I tratti consecutivi tendono a mantenere segni e livelli vicini. La relazione dipende dalla distanza temporale.}
\PInfo{Il caso browser usa 120 osservazioni e blocchi circolari.}
''',"Per una serie dipendente, l'ordine delle osservazioni contiene informazioni necessarie per valutare l'incertezza.")

code(89,"varianza_ar1",'''
n89 <- 120
rho89 <- .7
h89 <- 1:(n89-1)
v89 <- (n89 + 2*sum(
  (n89-h89)*rho89^h89))/n89^2
sqrt(v89)      # SE teorico: .215
1/sqrt(n89)    # Ipotesi iid: .091
''')
acf_pic=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.8,0)--(9,0);\draw[pAxis](.8,0)--(.8,2);"]
for h in range(13):
    xx=.8+8*h/12
    acf_pic.append(rf"\draw[GeoA,line width=2pt]({xx:.4f},0)--({xx:.4f},{1.7*.7**h:.4f});")
for h in [0,4,8,12]:
    acf_pic.append(rf"\node[pNote,below] at({.8+8*h/12},-.05){{$ {h} $}};")
acf_pic.extend([r"\node[pNote,anchor=east] at(.65,1.7){1};",
                r"\node[pNote] at(4.8,-.65){distanza temporale $h$};",
                r"\end{tikzpicture}"])
add(89,"La varianza della media somma le covarianze",r'''
\PLabel{Correlazione teorica $\operatorname{Corr}(X_t,X_{t+h})=\rho^h$}
'''+"\n".join(acf_pic)+r'''
\[
\operatorname{Var}(\bar X)=
\frac{n+2\sum_{h=1}^{n-1}(n-h)\rho^h}{n^2}.
\]
\PSmall{Ci sono $n-h$ coppie a distanza $h$. La formula usa varianza marginale uno e dipendenza AR(1) stazionaria.}
''',r'''
\PCode{R · calcolo sotto il modello}{089_varianza_ar1.R}
\PBody{Per $n=120$ e $\rho=0{,}7$, il SE teorico è $0{,}215$. Con indipendenza e la stessa varianza marginale varrebbe $0{,}091$.}
\PInfo{La formula descrive nuove serie generate dal modello. Il bootstrap lavora invece sulla serie fissata che abbiamo osservato.}
''',"Le covarianze positive fra tempi vicini aumentano la varianza della media rispetto al modello indipendente.")

code(90,"indici_individuali",'''
set.seed(17)
j90 <- sample.int(length(x88),
  length(x88), replace = TRUE)
head(j90, 12)
# I valori adiacenti nella replica
# possono essere lontani nella serie.
head(diff(j90), 11)
''')
add(90,"Estrarre righe cambia le vicinanze temporali",r'''
\PLabel{Indici illustrativi della serie originale e della replica}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pNote,anchor=west] at(.3,4.2){sequenza originale};
\foreach \j in {1,2,3,4,5,6,7,8}{
\node[pFlow,minimum width=.8cm,minimum height=.8cm] (a\j) at({.3+\j},3.3){$\j$};}
\node[pNote,anchor=west] at(.3,1.8){estrazione individuale};
\foreach \v[count=\j] in {7,2,8,2,4,1,6,3}{
\node[pFlow,minimum width=.8cm,minimum height=.8cm,fill=GeoTint] at({.3+\j},.9){$\v$};}
\draw[pEdge,draw=GeoB](a7.south)--(1.3,1.4);
\draw[pEdge,draw=GeoB](a2.south)--(2.3,1.4);
\end{tikzpicture}
\PSmall{La distribuzione marginale dei valori resta empirica. La replica individuale non conserva la relazione fra osservazioni consecutive.}
''',r'''
\PCode{R · esaminare le distanze}{090_indici_individuali.R}
\[
\operatorname{Var}_*(\bar X^*_{\mathrm{iid}})
=\frac{n-1}{n^2}s^2.
\]
\PBody{Questa varianza include la dispersione dei singoli valori. Il modello AR(1) contiene anche contributi di covarianza.}
''',"L'estrazione indipendente delle righe conserva la distribuzione empirica marginale e rimuove la struttura temporale della replica.")

code(91,"blocchi_esempio",'''
n91 <- 8
L91 <- 3
inizi91 <- c(7, 3, 5)
j91 <- unlist(lapply(inizi91,
  function(s)
    ((s-1+0:(L91-1)) %% n91)+1))
j91             # 9 indici
j91[1:n91]      # Troncamento a 8
''')
add(91,"Un blocco circolare può attraversare il bordo",r'''
\PLabel{Esempio illustrativo: $n=8$, lunghezza $L=3$}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \j in {1,2,3,4,5,6,7,8}{
\node[pFlow,minimum width=.78cm,minimum height=.7cm] (a\j) at({.3+\j},3.8){$\j$};}
\draw[pEdge,draw=GeoC](a8.north)--++(0,.55)-|(a1.north);
\node[pNote] at(4.7,5){dopo 8 si torna a 1};
\foreach \v[count=\j] in {7,8,1,3,4,5,5,6,7}{
\pgfmathtruncatemacro{\b}{ceil(\j/3)}
\ifnum\b=1\def\col{GeoA}\else\ifnum\b=2\def\col{GeoB}\else\def\col{GeoC}\fi\fi
\node[pFlow,draw=\col,fill=\col!10,minimum width=.75cm,minimum height=.75cm] (r\j) at({.3+.94*\j},1.8){$\v$};}
\draw[Muted,line width=.8pt](r9.south west)--(r9.north east);
\node[pNote,text=GeoA] at(2.18,.8){inizio 7};
\node[pNote,text=GeoB] at(5,.8){inizio 3};
\node[pNote,text=GeoC] at(7.82,.8){inizio 5};
\node[pNote] at(4.7,0){concatenare i blocchi e conservare i primi otto indici};
\end{tikzpicture}
''',r'''
\PCode{R · concatenazione circolare}{091_blocchi_esempio.R}
\PSmall{\texttt{\%\%} restituisce il resto della divisione. Dopo l'ultima posizione, la formula riparte dalla prima.}
\PInfo{I blocchi mantengono l'ordine interno. Le giunzioni fra blocchi creano nuove vicinanze e la chiusura circolare è una scelta della procedura.}
''',"Il bootstrap circolare seleziona tratti consecutivi, consente il ritorno all'inizio e tronca la concatenazione alla lunghezza originale.")

code(92,"replica_blocchi",'''
n92 <- length(x88)
L92 <- 8
set.seed(17)
s92 <- sample.int(n92,
  ceiling(n92/L92), replace = TRUE)
j92 <- unlist(lapply(s92,
  function(s)
    ((s-1+0:(L92-1)) %% n92)+1))
mean(x88[j92[1:n92]])
''')
add(92,"La replica ha ancora 120 osservazioni",r'''
\PLabel{Quindici blocchi di otto valori}
\[
K=\left\lceil\frac nL\right\rceil,\qquad
S_k\overset{\mathrm{iid}}{\sim}\operatorname{Unif}\{1,\ldots,n\},
\]
\[
J_{kr}=1+\big[(S_k-1+r)\bmod n\big],
\quad r=0,\ldots,L-1.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (a) at(2,2.8){15 inizi estratti\\uno per blocco};
\node[pFlow,text width=3.5cm,fill=GeoTint] (b) at(7,2.8){120 indici\\15 sequenze da 8};
\node[pFlow,text width=7.8cm] (c) at(4.5,.8){$\bar X^*=n^{-1}\sum_{j=1}^{n}X_{J_j}$};
\draw[pEdge](a)--(b);
\draw[pEdge](b.south)--(c.north east);
\end{tikzpicture}
\PSmall{Per lunghezze che non dividono $n$, si conservano solo i primi $n$ indici concatenati.}
''',r'''
\PCode{R · una replica circolare}{092_replica_blocchi.R}
\PSmall{\texttt{ceiling(n/L)} arrotonda in eccesso il numero di blocchi. Il seme del frammento identifica una replica illustrativa.}
''',"La lunghezza della serie ricampionata rimane n; cambia il numero di blocchi necessari per costruirla.")

code(93,"confronto_blocchi",'''
# Output del caso iniziale r88
r88$indicatori
split(r88$dati$media,
      r88$dati$metodo) |>
  lapply(sd)
# SE teorico: modello AR(1)
sqrt(v89)
''')
add(93,"Il bootstrap a blocchi cambia la dispersione",r'''
\PLabel{Serie AR(1) fissata, $n=120$, $\rho=0{,}7$, $L=8$}
'''+histplot(["blocchi_righe","blocchi_circolari"],["GeoA","GeoB"],
             ["singole osservazioni","blocchi circolari"],
             -.65,.9,[-.5,0,.5],r"media ricampionata (adimensionale)")+r'''
\PSmall{Con $B=200$ e seme 17: SE individuale $0{,}122$, SE a blocchi $0{,}264$. Il SE teorico di nuove serie è $0{,}215$.}
\PBody{Una singola serie e una lunghezza illustrativa del blocco producono una stima approssimata.}
''',r'''
\PCode{R · leggere le tre quantità}{093_confronto_blocchi.R}
\PInfo{Lo scarto dal riferimento teorico comprende la variabilità del campione e l'approssimazione del metodo. Un numero finito di repliche aggiunge errore numerico.}
\PSmall{L'unità rimane adimensionale, come quella del generatore.}
''',"Conservare sequenze temporali modifica la stima dell'incertezza, senza garantire un risultato esatto per ogni serie e ogni lunghezza.")

code(94,"numero_blocchi",'''
n94 <- 120
L94 <- c(1, 8, 30)
data.frame(lunghezza = L94,
  blocchi = ceiling(n94/L94))
# L=1: 120 blocchi individuali
# L=8: 15 blocchi
# L=30: 4 blocchi
''')
add(94,"La lunghezza del blocco cambia il compromesso",r'''
\PLabel{Stessa serie, lunghezze da 1 a 30}
'''+lineplot([(float(r["L"]),float(r["se"])) for r in rows("lunghezza_blocchi")],
              1,30,.1,.3,[1,8,15,22,30],[.1,.2,.3],
              "lunghezza del blocco $L$", "SE bootstrap",
              reference=MET["serie_se_teorico"])+r'''
\PSmall{$B=1000$ per ogni $L$, serie generata con seme 17 e ricampionamenti con seme 417. Tratteggio: SE teorico AR(1).}
\PBody{Blocchi lunghi conservano più vicinanze e riducono il numero di segmenti estratti. La precisione non migliora necessariamente al crescere di $L$.}
''',r'''
\PCode{R · contare i segmenti}{094_numero_blocchi.R}
\PInfo{A $L=1$ i due schemi hanno la stessa distribuzione. Sequenze diverse danno stime simulate diverse.}
\PSmall{La curva misura la sensibilità a $L$. Il valore appropriato dipende da struttura e stabilità della serie.}
''',"Una lunghezza appropriata dipende dalla dipendenza della serie e dalla statistica; il valore otto è illustrativo.")

code(95,"laboratorio_blocchi",'''
r95 <- lab_blocchi(length = 8,
  rho = .7, B = 200, seed = 17)
r95$indicatori
r95b <- lab_blocchi(length = 1,
  rho = .7, B = 200, seed = 17)
r95b$indicatori
identical(r95$campione,
          r95b$campione) # TRUE
''')
add(95,"Laboratorio: variare L sulla stessa serie",r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-blocchi}{Esperimento · bootstrap a blocchi}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=7.6cm] (x) at(4.6,4.6){Serie fissata: $n=120$, $\rho=0{,}7$, seme 17};
\foreach \xx/\l/\k in {1.55/1/120,4.65/8/15,7.75/30/4}{
\node[pFlow,text width=2.55cm,fill=GeoTint] (b\l) at(\xx,2.5){$L=\l$\\$\k$ blocchi};
\draw[pEdge](x.south)--(b\l.north);}
\node[pFlow,text width=7.6cm] at(4.6,.4){Confrontare SE, forma delle repliche\\e stabilità cambiando $B$};
\end{tikzpicture}
\PSmall{Il controllo del sito consente $L$ da 1 a 30. Cambiare solo $L$ mantiene la serie iniziale identica.}
''',r'''
\PCode{R · confrontare le lunghezze}{095_laboratorio_blocchi.R}
\PBody{Confrontare $L=1,8,30$ per $\rho=0{,}7$. Ripetere con $\rho=0$, che cambia il campione.}
\PInfo{Il laboratorio assume stazionarietà. Tendenze o salti di regime richiedono altre valutazioni.}
''',"Il confronto fra lunghezze è interpretabile quando campione, statistica e numero di repliche restano espliciti.")

code(96,"tre_numeri",'''
n96 <- 30   # Osservazioni fissate
B96 <- 200  # Repliche per calcolo
R96 <- 30   # Ripetizioni del calcolo
c(osservazioni = n96,
  repliche = B96,
  ripetizioni = R96)
B96*R96     # 6000 medie calcolate
''')
add(96,"n, B e R contano oggetti diversi",r'''
\PLabel{Tre livelli nell'esperimento di precisione}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=7.8cm] (x) at(4.7,4.9){Un campione osservato\\$n=30$ valori fissati};
\node[pFlow,text width=7.8cm,fill=GeoTint] (b) at(4.7,2.8){Un calcolo dell'estremo\\$B=200$ medie bootstrap e un quantile};
\node[pFlow,text width=7.8cm] (r) at(4.7,.7){Ripetizione del calcolo\\$R=30$ quantili ottenuti dallo stesso campione};
\draw[pEdge](x)--(b);\draw[pEdge](b)--(r);
\end{tikzpicture}
''',r'''
\PCode{R · tre dimensioni}{096_tre_numeri.R}
\PBody{Il laboratorio genera una sola volta i 30 dati. Ogni ripetizione usa nuove estrazioni bootstrap per approssimare lo stesso quantile condizionato.}
\PInfo{La dispersione fra i 30 limiti descrive l'errore numerico dell'algoritmo sul campione fissato.}
''',"Le osservazioni, le repliche bootstrap e le ripetizioni dell'algoritmo appartengono a livelli diversi della procedura.")

code(97,"stabilita_se",'''
set.seed(17)
x97 <- rlnorm(30, 0, .6)
se97 <- function(B)
  sd(replicate(B,
    mean(sample(x97, replace = TRUE))))
set.seed(717)
s97 <- sapply(c(50, 200, 1000),
  function(B) replicate(12, se97(B)))
s97
''')
mcse_pic=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
          r"\draw[pAxis](.8,0)--(9,0);\draw[pAxis](.8,0)--(.8,3);"]
scy=lambda y:(y-.10)/.03*2.7
for val in [.10,.11,.12,.13]:
    mcse_pic.extend([rf"\draw[Rule](.8,{scy(val):.5f})--(8.8,{scy(val):.5f});",
                     rf"\node[pNote,anchor=east] at(.65,{scy(val):.5f}){{$ {fmt(val,2)} $}};"])
for row in rows("mc_se"):
    B,rep,se=int(row["B"]),int(row["ripetizione"]),float(row["se"])
    xx={50:2,200:4.9,1000:7.8}[B]+(rep-6.5)*.055
    mcse_pic.append(rf"\fill[GeoA]({xx:.5f},{scy(se):.5f}) circle(2.4pt);")
mcse_pic.append(rf"\draw[GeoB,dashed,line width=1pt](.8,{scy(MET['precisione_se_exact']):.5f})--(8.8,{scy(MET['precisione_se_exact']):.5f});")
for x,B in [(2,50),(4.9,200),(7.8,1000)]:
    mcse_pic.append(rf"\node[pNote,below] at({x},-.08){{$ {B} $}};")
mcse_pic.extend([r"\node[pNote] at(4.8,-.65){repliche bootstrap $B$};",
                  r"\node[pNote,rotate=90] at(-.23,1.4){SE bootstrap stimato};",
                  r"\end{tikzpicture}"])
add(97,"Anche l'errore standard ha errore numerico",r'''
\PLabel{Dodici esecuzioni per ogni valore di B}
'''+"\n".join(mcse_pic)+r'''
\[
\mathrm{SE}_*=\sqrt{\frac{29}{30^2}s^2}=0{,}1136.
\]
\PSmall{Tratteggio: valore condizionato esatto della media. I punti sono stime da nuove sequenze bootstrap sullo stesso campione di 30 valori.}
''',r'''
\PCode{R · ripetere la stima del SE}{097_stabilita_se.R}
\PBody{Con $B$ maggiore, le stime oscillano meno attorno allo stesso SE condizionato.}
\PInfo{Il campione e la sua rappresentatività restano invariati.}
''',"L'errore standard bootstrap è una quantità da stimare; la sua approssimazione numerica dipende da B.")

code(98,"limiti_ripetuti",'''
set.seed(17)
x98 <- rlnorm(30, 0, .6)
q98 <- replicate(30, {
  b <- replicate(200,
    mean(sample(x98, replace = TRUE)))
  quantile(b, .975, type = 7)
})
sd(q98)  # Variabilita numerica
''')
add(98,"L'estremo superiore cambia fra esecuzioni",r'''
\PLabel{Trenta calcoli sullo stesso campione}
'''+lineplot([(float(r["ripetizione"]),float(r["limite"])) for r in rows("precisione_200")],
              1,30,1.53,1.67,[1,10,20,30],[1.55,1.60,1.65],
              "ripetizione del calcolo", "quantile 0,975",color="GeoC")+r'''
\[
s_{\mathrm{MC}}=
\operatorname{SD}(\widehat q^{*(1)}_{0{,}975},
\ldots,\widehat q^{*(30)}_{0{,}975}).
\]
\PSmall{Con $B=200$, la SD dei 30 limiti è $0{,}0237$. I dati originari sono identici in ogni ripetizione.}
''',r'''
\PCode{R · ripetere il quantile}{098_limiti_ripetuti.R}
\PBody{Il ciclo interno calcola un limite da 200 medie. Il ciclo esterno ripete 30 volte il calcolo.}
\PInfo{La SD quantifica la precisione del limite calcolato sul campione fissato.}
''',"Ripetere il calcolo con dati fissati permette di stimare quanto l'estremo dell'intervallo dipende dall'approssimazione Monte Carlo.")

code(99,"posizione_coda",'''
B99 <- c(40, 200, 1000)
p99 <- .975
h99 <- 1 + (B99-1)*p99
data.frame(B = B99, posizione = h99,
  repliche_coda_circa = B99*(1-p99))
# Il quantile dipende da pochi
# valori vicini alla coda superiore.
''')
add(99,"Le code contengono poche repliche",r'''
\PLabel{Estremo superiore del percentile al 95\%}
'''+table([r"$B$",r"$h=1+(B-1)\,0{,}975$","Coda del 2,5\\%"],
          [["40","39,025","circa 1 replica"],
           ["200","195,025","circa 5 repliche"],
           ["1000","975,025","circa 25 repliche"]],
          [1.6,4.0,3.7],h=.85)+r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.4,.4)--(9,.4);
\draw[GeoA,line width=3pt](.6,.4)--(7.7,.4);
\draw[GeoB,line width=3pt](7.7,.4)--(8.7,.4);
\node[pNote,text=GeoB,above] at(7.7,.7){coda superiore};
\node[pNote] at(4.5,-.35){ordinamento delle statistiche, schema non in scala};
\end{tikzpicture}
\PSmall{Le posizioni determinano i valori che entrano nell'interpolazione. Una coda poco popolata può dare limiti instabili.}
''',r'''
\PCode{R · la posizione del quantile}{099_posizione_coda.R}
\PBody{La stabilità del SE non garantisce quella dei quantili. Occorre controllare anche gli estremi.}
\PInfo{\texttt{sd(b)/sqrt(B)} riguarda la media. I quantili richiedono un controllo specifico.}
''',"Per valutare la precisione di un intervallo, occorre controllare la stabilità dei suoi estremi e dichiarare la convenzione dei quantili.")

code(100,"confronto_B",'''
r100a <- lab_precisione(
  B = 200, seed = 17)
r100b <- lab_precisione(
  B = 1000, seed = 17)
c(B200 = sd(r100a$dati$y),
  B1000 = sd(r100b$dati$y))
identical(r100a$campione,
          r100b$campione)
''')
qcompare=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
          r"\draw[pAxis](.8,0)--(9,0);\draw[pAxis](.8,0)--(.8,3);"]
qy=lambda x:(x-1.53)/.14*2.8
for v in [1.55,1.60,1.65]:
    qcompare.extend([rf"\draw[Rule](.8,{qy(v):.5f})--(8.8,{qy(v):.5f});",
                     rf"\node[pNote,anchor=east] at(.65,{qy(v):.5f}){{$ {fmt(v,2)} $}};"])
for center,name,col,lab in [(2.9,"precisione_200","GeoC","200"),
                          (6.8,"precisione_1000","GeoA","1000")]:
    for row in rows(name):
        j,v=int(row["ripetizione"]),float(row["limite"])
        xx=center+(j-15.5)*.045
        qcompare.append(rf"\fill[{col}]({xx:.5f},{qy(v):.5f}) circle(2.4pt);")
    qcompare.append(rf"\node[pNote,below] at({center},-.08){{$B={lab}$}};")
qcompare.extend([r"\node[pNote,rotate=90] at(-.23,1.4){quantile superiore};",
                  r"\node[pNote] at(4.8,-.65){30 ripetizioni per ciascun B};",
                  r"\end{tikzpicture}"])
add(100,"Più repliche stabilizzano il calcolo",r'''
\PLabel{Stesso campione di 30 valori, due scelte di B}
'''+"\n".join(qcompare)+r'''
\PSmall{SD dei limiti: $0{,}0237$ con $B=200$ e $0{,}0129$ con $B=1000$. I punti sono sfalsati orizzontalmente per renderli visibili.}
\PBody{Il confronto quantifica la precisione numerica raggiunta in questa esecuzione.}
''',r'''
\PCode{R · verificare il campione fissato}{100_confronto_B.R}
\[
\mathrm{SE}_{\mathrm{MC}}(\overline\theta^*)
=\frac{\mathrm{SD}_*(\widehat\theta^*)}{\sqrt B}.
\]
\PSmall{La formula riguarda la media delle repliche. Per i quantili, controllare la stabilità con ripetizioni.}
''',"B controlla la precisione dell'approssimazione della distribuzione bootstrap costruita da un campione che rimane fissato.")

code(101,"laboratorio_precisione",'''
r101 <- lab_precisione(
  B = 200, seed = 17)
r101$indicatori
plot(r101$dati$x, r101$dati$y,
  xlab = "Ripetizione",
  ylab = "Limite superiore")
mean(r101$campione) # Media fissata
''')
add(101,"Laboratorio: quanto è stabile il limite?",r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-precisione}{Esperimento · precisione del quantile}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\tit/\txt/\col [count=\idx] in {
4.6/{Dato osservato}/{30 valori, media fissata a 1,364}/{GeoA},
2.8/{Calcolo interno}/{B medie bootstrap, un quantile 0,975}/{GeoB},
1/{Calcolo esterno}/{30 limiti, SD fra le ripetizioni}/{GeoC}}{
\node[pFlow,text width=2.7cm,draw=\col] (a\idx) at(1.65,\yy){\tit};
\node[pFlow,text width=5.2cm,fill=\col!8] (b\idx) at(6.5,\yy){\txt};
\draw[pEdge,draw=\col](a\idx)--(b\idx);}
\end{tikzpicture}
\PSmall{Il sito consente $B$ da 40 a 1000. La statistica mostrata riguarda soltanto il limite superiore al 97,5\%.}
''',r'''
\PCode{R · riprodurre il laboratorio}{101_laboratorio_precisione.R}
\PBody{Confrontare $B=40,200,1000$ registrando la SD dei limiti. Ripetere con un altro seme.}
\PInfo{Un nuovo seme rigenera anche i dati. Il confronto a campione fissato richiede lo stesso seme.}
''',"Il laboratorio di precisione ripete l'algoritmo sullo stesso campione e misura l'oscillazione numerica dell'estremo superiore.")

code(102,"registro",'''
dir.create("Risultati",
           showWarnings = FALSE)
registro102 <- list(
  n = 30, B = 200, seed = 17,
  unita = "osservazione",
  statistica = "media",
  quantili = "type 7",
  ambiente = sessionInfo())
saveRDS(registro102,
        "Risultati/registro.rds")
''')
add(102,"Il risultato deve poter essere ricostruito",r'''
\PLabel{Che cosa accompagna un intervallo bootstrap}
'''+table(["Elemento","Informazione da registrare"],
          [["Dati","file, unità, criteri di selezione"],
           ["Estimando","popolazione, pesi, orientamento del contrasto"],
           ["Schema","individui, coppie, stazioni o blocchi"],
           ["Calcolo","statistica, B, seme, tipo di quantile"],
           ["Ambiente","versione di R, algoritmo, codice eseguito"]],
          [2.4,6.9],h=.86)+r'''
\PSmall{Se si confrontano più schemi, riportare per ciascuno ipotesi, numerosità delle unità indipendenti e limiti dell'inferenza.}
''',r'''
\PCode{R · salvare il registro}{102_registro.R}
\PSmall{\texttt{readRDS()} rilegge l'oggetto salvato. \texttt{sessionInfo()} descrive l'ambiente.}
\PInfo{La riproduzione richiede lo stesso algoritmo, un ambiente compatibile e i dati originari.}
''',"La riproducibilità richiede dati, disegno, statistica, impostazioni numeriche e ambiente di esecuzione.")
