from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):SLIDES[n]=dict(title=title,section='VII · VALUTAZIONE SU NUOVI DATI' if n<94 else 'VIII · UN’ANALISI COMPLETA',left=left,right=right,recall=recall)
def code(n,name,s):CODES[f'{n:03}_{name}.R']=s.strip()+'\n'

S(82,'La previsione riguarda casi ancora da osservare',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] (a) at(2.3,4.1){Campione di stima\\formula e coefficienti};
\node[pFlow,text width=3.8cm] (b) at(7.2,4.1){Nuovi esemplari\\predittori disponibili};
\node[pFlow,text width=3.8cm] (c) at(7.2,1.7){Previsioni fissate\\prima della risposta};
\draw[pEdge](a)--(b);\draw[pEdge](b)--(c);
\node[pNote,text width=3.8cm] at(2.3,1.7){Confronto finale con le risposte osservate};
\draw[pEdge](c)--(4.4,1.7);
\end{tikzpicture}
''',r'''
\PBody{Per giudicare la previsione serve una distanza fra costruzione del modello e valutazione. Un errore calcolato sui dati usati per scegliere la formula è ottimistico.}
\PInfo{Le figure precedenti descrivono l’intero campione a scopo didattico. Ora ricostruiamo una procedura con divisione fissata, selezione nel training e test separato. Non è una validazione esterna.}
\PBody{La popolazione futura deve essere compatibile con quella rappresentata dai dati.}
''','La procedura di valutazione deve imitare le condizioni in cui il modello sarà usato.')

code(83,'split','''
# Regola fissata prima della selezione.
is_test <- seq_len(nrow(f)) %% 5L == 0L
training <- f[!is_test, ]
test <- f[is_test, ]
c(training = nrow(training),
  test = nrow(test))
stopifnot(length(intersect(training$id,
                         test$id)) == 0L)
''')
S(83,'La partizione conserva 32 casi per il test',r'''
\begin{tikzpicture}[x=1cm,y=.95cm]
\foreach \r in {0,...,7}{\foreach \c in {0,...,19}{
\pgfmathtruncatemacro{\t}{mod(\c+1,5)}
\ifnum\t=0\def\col{GeoB}\else\def\col{Classical}\fi
\fill[\col!70](.5+\c*.42,1+\r*.4) rectangle(.83+\c*.42,1.28+\r*.4);
}}
\node[pLabel,text=Classical] at(2.8,5){128 training};
\node[pLabel,text=GeoB] at(7.2,5){32 test};
\node[pNote] at(4.8,.35){Un quadrato rappresenta un fossile};
\end{tikzpicture}
\PSmall{Il test include ogni quinta riga: 16 fossili per morfotipo. La regola riproduce i notebook originali.}
\PInfo{In dati reali, ordinamento, stazioni e repliche influenzano la divisione. Questa regola non è una scelta universale.}
''',r'''
\PCode{R · costruire insiemi disgiunti}{083_split.R}
\PSmall{\texttt{intersect()} cerca identificativi presenti in entrambi gli insiemi. Il risultato deve essere vuoto.}
''','Un identificativo deve appartenere a un solo insieme. La partizione va motivata rispetto al campionamento.')

code(84,'riferimento','''
# Il riferimento usa solo il training.
media_train <- mean(
  training$diametro_int_um)
prev_base <- rep(media_train,
                 nrow(test))
media_train
''')
S(84,'La media del training è un riferimento semplice',r'''
\[\hat y_{{\rm base},i}=\bar y_{\rm training}.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.7)--(9,.7);\draw[pAxis](.7,.7)--(.7,5.1);
\draw[GeoB,line width=1.5pt](.8,2.9)--(8.7,2.9);
\foreach \x/\y in {1.2/1.1,2.2/1.8,3.2/2.8,4.2/2.4,5.2/3.5,6.2/3.6,7.2/4.4,8.2/4.7}{\fill[GeoA](\x,\y) circle(2.2pt);}
\node[pLabel,text=GeoB] at(6.4,2.45){$5{,}418\ \mu$m};
\node[pNote] at(4.8,.2){Schema di una previsione costante};
\end{tikzpicture}
\PInfo{La media del test utilizzerebbe risposte ancora ignote nel momento della previsione.}
''',r'''
\PCode{R · fissare il confronto di base}{084_riferimento.R}
\PBody{Il modello aggiunge valore se riduce l’errore rispetto a un riferimento pertinente. Qui la media del training fornisce una previsione costante.}
''','Anche il modello di riferimento deve usare soltanto informazioni disponibili al momento della previsione.')

code(85,'metriche','''
metriche <- function(osservato, previsto) {
  e <- osservato - previsto
  c(MAE = mean(abs(e)),
    RMSE = sqrt(mean(e^2)))
}
# Esempio con scarti noti.
metriche(c(0, 0, 0), c(1, 1, 4))
''')
S(85,'MAE e RMSE pesano gli errori in modo diverso',r'''
\[\operatorname{MAE}=\frac1m\sum_{i=1}^m|y_i-\hat y_i|,\]
\[\operatorname{RMSE}=\sqrt{\frac1m\sum_{i=1}^m(y_i-\hat y_i)^2}.\]
\begin{tikzpicture}[x=1cm,y=.9cm]
\foreach \x/\h/\lab in {2/.8/1,4.6/.8/1,7.2/3.2/4}{\fill[GeoB!60](\x-.45,.4) rectangle(\x+.45,.4+\h);\node[pNote] at(\x,.1){$\lab$};}
\node[pNote] at(4.6,4.2){Errori assoluti dell’esempio};
\end{tikzpicture}
''',r'''
\PCode{R · definire le metriche}{085_metriche.R}
\PSmall{Per gli errori $1,1,4$: MAE $=2$, RMSE $\simeq2{,}449$. La RMSE pesa maggiormente i grandi scarti.}
\PInfo{Le metriche conservano le unità della risposta. La scelta dipende dalle conseguenze degli errori.}
''','Una metrica è una scelta su quali errori contano di più.')

code(86,'fold','''
# Cinque parti interne al solo training.
set.seed(714)
fold <- sample(rep(1:5,
  length.out = nrow(training)))
table(fold)
# Il test esterno non compare nei fold.
''')
_grid=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
for r in range(5):
    _grid.append(rf'\node[pNote,anchor=east] at(1.1,{4.8-r*.72}){{giro {r+1}}};')
    for c in range(5):
        col='GeoB' if r==c else 'Classical'
        _grid.append(rf'\fill[{col}!65]({1.4+c*1.45},{4.5-r*.72}) rectangle({2.7+c*1.45},{5.05-r*.72});')
_grid += [r'\node[pNote,text=GeoB] at(3,.55){validazione interna};\node[pNote,text=Classical] at(7,.55){stima};',r'\end{tikzpicture}']
S(86,'La validazione incrociata riusa il training', '\n'.join(_grid)+r'''\PInfo{Il test di 32 casi resta esterno ai giri. Valuterà la procedura selezionata.}''', r'''
\PCode{R · fissare cinque fold}{086_fold.R}
\PBody{In ogni giro si stima su quattro parti e si prevede la quinta. Ogni caso del training riceve una previsione da un modello che non lo ha usato nella stima.}
''','La validazione incrociata confronta procedure mediante previsioni fuori dalla stima del singolo giro.')

code(87,'trasformazioni','''
# Parametri appresi soltanto nel training.
mu_x <- mean(training$diametro_tot_um)
sd_x <- sd(training$diametro_tot_um)
z_train <- (training$diametro_tot_um - mu_x) / sd_x
z_test <- (test$diametro_tot_um - mu_x) / sd_x
# Nei fold, mu_x e sd_x si ristimano
# ogni volta sui quattro fold di stima.
''')
S(87,'Le trasformazioni fanno parte della procedura',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.3,4.3){Dati di stima\\$\hat\mu_x,\hat s_x$};
\node[pFlow,text width=3.7cm] (b) at(7.2,4.3){Trasformazione fissata\\$z=(x-\hat\mu_x)/\hat s_x$};
\node[pFlow,text width=3.7cm] (c) at(7.2,1.8){Dati da prevedere\\stessa trasformazione};
\draw[pEdge](a)--(b);\draw[pEdge](b)--(c);
\node[pNote,text width=3.6cm] at(2.3,1.8){Vale anche per imputazione e selezione dei predittori.};
\end{tikzpicture}
''',r'''
\PCode{R · standardizzare senza anticipare dati}{087_trasformazioni.R}
\PSmall{La sola standardizzazione lascia invariate le previsioni OLS con intercetta. La regola è essenziale per selezione, penalizzazione e imputazione.}
''','Una trasformazione appresa sui dati deve essere ristimata dentro ogni partizione di addestramento.')

S(88,'Un modello flessibile può inseguire il rumore',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.7)--(9,.7);\draw[pAxis](.7,.7)--(.7,5.1);
\draw[Classical,line width=1.2pt,domain=.9:8.7,samples=80] plot(\x,{1.5+.32*\x});
\draw[GeoB,line width=1.2pt,domain=.9:8.7,samples=100] plot(\x,{1.5+.32*\x+.55*sin(130*\x)});
\foreach \x/\y in {1/2.24,2/1.6,3/2.65,4/2.97,5/2.6,6/3.96,7/3.55,8/3.7}{\fill[Ink](\x,\y) circle(2pt);}
\node[pNote,text=Classical] at(3,5.6){forma semplice};\node[pNote,text=GeoB] at(7,5.6){forma flessibile};
\end{tikzpicture}
''',r'''
\PBody{Aumentare i gradi di libertà permette di seguire più dettagli del campione. Alcuni dettagli possono essere specifici di quel rumore.}
\PBody{La scelta della complessità deve considerare previsioni su casi esclusi dalla stima, oltre alla plausibilità scientifica della forma.}
\PInfo{Lo schema illustra il rischio di sovradattamento. La procedura seguente confronta formule fissate prima del test.}
''','L’errore di training misura l’adattamento ai dati già disponibili e tende a favorire la flessibilità.')

code(89,'cv','''
# Formule definite nel progetto.
formule <- formule_annula()
# Stessi fold per tutti i modelli.
cv <- valida_annula(training, fold,
                   formule)
cv[order(cv$RMSE), ]
scelta <- cv$modello[
  which.min(cv$RMSE)]
''')
S(89,'Le formule si confrontano sugli stessi fold',bars(['Lineare','Con morfotipo','Polinomio cubico'],[.2733109642,.2521794479,.2718532208],.36)+r'''
\PSmall{\texttt{valida\_annula()} esegue \texttt{lm()} e \texttt{predict()} in ogni fold. Il codice completo è in \texttt{R/protocollo.R} e nei notebook N12--N13.}
\PInfo{Differenze piccole possono dipendere dalla partizione. Il criterio e le formule sono fissati prima del test.}
''',r'''
\PCode{R · confrontare la RMSE interna}{089_cv.R}
\PBody{La media delle cinque RMSE è minore per il modello additivo con morfotipo: $0{,}252\ \mu$m. Nessuna risposta del test interviene nella scelta.}
''','Il criterio seleziona una procedura nel training. La sua valutazione finale richiede dati tenuti da parte.')

code(90,'test_finale','''
# Ristima sui 128 casi di training.
mod_finale <- lm(formule[[scelta]],
                 data = training)
prev_test <- predict(mod_finale, newdata = test)
metriche(test$diametro_int_um, prev_test)
metriche(test$diametro_int_um, prev_base)
''')
S(90,'Il modello selezionato incontra il test',bars(['Media training','Con morfotipo'],[1.0029129468,.1994387375],1.25),r'''
\PCode{R · valutazione conclusiva}{090_test_finale.R}
\PBody{Sui 32 casi esclusi dalla stima, la RMSE vale $0{,}199\ \mu$m per il modello e $1{,}003\ \mu$m per la media del training.}
\PSmall{MAE del modello: $0{,}172\ \mu$m. Il risultato riguarda questa partizione didattica dei dati sintetici.}
''','Dopo avere osservato il test, modificare il modello richiede nuovi dati per una valutazione finale indipendente.')

S(91,'Gruppi e tempo richiedono partizioni coerenti',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,anchor=west] at(.7,5.3){Nuove stazioni};
\foreach \x/\lab/\col in {1.7/A/Classical,4/B/Classical,6.3/C/GeoB,8.6/D/Classical}{
\draw[\col,rounded corners=2pt](\x-.7,3.4) rectangle(\x+.7,4.7);
\node[pNote] at(\x,4.45){\lab};
\foreach \y in {3.65,3.95}{\fill[\col](\x-.25,\y) circle(2pt);\fill[\col](\x+.25,\y) circle(2pt);}}
\node[pLabel,anchor=west] at(.7,2.6){Previsioni nel futuro};
\draw[Classical,line width=8pt](.8,1.6)--(6.1,1.6);
\draw[GeoB,line width=8pt](6.3,1.6)--(8.7,1.6);
\draw[pAxis](.8,1)--(9.1,1);
\node[pNote] at(3.3,.5){passato};\node[pNote] at(7.5,.5){futuro};
\end{tikzpicture}
''',r'''
\PBody{Se la domanda riguarda stazioni mai osservate, tutte le misure di una stazione devono rimanere nello stesso insieme.}
\PBody{Per prevedere il futuro, si stima sul passato e si valuta su osservazioni successive. Una divisione casuale può mescolare informazioni temporalmente dipendenti.}
\PInfo{La validazione deve rappresentare il tipo di trasferimento richiesto: nuovo esemplare, nuova stazione o nuovo periodo.}
''','La riga del file e l’unità indipendente di valutazione possono essere diverse.')

code(92,'simulazione','''
# Nuovi dati dalla stessa legge.
set.seed(17)
sim <- data.frame(
  x = seq(-1, 1, length.out = 24))
sim$y <- sin(3 * sim$x) + rnorm(24)
mp <- lm(y ~ poly(x, 3, raw = TRUE),
         data = sim)
nuovi <- data.frame(
  x = seq(-1, 1, length.out = 150))
nuovi$y <- sin(3 * nuovi$x) + rnorm(150)
metriche(nuovi$y,
  predict(mp, newdata = nuovi))
''')
S(92,'La simulazione rende visibile il sovradattamento',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.7)--(9.1,.7);\draw[pAxis](.7,.7)--(.7,5.3);
\draw[Classical,line width=1.3pt,domain=1:8.6,samples=60] plot(\x,{.9+2.7/(\x+1)});
\draw[GeoB,line width=1.3pt,domain=1:8.6,samples=60] plot(\x,{1.9+.11*(\x-4)^2});
\node[pNote,text=Classical] at(7.4,1.1){training};
\node[pNote,text=GeoB] at(6.8,4.8){nuove osservazioni};
\node[pNote] at(4.8,.2){complessità crescente, schema qualitativo};
\end{tikzpicture}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-validazione}{Esperimento: validazione}
\PSmall{Nel sito si varia il grado del polinomio. Sceglierlo guardando questi errori rende i nuovi casi parte della selezione. La verifica finale richiederà un altro campione.}
''',r'''
\PCode{R · nuovi errori dalla stessa legge}{092_simulazione.R}
''','La simulazione consente di osservare la differenza tra adattamento e previsione sotto una legge nota.')

S(93,'Anche una metrica sul test è una stima',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,1)--(9.1,1);
\foreach \x/\h in {1.1/.8,1.6/1.2,2.1/1.7,2.6/2.3,3.1/2.8,3.6/3.4,4.1/3.7,4.6/3.6,5.1/3.1,5.6/2.6,6.1/1.9,6.6/1.4,7.1/.9,7.6/.6,8.1/.3}{\fill[GeoA!45](\x,1) rectangle(\x+.43,1+\h);}
\node[pLabel] at(4.8,5.6){Possibili risultati su altri campioni};
\node[pNote] at(4.8,.4){Schema della variabilità di una metrica};
\end{tikzpicture}
''',r'''
\PBody{La RMSE su 32 casi dipende dai casi disponibili. Una metrica puntuale non descrive tutta l’incertezza sulla prestazione futura.}
\PBody{Repliche della partizione o procedure di ricampionamento possono studiare la stabilità, rispettando gruppi e tempo. Una validazione esterna riguarda anche il trasferimento a un’altra raccolta di dati.}
\PInfo{Il risultato $0{,}199\ \mu$m resta una valutazione interna, legata al protocollo e al campione sintetico.}
''','La generalizzazione richiede sia nuovi casi sia compatibilità tra condizioni di stima e condizioni d’uso.')

S(94,'Una domanda applicativa guida il confronto',r'''
\PLabel{Il diametro totale basta a prevedere quello interno?}
\[M_1:\quad E(Y\mid x)=\beta_0+\beta_1x,\]
\[M_2:\quad E(Y\mid x,G)=\beta_0+\beta_1x+\beta_2G.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.3,2.7){Misure geometriche\\stessa risposta};
\node[pFlow,text width=3.7cm] (b) at(7.2,2.7){Morfotipo disponibile\\informazione aggiuntiva};
\draw[pEdge](a)--(b);
\node[pNote,text width=8.6cm] at(4.8,1){Il gruppo deve essere noto quando si effettua la previsione.};
\end{tikzpicture}
''',r'''
\PBody{Il modello additivo chiede se, a pari diametro totale, i due morfotipi mostrino un livello medio diverso.}
\PBody{L’interazione aggiunge una domanda sulla differenza di pendenza. Va motivata dalla forma e dal processo, oltre che esaminata nei dati.}
\PInfo{Confronto scientifico e valutazione predittiva restano distinti: lo stesso coefficiente può essere utile a descrivere un contrasto senza migliorare molto la previsione.}
''','La scelta dei termini deve riflettere quale confronto scientifico si vuole rappresentare.')

S(95,'Il contrasto fra morfotipi dipende dal modello',r'''
\PLabel{Modello additivo sui 160 casi, analisi descrittiva}
\[\widehat D_{\rm int}=-0{,}798+0{,}990D_{\rm tot}-0{,}228G,\]
\[G=0\ (\text{Rounded}),\qquad G=1\ (\text{Spiky}).\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.7)--(9,.7);\draw[pAxis](.7,.7)--(.7,4.2);
\draw[GeoA,line width=1.4pt](1,1.4)--(8.5,3.9);
\draw[GeoB,line width=1.4pt](1,.95)--(8.5,3.45);
\draw[{Latex}-{Latex},Navy](6,2.62)--(6,3.07);
\node[pNote,anchor=west] at(6.25,2.5){$-0{,}228\ \mu$m};
\end{tikzpicture}
''',r'''
\PBody{A pari diametro totale, il modello additivo stima per Spiky una media inferiore di circa $0{,}228\ \mu$m.}
\PBody{L’IC classico al 95\% del contrasto è $[-0{,}305;-0{,}151]\ \mu$m. Il confronto riguarda l’associazione condizionata nel campione.}
\PInfo{Nel modello con interazione, le pendenze stimate sono $0{,}998$ per Rounded e $0{,}982$ per Spiky. L’intervallo della differenza include lo zero.}
''','Il coefficiente del gruppo descrive un confronto a pari predittore e dipende dai termini inclusi.')

S(96,'La media e il nuovo fossile',r'''
\PLabel{Esempio descrittivo con il modello semplice}
\[D_{\rm tot}=7\ \mu\mathrm m\quad\Longrightarrow\quad \hat D_{\rm int}=5{,}999\ \mu\mathrm m.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.8,.8)--(9,.8);
\draw[GeoA,line width=2pt](1.7,2.3)--(8.1,2.3);
\draw[Classical,line width=3pt](4.6,3.7)--(5.2,3.7);
\fill[Navy](4.9,2.3) circle(3pt);\fill[Navy](4.9,3.7) circle(3pt);
\node[pNote,anchor=west] at(.9,4.5){Media: $[5{,}950;6{,}047]\ \mu$m};
\node[pNote,anchor=west] at(.9,1.6){Individuo: $[5{,}484;6{,}514]\ \mu$m};
\node[pNote] at(4.9,.3){stessa scala e stesso livello 95\%};
\end{tikzpicture}
''',r'''
\PBody{Per descrivere una popolazione di fossili di diametro totale $7\ \mu$m, interessa la media condizionata. Per un nuovo fossile, interessa l’intervallo individuale.}
\PBody{Il valore cade nel dominio osservato. Restano da considerare forma, omogeneità della varianza e ragioni di eventuali differenze di gruppo.}
\PInfo{Questi intervalli appartengono al modello semplice sull’intero campione. Non sono gli intervalli del modello selezionato sul training.}
''','Precisare modello e quantità prevista evita di attribuire un intervallo alla domanda sbagliata.')

code(97,'logistica_test','''
# Risposta: TRUE per i fossili Spiky.
g_train <- glm(
  I(morfotipo == "Spiky") ~
    diametro_tot_um +
    rapporto_int_tot,
  data = training,
  family = binomial())
p_test <- predict(g_train,
  newdata = test, type = "response")
y_test <- as.integer(
  test$morfotipo == "Spiky")
mean((p_test - y_test)^2) # Brier.
mean((p_test >= 0.5) == y_test)
''')
S(97,'Probabilità e classi hanno valutazioni distinte',r'''
\PLabel{Spiky come risposta binaria, test di 32 casi}
\begin{tabular}{lcc}
\toprule\textbf{Osservato}&\textbf{\shortstack{Previsto\\Rounded}}&\textbf{\shortstack{Previsto\\Spiky}}\\\midrule
Rounded&12&4\\[2mm]
Spiky&4&12\\\bottomrule
\end{tabular}
\vspace{4mm}
\[\text{accuratezza}=0{,}75\qquad (\text{soglia }0{,}5),\]
\[\operatorname{Brier}=0{,}159\quad\text{contro }0{,}250\text{ del riferimento}.\]
\PSmall{Le probabilità e la soglia hanno ruoli diversi. La matrice dipende dalla soglia, il Brier usa direttamente le probabilità.}
''',r'''
\PCode{R · valutare probabilità fuori stima}{097_logistica_test.R}
\PSmall{Le misure geometriche devono essere note quando si prevede il morfotipo.}
''','Una buona classificazione a una soglia non garantisce probabilità ben calibrate.')

S(98,'Una variabile derivata può rivelare la risposta',r'''
\[q=\frac{D_{\rm int}}{D_{\rm tot}}\quad\Longrightarrow\quad D_{\rm int}=qD_{\rm tot}.\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.3,3.5){Risposta da prevedere\\$D_{\rm int}$};
\node[pFlow,text width=3.7cm] (b) at(7.2,3.5){Predittore costruito\\$q=D_{\rm int}/D_{\rm tot}$};
\draw[pEdge,GeoB](a)--(b);
\draw[pEdge,GeoB](b.south)--(7.2,1.8)--(2.3,1.8)--(a.south);
\node[pNote,fill=Paper] at(4.8,1.8){informazione sulla risposta};
\end{tikzpicture}
''',r'''
\PBody{Se la domanda è prevedere il diametro interno prima di misurarlo, il rapporto interno/totale contiene già l’informazione cercata.}
\PBody{Nella classificazione del morfotipo, invece, le due misure possono essere predittori legittimi se disponibili al momento d’uso.}
\PInfo{Il controllo riguarda la domanda e la sequenza di misura. Una colonna può essere appropriata in un’analisi e creare contaminazione in un’altra.}
''','La disponibilità del predittore nel file non garantisce la sua disponibilità nella previsione reale.')

S(99,'Il confronto conserva stima e valutazione separate',r'''
\PLabel{Stesso training, stessi fold, stesso test}
\begin{tabular}{lcc}
\toprule\textbf{Procedura}&\textbf{RMSE CV}&\textbf{RMSE test}\\\midrule
Media del training&---&$1{,}003$\\[2mm]
Lineare semplice&$0{,}273$&---\\[2mm]
Con morfotipo&$0{,}252$&$0{,}199$\\[2mm]
Polinomio cubico&$0{,}272$&---\\\bottomrule
\end{tabular}
\vspace{3mm}
\PSmall{Valori in $\mu$m. Il test valuta la procedura selezionata e il riferimento fissato. Non viene usato per scegliere fra le tre formule.}
''',r'''
\PBody{L’informazione di gruppo migliora la previsione interna in questo esempio. La metrica finale è inferiore anche al riferimento costante.}
\PBody{Il risultato non dimostra un meccanismo causale né garantisce la stessa prestazione in un altro ambiente deposizionale.}
\PInfo{Confrontare ripetutamente tutti i modelli sul test e scegliere il migliore trasformerebbe il test in un insieme di selezione.}
''','Una conclusione predittiva deve nominare procedura, confronto, unità e popolazione a cui si riferisce.')

S(100,'Una relazione utile conserva il proprio dominio',r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.8cm] (a) at(2.3,4.7){Domanda scientifica\\variabili e misure disponibili};
\node[pFlow,text width=3.8cm] (b) at(7.2,4.7){Modello condizionato\\forma e coefficienti};
\node[pFlow,text width=3.8cm] (c) at(2.3,1.9){Diagnostica\\compatibilità con le ipotesi};
\node[pFlow,text width=3.8cm] (d) at(7.2,1.9){Nuovi casi\\errore e condizioni d’uso};
\draw[pEdge](a)--(b);\draw[pEdge](b)--(d);\draw[pEdge](c)--(d);\draw[pEdge](b.south west)--(c.north east);
\end{tikzpicture}
''',r'''
\PBody{Nei fossili sintetici, il diametro totale descrive gran parte della variazione del diametro interno. Il morfotipo aggiunge informazione condizionata.}
\PBody{La geometria contribuisce all’associazione. Gli intervalli distinguono media e individuo, mentre il test separato misura l’errore della procedura selezionata.}
\PInfo{La conclusione resta legata a misure, dominio e campionamento. Un nuovo contesto richiede nuove verifiche.}
''','Una regressione è interpretabile quando domanda, modello, incertezza e valutazione riguardano lo stesso problema.')
