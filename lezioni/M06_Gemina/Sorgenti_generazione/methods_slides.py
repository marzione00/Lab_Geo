"""Gemina M06, slide 47-77: appaiamento, ranghi, categorie e molteplicità.

Le figure quantitative sono costruite dalle coordinate prodotte in R da
methods_proof/calcoli_figure.R. I diagrammi restano interamente editabili.
"""
from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "methods_proof/coordinate"
SLIDES, CODES = {}, {}
MET = {r["indicatore"]: float(r["valore"])
       for r in csv.DictReader((FIG / "metriche.csv").open())}

def rows(name):
    return list(csv.DictReader((FIG / (name + ".csv")).open()))

def fmt(x, d=3):
    return f"{x:.{d}f}".replace(".", "{,}")

def add(n, title, left, right, recall):
    sec = ("COPPIE E DIFFERENZE" if n <= 53 else "CONFRONTI BASATI SUI RANGHI" if n <= 59
           else "CONTEGGI E ASSOCIAZIONE" if n <= 64 else "PIÙ GRUPPI" if n <= 69
           else "FAMIGLIE DI CONFRONTI")
    SLIDES[n] = dict(title=title, section=sec, left=left, right=right, recall=recall)

def code(n, name, body):
    key = f"{n:03}_{name}.R"
    CODES[key] = body.strip() + "\n"
    return key

def rhs(n, name, title, body):
    return rf"\PCode{{R · {title}}}{{{n:03}_{name}.R}}" + "\n" + rf"\PBody{{{body}}}"

def table(headers, data, widths, h=.67):
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for j, row in enumerate([headers] + data):
        y = -j*h
        fill = "Navy" if j == 0 else "white" if j % 2 else "GeoTint"
        color = "white" if j == 0 else "Ink"
        out.append(rf"\fill[{fill}] (0,{y}) rectangle ({sum(widths)},{y+h});")
        x = 0
        for cell, w in zip(row, widths):
            out.append(rf"\node[pLabel,text={color}] at({x+w/2},{y+h/2}){{{cell}}};")
            x += w
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)

def lineplot(series, xmin, xmax, ymin, ymax, xticks, yticks, xlab, ylab, height=2.8):
    sx = lambda x: .8+8*(x-xmin)/(xmax-xmin)
    sy = lambda y: height*(y-ymin)/(ymax-ymin)
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for y in yticks:
        out += [rf"\draw[Rule](.8,{sy(y):.5f})--(8.8,{sy(y):.5f});",
                rf"\node[pNote,anchor=east] at(.65,{sy(y):.5f}){{$ {fmt(y,2)} $}};"]
    for x in xticks:
        out += [rf"\draw[Muted]({sx(x):.5f},0)--++(0,-.08);",
                rf"\node[pNote,below] at({sx(x):.5f},-.08){{$ {fmt(x,0)} $}};"]
    for i,(pts,color,label) in enumerate(series):
        out.append(rf"\draw[{color},line width=1pt] plot coordinates{{"+
                   " ".join(f"({sx(x):.5f},{sy(y):.5f})" for x,y in pts)+"};")
        out.append(rf"\draw[{color},line width=1.5pt]({.8+4.3*i},{height+.42})--++(.4,0);")
        out.append(rf"\node[pNote,anchor=west,text={color}] at({1.3+4.3*i},{height+.42}){{{label}}};")
    out += [rf"\draw[pAxis](.8,0)--(9,0);",rf"\draw[pAxis](.8,0)--(.8,{height+.12});",
            rf"\node[pNote] at(4.8,-.62){{{xlab}}};",
            rf"\node[pNote,rotate=90] at(-.25,{height/2}){{{ylab}}};",r"\end{tikzpicture}"]
    return "\n".join(out)

def paired_plot():
    dat = rows("coppie")
    ys = [float(r[k]) for r in dat for k in ("prima","dopo")]
    lo, hi = min(ys)-.01,max(ys)+.01
    sy = lambda y: 3.4*(y-lo)/(hi-lo)
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for j in range(4):
        v=lo+(hi-lo)*j/3
        out += [rf"\draw[Rule](1.1,{sy(v)})--(8.6,{sy(v)});",
                rf"\node[pNote,anchor=east] at(.95,{sy(v)}){{$ {fmt(v,2)} $}};"]
    for r in dat:
        a,b=float(r['prima']),float(r['dopo'])
        out += [rf"\draw[GeoC!45,line width=.6pt](2.4,{sy(a):.5f})--(7.4,{sy(b):.5f});",
                rf"\fill[GeoA](2.4,{sy(a):.5f}) circle(1.4pt);",
                rf"\fill[GeoB](7.4,{sy(b):.5f}) circle(1.4pt);"]
    out += [r"\node[pLabel,text=GeoA] at(2.4,-.35){Prima};",
            r"\node[pLabel,text=GeoB] at(7.4,-.35){Dopo};",
            r"\node[pNote,rotate=90] at(-.1,1.7){misura (u.c.)};",r"\end{tikzpicture}"]
    return "\n".join(out)

def ci_plot(mean, lo, hi, xmin, xmax, label, unit):
    sx=lambda v: .85+8*(v-xmin)/(xmax-xmin)
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         rf"\draw[pAxis](.85,0)--(9,0);",
         rf"\draw[Muted,dashed]({sx(0):.5f},-.1)--({sx(0):.5f},2.15);",
         rf"\draw[GeoA,line width=2pt]({sx(lo):.5f},1.15)--({sx(hi):.5f},1.15);",
         rf"\fill[GeoA]({sx(mean):.5f},1.15) circle(3pt);",
         rf"\draw[GeoA]({sx(lo):.5f},.96)--({sx(lo):.5f},1.34);",
         rf"\draw[GeoA]({sx(hi):.5f},.96)--({sx(hi):.5f},1.34);",
         rf"\node[pLabel] at(4.8,2.1){{{label}}};"]
    for v in [xmin,0,xmax]:
        out.append(rf"\node[pNote,below] at({sx(v):.5f},-.07){{$ {fmt(v,2)} $}};")
    out+=[rf"\node[pNote] at(4.8,-.62){{{unit}}};",r"\end{tikzpicture}"]
    return "\n".join(out)

add(47,"La coppia identifica l’unità del confronto",r'''
\PLabel{Tre provini: sei misure, tre cambiamenti}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pNote] at(1,4){identificativo};
\node[pNote,text=GeoA] at(3.45,4){prima};
\node[pNote,text=GeoB] at(5.9,4){dopo};
\node[pNote] at(8.3,4){differenza};
\foreach \y/\id/\a/\b/\d in {3.1/P01/10/11/{+1},1.9/P02/14/16/{+2},.7/P03/8/7/{-1}}{
\node[pLabel] at(1,\y){\id};
\node[pFlow,minimum width=1.2cm,minimum height=.75cm] (a\id) at(3.45,\y){$\a$};
\node[pFlow,minimum width=1.2cm,minimum height=.75cm] (b\id) at(5.9,\y){$\b$};
\node[pFlow,fill=GeoTint,minimum width=1.2cm,minimum height=.75cm] (d\id) at(8.3,\y){$\d$};
\draw[pEdge](a\id)--(b\id);\draw[pEdge](b\id)--(d\id);}
\end{tikzpicture}
\PSmall{Valori costruiti in unità convenzionali. Ogni riga riguarda lo stesso provino osservato in due condizioni.}
''',r'''
\PLabel{Parametro e verso}
\[
D_i=Y_{i,\mathrm{dopo}}-Y_{i,\mathrm{prima}},
\qquad \Delta=E(D_i).
\]
\PBody{Il campione per l’analisi è il vettore dei cambiamenti. Le coppie devono essere indipendenti secondo il disegno.}
\PInfo{Una misura ripetuta sullo stesso provino conserva l’abbinamento. Se più provini appartengono allo stesso sito, va valutata anche la dipendenza tra provini.}
''',"Il numero di coppie determina la numerosità dell’analisi; gli identificativi conservano l’abbinamento.")

code(48,"allineare_coppie",'''
# Esempio: righe in ordine diverso
p48 <- data.frame(id=c(1,2,3),
                  prima=c(10,14,8))
d48 <- data.frame(id=c(3,1,2),
                 dopo=c(7,11,16))
j48 <- merge(p48,d48,by="id")
stopifnot(!anyDuplicated(j48$id))
j48$D <- j48$dopo-j48$prima
j48  # Differenze: 1, 2, -1
''')
add(48,"Allineare le misure tramite identificativo",r'''
\PLabel{Unione per chiave}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3cm] (p) at(2,3.65){Prima\\ordine: 1, 2, 3};
\node[pFlow,text width=3cm] (d) at(7.1,3.65){Dopo\\ordine: 3, 1, 2};
\node[pFlow,fill=GeoTint,text width=5.5cm] (j) at(4.55,1.8){Unire per \texttt{id}\\1: $(10,11)$ · 2: $(14,16)$ · 3: $(8,7)$};
\draw[pEdge](p.south)--++(0,-.45)-|(j.north);
\draw[pEdge](d.south)--++(0,-.45)-|(j.north);
\node[pNote,text width=8.5cm] at(4.55,.25){Controllare chiavi duplicate, identificativi assenti e coppie incomplete prima di sottrarre.};
\end{tikzpicture}
\PSmall{La sottrazione per posizione avrebbe prodotto $-3,-3,+8$: tre abbinamenti errati.}
''',rhs(48,"allineare_coppie","unire per chiave",r"\texttt{merge()} associa le righe con lo stesso identificativo. Qui tutte le chiavi compaiono una sola volta in entrambe le tabelle."),"L’ordine delle righe può cambiare; l’identificativo della coppia deve restare stabile.")

code(49,"osservare_coppie",'''
d49 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
stopifnot(!anyDuplicated(d49$id))
D49 <- d49$dopo-d49$prima
# Una differenza per provino
c(n=length(D49), media=mean(D49))
plot(D49, ylab="Dopo - prima (u.c.)",
     xlab="Indice del provino")
abline(h=0, lty=2)
qqnorm(D49); qqline(D49)
''')
add(49,"Osservare il cambiamento di ciascun provino",
    r"\PLabel{24 coppie sintetiche del corso}"+paired_plot()+
    rf"\PSmall{{Ogni segmento conserva una coppia. Cambiamento medio: $\bar D={fmt(MET['coppie_media'],5)}$ u.c.; la pendenza descrive il segno di ciascun cambiamento.}}",
    rhs(49,"osservare_coppie","dati e differenze",r"Il grafico dei cambiamenti mostra la risposta di ciascun provino; il grafico quantile-quantile aiuta a valutarne la forma rispetto alla normale."),
    "Il grafico delle coppie conserva l’eterogeneità dei provini e rende visibili i cambiamenti individuali.")

code(50,"covarianza",'''
d50 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
a50 <- d50$prima; b50 <- d50$dopo
v50 <- var(b50)+var(a50)-
       2*cov(b50,a50)
stopifnot(isTRUE(all.equal(
  v50,var(b50-a50))))
c(var_D=v50,cor=cor(a50,b50))
''')
add(50,"La covarianza entra nella differenza",r'''
\PLabel{Il termine condiviso si cancella}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm] (a) at(2.2,3.2){Prima\\$10+u_i+\varepsilon_{i,p}$};
\node[pFlow,text width=3.6cm] (b) at(7,3.2){Dopo\\$10+u_i+0{,}6+\varepsilon_{i,d}$};
\node[pFlow,text width=6.5cm,fill=GeoTint] (d) at(4.6,1.25){$D_i=0{,}6+\varepsilon_{i,d}-\varepsilon_{i,p}$};
\draw[pEdge](a.south)--++(0,-.35)-|(d.north);
\draw[pEdge](b.south)--++(0,-.35)-|(d.north);
\end{tikzpicture}
\[
\operatorname{Var}(D)=\sigma_d^2+\sigma_p^2-2\operatorname{Cov}(Y_d,Y_p).
\]
\PSmall{Modello del laboratorio: $u_i\sim N(0,\tau^2)$; errori indipendenti $N(0,1)$, indipendenti da $u_i$. Quindi $\operatorname{Var}(D)=2$.}
''',rhs(50,"covarianza","verificare l’identità",r"La relazione vale anche per le varianze campionarie calcolate sulle stesse coppie complete. Una covarianza positiva riduce la variabilità della differenza."),"La variabilità condivisa dalle due misure si elimina nella differenza entro coppia.")

code(51,"se_appaiato",'''
# Generatore del laboratorio, tau=3
set.seed(17); n51 <- 30
u51 <- rnorm(n51,0,3)
a51 <- 10+u51+rnorm(n51)
b51 <- 10+u51+.6+rnorm(n51)
c(appaiato=sd(b51-a51)/sqrt(n51),
  indipendente=sqrt(var(a51)/n51+
                    var(b51)/n51))
''')
tr=rows("tau_se")
add(51,"Ignorare le coppie cambia l’errore standard",
    r"\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m06-appaiati}{Laboratorio · appaiati}"+
    lineplot([([(float(r['tau']),float(r['appaiato'])) for r in tr],"GeoA","coppie conservate"),
              ([(float(r['tau']),float(r['indipendente'])) for r in tr],"GeoB","coppie ignorate")],
              0,6,0,2,[0,2,4,6],[0,.5,1,1.5,2],r"deviazione standard condivisa $\tau$","errore standard",2.7)+
    r"\PSmall{Trenta coppie, seme 17, $\tau>0$. A seme fisso i cambiamenti restano uguali. Con $\tau=0$, R cambia il consumo di numeri casuali: il confronto numerico richiede cautela.}",
    rhs(51,"se_appaiato","due calcoli a confronto",r"L’errore standard appaiato usa la dispersione dei cambiamenti. Il secondo calcolo trascura la covarianza tra le due misure."),
    "La maggiore precisione deriva dal disegno appaiato quando la covarianza è positiva, e non dal raddoppio della numerosità.")

code(52,"t_differenze",'''
d52 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
D52 <- d52$dopo-d52$prima
n52 <- length(D52)
se52 <- sd(D52)/sqrt(n52)
t52 <- mean(D52)/se52  # H0: Delta=0
p52 <- 2*pt(-abs(t52),df=n52-1)
c(t=t52,p=p52)
''')
add(52,"Il test appaiato usa le differenze",r'''
\PLabel{Una sola variabile per coppia}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.45cm] (d) at(1.5,2.9){$D_1,\ldots,D_n$\\cambiamenti};
\node[pFlow,text width=2.35cm] (m) at(4.7,2.9){$\bar D$ e $s_D$\\media e dispersione};
\node[pFlow,text width=2.2cm,fill=GeoTint] (t) at(7.9,2.9){$t_{n-1}$\\riferimento nullo};
\draw[pEdge](d)--(m);\draw[pEdge](m)--(t);
\end{tikzpicture}
\[
t=\frac{\bar D-\Delta_0}{s_D/\sqrt n},\qquad
IC_{1-\alpha}:\ \bar D\pm t_{n-1,1-\alpha/2}\frac{s_D}{\sqrt n}.
\]
\PBody{Il riferimento $t$ è esatto se le differenze sono indipendenti e normali. Con $n=24$ coppie, i gradi di libertà sono 23.}
\PSmall{$\Delta_0$: cambiamento medio sotto l’ipotesi nulla; $s_D$: deviazione standard dei cambiamenti.}
''',rhs(52,"t_differenze","statistica e p-value",r"\texttt{pt()} calcola probabilità della distribuzione $t$. Il raddoppio della coda inferiore produce il p-value bilaterale."),"Le condizioni del test riguardano le differenze e l’indipendenza fra coppie.")

code(53,"due_chiamate",'''
d53 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
a53 <- t.test(d53$dopo-d53$prima)
b53 <- t.test(d53$dopo,d53$prima,
              paired=TRUE)
stopifnot(isTRUE(all.equal(
  a53$p.value,b53$p.value)))
a53$conf.int  # Intervallo al 95%
''')
add(53,"Due chiamate, lo stesso confronto",
    r"\PLabel{Ventiquattro provini, dopo meno prima}"+
    ci_plot(MET['coppie_media'],MET['coppie_lo'],MET['coppie_hi'],-.01,.065,r"Stima e intervallo al 95\%","cambiamento medio (u.c.)")+
    rf"\PBody{{$\bar D={fmt(MET['coppie_media'],5)}$ u.c.; IC 95\% $[{fmt(MET['coppie_lo'],5)};\ {fmt(MET['coppie_hi'],5)}]$ u.c.}}"+
    r"\PSmall{La procedura stima il cambiamento medio della popolazione rappresentata dai provini. L’attribuzione a un trattamento richiede un disegno adeguato.}",
    rhs(53,"due_chiamate","verifica equivalente",r"\texttt{paired=TRUE} sottrae il secondo argomento dal primo. Invertire gli argomenti cambia segno a stima e intervallo, mantenendo il p-value bilaterale."),
    "Un controllo equivalente verifica contemporaneamente verso, abbinamento e specificazione del test.")

code(54,"confronti_ranghi",'''
# Esempio con un pareggio: valore 3
a54 <- c(1,3,5); b54 <- c(2,3,6)
M54 <- outer(b54,a54,">")+
       .5*outer(b54,a54,"==")
M54  # Righe B, colonne A
c(U=sum(M54),theta=mean(M54))
''')
add(54,"I ranghi contano confronti a coppie",
    r"\PLabel{Ogni osservazione B viene confrontata con ogni A}"+
    table(["B / A","1","3","5"],[["2","1","0","0"],["3","1",r"$1/2$","0"],["6","1","1","1"]],[2,2.2,2.2,2.2],.73)+
    r'''
\[
U=\sum_{i=1}^{n_B}\sum_{j=1}^{n_A}
\left[\mathbf1(B_i>A_j)+\tfrac12\mathbf1(B_i=A_j)\right].
\]
\PSmall{Nell’esempio $U=5{,}5$ su 9 confronti: $\widehat\theta=5{,}5/9\simeq0{,}611$. Un pareggio contribuisce per metà.}
''',rhs(54,"confronti_ranghi","tutti i confronti",r"\texttt{outer()} applica un confronto a tutte le combinazioni. Il risultato descrive l’ordinamento relativo dei due campioni."),"La statistica dei ranghi conserva l’ordine dei valori; i pareggi ricevono un contributo esplicito.")

add(55,"La probabilità di superiorità ha un verso",r'''
\PLabel{Due estrazioni indipendenti dalle popolazioni}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.2cm] (a) at(2.1,3.5){Una unità da A\\valore $A$};
\node[pFlow,text width=3.2cm] (b) at(7,3.5){Una unità da B\\valore $B$};
\node[pFlow,text width=5.6cm,fill=GeoTint] (c) at(4.55,1.6){Confrontare $B$ con $A$\\maggiore: 1 · pari: $1/2$ · minore: 0};
\draw[pEdge](a.south)--++(0,-.4)-|(c.north);
\draw[pEdge](b.south)--++(0,-.4)-|(c.north);
\end{tikzpicture}
\[
\theta=P(B>A)+\tfrac12P(B=A),\qquad
\widehat\theta=\frac{U}{n_Bn_A}.
\]
\PSmall{Con dati continui i pareggi hanno probabilità zero; con misure arrotondate o discrete possono essere frequenti.}
''',r'''
\PLabel{Parametro e riferimento del test}
\PBody{$\theta>1/2$ descrive una maggiore probabilità di osservare B sopra A. Scambiando i gruppi si ottiene $1-\theta$.}
\PInfo{Il rank-sum usuale è calibrato sotto l’uguaglianza delle distribuzioni, con osservazioni indipendenti. La sola ipotesi $\theta=1/2$ non basta a giustificare la stessa calibrazione per forme diverse.}
\PSmall{Se il modello ammette soltanto uno spostamento di posizione fra forme uguali, la lettura del confronto come spostamento è appropriata.}
''',"Definire il parametro di interesse e le condizioni del riferimento nullo prima di interpretare il p-value dei ranghi.")

code(56,"rank_sum",'''
f56 <- read.csv(
  "Dati/fossili_simulati.csv")
g56 <- split(f56$diametro_tot_um,
             f56$morfotipo)
x56 <- g56$Spiky; y56 <- g56$Rounded
wilcox.test(x56,y56,exact=FALSE,
            correct=TRUE)
mean(outer(x56,y56,">")+
     .5*outer(x56,y56,"=="))
''')
add(56,"Ranghi e diametro dei fossili",r'''
\PLabel{Spiky rispetto a Rounded}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[Rule,line width=10pt](.8,1.1)--(8.8,1.1);
\draw[GeoA,line width=10pt](.8,1.1)--(4.8,1.1);
\foreach \x/\t in {.8/0,4.8/{1/2},8.8/1}{
\draw[Muted](\x,.8)--(\x,1.4);\node[pLabel,below] at(\x,.65){$\t$};}
\node[pNote] at(4.8,2.8){probabilità di superiorità stimata};
'''+rf"\fill[GeoB]({.8+8*MET['fossili_theta']:.5f},1.1) circle(4pt);\node[pLabel,text=GeoB] at({.8+8*MET['fossili_theta']:.5f},1.95){{$\widehat\theta={fmt(MET['fossili_theta'],3)}$}};"+
    r'''
\end{tikzpicture}
\PBody{I diametri sono sintetici; ciascun gruppo comprende 80 fossili. Il parametro mantiene il verso Spiky rispetto a Rounded.}
\PSmall{Si specificano approssimazione normale e correzione di continuità. Un confronto su una media risponde a una domanda diversa.}
''',rhs(56,"rank_sum","ipotesi e opzioni",r"La lista \texttt{g56} contiene i diametri separati per morfotipo. La superiorità descrive l’effetto; il p-value riguarda l’ipotesi di distribuzioni uguali."),"La scelta del test segue la quantità da confrontare; le opzioni di calcolo fanno parte del risultato.")

code(57,"stessa_mediana",'''
# Normali teoriche: mediana comune
x57 <- seq(-6,6,length.out=241)
matplot(x57,cbind(dnorm(x57),
        dnorm(x57,0,2)),type="l",
        xlab="Valore",ylab="Densita")
pnorm(0/sqrt(1^2+2^2))  # P(B>A)=.5
''')
den=rows("densita_scale")
add(57,"Stessa mediana, dispersioni diverse",
    r"\PLabel{Distribuzioni normali teoriche}"+
    lineplot([([(float(r['x']),float(r['stretta'])) for r in den],"GeoA",r"$A\sim N(0,1)$"),
              ([(float(r['x']),float(r['larga'])) for r in den],"GeoB",r"$B\sim N(0,4)$")],
              -6,6,0,.42,[-6,-3,0,3,6],[0,.2,.4],"valore (adimensionale)","densità",2.5)+
    r"\PSmall{Entrambe hanno mediana zero. Per simmetria $P(B>A)=1/2$, benché le distribuzioni siano differenti. In $N(\mu,\sigma^2)$ il secondo parametro è la varianza.}",
    rhs(57,"stessa_mediana","un controesempio",r"Il rank-sum non è un test universale di ogni differenza di forma. L’uguaglianza delle mediane e quella delle distribuzioni richiedono interpretazioni distinte."),
    "Una dispersione diversa può lasciare invariata la probabilità di superiorità; il confronto deve corrispondere alla domanda.")

code(58,"signed_rank",'''
D58 <- c(1,-2,3,-4) # Esempio
z58 <- D58[D58!=0]  # Escludere zeri
r58 <- rank(abs(z58))
sum(r58[z58>0])     # W+ = 4
wilcox.test(D58,mu=0,
            exact=FALSE,correct=TRUE)
# Ipotesi: simmetria attorno a zero
''')
add(58,"Il signed-rank conserva segno e ampiezza",
    r"\PLabel{Differenze costruite, senza pareggi}"+
    table([r"$D_i$",r"$|D_i|$","rango",r"contributo a $W^+$"],
          [["+1","1","1","1"],["−2","2","2","0"],["+3","3","3","3"],["−4","4","4","0"]],[1.8,1.8,2,3],.62)+
    r'''
\[
W^+=\sum_{i:D_i>0}\operatorname{rank}(|D_i|)=1+3=4.
\]
\PSmall{Differenze indipendenti e simmetriche attorno al centro nullo. Gli zeri e i pareggi richiedono convenzioni esplicite di calcolo.}
''',rhs(58,"signed_rank","ranghi delle differenze",r"\texttt{wilcox.test(D58)} usa il signed-rank. Qui sono dichiarate approssimazione normale e correzione di continuità."),"Il signed-rank appaiato richiede simmetria delle differenze attorno al centro specificato dall’ipotesi nulla.")

code(59,"test_segni",'''
D59 <- c(1,-2,3,-4,2,0,1)
z59 <- D59[D59!=0]
k59 <- sum(z59>0); n59 <- length(z59)
# Tra i cambiamenti non nulli
binom.test(k59,n59,p=.5)
# Si usano soltanto i segni;
# le ampiezze non entrano nel test.
''')
add(59,"Quale caratteristica delle differenze?",
    r"\PLabel{Tre domande, tre riferimenti}"+
    table(["procedura","caratteristica usata"],
          [[r"$t$ appaiato","media e dispersione"],
           ["signed-rank","segni e ranghi delle ampiezze"],
           ["test dei segni","numero di cambiamenti positivi"]],[2.9,6.4],.8)+
    r'''
\[
K=\sum_{i=1}^{n_*}\mathbf1(D_i>0),\qquad
K\sim\operatorname{Bin}(n_*,1/2)\quad\text{sotto }H_0.
\]
\PSmall{$n_*$ conta le differenze non nulle. L’ipotesi riguarda $P(D>0\mid D\ne0)=1/2$, con segni indipendenti.}
''',rhs(59,"test_segni","positivo o negativo",r"L’esclusione degli zeri è dichiarata. Il test sui segni tratta una domanda diversa dal cambiamento medio e non usa le ampiezze osservate."),"Procedure applicate agli stessi dati possono confrontare parametri diversi; vanno motivate prima di conoscere il p-value.")

code(60,"conteggi_quote",'''
# Esempio costruito: 30 unita per sito
T60 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
dimnames(T60) <- list(
  sito=c("A","B"),
  esito=c("Presenza","Assenza"))
T60
prop.table(T60,1) # Quote per riga
''')
add(60,"Le percentuali conservano il denominatore",r'''
\PLabel{Presenza e assenza in due siti: esempio costruito}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,anchor=east] at(.75,2.75){A};
\node[pLabel,anchor=east] at(.75,1.2){B};
\fill[GeoA](1,2.35) rectangle(5.8,3.15);
\fill[GeoA!15](5.8,2.35) rectangle(9,3.15);
\fill[GeoB](1,.8) rectangle(3.4,1.6);
\fill[GeoB!15](3.4,.8) rectangle(9,1.6);
\node[pLabel,text=white] at(3.4,2.75){18 / 30 = 60\%};
\node[pLabel] at(7.4,2.75){12 assenze};
\node[pLabel,text=white] at(2.2,1.2){30\%};
\node[pLabel] at(6.2,1.2){21 assenze};
\node[pNote] at(2.2,.25){9 presenze su 30};
\node[pNote] at(5,3.75){lunghezza totale = 100\% del sito};
\end{tikzpicture}
\[
\widehat p_A=\frac{18}{30}=0{,}60,\qquad
\widehat p_B=\frac9{30}=0{,}30.
\]
\PSmall{Le quote descrivono i dati; la tabella dei conteggi alimenta il confronto statistico.}
''',rhs(60,"conteggi_quote","conteggi e quote",r"Il secondo argomento di \texttt{prop.table()} vale 1 per normalizzare ciascuna riga. Nomi di righe e colonne rendono leggibile il verso del confronto."),"Una percentuale richiede un denominatore; le unità contate devono corrispondere al disegno di campionamento.")

code(61,"attesi",'''
O61 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
E61 <- outer(rowSums(O61),
             colSums(O61))/sum(O61)
E61  # 13.5 e 16.5 per riga
chisq.test(O61,correct=FALSE)$expected
''')
add(61,"Gli attesi derivano dai margini",
    r"\PLabel{Indipendenza fra sito ed esito}"+
    table(["osservati","presenza","assenza","totale"],
          [["A","18","12","30"],["B","9","21","30"],["totale","27","33","60"]],[2.2,2.3,2.3,2.3],.65)+
    r'''
\[
E_{ij}=\frac{n_{i+}\,n_{+j}}n,\qquad
E_{A,\mathrm{presenza}}=\frac{30\cdot27}{60}=13{,}5.
\]
\PSmall{$n_{i+}$: totale della riga; $n_{+j}$: totale della colonna; $n$: totale generale. Gli attesi possono essere non interi.}
''',rhs(61,"attesi","ricostruire gli attesi",r"Il prodotto esterno dei margini riproduce tutti i conteggi attesi sotto indipendenza. Il controllo con \texttt{chisq.test()} verifica il calcolo."),"Gli attesi sono valori del modello nullo stimati dai margini, non nuovi conteggi osservati.")

code(62,"chi_quadrato",'''
O62 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
q62 <- chisq.test(O62,correct=FALSE)
C62 <- (O62-q62$expected)^2/
        q62$expected
C62  # Contributi delle quattro celle
c(X2=sum(C62),p=q62$p.value)
''')
add(62,"Ogni cella contribuisce al chi-quadrato",
    r"\PLabel{Scarti quadratici rapportati agli attesi}"+
    table(["cella","presenza","assenza"],
          [["A",r"$20{,}25/13{,}5=1{,}500$",r"$20{,}25/16{,}5=1{,}227$"],
           ["B",r"$20{,}25/13{,}5=1{,}500$",r"$20{,}25/16{,}5=1{,}227$"]],[1.4,3.8,3.8],.83)+
    r'''
\[
X^2=\sum_{i,j}\frac{(O_{ij}-E_{ij})^2}{E_{ij}},\qquad
df=(r-1)(c-1).
\]
'''+rf"\PBody{{Qui $X^2={fmt(MET['chi_stat'],3)}$, $df=1$, $p={fmt(MET['chi_p'],4)}$ senza correzione di continuità.}}"+
    r"\PSmall{La calibrazione chi-quadrato è approssimata e richiede unità indipendenti e frequenze adeguate.}",
    rhs(62,"chi_quadrato","somma dei contributi",r"\texttt{correct=FALSE} disattiva la correzione di Yates nella tabella $2\times2$. Confronti software richiedono le stesse opzioni."),"Gli scarti vengono standardizzati per gli attesi; l’accuratezza del riferimento dipende anche dalle frequenze e dal disegno.")

code(63,"fisher",'''
# Margini: 27 presenze, 33 assenze
a63 <- 0:27
pr63 <- dhyper(a63,27,33,30)
pobs63 <- dhyper(18,27,33,30)
# Bilaterale: includere tabelle
# non piu probabili dell'osservata
sum(pr63[pr63<=pobs63*(1+1e-7)])
T63 <- matrix(c(18,12,9,21),2,
              byrow=TRUE)
fisher.test(T63)$p.value
''')
fish=rows("fisher")
fisherplot=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
for r in fish:
    x=.8+8*int(r['a'])/27; y=2.4*float(r['p'])/.21
    col="GeoB" if r['estremo']=="TRUE" else "GeoA"
    fisherplot.append(rf"\draw[{col},line width=2.6pt]({x:.5f},0)--({x:.5f},{y:.5f});")
for a in [0,9,18,27]:
    fisherplot.append(rf"\node[pNote,below] at({.8+8*a/27:.5f},-.05){{$ {a} $}};")
for p in [0,.1,.2]:
    fisherplot.append(rf"\node[pNote,anchor=east] at(.65,{2.4*p/.21:.5f}){{$ {fmt(p,1)} $}};")
fisherplot += [r"\draw[pAxis](.8,0)--(9,0);\draw[pAxis](.8,0)--(.8,2.6);",
              r"\node[pNote,rotate=90] at(-.12,1.2){probabilità};",
              r"\node[pNote] at(4.8,-.6){presenze nel sito A, a margini fissati};",
              r"\node[pNote,text=GeoB] at(4.8,2.95){arancio: tabelle incluse nel p-value bilaterale};",r"\end{tikzpicture}"]
add(63,"Fisher condiziona sui margini osservati",
    r"\PLabel{Riferimento ipergeometrico sotto odds ratio = 1}"+"\n".join(fisherplot)+
    r'''
\[
P(A=a\mid\text{margini})=
\frac{\binom{27}{a}\binom{33}{30-a}}{\binom{60}{30}}.
\]
'''+rf"\PSmall{{Il bilaterale di R somma le probabilità delle tabelle non più probabili dell’osservata: qui $p={fmt(MET['fisher_p'],4)}$.}}",
    rhs(63,"fisher","calcolo condizionato",r"\texttt{dhyper()} assegna una probabilità a ciascuna tabella compatibile con i margini. La tolleranza numerica include correttamente probabilità uguali."),
    "Esatto descrive il riferimento condizionato; l’indipendenza delle unità e la coerenza del disegno restano necessarie.")

code(64,"categorie_browser",'''
# Impostazione iniziale del browser
T64 <- matrix(c(15,35,25,35),2,
              byrow=TRUE)
q64 <- chisq.test(T64,correct=FALSE)
prop.table(T64,1)
c(atteso_min=min(q64$expected),
  p_chi=q64$p.value,
  p_fisher=fisher.test(T64)$p.value)
''')
add(64,"Leggere il laboratorio delle categorie",r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m06-categorie}{Laboratorio · categorie}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (a) at(2.2,3.55){Gruppo A: 50 unità\\15 presenze · 35 assenze};
\node[pFlow,text width=3.5cm] (b) at(7,3.55){Gruppo B: 60 unità\\25 presenze · 35 assenze};
\node[pFlow,fill=GeoTint,text width=6cm] (t) at(4.6,1.55){Confrontare quote e conteggi\\$15/50=0{,}30$ · $25/60\simeq0{,}417$};
\draw[pEdge](a.south)--++(0,-.4)-|(t.north);
\draw[pEdge](b.south)--++(0,-.4)-|(t.north);
\end{tikzpicture}
\PSmall{Il controllo cambia le presenze in B; il suo totale resta 60. Questo esempio usa denominatori diversi da quelli delle slide precedenti.}
''',rhs(64,"categorie_browser","riferimenti dichiarati",r"Una frequenza attesa piccola segnala un possibile problema dell’approssimazione. La scelta del riferimento considera la tabella e il disegno, oltre a una soglia numerica."),"Nel laboratorio cambiano le presenze in B; le numerosità di A e B restano rispettivamente 50 e 60.")

code(65,"quattro_gruppi",'''
# Generatore iniziale: quattro gruppi
set.seed(17); n65 <- 30
g65 <- factor(rep(LETTERS[1:4],
                  each=n65))
mu65 <- rep((0:3)*.5,each=n65)
s65 <- rep(seq(1,2,length.out=4),
            each=n65)
y65 <- rnorm(4*n65,mu65,s65)
tapply(y65,g65,mean)
''')
anova_dat=rows("anova_dati")
ys=[float(r['y']) for r in anova_dat]; yl=math.floor(min(ys)); yh=math.ceil(max(ys))
sy=lambda y: .15+3.2*(y-yl)/(yh-yl)
groupplot=[r"\begin{tikzpicture}[x=1cm,y=1cm]"]
for tick in range(yl,yh+1,2):
    groupplot += [rf"\draw[Rule](.8,{sy(tick)})--(8.9,{sy(tick)});",
                  rf"\node[pNote,anchor=east] at(.65,{sy(tick)}){{$ {tick} $}};"]
for j,g in enumerate("ABCD"):
    x=1.7+2.1*j
    vals=[float(r['y']) for r in anova_dat if r['gruppo']==g]
    for k,y in enumerate(vals):
        groupplot.append(rf"\fill[GeoA!70]({x+(.11*(k%5-2)):.5f},{sy(y):.5f}) circle(1.15pt);")
    ym=sy(sum(vals)/len(vals))
    groupplot += [rf"\draw[GeoB,line width=1.6pt]({x-.4},{ym:.5f})--({x+.4},{ym:.5f});",
                  rf"\node[pLabel] at({x},-.25){{{g}}};"]
groupplot += [r"\node[pNote,rotate=90] at(-.1,1.8){valore (adimensionale)};",
              r"\node[pNote,text=GeoB] at(4.8,3.9){punti: osservazioni · tratti: medie campionarie};",r"\end{tikzpicture}"]
add(65,"Quattro gruppi, una domanda sulle medie",
    r"\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m06-anova}{Laboratorio · ANOVA}"+"\n".join(groupplot)+
    r"\PSmall{Trenta valori per gruppo, seme 17. Medie generatrici: $0;0{,}5;1;1{,}5$. Deviazioni standard: $1;4/3;5/3;2$.}",
    rhs(65,"quattro_gruppi","generare e descrivere",r"Il controllo \texttt{ratio=2} indica il rapporto tra deviazioni standard estreme. La configurazione iniziale ammette già varianze diverse."),
    "Il confronto globale riguarda le medie; il grafico permette di esaminare anche dispersioni, numerosità e valori estremi.")

add(66,"Scomporre gli scarti entro e fra gruppi",r'''
\PLabel{Esempio costruito: A = (1,3), B = (4,6)}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,.1)--(9,.1);
\foreach \x/\v in {1/1,2.5/2,4/3,4.75/{3{,}5},5.5/4,7/5,8.5/6}{
\node[pNote,below] at(\x,0){$\v$};}
\foreach \x in {1,4}{\fill[GeoA](\x,1.35) circle(3pt);}
\foreach \x in {5.5,8.5}{\fill[GeoB](\x,2.65) circle(3pt);}
\draw[GeoA,line width=1.2pt](1,1.35)--(4,1.35);
\draw[GeoB,line width=1.2pt](5.5,2.65)--(8.5,2.65);
\draw[GeoA,dashed](2.5,.25)--(2.5,1.75);
\draw[GeoB,dashed](7,.25)--(7,3.05);
\draw[GeoC,dashed](4.75,.25)--(4.75,3.6);
\node[pNote,text=GeoA] at(2.5,1.95){$\bar x_A=2$};
\node[pNote,text=GeoB] at(7,3.3){$\bar x_B=5$};
\node[pNote,text=GeoC] at(4.75,3.95){media globale $\bar x=3{,}5$};
\end{tikzpicture}
\PSmall{I segmenti mostrano la dispersione interna; le medie di gruppo si discostano dalla media globale.}
''',r'''
\PLabel{Identità algebrica}
\[
SS_T=SS_B+SS_W.
\]
\[
SS_B=\sum_gn_g(\bar x_g-\bar x)^2=9,
\]
\[
SS_W=\sum_g\sum_i(x_{gi}-\bar x_g)^2=4.
\]
\PBody{La somma totale vale 13. Le somme quadratiche hanno unità pari al quadrato della risposta.}
\PInfo{$n_g$ conta le unità del gruppo; $\bar x_g$ è la sua media; $\bar x$ è la media di tutte le osservazioni.}
''',"La scomposizione delle somme quadratiche è un’identità; il riferimento probabilistico del test richiede ulteriori ipotesi.")

code(67,"anova_a_mano",'''
y67 <- c(1,3,4,6)
g67 <- factor(c("A","A","B","B"))
m67 <- ave(y67,g67,FUN=mean)
W67 <- sum((y67-m67)^2)  # Entro: 4
B67 <- sum((m67-mean(y67))^2) # 9
F67 <- (B67/1)/(W67/2)
F67
pf(F67,1,2,lower.tail=FALSE)
anova(lm(y67~g67))  # Stesso F
''')
add(67,"Il rapporto F confronta quadrati medi",
    r"\PLabel{Esempio: due gruppi, quattro unità}"+
    table(["origine","somma","gradi di libertà","quadrato medio"],
          [["fra gruppi","9",r"$G-1=1$","9"],["entro gruppi","4",r"$N-G=2$","2"],["totale","13",r"$N-1=3$","—"]],[2.15,1.4,2.8,2.85],.7)+
    r'''
\[
F=\frac{SS_B/(G-1)}{SS_W/(N-G)}=\frac92=4{,}5.
\]
\PSmall{Sotto medie uguali, errori indipendenti, normali e con varianza comune: $F\sim F_{G-1,N-G}$. $G$: gruppi; $N$: unità totali.}
''',rhs(67,"anova_a_mano","verificare il rapporto F",r"\texttt{lm(y67\textasciitilde g67)} descrive una media per gruppo. \texttt{anova()} confronta la variabilità fra gruppi con quella residua."),"Il rapporto F non ha unità; il suo riferimento esatto richiede normalità, indipendenza e varianza comune degli errori.")

code(68,"welch_piu_gruppi",'''
r68 <- read.csv(
  "Dati/rocce_simulate.csv")
# Densita nelle litologie simulate
q68 <- oneway.test(
  densita~litologia_generatrice,
  data=r68,var.equal=FALSE)
q68
tapply(r68$densita,
       r68$litologia_generatrice,sd)
''')
add(68,"Welch ammette varianze diverse",r'''
\PLabel{Pesi inversi alla varianza della media}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \x/\name/\v/\w in {1.65/A/1/30,4.6/B/4/{7{,}5},7.55/C/9/{3{,}33}}{
\node[pFlow,text width=2.5cm] at(\x,3.6){Gruppo \name\\$n_g=30$, $s_g^2=\v$};
\node[pFlow,fill=GeoTint,text width=2.5cm] at(\x,1.55){peso $w_g\simeq\w$};
\draw[pEdge](\x,2.95)--(\x,2.2);}
\end{tikzpicture}
\[
w_g=\frac{n_g}{s_g^2},\qquad
\bar x_w=\frac{\sum_gw_g\bar x_g}{\sum_gw_g}.
\]
\PSmall{Esempio di pesi costruito. La procedura corregge statistica e gradi di libertà; non basta sostituire la media globale con $\bar x_w$.}
''',rhs(68,"welch_piu_gruppi","dati delle rocce",r"\texttt{oneway.test(..., var.equal=FALSE)} applica l’estensione di Welch. Le osservazioni devono essere indipendenti; forma e valori estremi vanno esaminati."),"Pesi maggiori corrispondono a medie stimate più precisamente; Welch mantiene la domanda sull’uguaglianza delle medie.")

code(69,"contrasti_previsti",'''
# Famiglia prevista: tre confronti
set.seed(17)
g69 <- rep(LETTERS[1:4],each=30)
y69 <- rnorm(120,rep(0:3,each=30))
z69 <- split(y69,g69)
p69 <- sapply(z69[c("B","C","D")],
  function(z) t.test(z,z69$A)$p.value)
p.adjust(p69,method="holm")
''')
add(69,"Il test globale non identifica le coppie",r'''
\PLabel{Ipotesi globale e contrasti dichiarati}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=7.5cm] (h) at(4.55,3.8){$H_0:\mu_A=\mu_B=\mu_C=\mu_D$};
\node[pNote,text width=8.4cm] at(4.55,2.45){Il rifiuto fornisce evidenza di almeno una differenza; non stabilisce quali coppie differiscano.};
\node[pFlow,fill=GeoTint,text width=2.4cm] at(1.6,.9){$\mu_B-\mu_A$};
\node[pFlow,fill=GeoTint,text width=2.4cm] at(4.6,.9){$\mu_C-\mu_A$};
\node[pFlow,fill=GeoTint,text width=2.4cm] at(7.6,.9){$\mu_D-\mu_A$};
\end{tikzpicture}
\PSmall{Esempio: tre confronti con un gruppo di riferimento, definiti prima di osservare i risultati. Il test globale non elimina la molteplicità.}
''',rhs(69,"contrasti_previsti","famiglia con riferimento A",r"\texttt{split()} separa i valori per gruppo. Le tre chiamate a Welch conservano verso e metodo; Holm tiene conto della famiglia dichiarata."),"Dalla domanda scientifica derivano il confronto globale e gli eventuali contrasti; ciascun livello richiede un’interpretazione propria.")

add(70,"Definire la famiglia dei confronti",r'''
\PLabel{Quattro gruppi: sei confronti a coppie}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,minimum width=1.1cm] (a) at(1.3,3.6){A};
\node[pFlow,minimum width=1.1cm] (b) at(7.6,3.6){B};
\node[pFlow,minimum width=1.1cm] (c) at(1.3,.8){C};
\node[pFlow,minimum width=1.1cm] (d) at(7.6,.8){D};
\draw[GeoA,line width=.9pt](a)--(b);\draw[GeoA,line width=.9pt](a)--(c);
\draw[GeoA,line width=.9pt](b)--(d);\draw[GeoA,line width=.9pt](c)--(d);
\draw[GeoC,line width=.9pt](a)--(d);\draw[GeoC,line width=.9pt](b)--(c);
\end{tikzpicture}
\[
m=\binom G2=\frac{G(G-1)}2=6\quad\text{per }G=4.
\]
\PSmall{Tutte le coppie formano una famiglia diversa dai soli tre confronti con A. La famiglia deriva dalle domande che si vogliono valutare insieme.}
''',r'''
\PLabel{Errore nell’insieme dei test}
\[
\mathrm{FWER}=P(V\ge1),
\]
\PBody{dove $V$ conta i falsi rifiuti nella famiglia. Un livello del 5\% per ciascun test non determina un rischio familiare del 5\%.}
\PInfo{Dichiarare quali esiti, gruppi e contrasti appartengono alla famiglia. Conservarli nella relazione, compresi quelli con p-value grandi.}
''',"La famiglia precisa l’insieme di conclusioni rispetto al quale si vuole controllare almeno un falso rifiuto.")

code(71,"rischio_familiare",'''
# Nulle vere; test indipendenti
m71 <- c(1,6,10,20,50)
a71 <- .05
risk71 <- 1-(1-a71)^m71
cbind(test=m71,FWER=risk71)
''')
fw=rows("fwer")
add(71,"Il rischio cresce con i test indipendenti",
    r"\PLabel{Tutte le ipotesi nulle vere; livello individuale 0,05}"+
    lineplot([([(float(r['m']),float(r['FWER'])) for r in fw],"GeoA",r"$1-0{,}95^m$")],
             1,50,0,1,[1,10,20,30,40,50],[0,.25,.5,.75,1],"numero di test m","almeno un falso rifiuto",2.6)+
    r'''\[
\mathrm{FWER}=1-(1-\alpha)^m.
\]
\PSmall{Per dieci test il rischio è circa 40,1\%. La formula richiede indipendenza e probabilità di rifiuto individuali esattamente pari ad $\alpha$.}
''',rhs(71,"rischio_familiare","la probabilità complementare",r"\texttt{(1-a71)\textasciicircum m71} calcola la probabilità che nessun test rifiuti. La dipendenza tra test può cambiare questo risultato."),"La formula del rischio familiare è esatta in condizioni specifiche; non va applicata automaticamente a test dipendenti.")

code(72,"ripetere_famiglie",'''
set.seed(17)
v72 <- replicate(2000, {
  p72 <- runif(20) # Ipotesi nulle
  h72 <- p.adjust(p72,"holm")
  c(grezzi=any(p72<.05),
    Holm=any(h72<.05))
})
rowMeans(v72) # Quote di famiglie
# 2000 famiglie, 20 test per famiglia
''')
add(72,"Una famiglia non misura il rischio",r'''
\PLabel{Ripetere l’intera famiglia per stimare una probabilità}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.5cm] (p) at(1.5,3.4){20 p-value\\sotto ipotesi nulle};
\node[pFlow,text width=2.4cm] (v) at(4.7,3.4){almeno un rifiuto?\\0 oppure 1};
\node[pFlow,fill=GeoTint,text width=2.4cm] (r) at(7.85,3.4){2000 famiglie\\media degli indicatori};
\draw[pEdge](p)--(v);\draw[pEdge](v)--(r);
\node[pNote,text width=8.6cm] at(4.7,1.75){La variabilità tra famiglie descrive il rischio della procedura; una singola famiglia mostra soltanto il suo esito.};
\end{tikzpicture}
'''+rf"\PBody{{Con seme 17: quota grezza ${fmt(MET['fwer_mc_grezzi'],4)}$; quota con Holm ${fmt(MET['fwer_mc_holm'],3)}$.}}"+
    r"\PSmall{La quota Holm ha errore standard Monte Carlo circa 0,005: un valore simulato poco sopra 0,05 è compatibile con la variabilità del calcolo.}",
    rhs(72,"ripetere_famiglie","simulare famiglie intere",r"Nel laboratorio il controllo genera una sola famiglia. Questo codice aggiunge ripetizioni indipendenti per stimarne il rischio."),
    "Una frequenza simulata approssima il rischio e ha una propria incertezza Monte Carlo.")

add(73,"Holm procede fino al primo mancato rifiuto",r'''
\PLabel{Quattro p-value ordinati; livello familiare 0,05}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=7.4cm,fill=GeoTint] (a) at(4.5,4.1){$0{,}003\le0{,}05/4=0{,}0125$\quad rifiutare $H_{(1)}$};
\node[pFlow,text width=7.4cm,draw=GeoB,fill=GeoB!7] (b) at(4.5,2.4){$0{,}018>0{,}05/3\simeq0{,}0167$\quad arrestarsi};
\node[pFlow,text width=7.4cm] (c) at(4.5,.7){$H_{(2)},H_{(3)},H_{(4)}$\quad non rifiutate};
\draw[pEdge](a)--(b);\draw[pEdge](b)--(c);
\end{tikzpicture}
\[
p_{(j)}\le\frac{\alpha}{m-j+1}\quad\text{fino al primo confronto non soddisfatto.}
\]
''',r'''
\PLabel{Significato della procedura}
\PBody{Ordinare i p-value dal minore al maggiore. Il numero di ipotesi ancora considerate determina la soglia di ciascun passo.}
\PInfo{Holm controlla fortemente la FWER per p-value marginali validi, anche in presenza di dipendenza tra test. Forte significa per qualunque configurazione di ipotesi nulle vere e false.}
\PSmall{I p-value dell’esempio sono $0{,}003$; $0{,}018$; $0{,}041$; $0{,}2$.}
''',"Dopo il primo mancato rifiuto Holm si arresta; confrontare isolatamente le soglie successive cambierebbe la procedura.")

code(74,"holm",'''
p74 <- c(.003,.018,.041,.2)
adj74 <- p.adjust(p74,method="holm")
# Calcolo sui p-value gia ordinati
manuale74 <- pmin(1,cummax(4:1*p74))
stopifnot(isTRUE(all.equal(
  adj74,manuale74)))
data.frame(p74,adj74,rifiuto=adj74<=.05)
''')
add(74,"I p-value corretti conservano l’ordinamento",
    r"\PLabel{La stessa decisione attraverso i valori corretti}"+
    table(["ipotesi","p-value","Holm",r"rifiuto al 5\%"],
          [["1","0,003","0,012","sì"],["2","0,018","0,054","no"],
           ["3","0,041","0,082","no"],["4","0,200","0,200","no"]],[1.6,2.1,2.1,3.3],.66)+
    r'''
\[
\widetilde p_{(j)}=\min\!\left\{1,\max_{k\le j}\big[(m-k+1)p_{(k)}\big]\right\}.
\]
\PSmall{La massimizzazione cumulativa mantiene l’arresto di Holm. I valori corretti si confrontano con il livello familiare $\alpha$.}
''',rhs(74,"holm","funzione e calcolo manuale",r"\texttt{cummax()} restituisce il massimo raggiunto fino a ciascuna posizione. Il calcolo manuale qui presume p-value già ordinati; \texttt{p.adjust()} gestisce anche l’ordine originale."),"Riportare p-value originali e corretti permette di ricostruire il controllo della famiglia.")

code(75,"famiglia_completa",'''
p75 <- c(A_B=.003,A_C=.018,
          A_D=.041,B_C=.2)
# Correggere la famiglia dichiarata
adj75 <- p.adjust(p75,"holm")
data.frame(contrasto=names(p75),
           p=unname(p75),
           Holm=unname(adj75))
''')
add(75,"Conservare anche gli esiti sfavorevoli",r'''
\PLabel{La selezione non deve ridefinire la famiglia}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.9cm] (all) at(2.2,3.6){Quattro contrasti\\$0{,}003;0{,}018;0{,}041;0{,}2$};
\node[pFlow,text width=3.9cm,fill=GeoTint] (adj) at(7.1,3.6){Correggere la famiglia\\primo p corretto: $0{,}012$};
\draw[pEdge](all)--(adj);
\node[pFlow,text width=8.3cm,draw=GeoB] at(4.65,1.4){Se si conservasse solo $0{,}003$, la correzione non rappresenterebbe più le quattro domande esaminate.};
\end{tikzpicture}
\PSmall{L’analisi esplorativa può suggerire nuove domande. La verifica successiva deve riconoscere come le domande sono state selezionate.}
''',rhs(75,"famiglia_completa","nomi e risultati",r"I nomi dei contrasti accompagnano i risultati. Una tabella completa conserva la famiglia e documenta la decisione senza eliminare esiti poco favorevoli."),"La famiglia va definita rispetto alle domande esaminate; filtrare i risultati prima della correzione altera il rischio dichiarato.")

add(76,"Scegliere il confronto a partire dal disegno",
    r"\PLabel{Domanda, struttura delle unità e parametro}"+
    table(["domanda","disegno",r"procedura\\da valutare"],
          [["due medie",r"unità\\indipendenti","Welch"],
           [r"cambiamento\\medio",r"coppie\\indipendenti",r"$t$ sulle differenze"],
           [r"ordinamento\\relativo",r"unità\\indipendenti",r"rank-sum e\\superiorità"],
           ["associazione",r"conteggi\\indipendenti",r"$\chi^2$ o Fisher"],
           ["più medie",r"gruppi\\indipendenti","ANOVA o Welch"]],[3.1,2.9,3.4],.95)+
    r"\PSmall{Prima del calcolo: controllare modello, forma dei dati e famiglia dei confronti.}",
    r'''
\PLabel{Tre verifiche prima del test}
\PBody{1. Quale unità può essere considerata indipendente?}
\vspace{3mm}
\PBody{2. Quale quantità distingue i gruppi e in quale verso?}
\vspace{3mm}
\PBody{3. Quale riferimento descrive la statistica sotto l’ipotesi nulla?}
\PInfo{Misure ripetute, siti o serie possono richiedere modelli che rappresentino la dipendenza. Non basta scegliere un test diverso dalla tabella.}
''',"La struttura dei dati, il parametro e le condizioni del modello determinano il confronto pertinente.")

code(77,"risultato_appaiato",'''
d77 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
z77 <- d77$dopo-d77$prima
t77 <- t.test(z77)
data.frame(n=length(z77),
  stima=mean(z77),lo=t77$conf.int[1],
  hi=t77$conf.int[2],p=t77$p.value)
''')
add(77,"Scrivere una conclusione verificabile",r'''
\PLabel{Esempio sui 24 provini sintetici}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=8.3cm] at(4.65,4.6){Disegno: 24 coppie · contrasto: dopo meno prima};
\node[pFlow,fill=GeoTint,text width=8.3cm] at(4.65,3.05){Cambiamento medio $0{,}03573$ u.c.\\IC 95\% $[0{,}02278;\ 0{,}04868]$ u.c.};
\node[pFlow,text width=8.3cm] at(4.65,1.5){$t=5{,}710$, $df=23$, $p\simeq8{,}17\times10^{-6}$\\riferimento: differenze indipendenti e normali};
\end{tikzpicture}
\PSmall{I dati sostengono un cambiamento medio positivo nel modello adottato. La rilevanza richiede un criterio nelle unità della misura; l’attribuzione causale dipende dal disegno.}
''',rhs(77,"risultato_appaiato","tabella riproducibile",r"La relazione conserva numerosità, verso, unità, stima, intervallo e p-value. Le condizioni del modello e i limiti dell’interpretazione accompagnano i numeri."),"La conclusione deve mantenere la stessa popolazione, lo stesso parametro e le stesse condizioni dell’analisi.")
