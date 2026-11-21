from pathlib import Path
import math
SLIDES={}
CODES={}
ROOT=Path(__file__).resolve().parent
def S(n,title,left,right,recall):
    SLIDES[n]=dict(title=title,section='POPOLAZIONI E PARAMETRI' if n<16 else 'SELEZIONE E DISTORSIONE',left=left,right=right,recall=recall)
def code(n,name,s):
    CODES[f'{n:03}_{name}.R']=s.strip()+'\n'
def density(mu,sd,h=2.7):
    return ' '.join(f'({.6+8*k/180:.5f},{.2+h*math.exp(-.5*((8+3*k/180-mu)/sd)**2):.5f})' for k in range(181))

code(3,'avvio','''# Aprire Pelago_M05.Rproj.
source("setup.R", encoding="UTF-8")
# Dati sintetici del corso
head(fossili)
head(provini)
# Argomenti e documentazione
args(mean)
help("sample")
''')
S(3,'Dal modello ai campioni possibili',r'''
\PLabel{Il passaggio da Aurea a Pelago}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (p) at(2,3.3){\textbf{Popolazione e disegno}\\quali unità possono entrare?};
\node[pFlow,text width=3.5cm] (s) at(7.1,3.3){\textbf{Campioni possibili}\\ripetizioni del prelievo};
\node[pFlow,text width=3.5cm] (o) at(2,1.05){\textbf{Campione osservato}\\una realizzazione};
\node[pFlow,text width=3.5cm] (t) at(7.1,1.05){\textbf{Stime possibili}\\variabilità fra campioni};
\draw[pEdge](p)--(s);\draw[pEdge](p)--(o);\draw[pEdge](s)--(t);
\end{tikzpicture}
\PBody{Aurea ha introdotto distribuzioni e simulazione. Qui studiamo le proprietà di una stima quando cambia il campione.}
''',r'''
\PCode{R · progetto della lezione}{003_avvio.R}
\PSmall{Dati, nove funzioni di laboratorio e codice seguono l'ordine delle slide. File completo: \texttt{Lezione\_Pelago.R}.}
\PInfo{Prerequisiti: vettori, media, deviazione standard, probabilità e \texttt{replicate()}.}
''','Una stima dipende sia dai valori osservati sia dal modo in cui il campione è stato raccolto.')

code(4,'popolazione','''# Popolazione finita costruita
U04 <- data.frame(
  id=1:12,
  valore=seq(2.1,3.2,by=.1))
set.seed(17)
i04 <- sample(U04$id, size=4)
U04[i04, ]        # un campione
mean(U04$valore)  # media nota qui
''')
S(4,'Popolazione, lista di selezione e campione',r'''
\PLabel{Tre insiemi da distinguere}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pGroup,fill=GeoTint](.2,.1) rectangle(9.3,4.4);
\node[pLabel,anchor=west] at(.55,4){Popolazione di interesse};
\draw[pGroup](.6,.45) rectangle(6.7,3.45);
\node[pNote,anchor=west] at(.9,3.1){Lista delle unità raggiungibili};
\foreach \x/\y in {1.3/1.1,2.5/1.1,3.7/1.1,4.9/1.1,6.1/1.1,1.3/2.2,2.5/2.2,3.7/2.2,4.9/2.2,6.1/2.2}
\node[pDotA] at(\x,\y){};
\foreach \x/\y in {1.3/1.1,3.7/2.2,4.9/1.1,6.1/2.2}
\draw[GeoB,line width=1.1pt](\x,\y) circle(.19);
\node[pLabel,text width=1.8cm] at(8,2.1){unità\\escluse\\dalla lista};
\node[pNote,text=GeoB] at(4.6,-.35){cerchi: unità selezionate};
\end{tikzpicture}
\PSmall{Schema di appartenenza. Le unità escluse dalla lista restano senza osservazioni anche quando il prelievo dalla lista è casuale.}
''',r'''
\PCode{R · selezione da una lista completa}{004_popolazione.R}
\PSmall{Qui conosciamo tutta la popolazione finita. In una ricerca reale la lista può contenere gli identificativi senza riportare ancora i valori della variabile.}
\PInfo{Prima del prelievo: area, periodo, tipo di unità, criteri di inclusione e lista da cui si seleziona.}
''','La popolazione di interesse e l’insieme delle unità effettivamente selezionabili possono essere diversi.')

code(5,'unita','''# Tre stazioni con quattro misure
d05 <- data.frame(
 stazione=rep(c("A","B","C"),each=4),
 misura=c(2.3,2.4,2.5,2.4,
          2.6,2.7,2.6,2.5,
          2.8,2.9,2.7,2.8))
G05 <- length(unique(d05$stazione))
c(righe=nrow(d05),stazioni=G05)
''')
S(5,'Una stazione può fornire più osservazioni',r'''
\PLabel{Il livello del prelievo}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\lab/\col in {1.6/A/GeoA,4.7/B/GeoB,7.8/C/GeoC}{
\draw[pGroup,fill=\col!7](\xx-1.3,.35) rectangle(\xx+1.3,3.7);
\node[pLabel] at(\xx,3.2){Stazione \lab};
\foreach \yy in {1,1.65,2.3}\node[circle,fill=\col,inner sep=2pt] at(\xx-.45,\yy){};
\node[circle,fill=\col,inner sep=2pt] at(\xx+.45,1.65){};
}
\node[pNote] at(4.7,-.2){3 stazioni, 4 misure per stazione};
\end{tikzpicture}
\PBody{Vicinanza e storia comune possono rendere simili le misure della stessa stazione. Il numero di righe descrive solo una parte del disegno.}
''',r'''
\PCode{R · righe e unità di prelievo}{005_unita.R}
\PSmall{Valori costruiti per l'esempio.}
\PInfo{$G$: numero di stazioni.\\$n_g$: misure nella stazione $g$.\\$n=\sum_g n_g$: osservazioni totali.}
''','La dipendenza fra osservazioni richiede di conservare gli identificativi delle unità a cui appartengono.')

code(6,'stimatore','''# Modello didattico con media nota
mu06 <- 10
set.seed(17)
x06 <- rnorm(6,mean=mu06,sd=2)
mean(x06)  # stima ottenuta dai dati
# La regola vale per ogni campione.
stimatore06 <- function(x) mean(x)
stimatore06(x06)
''')
S(6,'Parametro, stimatore e stima osservata',r'''
\PLabel{Prima e dopo l'osservazione}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=2.5cm] (f) at(1.7,3){Popolazione\\$F$};
\node[pFlow,text width=3.8cm] (th) at(6.8,3){Parametro\\$\theta=T(F)$};
\node[pFlow,text width=2.5cm] (x) at(1.7,.9){Campione aleatorio\\$X_1,\ldots,X_n$};
\node[pFlow,text width=3.8cm] (t) at(6.8,.9){Stimatore\\$\widehat\theta=T_n(X_1,\ldots,X_n)$};
\draw[pEdge](f)--(th);\draw[pEdge](f)--(x);\draw[pEdge](x)--(t);
\end{tikzpicture}
\[
X_i=x_i\quad\Longrightarrow\quad
\widehat\theta_{\mathrm{oss}}=T_n(x_1,\ldots,x_n).
\]
\PSmall{Il parametro resta fisso. Lo stimatore varia fra campioni. La stima osservata è il valore calcolato.}
''',r'''
\PCode{R · una regola e un risultato}{006_stimatore.R}
\PSmall{Qui $\mu=10$ è noto perché generiamo i dati. \texttt{x06} contiene un campione e produce una stima.}
\PInfo{Maiuscole per variabili aleatorie, minuscole per valori osservati. L'asterisco indicherà il ricampionamento bootstrap.}
''','Il parametro è il bersaglio, lo stimatore è la regola di calcolo e la stima è il risultato sul campione.')

code(7,'bersagli','''# Diametri costruiti, in micrometri
x07 <- c(4.2,5.1,6.4,7.0,7.3)
mean(x07)        # diametro medio
mean(x07 > 6)    # quota sopra 6
# Contrasto con ordine dichiarato
r07 <- c(4.8,5.2,5.6)
s07 <- c(6.1,6.5,7.2)
mean(s07)-mean(r07) # Spiky-Rounded
''')
S(7,'La domanda determina il parametro',r'''
\PLabel{Tre domande su una variabile quantitativa}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\lab/\form/\unit in {
3.75/{Diametro medio}/{$\mu=\mathrm E(X)$}/{micrometri},
2.2/{Quota sopra una soglia}/{$p=P(X>c)$}/{senza unità},
.65/{Differenza fra gruppi}/{$\Delta=\mu_{\mathrm S}-\mu_{\mathrm R}$}/{micrometri}}{
\node[pFlow,text width=3.5cm] at(2,\yy){\lab};
\node[pLabel] at(6.8,\yy+.24){\form};
\node[pNote] at(6.8,\yy-.32){\unit};
}
\end{tikzpicture}
\PBody{La soglia $c$ e l'ordine del contrasto fanno parte della domanda. Un $\Delta$ positivo indica una media maggiore nel gruppo Spiky.}
''',r'''
\PCode{R · statistiche per tre domande}{007_bersagli.R}
\PSmall{La condizione \texttt{x07 > 6} produce valori logici. La loro media restituisce la proporzione osservata.}
\PInfo{Media e quota sopra soglia possono cambiare in modo diverso. La domanda guida la scelta della statistica.}
''','Prima del calcolo occorre precisare variabile, unità di misura, popolazione e parametro di interesse.')

code(8,'pesi','''# Medie costruite di tre stazioni
m08 <- c(A=5,B=6,C=12)
w08 <- c(A=.2,B=.3,C=.5)
sum(w08)           # somma: 1
sum(w08*m08)       # media pesata
weighted.mean(m08,w08)
# Ogni stazione conta 1/3.
mean(m08)
''')
S(8,'I pesi definiscono quale media interessa',r'''
\PLabel{Un parametro costruito su gruppi}
\[
\theta_w=\sum_{g=1}^{G}w_g\mu_g,\qquad
w_g\ge0,\quad\sum_gw_g=1.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\ww/\mm/\col in {1.5/{0{,}2}/5/GeoA,4.7/{0{,}3}/6/GeoB,7.9/{0{,}5}/12/GeoC}{
\node[pFlow,text width=2cm,fill=\col!8] at(\xx,2.3){$\mu_g=\mm$\\$w_g=\ww$};
\draw[pEdge](\xx,1.65)--(\xx,.9);
}
\node[pFlow,text width=7.8cm] at(4.7,.25){$\theta_w=0{,}2(5)+0{,}3(6)+0{,}5(12)=8{,}8$};
\end{tikzpicture}
\PSmall{I pesi possono descrivere quote note della popolazione o assegnare uguale importanza alle stazioni. Il criterio va dichiarato.}
''',r'''
\PCode{R · pesi normalizzati}{008_pesi.R}
\PSmall{\texttt{weighted.mean()} normalizza i pesi. Verificarne la somma rende trasparente il calcolo.}
\PInfo{La quota osservata nel campione e la quota nella popolazione coincidono soltanto in particolari disegni o realizzazioni.}
''','Cambiare i pesi può cambiare il parametro, anche mantenendo identici i valori delle medie di gruppo.')

code(9,'due_medie','''# Densita: g/cm^3, dati costruiti
n09 <- c(2,8)
m09 <- c(2.4,2.8)
weighted.mean(m09,n09) # 2.72
mean(m09)             # 2.60
c(peso_misure=n09[1]/sum(n09),
  peso_stazioni=1/length(n09))
''')
S(9,'Media delle misure e media delle stazioni',r'''
\PLabel{Due stazioni con numerosità diverse}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm,fill=GeoA!7] at(2.2,3.1){Stazione A\\$n_A=2,\ \bar x_A=2{,}4$};
\node[pFlow,text width=3.6cm,fill=GeoB!7] at(7,3.1){Stazione B\\$n_B=8,\ \bar x_B=2{,}8$};
\foreach \x in {1.9,2.5}\node[pDotA] at(\x,2.1){};
\foreach \x in {5.6,6,6.4,6.8,7.2,7.6,8,8.4}\node[pDotB] at(\x,2.1){};
\node[pLabel] at(4.6,1.15){$\displaystyle\bar x_{\mathrm{misure}}=\frac{2(2{,}4)+8(2{,}8)}{10}=2{,}72$};
\node[pLabel] at(4.6,.1){$\displaystyle\bar x_{\mathrm{stazioni}}=\frac{2{,}4+2{,}8}{2}=2{,}60$};
\end{tikzpicture}
\PSmall{Unità: $\mathrm{g/cm^3}$. La prima media dà più peso alla stazione con più misure. La seconda dà peso $1/2$ a ciascuna stazione.}
''',r'''
\PCode{R · stessi valori, pesi diversi}{009_due_medie.R}
\PBody{Una raccolta più intensa in B non dimostra che B rappresenti una quota maggiore del territorio. Occorre precisare la quantità da stimare.}
\PInfo{Le formule coincidono se i gruppi hanno uguale numerosità oppure uguale media.}
''','La scelta fra media delle misure e media delle stazioni richiede una motivazione legata alla popolazione di interesse.')

code(10,'bilanciato','''# Riprendiamo i gruppi di slide 5.
m10 <- tapply(d05$misura,
  d05$stazione,mean)
c(righe=mean(d05$misura),
  stazioni=mean(m10))
table(d05$stazione)  # 4,4,4
# L'uguaglianza deriva dai pesi.
''')
S(10,'Un disegno bilanciato rende uguali le due medie',r'''
\PLabel{$n_g=m$ per tutte le $G$ stazioni}
\[
\bar x=\frac{1}{Gm}\sum_{g=1}^{G}\sum_{i=1}^{m}x_{gi}
=\frac1G\sum_{g=1}^{G}\bar x_g.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\lab/\col in {1.6/A/GeoA,4.7/B/GeoB,7.8/C/GeoC}{
\node[pFlow,text width=2.2cm,fill=\col!7] at(\xx,2.1){Stazione \lab\\4 osservazioni};
\node[pLabel] at(\xx,.85){$w_g=4/12=1/3$};
}
\draw[Rule](.4,.1)--(9,.1);
\node[pNote,text width=8.8cm] at(4.7,-.45){Identità algebrica valida anche con misure dipendenti nella stessa stazione.};
\end{tikzpicture}
\PSmall{Il calcolo dell'errore standard richiede anche la struttura della dipendenza.}
''',r'''
\PCode{R · un'uguaglianza da verificare}{010_bilanciato.R}
\PSmall{\texttt{tapply()} suddivide la variabile in gruppi e applica la funzione indicata. Qui restituisce una media per stazione.}
\PInfo{Stessa stima puntuale e stesso numero di righe non garantiscono la stessa quantità di informazione.}
''','La coincidenza delle medie in un disegno bilanciato non risolve la questione dell’incertezza della stima.')

code(11,'densita','''# Due provini costruiti
m11 <- c(96,168)   # massa: g
v11 <- c(40,60)    # volume: cm^3
rho11 <- m11/v11
mean(rho11)       # 2.60 g/cm^3
sum(m11)/sum(v11) # 2.64 g/cm^3
weighted.mean(rho11,v11)
''')
S(11,'Media dei rapporti e rapporto dei totali',r'''
\PLabel{Domanda e supporto fisico}
\[
\rho_i=\frac{m_i}{V_i},\qquad\bar\rho=\frac1n\sum_i\rho_i.
\]
\[
\rho_{\mathrm{tot}}=\frac{\sum_i m_i}{\sum_i V_i}
=\sum_i\frac{V_i}{\sum_jV_j}\rho_i.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm,fill=GeoA!7] at(2.2,1.4){Provino 1\\$V_1=40,\ \rho_1=2{,}4$};
\node[pFlow,text width=3.6cm,fill=GeoB!7] at(7,1.4){Provino 2\\$V_2=60,\ \rho_2=2{,}8$};
\node[pNote] at(4.6,.25){Volume in $\mathrm{cm^3}$, densità in $\mathrm{g/cm^3}$.};
\end{tikzpicture}
\PSmall{Il rapporto dei totali pesa ciascuna densità con il volume del provino.}
''',r'''
\PCode{R · due quantità fisiche}{011_densita.R}
\PSmall{La media dei rapporti descrive il provino medio con pesi uguali. Il rapporto dei totali descrive massa complessiva per volume complessivo.}
\PInfo{La relazione deve indicare sia la formula usata per ogni osservazione sia il criterio di aggregazione.}
''','Aggregare prima o dopo una divisione può cambiare il parametro di interesse.')

code(12,'casuale_semplice','''# Tutti i campioni di 2 fra 6 unita
u12 <- c(2,4,5,7,8,10)
ind12 <- combn(seq_along(u12),2)
medie12 <- apply(ind12,2,
  function(i) mean(u12[i]))
length(medie12)       # 15 campioni
c(pop=mean(u12),
  attesa=mean(medie12))
''')
S(12,'Il campionamento casuale semplice',r'''
\PLabel{Popolazione finita, senza reinserimento}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\lab in {1/2,2.5/4,4/5,5.5/7,7/8,8.5/10}
\node[pFlow,minimum width=.95cm] at(\xx,2.6){\lab};
\draw[GeoB,line width=1.1pt](2.5,2.6) circle(.5);
\draw[GeoB,line width=1.1pt](7,2.6) circle(.5);
\node[pNote] at(4.7,1.5){Un campione di $n=2$ fra $N_U=6$ unità};
\node[pLabel] at(4.7,.6){$\displaystyle P(i\text{ incluso})=\frac{n}{N_U}=\frac13$};
\end{tikzpicture}
\[
\mathrm E_d(\bar X)=\bar Y_U,\qquad
\bar Y_U=\frac1{N_U}\sum_{i\in U}y_i.
\]
\PSmall{$\mathrm E_d$ media sui campioni del disegno. Ogni sottoinsieme di due unità ha uguale probabilità.}
''',r'''
\PCode{R · enumerare i campioni}{012_casuale_semplice.R}
\PSmall{\texttt{combn()} elenca le 15 coppie. La media delle loro medie coincide con quella della popolazione.}
\PInfo{La casualità deve riguardare la selezione. Mescolare le righe dopo una raccolta selettiva lascia invariato il campione.}
''','La non distorsione della media nel campionamento casuale semplice deriva dalle probabilità del disegno.')

code(13,'strati','''# Quote note della popolazione
W13 <- c(.3,.7)
m13 <- c(5.2,8.4) # medie campionarie
n13 <- c(20,20)   # allocazione
sum(W13*m13)      # 7.44
weighted.mean(m13,n13) # 6.80
# I pesi W descrivono la popolazione.
''')
S(13,'La stima stratificata usa le quote della popolazione',r'''
\PLabel{Strati definiti prima della selezione}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!15](.3,2.1) rectangle(3,3.3);
\fill[GeoB!15](3,2.1) rectangle(9.3,3.3);
\node[pLabel] at(1.65,2.7){$W_1=0{,}3$};
\node[pLabel] at(6.15,2.7){$W_2=0{,}7$};
\node[pFlow,text width=2.5cm] (a) at(1.65,.9){$n_1=20$\\$\bar x_1=5{,}2$};
\node[pFlow,text width=2.5cm] (b) at(6.15,.9){$n_2=20$\\$\bar x_2=8{,}4$};
\draw[pEdge](1.65,2.1)--(a);\draw[pEdge](6.15,2.1)--(b);
\end{tikzpicture}
\[
\widehat\theta_{\mathrm{str}}=\sum_{h=1}^{H}W_h\bar X_h,
\qquad W_h=\frac{N_h}{N_U}.
\]
\PSmall{Il prelievo casuale avviene separatamente in ogni strato. Le quote $W_h$ si riferiscono alla popolazione.}
''',r'''
\PCode{R · quote note e quote raccolte}{013_strati.R}
\PBody{Campione: metà osservazioni per strato. Popolazione: quote $30\%$ e $70\%$. I pesi seguono il parametro.}
\PInfo{La fonte dei pesi deve essere esplicita: dimensione degli strati, area rappresentata o altro criterio pertinente.}
''','L’allocazione del campione fra strati può differire dalla loro importanza nella popolazione.')

code(14,'selezione_stazioni','''# Prima stazioni, poi le loro righe
ids14 <- unique(d05$stazione)
set.seed(17)
scelte14 <- sample(ids14,size=2)
d05[d05$stazione %in% scelte14, ]
# Le righe della stessa stazione
# restano insieme nella selezione.
''')
S(14,'Selezionare stazioni e poi misure',r'''
\PLabel{Un disegno con unità raggruppate}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\lab/\col in {1.6/A/GeoA,4.7/B/GeoB,7.8/C/GeoC}{
\node[pFlow,text width=2.2cm,fill=\col!6] at(\xx,3.5){Stazione \lab};
\foreach \dx in {-.6,-.2,.2,.6}\node[circle,fill=\col,inner sep=1.7pt] at(\xx+\dx,2.6){};
}
\draw[GeoB,line width=1pt](.25,2.2) rectangle(2.95,4.2);
\draw[GeoB,line width=1pt](6.45,2.2) rectangle(9.15,4.2);
\node[pFlow,text width=8.2cm] at(4.7,.7){Campione: misure delle stazioni selezionate};
\draw[pEdge](1.6,2.2)--(1.6,1.55)--(2.4,1.55)--(2.4,1.25);
\draw[pEdge](7.8,2.2)--(7.8,1.55)--(7,1.55)--(7,1.25);
\end{tikzpicture}
\PSmall{Schema esemplificativo. Si possono osservare tutte le misure disponibili o selezionare ulteriori unità a un secondo stadio.}
''',r'''
\PCode{R · una selezione gerarchica}{014_selezione_stazioni.R}
\PSmall{\texttt{\%in\%} riconosce le righe delle stazioni scelte. L'appartenenza resta conservata nella tabella.}
\PInfo{Il bootstrap per stazioni riprenderà questo livello di organizzazione delle osservazioni.}
''','Il livello della selezione orienta il calcolo dell’incertezza e il successivo ricampionamento.')

code(15,'lab_estimandi','''# Stesso seme, diversa numerosita C
a15 <- lab_estimandi(nHigh=40)
b15 <- lab_estimandi(nHigh=10)
a15$indicatori
b15$indicatori
# Medie teoriche: A=5, B=6, C=12.
''')
S(15,'Laboratorio: quanto pesa la stazione C?',r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-estimandi}{Esperimento · misure o stazioni}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\lab/\ng/\mg/\col in {1.6/A/10/5/GeoA,4.7/B/10/6/GeoB,7.8/C/40/12/GeoC}{
\node[pFlow,text width=2.2cm,fill=\col!8] at(\xx,2.9){\lab\\$n_g=\ng$\\$\mu_g=\mg$};
}
\node[pLabel] at(4.7,1.35){$\displaystyle\theta_{\mathrm{alloc}}=\frac{10(5)+10(6)+40(12)}{60}=9{,}833$};
\node[pLabel] at(4.7,.35){$\displaystyle\theta_{\mathrm{stazioni}}=\frac{5+6+12}{3}=7{,}667$};
\end{tikzpicture}
\PSmall{Osservazioni normali con deviazione standard 1. Le formule riportano i bersagli teorici. Le medie osservate oscillano.}
''',r'''
\PCode{R · due allocazioni}{015_lab_estimandi.R}
\PBody{Confrontare \texttt{nHigh = 10} e \texttt{nHigh = 40}. Annotare pesi e risultati delle due medie.}
\PInfo{Aumentando \texttt{nHigh} cambiano sia il peso sia le osservazioni generate per C. Anche la sua media osservata può cambiare.}
''','Il confronto richiede di separare la variazione dei pesi dalla variazione casuale delle medie osservate.')

code(16,'lista_incompleta','''# Lista incompleta: esempio costruito
u16 <- data.frame(
 valore=c(4,5,5,6,8,9,10,11),
 accessibile=c(rep(TRUE,4),
               rep(FALSE,4)))
mean(u16$valore)
mean(u16$valore[u16$accessibile])
''')
S(16,'L’accessibilità può modificare il campione',r'''
\PLabel{Copertura incompleta: esempio costruito}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!8](.3,.4) rectangle(4.7,3.7);
\fill[GeoB!8](4.7,.4) rectangle(9.1,3.7);
\draw[Muted,dashed](4.7,.4)--(4.7,3.7);
\foreach \x/\y/\v in {1.2/1.2/4,3.4/1.2/5,1.2/2.4/5,3.4/2.4/6}
\node[pFlow,minimum width=.8cm,minimum height=.65cm] at(\x,\y){\v};
\foreach \x/\y/\v in {5.9/1.2/8,8.1/1.2/9,5.9/2.4/10,8.1/2.4/11}
\node[pFlow,minimum width=.8cm,minimum height=.65cm,fill=GeoB!10] at(\x,\y){\v};
\node[pNote] at(2.5,3.35){settore accessibile};
\node[pNote] at(7,3.35){settore escluso};
\node[pLabel] at(4.7,-.1){$\bar y_U=7{,}25\qquad\bar y_{\mathrm{lista}}=5$};
\end{tikzpicture}
\PSmall{Se il settore escluso ha valori diversi, la media della lista può differire da quella della popolazione.}
''',r'''
\PCode{R · effetto di una lista parziale}{016_lista_incompleta.R}
\PBody{Più osservazioni nel settore accessibile possono stabilizzare la stima sulla popolazione incompleta.}
\PInfo{Per interpretare la selezione servono informazioni sulle unità escluse e sui motivi dell'esclusione.}
''','La rappresentatività richiede un legame giustificabile fra le unità osservate e la popolazione a cui si estende il risultato.')

code(17,'bias','''# Simulazione diretta delle stime
n17 <- 60
set.seed(17)
t17 <- rnorm(200,mean=9,
             sd=2/sqrt(n17))
mean(t17)-10 # bias simulato
9-10         # bias del modello
''')
S(17,'La distorsione è uno scarto medio',r'''
\PLabel{Una proprietà delle ripetizioni}
\[
\operatorname{Bias}(\widehat\theta)=\mathrm E(\widehat\theta)-\theta.
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,.2)--(9,.2);
\draw[GeoA,line width=1pt] plot coordinates{'''+density(9,2/math.sqrt(60))+r'''};
\draw[GeoA,dashed](3.2667,.2)--(3.2667,3.1);
\draw[GeoB,line width=.9pt](5.9333,.2)--(5.9333,3.1);
\node[pNote] at(3.2667,-.18){9};
\node[pNote] at(5.9333,-.18){10};
\node[pNote,text=GeoA] at(2.1,3.3){$\mathrm E(\widehat\theta)$};
\node[pNote,text=GeoB] at(6.2,3.3){$\theta$};
\draw[{Latex}-{Latex},Muted](3.2667,3.05)--(5.9333,3.05);
\end{tikzpicture}
\PSmall{Curva teorica: $\widehat\theta\sim N(9,4/60)$, bersaglio $\theta=10$. La distorsione vale $-1$.}
''',r'''
\PCode{R · media delle stime meno parametro}{017_bias.R}
\PSmall{La media di 200 stime approssima l'attesa. Il bias simulato può differire da $-1$ per errore Monte Carlo.}
\PInfo{L'errore di una singola stima è $\widehat\theta_{\mathrm{oss}}-\theta$. La distorsione media l'errore sulle ripetizioni.}
''','Una singola osservazione dello scarto non permette di conoscere direttamente la distorsione dello stimatore.')

code(18,'mse','''# Modello della slide precedente
n18 <- 60
bias18 <- -1
var18 <- 4/n18
mse18 <- var18+bias18^2
c(varianza=var18,bias=bias18,
  mse=mse18,rmse=sqrt(mse18))
''')
S(18,'Errore quadratico: variabilità e distorsione',r'''
\PLabel{La scomposizione della MSE}
\[
\begin{aligned}
\operatorname{MSE}(\widehat\theta)
&=\mathrm E[(\widehat\theta-\theta)^2]\\
&=\operatorname{Var}(\widehat\theta)
+\{\mathrm E(\widehat\theta)-\theta\}^{2}.
\end{aligned}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.4cm,fill=GeoA!8] at(2.1,1.8){Variabilità attorno\\alla propria attesa};
\node[pFlow,text width=3.4cm,fill=GeoB!8] at(7.1,1.8){Scarto dell'attesa\\dal parametro};
\node[pLabel] at(4.6,1.8){$+$};
\node[pNote,text width=8.8cm] at(4.6,.45){Il termine incrociato scompare perché\\$\mathrm E[\widehat\theta-\mathrm E(\widehat\theta)]=0$.};
\end{tikzpicture}
\PSmall{Varianza e MSE hanno l'unità del parametro al quadrato. La radice della MSE torna all'unità originale.}
''',r'''
\PCode{R · errore quadratico medio}{018_mse.R}
\PBody{La varianza è $4/60\simeq0{,}0667$. La distorsione al quadrato è $1$. La MSE vale circa $1{,}0667$.}
\PInfo{Una procedura molto concentrata può avere MSE elevata quando è concentrata lontano dal parametro.}
''','La valutazione di una procedura considera sia la dispersione delle stime sia la loro distorsione.')

code(19,'piu_osservazioni','''# Confronto teorico
n19 <- c(60,300)
data.frame(
 n=n19,
 se=2/sqrt(n19),
 bias=rep(-1,2),
 mse=4/n19+1)
''')
S(19,'Più osservazioni riducono la varianza',r'''
\PLabel{Il bias resta costante in questo modello}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,.2)--(9,.2);
\draw[GeoA,line width=1pt] plot coordinates{'''+density(9,2/math.sqrt(60),h=1.25)+r'''};
\draw[GeoC,line width=1pt] plot coordinates{'''+density(9,2/math.sqrt(300),h=1.25*math.sqrt(5))+r'''};
\draw[GeoB,line width=.9pt](5.9333,.2)--(5.9333,3.3);
\node[pNote] at(3.2667,-.18){9};
\node[pNote] at(5.9333,-.18){$\theta=10$};
\node[pNote,text=GeoA] at(7.4,2.6){$n=60$};
\node[pNote,text=GeoC] at(7.4,2.05){$n=300$};
\end{tikzpicture}
\[
\operatorname{Var}(\widehat\theta)=\frac4n\longrightarrow0,\quad
\operatorname{MSE}(\widehat\theta)=\frac4n+1\longrightarrow1.
\]
\PSmall{Densità normali teoriche con la stessa attesa 9. Le altezze usano un'unica scala.}
''',r'''
\PCode{R · aumentare n nello stesso disegno}{019_piu_osservazioni.R}
\PBody{Da 60 a 300 osservazioni, il SE diminuisce. La distanza fra attesa della stima e parametro resta uguale.}
\PInfo{La formula $4/n+1$ appartiene a questo modello. In una ricerca reale la distorsione richiede di valutare il processo di selezione.}
''','L’aumento della numerosità migliora la precisione rispetto al bersaglio effettivo della procedura.')

code(20,'confronto_procedure','''# Bersaglio comune theta=10
v20 <- c(casuale=4/60,
         selettiva=4/300)
b20 <- c(casuale=0,selettiva=-1)
data.frame(se=sqrt(v20),
 bias=b20,mse=v20+b20^2)
''')
S(20,'Precisione e accuratezza possono differire',r'''
\PLabel{Confronto teorico su un bersaglio comune}
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[Navy](.2,3.2) rectangle(9.3,3.85);
\foreach \x/\t in {2.1/Procedura,4.8/SE,6.7/Bias,8.45/MSE}
\node[pLabel,text=white] at(\x,3.52){\t};
\fill[white](.2,1.95) rectangle(9.3,3.2);
\fill[GeoTint](.2,.7) rectangle(9.3,1.95);
\node[pLabel] at(2.1,2.57){Casuale, $n=60$};
\node[pLabel] at(4.8,2.57){$0{,}258$};
\node[pLabel] at(6.7,2.57){$0$};
\node[pLabel] at(8.45,2.57){$0{,}067$};
\node[pLabel] at(2.1,1.32){Selettiva, $n=300$};
\node[pLabel] at(4.8,1.32){$0{,}115$};
\node[pLabel] at(6.7,1.32){$-1$};
\node[pLabel] at(8.45,1.32){$1{,}013$};
\end{tikzpicture}
\PSmall{Qui l'accuratezza riguarda lo scarto complessivo valutato dalla MSE. I valori provengono dalle distribuzioni teoriche delle due procedure.}
''',r'''
\PCode{R · confronto su SE e MSE}{020_confronto_procedure.R}
\PBody{La seconda procedura ha un SE minore e una MSE maggiore. La larghezza di un intervallo, da sola, lascia fuori il problema di selezione.}
\PInfo{Nella pratica il parametro è ignoto. Conoscere il disegno e documentare le esclusioni permette di discutere i limiti della stima.}
''','La precisione descrive la dispersione delle stime. La MSE comprende anche la distorsione rispetto al parametro.')

code(21,'dati_mancanti','''# Registrare ogni esito del prelievo
d21 <- data.frame(
 id=1:6,
 misura=c(2.4,NA,2.7,2.5,NA,2.8),
 esito=c("ok","perso","ok","ok",
         "non accessibile","ok"))
table(d21$esito)
mean(d21$misura,na.rm=TRUE)
''')
S(21,'I dati mancanti hanno una storia di raccolta',r'''
\PLabel{Dal prelievo previsto al dato utilizzabile}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3cm] (p) at(2,3.3){6 unità previste};
\node[pFlow,text width=3.2cm,fill=GeoA!7] (o) at(7,3.3){4 misure disponibili};
\node[pFlow,text width=3cm,fill=GeoB!7] (l) at(2,.9){1 campione perso};
\node[pFlow,text width=3.2cm,fill=GeoB!7] (a) at(7,.9){1 unità non accessibile};
\draw[pEdge](p)--(o);\draw[pEdge](p)--(l);
\draw[pEdge](p.south east)--(a.north west);
\end{tikzpicture}
\PBody{Perdita accidentale e impossibilità di accesso possono avere conseguenze diverse. Registrare il motivo permette di discuterle.}
''',r'''
\PCode{R · conteggio degli esiti}{021_dati_mancanti.R}
\PSmall{\texttt{na.rm = TRUE} calcola la media delle misure disponibili. La rappresentatività delle unità restanti richiede un'analisi separata.}
\PInfo{Riportare unità previste, unità osservate e motivi delle esclusioni.}
''','La gestione informatica dei valori mancanti va accompagnata dalla descrizione del processo che li ha prodotti.')

code(22,'registro','''# Metadati: esempio costruito
registro22 <- data.frame(
 id=c("P01","P02","P03"),
 stazione=c("A","A","B"),
 strato=c("Nord","Nord","Sud"),
 ordine=c(1,2,3),
 protocollo=rep("casuale",3))
registro22
''')
S(22,'Il registro conserva il disegno del campione',r'''
\PLabel{Informazioni da mantenere nella tabella}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm] at(2.2,3.4){\textbf{Identificativi}\\misura, provino, stazione};
\node[pFlow,text width=3.6cm] at(7,3.4){\textbf{Appartenenza}\\strato, coppia, gruppo};
\node[pFlow,text width=3.6cm] at(2.2,1.1){\textbf{Ordine e posizione}\\tempo, coordinate, sequenza};
\node[pFlow,text width=3.6cm] at(7,1.1){\textbf{Protocollo}\\selezione, esclusioni, pesi};
\draw[Rule](4.6,.2)--(4.6,4.25);
\end{tikzpicture}
\PSmall{Il registro deve permettere di ricostruire le unità indipendenti e le relazioni fra osservazioni. I campi necessari dipendono dall'indagine.}
''',r'''
\PCode{R · identificativi e metadati}{022_registro.R}
\PBody{Tabelle con gli stessi numeri possono richiedere calcoli diversi se una contiene coppie e l'altra campioni indipendenti.}
\PInfo{Verificare duplicati, codici di stazione, ordine delle serie e corrispondenza fra coppie.}
''','Perdere le informazioni sul disegno può impedire di calcolare correttamente l’incertezza anche quando i valori numerici sono integri.')

code(23,'lab_selezione','''# Il sito genera direttamente stime.
a23 <- lab_selezione(n=60,bias=1)
b23 <- lab_selezione(n=300,bias=1)
a23$indicatori
b23$indicatori
c23 <- lab_selezione(n=60,bias=0)
c23$indicatori
''')
S(23,'Laboratorio: precisione e selezione',r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m05-selezione}{Esperimento · precisione e bias}
\[
\widehat\theta_{\mathrm C}\sim N\!\left(10,\frac4n\right),
\qquad
\widehat\theta_{\mathrm S}\sim N\!\left(10-b,\frac4n\right).
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm,fill=GeoA!7] at(2.1,2.1){$n=60$\\$SE=0{,}258$};
\node[pFlow,text width=3.5cm,fill=GeoB!7] at(7.1,2.1){$n=300$\\$SE=0{,}115$};
\node[pLabel] at(4.6,.8){Con $b=1$: bias $=-1$ per entrambe};
\end{tikzpicture}
\PSmall{Il laboratorio genera direttamente $B$ stime normali per procedura. Rappresenta uno spostamento, senza simulare una selezione geografica.}
''',r'''
\PCode{R · confronto fra scenari}{023_lab_selezione.R}
\PBody{Annotare centro, dispersione e MSE. Ripetere con bias nullo e confrontare ciò che cambia.}
\PInfo{$n$ controlla la variabilità della stima. $B$ conta le stime simulate. Il parametro del sito \texttt{bias} è $b$: la distorsione effettiva vale $-b$.}
''','Una simulazione si interpreta a partire dal meccanismo scritto nel codice e dal significato esatto dei parametri.')

code(24,'numerosita','''# Conteggi con significati diversi
G24 <- 6       # stazioni
m24 <- 4       # misure per stazione
n24 <- G24*m24 # osservazioni
B24 <- 2000    # repliche al computer
c(stazioni=G24,osservazioni=n24,
  repliche=B24)
''')
S(24,'n, G e B contano quantità diverse',r'''
\PLabel{Le dimensioni del problema}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\sim/\tit/\desc/\col in {
3.7/n/{Osservazioni}/{Righe con una misura.}/GeoA,
2.1/G/{Unità di prelievo}/{Per esempio, stazioni indipendenti.}/GeoB,
.5/B/{Repliche simulate}/{Ripetizioni di un algoritmo.}/GeoC}{
\node[circle,fill=\col!10,draw=\col,minimum size=1.05cm,font=\large] at(1,\yy){$\sim$};
\node[pLabel,anchor=west] at(2,\yy+.2){\textbf{\tit}};
\node[pNote,anchor=west] at(2,\yy-.28){\desc};
}
\end{tikzpicture}
\PSmall{Nel caso dei provini: 24 osservazioni in 6 stazioni. Il numero di ricampionamenti è una scelta del calcolo.}
''',r'''
\PCode{R · tre conteggi espliciti}{024_numerosita.R}
\PBody{Più $G$: nuove unità. Più $n$: anche misure nelle unità già note. Più $B$: repliche al computer.}
\PInfo{Per la stabilità numerica useremo anche $R=30$: ripetizioni complete del bootstrap sullo stesso campione.}
''','Le repliche del computer stabilizzano il calcolo. La quantità di informazione dipende dai dati e dal disegno.')

code(25,'ripetizioni','''# Ogni colonna e' un nuovo campione.
set.seed(17)
X25 <- replicate(5,
  rnorm(4,mean=10,sd=2))
round(X25,2)
colMeans(X25) # una stima per campione
dim(X25)     # 4 misure x 5 campioni
''')
S(25,'Una distribuzione di stime richiede campioni ripetuti',r'''
\PLabel{Dalle osservazioni alle statistiche}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\k/\col in {1.2/1/GeoA,3/2/GeoB,4.8/3/GeoC,6.6/4/GeoA,8.4/5/GeoB}{
\draw[pGroup,fill=\col!6](\xx-.6,1.4) rectangle(\xx+.6,3.6);
\node[pNote] at(\xx,3.95){camp. \k};
\foreach \yy in {1.8,2.3,2.8,3.3}\node[circle,fill=\col,inner sep=1.5pt] at(\xx,\yy){};
\draw[pEdge](\xx,1.4)--(\xx,.75);
\node[pLabel] at(\xx,.35){$\bar x_{\k}$};
}
\end{tikzpicture}
\PBody{Ogni colonna rappresenta un campione completo. Le cinque medie descrivono la variazione della stima fra queste ripetizioni.}
''',r'''
\PCode{R · una statistica per colonna}{025_ripetizioni.R}
\PSmall{\texttt{replicate()} ripete l'estrazione completa. \texttt{colMeans()} calcola la media di ogni campione. Riunire le 20 misure descriverebbe la distribuzione empirica dei dati individuali.}
\PInfo{Confronteremo la distribuzione dei dati individuali con quella della loro media.}
''','La distribuzione campionaria riguarda una statistica calcolata su campioni ripetuti dello stesso disegno.')
