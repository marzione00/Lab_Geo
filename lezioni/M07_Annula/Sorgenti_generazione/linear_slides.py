from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):SLIDES[n]=dict(title=title,section='II · MODELLO LINEARE',left=left,right=right,recall=recall)
def code(n,name,s):CODES[f'{n:03}_{name}.R']=s.strip()+'\n'

S(14,'Il modello lineare per la risposta media',schematic('linear'),r'''
\[Y_i=\beta_0+\beta_1x_i+\varepsilon_i.\]
\PBody{Assumendo $E(\varepsilon_i\mid x_i)=0$, la risposta media condizionata è una retta:}
\[E(Y_i\mid x_i)=\beta_0+\beta_1x_i.\]
\PBody{I parametri $\beta_0$ e $\beta_1$ descrivono la popolazione nel modello. I dati producono le stime $\hat\beta_0$ e $\hat\beta_1$.}
\PInfo{Il diagramma è schematico. La scelta di una retta richiede un controllo della forma sui dati.}
''','La linearità riguarda la media della risposta, non l’allineamento perfetto di tutti i punti.')

S(15,'Intercetta e pendenza hanno un significato diverso',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.8,.7)--(9,.7);\draw[pAxis](.8,.7)--(.8,5.1);
\draw[Classical,line width=1.4pt](.8,1.7)--(8.5,4.8);
\draw[GeoB,line width=1pt](3.3,2.7)--(6.3,2.7)--(6.3,3.91);
\node[pLabel,text=GeoB] at(4.8,2.3){$\Delta x$};
\node[pLabel,text=GeoB,anchor=west] at(6.5,3.3){$\beta_1\Delta x$};
\fill[Classical](.8,1.7) circle(3pt);
\node[pLabel,anchor=west] at(1.1,1.35){$\beta_0$ a $x=0$};
\node[pNote] at(4.6,.2){Schema della variazione media};
\end{tikzpicture}
''',r'''
\[\beta_1=\frac{\Delta E(Y\mid x)}{\Delta x}.\]
\PBody{La pendenza indica quanto cambia la risposta media per un’unità in più del predittore. Ha unità $[Y]/[X]$.}
\vspace{3mm}
\PBody{L’intercetta è la media a $x=0$. La sua interpretazione fisica dipende dal dominio. Per i fossili, un diametro totale nullo è fuori dalle condizioni del campione.}
''','Il valore algebrico dell’intercetta può essere utile al calcolo senza rappresentare un esemplare possibile.')

S(16,'Errori del modello e residui osservabili',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,.6)--(9,.6);\draw[pAxis](.6,.6)--(.6,5.2);
\draw[Classical,line width=1.1pt](1,1.1)--(8.4,4.6);
\draw[GeoB,dashed,line width=1.1pt](1,1.8)--(8.4,4.3);
\fill[Ink](5,4.5) circle(3pt);
\draw[Muted,densely dotted](4.65,4.5)--(5.35,4.5);
\draw[Muted,densely dotted](4.65,2.99189)--(5,2.99189);
\draw[Muted,densely dotted](5,3.15135)--(5.35,3.15135);
\draw[{Latex}-{Latex},Classical](4.65,2.99189)--(4.65,4.5);
\draw[{Latex}-{Latex},GeoB](5.35,3.15135)--(5.35,4.5);
\node[pLabel,text=Classical,anchor=east] at(4.4,3.9){$\varepsilon_i$};
\node[pLabel,text=GeoB,anchor=west] at(5.6,3.9){$e_i$};
\node[pNote,text=Classical] at(3.0,1.2){media vera};
\node[pNote,text=GeoB] at(6.6,2.7){media stimata};
\node[pNote] at(4.8,.15){Schema: la retta vera è normalmente ignota};
\end{tikzpicture}
''',r'''
\[\varepsilon_i=y_i-E(Y_i\mid x_i),\qquad e_i=y_i-\hat y_i.\]
\PBody{Il residuo si calcola dopo la stima. L’errore rispetto alla media vera rimane generalmente ignoto.}
\PBody{Le ipotesi probabilistiche riguardano gli errori. I grafici dei residui permettono di cercare incompatibilità con quelle ipotesi.}
\PInfo{I residui di una regressione condividono i parametri stimati e non sono indipendenti tra loro.}
''','Un residuo è una differenza calcolata rispetto a una funzione stimata dagli stessi dati.')

code(17,'scarti','''
# Retta proposta, prima dell'ottimizzazione.
a <- -0.5
b <- 0.9
e_proposti <- y - (a + b * x)
sum(e_proposti^2)
# Confronto con il minimo trovato da lm.
sum(residuals(m0)^2)
''')
S(17,'I minimi quadrati misurano scarti verticali',schematic('residual')+r'''
\PBody{Il criterio somma le distanze verticali al quadrato. Un grande scarto pesa più di diversi piccoli scarti della stessa somma assoluta.}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-minimi-quadrati}{Esperimento: minimi quadrati}
''',r'''
\[S(b_0,b_1)=\sum_{i=1}^{n}\{y_i-(b_0+b_1x_i)\}^2.\]
\PCode{R · confrontare una retta proposta}{017_scarti.R}
''','La regressione ordinaria minimizza gli scarti lungo l’asse della risposta.')

S(18,'La somma dei quadrati ha un minimo',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.7)--(9.1,.7);\draw[pAxis](.7,.7)--(.7,5.3);
\draw[Classical,line width=1.4pt,domain=1.25:8.35,samples=60] plot(\x,{1.05+.32*(\x-4.8)^2});
\draw[Muted,dashed](4.8,.7)--(4.8,1.05);
\fill[Classical](4.8,1.05) circle(3pt);
\node[pLabel] at(4.8,.2){$\hat\beta_1$};
\node[pLabel] at(7.2,4.8){$S(b_1)$};
\node[pNote] at(4.8,5.75){L’intercetta segue $b_0=\bar y-b_1\bar x$};
\end{tikzpicture}
''',r'''
\[S(b_1)=\sum_i\{(y_i-\bar y)-b_1(x_i-\bar x)\}^2.\]
\PBody{Dopo avere centrato le variabili, resta da scegliere una pendenza. Il criterio è una parabola convessa in $b_1$.}
\[\frac{\partial^2 S}{\partial b_1^2}=2\sum_i(x_i-\bar x)^2>0.\]
\PInfo{La disuguaglianza richiede almeno due valori diversi del predittore. In quel caso il minimo è unico.}
''','La variabilità di X permette di identificare la pendenza.')

S(19,'La prima equazione impone residui a somma zero',r'''
\PLabel{Derivata rispetto all’intercetta}
\[\frac{\partial S}{\partial b_0}=-2\sum_i(y_i-b_0-b_1x_i).\]
\[\sum_i y_i-n\hat\beta_0-\hat\beta_1\sum_i x_i=0.\]
\[\boxed{\hat\beta_0=\bar y-\hat\beta_1\bar x}\]
\PBody{La retta stimata attraversa il punto delle medie $(\bar x,\bar y)$. Il suo livello verticale si adatta alla media osservata.}
''',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,2.7)--(6.9,2.7);
\foreach \x/\v in {.8/1.1,1.8/-.8,2.8/.6,3.8/-1.3,4.8/.9,5.8/-.5}{\draw[GeoA,line width=2pt](\x,2.7)--(\x,2.7+\v);}
\node[pLabel] at(3.8,4.7){$\sum_i e_i=0$};
\node[pNote,text width=6.6cm] at(3.7,1){Schema degli scarti positivi e negativi};
\end{tikzpicture}
\PInfo{La proprietà vale per minimi quadrati ordinari con intercetta. Non garantisce che il modello descriva bene la forma.}
''','La somma zero dei residui è una conseguenza algebrica della stima con intercetta.')

S(20,'La seconda equazione determina la pendenza',r'''
\PLabel{Derivata rispetto alla pendenza}
\[\frac{\partial S}{\partial b_1}=-2\sum_i x_i(y_i-b_0-b_1x_i).\]
\PBody{Sostituendo l’espressione dell’intercetta e raccogliendo gli scarti centrati:}
\[\sum_i(x_i-\bar x)(y_i-\bar y)=\hat\beta_1\sum_i(x_i-\bar x)^2.\]
\[\boxed{\hat\beta_1=\frac{S_{xy}}{S_{xx}}}\]
''',r'''
\PLabel{Due quantità con ruoli diversi}
\[S_{xy}=\sum_i(x_i-\bar x)(y_i-\bar y),\]
\[S_{xx}=\sum_i(x_i-\bar x)^2.\]
\PBody{Il numeratore misura la covariazione. Il denominatore misura la dispersione del predittore.}
\PInfo{Se $S_{xx}=0$, tutti i valori di $x$ coincidono. I dati non separano intercetta e pendenza.}
''','La pendenza divide covariazione per dispersione del predittore.')

S(21,'La retta attraversa il baricentro della nuvola',scatter(fit=True,means=True),r'''
\[\hat y=\bar y+\hat\beta_1(x-\bar x).\]
\PBody{Questa forma mette in evidenza il riferimento: la previsione parte dalla media della risposta e cambia secondo la distanza di $x$ dalla sua media.}
\[\bar x=6{,}355\ \mu\mathrm m,\qquad \bar y=5{,}381\ \mu\mathrm m.\]
\PInfo{La retta nella figura è stimata su tutti i 160 fossili per descrivere il campione. La valutazione predittiva userà un protocollo separato.}
''','Centrare il predittore cambia l’intercetta, mentre pendenza e valori stimati restano uguali.')

code(22,'minimi_mano','''
# Scarti dalle rispettive medie.
xc <- x - mean(x)
yc <- y - mean(y)
b1 <- sum(xc * yc) / sum(xc^2)
b0 <- mean(y) - b1 * mean(x)
c(intercetta = b0, pendenza = b1)
# Le due procedure devono coincidere.
all.equal(unname(coef(m0)), c(b0, b1))
''')
S(22,'La formula e il calcolo in R coincidono',r'''
\PLabel{Stime sui 160 fossili}
\[\hat\beta_0=-0{,}700282,\qquad\hat\beta_1=0{,}956997.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.3,3.3){Somme degli scarti\\$S_{xy}/S_{xx}$};
\node[pFlow,text width=3.7cm] (b) at(7.2,3.3){Algoritmo numerico\\\texttt{lm()}};
\node[pLabel] (stessa) at(4.8,1.2){Stessa retta, entro la precisione numerica};
\draw[Classical,line width=.95pt](a.south)--(2.3,2.1)--(7.2,2.1)--(b.south);
\draw[pEdge](4.8,2.1)--(stessa.north);
\end{tikzpicture}
''',r'''
\PCode{R · ricostruire le stime}{022_minimi_mano.R}
\PSmall{\texttt{unname()} rimuove solo i nomi dei coefficienti. \texttt{all.equal()} confronta valori numerici con una tolleranza.}
''','Ricostruire una stima semplice aiuta a capire che cosa calcola la funzione.')

code(23,'lm','''
# La risposta compare a sinistra di ~.
m0 <- lm(diametro_int_um ~
           diametro_tot_um, data = f)
coef(m0)      # Intercetta e pendenza.
fitted(m0)    # Valori medi stimati.
residuals(m0) # Osservato - stimato.
summary(m0)
''')
S(23,'La formula di R assegna i ruoli alle variabili',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.9cm] (a) at(2.4,3.7){\texttt{diametro\_int\_um}\\risposta};
\node[pFlow,text width=3.9cm] (b) at(7.3,3.7){\texttt{diametro\_tot\_um}\\predittore};
\node[pLabel,font=\fontsize{22}{25}\selectfont] at(4.85,3.7){$\sim$};
\node[pLabel,text width=8.4cm] at(4.8,1.8){\texttt{data = f} indica la tabella che contiene le variabili.};
\node[pNote,text width=8.4cm] at(4.8,.65){L’intercetta è inclusa per impostazione predefinita.};
\end{tikzpicture}
''',r'''
\PCode{R · stimare e interrogare il modello}{023_lm.R}
\PSmall{\texttt{m0} conserva dati, formula e risultati. Le funzioni successive estraggono componenti specifiche senza ristimare manualmente il modello.}
''','Un oggetto lm conserva una procedura di stima e permette di interrogare risultati diversi.')

code(24,'pendenza','''
# Incremento medio per +0.5 um in X.
delta_x <- 0.5
coef(m0)[2] * delta_x
# Previsione media a diametro totale 7.
predict(m0, newdata = data.frame(
  diametro_tot_um = 7))
''')
S(24,'La pendenza traduce un incremento nelle unità',r'''
\PLabel{La retta stimata sui fossili}
\[\widehat D_{\rm int}=-0{,}700+0{,}957D_{\rm tot}.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.3,2.9){$+0{,}5\ \mu$m\\di diametro totale};
\node[pFlow,text width=3.7cm] (b) at(7.2,2.9){$+0{,}4785\ \mu$m\\nella media prevista};
\draw[pEdge](a)--(b);
\node[pNote,text width=8.6cm] at(4.8,1){Il confronto vale entro il modello e il campo osservato.};
\end{tikzpicture}
\PInfo{Questa stima riassume l’associazione campionaria. Non quantifica l’effetto di modificare fisicamente un fossile.}
''',r'''
\PCode{R · interpretare un incremento}{024_pendenza.R}
\PBody{Il coefficiente è circa $0{,}957\ \mu$m per $\mu$m. Le stesse unità al numeratore e denominatore si semplificano, ma l’interpretazione resta legata alle due misure.}
''','Specificare incremento, unità e condizioni rende interpretabile un coefficiente.')

S(25,'Le ipotesi sostengono conclusioni diverse',r'''
\PLabel{Dal calcolo all’inferenza}
\begin{tabular}{p{4.15cm}p{4.9cm}}
\toprule
\textbf{Condizione}&\textbf{Che cosa sostiene}\\\midrule
Matrice $X$ a rango pieno&Stima univoca dei coefficienti\\[2mm]
$E(\varepsilon\mid X)=0$&Non distorsione di OLS nel modello\\[2mm]
$\operatorname{Var}(\varepsilon\mid X)=\sigma^2I$&Formule classiche della varianza\\[2mm]
Normalità degli errori&Intervalli e test t esatti a campione finito\\\bottomrule
\end{tabular}
''',r'''
\PBody{La retta dei minimi quadrati si può calcolare senza assumere normalità. Per interpretare l’incertezza occorre dichiarare ipotesi sulla generazione dei dati.}
\vspace{3mm}
\PBody{Indipendenza e campionamento coerente con la popolazione sono questioni del disegno. Un grafico dei residui può segnalare problemi, ma da solo non certifica il disegno.}
\PInfo{Nel seguito le formule classiche usano errori indipendenti, varianza costante e, per gli intervalli t esatti, normalità condizionata.}
''','Una formula di stima e una formula d’incertezza possono richiedere condizioni differenti.')

code(26,'matrice','''
# X contiene una colonna di 1 e il predittore.
X <- model.matrix(m0)
head(X)
dim(X)       # 160 righe, 2 colonne.
qr(X)$rank   # Rango della matrice.
''')
S(26,'La matrice del disegno raccoglie i predittori',r'''
\[\underbrace{\begin{pmatrix}y_1\\y_2\\\vdots\\y_n\end{pmatrix}}_{n\times1}
=\underbrace{\begin{pmatrix}1&x_1\\1&x_2\\\vdots&\vdots\\1&x_n\end{pmatrix}}_{X:\ n\times2}
\underbrace{\begin{pmatrix}\beta_0\\\beta_1\end{pmatrix}}_{2\times1}
+\underbrace{\begin{pmatrix}\varepsilon_1\\\varepsilon_2\\\vdots\\\varepsilon_n\end{pmatrix}}_{n\times1}.\]
\vspace{3mm}
\PBody{Ogni riga descrive un’osservazione. Ogni colonna rappresenta un termine della formula, compresa l’intercetta.}
\[\mathbf y=X\boldsymbol\beta+\boldsymbol\varepsilon.\]
''',r'''
\PCode{R · vedere il disegno usato da lm}{026_matrice.R}
\PBody{Con $p$ coefficienti, $X$ ha $p$ colonne. Qui $p=2$. Nei modelli con gruppi, interazioni e trasformazioni sarà importante contare i coefficienti effettivi.}
\PInfo{Useremo $p$ includendo l’intercetta. I gradi di libertà residui sono $n-p$ se il rango è pieno.}
''','La matrice X rende esplicito ciò che la formula chiede al modello di stimare.')

S(27,'I minimi quadrati sono una proiezione',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[GeoA!8](.8,.7)--(6.7,.7)--(8.8,3.2)--(2.9,3.2)--cycle;
\draw[GeoA!40](.8,.7)--(6.7,.7)--(8.8,3.2)--(2.9,3.2)--cycle;
\coordinate(o)at(1.5,1.1);\coordinate(yh)at(6.1,2.1);\coordinate(y)at(6.1,5.4);
\draw[pEdge,Navy,line width=1.3pt](o)--(y) node[above,pLabel]{$\mathbf y$};
\draw[pEdge,Classical,line width=1.3pt](o)--(yh) node[below,pLabel]{$\hat{\mathbf y}$};
\draw[pEdge,GeoB,line width=1.3pt](yh)--(y) node[midway,right,pLabel]{$\mathbf e$};
\draw[Muted](5.8,2.03)--(5.8,2.34)--(6.1,2.41);
\node[pNote] at(4.4,.15){Spazio generato dalle colonne di $X$};
\end{tikzpicture}
''',r'''
\[X^\top(\mathbf y-X\hat{\boldsymbol\beta})=\mathbf0.\]
\PBody{Il residuo è ortogonale a ogni colonna del disegno. La previsione è il punto dello spazio del modello più vicino a $\mathbf y$.}
\[\hat{\boldsymbol\beta}=(X^\top X)^{-1}X^\top\mathbf y.\]
\PSmall{L’espressione con l’inversa richiede rango pieno. Il diagramma rappresenta uno spazio a $n$ dimensioni mediante uno schema tridimensionale.}
''','L’ortogonalità dei residui esprime il criterio dei minimi quadrati in forma geometrica.')

code(28,'qr','''
X <- model.matrix(m0)
# QR evita di formare esplicitamente
# l'inversa di t(X) %*% X.
b_qr <- qr.coef(qr(X), y)
max(abs(b_qr - coef(m0)))
# Equazioni normali: quasi zero.
max(abs(crossprod(X, residuals(m0))))
''')
S(28,'La decomposizione QR esegue il calcolo',r'''
\[X=QR,\qquad Q^\top Q=I.\]
\[R\hat{\boldsymbol\beta}=Q^\top\mathbf y.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] (a) at(2.3,2.8){Colonne di $X$\\predittori originali};
\node[pFlow,text width=3.8cm] (b) at(7.2,2.8){Colonne di $Q$\\base ortonormale};
\draw[pEdge](a)--(b);
\node[pNote,text width=8.5cm] at(4.8,.9){Un sistema triangolare in $R$ fornisce i coefficienti.};
\end{tikzpicture}
''',r'''
\PCode{R · verificare stima e ortogonalità}{028_qr.R}
\PBody{La formula con l’inversa è utile per ragionare. Per il calcolo numerico \texttt{lm()} usa QR.}
\PInfo{Valori residui dell’ordine della precisione numerica sono compatibili con lo zero teorico. Il controllo usa tolleranze.}
''','Le formule spiegano il problema. Gli algoritmi numerici lo risolvono in modo stabile.')

code(29,'identita','''
# Deviazioni standard con lo stesso denominatore.
b_da_r <- cor(x, y) * sd(y) / sd(x)
c(formula = b_da_r,
  lm = unname(coef(m0)[2]))
# R2 = r^2: solo regressione semplice
# OLS con intercetta, sugli stessi casi.
c(r2 = cor(x, y)^2,
  R2 = summary(m0)$r.squared)
''')
S(29,'Correlazione e pendenza sono collegate',r'''
\[\hat\beta_1=r\frac{s_y}{s_x}.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.3,3.3){$r$\\intensità e segno};
\node[pFlow,text width=3.7cm] (b) at(7.2,3.3){$s_y/s_x$\\rapporto delle scale};
\node[pLabel] (prodotto) at(4.8,1.2){Il prodotto restituisce la pendenza};
\draw[Classical,line width=.95pt](a.south)--(2.3,2.1)--(7.2,2.1)--(b.south);
\draw[pEdge](4.8,2.1)--(prodotto.north);
\end{tikzpicture}
\PInfo{L’identità $R^2=r^2$ riguarda la regressione semplice con intercetta. Nei modelli multipli non si trasferisce a una singola correlazione.}
''',r'''
\PCode{R · controllare due identità}{029_identita.R}
\PBody{Se la dispersione della risposta raddoppia mentre $r$ resta uguale, la pendenza raddoppia a parità di $s_x$.}
''','La pendenza conserva le scale delle variabili, mentre la correlazione le standardizza.')
