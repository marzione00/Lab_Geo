"""Annula M07, slide 42–81. Testi e diagrammi nativi LaTeX/TikZ."""
from math import exp, sin, cos

SLIDES = {}
CODES = {}


def S(n, title, left, right, recall):
    section = ('IV · DIAGNOSTICA' if n <= 55 else
               'V · PREDITTORI E INTERAZIONI' if n <= 70 else
               'VI · RISPOSTE BINARIE')
    SLIDES[n] = dict(title=title, section=section,
                     left=left.strip(), right=right.strip(), recall=recall)


def code(n, name, text):
    filename = f'{n:03}_{name}.R'
    CODES[filename] = text.strip() + '\n'
    return filename


def axes(xlabel, ylabel, width=8.4, height=3.5):
    return (r'\begin{tikzpicture}[x=1cm,y=1cm]' + '\n' +
            rf'\draw[pAxis](.65,.5)--({width+.65},.5);' + '\n' +
            rf'\draw[pAxis](.65,.5)--(.65,{height+.5});' + '\n' +
            rf'\node[pNote] at({width/2+.65},.08){{{xlabel}}};' + '\n' +
            rf'\node[pNote,anchor=west] at(.7,{height+.75}){{{ylabel}}};' + '\n')


def residual_cloud(kind='random'):
    out=[axes(r'Valore stimato $\widehat y$', r'Residuo $e$ · schema')]
    out += [r'\draw[Muted,dashed](.65,2.2)--(8.95,2.2);',
            r'\node[pNote,anchor=east] at(.55,2.2){0};']
    for i in range(42):
        x=.9+7.7*i/41
        base=.6*sin(i*2.37)+.13*cos(i*5.1)
        if kind=='curve': y=1.65+.065*(x-4.7)**2+.24*base
        elif kind=='fan': y=2.2+base*(.12+.22*(x-.9))
        else: y=2.2+base
        out.append(rf'\fill[GeoA,opacity=.8]({x:.3f},{y:.3f}) circle(1.7pt);')
    if kind=='curve':
        out.append(r'\draw[GeoB,line width=1.2pt,domain=.9:8.6,samples=60] plot(\x,{1.65+.065*(\x-4.7)^2});')
    elif kind=='fan':
        out += [r'\draw[GeoB,dashed](.9,2.35)--(8.6,3.62);',r'\draw[GeoB,dashed](.9,2.05)--(8.6,.78);']
    out.append(r'\end{tikzpicture}')
    return '\n'.join(out)


def lines_plot(interaction=False, contrast=False):
    out=[axes(r'Diametro totale $x$ · schema', r'Diametro interno medio')]
    out += [r'\draw[GeoA,line width=1.4pt](1,1)--(8.4,2.75);']
    yend=2.15 if interaction else 2.45
    ystart=.75 if interaction else .7
    out += [rf'\draw[GeoB,line width=1.4pt](1,{ystart})--(8.4,{yend});',
            r'\node[pNote,text=GeoA,anchor=east] at(8.5,3.05){Rounded};',
            rf'\node[pNote,text=GeoB,anchor=east] at(8.5,{yend-.35}){{Spiky}};']
    for xx in ([2.5,6.4] if contrast else [4.8]):
        ya=1+(xx-1)*1.75/7.4
        yb=ystart+(xx-1)*(yend-ystart)/7.4
        out.append(rf'\draw[<->,Classical,line width=1pt]({xx:.3f},{ya:.3f})--({xx:.3f},{yb:.3f});')
        if contrast:out.append(rf'\node[pNote] at({xx:.3f},.82){{$x_{1 if xx<4 else 2}$}};')
    out.append(r'\end{tikzpicture}')
    return '\n'.join(out)


code(42,'residui',r'''
# m0 descrive il diametro interno.
e42 <- residuals(m0)
yhat42 <- fitted(m0)
plot(yhat42, e42, pch = 19,
     xlab = "Valore stimato (um)",
     ylab = "Residuo (um)")
abline(h = 0, lty = 2)
# La curva locale aiuta la lettura.
lines(lowess(yhat42, e42), col = 2)
''')
S(42,'Residui e valori stimati',
  r'\PLabel{Una figura per la forma media}' + residual_cloud() + r'''
\PBody{Ogni punto associa il residuo di un fossile al suo valore stimato. Una struttura sistematica può indicare informazione che il modello lascia nei residui.}
''',r'''
\PCode{R · residui e curva locale}{042_residui.R}
\PSmall{\texttt{residuals()} restituisce $y_i-\widehat y_i$. \texttt{fitted()} restituisce i valori stimati sulle righe usate nel modello.}
\PSmall{La curva locale va letta tenendo conto della numerosità.}
''','Un residuo è uno scarto stimato. La sua struttura suggerisce quali aspetti del modello riesaminare.')

code(43,'vincoli',r'''
# Con intercetta e minimi quadrati:
e43 <- residuals(m0)
c(somma = sum(e43),
  media = mean(e43))
# Anche X trasposta per e e' quasi 0.
X43 <- model.matrix(m0)
drop(crossprod(X43, e43))
''')
S(43,'La media dei residui e i pattern',r'''
\PLabel{Un vincolo prodotto dalla stima}
\[
\sum_{i=1}^n e_i=0,\qquad \mathbf X^\top\mathbf e=\mathbf0
\]
\PBody{Nel modello dei minimi quadrati con intercetta, residui positivi e negativi si compensano. Questa proprietà vale anche quando la relazione media ha una forma inadeguata.}
\vspace{3mm}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,1.5)--(9,1.5);
\foreach \x/\v in {1/.9,2/.5,3/-.6,4/-.8,5/-.8,6/-.6,7/.5,8/.9}{
\draw[GeoA,line width=2pt](\x,1.5)--(\x,{1.5+\v});}
\node[pNote] at(4.7,.05){Scarti che si compensano, ma con andamento curvo};
\end{tikzpicture}
''',r'''
\PCode{R · controllare le identità}{043_vincoli.R}
\PSmall{Valori dell’ordine dell’errore numerico rappresentano lo zero. Una media residua quasi nulla, da sola, non dimostra che il modello descriva bene i dati.}
''','I vincoli algebrici della stima vanno distinti dalle ipotesi sul processo che ha generato le osservazioni.')

code(44,'curvatura',r'''
# Aggiungiamo un termine quadratico.
m_quad <- lm(diametro_int_um ~
  diametro_tot_um +
  I(diametro_tot_um^2), data = f)
plot(fitted(m_quad), resid(m_quad),
     pch = 19, xlab = "Stima (um)",
     ylab = "Residuo (um)")
abline(h = 0, lty = 2)
''')
S(44,'Curvatura della risposta media',
  r'\PLabel{Un andamento che resta nei residui}' + residual_cloud('curve') + r'''
\PBody{Una curva nei residui suggerisce di rivedere $E(Y\mid x)$. Un termine quadratico è una possibilità da motivare e poi valutare su nuovi dati.}
''',r'''
\[
E(Y\mid x)=\beta_0+\beta_1x+\beta_2x^2
\]
\PCode{R · una forma media alternativa}{044_curvatura.R}
\PSmall{\texttt{I(x\^{}2)} chiede a R di calcolare il quadrato. Aggiungere un termine riduce o lascia invariata la somma degli scarti sul campione di stima.}
''','Una maggiore flessibilità deve risolvere un problema scientifico e mantenere capacità predittiva fuori campione.')

code(45,'dispersione',r'''
# Scala dei residui standardizzati.
rs45 <- rstandard(m0)
plot(fitted(m0), sqrt(abs(rs45)),
     pch = 19, xlab = "Stima (um)",
     ylab = "Radice di |residuo std| ")
lines(lowess(fitted(m0),
             sqrt(abs(rs45))), col = 2)
''')
S(45,'Varianza condizionale variabile',
  r'\PLabel{Una dispersione a ventaglio}' + residual_cloud('fan') + r'''
\PBody{Qui la dispersione cresce con il valore stimato. La media può essere ben descritta, mentre l’ipotesi di varianza costante richiede una revisione.}
''',r'''
\[
\operatorname{Var}(Y\mid x)=\sigma^2(x)
\]
\PCode{R · il grafico della dispersione}{045_dispersione.R}
\PSmall{La trasformazione, un modello della varianza o errori standard robusti rispondono a obiettivi diversi. Pesi arbitrari non risolvono il problema.}
''','Forma della media e dispersione condizionale sono proprietà diverse, da controllare separatamente.')

code(46,'ordine',r'''
# Esempio simulato: errori correlati.
set.seed(746)
e46 <- as.numeric(arima.sim(
  model = list(ar = 0.75), n = 80))
plot(e46, type = "b",
     xlab = "Ordine temporale",
     ylab = "Errore simulato")
abline(h = 0, lty = 2)
acf(e46, main = "Autocorrelazione")
''')
S(46,'Residui e ordine delle osservazioni',r'''
\PLabel{Il tempo o la posizione aggiungono informazione}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,1.8)--(9,1.8);
\draw[pAxis](.6,.5)--(.6,3.5);
\draw[GeoA,line width=1.1pt] plot[smooth] coordinates{(.9,2)(1.3,2.4)(1.7,2.8)(2.1,2.5)(2.5,2.7)(2.9,2)(3.3,1.1)(3.7,.9)(4.1,1.3)(4.5,1)(4.9,1.6)(5.3,2.3)(5.7,2.8)(6.1,2.5)(6.5,2.2)(6.9,1.4)(7.3,1)(7.7,1.3)(8.1,1.8)(8.5,2.1)};
\node[pNote,anchor=west] at(.7,3.85){Residui ordinati · schema};
\node[pNote] at(4.8,.1){Ordine temporale oppure distanza lungo un transetto};
\end{tikzpicture}
\PBody{Sequenze di residui con lo stesso segno possono segnalare dipendenza. L’ordine delle righe ha significato soltanto se corrisponde al disegno di raccolta.}
''',r'''
\PCode{R · una dipendenza simulata}{046_ordine.R}
\PSmall{\texttt{acf()} confronta una serie con copie ritardate. Nel file dei fossili, l’identificativo non rappresenta automaticamente il tempo o la distanza.}
''','La verifica dell’indipendenza comincia dal disegno di campionamento e dal significato dell’ordine delle osservazioni.')

S(47,'Dipendenza entro stazioni',r'''
\PLabel{Unità raggruppate sul terreno}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \xx/\lab/\col in {1.6/A/GeoA,4.7/B/GeoB,7.8/C/GeoC}{
\draw[\col,fill=\col!6,rounded corners=2mm](\xx-1.25,.7) rectangle(\xx+1.25,3.55);
\node[pLabel,text=\col] at(\xx,3.15){Stazione \lab};
\foreach \dx/\dy in {-.55/1.4,.5/1.2,-.35/2.1,.55/2.2}{\fill[\col](\xx+\dx,\dy) circle(3pt);}}
\node[pNote] at(4.7,.2){Più campioni possono condividere la stessa condizione locale};
\end{tikzpicture}
\PBody{Campioni della stessa stazione possono condividere litologia, storia e strumenti. Aumentare le righe entro una stazione non equivale ad aggiungere stazioni indipendenti.}
''',r'''
\[
Y_{ij}=\beta_0+\beta_1x_{ij}+b_j+\varepsilon_{ij}
\]
\PSmall{$j$ identifica la stazione. Il contributo comune $b_j$ induce una somiglianza tra osservazioni dello stesso gruppo.}
\vspace{3mm}
\PBody{Un modello con struttura di gruppo o una procedura che rispetti i gruppi può essere necessario. Nella validazione, tenere insieme i campioni della stessa stazione evita che informazione locale passi da training a test.}
\PInfo{Schema concettuale per dati di campo. I fossili sintetici del corso non contengono una variabile stazione.}
''','Il numero delle righe e il numero delle unità indipendenti possono essere diversi.')

code(48,'qqplot',r'''
# Quantili dei residui standardizzati.
rs48 <- rstandard(m0)
qqnorm(rs48, pch = 19,
       xlab = "Quantile normale",
       ylab = "Residuo standardizzato")
qqline(rs48, col = 2)
''')
S(48,'QQ plot dei residui',r'''
\PLabel{Un confronto tra quantili}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.65,.5)--(8.9,.5);\draw[pAxis](.65,.5)--(.65,4.05);
\draw[Muted,dashed](1,.8)--(8.2,3.65);
\foreach \x/\y in {1.1/.65,1.6/.9,2.2/1.2,2.8/1.5,3.4/1.75,4/1.98,4.6/2.22,5.2/2.45,5.8/2.68,6.4/2.91,7/3.3,7.6/3.65,8.1/3.95}{\fill[GeoA](\x,\y) circle(2pt);}
\node[pNote] at(4.8,.08){Quantile della normale di riferimento};
\node[pNote,anchor=west] at(.7,4.35){Quantile residuo · schema};
\end{tikzpicture}
\PBody{Scostamenti nelle code richiedono attenzione alle osservazioni estreme e agli intervalli. Il grafico valuta l’approssimazione normale degli errori, tenendo conto che i residui derivano da un modello stimato.}
''',r'''
\PCode{R · quantili e retta di riferimento}{048_qqplot.R}
\[
r_i=\frac{e_i}{s\sqrt{1-h_{ii}}}
\]
\PSmall{La normalità serve per l’inferenza classica esatta a campione finito. La stima dei coefficienti con minimi quadrati non richiede, da sola, errori normali.}
''','Un QQ plot quasi rettilineo sostiene un’approssimazione, senza dimostrare tutte le ipotesi del modello.')

code(49,'leva',r'''
# La leva dipende dalla matrice X.
h49 <- hatvalues(m0)
plot(f$diametro_tot_um, h49,
     pch = 19, xlab = "Diametro (um)",
     ylab = "Leva")
c(somma = sum(h49),
  parametri = m0$rank)
''')
S(49,'La leva dipende dai predittori',r'''
\PLabel{Una distanza rispetto al disegno}
\[
h_{ii}=\frac1n+\frac{(x_i-\bar x)^2}{\sum_j(x_j-\bar x)^2}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.65,.5)--(9,.5);\draw[pAxis](.65,.5)--(.65,3.0);
\draw[GeoA,line width=1.4pt,domain=1.1:8.5,samples=60] plot(\x,{.8+.14*(\x-4.8)^2});
\draw[Muted,dashed](4.8,.5)--(4.8,2.85);
\node[pNote] at(4.8,.1){$\bar x$};
\node[pNote,anchor=west] at(.75,3.3){Leva nella regressione semplice · schema};
\end{tikzpicture}
\PBody{Punti lontani dalla media di $x$ possono orientare maggiormente la retta. La leva non dipende dal valore osservato della risposta.}
''',r'''
\PCode{R · le leve del modello}{049_leva.R}
\[
\sum_i h_{ii}=p,\qquad \bar h=\frac pn
\]
\PSmall{$p$ è il rango della matrice del modello, inclusa l’intercetta. La formula in alto riguarda una sola variabile quantitativa con intercetta.}
''','La leva descrive la posizione nei predittori. Il residuo descrive lo scarto nella risposta.')

S(50,'Residuo, leva e influenza',r'''
\PLabel{Tre proprietà da distinguere}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.6)--(8.9,.6);\draw[pAxis](.7,.6)--(.7,4.55);
\draw[GeoA,line width=1pt](1,1.1)--(8.5,3.2);
\foreach \x/\y in {1.2/1.2,1.6/1.1,2/1.5,2.4/1.3,2.8/1.7,3.2/1.8,3.6/1.7,4/2,4.4/2.2}{\fill[GeoA](\x,\y) circle(2pt);}
\fill[GeoB](3,3.8) circle(3pt);\node[pNote,text=GeoB] at(3.2,4.3){Residuo elevato};
\fill[GeoC](8.1,3.1) circle(3pt);\node[pNote,text=GeoC,anchor=east] at(8.7,3.65){Leva elevata};
\draw[GeoB,dashed](3,1.66)--(3,3.8);
\node[pNote] at(4.8,.12){Predittore $x$ · schema};
\end{tikzpicture}
\PBody{Un punto estremo in $x$, vicino alla retta, può avere residuo piccolo. Un punto lontano verticalmente può avere leva ordinaria. L’influenza riguarda il cambiamento della stima.}
''',r'''
\PLabel{La domanda dell’analisi di influenza}
\[
\widehat{\boldsymbol\beta}
\quad\hbox{e}\quad
\widehat{\boldsymbol\beta}_{(-i)}
\]
\PBody{Quanto cambiano coefficienti e previsioni quando il caso $i$ viene escluso dal calcolo?}
\vspace{3mm}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-influenza}{Esperimento · leva e influenza}
\PSmall{Spostare il punto aggiunto prima lungo $x$, poi lungo $y$. Confrontare le due rette e osservare come cambiano leva e distanza di Cook.}
''','La parola “anomalo” è troppo generica. Occorre precisare se si parla di leva, residuo o influenza.')

code(51,'cook',r'''
# Una misura del cambiamento globale.
D51 <- cooks.distance(m0)
plot(D51, type = "h",
     xlab = "Indice del fossile",
     ylab = "Distanza di Cook")
j51 <- which.max(D51)
f[j51, c("id", "morfotipo")]
''')
S(51,'La distanza di Cook',r'''
\PLabel{Residuo e leva nella stessa misura}
\[
D_i=\frac{e_i^2}{p\,s^2}\,
     \frac{h_{ii}}{(1-h_{ii})^2}
\]
\PBody{La prima parte misura lo scarto rispetto alla variabilità residua. La seconda aumenta quando la leva si avvicina a uno.}
\vspace{4mm}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.5,.5)--(9,.5);
\foreach \x/\y in {1/.25,1.5/.4,2/.12,2.5/.2,3/.75,3.5/.3,4/.18,4.5/2.15,5/.4,5.5/.15,6/.3,6.5/.65,7/.22,7.5/.18,8/.36}{\draw[GeoA,line width=1.3pt](\x,.5)--(\x,{.5+\y});}
\node[pNote,text=GeoB] at(5,3.1){Caso da esaminare};
\draw[pEdge,draw=GeoB](4.9,2.85)--(4.5,2.65);
\node[pNote] at(4.8,.08){Distanze di Cook · schema};
\end{tikzpicture}
''',r'''
\PCode{R · individuare il caso influente}{051_cook.R}
\PSmall{Una soglia pratica è un criterio di segnalazione. La provenienza della misura e il dominio scientifico devono guidare la decisione sul caso.}
\PInfo{La formula riguarda il modello lineare ordinario. Le misure per modelli generalizzati usano approssimazioni specifiche.}
''','Un valore elevato di Cook richiede un controllo e un’analisi di sensibilità, senza implicare un errore nei dati.')

code(52,'sensibilita',r'''
# Confronto, senza modificare f.
j52 <- which.max(cooks.distance(m0))
m_sens <- update(m0, data = f[-j52, ])
rbind(completo = coef(m0),
      senza_caso = coef(m_sens))
# Conserviamo l'identita' del caso.
f[j52, ]
''')
S(52,'L’analisi di sensibilità di un caso',r'''
\PLabel{Il risultato completo resta il riferimento}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.4cm] (a) at(2.4,3.8){Modello completo};
\node[pFlow,text width=3.4cm] (b) at(7,3.8){Caso segnalato};
\node[pFlow,text width=3.4cm] (c) at(2.4,1.45){Stima completa};
\node[pFlow,text width=3.4cm] (d) at(7,1.45){Stima senza\\quel caso};
\draw[pEdge](a)--(c);\draw[pEdge](b)--(d);
\draw[pEdge](a)--(b);
\draw[<->,Classical,line width=1pt](c)--node[pNote,above]{confronto}(d);
\end{tikzpicture}
\PBody{Si riportano la variazione dei coefficienti, delle previsioni e della conclusione scientifica. Una correzione o esclusione richiede una motivazione documentabile.}
''',r'''
\PCode{R · rifare il calcolo senza un caso}{052_sensibilita.R}
\PSmall{\texttt{update()} conserva la formula e ristima il modello sul sottoinsieme. Il file originale rimane disponibile per confrontare i risultati.}
\PInfo{Controlli utili: unità di misura, trascrizione, metodo di raccolta, condizioni diverse e campo di validità dichiarato.}
''','La sensibilità del risultato è informazione scientifica da riportare, anche quando il caso risulta corretto.')

code(53,'errore_misura',r'''
# Esempio classico, tutto simulato.
set.seed(753)
x53 <- rnorm(1000)
y53 <- 2 + 1.5*x53 + rnorm(1000)
w53 <- x53 + rnorm(1000, sd = 0.8)
c(latente = coef(lm(y53 ~ x53))[2],
  misurato = coef(lm(y53 ~ w53))[2])
# Pendenza limite attesa:
1.5 / (1 + 0.8^2)
''')
S(53,'Errore di misura nel predittore',r'''
\PLabel{Il valore misurato differisce da quello latente}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,minimum width=2cm] (x) at(1.9,2.8){$X$ latente};
\node[pFlow,minimum width=2cm] (w) at(7,2.8){$W=X+U$};
\node[pFlow,minimum width=2cm] (y) at(1.9,.8){$Y$};
\node[pFlow,minimum width=2cm] (u) at(7,.8){$U$};
\draw[pEdge](x)--(w);\draw[pEdge](x)--(y);\draw[pEdge](u)--(w);
\end{tikzpicture}
\[
\operatorname{plim}\widehat\beta_W
=\beta_X\frac{\operatorname{Var}(X)}{\operatorname{Var}(X)+\operatorname{Var}(U)}
\]
\PSmall{Modello classico: errore additivo centrato, indipendente da $X$ e dall’errore della risposta. Il rapporto attenua la pendenza verso zero.}
''',r'''
\PCode{R · osservare l’attenuazione}{053_errore_misura.R}
\PSmall{La formula descrive un limite con campioni grandi. Un singolo campione può discostarsene. Altri meccanismi di errore possono produrre effetti diversi.}
''','La precisione del predittore è parte del modello. L’attenuazione richiede ipotesi specifiche sull’errore di misura.')

code(54,'loglog',r'''
# I logaritmi richiedono valori > 0.
stopifnot(all(f$diametro_int_um > 0),
          all(f$diametro_tot_um > 0))
m_loglog <- lm(log(diametro_int_um) ~
  log(diametro_tot_um), data = f)
coef(m_loglog)
plot(m_loglog, which = 1)
''')
S(54,'La scala logaritmica',r'''
\PLabel{Una relazione moltiplicativa}
\[
\log Y=\beta_0+\beta_1\log X+\varepsilon
\]
\[
Y=e^{\beta_0}X^{\beta_1}e^\varepsilon
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,text width=3.6cm] (a) at(2.2,2.35){$X$ diventa $kX$};
\node[pLabel,text width=4cm] (b) at(7,2.35){La mediana condizionale si moltiplica per $k^{\beta_1}$};
\draw[pEdge](a)--(b);
\draw[Classical,line width=1.2pt](.65,1.15)--(8.7,1.15);
\node[pNote,text width=8cm] at(4.7,.6){Se la mediana di $\varepsilon$ è zero};
\end{tikzpicture}
\PBody{Per piccoli cambiamenti relativi, $\beta_1$ descrive l’elasticità della risposta. La trasformazione modifica l’oggetto interpretato e richiede nuovi controlli dei residui.}
''',r'''
\PCode{R · stimare sulla scala logaritmica}{054_loglog.R}
\PSmall{Nel modello log--log, una variazione dell’1\% in $X$ corrisponde approssimativamente a una variazione del $\beta_1$\% nella mediana di $Y$, alle condizioni indicate.}
''','La scala deve seguire la domanda e il processo di misura. Il logaritmo richiede valori strettamente positivi.')

code(55,'ritrasformazione',r'''
# Profilo dentro il dominio osservato.
nuovo55 <- data.frame(
  diametro_tot_um = 7)
eta55 <- predict(m_loglog, nuovo55)
mediana55 <- exp(eta55)
# Media con errori log-normali omogenei.
media55 <- exp(eta55 +
  sigma(m_loglog)^2 / 2)
c(mediana = mediana55, media = media55)
''')
S(55,'Ritornare alla scala originale',r'''
\PLabel{Media logaritmica e media aritmetica}
\[
\eta(x)=\beta_0+\beta_1\log x
\]
\[
\operatorname{Med}(Y\mid x)=e^{\eta(x)}
\]
\[
E(Y\mid x)=e^{\eta(x)+\sigma^2/2}
\]
\PBody{Le ultime due espressioni valgono se $\varepsilon\sim N(0,\sigma^2)$ sulla scala logaritmica. La dispersione sposta la media aritmetica rispetto alla mediana.}
\vspace{1mm}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,.6)--(9,.6);
\draw[GeoA,line width=1.3pt](3.4,.6)--(3.4,1.75);
\draw[GeoB,line width=1.3pt](5.3,.6)--(5.3,1.75);
\node[pNote,text=GeoA] at(2.8,2.15){Mediana};
\node[pNote,text=GeoB] at(6,2.15){Media};
\node[pNote] at(4.8,.15){Posizioni schematiche sulla scala originale};
\end{tikzpicture}
''',r'''
\PCode{R · due previsioni con significati diversi}{055_ritrasformazione.R}
\PSmall{Il codice usa una correzione parametrica stimata. Se la varianza cambia con $x$ o gli errori logaritmici hanno altra forma, occorre una ritrasformazione appropriata.}
''','Applicare exp() alla previsione logaritmica non restituisce in generale la media aritmetica della risposta.')

code(56,'multiplo',r'''
# Un predittore quantitativo e un gruppo.
m_add <- lm(diametro_int_um ~
  diametro_tot_um + morfotipo,
  data = f)
coef(m_add)
summary(m_add)$sigma
''')
S(56,'Il modello con più predittori',r'''
\PLabel{La risposta dipende da un profilo}
\[
Y_i=\beta_0+\beta_1x_{i1}+\beta_2x_{i2}+\varepsilon_i
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.3cm] (x) at(2.2,3.2){Diametro totale};
\node[pFlow,text width=3.3cm] (g) at(2.2,1.1){Morfotipo};
\node[pFlow,text width=3.7cm] (y) at(7,2.15){Diametro interno medio condizionato};
\draw[pEdge](x)--(y);\draw[pEdge](g)--(y);
\end{tikzpicture}
\PBody{Nei fossili aggiungiamo il morfotipo al diametro totale. Il modello confronta risposte medie per profili con lo stesso diametro e diverso gruppo.}
''',r'''
\PCode{R · aggiungere il morfotipo}{056_multiplo.R}
\PSmall{Il simbolo \texttt{+} include i contributi dei due predittori. In questa formula la pendenza rispetto al diametro è comune ai gruppi.}
\PInfo{L’informazione di gruppo deve essere disponibile nel momento in cui si intende usare il modello.}
''','Ogni previsione del modello multiplo riguarda una combinazione specifica dei predittori.')

S(57,'Coefficienti condizionati',r'''
\PLabel{La variazione a parità degli altri predittori}
\[
E(Y\mid x_1,x_2)=\beta_0+\beta_1x_1+\beta_2x_2
\]
\[
E(Y\mid x_1+\delta,x_2)-E(Y\mid x_1,x_2)=\beta_1\delta
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.5)--(8.9,.5);\draw[pAxis](.7,.5)--(.7,3.15);
\draw[GeoA,line width=1.3pt](1,1)--(8.1,2.7);
\draw[GeoB,line width=1.3pt](1,1.55)--(7.5,3.1);
\draw[Classical,dashed](3,1.48)--(5.6,1.48)--(5.6,2.1);
\node[pNote] at(4.3,1.2){$\delta$};\node[pNote,anchor=west] at(5.75,1.8){$\beta_1\delta$};
\node[pNote] at(4.8,.08){$x_1$ con $x_2$ fissato · schema};
\end{tikzpicture}
''',r'''
\PBody{Il coefficiente descrive un confronto condizionato dal modello. Il confronto marginale, ottenuto ignorando gli altri predittori, può avere dimensione o segno diverso.}
\vspace{3mm}
\PInfo{“A parità di” richiede combinazioni dei predittori compatibili con i dati. Con scarso supporto comune, il confronto dipende maggiormente dall’estrapolazione.}
\vspace{2mm}
\PSmall{Interpretazione causale e aggiustamento statistico richiedono ipotesi sul disegno e sulle variabili coinvolte. L’aggiunta di covariate, da sola, non stabilisce un effetto causale.}
''','Il significato di un coefficiente dipende dagli altri termini inclusi e dal dominio in cui il confronto è sostenuto dai dati.')

code(58,'riferimento',r'''
# Scegliamo il gruppo di riferimento.
f$morfotipo <- relevel(
  factor(f$morfotipo), ref = "Rounded")
levels(f$morfotipo)
contrasts(f$morfotipo)
# La scelta entra nella parametrizzazione.
m_add <- lm(diametro_int_um ~
  diametro_tot_um + morfotipo, data = f)
''')
S(58,'Un indicatore per il morfotipo',r'''
\PLabel{La codifica rende esplicito il confronto}
\[
G_i=\begin{cases}0&\text{Rounded}\\1&\text{Spiky}\end{cases}
\]
\[
E(Y\mid x,G)=\beta_0+\beta_1x+\beta_2G
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.6cm] at(2.3,2.25){Rounded\\$\beta_0+\beta_1x$};
\node[pFlow,text width=3.6cm] at(7,2.25){Spiky\\$\beta_0+\beta_1x+\beta_2$};
\draw[<->,Classical,line width=1pt](2.3,.9)--node[pNote,above]{$\beta_2$: Spiky meno Rounded}(7,.9);
\end{tikzpicture}
\PBody{Il coefficiente del gruppo è una differenza nella risposta media a pari $x$, sotto l’ipotesi di pendenza comune.}
''',r'''
\PCode{R · fissare Rounded come riferimento}{058_riferimento.R}
\PSmall{\texttt{relevel()} rende esplicito il riferimento. Il codice usa i contrasti di trattamento predefiniti per un fattore non ordinato.}
''','Riportare il gruppo di riferimento è necessario per interpretare segno e significato del coefficiente categoriale.')

code(59,'matrice',r'''
# Colonne usate realmente dal modello.
X59 <- model.matrix(m_add)
colnames(X59)
head(X59, 6)
# La colonna iniziale vale sempre 1.
stopifnot(all(X59[, 1] == 1))
''')
S(59,'La matrice del modello in R',r'''
\PLabel{Ogni riga descrive un fossile}
\[
\mathbf X=
\begin{pmatrix}
1&x_1&0\\
1&x_2&1\\
1&x_3&0\\
\vdots&\vdots&\vdots
\end{pmatrix}
\quad
\boldsymbol\beta=
\begin{pmatrix}\beta_0\\\beta_1\\\beta_2\end{pmatrix}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,text width=2.5cm] at(1.6,1.6){Intercetta\\colonna di uno};
\node[pLabel,text width=2.5cm] at(4.7,1.6){Diametro\\valore misurato};
\node[pLabel,text width=2.5cm] at(7.8,1.6){Gruppo\\indicatore 0/1};
\draw[Classical,line width=1pt](.6,.6)--(8.8,.6);
\node[pNote] at(4.7,.12){La formula stabilisce quali colonne costruire};
\end{tikzpicture}
''',r'''
\PCode{R · ispezionare model.matrix()}{059_matrice.R}
\PSmall{I nomi delle colonne chiariscono quale coefficiente moltiplica ciascun termine. Per una riga $\mathbf x_i^\top$, il valore stimato è $\mathbf x_i^\top\widehat{\boldsymbol\beta}$.}
\PInfo{Una variabile con $k$ categorie richiede normalmente $k-1$ indicatori quando il modello include l’intercetta.}
''','La matrice del modello collega una formula R alla parametrizzazione matematica effettivamente stimata.')

code(60,'additivo',r'''
# Contrasto a diametro totale fissato.
nuovi60 <- data.frame(
  diametro_tot_um = c(7, 7),
  morfotipo = c("Rounded", "Spiky"))
mu60 <- predict(m_add, nuovi60)
diff(mu60)
# Coincide con il coefficiente di gruppo.
coef(m_add)["morfotipoSpiky"]
''')
S(60,'Il modello additivo',r'\PLabel{Due rette con pendenza comune}'+lines_plot()+r'''
\[
\Delta(x)=E(Y\mid x,G=1)-E(Y\mid x,G=0)=\beta_2
\]
\PSmall{Le rette parallele impongono un contrasto costante lungo il dominio.}
''',r'''
\PCode{R · leggere il contrasto condizionato}{060_additivo.R}
\PSmall{Le due righe di \texttt{newdata} differiscono soltanto per il morfotipo. Il confronto deve riguardare diametri presenti nel supporto comune dei gruppi.}
''','L’assenza di interazione impone una pendenza comune e una differenza di gruppo costante.')

code(61,'interazione',r'''
# * include effetti principali e prodotto.
m_int <- lm(diametro_int_um ~
  diametro_tot_um * morfotipo,
  data = f)
coef(m_int)
# Le colonne rendono visibile il prodotto.
colnames(model.matrix(m_int))
''')
S(61,'Pendenze diverse tra gruppi',r'\PLabel{Un prodotto aggiunge l’interazione}'+lines_plot(True)+r'''
\[
E(Y\mid x,G)=\beta_0+\beta_1x+\beta_2G+\beta_3xG
\]
\PSmall{La pendenza è $\beta_1$ per Rounded e $\beta_1+\beta_3$ per Spiky. Il coefficiente $\beta_3$ misura la differenza tra pendenze.}
''',r'''
\PCode{R · stimare pendenze di gruppo}{061_interazione.R}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-interazioni}{Esperimento · interazioni}
\PSmall{Nel simulatore modificare il termine $xG$. Osservare come cambia la differenza fra le pendenze, mantenendo riconoscibili i due gruppi.}
''','In R, x * gruppo equivale a x + gruppo + x:gruppo.')

code(62,'contrasto',r'''
# Confrontiamo tre diametri scelti.
x62 <- c(6, 7, 8)
a62 <- data.frame(diametro_tot_um = x62,
                   morfotipo = "Rounded")
b62 <- a62; b62$morfotipo <- "Spiky"
delta62 <- predict(m_int, b62) -
           predict(m_int, a62)
data.frame(diametro = x62, delta = delta62)
''')
S(62,'Il contrasto dipende da x',r'\PLabel{La distanza verticale cambia lungo la scala}'+lines_plot(True,True)+r'''
\[
\Delta(x)=\beta_2+\beta_3x
\]
\PBody{Con l’interazione, il confronto dipende dal diametro. Un solo coefficiente non lo riassume.}
''',r'''
\PCode{R · contrasti per valori dichiarati}{062_contrasto.R}
\PSmall{Il codice produce confronti puntuali. Prima di interpretarli si controlla il dominio di ciascun morfotipo, soprattutto vicino agli estremi.}
''','Con un’interazione, il contrasto di gruppo è una funzione del predittore.')

code(63,'centrare',r'''
# Il valore 7 um ha significato nel dominio.
f$x_c <- f$diametro_tot_um - 7
m_c <- lm(diametro_int_um ~
  x_c * morfotipo, data = f)
coef(m_c)
# Le previsioni restano uguali.
max(abs(fitted(m_c) - fitted(m_int)))
''')
S(63,'Centrare il predittore',r'''
\PLabel{Un’origine interpretabile}
\[
x_c=x-x_0,\qquad x_0=7\ \mu\mathrm m
\]
\[
E(Y\mid x_c,G)=\alpha_0+\alpha_1x_c+\alpha_2G+\alpha_3x_cG
\]
\[
\alpha_2=\beta_2+\beta_3x_0=\Delta(x_0)
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,1.7)--(8.9,1.7);
\foreach \x/\lab in {1.2/5,3/6,4.8/7,6.6/8,8.4/9}{\draw[Muted](\x,1.55)--(\x,1.85);\node[pNote] at(\x,2.2){\lab};}
\foreach \x/\lab in {1.2/{-2},3/{-1},4.8/0,6.6/1,8.4/2}{\node[pNote,text=Classical] at(\x,.9){\lab};}
\node[pNote,anchor=west] at(.8,2.8){Scala originale $x$};
\node[pNote,anchor=west] at(.8,.25){Scala centrata $x_c$};
\end{tikzpicture}
''',r'''
\PCode{R · cambiare l’origine della scala}{063_centrare.R}
\PSmall{Il coefficiente di gruppo ora descrive Spiky meno Rounded a $7\,\mu$m. Il modello rappresenta le stesse rette, con coefficienti più comodi da interpretare.}
''','Centrare cambia la parametrizzazione e il significato dell’intercetta, conservando le previsioni del modello equivalente.')

code(64,'intervallo_contrasto',r'''
# m_c e' centrato a 7 um.
j64 <- match("morfotipoSpiky",
             names(coef(m_c)))
d64 <- coef(m_c)[j64]
se64 <- sqrt(vcov(m_c)[j64, j64])
t64 <- qt(0.975, df.residual(m_c))
c(stima = d64,
  basso = d64 - t64*se64,
  alto = d64 + t64*se64)
''')
S(64,'Incertezza di un contrasto',r'''
\PLabel{La covarianza dei coefficienti conta}
\[
\widehat\Delta(x)=\mathbf c(x)^\top\widehat{\boldsymbol\beta},
\quad \mathbf c(x)=(0,0,1,x)^\top
\]
\[
\operatorname{SE}\{\widehat\Delta(x)\}
=\sqrt{\mathbf c(x)^\top\widehat{\operatorname{Var}}(\widehat{\boldsymbol\beta})\mathbf c(x)}
\]
\[
\widehat\Delta(x)\ \pm\ t_{n-p,\,0.975}\,
\operatorname{SE}\{\widehat\Delta(x)\}
\]
\PBody{Il vettore $\mathbf c(x)$ usa l’ordine intercetta, $x$, gruppo, interazione. Dopo il centraggio in $x_0$, il contrasto in $x_0$ coincide con il coefficiente di gruppo.}
\vspace{3mm}
\PSmall{Intervallo puntuale al 95\% nel modello lineare classico con errori normali indipendenti e varianza costante. Una banda simultanea è un oggetto diverso.}
''',r'''
\PCode{R · intervallo a 7 micrometri}{064_intervallo_contrasto.R}
\PSmall{\texttt{vcov()} restituisce la matrice delle covarianze stimate. Per altri valori di $x$ bisogna includere anche il termine di interazione e la sua covarianza.}
''','L’incertezza di una combinazione di coefficienti dipende anche dalle covarianze tra le stime.')

code(65,'profilo',r'''
# Stessi nomi e livelli del modello.
nuovi65 <- data.frame(
  diametro_tot_um = c(6.5, 7.5),
  morfotipo = c("Rounded", "Spiky"))
predict(m_int, newdata = nuovi65,
        interval = "confidence")
# Nuovi individui: intervallo piu' ampio.
predict(m_int, newdata = nuovi65,
        interval = "prediction")
''')
S(65,'Prevedere per un profilo',r'''
\PLabel{Una nuova riga della matrice del modello}
\[
\mathbf x_0^\top=(1,\ x_0,\ G_0,\ x_0G_0)
\]
\[
\widehat y_0=\mathbf x_0^\top\widehat{\boldsymbol\beta}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (a) at(2.3,2.3){Diametro e morfotipo del nuovo caso};
\node[pFlow,text width=3.7cm] (b) at(7,2.3){Risposta media stimata e incertezza};
\draw[pEdge](a)--(b);
\node[pNote,text width=8.5cm] at(4.7,.8){Il profilo deve appartenere a un dominio sostenuto dai dati};
\end{tikzpicture}
\PBody{Un livello categoriale mai osservato non ha un coefficiente stimato. Anche una combinazione nuova di valori già presenti può richiedere estrapolazione.}
''',r'''
\PCode{R · due profili completi}{065_profilo.R}
\PSmall{L’intervallo di confidenza riguarda la media condizionata. L’intervallo di previsione include anche la variabilità di un nuovo fossile.}
''','La validità di una previsione dipende dalla combinazione dei predittori, oltre che dall’intervallo di ogni singola variabile.')

S(66,'Collinearità tra predittori',r'''
\PLabel{Quando i contributi diventano difficili da separare}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.5)--(8.9,.5);\draw[pAxis](.7,.5)--(.7,4.1);
\draw[GeoA!20,line width=12pt](1.3,.9)--(8,3.6);
\foreach \x/\y in {1.3/.95,1.8/1.2,2.3/1.18,2.8/1.65,3.3/1.72,3.8/2.02,4.3/2.05,4.8/2.42,5.3/2.5,5.8/2.78,6.3/2.83,6.8/3.18,7.3/3.32,7.8/3.45}{\fill[GeoA](\x,\y) circle(2pt);}
\node[pNote] at(4.8,.08){Predittore $x_1$};
\node[pNote,anchor=west] at(.8,4.4){Predittore $x_2$ · schema};
\end{tikzpicture}
\PBody{Se $x_1$ e $x_2$ variano quasi insieme, il campione informa poco sul cambiamento di uno a parità dell’altro. I singoli coefficienti possono diventare instabili.}
''',r'''
\[
\widehat{\operatorname{Var}}(\widehat{\boldsymbol\beta})
=s^2(\mathbf X^\top\mathbf X)^{-1}
\]
\PBody{Vicino a una dipendenza lineare, alcune direzioni contengono poca informazione. Intervalli ampi e coefficienti sensibili a piccole modifiche possono coesistere con previsioni stabili entro il dominio osservato.}
\vspace{3mm}
\PInfo{Centrare o cambiare unità può migliorare il calcolo numerico. Non crea nuove combinazioni dei predittori nel campione.}
''','Una buona previsione entro il campione non garantisce che i contributi dei singoli predittori siano ben separati.')

code(67,'identita',r'''
# Identita' delle misure sintetiche.
scarto67 <- with(f, diametro_tot_um -
  diametro_int_um - 2*spessore_um)
max(abs(scarto67))
# Anche l'arrotondamento conta.
summary(scarto67)
''')
S(67,'L’identità geometrica dei fossili',r'''
\PLabel{Una relazione costruita per definizione}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[GeoA,fill=GeoA!9,line width=1pt](3.1,2.6) circle(1.75cm);
\draw[Classical,fill=Paper,line width=1pt](3.1,2.6) circle(1.18cm);
\draw[<->,GeoA,line width=1pt](1.35,.5)--(4.85,.5);\draw[GeoA!50,dashed](1.35,.5)--(1.35,2.6);\draw[GeoA!50,dashed](4.85,.5)--(4.85,2.6);
\node[pNote,text=GeoA] at(3.1,.1){$D_{\rm tot}$};
\draw[<->,Classical,line width=1pt](1.92,2.6)--(4.28,2.6);
\node[pNote] at(3.1,2.2){$D_{\rm int}$};
\draw[<->,GeoB,line width=1pt](4.28,2.6)--(4.85,2.6);
\node[pNote,text=GeoB] at(5.15,3.25){$s$};
\node[pLabel,text width=3cm] at(7.6,2.6){$D_{\rm tot}-D_{\rm int}-2s=0$};
\end{tikzpicture}
\PBody{Nel dataset sintetico, diametri e spessore soddisfano questa identità, salvo arrotondamenti. La relazione algebrica deve entrare nella scelta delle variabili.}
''',r'''
\PCode{R · verificare la definizione}{067_identita.R}
\PSmall{Usare simultaneamente queste tre quantità come predittori genera ridondanza esatta o quasi esatta. Usare una quantità che ricostruisce direttamente la risposta può rendere la previsione priva dell’utilità prevista.}
''','Prima di interpretare una correlazione occorre conoscere come ciascuna variabile è definita e calcolata.')

code(68,'rango',r'''
# Esempio con dipendenza esatta costruita.
x68 <- f$diametro_tot_um
s68 <- f$spessore_um
z68 <- x68 - 2*s68
X68 <- cbind(1, x68, z68, s68)
c(colonne = ncol(X68),
  rango = qr(X68)$rank)
''')
S(68,'Rango e coefficienti identificabili',r'''
\PLabel{Una combinazione delle colonne vale zero}
\[
\mathbf X\mathbf a=\mathbf0,\qquad \mathbf a\ne\mathbf0
\]
\[
\mathbf X(\boldsymbol\beta+t\mathbf a)=\mathbf X\boldsymbol\beta
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.7cm] (b1) at(2.4,3){$\boldsymbol\beta$};
\node[pFlow,text width=3.7cm] (b2) at(2.4,1){$\boldsymbol\beta+t\mathbf a$};
\node[pFlow,text width=3.4cm] (y) at(7.1,2){Stesse risposte medie};
\draw[pEdge](b1)--(y);\draw[pEdge](b2)--(y);
\end{tikzpicture}
\PSmall{Se il rango è minore del numero di colonne, i coefficienti non hanno una soluzione unica. La formula con l’inversa ordinaria di $\mathbf X^\top\mathbf X$ non è applicabile.}
''',r'''
\PCode{R · confrontare rango e colonne}{068_rango.R}
\PSmall{Qui $z=x-2s$ viene ricostruita per mostrare una dipendenza esatta. Nei dati arrotondati, il rango numerico dipende anche dalla tolleranza e dalla scala.}
\PSmall{La scelta delle colonne deve conservare un significato scientifico leggibile.}
''','Identificabilità dei coefficienti e qualità delle previsioni sono problemi distinti.')

code(69,'modelli',r'''
# Formule motivate da ipotesi diverse.
formule69 <- list(
  comune = diametro_int_um ~
    diametro_tot_um,
  additivo = diametro_int_um ~
    diametro_tot_um + morfotipo,
  interazione = diametro_int_um ~
    diametro_tot_um * morfotipo)
# La valutazione seguira' un protocollo.
names(formule69)
''')
S(69,'Confrontare modelli motivati',r'''
\PLabel{Ogni formula rappresenta un’ipotesi}
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \yy/\tit/\desc in {4.4/{Retta comune}/{La relazione media ignora il gruppo},2.75/{Modello additivo}/{Differenza costante tra gruppi},1.1/{Interazione}/{La differenza varia con il diametro}}{
\node[pLabel,anchor=west,text width=3cm,align=left] at(.45,\yy){\textbf{\tit}};
\node[pLabel,anchor=west,text width=5.4cm,align=left] at(3.8,\yy){\desc};
\draw[Rule](.45,\yy-.65)--(9.1,\yy-.65);}
\end{tikzpicture}
\PBody{La scelta dipende dalla domanda, dalla disponibilità dei predittori e dalle prestazioni su dati lasciati fuori dalla stima.}
''',r'''
\PCode{R · dichiarare i modelli candidati}{069_modelli.R}
\PSmall{Una ricerca automatica su molte formule può adattarsi alle particolarità del campione. L’intera procedura di selezione deve rientrare nella validazione.}
''','Il confronto tra modelli comincia dalle ipotesi che ogni formula impone alla relazione scientifica.')

S(70,'Interpretare una relazione condizionata',r'''
\PLabel{La conclusione deve indicare il confronto}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,text width=8.5cm,align=left] at(4.8,4.3){\textbf{Risposta}\\Diametro interno, in micrometri};
\node[pLabel,text width=8.5cm,align=left] at(4.8,2.9){\textbf{Confronto}\\Spiky rispetto a Rounded a diametro totale fissato};
\node[pLabel,text width=8.5cm,align=left] at(4.8,1.5){\textbf{Dominio}\\Valori condivisi dai due gruppi e unità osservate};
\draw[Classical,line width=1.3pt](.4,.5)--(9,.5);
\end{tikzpicture}
\PBody{Un risultato interpretabile riporta stima e intervallo, forma del modello e limiti del campionamento. L’interazione richiede di specificare il valore di $x$.}
''',r'''
\PLabel{Una domanda di lettura}
\PBody{Che cosa significa il coefficiente di Spiky dopo aver centrato il diametro totale a $7\,\mu$m?}
\vspace{3mm}
\PInfo{È la differenza media Spiky meno Rounded a $7\,\mu$m, secondo il modello. L’intervallo misura l’incertezza di questo contrasto alle ipotesi dichiarate.}
\vspace{2mm}
\PSmall{I fossili sono sintetici. Il risultato descrive il caso didattico e non costituisce una conclusione empirica su una popolazione paleontologica.}
''','Una conclusione statistica acquista significato quando variabile, unità, confronto e dominio sono espliciti.')

code(71,'risposta_binaria',r'''
# 1 indica Spiky, 0 indica Rounded.
f$spiky <- as.integer(
  f$morfotipo == "Spiky")
table(f$morfotipo, f$spiky)
stopifnot(all(f$spiky %in% c(0, 1)))
''')
S(71,'Una risposta binaria',r'''
\PLabel{Il parametro di interesse è una probabilità}
\[
Y_i\mid\mathbf x_i\sim\operatorname{Bernoulli}(p_i)
\]
\[
E(Y_i\mid\mathbf x_i)=p_i,\qquad
\operatorname{Var}(Y_i\mid\mathbf x_i)=p_i(1-p_i)
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.6,.7)--(9,.7);
\foreach \x/\y/\col in {1/1.1/GeoA,1.6/1.1/GeoA,2.2/2.9/GeoB,2.8/1.1/GeoA,3.4/2.9/GeoB,4/1.1/GeoA,4.6/2.9/GeoB,5.2/1.1/GeoA,5.8/2.9/GeoB,6.4/2.9/GeoB,7/1.1/GeoA,7.6/2.9/GeoB,8.2/2.9/GeoB}{\fill[\col](\x,\y) circle(2.5pt);}
\node[pNote,anchor=east] at(.5,1.1){0};\node[pNote,anchor=east] at(.5,2.9){1};
\node[pNote] at(4.8,.25){Predittore quantitativo · schema};
\end{tikzpicture}
''',r'''
\PCode{R · costruire la risposta 0/1}{071_risposta_binaria.R}
\PSmall{La codifica stabilisce quale evento ha probabilità $p_i$. La media dei valori 0/1 è la frequenza dell’evento nel gruppo considerato.}
\PInfo{Qui descriviamo l’etichetta sintetica Spiky. Una regola tassonomica per nuovi fossili richiederebbe una validazione specifica.}
''','Una regressione per risposte binarie descrive la probabilità dell’evento dichiarato.')

code(72,'odds',r'''
# Tre scale per la stessa probabilita'.
p72 <- c(0.2, 0.5, 0.8)
data.frame(
  probabilita = p72,
  odds = p72 / (1 - p72),
  logit = qlogis(p72))
# La funzione inversa recupera p.
plogis(qlogis(p72))
''')
S(72,'Logit, odds e probabilità',r'''
\PLabel{Tre scale con intervalli differenti}
\[
\operatorname{odds}=\frac{p}{1-p},\qquad
\eta=\operatorname{logit}(p)=\log\frac{p}{1-p}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel,anchor=west] at(.5,3.5){Probabilità};
\node[pLabel,anchor=west] at(.5,2.2){Odds};
\node[pLabel,anchor=west] at(.5,.9){Logit};
\foreach \x/\p/\o/\l in {4/{0,2}/{0,25}/{-1,386},6/{0,5}/{1}/{0},8/{0,8}/{4}/{1,386}}{
\node[pLabel] at(\x,3.5){$\p$};\node[pLabel] at(\x,2.2){$\o$};\node[pLabel] at(\x,.9){$\l$};}
\draw[Rule](.5,2.85)--(9,2.85);\draw[Rule](.5,1.55)--(9,1.55);
\end{tikzpicture}
\PSmall{Esempi di conversione. Gli odds possono superare uno, mentre una probabilità rimane tra zero e uno.}
''',r'''
\PCode{R · qlogis() e plogis()}{072_odds.R}
\[
p=\frac{1}{1+e^{-\eta}}
\]
\PSmall{\texttt{qlogis()} passa dalla probabilità al logit. \texttt{plogis()} applica la trasformazione inversa.}
''','Odds e probabilità hanno significati e scale diversi. Una variazione negli odds non è una variazione uguale nella probabilità.')

_logistic_plot=axes(r'Predittore lineare $\eta$', r'Probabilità $p$',8.4,3.4)
_logistic_plot += r'\draw[Muted,dashed](.65,2.2)--(8.9,2.2);\node[pNote,anchor=east] at(.55,2.2){$0{,}5$};'+'\n'
_logistic_plot += r'\draw[GeoA,line width=1.6pt] plot[smooth] coordinates{'
for i in range(81):
    eta=-4+8*i/80;x=.9+(eta+4)*.95;y=.7+3/(1+exp(-eta))
    _logistic_plot += f'({x:.4f},{y:.4f}) '
_logistic_plot += r'};\draw[Muted,dashed](4.7,.5)--(4.7,3.9);\node[pNote,anchor=west] at(4.85,.85){0};\end{tikzpicture}'
code(73,'curva_logistica',r'''
# Curva teorica: eta varia da -4 a 4.
eta73 <- seq(-4, 4, length.out = 101)
plot(eta73, plogis(eta73), type = "l",
     xlab = "Predittore lineare eta",
     ylab = "Probabilita'", ylim = c(0, 1))
abline(h = 0.5, v = 0, lty = 2)
''')
S(73,'La curva logistica',r'\PLabel{Il predittore lineare viene trasformato}'+_logistic_plot+r'''
\[
\eta_i=\beta_0+\beta_1x_i,\qquad p_i=\operatorname{logit}^{-1}(\eta_i)
\]
\PSmall{Per $\eta=0$, la probabilità vale $0{,}5$. Valori molto positivi o negativi si avvicinano rispettivamente a uno o zero.}
''',r'''
\PCode{R · tracciare la funzione inversa}{073_curva_logistica.R}
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m07-logistica}{Esperimento · curva logistica}
\PSmall{Il simulatore varia coefficienti dichiarati e genera risposte 0/1. La curva teorica è nota: stimare i coefficienti dai dati è il passo successivo.}
''','Il modello è lineare nella scala del logit. La probabilità segue una curva compresa fra zero e uno.')

code(74,'glm',r'''
# Stima descrittiva sul campione.
m_log <- glm(spiky ~ diametro_tot_um,
  data = f, family = binomial())
summary(m_log)$coefficients
m_log$converged
# Probabilita' nella scala 0--1.
p_log <- predict(m_log,
                 type = "response")
range(p_log)
''')
S(74,'Stimare la logistica con glm',r'''
\PLabel{Risposte condizionatamente indipendenti}
\[
L(\boldsymbol\beta)=\prod_{i=1}^n
p_i^{y_i}(1-p_i)^{1-y_i}
\]
\[
\ell(\boldsymbol\beta)=\sum_i
\{y_i\log p_i+(1-y_i)\log(1-p_i)\}
\]
\PBody{La stima sceglie coefficienti che rendono plausibile la sequenza osservata di zeri e uno. \texttt{glm()} esegue un algoritmo iterativo.}
\vspace{4mm}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (a) at(2.4,1.6){Coefficienti provvisori};
\node[pFlow,text width=3.5cm] (b) at(7,1.6){Probabilità\\e aggiornamento};
\draw[pEdge](a)--(b);\draw[pEdge](b.south)--++(0,-.8)-|(a.south);
\end{tikzpicture}
''',r'''
\PCode{R · una famiglia binomiale}{074_glm.R}
\PSmall{\texttt{binomial()} usa il logit. Controllare convergenza e avvisi: probabilità estreme possono segnalare separazione.}
\PSmall{La prestazione predittiva richiede dati esclusi dalla stima.}
''','La regressione logistica stima probabilità tramite una verosimiglianza Bernoulli e richiede il controllo della convergenza.')

code(75,'odds_ratio',r'''
# Effetto di +1 um sul rapporto degli odds.
b75 <- coef(m_log)["diametro_tot_um"]
c(per_1_um = exp(b75),
  per_0_5_um = exp(0.5*b75))
# Cambiare l'unita' cambia l'incremento.
''')
S(75,'Il rapporto tra odds',r'''
\PLabel{Un incremento del predittore}
\[
\frac{\operatorname{odds}(x+\delta)}{\operatorname{odds}(x)}
=e^{\beta_1\delta}
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pFlow,text width=3.5cm] (a) at(2.3,3.1){Odds a $x$};
\node[pFlow,text width=3.5cm] (b) at(7,3.1){Odds a $x+\delta$};
\draw[pEdge](a)--node[pNote,above]{$\times e^{\beta_1\delta}$}(b);
\node[pLabel,text width=8cm] at(4.7,1.35){$\beta_1=0\;\Longleftrightarrow\;OR=1$};
\end{tikzpicture}
\PBody{Senza interazione, lo stesso incremento moltiplica gli odds per lo stesso fattore. Con più predittori, gli altri termini rimangono fissati.}
''',r'''
\PCode{R · esponenziare un coefficiente}{075_odds_ratio.R}
\PSmall{Il diametro è espresso in micrometri. Il rapporto per mezzo micrometro è $e^{0{,}5\beta_1}$, non metà del rapporto per un micrometro.}
\PInfo{Un odds ratio pari a 2 indica odds doppi. L’aumento della probabilità dipende dal valore di partenza.}
''','Un odds ratio deve sempre essere accompagnato dall’incremento e dall’unità del predittore.')

code(76,'effetto_probabilita',r'''
# Probabilita' per profili espliciti.
nuovi76 <- data.frame(
  diametro_tot_um = c(6, 7, 8))
p76 <- predict(m_log, nuovi76,
               type = "response")
data.frame(nuovi76, probabilita = p76)
# Differenze per incrementi di 1 um.
diff(p76)
''')
S(76,'L’effetto sulla probabilità',r'''
\PLabel{Lo stesso coefficiente ha effetti locali diversi}
\[
\frac{dp}{dx}=\beta_1p(1-p)
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.5)--(8.9,.5);\draw[pAxis](.7,.5)--(.7,3.85);
\draw[GeoA,line width=1.4pt,domain=.9:8.5,samples=80] plot(\x,{.7+3/(1+exp(-1.1*(\x-4.7)))});
\draw[GeoB,line width=1.2pt](3.9,1.55)--(5.5,2.85);
\draw[GeoB,line width=1.2pt](6.6,3.28)--(8.2,3.58);
\node[pNote,text width=3cm] at(2.6,3.3){Maggiore sensibilità vicino a $p=0{,}5$};
\node[pNote] at(4.8,.08){Predittore $x$ · schema};
\end{tikzpicture}
\PBody{Vicino agli estremi zero e uno, la probabilità varia meno per lo stesso incremento di $x$. Conviene mostrare probabilità previste per profili scientificamente pertinenti.}
''',r'''
\PCode{R · confrontare probabilità previste}{076_effetto_probabilita.R}
\PSmall{Le differenze in \texttt{diff(p76)} sono variazioni di probabilità, interpretabili in punti percentuali moltiplicando per 100.}
''','Il coefficiente logistico agisce linearmente sul logit, mentre la variazione di probabilità dipende dal profilo iniziale.')

code(77,'soglia',r'''
# Probabilita' descrittive gia' calcolate.
soglia77 <- 0.5
classe77 <- as.integer(p_log >= soglia77)
head(data.frame(
  probabilita = p_log,
  classe = classe77,
  osservato = f$spiky))
''')
S(77,'Probabilità e soglia',r'''
\PLabel{La decisione richiede una regola aggiuntiva}
\[
\widehat Y=\mathbf1(\widehat p\ge\tau)
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[GeoA!25,line width=12pt](.85,2)--(4.7,2);
\draw[GeoB!30,line width=12pt](4.7,2)--(8.55,2);
\draw[pAxis](.7,2)--(8.9,2);
\foreach \x/\lab in {.85/0,4.7/{\tau},8.55/1}{\draw[Muted](\x,1.75)--(\x,2.25);\node[pNote] at(\x,1.35){$\lab$};}
\node[pLabel,text=GeoA] at(2.65,3){Decisione 0};
\node[pLabel,text=GeoB] at(6.65,3){Decisione 1};
\node[pNote] at(4.7,.55){Scala delle probabilità};
\end{tikzpicture}
\PBody{La soglia traduce una probabilità in un’etichetta. Le probabilità conservano informazione che si perde riducendo ogni caso a zero o uno.}
''',r'''
\PCode{R · applicare una soglia dichiarata}{077_soglia.R}
\PSmall{La scelta $0{,}5$ è un riferimento didattico. La soglia adatta all’uso dipende dai costi degli errori e dalla calibrazione delle probabilità.}
''','Il modello fornisce una probabilità. La classificazione aggiunge una soglia e quindi una scelta decisionale.')

code(78,'classificazione',r'''
# Livelli espliciti anche se un conteggio e' 0.
tab78 <- table(
  osservato = factor(f$spiky, levels = 0:1),
  previsto = factor(classe77, levels = 0:1))
tab78
sum(diag(tab78)) / sum(tab78)
''')
S(78,'La matrice di classificazione',r'''
\PLabel{Risposta osservata e decisione}
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel] at(4.6,4.65){Previsto 0};\node[pLabel] at(7.3,4.65){Previsto 1};
\node[pLabel,anchor=east] at(2.9,3.2){Osservato 0};\node[pLabel,anchor=east] at(2.9,1.4){Osservato 1};
\draw[Rule,fill=GeoA!8](3.25,2.3) rectangle(5.95,4.1);
\draw[Rule,fill=GeoB!10](5.95,2.3) rectangle(8.65,4.1);
\draw[Rule,fill=GeoB!10](3.25,.5) rectangle(5.95,2.3);
\draw[Rule,fill=GeoA!8](5.95,.5) rectangle(8.65,2.3);
\node[pLabel] at(4.6,3.2){TN\\vero negativo};\node[pLabel] at(7.3,3.2){FP\\falso positivo};
\node[pLabel] at(4.6,1.4){FN\\falso negativo};\node[pLabel] at(7.3,1.4){TP\\vero positivo};
\end{tikzpicture}
\[
\operatorname{Accuracy}=\frac{TP+TN}{n}
\]
''',r'''
\PCode{R · conteggi per la soglia scelta}{078_classificazione.R}
\PSmall{Questi conteggi descrivono il campione di stima. Con una classe dominante, anche una regola costante può avere alta accuratezza.}

''','La matrice dei conteggi mostra quali errori produce una soglia e quale classe ne sostiene il costo.')

code(79,'sensibilita_specificita',r'''
# tab78: righe osservate, colonne previste.
TP79 <- tab78["1", "1"]
FN79 <- tab78["1", "0"]
TN79 <- tab78["0", "0"]
FP79 <- tab78["0", "1"]
c(sensibilita = TP79/(TP79+FN79),
  specificita = TN79/(TN79+FP79))
''')
S(79,'Sensibilità, specificità e costi',r'''
\PLabel{Le due classi hanno denominatori differenti}
\[
\operatorname{Sensibilità}=\frac{TP}{TP+FN},\qquad
\operatorname{Specificità}=\frac{TN}{TN+FP}
\]
\vspace{0mm}
\PBody{Abbassare la soglia aumenta le decisioni positive: possono crescere sia TP sia FP.}
\vspace{0mm}
\[
\underbrace{C_{FP}(1-p)}_{\text{costo atteso se decido 1}}
\ \le\
\underbrace{C_{FN}p}_{\text{costo atteso se decido 0}}
\]
\[
\tau^*=\frac{C_{FP}}{C_{FP}+C_{FN}}
\]
\PSmall{Con probabilità calibrate, costi positivi costanti e decisioni corrette a costo zero.}
''',r'''
\PCode{R · leggere le due proporzioni}{079_sensibilita_specificita.R}
\PSmall{Le proporzioni richiedono casi osservati in entrambe le classi. La scelta o l’ottimizzazione della soglia deve avvenire senza consultare il test finale.}
''','La soglia dipende dallo scopo della decisione. Sensibilità e specificità descrivono aspetti diversi della classificazione.')

code(80,'brier',r'''
# Valutazione descrittiva sul campione.
brier80 <- mean((p_log - f$spiky)^2)
# Riferimento costante: frequenza osservata.
pbase80 <- mean(f$spiky)
base80 <- mean((pbase80 - f$spiky)^2)
c(modello = brier80, riferimento = base80)
''')
S(80,'Il punteggio di Brier',r'''
\PLabel{Valutare direttamente le probabilità}
\[
\operatorname{BS}=\frac1n\sum_{i=1}^n(\widehat p_i-y_i)^2
\]
\begin{tikzpicture}[x=1cm,y=1cm]
\node[pLabel] at(4.7,3.55){Esempio con evento osservato $y=1$};
\node[pFlow,text width=3.6cm] at(2.3,2){$\widehat p=0{,}8$\\perdita $=0{,}04$};
\node[pFlow,text width=3.6cm] at(7,2){$\widehat p=0{,}2$\\perdita $=0{,}64$};
\node[pNote,text width=8.4cm] at(4.7,.6){Una previsione molto sicura e sbagliata riceve una penalità maggiore};
\end{tikzpicture}
\PBody{Il punteggio confronta probabilità e risposte senza soglie. Valori più bassi indicano una perdita minore.}
''',r'''
\PCode{R · probabilità contro risposta}{080_brier.R}
\PSmall{Il valore sul campione di stima è una descrizione dell’adattamento. Per misurare la prestazione predittiva si usa un campione separato e un riferimento stimato solo sul training.}
''','Un modello può produrre le stesse classi di un altro e assegnare probabilità molto diverse.')

code(81,'calibrazione',r'''
# Intervalli fissi di probabilita'.
d81 <- data.frame(
  bin = cut(p_log, breaks = seq(0, 1, 0.2),
            include.lowest = TRUE),
  p = p_log, y = f$spiky)
aggregate(cbind(p, y) ~ bin,
          data = d81, FUN = mean)
table(d81$bin)
''')
S(81,'La calibrazione delle probabilità',r'''
\PLabel{Probabilità previste e frequenze osservate}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[pAxis](.7,.6)--(8.9,.6);\draw[pAxis](.7,.6)--(.7,4.35);
\draw[Muted,dashed](.9,.8)--(8.35,4.1);
\foreach \x/\y/\n in {1.7/1.15/7,3.4/1.65/16,5.2/2.95/22,7.3/3.4/9}{
\fill[GeoA](\x,\y) circle(2.7pt);\node[pNote,text=GeoA] at(\x,\y+.38){$n=\n$};}
\node[pNote] at(4.8,.15){Probabilità media nel gruppo};
\node[pNote,anchor=west] at(.8,4.7){Frequenza osservata · schema illustrativo};
\end{tikzpicture}
\PBody{Tra casi con probabilità prevista vicina a $0{,}7$, ci si aspetta circa il 70\% di eventi in ripetizioni adeguate. Gruppi piccoli producono frequenze instabili.}
''',r'''
\PCode{R · medie e numerosità per intervallo}{081_calibrazione.R}
\PSmall{La tabella confronta probabilità e frequenze medie. \texttt{table()} mostra le numerosità.}
\PSmall{La figura è uno schema. La calibrazione va poi verificata su nuovi dati.}
''','La calibrazione richiede probabilità, frequenze e numerosità. La verifica predittiva deve usare osservazioni lasciate fuori dalla stima.')

assert set(SLIDES) == set(range(42,82))

