from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):SLIDES[n]=dict(title=title,section='III · INCERTEZZA E PREVISIONE',left=left,right=right,recall=recall)
def code(n,name,s):CODES[f'{n:03}_{name}.R']=s.strip()+'\n'

code(30,'scomposizione','''
SST <- sum((y - mean(y))^2)
SSE <- sum(residuals(m0)^2)
SSR <- sum((fitted(m0) - mean(y))^2)
c(totale = SST, modello = SSR,
  residua = SSE)
all.equal(SST, SSR + SSE)
''')
S(30,'La variabilità si scompone con l’intercetta',r'''
\[y_i-\bar y=(\hat y_i-\bar y)+e_i.\]
\[\underbrace{\sum_i(y_i-\bar y)^2}_{SST}
=\underbrace{\sum_i(\hat y_i-\bar y)^2}_{SSR}
+\underbrace{\sum_i e_i^2}_{SSE}.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\fill[Classical!60](.5,1.5) rectangle(8.4,2.2);
\fill[GeoB!70](8.4,1.5) rectangle(9,2.2);
\node[pNote] at(4.3,1){variabilità della media stimata};
\node[pNote,text=GeoB,anchor=east] at(9,2.65){residua};
\end{tikzpicture}
\PSmall{La scomposizione usa l’ortogonalità dei residui. Vale per OLS con intercetta sugli stessi casi.}
''',r'''
\PCode{R · verificare le somme dei quadrati}{030_scomposizione.R}
\PBody{Per i fossili, $SST=156{,}647$ e $SSE=10{,}646\ \mu\mathrm m^2$. Una retta riduce molto lo scarto rispetto alla sola media.}
\PInfo{Il confronto descrive l’adattamento sui dati usati per stimare il modello.}
''','La somma dei quadrati residua misura la parte rimasta attorno alla media stimata.')

S(31,'R quadrato misura una riduzione relativa',r'''
\[R^2=1-\frac{SSE}{SST}=0{,}932.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[Rule,line width=12pt](.9,3.1)--(9,3.1);
\draw[Classical,line width=12pt](.9,3.1)--(8.449,3.1);
\node[pLabel] at(4.7,4.1){$93{,}2\%$ della somma dei quadrati};
\node[pNote] at(1,2.35){0};\node[pNote] at(9,2.35){1};
\node[pNote,text width=8.5cm] at(4.8,1){Confronto con la previsione costante $\bar y$};
\end{tikzpicture}
''',r'''
\PBody{Nel campione, la retta riduce la somma dei quadrati del $93{,}2\%$ rispetto alla media.}
\PBody{Il valore non significa che il $93{,}2\%$ dei fossili abbia una previsione corretta. Per quantificare gli errori in micrometri serve una misura sulla scala della risposta.}
\PInfo{La relazione geometrica tra le variabili contribuisce al valore elevato di $R^2$.}
''','R quadrato è una misura relativa di adattamento, riferita a una precisa risposta e a un preciso campione.')

S(32,'Un R quadrato alto lascia aperte altre domande',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,anchor=west] at(.7,4.8){Adattamento nel campione};
\draw[Classical,line width=4pt](.8,4.15)--(8.6,4.15);
\node[pLabel,anchor=west] at(.7,3.25){Forma corretta della relazione};
\node[pNote,anchor=west] at(.8,2.65){I residui possono mostrare una curvatura.};
\node[pLabel,anchor=west] at(.7,1.65){Previsione per nuovi casi};
\node[pNote,anchor=west] at(.8,1.05){Occorre osservare errori su dati esclusi dalla stima.};
\end{tikzpicture}
''',r'''
\PBody{Aggiungendo termini a un modello OLS annidato, la somma dei quadrati nel training non aumenta. Il valore di $R^2$ può crescere anche con termini inutili.}
\PBody{Il confronto tra modelli deve quindi considerare diagnostica, complessità e prestazioni su nuovi casi.}
\PInfo{Per confrontare $R^2$ tra modelli, risposta e casi devono coincidere. Una trasformazione della risposta cambia il confronto.}
''','La bontà dell’adattamento non basta per scegliere la complessità o sostenere una previsione.')

code(33,'sigma','''
e <- residuals(m0)
n <- nobs(m0)
p <- m0$rank
s <- sqrt(sum(e^2) / (n - p))
c(calcolo = s, R = sigma(m0))
# RMSE in campione usa invece n.
sqrt(mean(e^2))
''')
S(33,'La dispersione residua conserva le unità',r'''
\[s^2=\frac{\sum_i e_i^2}{n-p},\qquad s=0{,}260\ \mu\mathrm m.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,2.6)--(9.2,2.6);
\draw[GeoA,line width=1.3pt,domain=.9:8.8,samples=65] plot(\x,{2.6+1.8*exp(-((\x-4.8)^2)/2)});
\draw[GeoB,line width=1.2pt](3.8,2.4)--(5.8,2.4);
\node[pNote] at(4.8,1.7){Scala degli scarti attorno alla media};
\node[pNote] at(4.8,4.9){Schema di errori a varianza costante};
\end{tikzpicture}
''',r'''
\PCode{R · stimare la deviazione residua}{033_sigma.R}
\PBody{Si sottraggono i $p$ coefficienti stimati dai $n$ dati. Qui $n-p=158$. Sotto le ipotesi classiche, $s^2$ stima $\sigma^2$.}
\PInfo{$s$ e RMSE nel campione usano denominatori diversi. Entrambi sono espressi in micrometri, ma hanno ruoli differenti.}
''','La deviazione residua misura una scala di variabilità condizionata, non l’errore della pendenza.')

S(34,'La precisione della pendenza dipende dal disegno',r'''
\[\operatorname{SE}(\hat\beta_1)=\frac{s}{\sqrt{\sum_i(x_i-\bar x)^2}}.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,1.6)--(9,1.6);\draw[pAxis](.7,3.6)--(9,3.6);
\foreach \x in {3.6,3.85,4.1,4.35,4.6,4.85,5.1,5.35,5.6}{\fill[GeoB](\x,3.6) circle(2.8pt);}
\foreach \x in {1.1,2,2.9,3.8,4.7,5.6,6.5,7.4,8.3}{\fill[Classical](\x,1.6) circle(2.8pt);}
\node[pNote] at(4.8,4.3){predittore concentrato};
\node[pNote] at(4.8,.7){stesso numero di casi, campo più ampio};
\end{tikzpicture}
''',r'''
\PBody{A parità di $s$, una maggiore dispersione di $X$ riduce l’errore standard della pendenza. Una maggiore variabilità residua lo aumenta.}
\PBody{Ampliare il campo di misura può migliorare la precisione, purché la forma del modello e la popolazione restino appropriate.}
\PInfo{La formula assume errori a varianza costante e non correlati. Con dipendenze spaziali o temporali occorre un modello della covarianza.}
''','La precisione dipende sia dal numero di osservazioni sia da dove si trovano i predittori.')

code(35,'ci_coef','''
# Intervalli t sotto le ipotesi classiche.
confint(m0, level = 0.95)
# La tabella riporta anche gli errori standard.
coef(summary(m0))
''')
S(35,'Un intervallo accompagna la stima della pendenza',r'''
\[\hat\beta_1\pm t_{n-p,\,1-\alpha/2}\operatorname{SE}(\hat\beta_1).\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,1.3)--(9.2,1.3);
\foreach \x/\lab in {1.2/{0,90},4.7/{0,95},8.2/{1,00}}{\node[pNote] at(\x,.8){$\lab$};}
\draw[Classical,line width=2pt](2.347,2.8)--(8.032,2.8);
\foreach \x in {2.347,8.032}{\draw[Classical](\x,2.55)--(\x,3.05);}
\fill[Classical](5.19,2.8) circle(3.3pt);
\node[pLabel] at(5.19,3.75){$0{,}957$};
\node[pNote] at(4.8,4.6){IC 95\%: $[0{,}916;\ 0{,}998]$};
\end{tikzpicture}
\PInfo{La copertura del 95\% riguarda la procedura in campioni ripetuti sotto le ipotesi, come discusso in Pelago.}
''',r'''
\PCode{R · intervalli dei coefficienti}{035_ci_coef.R}
\PBody{L’intervallo descrive l’incertezza della pendenza nel modello dichiarato. Non incorpora automaticamente errori di misura, distorsioni del campionamento o una forma media sbagliata.}
''','Un intervallo richiede un parametro definito, una procedura e condizioni esplicite.')

S(36,'L’intervallo per la risposta media',r'''
\PLabel{Media condizionata a un valore fissato}
\[\hat y_0=\hat\beta_0+\hat\beta_1x_0,\qquad
h_0=\frac1n+\frac{(x_0-\bar x)^2}{S_{xx}}.\]
\[\operatorname{SE}(\hat y_0)=s\sqrt{h_0}.\]
\[\boxed{\hat y_0\pm t_{n-p,\,1-\alpha/2}\,s\sqrt{h_0}}\]
\PBody{L’intervallo riguarda $E(Y\mid X=x_0)$. È più stretto vicino a $\bar x$, dove il disegno sostiene meglio la stima della media.}
''',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,.7)--(7,.7);\draw[pAxis](.6,.7)--(.6,5.3);
\draw[Classical,line width=1.2pt](1,1.4)--(6.6,4.3);
\foreach \x/\y/\s in {1.4/1.61/.55,3.8/2.85/.22,6.2/4.09/.55}{\draw[GeoB,line width=2pt](\x,\y-\s)--(\x,\y+\s);\fill[Classical](\x,\y) circle(2pt);}
\node[pNote] at(3.8,.25){$\bar x$};
\node[pNote,text width=6.2cm] at(3.8,5.65){Schema di intervalli della media};
\end{tikzpicture}
\PSmall{Per un modello multiplo, $h_0=\mathbf x_0^\top(X^\top X)^{-1}\mathbf x_0$, con intercetta inclusa in $\mathbf x_0$.}
''','L’intervallo della media quantifica l’incertezza sulla posizione della funzione media.')

S(37,'Un nuovo individuo aggiunge la propria variabilità',r'''
\[Y_{\rm nuovo}-\hat y_0=\varepsilon_{\rm nuovo}+
\{E(Y\mid x_0)-\hat y_0\}.\]
\[\operatorname{SE}_{\rm pred}=s\sqrt{1+h_0}.\]
\[\boxed{\hat y_0\pm t_{n-p,\,1-\alpha/2}\,s\sqrt{1+h_0}}\]
\PBody{Il termine $1$ corrisponde alla variabilità del nuovo individuo. L’altro termine riguarda la stima della media.}
''',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,2.5)--(7,2.5);
\draw[GeoA!50,line width=7pt](1.1,3.8)--(6.6,3.8);
\draw[Classical,line width=7pt](3.2,1.3)--(4.5,1.3);
\fill[Navy](3.85,3.8) circle(3pt);\fill[Navy](3.85,1.3) circle(3pt);
\node[pNote] at(3.85,4.5){nuovo individuo};
\node[pNote] at(3.85,.55){risposta media};
\end{tikzpicture}
\PInfo{La previsione classica assume un nuovo errore indipendente, con la stessa varianza. La normalità rende esatta la copertura t a campione finito.}
''','Una media stimata con precisione può convivere con una forte variabilità individuale.')

S(38,'Le due bande rispondono a domande differenti',scatter(fit=True,band=True),r'''
\PLabel{Stesso modello e stesso livello 95\%}
\PBody{La banda interna verde riguarda la risposta media. La banda esterna azzurra riguarda una nuova osservazione.}
\vspace{2mm}
\PBody{I punti sono i 160 fossili sintetici. La retta e le bande derivano dal modello semplice con intercetta.}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-previsione}{Esperimento: previsione}
\PInfo{Sono intervalli puntuali al variare di $x$. La copertura simultanea dell’intera curva richiede una procedura diversa.}
''','Il livello nominale coincide, mentre cambia la quantità a cui si riferisce l’intervallo.')

code(39,'predict','''
nuovo <- data.frame(diametro_tot_um = 7)
# Incertezza della media condizionata.
predict(m0, newdata = nuovo,
        interval = "confidence")
# Variabilita di un nuovo individuo.
predict(m0, newdata = nuovo,
        interval = "prediction")
''')
_q=[r for r in VALUES['intervalli_esempi'] if float(r['x'])==7][0]
_media=rf"\PSmall{{A $x_0=7\ \mu$m, la previsione media è ${it(_q['fit'])}\ \mu$m. L’intervallo della media è $[{it(_q['ic_lwr'])};\ {it(_q['ic_upr'])}]$ e quello individuale $[{it(_q['ip_lwr'])};\ {it(_q['ip_upr'])}]$.}}"
S(39,'predict distingue media e osservazione',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] (a) at(2.3,3.8){\texttt{confidence}\\$E(Y\mid x_0)$};
\node[pFlow,text width=3.8cm] (b) at(7.2,3.8){\texttt{prediction}\\$Y_{\rm nuovo}\mid x_0$};
\node[pLabel,text width=8.5cm] at(4.8,1.9){\texttt{fit}\quad stima centrale\qquad \texttt{lwr}, \texttt{upr}\quad estremi};
\end{tikzpicture}
'''+_media,r'''
\PCode{R · richiedere l’intervallo corretto}{039_predict.R}
\PSmall{\texttt{newdata} deve contenere nomi e tipi coerenti con la formula. Per i gruppi servono livelli già presenti nella stima.}
\PInfo{Il livello predefinito è 0,95. Una scelta diversa va dichiarata con \texttt{level}.}
''','L’argomento interval esprime la domanda statistica, non una preferenza grafica.')

code(40,'estrapolazione','''
# Lo stesso comando produce numeri
# anche fuori dal campo osservato.
fuori <- data.frame(diametro_tot_um = 11)
predict(m0, newdata = fuori,
        interval = "prediction")
range(f$diametro_tot_um)
''')
S(40,'La formula continua oltre i dati',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.6)--(9.2,.6);\draw[pAxis](.7,.6)--(.7,5.3);
\fill[GeoA!10](.8,.7) rectangle(5.2,5.1);
\draw[Classical,line width=1.3pt](1,1.1)--(8.7,4.25);
\draw[GeoB,line width=1.3pt,domain=1:8.7,samples=60] plot(\x,{1+.18*\x+.035*\x*\x});
\draw[Muted,dashed](5.2,.6)--(5.2,5.2);
\node[pNote] at(3,5.6){campo osservato};\node[pNote] at(7.3,5.6){estrapolazione};
\node[pNote,text=Classical] at(7.3,2.4){retta};\node[pNote,text=GeoB] at(7.3,4.9){curva possibile};
\end{tikzpicture}
''',r'''
\PCode{R · riconoscere un caso esterno}{040_estrapolazione.R}
\PBody{Il calcolo dell’intervallo non protegge da una forma media sbagliata fuori dal campione. Il modello potrebbe trascurare soglie, limiti fisici o cambiamenti di processo.}
\PSmall{Il diagramma confronta due andamenti ipotetici che divergono oltre il campo osservato.}
''','Un intervallo numerico oltre il dominio resta condizionato all’ipotesi di continuazione del modello.')

S(41,'Campione, distanza e variabilità',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,anchor=west] at(.5,5){Più dati nella stessa popolazione};
\node[pNote,anchor=west] at(.7,4.35){Riduzione dell’incertezza della media, a disegno comparabile.};
\node[pLabel,anchor=west] at(.5,3.2){Nuovo valore lontano da $\bar x$};
\node[pNote,anchor=west] at(.7,2.55){Aumento del termine $h_0$ e degli intervalli.};
\node[pLabel,anchor=west] at(.5,1.4){Maggiore dispersione individuale};
\node[pNote,anchor=west] at(.7,.75){Aumento di $s$ e di entrambe le incertezze.};
\end{tikzpicture}
''',r'''
\[\operatorname{SE}_{\rm media}=s\sqrt{h_0},\qquad
\operatorname{SE}_{\rm pred}=s\sqrt{1+h_0}.\]
\PBody{Anche se $h_0$ diventa molto piccolo, l’incertezza individuale resta legata a $s$. Aumentare il campione non elimina la variabilità dei nuovi esemplari.}
\PInfo{Queste relazioni valgono nel modello. Prima di usarle occorre esaminare forma media, varianza e dipendenze.}
''','La diagnostica controlla se il modello offre una base adeguata per le formule d’incertezza.')
