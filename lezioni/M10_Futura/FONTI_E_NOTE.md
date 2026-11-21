# M10 Futura — Fonti, dati e note di metodo

Edizione verificata il **20 novembre 2026**. Questo documento collega il programma del corso, le fonti teoriche e i risultati eseguibili del pacchetto. Le scelte statistiche sono distinte dalle aggiunte didattiche e dalle prove di riproducibilità.

## 1. Fonte del programma e continuità con il corso

Il riferimento editoriale è [GeoStat Lab, modulo M10](https://marzione00.github.io/Lab_Geo/percorso/M10.html), successivo a M09 Borealis. Le 20 attività conservano gli identificativi `M10_N01`–`M10_N20`. La CO2 guida la lezione sulla previsione; la morfometria è il progetto base dei laboratori N10–N13; il VAR costituisce l'approfondimento facoltativo.

Il programma e gli script pubblicati sono stati consultati nella revisione Git:

`649f7cc577b96bd1044d81e78a2f530813e4f96b`

La [revisione del repository](https://github.com/marzione00/Lab_Geo/tree/649f7cc577b96bd1044d81e78a2f530813e4f96b) identifica lo stato usato per questa edizione. Il controllo dei 26 file acquisiti dal sito è registrato in `Verifiche/PROVENIENZA_GIT_SITO.json`: URL di origine, identificatore del blob, SHA-256 e risultato del confronto. Gli script locali sviluppano il percorso, mantenendo il protocollo centrale e aggiungendo spiegazioni, verifiche e figure dai calcoli effettivi.

## 2. Fonti teoriche e documentazione primaria

### Forecasting: Principles and Practice, terza edizione

Rob J. Hyndman e George Athanasopoulos, [*Forecasting: Principles and Practice*](https://otexts.com/fpp3/), OTexts, edizione online degli autori. Le sezioni pertinenti sono:

| Capitolo | Argomenti usati nel modulo | Collegamento |
|---|---|---|
|5, The forecaster's toolbox|Riferimenti semplici, residui, intervalli, MAE/RMSE e validazione a origini successive|[Capitolo 5](https://otexts.com/fpp3/toolbox.html)|
|9, ARIMA models|Stazionarietà, differenze, AR/MA/ARIMA, criteri informativi e stagionalità|[Capitolo 9](https://otexts.com/fpp3/arima.html)|
|12.3, Vector autoregressions|Struttura multivariata e previsione VAR|[Capitolo 12](https://otexts.com/fpp3/advanced.html)|

Nella versione consultata, alcuni vecchi indirizzi delle singole sezioni reindirizzano ai capitoli riuniti. Sono quindi forniti i collegamenti correnti ai capitoli. Il libro impiega anche il sistema `fable`; il codice di questo pacchetto usa invece le funzioni standard di R indicate sotto. Nomi dei parametri e dettagli della stima vengono verificati nella documentazione del software effettivamente eseguito.

### R Core Team: documentazione delle funzioni effettive

| Funzione | Aspetto verificato | Fonte ufficiale |
|---|---|---|
|`stats::arima`|Ordini, periodo, convenzione MA, media, massima verosimiglianza, convergenza|[arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.html)|
|`predict.Arima`|Previsione da storia finita e significato dell'errore standard restituito|[predict.Arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.arima.html)|
|`stats::Box.test`|Statistica Ljung–Box, ritardo massimo e gradi di libertà sottratti|[Box.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/box.test.html)|
|`stats::ARMAacf`|ACF e PACF teoriche|[ARMAacf](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/ARMAacf.html)|
|`stats::ARMAtoMA`|Coefficienti della rappresentazione a innovazioni e risposta a impulso|[ARMAtoMA](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/ARMAtoMA.html)|
|`stats::arima.sim`|Simulazione e periodo di avviamento|[arima.sim](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.sim.html)|
|`stats::lm`|Regressione sui fossili e due equazioni del VAR|[lm](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/lm.html)|
|`stats::anova.lm`|Confronti fra modelli annidati sulle stesse osservazioni|[anova.lm](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/anova.lm.html)|
|`stats::p.adjust`|Correzione di Holm per i due confronti di Granger|[p.adjust](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html)|
|`base::eigen`|Autovalori della matrice dinamica stimata|[eigen](https://stat.ethz.ch/R-manual/R-devel/library/base/html/eigen.html)|

Le pagine R-devel sono documentazione aggiornata. La versione realmente usata per i risultati consegnati è registrata separatamente in `Verifiche/SESSIONE_R.txt`; il collegamento a una pagina aggiornata non sostituisce tale registrazione.

## 3. Provenienza dei tre dataset

I tre CSV sono copiati senza modifiche dagli archivi dei moduli precedenti. Il metadato completo è `Dati/PROVENIENZA.json`. Gli hash sono verificati nuovamente dall'audit indipendente.

| File | Natura e dimensione | Provenienza nel pacchetto M01–M09 |
|---|---|---|
|`co2_1985_2001.csv`|204 medie mensili storiche, gennaio 1985–dicembre 2001; ppm|`M09_Borealis/Dati`|
|`fossili_simulati.csv`|160 individui simulati; misure morfometriche in micrometri|`M07_Annula/Dati`|
|`processi_simulati.csv`|300 passi di processi sintetici del corso; in M10 si usano X e Y del VAR|`M09_Borealis/Dati`|

### CO2: archivio settimanale e derivazione mensile

La fonte storica è la serie settimanale di Mauna Loa distribuita con statsmodels, relativa al periodo marzo 1958–dicembre 2001. La [scheda ufficiale del dataset](https://www.statsmodels.org/stable/datasets/generated/co2.html) descrive origine, misura e periodo di registrazione. La documentazione di M09 attribuisce l'archivio a Keeling, Whorf e CDIAC.

Il corso assegna ogni osservazione settimanale al mese della propria data e calcola la media dei valori non mancanti di quel mese. Nel CSV locale:

- `data` è il primo giorno del mese associato alla media;
- `co2_ppm` è la media mensile derivata, in ppm;
- `n_settimane` è il numero di osservazioni settimanali non mancanti che vi contribuiscono.

Il conteggio delle settimane rimane un metadato di copertura; il modello non lo usa come peso né come covariata. Questa derivazione locale non viene presentata come una serie mensile ufficiale NOAA moderna. L'esperimento è storico: non produce una previsione della concentrazione atmosferica odierna.

### Fossili e processi temporali

I fossili e i processi sono simulazioni didattiche. Non sono osservazioni raccolte sul campo. Nei fossili, diametro interno, diametro totale e spessore rispettano un'identità geometrica entro l'arrotondamento del CSV. Questa struttura deve accompagnare l'interpretazione della buona prestazione della retta.

Il file dei processi contiene 300 passi. Per il caso VAR si usano i passi 1–250 per la stima e 251–260 per la verifica a 10 passi. I passi 261–300 non partecipano a tale confronto.

### Impronte dei file consegnati

| File | SHA-256 |
|---|---|
| `co2_1985_2001.csv` | `4e7ebf59451d56ab51f021eaa6e3c7cc4d7e9095cffa83cca45143dcefd83e3a` |
| `processi_simulati.csv` | `eed3c48a3c73a503e4c52963ac21646b30eec986e1701564814826c32f649be3` |
| `fossili_simulati.csv` | `5ec23e7dc8a743f9ee809c66fffba72fef5189dd67c87bbe43b664d4112a0c3a` |

## 4. Protocollo che genera gli output

### CO2: stima e verifica finale

| Elemento | Scelta fissata |
|---|---|
|Addestramento|168 mesi, gennaio 1985–dicembre 1998|
|Origine finale|Dicembre 1998|
|Test|36 mesi, gennaio 1999–dicembre 2001|
|Specificazione|SARIMA(0,1,1)(0,1,1)[12]|
|Stima|`stats::arima`, `method="ML"`, `include.mean=FALSE`, nessun regressore di deriva|
|Riferimenti|Media del train, ultimo valore, ultimo ciclo stagionale ripetuto, deriva fra primo e ultimo valore|
|Errori|Osservato meno previsto; MAE, RMSE e bias in ppm|
|Residui diagnostici|Indici 14–168: 155 innovazioni stimate finite|
|Ljung–Box|24 ritardi, `fitdf=2`, riferimento con 22 gradi di libertà|

La chiamata passa i livelli al SARIMA: le differenze sono gestite nella specificazione, senza applicarle una seconda volta prima della stima. La convenzione di R ha segno positivo nel polinomio MA. Nei modelli differenziati `include.mean` non introduce una deriva; questo comportamento è esplicitato nella [documentazione di arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.html).

L'esclusione dei primi 13 residui segue il protocollo del sito e non viene proposta come una regola per qualsiasi ARIMA. L'assenza di evidenza nel test di autocorrelazione non dimostra indipendenza, normalità o correttezza generale del modello.

### Tre origini del sito e 37 origini di approfondimento

Il protocollo centrale ristima il modello alle origini 120, 132 e 144, cioè dicembre 1994, 1995 e 1996. Ogni origine prevede i 12 mesi successivi, rispettivamente 1995, 1996 e 1997. Si ottengono 36 coppie origine–orizzonte, interamente nel periodo di addestramento.

L'approfondimento aggiunto per le slide usa le origini mensili da 120 a 156 incluse: 37 origini e 444 coppie, sempre con orizzonte 1–12. L'ultima osservazione valutata è il mese 168. Questo ampliamento non sostituisce le tre origini del sito e non utilizza il test 1999–2001. Le finestre sovrapposte producono errori dipendenti; le 444 righe non vengono trattate come repliche statisticamente indipendenti.

Il confronto AIC aggiunto considera solo tre specificazioni, tutte sul medesimo train e con `d=D=1`. Il modello centrale rimane quello prefissato. Per AIC/BIC la varianza rientra nel conteggio dei parametri; la verosimiglianza di questo fit usa un campione efficace di 155 osservazioni. Nel grafico dei candidati, le altezze sono differenze rispetto all'AIC minimo e le etichette sono AIC assoluti.

### Fossili: progetto base

Si riserva al test ogni quinta riga: 128 individui per la stima e 32 per la verifica. La retta `diametro_int_um ~ diametro_tot_um` è confrontata con la media del diametro interno nel train. Le metriche sono calcolate sulle stesse 32 righe. Il modello usa solo il diametro totale; il legame geometrico con lo spessore delimita il risultato. Lo split deterministico rende replicabile l'esercizio e non dimostra trasferibilità a nuovi siti o popolazioni.

### VAR e confronto di Granger

Il VAR(1) usa le prime 250 coppie X,Y e genera 249 righe con ritardo. Le due equazioni OLS condividono la stessa matrice dei regressori. La stabilità è controllata sugli autovalori della matrice A, che devono avere modulo inferiore a uno; le radici del polinomio AR usano la convenzione reciproca.

La previsione parte dal passo 250 e reinserisce ricorsivamente i propri valori per 10 passi. I dati futuri non aggiornano lo stato. Il confronto include il riferimento all'ultimo valore per ciascuna variabile.

I due test di Granger confrontano modelli annidati sulle medesime righe; i due valori p ricevono correzione di Holm. I confronti richiedono le ipotesi dei test F e descrivono utilità predittiva condizionata alle variabili e ai ritardi scelti. Non stabiliscono causalità fisica. La necessità di confrontare regressioni sullo stesso dataset è richiamata da [anova.lm](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/anova.lm.html); la correzione è documentata in [p.adjust](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html).

## 5. Intervalli e limiti dell'inferenza

Gli intervalli del SARIMA sono puntuali al 95%: centro previsto più o meno `qnorm(.975)` volte l'errore standard restituito da `predict`. Secondo la [documentazione di predict.Arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.arima.html), tali errori standard non propagano l'incertezza di stima dei parametri ARMA e dei coefficienti di regressione. Neppure l'incertezza nella scelta della famiglia o cambiamenti strutturali futuri vengono aggiunti automaticamente.

Tutti i 36 valori osservati del test storico rientrano negli intervalli. Questo è un conteggio descrittivo di una sola traiettoria dipendente: non dimostra calibrazione al 95% e non fornisce una probabilità del 95% per l'inclusione simultanea di tutti i valori futuri. Copertura e ampiezza vengono quindi discusse insieme al comportamento del centro e alla sovrastima media osservata.

La simulazione di controllo usa 2.000 traiettorie AR(1) indipendenti con parametri noti, da uno stato iniziale comune. Confronta media, varianza e copertura per orizzonte con le formule teoriche. L'indipendenza riguarda le traiettorie; i 30 orizzonti di una stessa traiettoria restano dipendenti. Le linee di riferimento Monte Carlo sono puntuali, non simultanee. Questa verifica non certifica il SARIMA sul sistema atmosferico reale.

## 6. Figure, dati di supporto e originalità dei grafici

Il motore genera **36 PDF principali e 9 PDF di dettaglio**, tutti vettoriali, a partire da dati numerici o formule dichiarate. Le 110 pagine della presentazione richiamano 33 dei 36 principali. Restano disponibili come supplemento:

- `05_metriche_CO2.pdf`;
- `30_VAR_serie.pdf`;
- `34_VAR_RMSE.pdf`.

I nove dettagli separano i pannelli delle simulazioni AR(1), delle differenze CO2 e delle previsioni VAR. Le figure complete 14, 21 e 32 sono organizzate per la visualizzazione a larghezza intera. L'indice esatto è `Calcoli/INDICE_FIGURE.csv`; le sorgenti sono `R/genera_figure.R` e `R/rigenera_calcoli.R`. Nessun grafico quantitativo è un'immagine generativa. Il tema della copertina e il relativo modello 3D sono documentati separatamente.

Le tabelle numeriche derivano dagli stessi oggetti R delle figure. I CSV conservano la precisione del calcolo; l'arrotondamento avviene nella presentazione. `Calcoli/riassunto.json` raccoglie i valori principali per l'impaginazione automatica. `R/LEGGIMI_MOTORE.md` descrive funzioni, oggetti e risultati in maggior dettaglio.

## 7. Ambiente eseguito e verifiche conservate

I calcoli sono stati realmente eseguiti in **R 4.6.0 (2026-04-24)** mediante **WebR 0.6.1**, piattaforma `wasm32-unknown-emscripten`. R nativo non era disponibile nell'ambiente di produzione; WebR ha eseguito gli stessi sorgenti R usando dati locali. Il [progetto WebR](https://docs.r-wasm.org/webr/latest/) documenta questo ambiente. Il pacchetto consegna normali file R: per l'uso locale non richiede WebR.

Il motore usa solo i pacchetti standard base, stats, graphics, grDevices e utils. Non scarica dati e non installa pacchetti durante l'analisi. Si avvia dalla radice del progetto con:

```r
source("R/rigenera_calcoli.R", encoding="UTF-8")
```

`Lezione_Futura.R` e `R/stato_lezione.R` preparano invece gli oggetti didattici senza rigenerare tutti gli output.

| Evidenza | File o cartella |
|---|---|
|Versione e ambiente effettivi|`Verifiche/SESSIONE_R.txt`|
|12 controlli R, inclusa perturbazione del test|`Verifiche/test_numerici.csv`|
|14 confronti indipendenti NumPy/SciPy e hash|`Verifiche/controlli_indipendenti_python.json`|
|48 frammenti delle slide eseguiti in sequenza|`Verifiche/frammenti_slide.csv` e relativo log|
|Verifica dei 45 PDF scientifici|`Verifiche/audit_figure_pdf.json`|
|Revisione di formule e interpretazioni delle slide|`Verifiche/AUDIT_SCIENTIFICO_SLIDE.md`|

L'audit Python ricalcola metriche, OLS, ricorsioni VAR, autovalori e confronti F; non è una seconda stima indipendente del SARIMA. I 12 controlli R includono un caso con tutti i valori del test alterati, verificando che train, riferimenti e previsioni emesse all'origine restino identici. Questi controlli riguardano rischi di implementazione espliciti. La validità scientifica resta legata al disegno dell'esperimento, alla natura dei dati e alle ipotesi dichiarate.
