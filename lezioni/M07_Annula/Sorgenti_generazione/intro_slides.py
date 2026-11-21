from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):SLIDES[n]=dict(title=title,section='I · RISPOSTA E RELAZIONE',left=left,right=right,recall=recall)
def code(n,name,s):CODES[f'{n:03}_{name}.R']=s.strip()+'\n'

S(2,'Una relazione descrive una risposta condizionata',r'''
\PLabel{Un fossile di diametro totale noto}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.6)--(9.1,.6) node[pNote,below]{$x$};
\draw[pAxis](.7,.6)--(.7,5.2) node[pNote,left]{$y$};
\draw[Classical,line width=1.4pt](1,1.2)--(8.5,4.5);
\fill[Classical!10](4.6,.7) rectangle(5.4,5);
\draw[GeoB,line width=1.3pt](5,1.6)--(5,4.3);
\foreach \yy in {1.85,2.3,2.7,3.3,3.8,4.05}{\fill[GeoA](5,\yy) circle(2pt);}
\fill[Classical](5,2.96) circle(3.5pt);
\node[pLabel,anchor=west] at(5.5,2.85){$E(Y\mid X=x_0)$};
\node[pNote] at(5,.25){$x_0$};
\node[pNote,align=left,text width=3.5cm] at(2.6,4.6){Schema: esemplari con lo stesso valore di $x$};
\end{tikzpicture}
''',r'''
\PBody{Il diametro totale aiuta a prevedere il diametro interno. A parità di diametro totale, i fossili conservano una variabilità.}
\vspace{4mm}
\[Y=m(X)+\varepsilon,\qquad E(\varepsilon\mid X)=0.\]
\PBody{La funzione $m(x)$ descrive la risposta media. L’errore $\varepsilon$ rappresenta gli scarti individuali attorno a quella media.}
\vspace{3mm}
\PInfo{La domanda scientifica precisa quali variabili sono disponibili quando occorre fare la previsione.}
''','Il modello collega una risposta alle informazioni disponibili e conserva l’incertezza delle osservazioni.')

code(3,'dati', '''
# Avvio dalla cartella Annula_M07.
source("setup.R", encoding = "UTF-8")
# Una riga corrisponde a un fossile.
head(f[, c("id", "diametro_tot_um",
           "diametro_int_um")])
stopifnot(!anyDuplicated(f$id))
''')
S(3,'Risposta, predittore e unità di osservazione',r'''
\PLabel{La stessa tabella, una domanda precisa}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] (x) at(2.3,3.6){$X$\quad Diametro totale\\misurato in $\mu$m};
\node[pFlow,text width=3.8cm] (y) at(7.2,3.6){$Y$\quad Diametro interno\\misurato in $\mu$m};
\draw[pEdge](x)--node[above,pNote]{previsione}(y);
\node[pLabel,text width=8.5cm] at(4.8,1.6){Ogni coppia $(x_i,y_i)$ appartiene allo stesso fossile $i$.};
\draw[Rule](.5,.8)--(9.1,.8);
\node[pNote,text width=8.5cm] at(4.8,.25){160 fossili sintetici, 80 per ciascun morfotipo};
\end{tikzpicture}
\PBody{Scambiare risposta e predittore cambia la domanda e il criterio di adattamento della regressione.}
''',r'''
\PCode{R · leggere le coppie di misure}{003_dati.R}
\PSmall{Il file \texttt{setup.R} carica i dati in \texttt{f}. La sigla \texttt{um} nei nomi indica micrometri.}
\PInfo{Sono dati sintetici del corso. I risultati descrivono questo esempio didattico.}
''','Prima della formula: un’unità di osservazione, una risposta, predittori disponibili e unità di misura.')

code(4,'geometria','''
# La relazione deriva dalla costruzione
# geometrica delle tre misure.
scarto <- with(f, diametro_tot_um -
  diametro_int_um - 2 * spessore_um)
max(abs(scarto))
# Circa 1e-8: arrotondamento del CSV.
''')
S(4,'La geometria lega i due diametri',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\filldraw[fill=GeoB!20,draw=GeoB,line width=1pt](4.5,2.6) circle(2.1);
\filldraw[fill=Paper,draw=Classical,line width=1pt](4.5,2.6) circle(1.5);
\draw[Muted,densely dotted](2.4,2.6)--(2.4,.05);
\draw[Muted,densely dotted](6.6,2.6)--(6.6,.05);
\draw[{Latex}-{Latex},Navy,line width=1pt](2.4,.1)--(6.6,.1);
\node[pLabel,fill=Paper] at(4.5,.1){$D_{\rm tot}$};
\draw[{Latex}-{Latex},Classical,line width=1pt](3,2.6)--(6,2.6);
\node[pLabel,fill=Paper,text=Classical] at(4.5,2.6){$D_{\rm int}$};
\draw[{Latex}-{Latex},GeoB,line width=1pt](6,2.6)--(6.6,2.6);
\node[pLabel,text=GeoB] at(6.5,3.15){$s$};
\node[pNote] at(4.5,-.5){Sezione ideale con parete di spessore $s$};
\end{tikzpicture}
\PInfo{Ricostruire $D_{\rm int}$ da $D_{\rm tot}$ e $s$ applica l’identità geometrica: la domanda deve dichiararlo.}
''',r'''
\[D_{\rm int}=D_{\rm tot}-2s.\]
\PCode{R · controllare l’identità}{004_geometria.R}
\PBody{Una parte dell’associazione nasce dalla definizione delle variabili. La dispersione dello spessore contribuisce alla dispersione del diametro interno.}
''','Una correlazione elevata può riflettere una definizione condivisa delle misure.')

code(5,'nuvola','''
# Colore secondo il morfotipo.
col <- c("#1D7890", "#C57E42")
plot(diametro_int_um ~ diametro_tot_um,
  data = f, col = col[f$morfotipo],
  pch = 16, xlab = "Totale (um)",
  ylab = "Interno (um)")
''')
S(5,'La nuvola conserva le coppie di osservazioni',scatter()+r'''
\PInfo{Una figura iniziale aiuta a riconoscere forma, dominio e osservazioni insolite prima di sintetizzare tutto con un coefficiente.}
''',r'''
\PCode{R · rappresentare le due variabili}{005_nuvola.R}
\PBody{L’andamento è crescente. I colori mantengono visibile il morfotipo e permettono di cercare differenze a parità di diametro totale.}
''','Ogni punto mantiene l’abbinamento tra le due misure dello stesso fossile.')

S(6,'Media marginale e media condizionata',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.6)--(9,.6);\draw[pAxis](.7,.6)--(.7,5.2);
\draw[GeoB,dashed,line width=1.1pt](.8,2.7)--(8.7,2.7);
\draw[Classical,line width=1.3pt](1,1.1)--(8.6,4.6);
\foreach \xx/\yy in {2/1.56,4.8/2.85,7.5/4.1}{
\draw[GeoA,line width=1.1pt](\xx,\yy-.6)--(\xx,\yy+.6);
\fill[Classical](\xx,\yy) circle(3pt);}
\node[pLabel,anchor=west,text=GeoB] at(1,3.05){$E(Y)$};
\node[pLabel,anchor=west,text=Classical] at(5.2,4.8){$E(Y\mid X=x)$};
\node[pNote] at(4.8,.15){Diametro totale noto};
\end{tikzpicture}
''',r'''
\PLabel{Quanto aiuta conoscere il predittore?}
\PBody{La media marginale assegna la stessa previsione a ogni fossile. La media condizionata cambia al variare del diametro totale.}
\[\hat y_{\rm base}=\bar y,\qquad \hat y(x)=\hat m(x).\]
\PBody{La variabilità residua riguarda esemplari confrontabili per $x$. Resta anche quando la retta descrive bene l’andamento medio.}
''','La regressione usa informazioni sul singolo caso per modificare la previsione della risposta.')

code(7,'dominio','''
# Campo realmente osservato nel file.
range(f$diametro_tot_um)
# Un nuovo valore deve essere esaminato.
x0 <- 9
x0 >= min(f$diametro_tot_um) &&
  x0 <= max(f$diametro_tot_um)
''')
S(7,'Il dominio osservato delimita l’esperienza',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,2.1)--(9.2,2.1);
\draw[Classical,line width=6pt](1.55,2.1)--(7.7,2.1);
\foreach \x/\t in {1.55/{3,68},7.7/{8,62},8.2/9}{\draw[Navy](\x,1.9)--(\x,2.3);\node[pNote] at(\x,1.55){$\t$};}
\fill[GeoB](8.2,2.1) circle(4pt);
\node[pLabel] at(4.6,3.1){Campo dei 160 fossili};
\node[pNote,anchor=east,text=GeoB] at(9.1,4.1){Nuovo caso: $9\ \mu$m};
\draw[pEdge,GeoB](8.2,3.8)--(8.2,2.4);
\node[pNote] at(4.8,.7){Diametro totale ($\mu$m)};
\end{tikzpicture}
''',r'''
\PCode{R · confrontare nuovo e osservato}{007_dominio.R}
\PBody{Il file copre circa $3{,}68$--$8{,}62\ \mu$m. Il valore $9\ \mu$m è già fuori dal campo osservato.}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-dominio}{Esperimento: dominio}
\PSmall{Nel sito la relazione vera è curva. Una retta stimata nel campo osservato può allontanarsi molto oltre quel campo.}
''','L’estrapolazione aggiunge un’ipotesi sulla validità del modello in condizioni non osservate.')

S(8,'La correlazione riassume gli scarti concordi',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[Classical!8](.6,.6) rectangle(4.6,2.8);
\fill[Classical!8](4.6,2.8) rectangle(8.8,5.1);
\draw[pAxis](.6,2.8)--(9.1,2.8);\draw[pAxis](4.6,.4)--(4.6,5.4);
\foreach \x/\y in {1.5/1.1,2.5/2,3/1.6,4.1/2.4,5.3/3.4,6.4/3.9,7.5/4.7,8/4.3}{\fill[GeoA](\x,\y) circle(2.3pt);}
\node[pLabel] at(7,1.1){prodotto negativo};\node[pLabel] at(2.4,4.4){prodotto negativo};
\node[pLabel,text=Classical] at(2.6,.1){scarti concordi};\node[pLabel,text=Classical] at(7,5.8){scarti concordi};
\node[pNote] at(7.1,2.45){$x-\bar x$};\node[pNote] at(5.3,5.2){$y-\bar y$};
\end{tikzpicture}
''',r'''
\[r=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_i(x_i-\bar x)^2\sum_i(y_i-\bar y)^2}}.\]
\PBody{Gli scarti concordi danno contributi positivi. La normalizzazione elimina le unità e colloca $r$ tra $-1$ e $1$.}
\PInfo{Il coefficiente è definito quando entrambe le variabili hanno varianza positiva. Riassume l’associazione lineare.}
''','Pearson confronta covariazione e dispersioni delle due variabili.')

code(9,'correlazione','''
x <- f$diametro_tot_um
y <- f$diametro_int_um
cor(x, y, method = "pearson")
# Cambio di unita positivo: stesso r.
cor(x / 1000, y / 1000)
# L'inversione del segno cambia r.
cor(x, -y)
''')
S(9,'Correlazione e unità di misura',scatter()+r'''
\PInfo{Pearson è simmetrico: $r(x,y)=r(y,x)$. La regressione assegna ruoli differenti a risposta e predittore.}
''',r'''
\PCode{R · calcolare Pearson}{009_correlazione.R}
\[r=0{,}965\quad\text{nei 160 fossili}.\]
\PBody{Passare da micrometri a millimetri lascia invariata la correlazione. La pendenza conserva invece il rapporto fra le unità delle due variabili.}
''','Un numero senza unità misura associazione. Per prevedere la risposta serve anche la scala.')

code(10,'ranghi','''
# Spearman applica Pearson ai ranghi.
cor(x, y, method = "spearman")
cor(rank(x), rank(y))
# In caso di pareggi R usa ranghi medi.
''')
S(10,'Monotonia e linearità',r'''
\PLabel{Schema di una relazione crescente curva}
'''+schematic('monotonic')+r'''
\PBody{Spearman riassume la concordanza degli ordinamenti. Una curva strettamente crescente può avere $r_S=1$ anche se la pendenza cambia con $x$.}
''',r'''
\[r_S=\operatorname{cor}\{\operatorname{rank}(X),\operatorname{rank}(Y)\}.\]
\PCode{R · confrontare i ranghi}{010_ranghi.R}
\PSmall{Nei fossili: Pearson $0{,}965$, Spearman $0{,}952$. La figura resta necessaria per capire la forma.}
''','L’associazione monotona riguarda l’ordine. L’associazione lineare riguarda una retta.')

code(11,'curvatura','''
# Esempio costruito, senza rumore.
u <- seq(-2, 2, length.out = 101)
v <- u^2
cor(u, v)  # Praticamente zero.
plot(u, v, pch = 16)
''')
S(11,'Una relazione curva può avere correlazione nulla',schematic('u'),r'''
\[Y=X^2,\qquad X\sim U(-a,a).\]
\PBody{Per simmetria, $E(X)=E(X^3)=0$, quindi $\operatorname{Cov}(X,X^2)=0$. Eppure conoscere $X$ determina esattamente $Y$.}
\PCode{R · verificare un controesempio}{011_curvatura.R}
\PSmall{Il diagramma riproduce la forma a U su assi traslati e riscalati. La retta orizzontale ignora la sua struttura.}
''','Una correlazione vicina a zero esclude una forte associazione lineare, non ogni relazione.')

code(12,'campo','''
# Stessa legge, due campi del predittore.
set.seed(17)
u <- runif(1000, -4, 4)
v <- 2 * u + rnorm(1000)
centrali <- abs(u) < 1
c(intero = cor(u, v),
  ristretto = cor(u[centrali],
                 v[centrali]))
''')
S(12,'La restrizione del campo cambia la correlazione',r'''
\PLabel{Modello $Y=2X+\varepsilon$ con rumore invariato}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.8)--(9,.8);\draw[pAxis](.7,.8)--(.7,5.1);
\fill[GeoB!12](4,.9) rectangle(5.9,4.9);
\draw[Classical,line width=1.3pt](1,1.1)--(8.5,4.7);
\foreach \x/\y in {1.3/1.6,2/1.2,2.7/2.1,3.5/2.8,4.1/2.4,4.6/3.2,5/2.9,5.7/3.6,6.2/3.1,7.3/4,8.1/4.8}{\fill[GeoA](\x,\y) circle(2pt);}
\node[pNote,text=GeoB] at(4.95,5.4){campo ristretto};
\node[pNote] at(4.8,.3){stessa pendenza, minore dispersione di $X$};
\end{tikzpicture}
\[\rho^2=\frac{\beta_1^2\operatorname{Var}(X)}{\beta_1^2\operatorname{Var}(X)+\sigma^2}.\]
''',r'''
\PCode{R · restringere il campione}{012_campo.R}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-correlazione}{Esperimento: correlazione}
\PSmall{Con errore indipendente da $X$, la riduzione di $\operatorname{Var}(X)$ rende più grande il peso relativo del rumore.}
''','La correlazione dipende anche dal campo dei predittori presente nel campione.')

S(13,'Una causa comune può generare associazione',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.2cm] (z) at(4.8,4.8){Ambiente deposizionale\\$Z$};
\node[pFlow,text width=3.2cm] (x) at(2.3,2){Misura $X$};
\node[pFlow,text width=3.2cm] (y) at(7.3,2){Misura $Y$};
\draw[pEdge](z)--(x);\draw[pEdge](z)--(y);
\draw[GeoB,dashed,line width=1pt](x)--node[pNote,below]{associazione osservata}(y);
\node[pNote,text width=8.5cm] at(4.8,.4){Schema causale ipotetico da sostenere con conoscenze del processo};
\end{tikzpicture}
''',r'''
\PBody{Una variabile comune può modificare entrambe le misure. Una relazione osservata tra $X$ e $Y$ può quindi dipendere dalla composizione del campione.}
\[E(Y\mid X=x)\quad\text{e}\quad E\{Y\mid \operatorname{do}(X=x)\}\]
\PSmall{La prima quantità è osservativa. La seconda descrive un intervento e richiede ipotesi causali aggiuntive. La notazione serve a distinguere le domande.}
\PInfo{Aggiungere variabili a una regressione richiede una ragione scientifica. La sola disponibilità di una colonna non basta.}
''','La regressione descrive una relazione condizionata. Un’interpretazione causale richiede un disegno e ipotesi specifici.')
