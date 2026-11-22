"""Borealis M09: processi, trasformazioni e test (slide 54–96)."""
from process_diagrams import *

SLIDES={}
CODES={}

def S(n,title,left,right,recall):
    sec='V · PROCESSI E STAZIONARIETÀ' if n<=67 else 'VI · TREND E TRASFORMAZIONI' if n<=83 else 'VII · DIAGNOSI CON ADF E KPSS'
    SLIDES[n]=dict(title=title,section=sec,left=left.strip(),right=right.strip(),recall=recall)

def C(n,name,text,title):
    filename=f'{n:03}_{name}.R'
    CODES[filename]=text.strip()+'\n'
    return rf'\PCode{{R · {title}}}{{{filename}}}'

S(54,'Un processo, molte traiettorie',paths()+r'''
\[\{X_t:t\in\mathbb Z\},\qquad x_1,\ldots,x_n.\]
\PSmall{$X_t$ è una variabile casuale. $x_t$ è il valore osservato in una realizzazione del processo.}
''',r'''
\PBody{Il modello descrive come potrebbero variare le osservazioni nel tempo. Il file contiene una sola traiettoria, registrata in condizioni specifiche.}
\vspace{4mm}
\PInfo{Per studiare una proprietà del processo possiamo simulare molte repliche. Le repliche permettono di confrontare la distribuzione allo stesso istante.}
\vspace{3mm}
\PBody{Una traiettoria che sembra regolare non dimostra, da sola, una proprietà della distribuzione.}
''','La serie osservata è una realizzazione. Stazionarietà e dipendenza sono proprietà del modello probabilistico.')

S(55,'Le condizioni di stazionarietà debole',stationarity()+r'''
\[
\begin{aligned}
\mathbb E(X_t)&=\mu,\\
\operatorname{Var}(X_t)&=\gamma(0)<\infty,\\
\operatorname{Cov}(X_t,X_{t-k})&=\gamma(k).
\end{aligned}
\]
''',r'''
\PBody{La media e la varianza restano costanti. La covarianza dipende dal ritardo $k$, senza dipendere dalla posizione nel calendario.}
\vspace{4mm}
\PInfo{La stazionarietà debole riguarda momenti di ordine uno e due. Una distribuzione completa invariata richiede una condizione più forte.}
\vspace{3mm}
\PBody{Un grafico aiuta a individuare incompatibilità evidenti. La stabilità apparente di un tratto breve offre un’evidenza limitata.}
''','L’ACF di un processo stazionario dipende dalla distanza temporale fra le osservazioni.')

S(56,'Il rumore bianco ha covarianze nulle',acf_theory('white')+r'''
\[\mathbb E(\varepsilon_t)=0,\qquad
\operatorname{Var}(\varepsilon_t)=\sigma_\varepsilon^2.\]
\[\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-k})=0\quad(k\ne0).\]
''',C(56,'rumore',r'''
set.seed(19056)
# Rumore gaussiano IID.
e56 <- rnorm(300)
acf(e56, lag.max = 24,
    main = "Rumore bianco simulato")
# L'ACF campionaria oscilla attorno a zero.
mean(e56)
var(e56)
''','simulare rumore bianco')+r'''
\PInfo{IID significa indipendente e identicamente distribuito. Con varianza finita, rumore IID a media zero soddisfa le condizioni di rumore bianco.}
\PSmall{Il grafico mostra la teoria. L’ACF calcolata da 300 valori presenta fluttuazioni campionarie.}
''','Covarianze nulle escludono dipendenza lineare ai ritardi considerati. L’indipendenza richiede di più.')

S(57,'Assenza di correlazione e dipendenza',dependence()+r'''
\[U_t\overset{\mathrm{IID}}\sim\mathcal N(0,1),\qquad E_t=U_{t-1}U_t.\]
\[\operatorname{Corr}(E_t,E_{t+1})=0,\qquad
\operatorname{Corr}(E_t^2,E_{t+1}^2)=\tfrac14.\]
''',C(57,'dipendenza',r'''
set.seed(19057)
u57 <- rnorm(10001)
e57 <- head(u57, -1) * tail(u57, -1)
# Stessa coppia di tempi, due confronti.
cor(head(e57, -1), tail(e57, -1))
cor(head(e57^2, -1), tail(e57^2, -1))
''','confrontare valori e quadrati')+r'''
\PBody{I valori hanno covarianza nulla. I loro quadrati condividono $U_t^2$: un valore grande di questo fattore può rendere grandi entrambi i prodotti.}
\PInfo{Questo esempio soddisfa la definizione debole di rumore bianco, pur conservando dipendenza non lineare.}
''','Un’ACF vicina a zero non esaurisce lo studio della dipendenza temporale.')

S(58,'L’AR(1) eredita una parte del passato',ar_recursion()+r'''
\[X_t=\phi X_{t-1}+\varepsilon_t,\qquad |\phi|<1.\]
\PSmall{Innovazioni a media zero, varianza $\sigma_\varepsilon^2$, indipendenti dal passato. Per ora il livello medio è zero.}
''',C(58,'ar1',r'''
set.seed(19058)
# arima.sim gestisce il tratto iniziale.
a58 <- arima.sim(
  model = list(ar = 0.65), n = 300)
plot(a58, ylab = "Valore",
     main = "AR(1), phi = 0.65")
acf(a58, lag.max = 24)
''','generare una traiettoria AR(1)')+r'''
\PBody{$\phi$ controlla quanto del valore precedente entra in quello successivo. L’innovazione aggiunge informazione nuova.}
\PInfo{La condizione $|\phi|<1$ ammette una soluzione stazionaria. Occorre considerare anche come parte la simulazione.}
''','Nell’AR(1), la memoria del passato è regolata da un solo coefficiente.')

S(59,'L’effetto di uno shock si attenua',impulse()+r'''
\[\varepsilon_t=1\quad\Longrightarrow\quad
\text{effetto su }X_{t+k}=\phi^k.\]
\PSmall{Si confrontano due traiettorie identiche, alle quali si aggiunge uno shock unitario in una sola data.}
''',C(59,'impulso',r'''
# Risposta teorica a un impulso unitario.
k59 <- 0:12
effetto59 <- 0.65^k59
data.frame(ritardo = k59,
           effetto = round(effetto59, 4))
''','quantificare la persistenza')+r'''
\PBody{Con $\phi=0{,}65$, dopo quattro passi resta circa il 18\% dello shock iniziale. Il decadimento prosegue geometricamente.}
\PInfo{Per $-1<\phi<0$ l’effetto cambia segno a ogni passo, mentre la sua ampiezza diminuisce.}
''','La persistenza di uno shock dipende da φ. Vicino a uno, il decadimento diventa lento.')

S(60,'La varianza dell’AR(1) in equilibrio',variance_balance()+r'''
\[
\begin{aligned}
\gamma(0)&=\phi^2\gamma(0)+\sigma_\varepsilon^2,\\
\gamma(0)&=\frac{\sigma_\varepsilon^2}{1-\phi^2}.
\end{aligned}
\]
''',C(60,'varianza_ar',r'''
phi60 <- c(0, 0.3, 0.65, 0.9)
# Innovazioni con varianza unitaria.
data.frame(phi = phi60,
  varianza = 1 / (1 - phi60^2))
''','varianza e persistenza')+r'''
\PBody{L’innovazione è incorrelata con $X_{t-1}$, quindi il termine di covarianza della somma è nullo. La stazionarietà impone la stessa varianza nei due tempi.}
\PInfo{A parità di varianza delle innovazioni, un valore maggiore di $|\phi|$ produce una varianza marginale più grande.}
''','La varianza del processo combina la variabilità delle innovazioni e la persistenza del passato.')

S(61,'L’ACF teorica dell’AR(1)',ar_acfs()+r'''
\[\gamma(k)=\phi\gamma(k-1)\ (k\ge1),\qquad
\rho(k)=\phi^{|k|}.\]
\PSmall{Tre ACF teoriche di processi AR(1) stazionari.}
''',C(61,'acf_ar',r'''
k61 <- 0:12
# Curve teoriche, senza errore campionario.
rho61 <- sapply(c(0.65, -0.65, 0.9),
               function(p) p^k61)
matplot(k61, rho61, type = "b",
        xlab = "Ritardo", ylab = "ACF")
abline(h = 0, col = "grey70")
''','confrontare tre coefficienti')+r'''
\PBody{Un coefficiente positivo genera un decadimento dello stesso segno. Un coefficiente negativo alterna correlazioni positive e negative.}
\PInfo{Un tratto breve di ACF osservata può assomigliare a più modelli. La forma teorica orienta il confronto.}
''','Il segno e la velocità di decadimento dell’ACF descrivono aspetti diversi della memoria.')

S(62,'L’inizializzazione modifica i primi passi',initial_variance()+r'''
\[\operatorname{Var}(X_h\mid X_0=0)
=\sigma_\varepsilon^2\frac{1-\phi^{2h}}{1-\phi^2}.\]
\PSmall{La varianza parte da zero e si avvicina al limite stazionario. $h$ conta i passi dopo il valore fissato.}
''',C(62,'inizializzazione',r'''
# Il CSV fornito parte da un valore fissato.
head(proc[, c("passo", "ar1")])
stopifnot(proc$ar1[1] == 0)
h62 <- 0:10
v62 <- (1 - 0.65^(2 * h62)) /
       (1 - 0.65^2)
data.frame(passi = h62, varianza = v62)
''','riconoscere il transitorio')+r'''
\PInfo{L’AR(1) del CSV ha $\phi=0{,}65$ e inizia da zero. I primi valori seguono un transitorio: il file non parte dalla distribuzione stazionaria.}
''','Il parametro ammette un processo stazionario, ma una partenza fissata ne modifica la distribuzione iniziale.')

S(63,'Lo stesso rumore, due memorie diverse',two_paths()+r'''
\PSmall{Schema con innovazioni condivise e valori iniziali nulli. Cambia soltanto il coefficiente autoregressivo.}
''',C(63,'rumore_comune',r'''
set.seed(19063)
e63 <- rnorm(150)
ar63 <- function(phi) {
  x <- numeric(length(e63))
  for (t in 2:length(x))
    x[t] <- phi * x[t-1] + e63[t]
  x
}
# Le due traiettorie usano lo stesso e63.
matplot(cbind(ar63(0.3), ar63(0.9)),
        type = "l", ylab = "Valore")
''','isolare l’effetto di φ')+r'''
\PBody{Usare le stesse innovazioni rende più leggibile l’effetto di un parametro. Per stimare una distribuzione servono invece repliche indipendenti.}
''','Una simulazione comparativa dichiara quali elementi sono condivisi e quali cambiano.')

S(64,'Nel random walk gli shock si accumulano',accumulation()+r'''
\[X_t=X_{t-1}+\varepsilon_t
=X_0+\sum_{j=1}^{t}\varepsilon_j.\]
\PSmall{$X_0$ fissato. Innovazioni indipendenti, a media zero e varianza $\sigma_\varepsilon^2$.}
''',C(64,'random_walk',r'''
set.seed(19064)
e64 <- rnorm(150)
# X0 = 0. cumsum conserva gli shock.
rw64 <- c(0, cumsum(e64))
plot(0:150, rw64, type = "l",
     xlab = "Tempo", ylab = "X")
stopifnot(isTRUE(all.equal(
  diff(rw64), e64)))
''','costruire i livelli')+r'''
\PInfo{Ogni innovazione modifica tutti i livelli successivi. La differenza fra due valori consecutivi restituisce l’innovazione.}
''','Un random walk senza deriva può mostrare lunghi tratti crescenti o decrescenti in una singola realizzazione.')

S(65,'La dispersione cresce con il tempo',rw_variance()+r'''
\[\operatorname{Var}(X_t)=t\sigma_\varepsilon^2,\qquad
\operatorname{SD}(X_t)=\sqrt t\,\sigma_\varepsilon.\]
\PSmall{Curve teoriche a due deviazioni standard. Con innovazioni gaussiane descrivono bande marginali, non simultanee.}
''',C(65,'varianza_rw',r'''
t65 <- c(1, 4, 25, 100)
# X0 fissato, varianza innovazioni = 1.
data.frame(tempo = t65,
           varianza = t65,
           deviazione = sqrt(t65))
''','distinguere varianza e deviazione')+r'''
\PBody{Le covarianze tra innovazioni diverse sono nulle. La varianza della somma è quindi la somma delle varianze.}
\PInfo{La distribuzione dei livelli cambia con il tempo. La media costante, da sola, non rende stazionario il random walk.}
''','Il random walk ha innovazioni con varianza costante, ma livelli con varianza crescente.')

S(66,'La varianza si confronta tra repliche',ensemble()+r'''
\[\widehat{\operatorname{Var}}(X_t)
=\frac{1}{B-1}\sum_{b=1}^{B}
\bigl(X_t^{(b)}-\bar X_t\bigr)^2.\]
''',C(66,'repliche',r'''
set.seed(19066)
B66 <- 2000
# Ogni colonna usa innovazioni nuove.
rw66 <- replicate(B66, cumsum(rnorm(100)))
# Varianza tra repliche, a tempo fissato.
v66 <- apply(rw66, 1, var)
round(v66[c(1, 25, 100)], 1)
''','stimare la dispersione marginale')+r'''
\PBody{Si confrontano le colonne alla stessa riga temporale. La dispersione lungo una singola traiettoria risponde a una domanda diversa.}
\PInfo{Poche repliche producono stime instabili. L’esperimento sul sito usa sei traiettorie per rendere visibile l’idea.}
''','Nel confronto tra tempi, la varianza marginale richiede repliche indipendenti allo stesso istante.')

S(67,'AR(1) e random walk reagiscono diversamente',impulse(compare=True)+r'''
\[\text{AR(1): }\phi^k\longrightarrow0,
\qquad\text{random walk: }1.\]
''',r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m09-stazionarieta}{Esperimento · Stazionarietà}
\PBody{Nell’AR(1) stazionario, il passato perde peso. Nel random walk, lo shock modifica in modo permanente il livello della traiettoria.}
\vspace{4mm}
\PInfo{Un AR(1) con $\phi$ molto vicino a uno può somigliare a un random walk su campioni brevi. La lunghezza della serie limita la distinzione empirica.}
\vspace{3mm}
\PBody{Confrontiamo quindi il grafico, la dipendenza e le ipotesi del modello prima di scegliere una trasformazione.}
''','Persistenza elevata e radice unitaria possono essere difficili da distinguere in una serie breve.')

S(68,'Un trend può avere origini diverse',trend_comparison()+r'''
\[X_t=a+bt+U_t\qquad\text{oppure}\qquad
X_t=X_{t-1}+\varepsilon_t.\]
\PSmall{Nel primo modello $U_t$ è stazionario. Nel secondo, il livello accumula innovazioni.}
''',r'''
\PBody{Nel trend deterministico, una funzione del tempo descrive il cambiamento della media. Nel random walk, gli shock cambiano la traiettoria futura.}
\vspace{4mm}
\PInfo{Una linea crescente in un grafico non identifica il meccanismo che l’ha generata. Le due spiegazioni conducono a trasformazioni e interpretazioni differenti.}
\vspace{3mm}
\PBody{La scelta deve rispettare le conoscenze sul fenomeno e le caratteristiche del campione.}
''','Togliere un trend e calcolare differenze sono operazioni con obiettivi diversi.')

S(69,'Il detrending sottrae un andamento stimato',detrending()+r'''
\[\widehat U_t=X_t-(\widehat a+\widehat b\,t).\]
\PSmall{Si sottrae una funzione del tempo. I residui restano allineati alle date originali.}
''',C(69,'detrending',r'''
# Temperatura sintetica: una retta da verificare.
t69 <- seq_along(z)
fit69 <- lm(as.numeric(z) ~ t69)
res69 <- residuals(fit69)
plot(t69, res69, type = "l",
     xlab = "Mese", ylab = "Residuo")
acf(res69, lag.max = 36)
''','esaminare i residui')+r'''
\PInfo{Nella temperatura resta una forte componente stagionale. Sottrarre una retta non elimina automaticamente la dipendenza o la stagionalità.}
''','I residui richiedono una nuova diagnosi. La rimozione di un trend non dimostra la stazionarietà.')

S(70,'La differenza misura un incremento',difference()+r'''
\[\Delta X_t=X_t-X_{t-1}.\]
\[10,\ 13,\ 12,\ 16\quad\longmapsto\quad3,\ -1,\ 4.\]
''',C(70,'incrementi',r'''
x70 <- c(10, 13, 12, 16)
diff(x70)
# Il secondo incremento e' negativo.
stopifnot(identical(diff(x70),
                    c(3, -1, 4)))
''','leggere un cambiamento')+r'''
\PBody{La differenza confronta due posizioni adiacenti. Per interpretarla serve conoscere l’intervallo temporale fra quelle posizioni.}
\PInfo{Una differenza mantiene l’unità della variabile. Dividere per la durata definisce invece un tasso di variazione.}
''','L’incremento descrive quanto cambia la variabile fra due tempi. La durata determina il significato del confronto.')

S(71,'La prima differenza perde una posizione',month_calendar(1)+r'''
\[\Delta x_2,\ldots,\Delta x_n\quad\text{contiene }n-1\text{ valori}.\]
''',C(71,'date_differenze',r'''
dy71 <- diff(y)
# Ogni differenza assume la data finale.
tab71 <- data.frame(
  data = tail(d$data, -1),
  incremento_ppm = as.numeric(dy71))
head(tab71)
c(n = length(dy71), start(dy71))
''','conservare il calendario')+r'''
\PBody{Per la CO$_2$ mensile, il primo incremento riguarda gennaio–febbraio 1985 e viene datato febbraio 1985.}
\PInfo{La serie iniziale ha 204 mesi. La prima differenza ne conserva 203. Nessuna interpolazione è necessaria sul segmento completo.}
''','Ogni trasformazione deve aggiornare insieme valori, numero di osservazioni e date.')

S(72,'La differenza stagionale confronta due anni',difference(lag=12)+r'''
\[\Delta_{12}X_t=X_t-X_{t-12}.\]
\PSmall{Gennaio si confronta con gennaio dell’anno precedente. La frequenza mensile rende il ritardo 12 interpretabile come un anno.}
''',r'''
\PBody{Una componente esattamente periodica con periodo 12 si annulla nella differenza stagionale. Rimangono il cambiamento del trend e quello del resto.}
\vspace{3mm}
\[
S_t-S_{t-12}=0\quad\text{se }S_t=S_{t-12}.
\]
\PInfo{Se forma o ampiezza stagionale cambiano, la cancellazione è incompleta. La serie trasformata richiede una nuova lettura.}
''','Il ritardo stagionale deriva dal calendario e dalla periodicità ipotizzata.')

S(73,'La differenza stagionale in R',month_calendar(12)+r'''
\[n=204\quad\Longrightarrow\quad n-12=192.\]
''',C(73,'stagionale',r'''
ds73 <- diff(y, lag = 12)
# Il primo valore confronta due gennaio.
data.frame(
  data = tail(d$data, -12),
  variazione_annua = as.numeric(ds73))[1:4, ]
c(start(ds73), end(ds73))
length(ds73)
''','confrontare lo stesso mese')+r'''
\PBody{Il primo risultato è datato gennaio 1986. La differenza stagionale misura un cambiamento su dodici mesi, espresso in ppm.}
\PInfo{\texttt{lag = 12} indica la distanza fra i termini. \texttt{differences = 12} chiederebbe dodici differenze consecutive di ordine uno.}
''','In diff(), il ritardo e l’ordine della differenza sono parametri distinti.')

S(74,'L’operatore ritardo compatta la scrittura',lag_operator()+r'''
\[BX_t=X_{t-1},\qquad B^{12}X_t=X_{t-12}.\]
\[\Delta X_t=(1-B)X_t,\qquad
\Delta_{12}X_t=(1-B^{12})X_t.\]
''',C(74,'operatore',r'''
# Identita' su un vettore numerico.
v74 <- as.numeric(y)
manuale74 <- v74[-1] - head(v74, -1)
stopifnot(isTRUE(all.equal(
  manuale74, as.numeric(diff(y)))))
''','verificare la notazione')+r'''
\PBody{$B$ sposta il riferimento temporale di un passo. Il simbolo $1$ lascia il termine alla sua data.}
\PInfo{La scrittura con operatori permette di sviluppare una trasformazione combinata e controllare tutti i segni.}
''','Un operatore ritardo descrive come cambiano gli indici temporali.')

S(75,'La differenza combinata usa quattro date',difference(combined=True)+r'''
\[
\begin{aligned}
(1-B)(1-B^{12})X_t
&=X_t-X_{t-1}\\
&\quad-X_{t-12}+X_{t-13}.
\end{aligned}
\]
''',C(75,'combinata',r'''
dc75 <- diff(diff(y, lag = 12))
# Cambiare l'ordine produce lo stesso filtro.
alt75 <- diff(diff(y), lag = 12)
stopifnot(isTRUE(all.equal(dc75, alt75)))
plot(dc75, ylab = "Differenza combinata")
acf(dc75, lag.max = 36)
''','comporre due differenze')+r'''
\PBody{La trasformazione confronta la variazione mensile con la variazione dello stesso intervallo nell’anno precedente.}
\PInfo{Le due differenze commutano su questa griglia completa. L’allineamento finale rimane parte del risultato.}
''','Sviluppare gli operatori rende controllabili segni, date e interpretazione della trasformazione.')

S(76,'Le differenze riducono la numerosità',losses()+r'''
\[204-1-12=191.\]
\PSmall{La differenza combinata inizia a febbraio 1986 e termina a dicembre 2001.}
''',C(76,'numerosita',r'''
# Confronto sul segmento completo.
forme76 <- list(livelli = y,
  ordinaria = diff(y),
  stagionale = diff(y, lag = 12),
  combinata = diff(diff(y, lag = 12)))
sapply(forme76, length)
sapply(forme76, start)
''','contare i valori disponibili')+r'''
\PBody{I valori iniziali non hanno antecedenti sufficienti. La data del primo risultato dipende dal filtro applicato.}
\PInfo{Se si vogliono confrontare metodi sullo stesso periodo, occorre prima allineare gli intervalli effettivamente disponibili.}
''','Una trasformazione cambia il campione utilizzabile. Il confronto deve dichiarare l’intervallo comune.')

S(77,'Le condizioni iniziali consentono di risalire',reconstruction()+r'''
\PSmall{Le differenze ordinarie perdono un livello iniziale. Le differenze stagionali richiedono un valore iniziale per ciascun mese.}
''',C(77,'ricostruzione',r'''
v77 <- as.numeric(y)
ric77 <- c(v77[1],
           v77[1] + cumsum(diff(v77)))
# Tolleranza dovuta all'aritmetica numerica.
max(abs(ric77 - v77))
stopifnot(max(abs(ric77 - v77)) < 1e-10)
''','ricostruire i livelli')+r'''
\PBody{Le differenze conservano il cambiamento relativo. Per ricostruire i livelli occorre mantenere le informazioni iniziali eliminate dal filtro.}
\PInfo{Il dataset originale rimane quindi necessario anche quando l’analisi usa una versione trasformata.}
''','Il registro della trasformazione conserva formule, calendario e condizioni iniziali.')

S(78,'Differenziare rumore crea dipendenza',shared_noise()+r'''
\[D_t=\varepsilon_t-\varepsilon_{t-1},\qquad
D_{t+1}=\varepsilon_{t+1}-\varepsilon_t.\]
''',r'''
\PBody{Due differenze consecutive condividono un’innovazione. Il suo segno cambia fra la prima e la seconda differenza.}
\vspace{3mm}
\PInfo{Se $\varepsilon_t$ è rumore bianco, la serie originale ha covarianze nulle ai ritardi diversi da zero. La differenziazione introduce una covarianza negativa al ritardo uno.}
\vspace{3mm}
\PBody{Questo meccanismo permette di riconoscere un possibile effetto di una trasformazione superflua.}
''','Una trasformazione può creare una struttura di dipendenza che prima non era presente.')

S(79,'Il valore −1/2 deriva dalla covarianza',acf_theory('diff')+r'''
\[
\begin{aligned}
\operatorname{Var}(D_t)&=2\sigma_\varepsilon^2,\\
\operatorname{Cov}(D_t,D_{t+1})&=-\sigma_\varepsilon^2,\\
\rho_D(1)&=-\tfrac12.
\end{aligned}
\]
''',r'''
\PBody{La covarianza contiene quattro prodotti. Tre si annullano perché coinvolgono tempi diversi del rumore bianco.}
\vspace{3mm}
\[
\operatorname{Cov}(\varepsilon_t,-\varepsilon_t)
=-\sigma_\varepsilon^2.
\]
\PInfo{Ai ritardi $|k|>1$ le due differenze non condividono innovazioni. Le loro covarianze sono quindi nulle.}
\PSmall{Il risultato vale per differenze di rumore bianco con varianza finita. Non è una formula universale per ogni serie differenziata.}
''','Per rumore bianco differenziato, la varianza raddoppia e l’ACF al primo ritardo vale −1/2.')

S(80,'Una simulazione controlla il risultato',acf_theory('diff')+r'''
\PSmall{Curva teorica da confrontare con l’ACF campionaria. Il valore osservato oscilla attorno a $-1/2$.}
''',C(80,'sovradifferenza',r'''
set.seed(19080)
e80 <- rnorm(10000)
de80 <- diff(e80)
r80 <- acf(de80, lag.max = 10,
           plot = FALSE)$acf
round(c(varianza = var(de80),
        acf1 = r80[2]), 3)
acf(de80, lag.max = 10)
''','verificare con molte osservazioni')+r'''
\PBody{Con innovazioni di varianza uno, attendiamo una varianza delle differenze vicina a due e un’ACF al primo ritardo vicina a $-0{,}5$.}
\PInfo{Aumentare la numerosità riduce le fluttuazioni della simulazione. Il calcolo teorico chiarisce perché emerge questo valore.}
''','La simulazione verifica un meccanismo noto e aiuta a distinguere teoria ed errore campionario.')

S(81,'Un primo ritardo negativo ha più spiegazioni',two_acfs()+r'''
\PSmall{Entrambe le ACF iniziano da $\rho(1)=-0{,}5$. I ritardi successivi differiscono.}
''',C(81,'alternative',r'''
# Due ACF teoriche con lo stesso primo lag.
lag81 <- 0:8
acf_diff81 <- c(1, -0.5, rep(0, 7))
acf_ar81 <- (-0.5)^lag81
data.frame(lag = lag81,
  rumore_differenziato = acf_diff81,
  ar_negativo = acf_ar81)
''','confrontare due spiegazioni')+r'''
\PBody{Un’ACF negativa al primo ritardo può dipendere da una differenziazione superflua oppure dalla dinamica del processo originario.}
\PInfo{Occorre conoscere i passaggi già applicati e leggere più ritardi. Un singolo valore non identifica la causa.}
''','La diagnosi di sovradifferenziazione richiede il confronto con la serie originale e con modelli alternativi.')

S(82,'Detrending e differenza lasciano resti diversi',detrending()+r'''
\[X_t=a+bt+\varepsilon_t
\quad\Longrightarrow\quad
\Delta X_t=b+\varepsilon_t-\varepsilon_{t-1}.\]
''',C(82,'due_trasformazioni',r'''
set.seed(19082)
t82 <- 1:200
x82 <- 10 + 0.04 * t82 + rnorm(200)
r82 <- residuals(lm(x82 ~ t82))
d82 <- diff(x82)
# Lo stesso input, due resti differenti.
c(detrend = acf(r82, plot = FALSE)$acf[2],
  differenza = acf(d82, plot = FALSE)$acf[2])
''','confrontare le due operazioni')+r'''
\PInfo{Con un trend lineare e rumore bianco, la differenza elimina il livello e lascia il coefficiente $b$, insieme a rumore differenziato. I residui della retta rispondono a una diversa costruzione.}
''','La trasformazione va scelta rispetto al modello ipotizzato e alla domanda scientifica.')

S(83,'Un registro per le trasformazioni',register()+r'''
\PSmall{Per una differenza: ritardo, ordine, unità, data iniziale, data finale e valori iniziali da conservare.}
''',C(83,'registro',r'''
registro83 <- data.frame(
  serie = c("livelli", "diff1", "diff12", "combinata"),
  n = sapply(forme76, length),
  prima_data = as.character(d$data[c(1,2,13,14)]),
  ultima_data = as.character(tail(d$data, 1)))
registro83
''','documentare il campione')+r'''
\PBody{Il registro permette di leggere un grafico e risalire al file originario. Aiuta anche a evitare confronti involontari fra periodi diversi.}
\PInfo{Un filtro centrato richiede inoltre di dichiarare quali valori futuri usa. Questa informazione conta quando si prepara una valutazione temporale.}
''','Ogni versione della serie deve conservare una descrizione verificabile della propria costruzione.')

S(84,'ADF e KPSS partono da ipotesi diverse',nulls()+r'''
\PSmall{Le ipotesi dipendono dai termini deterministici e dalla correzione della dipendenza adottati nel test.}
''',r'''
\PBody{ADF considera l’ipotesi di una radice unitaria nella specificazione scelta. KPSS considera la stazionarietà attorno a un livello oppure a un trend deterministico.}
\vspace{4mm}
\PInfo{Il mancato rifiuto indica che il campione non offre evidenza sufficiente contro l’ipotesi. Non dimostra che l’ipotesi sia vera.}
\vspace{3mm}
\PBody{Confrontare i due test aiuta a circoscrivere la diagnosi, purché le specificazioni rispondano alla stessa domanda.}
''','Il significato del p-value dipende dall’ipotesi nulla e dal modello utilizzato per calcolarlo.')

S(85,'La regressione ausiliaria dell’ADF',adf_design()+r'''
\[
\Delta X_t=a+bt+\gamma X_{t-1}
+\sum_{j=1}^{p}\delta_j\Delta X_{t-j}+u_t.
\]
\[H_0:\gamma=0,\qquad \gamma=\phi-1\ \text{nell’AR(1)}.\]
''',r'''
\PBody{Il livello passato serve a valutare la radice unitaria. Le differenze passate descrivono la dinamica di breve periodo dei residui.}
\vspace{3mm}
\[
\tau=\frac{\widehat\gamma}
{\operatorname{SE}(\widehat\gamma)}.
\]
\PInfo{Sotto l’ipotesi di radice unitaria, il riferimento della statistica non è la distribuzione $t$ ordinaria della regressione. Servono valori critici specifici.}
''','La regressione ADF si può stimare con OLS, ma il test della radice unitaria usa un riferimento non standard.')

S(86,'Costante e trend cambiano la domanda',deterministic_terms()+r'''
\[\Delta X_t=a+bt+\gamma X_{t-1}+\cdots+u_t.\]
''',r'''
\PBody{La scelta dei termini deterministici specifica quale andamento può essere presente anche quando si studia la stazionarietà degli scarti.}
\vspace{3mm}
\PInfo{\texttt{tseries::adf.test()} usa una regressione con costante e trend lineare. Il suo argomento \texttt{k} controlla le differenze ritardate, senza scegliere questi termini.}
\vspace{3mm}
\PBody{L’ADF semplificato del sito comprende una costante e una differenza ritardata, senza trend lineare. I due calcoli non hanno la stessa specificazione.}
''','La specificazione deterministica deve accompagnare ogni risultato del test.')

S(87,'Le differenze ritardate controllano i residui',lag_regression()+r'''
\[\sum_{j=1}^{p}\delta_j\Delta X_{t-j}.\]
''',C(87,'ritardi_adf',r'''
# Analisi di sensibilita', non ricerca del p minimo.
ks87 <- c(1, 4, 8)
stat87 <- sapply(ks87, function(k) {
  tseries::adf.test(as.numeric(y),
                    k = k)$statistic
})
data.frame(k = ks87, statistica = stat87)
''','variare la correzione')+r'''
\PBody{Pochi ritardi possono lasciare dipendenza nei residui. Molti ritardi consumano osservazioni e aumentano il numero di parametri da stimare.}
\PInfo{La sensibilità della conclusione ai ritardi è un risultato da discutere. Scegliere il solo p-value più favorevole altera la domanda iniziale.}
''','Il numero di ritardi descrive una scelta di modello e influenza l’informazione disponibile per il test.')

S(88,'Un ADF eseguito e documentato',adf_design()+r'''
\PSmall{La chiamata specifica $k=4$. Il riferimento include la costante e il trend previsti da \texttt{tseries::adf.test()}.}
''',C(88,'adf',r'''
# Pacchetto richiesto dal progetto.
stopifnot(requireNamespace("tseries",
                          quietly = TRUE))
adf88 <- tseries::adf.test(
  as.numeric(y), k = 4)
adf88
# Campi da riportare nel resoconto.
adf88[c("statistic", "parameter",
        "p.value", "alternative")]
''','conservare l’output del test')+r'''
\PBody{Annotiamo serie utilizzata, intervallo, numerosità, ritardi e termini deterministici. Il p-value acquista significato all’interno di questa descrizione.}
\PInfo{Un eventuale avviso sui limiti delle tabelle è parte del risultato e deve restare nel resoconto.}
''','Un risultato riproducibile comprende la chiamata, la specificazione e gli avvisi numerici.')

S(89,'KPSS esamina le somme dei residui',kpss_sums()+r'''
\[S_t=\sum_{j=1}^{t} e_j,\qquad
\eta=\frac{\sum_{t=1}^{n}S_t^2}{n^2\widehat\omega^2}.\]
\PSmall{$e_t$: scarti da un livello o da un trend. $\widehat\omega^2$: stima della varianza di lungo periodo.}
''',C(89,'somme_parziali',r'''
# Versione Level: si sottrae la media.
e89 <- as.numeric(y) - mean(y)
S89 <- cumsum(e89)
plot(S89, type = "l", ylab = "Somma residui",
     xlab = "Mese")
abline(h = 0, col = "grey70")
''','visualizzare l’accumulo')+r'''
\PBody{Scarti persistenti dallo stesso lato del riferimento fanno accumulare le somme parziali. La statistica ne misura l’ampiezza, tenendo conto della dipendenza.}
''','KPSS valuta l’accumulo degli scarti rispetto al riferimento deterministico scelto.')

S(90,'La varianza di lungo periodo usa i ritardi',bartlett()+r'''
\[\widehat\omega^2=\widehat\gamma_e(0)
+2\sum_{j=1}^{L}\left(1-\frac{j}{L+1}\right)
\widehat\gamma_e(j).\]
\PSmall{Schema della correzione Bartlett: i contributi ai ritardi più lontani ricevono peso minore.}
''',r'''
\PBody{La dipendenza dei residui modifica la variabilità delle somme parziali. La sola varianza istantanea non riassume questo effetto.}
\vspace{4mm}
\PInfo{La larghezza $L$ determina quali autocovarianze entrano nella stima. In \texttt{tseries::kpss.test()}, \texttt{lshort} seleziona una regola di troncamento.}
\vspace{3mm}
\PBody{La scelta della correzione e la numerosità possono influenzare la diagnosi. Devono comparire insieme al risultato.}
''','La correzione della dipendenza è parte del test KPSS, non un dettaglio separato dalla statistica.')

S(91,'KPSS può riferirsi al livello o al trend',deterministic_terms()+r'''
\[H_0^{\rm Level}:X_t=\mu+U_t,\qquad
H_0^{\rm Trend}:X_t=a+bt+U_t.\]
\PSmall{$U_t$ stazionario nell’ipotesi nulla. Le due versioni rimuovono riferimenti diversi.}
''',C(91,'kpss',r'''
kL91 <- tseries::kpss.test(as.numeric(y),
  null = "Level", lshort = TRUE)
kT91 <- tseries::kpss.test(as.numeric(y),
  null = "Trend", lshort = TRUE)
kL91
kT91
''','dichiarare il riferimento')+r'''
\PInfo{Una serie con trend deterministico può essere incompatibile con la versione Level e compatibile con quella Trend. La differenza riguarda l’ipotesi valutata.}
''','Prima di confrontare p-value, occorre confrontare le ipotesi e i termini deterministici.')

S(92,'Lettura congiunta dei due test',decisions()+r'''
\PSmall{Schema interpretativo, a soglia dichiarata e con specificazioni coerenti. Nessuna casella identifica automaticamente il processo.}
''',r'''
\PBody{Il rifiuto ADF con mancato rifiuto KPSS è compatibile con una descrizione stazionaria rispetto al riferimento scelto. Il caso opposto è compatibile con una radice unitaria.}
\vspace{3mm}
\PInfo{Se entrambi rifiutano, vanno esaminati specificazione, discontinuità e altre forme di non stazionarietà. Se nessuno rifiuta, il campione può discriminare poco.}
\vspace{3mm}
\PBody{Grafici, ACF e conoscenza del processo aiutano a interpretare tutti e quattro i casi.}
''','ADF e KPSS forniscono evidenze complementari. La conclusione rimane condizionata al modello e al campione.')

S(93,'I limiti dei p-value vanno riportati',p_bounds()+r'''
\PSmall{Limiti illustrati per KPSS. ADF usa anche il limite superiore 0,99. L’avviso precisa la disuguaglianza da riportare.}
''',C(93,'avvisi',r'''
w93 <- character()
a93 <- withCallingHandlers(
  tseries::adf.test(as.numeric(y), k = 4),
  warning = function(w) {
    w93 <<- c(w93, conditionMessage(w))
  })
# Gli avvisi sono registrati e restano visibili.
list(test = a93, avvisi = w93)
''','registrare anche gli avvisi')+r'''
\PBody{Se l’avviso segnala un p-value inferiore al minimo tabulato, il valore va riferito come limite superiore. Il caso oltre il massimo richiede la disuguaglianza opposta.}
''','Un limite tabulato non va presentato come un p-value esatto.')

S(94,'La simulazione del sito ha riferimenti propri',mc_reference()+r'''
\[\widehat p_{\rm ADF}
=\frac{1+\#\{T_b\leq T_{\rm obs}\}}{B+1}.\]
\PSmall{Con $B=200$, il passo minimo è $1/201\approx0{,}005$. Per KPSS si considera la coda superiore.}
''',r'''
\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m09-diagnosi}{Esperimento · diagnosi}
\PBody{L’ADF semplificato include una costante e una differenza ritardata. Il riferimento Monte Carlo usa random walk simulati, con la stessa regressione.}
\vspace{3mm}
\PInfo{La coda Monte Carlo del KPSS usa rumore IID. Non è una calibrazione generale per ogni processo stazionario dipendente.}
\PSmall{I risultati illustrano come si costruisce un riferimento. Le routine \texttt{tseries} usano specificazioni e tabelle proprie.}
''','Il generatore nullo e la statistica devono essere dichiarati insieme quando si costruisce un test per simulazione.')

S(95,'Una discontinuità può cambiare la diagnosi',break_series()+r'''
\[X_t=\mu_1+\varepsilon_t\ (t\leq\tau),
\qquad X_t=\mu_2+\varepsilon_t\ (t>\tau).\]
\PSmall{Schema di un cambiamento di livello. Una modifica dello strumento può produrre un andamento simile.}
''',C(95,'cambio_livello',r'''
set.seed(19095)
x95 <- c(rep(0, 80), rep(2, 80)) + rnorm(160)
plot(x95, type = "l", ylab = "Valore")
abline(v = 80.5, col = "darkorange")
# Consultare i metadati prima dei test.
c(media_prima = mean(x95[1:80]),
  media_dopo = mean(x95[81:160]))
''','simulare un cambio di livello')+r'''
\PInfo{Un test di radice unitaria non risolve da solo la distinzione fra trend, cambi strutturali e problemi di misura. Un campione breve aggiunge incertezza.}
''','Le discontinuità richiedono metadati e ipotesi sul processo che possano spiegarle.')

S(96,'La diagnosi collega più evidenze',evidence()+r'''
\PSmall{La conclusione indica la serie esaminata, le trasformazioni già applicate e le alternative ancora plausibili.}
''',C(96,'resoconto',r'''
resoconto96 <- list(
  serie = "CO2 mensile storica, livelli",
  periodo = range(d$data),
  osservazioni = length(y),
  adf = adf88,
  kpss_livello = kL91,
  kpss_trend = kT91)
resoconto96$periodo
''','conservare le scelte')+r'''
\PBody{Una buona conclusione descrive che cosa sostengono i dati e quali scelte potrebbero modificarla. I risultati numerici restano leggibili insieme ai grafici.}
\PInfo{Questa diagnosi prepara la valutazione temporale del modulo successivo. La capacità predittiva richiederà un controllo su osservazioni future.}
''','La diagnosi scientifica comprende evidenze, assunzioni e limiti della conclusione.')

# Distribuzione del testo fra le due colonne. Le spiegazioni si leggono
# sotto il diagramma, lasciando al codice una colonna libera e leggibile.
def sposta_primo(n,comando):
    s=SLIDES[n]['right']; start=s.index(comando+'{')
    depth=1;end=start+len(comando)+1
    while depth:
        if s[end]=='{':depth+=1
        elif s[end]=='}':depth-=1
        end+=1
    SLIDES[n]['left']+='\n'+s[start:end]
    SLIDES[n]['right']=s[:start]+s[end:]

for n in [57,58,61,63,66,71,73,75,76,77,80,81,83,87,88,93,96]:
    sposta_primo(n,r'\PBody')
sposta_primo(56,r'\PSmall')
sposta_primo(82,r'\PInfo')
for n in [57,61,76]:
    SLIDES[n]['left']=SLIDES[n]['left'].replace(r'\PBody{',r'\PSmall{')

assert set(SLIDES)==set(range(54,97))
