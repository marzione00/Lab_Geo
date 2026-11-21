from pathlib import Path
import csv, math

ROOT = Path(__file__).resolve().parent
SLIDES = {}
CODES = {}

def S(n, title, left, right, recall):
    SLIDES[n] = dict(title=title, section="I · DEFINIRE IL CONFRONTO",
                     left=left, right=right, recall=recall)

def code(n, name, value):
    CODES[f"{n:03}_{name}.R"] = value.strip() + "\n"

def rows(name):
    with (ROOT / "root_proof/coordinate" / name).open() as f:
        return [{k: float(v) for k,v in r.items()} for r in csv.DictReader(f)]

def it(x, digits=3):
    return f"{x:.{digits}f}".replace(".", "{,}")

F = rows("fossili_riepilogo.csv")[0]
P = rows("permutazione_riepilogo.csv")[0]

def fossils_plot():
    with (ROOT/"root_proof/Dati/fossili_simulati.csv").open() as f:
        data = list(csv.DictReader(f))
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]",
           r"\draw[pAxis](.45,.5)--(9.35,.5);"]
    for tick in range(4,11):
        x=.65+(tick-3.5)*1.23
        out += [rf"\draw[Muted]({x:.3f},.43)--({x:.3f},.57);",
                rf"\node[pNote] at({x:.3f},.12){{{tick}}};"]
    for group,y,col in [("Rounded",1.5,"GeoA"),("Spiky",3.0,"GeoB")]:
        vals=[float(d["diametro_tot_um"]) for d in data if d["morfotipo"]==group]
        out.append(rf"\node[pNote,text={col},anchor=west] at(.6,{y+.55}){{{group}: 80 fossili}};")
        for j,v in enumerate(vals):
            yy=y+.065*((j*7)%9-4)
            xx=.65+(v-3.5)*1.23
            out.append(rf"\fill[{col},opacity=.65]({xx:.4f},{yy:.4f}) circle(1.05pt);")
        xm=.65+(sum(vals)/len(vals)-3.5)*1.23
        out.append(rf"\draw[{col},line width=1.4pt]({xm:.4f},{y-.37})--({xm:.4f},{y+.37});")
    out += [r"\node[pNote] at(4.8,-.35){Diametro totale ($\mu$m); barre verticali: medie};",
            r"\end{tikzpicture}"]
    return "\n".join(out)

def interval_plot():
    def x(v): return 2.0+6.8*v
    return rf"""
\begin{{tikzpicture}}[x=1cm,y=1cm]
\draw[pAxis](.6,.8)--(9.1,.8);
\foreach \v/\lab in {{-.2/{{-0,2}},0/0,.2/{{0,2}},.4/{{0,4}},.6/{{0,6}},.8/{{0,8}},1/1}}{{
\pgfmathsetmacro{{\xx}}{{2+6.8*\v}}
\draw[Muted](\xx,.72)--(\xx,.88);
\node[pNote] at(\xx,.36){{$\lab$}};}}
\draw[Muted,dashed](2,1.05)--(2,3.5);
\draw[GeoB,line width=2pt]({x(F['inferiore']):.4f},2.1)--({x(F['superiore']):.4f},2.1);
\foreach \xx in {{{x(F['inferiore']):.4f},{x(F['superiore']):.4f}}}
\draw[GeoB,line width=1pt](\xx,1.9)--(\xx,2.3);
\fill[GeoB]({x(F['differenza']):.4f},2.1) circle(3pt);
\node[pLabel] at(5.2,3.2){{$\widehat\Delta={it(F['differenza'])}\ \mu\mathrm m$}};
\node[pNote] at(5.0,-.15){{Spiky meno Rounded ($\mu$m)}};
\end{{tikzpicture}}
"""

def perm_hist():
    out=[r"\begin{tikzpicture}[x=1cm,y=1cm]",
         r"\draw[pAxis](.6,.5)--(9.2,.5);"]
    for r in rows("istogramma_permutazioni.csv"):
        x1=.8+(r["sinistra"]+1.6)*2.5
        x2=.8+(r["destra"]+1.6)*2.5
        y=.5+r["conteggio"]*.055
        out.append(rf"\draw[GeoA!70,fill=GeoA!27]({x1:.3f},.5) rectangle({x2:.3f},{y:.3f});")
    for t in [-1.2,-.6,0,.6,1.2]:
        x=.8+(t+1.6)*2.5
        out.append(rf"\node[pNote] at({x:.3f},.13){{$ {it(t,1)} $}};")
    for t in [-abs(P["osservato"]), abs(P["osservato"])]:
        x=.8+(t+1.6)*2.5
        out.append(rf"\draw[GeoB,line width=1.2pt]({x:.4f},.5)--({x:.4f},3.55);")
    out += [r"\node[pNote] at(4.8,4.0){200 permutazioni; altezza = frequenza};",
            r"\node[pNote] at(4.8,-.35){Contrasto permutato B meno A};",
            r"\end{tikzpicture}"]
    return "\n".join(out)

code(3, "avvio", '''
# Aprire Gemina_M06.Rproj.
source("setup.R", encoding="UTF-8")
# Dati sintetici del corso
f03 <- read.csv(
  "Dati/fossili_simulati.csv")
head(f03)
# Documentazione del test per medie
help("t.test")
''')
S(3, "Dalla stima al confronto con un’ipotesi", r"""
\PLabel{Il passaggio da Pelago a Gemina}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (d) at(2.2,3.4){\textbf{Disegno e dati}\\unità, variabile, gruppi};
\node[pFlow,text width=3.7cm] (s) at(7.2,3.4){\textbf{Stima del contrasto}\\effetto e intervallo};
\node[pFlow,text width=3.7cm] (h) at(2.2,1.1){\textbf{Ipotesi nulla}\\riferimento dichiarato};
\node[pFlow,text width=3.7cm] (t) at(7.2,1.1){\textbf{Confronto statistico}\\risultati estremi sotto $H_0$};
\draw[pEdge](d)--(s);\draw[pEdge](h)--(t);\draw[pEdge](s)--(t);
\end{tikzpicture}
\PBody{Pelago ha introdotto stima e incertezza. Qui aggiungiamo un riferimento nullo, conservando la domanda scientifica e le ipotesi sul campione.}
""", r"""
\PCode{R · avviare il progetto}{003_avvio.R}
\PSmall{Il file completo \texttt{Lezione\_Gemina.R} raccoglie i frammenti nell’ordine della presentazione.}
\PInfo{Prerequisiti: vettori, tabelle, media, varianza, errore standard e intervalli di confidenza.}
""", "Il confronto statistico riguarda un parametro e un disegno espliciti. Stima e incertezza restano parte della conclusione.")

code(4, "domanda", '''
# Una riga = un fossile sintetico.
f04 <- read.csv(
  "Dati/fossili_simulati.csv")
stopifnot(!anyDuplicated(f04$id))
table(f04$morfotipo)
summary(f04$diametro_tot_um)
# um nel nome indica micrometri.
''')
S(4, "Precisare la domanda prima del calcolo", r"""
\PLabel{Un esempio che attraversa il modulo}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \y/\tit/\val in {
4.2/{Popolazioni}/{Fossili dei due morfotipi},
2.95/{Unità}/{Un fossile identificato},
1.7/{Risposta}/{Diametro totale in micrometri},
.45/{Parametro}/{Media Spiky meno media Rounded}}{
\node[pLabel,anchor=west,text width=2.8cm,align=left] at(.25,\y){\textbf{\tit}};
\node[pFlow,text width=5.7cm,minimum height=.85cm] at(6.15,\y){\val};
}
\end{tikzpicture}
\PSmall{Il file del corso contiene 160 fossili sintetici: 80 Rounded e 80 Spiky. Non sono osservazioni raccolte sul terreno.}
""", r"""
\PCode{R · controllare unità e gruppi}{004_domanda.R}
\PSmall{\texttt{table()} conta le osservazioni per gruppo. L’identificativo serve a riconoscere duplicati e abbinamenti.}
\PInfo{L’indipendenza deriva dal disegno. Un identificativo diverso per ogni riga, da solo, non la dimostra.}
""", "Una domanda completa specifica popolazioni, unità, variabile, unità di misura e caratteristica da confrontare.")

code(5, "contrasto", '''
# Ordine dichiarato: Spiky-Rounded.
f05 <- read.csv(
  "Dati/fossili_simulati.csv")
g05 <- split(f05$diametro_tot_um,
             f05$morfotipo)
d05 <- mean(g05$Spiky) -
       mean(g05$Rounded)
d05  # micrometri
''')
S(5, "Il contrasto ha un ordine e un’unità", r"""
\PLabel{Parametro e stima}
\[
\Delta=\mu_B-\mu_A,\qquad
\widehat\Delta=\bar y_B-\bar y_A.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,fill=GeoA!8,text width=3.0cm] (a) at(2.0,2.7){Gruppo A\\$\mu_A$};
\node[pFlow,fill=GeoB!8,text width=3.0cm] (b) at(7.2,2.7){Gruppo B\\$\mu_B$};
\draw[pEdge](a.east)--node[above,pLabel]{$B-A$}(b.west);
\node[pLabel,text width=8.6cm] at(4.6,.85){$\Delta>0$: media di B maggiore\\$\Delta<0$: media di A maggiore};
\end{tikzpicture}
\PSmall{$\mu_g$ è la media della popolazione $g$; $\bar y_g$ è la media del campione. Il contrasto mantiene l’unità della variabile.}
""", r"""
\PCode{R · differenza fra due medie}{005_contrasto.R}
\PSmall{\texttt{split()} separa i diametri per morfotipo. Si sottraggono le medie, senza appaiare fossili appartenenti a gruppi indipendenti.}
\PInfo{Nel caso del corso: $A=$ Rounded, $B=$ Spiky; $\Delta$ è espresso in $\mu$m.}
""", "Il segno descrive una direzione convenzionale. Va dichiarato prima di leggere stima, intervallo e risultato del test.")

code(6, "segno", '''
# Dati costruiti, in micrometri
a06 <- c(4, 5, 6)
b06 <- c(6, 7, 8)
mean(b06)-mean(a06)  # +2 um
mean(a06)-mean(b06)  # -2 um
# Cambio di unita: um -> mm
(mean(b06)-mean(a06))/1000
''')
S(6, "Cambiare segno o unità cambia la lettura", r"""
\PLabel{La stessa differenza, due rappresentazioni}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,2.65)--(9.2,2.65);
\foreach \x/\v in {1.0/4,2.9/5,4.8/6,6.7/7,8.6/8}{
\draw[Muted](\x,2.56)--(\x,2.74);
\node[pNote] at(\x,2.3){$\v$};}
\fill[GeoA](2.9,2.65) circle(3pt);
\fill[GeoB](6.7,2.65) circle(3pt);
\node[pLabel,text=GeoA] at(2.9,3.25){$\bar y_A=5$};
\node[pLabel,text=GeoB] at(6.7,3.25){$\bar y_B=7$};
\draw[pEdge,GeoB](2.9,1.65)--node[below,pLabel]{$B-A=+2\ \mu$m}(6.7,1.65);
\draw[pEdge,GeoA](6.7,.5)--node[below,pLabel]{$A-B=-2\ \mu$m}(2.9,.5);
\end{tikzpicture}
\PSmall{Convertendo da $\mu$m a mm, $2\ \mu$m diventano $0{,}002$ mm. Anche errore standard e limiti dell’intervallo vanno convertiti.}
""", r"""
\PCode{R · mantenere coerente il contrasto}{006_segno.R}
\PSmall{Il test bilaterale restituisce lo stesso $p$ invertendo i gruppi. Il segno della statistica cambia e l’intervallo si riflette rispetto a zero.}
\PInfo{Se $IC_{B-A}=[L,U]$, allora $IC_{A-B}=[-U,-L]$.}
""", "La direzione della sottrazione e l’unità devono restare coerenti in codice, grafici e relazione.")

code(7, "disegno", '''
# Esempio di misure ripetute
d07 <- data.frame(
  provino=rep(1:4, each=2),
  tempo=rep(c("prima","dopo"),4))
nrow(d07)                  # 8 righe
length(unique(d07$provino)) # 4 coppie
table(d07$provino, d07$tempo)
''')
S(7, "Il disegno stabilisce le unità indipendenti", r"""
\PLabel{Tre strutture da riconoscere}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel] at(1.6,4.5){Indipendenti};
\node[pLabel] at(4.8,4.5){Appaiati};
\node[pLabel] at(8.0,4.5){Raggruppati};
\foreach \y in {1.3,2.25,3.2}{
\node[pDotA] at(1.1,\y){};
\node[pDotB] at(2.1,\y+.25){};
\node[pDotA] at(4.25,\y){};
\node[pDotB] at(5.35,\y+.25){};
\draw[Muted](4.35,\y)--(5.25,\y+.25);
}
\foreach \y in {1.2,2.9}{
\draw[pGroup](6.9,\y-.6) rectangle(9.1,\y+.6);
\foreach \x in {7.35,8,8.65}\node[pDotC] at(\x,\y){};
}
\node[pNote,text width=2.7cm] at(1.6,.25){unità distinte\\nei due gruppi};
\node[pNote,text width=2.7cm] at(4.8,.25){due misure\\sulla stessa unità};
\node[pNote,text width=2.7cm] at(8,.25){più osservazioni\\per sito o provino};
\end{tikzpicture}
\PSmall{Le linee indicano legami del disegno. I gruppi di osservazioni dello stesso sito possono condividere condizioni ambientali.}
""", r"""
\PCode{R · contare righe e coppie}{007_disegno.R}
\PSmall{Il numero di righe è 8; le unità con una misura prima e una dopo sono 4. Nel test appaiato $n$ conta coppie complete.}
\PInfo{Un test per campioni indipendenti richiede una giustificazione dell’indipendenza fra le unità utilizzate.}
""", "L’unità di analisi dipende dal prelievo e dagli abbinamenti. Contare le righe non basta a determinare la numerosità informativa.")

code(8, "punti", '''
f08 <- read.csv(
  "Dati/fossili_simulati.csv")
stripchart(diametro_tot_um ~ morfotipo,
 data=f08, method="stack", pch=16,
 col=c("#1D7890","#C57E42"),
 xlab="Diametro totale (um)")
tapply(f08$diametro_tot_um,
       f08$morfotipo, mean)
''')
S(8, "Osservare tutti i valori dei due gruppi",
  r"\PLabel{Diametri sintetici del corso}"+fossils_plot()+r"""
\PSmall{Ogni punto rappresenta un fossile. Lo spostamento verticale rende visibili le sovrapposizioni; l’altezza dei punti non è una seconda variabile.}
""", r"""
\PCode{R · distribuzioni e medie}{008_punti.R}
\PSmall{Il codice impila i punti sovrapposti. Si osservano dispersione, asimmetria e valori estremi.}
\PInfo{I valori individuali permettono di valutare quanto la media rappresenti il gruppo.}
""", "Il grafico dei dati precede l’interpretazione del test e permette di riconoscere aspetti che una media da sola non descrive.")

code(9, "medie_individui", '''
f09 <- read.csv(
  "Dati/fossili_simulati.csv")
g09 <- split(f09$diametro_tot_um,
             f09$morfotipo)
mean(g09$Spiky)-mean(g09$Rounded)
# Tutti i confronti fra individui
mean(outer(g09$Spiky,
           g09$Rounded, ">"))
''')
S(9, "Medie diverse e individui sovrapposti", rf"""
\PLabel{{Due quantità rispondono a domande diverse}}
\begin{{tikzpicture}}[x=1cm,y=1cm]
\node[pFlow,text width=7.9cm,minimum height=1.15cm] at(4.7,3.7)
{{Differenza delle medie\\$\widehat\Delta={it(F['differenza'])}\ \mu\mathrm m$}};
\node[pFlow,text width=7.9cm,minimum height=1.15cm] at(4.7,1.8)
{{Quota di confronti con Spiky maggiore\\$\widehat P(S>R)={it(F['superiorita'])}$}};
\end{{tikzpicture}}
\PBody{{Una differenza media positiva può accompagnarsi a molti individui Rounded più grandi di alcuni Spiky.}}
\PSmall{{Qui non ci sono pareggi. Per la probabilità di superiorità con pareggi assegneremo metà contributo a ciascuna uguaglianza.}}
""", r"""
\PCode{R · medie e confronti individuali}{009_medie_individui.R}
\PSmall{\texttt{outer()} confronta ciascuno degli 80 Spiky con ciascuno degli 80 Rounded: $80\times80=6400$ confronti.}
\PInfo{I 6400 confronti condividono gli stessi 160 individui. Non costituiscono 6400 osservazioni indipendenti.}
""", "Una differenza fra medie non separa necessariamente gli individui. La probabilità di superiorità è un altro parametro.")

code(10, "intervallo", '''
f10 <- read.csv(
  "Dati/fossili_simulati.csv")
g10 <- split(f10$diametro_tot_um,
             f10$morfotipo)
tt10 <- t.test(g10$Spiky,
 g10$Rounded, var.equal=FALSE)
tt10$conf.int  # IC bilaterale 95%
tt10$stderr    # errore standard
''')
S(10, "Accompagnare l’effetto con l’incertezza",
  r"\PLabel{Intervallo di Welch per la differenza}"+interval_plot()+rf"""
\PSmall{{Nel caso dei fossili: $IC_{{95\%}}=[{it(F['inferiore'])};{it(F['superiore'])}]\ \mu$m e $SE={it(F['se'])}\ \mu$m. La derivazione di Welch inizia alla slide 37.}}
""", r"""
\PCode{R · estrarre intervallo e SE}{010_intervallo.R}
\PSmall{La copertura del 95\% riguarda il procedimento nelle ripetizioni previste dal modello. L’intervallo ottenuto riguarda il contrasto fra medie.}
\PInfo{L’interpretazione richiede unità indipendenti e condizioni adeguate per l’approssimazione del metodo.}
""", "La stima indica la differenza osservata; l’intervallo ne descrive l’incertezza secondo il modello e il disegno dichiarati.")

code(11, "ipotesi", '''
# Domanda fissata prima dei dati:
# H0: media_B-media_A = 0.
a11 <- c(3, 4, 6, 7, 9)
b11 <- c(4, 6, 7, 8, 10)
t.test(b11, a11, mu=0,
       alternative="two.sided")
# "greater" richiede H1: Delta>0.
''')
S(11, "Dichiarare ipotesi e direzione del confronto", r"""
\PLabel{Una differenza di medie come parametro}
\[
H_0:\Delta=\Delta_0,\qquad \Delta_0=0
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=4.0cm] at(2.3,2.75){Bilaterale\\$H_1:\Delta\ne0$};
\node[pFlow,text width=4.0cm] at(7.2,2.75){Unilaterale superiore\\$H_1:\Delta>0$};
\draw[pAxis](.6,.9)--(4.15,.9);
\draw[pAxis](5.45,.9)--(9,.9);
\foreach \x in {2.3,7.2}{
\draw[Muted](\x,.75)--(\x,1.05);
\node[pNote] at(\x,.45){0};}
\draw[GeoA,line width=1.5pt,-{Latex}](2.1,1.45)--(.9,1.45);
\draw[GeoA,line width=1.5pt,-{Latex}](2.5,1.45)--(3.7,1.45);
\draw[GeoB,line width=1.5pt,-{Latex}](7.35,1.45)--(8.65,1.45);
\end{tikzpicture}
\PSmall{La direzione dipende dalla domanda. Le condizioni sulla distribuzione e sul disegno completano il modello sotto cui il test è calibrato.}
""", r"""
\PCode{R · specificare l’alternativa}{011_ipotesi.R}
\PSmall{\texttt{mu=0} indica il contrasto ipotizzato. Con \texttt{t.test(b,a)}, \texttt{"greater"} si riferisce alla media di B maggiore di quella di A.}
\PInfo{Scegliere una coda dopo aver osservato il segno modifica la procedura e il suo controllo dell’errore.}
""", "Il valore nullo, la direzione e il metodo si definiscono prima di usare il risultato per sostenere una conclusione.")

code(12, "etichette", '''
# Valori fissi, etichette mobili
x12 <- c(1, 2, 4, 7)
g12 <- c("A","A","B","B")
set.seed(17)
gp12 <- sample(g12)
data.frame(valore=x12,
 originale=g12, permutato=gp12)
table(gp12) # 2 per gruppo
''')
S(12, "Quando le etichette sono scambiabili", r"""
\PLabel{La giustificazione della permutazione}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \x/\v/\g/\col in {1.3/1/A/GeoA,3.6/2/A/GeoA,5.9/4/B/GeoB,8.2/7/B/GeoB}{
\node[pFlow,text width=1.3cm,minimum height=.8cm] at(\x,3.55){$\v$};
\node[pFlow,fill=\col!10,text width=1.3cm,minimum height=.65cm] at(\x,2.3){\g};
}
\draw[decorate,decoration={brace,amplitude=5pt},Classical](.55,1.55)--(8.95,1.55);
\node[pNote,text width=8.3cm] at(4.75,.6){Si conservano valori e numerosità;\\si riassegnano le etichette A e B.};
\end{tikzpicture}
\PBody{Per campioni IID dalla stessa distribuzione, sotto $H_0$ le etichette non distinguono i valori. Anche una randomizzazione nota può fornire le assegnazioni ammesse.}
""", r"""
\PCode{R · riassegnare i gruppi}{012_etichette.R}
\PSmall{\texttt{sample(g12)} riordina il vettore senza rimpiazzo: restano due A e due B.}
\PInfo{L’uguaglianza delle sole medie non assicura la scambiabilità se cambiano dispersione o forma. La permutazione libera va giustificata.}
""", "La validità di una permutazione deriva dalle assegnazioni ammesse dal modello o dal disegno, non dalla disponibilità del comando sample().")

code(13, "sei_assegnazioni", '''
x13 <- c(1, 2, 4, 7)
# Scegliere 2 dei 4 indici per A.
i13 <- combn(4, 2)
t13 <- apply(i13, 2, function(i) {
  mean(x13[-i])-mean(x13[i])
})
t13
mean(abs(t13) >= 4) # 2/6 esatto
''')
S(13, "Quattro valori, sei assegnazioni distinte", r"""
\PLabel{Enumerare tutto il riferimento}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \x/\y/\aa/\bb/\tt in {
1.6/3.3/{1,2}/{4,7}/{+4},
4.8/3.3/{1,4}/{2,7}/{+2},
8.0/3.3/{1,7}/{2,4}/{-1},
1.6/1.2/{2,4}/{1,7}/{+1},
4.8/1.2/{2,7}/{1,4}/{-2},
8.0/1.2/{4,7}/{1,2}/{-4}}{
\node[pFlow,text width=2.6cm,minimum height=1.5cm] at(\x,\y)
{A: $\aa$\\B: $\bb$\\$\bar y_B-\bar y_A=\tt$};
}
\end{tikzpicture}
\[
N=\binom42=6,\qquad p_{\mathrm{esatto}}=\frac26
\quad\text{per }|T_{\mathrm{oss}}|=4.
\]
\PSmall{Ogni assegnazione ha lo stesso peso sotto il riferimento dichiarato. Si contano entrambe le direzioni.}
""", r"""
\PCode{R · tutte le combinazioni}{013_sei_assegnazioni.R}
\PSmall{\texttt{combn(4,2)} elenca i possibili indici di A. Il segno meno in \texttt{x13[-i]} seleziona gli indici rimasti per B.}
\PInfo{Questa è un’enumerazione completa. La formula Monte Carlo con $+1$ servirà quando estraiamo soltanto un insieme di permutazioni.}
""", "Un riferimento esatto può essere costruito enumerando tutte le assegnazioni ammesse e contando i risultati almeno altrettanto estremi.")

code(14, "una_permutazione", '''
x14 <- c(1, 2, 4, 7)
g14 <- c("A","A","B","B")
# Una riassegnazione ammessa
gp14 <- g14[c(1, 4, 2, 3)]
diff(tapply(x14, g14, mean))  # 4
diff(tapply(x14, gp14, mean)) # 2
# Per un riordino casuale:
sample(g14)
''')
S(14, "Seguire una singola riassegnazione", r"""
\PLabel{Valori invariati, appartenenza diversa}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \x/\v/\g/\gp in {1.3/1/A/A,3.6/2/A/B,5.9/4/B/A,8.2/7/B/B}{
\node[pLabel] at(\x,4.3){$\v$};
\node[pFlow,text width=1.3cm,minimum height=.7cm] at(\x,3.2){\g};
\node[pFlow,text width=1.3cm,minimum height=.7cm,fill=GeoTint] at(\x,1.5){\gp};
}
\foreach \x in {1.3,3.6,5.9,8.2}\draw[pEdge](\x,2.8)--(\x,1.9);
\node[pNote] at(4.75,.5){Prima: $T=4$\qquad Dopo: $T=2$};
\end{tikzpicture}
\PSmall{Nel secondo assetto A contiene 1 e 4, B contiene 2 e 7. Si applica la stessa statistica a una diversa assegnazione.}
""", r"""
\PCode{R · ricalcolare la statistica}{014_una_permutazione.R}
\PSmall{\texttt{tapply()} calcola le medie seguendo i gruppi. Con i nomi A e B, \texttt{diff()} restituisce B meno A.}
\PInfo{Mantenere una statistica e un ordine fissi evita che il significato del confronto cambi fra le permutazioni.}
""", "La permutazione modifica le etichette; la regola di calcolo del contrasto rimane identica.")

code(15, "molte_permutazioni", '''
set.seed(17)
x15 <- c(rnorm(20),rnorm(20,.6))
g15 <- rep(0:1, each=20)
obs15 <- diff(tapply(x15,g15,mean))
B15 <- 200
t15 <- replicate(B15, {
 gp <- sample(g15)
 diff(tapply(x15,gp,mean))
})
''')
S(15, "Ripetere la riassegnazione delle etichette",
  r"\PLabel{Il generatore del laboratorio di permutazione}"+perm_hist()+rf"""
\PSmall{{Campione: 20 osservazioni per gruppo, risposta senza unità fisica. Con seme 17 e $\Delta=0{{,}}6$, il contrasto osservato è $ {it(P['osservato'])}$. Le linee indicano $\pm|T_{{\mathrm{{oss}}}}|$.}}
""", r"""
\PCode{R · 200 contrasti sotto il riferimento}{015_molte_permutazioni.R}
\PSmall{\texttt{replicate()} cambia le etichette dei 40 valori generati una sola volta.}
\PInfo{Parametro e stima possono avere segni diversi in un singolo campione.}
""", "Le permutazioni descrivono il riferimento condizionato ai dati osservati. Aumentarle non aggiunge nuove osservazioni al campione.")

code(16, "estremita", '''
# Oggetti della slide 15
soglia16 <- abs(obs15)
estremi16 <- abs(t15) >= soglia16
K16 <- sum(estremi16)
K16  # 66 dei 200 contrasti
sum(t15 <= -soglia16) +
  sum(t15 >= soglia16)
''')
S(16, "Definire ciò che conta come estremo", rf"""
\PLabel{{Confronto bilaterale della differenza}}
\begin{{tikzpicture}}[x=1cm,y=1cm]
\fill[GeoB!15](.65,1.2) rectangle(3.25,2.45);
\fill[GeoB!15](6.35,1.2) rectangle(8.95,2.45);
\draw[pAxis](.45,1.2)--(9.2,1.2);
\draw[GeoB,line width=1pt](3.25,1.2)--(3.25,2.7);
\draw[GeoB,line width=1pt](6.35,1.2)--(6.35,2.7);
\node[pLabel] at(1.9,3.5){{$T_b\le-|T_{{\rm oss}}|$}};
\node[pLabel] at(7.6,3.5){{$T_b\ge|T_{{\rm oss}}|$}};
\node[pNote] at(3.25,.7){{$-{it(abs(P['osservato']))}$}};
\node[pNote] at(6.35,.7){{$+{it(abs(P['osservato']))}$}};
\node[pNote] at(4.8,.7){{0}};
\node[pLabel] at(4.8,.05){{$|T_b|\ge|T_{{\rm oss}}|$}};
\end{{tikzpicture}}
\PSmall{{Schema della regola, asse non in scala. Nel campione precedente $ {int(P['K'])}$ dei $ {int(P['B'])}$ contrasti permutati raggiungono o superano la soglia.}}
""", r"""
\PCode{R · contare entrambe le code}{016_estremita.R}
\PSmall{\texttt{abs()} elimina il segno; \texttt{>=} include anche le uguaglianze. La somma dei valori logici conta i risultati che soddisfano la regola.}
\PInfo{Una regola di estremità deve essere fissata e applicata allo stesso modo al dato osservato e a tutte le riassegnazioni.}
""", "Nel confronto bilaterale con differenza di medie sono estremi i contrasti grandi in valore assoluto, in entrambe le direzioni.")

code(17, "p_monte_carlo", '''
# Correzione per permutazioni estratte
p17 <- (1+K16)/(B15+1)
p17
# Risoluzione: caso di zero estremi
1/(B15+1)
data.frame(B=c(200,1000),
 minimo=1/(c(200,1000)+1))
''')
S(17, "Il p-value Monte Carlo e la risoluzione", rf"""
\PLabel{{Un conteggio finito di permutazioni}}
\[
p_{{MC}}=\frac{{1+\sum_{{b=1}}^B
\mathbf1(|T_b|\ge|T_{{\mathrm{{oss}}}}|)}}{{B+1}}
=\frac{{1+{int(P['K'])}}}{{{int(P['B'])}+1}}={it(P['p_MC'])}.
\]
\begin{{tikzpicture}}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (k) at(2.2,2.4){{$K$ risultati estremi\\fra $B$ permutazioni}};
\node[pFlow,text width=3.7cm] (p) at(7.1,2.4){{$p_{{MC}}\ge1/(B+1)$\\mai zero}};
\draw[pEdge](k)--(p);
\node[pNote,text width=8.5cm] at(4.7,.8){{$B=200$: minimo $1/201\approx0{{,}}00498$\\$B=1000$: minimo $1/1001\approx0{{,}}00100$}};
\end{{tikzpicture}}
\PSmall{{$B$ conta permutazioni estratte; $K$ conta quelle almeno altrettanto estreme. La validità richiede il riferimento di permutazione già giustificato.}}
""", r"""
\PCode{R · calcolare senza restituire zero}{017_p_monte_carlo.R}
\PSmall{Aumentando $B$ si raffina il calcolo sullo stesso campione. La variazione Monte Carlo va distinta dalla variabilità fra nuovi campioni.}
\PInfo{Con permutazioni indipendenti, $q$ è la probabilità di coda nel riferimento fissato; l’errore Monte Carlo ha scala circa $\sqrt{q(1-q)/B}$.}
""", "Nessun estremo osservato in un insieme finito di permutazioni non equivale a probabilità nulla.")

code(18, "bootstrap_permutazione", '''
a18 <- c(1,2,4,5)
b18 <- c(3,5,6,8)
set.seed(17)
# Bootstrap entro ciascun gruppo
mean(sample(b18,4,replace=TRUE)) -
 mean(sample(a18,4,replace=TRUE))
# Permutazione: valori fissi
sample(rep(c("A","B"), each=4))
''')
S(18, "Bootstrap e permutazione hanno scopi diversi", r"""
\PLabel{Quali elementi cambiano?}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm,fill=GeoA!6] at(2.2,3.9){\textbf{Bootstrap}\\stima dell’incertezza};
\node[pFlow,text width=3.7cm,fill=GeoB!6] at(7.1,3.9){\textbf{Permutazione}\\riferimento sotto $H_0$};
\node[pLabel,text width=3.7cm] at(2.2,2.35){Ricampionare con\\rimpiazzo entro A e B};
\node[pLabel,text width=3.7cm] at(7.1,2.35){Riassegnare le etichette\\ai valori osservati};
\draw[pEdge](2.2,1.8)--(2.2,1.2);
\draw[pEdge](7.1,1.8)--(7.1,1.2);
\node[pNote,text width=3.8cm] at(2.2,.55){I valori possono ripetersi\\o non comparire};
\node[pNote,text width=3.8cm] at(7.1,.55){Ogni valore compare\\una volta per riassegnazione};
\end{tikzpicture}
\PSmall{Gli schemi mostrati assumono unità indipendenti. Entrambi i procedimenti devono rispettare il disegno.}
""", r"""
\PCode{R · riconoscere le operazioni}{018_bootstrap_permutazione.R}
\PSmall{\texttt{replace=TRUE} permette ripetizioni nel bootstrap. Per la permutazione delle etichette, il valore predefinito è \texttt{FALSE}.}
\PInfo{Il bootstrap ordinario della differenza non impone automaticamente il contrasto nullo. I due riferimenti non sono intercambiabili.}
""", "Prima di ricampionare occorre precisare se interessa l’incertezza della stima oppure un riferimento sotto l’ipotesi nulla.")

code(19, "vincoli", '''
# Quattro differenze appaiate
d19 <- c(.4, -.2, .7, .5)
set.seed(17)
# Scambio delle due etichette
# soltanto entro ciascuna coppia.
s19 <- sample(c(-1,1), 4,
              replace=TRUE)
mean(s19*d19)
''')
S(19, "Conservare i vincoli del disegno", r"""
\PLabel{Permutazioni ammesse e unità dell’assegnazione}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \x/\id in {1.7/1,4.8/2,7.9/3}{
\draw[pGroup](\x-1.2,.9) rectangle(\x+1.2,4.1);
\node[pLabel] at(\x,3.6){Coppia \id};
\node[pFlow,fill=GeoA!8,text width=.65cm,minimum height=.6cm] at(\x-.55,2.4){A};
\node[pFlow,fill=GeoB!8,text width=.65cm,minimum height=.6cm] at(\x+.55,2.4){B};
\draw[Classical,<->,line width=1pt](\x-.7,1.5)--(\x+.7,1.5);
}
\end{tikzpicture}
\PSmall{Nelle coppie si può scambiare A e B entro la stessa unità se la randomizzazione lo consente o se il modello nullo giustifica il cambio di segno.}
""", r"""
\PCode{R · una trasformazione entro coppia}{019_vincoli.R}
\PSmall{Moltiplicare $D_i=B_i-A_i$ per $-1$ equivale a invertire A e B nella coppia.}
\PInfo{Per dati osservazionali il cambio di segno richiede, per esempio, differenze indipendenti e simmetriche attorno a zero sotto $H_0$.}
""", "Coppie, siti e blocchi limitano le trasformazioni ammesse. Una permutazione libera può distruggere la struttura da cui dipende la validità del test.")
