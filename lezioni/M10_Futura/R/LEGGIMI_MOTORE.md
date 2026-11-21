# Motore scientifico di M10 Futura

## Avvio e riproduzione

Aprire il progetto del modulo in RStudio, oppure impostare come directory corrente la cartella che contiene `setup.R`. Il motore usa soltanto pacchetti standard distribuiti con R: base, stats, graphics, grDevices e utils. Non scarica dati, non installa pacchetti e non richiede `forecast`, `vars` o `jsonlite`.

```r
source("Lezione_Futura.R", encoding="UTF-8")
# Rigenera CSV, modelli RDS, figure PDF e controlli numerici:
source("R/rigenera_calcoli.R", encoding="UTF-8")
```

Da terminale, in una normale installazione R:

```sh
Rscript R/rigenera_calcoli.R
```

L'edizione consegnata è stata realmente eseguita con R 4.6.0 attraverso WebR 0.6.1. La mancanza di R nativo nell'ambiente di produzione è stata risolta usando lo stesso interprete R compilato in WebAssembly: nessun risultato statistico è stato simulato fuori da R. `Verifiche/SESSIONE_R.txt` registra l'ambiente effettivo. I file del modulo sono normali sorgenti R e non dipendono da WebR per l'uso locale. Fra versioni di R, piattaforme e ottimizzatori sono possibili differenze negli ultimi decimali; interpretazioni e cifre presentate sono arrotondate coerentemente.

## File e oggetti

- `setup.R`: verifica e carica i tre dataset; crea `co2`, `y`, `train`, `test`, `fossili`, `processi`.
- `R/funzioni_M10.R`: funzioni pure per metriche, baseline, SARIMA, validazione per origine, VAR(1), previsione AR(1) teorica.
- `R/stato_lezione.R`: prepara gli oggetti per i frammenti delle slide senza produrre file. Oltre ai precedenti crea `d`, `h`, `fit`, `fc`, `b`, `res`, `cv`, `fossilitrain`, `fossilitest`, `fossilifit`, `v`, `varfit`, `varpred`.
- `R/rigenera_calcoli.R`: stima, confronto, simulazioni, esportazione dei risultati e verifiche.
- `R/genera_figure.R`: costruisce i grafici dai risultati effettivi; va richiamato dal motore completo, che prepara gli oggetti necessari.
- `Calcoli/riassunto.json`: risultati principali a piena precisione.
- `Calcoli/INDICE_FIGURE.csv`: elenco dei PDF effettivamente prodotti.
- `Risultati/modello_*.rds`: oggetti modello stimati e salvati da R.

### Contratto minimo delle funzioni

`metriche(osservato, previsto)` restituisce un vettore con `MAE`, `RMSE`, `bias`. L'errore è sempre **osservato meno previsto**: un bias negativo indica sovrastima media.

`baseline(train, h, periodo=12)` restituisce la media del train, l'ultimo valore, la ripetizione dell'ultimo ciclo stagionale e la retta di deriva fra il primo e l'ultimo valore del train. La deriva della baseline non è un parametro aggiunto al SARIMA.

`stima_sarima(y, order, seasonal, periodo)` chiama `stats::arima` con massima verosimiglianza e controlla il codice di convergenza. `previsione_sarima(fit,h)` restituisce `h`, `previsto`, `se`, `inferiore`, `superiore`.

`valida_origini(train, origini, h)` ristima il modello soltanto sulla storia disponibile a ciascuna origine. Le colonne sono `origine`, `h`, `osservato`, `SARIMA`, `Stagionale`, `Deriva`, `Ultimo`, `inferiore`, `superiore`.

`stima_VAR1(xy)` accetta un data.frame o una matrice con due colonne numeriche in ordine X,Y. Restituisce la matrice dei coefficienti `A` per righe di equazione, il vettore delle intercette `c`, `autovalori`, `stabile`, le due regressioni `x` e `y`, e i `dati_ritardati`. `previsione_VAR1` itera `c + A %*% stato` senza leggere osservazioni future.

`ar1_teoria(phi,sigma,x0,mu,h)` usa parametri noti, innovazioni indipendenti gaussiane e `abs(phi)<1`. Restituisce media, varianza e intervallo predittivo condizionale, con varianza `sigma^2 * (1-phi^(2*h))/(1-phi^2)`.

## Protocollo CO2

La serie è un archivio storico derivato: 204 medie mensili locali da gennaio 1985 a dicembre 2001. Le osservazioni settimanali appartengono al mese della propria data; `n_settimane` conta i valori settimanali non mancanti impiegati nella media. La colonna viene conservata come metadato, senza pesare il SARIMA. La provenienza risale al dataset storico CO2 distribuito con statsmodels, attribuito a Keeling, Whorf e CDIAC; non si presenta la derivazione locale come una serie mensile ufficiale NOAA contemporanea. I CSV sono copie identiche a quelli di M09/M07, con SHA256 in `Dati/PROVENIENZA.json`.

Il train contiene 168 mesi, gennaio 1985–dicembre 1998. Il test contiene 36 mesi, gennaio 1999–dicembre 2001. La previsione finale ha un'unica origine, dicembre 1998: per ogni orizzonte si usa la stessa storia congelata. È un esperimento retrospettivo e non una previsione attuale della concentrazione atmosferica.

Il modello fissato è `SARIMA(0,1,1)(0,1,1)[12]`, stimato con `method="ML"`, senza termine di deriva. In R, `include.mean=FALSE` è esplicito; con differenziazione il parametro `include.mean` non introduce comunque una deriva. La convenzione MA di R ha segno positivo nel polinomio delle innovazioni. I coefficienti stimati sono ma1=−0.328847912 e sma1=−0.889699102.

Le tre origini di validazione del protocollo sono 120,132,144, ciascuna con 12 mesi di valutazione. Non sono holdout alternativi del test 1999–2001. L'approfondimento con 37 origini mensili, da120 a156, resta interamente nel train; produce errori a ciascun orizzonte da1 a12. Le finestre sovrapposte generano errori dipendenti: non vengono trattate come repliche indipendenti.

Il confronto AIC usa tre specifiche con le stesse differenze d=1,D=1 e la stessa finestra. Ha una funzione didattica e non risceglie il modello dopo aver visto il test. AIC e RMSE test rispondono a domande differenti.

### Risultati verificati

| Modello | MAE test, ppm | RMSE test, ppm | Bias, ppm |
|---|---:|---:|---:|
| Media train |13.639891|13.80764|13.639891|
| Ultimo valore |2.839306|3.336407|2.554861|
| Stagionale |2.865694|3.108832|2.865694|
| Deriva |1.884206|2.148267|0.117735|
| SARIMA |0.974469|1.062193|−0.968499|

Il SARIMA ha il RMSE minore fra i confronti fissati. Il bias negativo indica che la previsione tende a essere più alta dell'osservato: un buon RMSE relativo non elimina un errore sistematico.

Gli intervalli nominali 95% sono `previsione ± qnorm(.975)*se`, con `se` restituito da `predict.Arima`. Sono condizionati al modello e ai parametri stimati; **non includono l'incertezza della stima dei parametri** e non sono bande simultanee sull'intera traiettoria. Tutti 36 valori osservati del test rientrano negli intervalli. Questo 36/36 è una descrizione di una traiettoria storica dipendente, non la dimostrazione di una copertura futura del 100% o della calibrazione al95%.

I residui diagnostici sono le innovazioni stimate agli indici 14:168,155 valori. L'esclusione iniziale segue il protocollo del corso e riduce l'effetto dell'inizializzazione con differenziazione. Il test di Ljung–Box usa lag 24 e fitdf2: Q=14.241537, gradi di libertà 22, p=0.892685. Il mancato rifiuto non dimostra indipendenza, gaussianità, corretta specificazione o buona previsione futura. La diagnostica del train e la valutazione del test rimangono distinte.

## Teoria e simulazioni

Le simulazioni supplementari hanno semi fissi:101001 per quattro AR(1),101002 per MA(1)/ARMA(1,1),101003 per il Monte Carlo. Gli AR(1) usano phi=0.20,0.65,0.95,−0.60 e un avviamento di500 passi. La teoria ACF è `phi^k`. Per MA(1) con theta=0.60, `rho(1)=theta/(1+theta^2)` e le autocorrelazioni sono nulle per k>1. Le risposte a impulso sono coefficienti teorici, non stime da un particolare campione.

Il Monte Carlo genera 2000 traiettorie AR(1) indipendenti, ciascuna lunga 30 passi, da x0=2 con phi=0.65 e sigma=1 noti. Si confrontano media, varianza e copertura marginale a ciascun orizzonte con le formule chiuse. Le linee intorno a0.95 sono un riferimento binomiale approssimato **puntuale**, non una banda simultanea sui 30 orizzonti. L'indipendenza è fra traiettorie; all'interno di ogni traiettoria gli orizzonti restano correlati.

## Progetto fossili

I160 individui sono simulati. Si riserva al test ogni quinta riga:128 train e32 test. La regressione `diametro_int_um ~ diametro_tot_um` viene stimata soltanto nel train e confrontata con la media della risposta del train. Intercetta=−0.721102214, pendenza=0.959999270. Il RMSE test passa da1.002912947 della media a0.228252161 micrometri della retta.

Le due misure sono geometricamente legate: diametro interno = diametro totale −2×spessore, entro arrotondamenti inferiori a2×10^−8 micrometri. La relazione predittiva non prova un meccanismo geologico, una causalità fisica o trasferibilità ad altri campioni. Lo split deterministico serve a replicare il progetto didattico; su dati reali andrebbe valutata l'eventuale struttura per sito, campione o individuo.

## Approfondimento VAR e Granger

Si usano le prime 250 righe di `x_VAR`,`y_VAR`, che producono 249 coppie ritardate. Il VAR(1) è stimato mediante due regressioni OLS con intercetta e i due ritardi. Il raggio spettrale di A è0.513872652<1: il sistema stimato risulta stabile.

Dal passo 250 si prevedono ricorsivamente i passi 251–260, reinserendo ogni previsione nella ricorsione. Non si aggiornano gli stati con i valori veri del test. RMSE di X=1.056526339 contro 1.668068436 dell'ultimo valore; RMSE di Y=1.192539671 contro 2.560779923.

I confronti di Granger sono test F fra modelli annidati, con 246 gradi di libertà residui; sono corretti con Holm sui due confronti dichiarati. X→Y: F=85.1974843, p=1.2890109×10^−17, pHolm=2.5780218×10^−17. Y→X: F=0.0570029, p=pHolm=0.8114961. L'evidenza riguarda utilità predittiva condizionata a queste variabili, questo ritardo e queste ipotesi; non stabilisce causalità fisica e non controlla variabili omesse.

## Verifiche e limiti dell'audit

Il motore esegue 12 verifiche R: caso noto delle metriche, media e varianza AR(1), equivalenza della somma geometrica, baseline stagionale, origini interne, ricorsione VAR, date previste, identità geometrica dei fossili, e tre prove effettive di separazione train/test. Per queste ultime si aggiunge 1000×h a tutti 36 valori del test, si ricostruisce il train per calendario e si verificano identità di train, baseline e previsioni SARIMA.

Un ricalcolo indipendente NumPy/SciPy verifica metriche CO2, OLS fossili, coefficienti e ricorsione VAR, autovalori e test F di Granger; controlla anche gli hash dei dati. Gli scarti numerici sono inferiori alle tolleranze dichiarate in `Verifiche/controlli_indipendenti_python.json`. Questo controllo non costituisce una seconda implementazione indipendente della massima verosimiglianza SARIMA.

I36 grafici principali e9 dettagli separati sono PDF vettoriali originali prodotti da R. Non impiegano immagini generative. Palette e fondo seguono il corso. I pannelli di dettaglio permettono di mantenere leggibili i grafici multipli in una colonna delle slide; le figure complete restano utili per il confronto e la stampa. Render e verifica visiva sono documentati nell'audit di consegna.

## Fonti primarie

- R `arima`: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.html
- R `predict.Arima`: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.arima.html
- R `Box.test`: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/box.test.html
- R `ARMAacf`: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/ARMAacf.html
- R `arima.sim`: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.sim.html
- R `p.adjust`: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html
- Sorgenti del corso, commit 649f7cc577b96bd1044d81e78a2f530813e4f96b: https://github.com/marzione00/Lab_Geo/tree/649f7cc577b96bd1044d81e78a2f530813e4f96b

I dati e le convenzioni del protocollo derivano dai materiali del corso. Le proprietà degli stimatori e dei comandi sono documentate nelle pagine ufficiali di R. Le conclusioni numeriche derivano dagli script eseguiti in questa edizione.
