from diagram_helpers import *
SLIDES={};CODES={}
def S(n,title,left,right,recall):
    SLIDES[n]=dict(title=title,section='IV · RITARDI E AUTOCORRELAZIONE',left=left,right=right,recall=recall)
def C(n,name,src,title):
    key=f'{n:03}_{name}.R';CODES[key]=src.strip()+'\n';return rf'\PCode{{R · {title}}}{{{key}}}'
def acf_comparison():
    out,X,Y=axes(0,24,-.4,1.05,'Ritardo (passi)',r'$\widehat\rho(k)$',h=4.4,xticks=[0,6,12,18,24],yticks=[0,.5,1])
    line(out,X,Y,[(0,0),(24,0)],'Rule')
    for col,color in [('rumore_bianco','GeoA'),('ar1','GeoB'),('random_walk','GeoC')]:
        line(out,X,Y,enumerate(acf_values([r[col] for r in PROC]),0),color)
    out.append(r'\node[pNote,fill=Paper] at(5,4.15){Blu: rumore. Rame: AR(1). Viola: random walk.};')
    return finish(out)
def scale_effect():
    out,X,Y=axes(0,12,0,110,'Ritardo $k$',r'$\gamma(k)$',h=4.3,xticks=[0,3,6,9,12],yticks=[0,50,100])
    line(out,X,Y,[(k,.65**k) for k in range(13)],'GeoA')
    line(out,X,Y,[(k,100*.65**k) for k in range(13)],'GeoB')
    out.append(r'\node[pNote,fill=Paper] at(5.2,3.9){Moltiplicare $X$ per 10 moltiplica $\gamma$ per 100};')
    return finish(out)
def bandplot():
    a=[val(r['rumore_bianco']) for r in PROC]
    return acf_chart(a=a,maxlag=24,title=r'ACF del rumore bianco simulato, $n=300$')
def paircount():
    return columns_bars([204,203,192,180],['$k=0$','$k=1$','$k=12$','$k=24$'],ylabel='Coppie disponibili',h=4.1)
def theoretical_pacf():
    out,X,Y=axes(0,12,-.2,1.05,'Ritardo $k$','Valore teorico',h=4.4,xticks=[0,1,4,8,12],yticks=[0,.65,1])
    line(out,X,Y,[(k,.65**k) for k in range(13)],'GeoA')
    for k in range(1,13):
        y=.65 if k==1 else 0
        out.append(rf'\draw[GeoB,line width=1.8pt]({X(k):.4f},{Y(0):.4f})--({X(k):.4f},{Y(y):.4f});\fill[GeoB]({X(k):.4f},{Y(y):.4f})circle(2pt);')
    out.append(r'\node[pNote,fill=Paper] at(5.1,4.15){AR(1), $\phi=0{,}65$: ACF blu, PACF rame};')
    return finish(out)

S(40,'Un ritardo costruisce coppie di osservazioni',
  lag_pairs(1)+r'\[(x_{t-1},x_t),\qquad t=2,\ldots,n.\]',
  C(40,'lag1',r'''
x40 <- proc$ar1
coppie1 <- data.frame(
  passato = head(x40, -1),
  presente = tail(x40, -1))
head(coppie1)
nrow(coppie1)
# 300 valori generano 299 coppie al ritardo 1.
''','allineare passato e presente')+r'\PBody{In una serie regolare, un passo separa ogni coppia. La prima osservazione non ha un precedente nel file.}',
'Il ritardo k specifica quali coppie confrontiamo. Aumentando k diminuisce il numero di coppie disponibili.')

S(41,'Dodici passi collegano lo stesso mese',
  lag_pairs(12)+r'\[(x_{t-12},x_t),\qquad t=13,\ldots,204.\]',
  C(41,'lag12',r'''
n41 <- nrow(d)
coppie12 <- data.frame(
  data = d$data[13:n41],
  passato = head(d$co2_ppm, -12),
  presente = tail(d$co2_ppm, -12))
head(coppie12, 3)
stopifnot(nrow(coppie12) == 192L)
''','allineare due anni')+r'\PInfo{Dodici passi valgono un anno perché la griglia è mensile e completa. In una tabella con mesi eliminati, dodici righe avrebbero un altro significato.}',
'L’unità temporale del ritardo deriva dal calendario, non dal nome attribuito alla colonna.')

S(42,'Il diagramma di ritardo mostra la dipendenza',
  lag_scatter(k=1)+r'\PSmall{AR(1) del file simulato: ciascun punto confronta un valore con il precedente.}',
  C(42,'scatter_lag',r'''
plot(coppie1$passato, coppie1$presente,
     pch = 16, col = "#1D789080",
     xlab = "Valore precedente",
     ylab = "Valore presente")
cor(coppie1$passato, coppie1$presente)
''','disegnare le coppie')+r'\PBody{Una nube orientata segnala una relazione lineare fra i valori. Strutture curve o ampiezze variabili possono richiedere descrizioni ulteriori.}'+r'\vspace{2mm}\PLab{https://marzione00.github.io/Lab_Geo/\#laboratorio/m09-autocorrelazione}{Esperimento · Autocorrelazione}',
'La correlazione fra valori vicini descrive persistenza. Non identifica da sola il meccanismo fisico che la produce.')

S(43,'La correlazione delle coppie e l’ACF',
  covariance_products()+r'\PSmall{Esempio $x=(1,2,3,5,4)$, media complessiva 3. I prodotti usano valori centrati sulla stessa media.}',
  C(43,'cor_vs_acf',r'''
x43 <- c(1, 2, 3, 5, 4)
cor(head(x43, -1), tail(x43, -1))
as.numeric(acf(x43, lag.max = 1,
               plot = FALSE)$acf[2])
# cor() ricentra separatamente le due colonne.
# acf() usa la media dell'intera serie.
''','confrontare due definizioni')+r'\PInfo{I due numeri possono differire nei campioni finiti. Prima di confrontare risultati bisogna conoscere centratura e normalizzazione.}',
'cor(head(x), tail(x)) e acf(x) non sono, in generale, lo stesso stimatore.')

S(44,'Lo stimatore usato da acf in R',
  r'''\[\widehat\rho(k)=
\frac{\sum_{t=k+1}^{n}(x_t-\bar x)(x_{t-k}-\bar x)}
     {\sum_{t=1}^{n}(x_t-\bar x)^2}.\]
\PSmall{Serie completa, demeaning predefinito. A ritardo zero il rapporto vale uno.}'''+covariance_products(),
  C(44,'acf_manuale',r'''
xc44 <- x43 - mean(x43)
rho44 <- sum(head(xc44, -1) *
               tail(xc44, -1)) / sum(xc44^2)
rho_R <- as.numeric(acf(x43, plot = FALSE)$acf[2])
stopifnot(abs(rho44 - rho_R) < 1e-12)
rho44 # 0.4
''','ricostruire il calcolo')+r'\PInfo{Nell’esempio il numeratore vale 4 e il denominatore 10. Il denominatore usa tutti i valori centrati, anche ai ritardi maggiori.}',
'La definizione dello stimatore spiega differenze numeriche che non sono errori di calcolo.')

S(45,'L’autocovarianza ha un ritardo',
  lag_scatter(k=4)+r'\PSmall{Le stesse osservazioni del simulatore, qui separate da quattro passi.}',
  r'''\[\gamma(k)=\operatorname{Cov}(X_t,X_{t-k}).\]
\[\rho(k)=\frac{\gamma(k)}{\gamma(0)}.\]
\PBody{Per un processo debolmente stazionario, $\gamma(k)$ dipende dal ritardo e la varianza $\gamma(0)$ è costante e finita. Supponiamo $\gamma(0)>0$.}
\vspace{3mm}
\PInfo{L’autocovarianza conserva l’unità al quadrato. L’autocorrelazione è adimensionale e vale uno per $k=0$.}
\vspace{2mm}
\PSmall{Le condizioni di stazionarietà saranno sviluppate nella sezione successiva.}''',
'Per interpretare l’ACF come una proprietà stabile del processo occorre esplicitare le ipotesi sulla serie.')

S(46,'Cambiare unità non cambia l’autocorrelazione',
  scale_effect()+r'\[\gamma_{aX}(k)=a^2\gamma_X(k),\qquad \rho_{aX+b}(k)=\rho_X(k)\ (a\ne0).\]',
  C(46,'scala_acf',r'''
a46 <- as.numeric(acf(proc$ar1,
  lag.max = 24, plot = FALSE)$acf)
b46 <- as.numeric(acf(10*proc$ar1 + 5,
  lag.max = 24, plot = FALSE)$acf)
stopifnot(max(abs(a46 - b46)) < 1e-12)
''','verificare l’invarianza')+r'\PBody{Una trasformazione affine cambia livello e scala, ma conserva la struttura lineare relativa fra i ritardi. Questo non vale per trasformazioni arbitrarie.}',
'L’ACF permette di confrontare dipendenze lineari senza incorporare l’unità di misura.')

S(47,'L’ACF raccoglie molti ritardi',
  acf_chart(a=[val(r['ar1']) for r in PROC],title='AR(1) simulato: stime fino al ritardo 24'),
  C(47,'leggere_acf',r'''
acf(proc$ar1, lag.max = 24,
    main = "AR(1): ritardi in passi")
acf(y, lag.max = 24,
    main = "CO2: ritardi espressi in anni")
# Per y mensile, il ritardo 1 del grafico
# corrisponde a 12 osservazioni.
''','leggere l’asse dei ritardi')+r'\PInfo{Su un oggetto ts, R esprime l’asse in unità di tempo. Su un vettore numerico, lo esprime in passi. Le figure didattiche indicano qui i passi.}',
'Prima di leggere un picco dell’ACF bisogna controllare l’unità dell’asse orizzontale.')

S(48,'Le bande usuali hanno un riferimento preciso',
  bandplot(),
  r'''\[\widehat\rho(k)\ \approx\ \mathcal N(0,1/n),\qquad
\pm\frac{1{,}96}{\sqrt n}.\]
\PSmall{Approssimazione per ritardi fissati, con riferimento a rumore IID (per esempio gaussiano), momenti appropriati e campioni grandi.}
\vspace{3mm}
\PBody{Per $n=300$, la semilarghezza è circa $0{,}113$. Un valore oltre la banda richiede attenzione rispetto a questo riferimento.}
\vspace{3mm}
\PInfo{Le bande puntuali non sono un intervallo di confidenza simultaneo per tutta l’ACF. Con dipendenza generale, la variabilità delle stime può cambiare.}''',
'La banda dell’ACF si interpreta insieme al modello di riferimento e al numero di ritardi esaminati.')

S(49,'Molti ritardi generano molti confronti',
  bandplot()+r'\PSmall{Stessa realizzazione della slide precedente. La lettura riguarda la forma complessiva e i singoli valori.}',
  C(49,'bande',r'''
a49 <- as.numeric(acf(proc$rumore_bianco,
  lag.max = 24, plot = FALSE)$acf)[-1]
banda49 <- 1.96 / sqrt(nrow(proc))
which(abs(a49) > banda49)
# Confronti puntuali, fra loro dipendenti.
''','individuare i ritardi oltre banda')+r'\PBody{Con 24 confronti puntuali al 5\%, il numero atteso di superamenti è circa $24\cdot0{,}05=1{,}2$ sotto l’approssimazione.}'+r'\vspace{2mm}\PInfo{Questa aspettativa non dà la probabilità di almeno un superamento. Le stime ai diversi ritardi non sono indipendenti.}',
'Un superamento isolato può verificarsi per variabilità campionaria. Sequenze e pattern richiedono una lettura congiunta.')

S(50,'Assenze e ritardi non si separano',
  paircount()+r'\PSmall{Numero di coppie in una serie completa di 204 mesi. Con assenze, il numero può dipendere anche dalla loro posizione.}',
  C(50,'na_acf',r'''
# Controllo prima di calcolare l'ACF.
stopifnot(!anyNA(y))
# Esempio: un mese rimane NA.
y50 <- y
y50[30] <- NA
sum(complete.cases(head(y50, -1),
                   tail(y50, -1)))
''','contare le coppie osservate')+r'\PInfo{Eliminare gli NA dal vettore e ricreare ts comprimerebbe il calendario. acf(..., na.action = na.pass) usa coppie complete, ma la sequenza risultante può non essere un’ACF valida.}',
'Gestire le assenze richiede una scelta metodologica. Eliminare posizioni cambia il significato dei ritardi.')

S(51,'La PACF rimuove i ritardi intermedi',
  pacf_chain()+r'\[\operatorname{PACF}(2)=\operatorname{Corr}(e_{t},e_{t-2}),\]',
  r'''\PBody{A ritardo 2 si regrediscono separatamente $X_t$ e $X_{t-2}$ sul valore intermedio $X_{t-1}$. Si confrontano poi i due residui.}
\vspace{3mm}
\PSmall{Nella formula a sinistra $e_t$ ed $e_{t-2}$ indicano questi residui di proiezione lineare.}
\vspace{3mm}'''+
  C(51,'pacf',r'''
pacf(proc$ar1, lag.max = 24,
     main = "Autocorrelazione parziale")
# R stima modelli autoregressivi
# di ordine via via maggiore.
''','calcolare la PACF')+r'\PInfo{La PACF considera la dipendenza lineare residua. Il suo significato richiede le stesse cautele dell’ACF.}',
'Una relazione fra tempi distanti può essere spiegata dai valori intermedi. La PACF studia ciò che rimane.')

S(52,'ACF e PACF rispondono a domande diverse',
  theoretical_pacf(),
  C(52,'acf_pacf_teoria',r'''
# Valori teorici per AR(1), phi = 0.65.
ARMAacf(ar = 0.65, lag.max = 12)
ARMAacf(ar = 0.65, lag.max = 12, pacf = TRUE)
''','confrontare le funzioni teoriche')+r'\PBody{Nell’AR(1) stazionario la relazione con il passato passa attraverso il valore immediatamente precedente. L’ACF decade, mentre la PACF teorica si annulla dopo il primo ritardo.}'+r'\vspace{3mm}\PInfo{Nei campioni finiti le stime oscillano attorno ai valori teorici. Un taglio netto non deve comparire esattamente.}',
'Il confronto con forme teoriche orienta un modello. Non trasforma una somiglianza grafica in una dimostrazione.')

S(53,'Tre forme di memoria da spiegare',
  acf_comparison(),
  C(53,'tre_acf',r'''
for (nome in c("rumore_bianco", "ar1",
               "random_walk")) {
  acf(proc[[nome]], lag.max = 24, main = nome)
}
''','confrontare i tre archivi')+r'\PBody{Il rumore oscilla attorno a zero. L’AR(1) mostra memoria che tende ad attenuarsi. Nel random walk l’ACF campionaria resta elevata a più ritardi.}'+r'\vspace{3mm}\PInfo{Il random walk non ha una varianza costante. La sua ACF campionaria è descrittiva e non è una funzione teorica stazionaria.}',
'La forma dell’ACF va interpretata insieme alla natura del processo e alla stabilità delle sue proprietà.')


# Spiegazioni accanto alla figura o alla formula corrispondente.
for n,p in [(49,r'\PBody{Con 24 confronti puntuali al 5\%, il numero atteso di superamenti è circa $24\cdot0{,}05=1{,}2$ sotto l’approssimazione.}'),(51,r'\PSmall{Nella formula a sinistra $e_t$ ed $e_{t-2}$ indicano questi residui di proiezione lineare.}'),(52,r'\PBody{Nell’AR(1) stazionario la relazione con il passato passa attraverso il valore immediatamente precedente. L’ACF decade, mentre la PACF teorica si annulla dopo il primo ritardo.}')]:
    assert p in SLIDES[n]['right']
    SLIDES[n]['right']=SLIDES[n]['right'].replace(p,'')
    SLIDES[n]['left']+=p
