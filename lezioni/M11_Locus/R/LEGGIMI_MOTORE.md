# M11 Locus: motore scientifico riproducibile

Edizione: 20 novembre 2026. Tutti i risultati in `Calcoli/` e i 40 PDF in `Risultati/Figure/` sono stati prodotti eseguendo R. I controlli indipendenti in Python verificano risultati già prodotti da R; non ne sostituiscono l'esecuzione.

## Avvio

Aprire il progetto e impostare come directory di lavoro la cartella `M11_Locus` che contiene `setup.R`.

```r
# Una sola volta, in una normale installazione R con accesso a CRAN:
install.packages("sf")

# Stato leggero per i frammenti didattici, senza riscrivere risultati:
source("R/stato_lezione.R", encoding = "UTF-8")

# Rigenerazione completa: CSV, JSON, GeoJSON, modelli, verifiche e 40 PDF:
source("R/rigenera_calcoli.R", encoding = "UTF-8")
```

`Lezione_Locus.R` carica lo stato e stampa un riepilogo. I calcoli numerici usano R base e `stats`; `sf` esegue realmente le operazioni geografiche. `spdep` e `gstat` sono riferimenti teorici e software per ulteriori analisi, ma non sono dipendenze necessarie di questo motore.

La produzione è stata eseguita con WebR 0.6.1, R 4.6.0 e sf 1.1-3, usando i pacchetti binari del repository ufficiale R-WASM. Sono state caricate GEOS 3.11.2, GDAL 3.8.1 e PROJ 9.2.0. `Verifiche/RUNTIME_E_PACCHETTI.json` registra versioni, URL e SHA-256 degli archivi effettivamente usati; `SESSIONE_R.txt` e `VERSIONI_SF.txt` registrano la sessione. Il codice R resta eseguibile in un'installazione nativa con `sf` e le sue dipendenze disponibili. Piccole differenze di arrotondamento fra versioni sono ammesse dalle tolleranze dichiarate.

## Organizzazione e oggetti

| File | Funzione |
|---|---|
| `setup.R` | Legge i dati, verifica la griglia, costruisce distanze, pesi e separazione geografica |
| `R/funzioni_M11.R` | Funzioni documentate per metriche, Moran, distanze, IDW, variogramma e kriging |
| `R/stato_lezione.R` | Aggiunge gli oggetti sf, il trend, le coppie, il semivariogramma e l'esempio di kriging |
| `R/rigenera_calcoli.R` | Esegue i protocolli e salva risultati e verifiche |
| `R/genera_figure.R` | Disegna i 40 PDF vettoriali dagli oggetti calcolati dal file precedente |
| `Calcoli/summary.json` | Riepilogo numerico; `riassunto.json` è un alias identico |
| `Calcoli/indice_figure.csv` | Nome, formato e significato di ogni figura |

Lo stato leggero espone `d`, `xy`, `z`, `n`, `D`, `A`, `W`, `nv`, `v`, `lag_W`, `I_A`, `I_W`, `train_idx`, `test_idx`, `train`, `test`, `geo`, `utm`, `ritorno`, `trend`, `residui`, `coppie`, `vg`, `pred_idw` e `ok`. L'ordine iniziale delle matrici segue quello degli ID del CSV. Se si riordinano i siti, occorre riordinare coerentemente valori e matrici.

Le interfacce principali sono:

```r
moran_I(z, W)                         # vale anche passando A come secondo argomento
haversine(lon1, lat1, lon2, lat2,
          R = 6371000)               # risultato in metri
idw_weights(xy, pos, p = 2)
idw_pred(xy, z, newxy, p = 2)
nn_pred(xy, z, newxy)
ok_solve(C, c0, C00, z)
```

`idw_weights` ripartisce il peso fra osservazioni coincidenti con il bersaglio e quindi ne restituisce la media. La tolleranza di coincidenza è `1e-10` nelle unità delle coordinate. In assenza di coincidenze, stabilizza i pesi dividendo le distanze per la distanza minima prima dell'elevamento alla potenza: questa riscalatura non cambia i pesi normalizzati. `nn_pred` media eventuali vicini equidistanti; nel test principale la scelta del vicino è univoca. Il laboratorio N11 adotta invece il primo indice per mostrare una regola esplicita di parità sulla griglia.

## Dati e riferimenti geografici

I due CSV sono copie intatte dal repository `marzione00/Lab_Geo`, commit `649f7cc577b96bd1044d81e78a2f530813e4f96b`. Percorsi e impronte si trovano in `Dati/PROVENIENZA.json`; la verifica contro i Git blob è conservata in `Verifiche/PROVENIENZA_GIT_SITO.json`.

`spazio_v3.csv` contiene 64 siti su una griglia 8 × 8, con passo 250 m ed estensione da 0 a 1750 m per asse. Concentrazione, quota e collocazione geografica sono sintetiche. La concentrazione è in unità arbitrarie, abbreviate u.a. Il piano `x_m/y_m` ha origine locale convenzionale e nessun EPSG attribuito. Le colonne `lon/lat` sono una distinta collocazione geografica sintetica vicino a 9° E, 45° N; la loro proiezione non è una ricostruzione esatta delle coordinate locali.

Il motore crea `geo` in `OGC:CRS84` per rendere esplicito l'ordine longitudine-latitudine, lo trasforma in EPSG:32632 e torna al riferimento geografico. Il massimo errore di ritorno è circa `1.421085e-14` gradi. Il GeoJSON `Risultati/campioni_RFC7946.geojson` è scritto con le opzioni `RFC7946=YES` e `COORDINATE_PRECISION=10`, poi riletto e allineato per ID. Il massimo scarto delle coordinate è circa `4.991563e-11` gradi. Un ritorno numericamente accurato non dimostra che il riferimento iniziale sia quello corretto: questo dipende dalla provenienza e dai metadati.

La haversine usa una sfera di raggio 6 371 000 m, coerente con i 6371 km del laboratorio originale. Le distanze UTM usano il piano della proiezione ellissoidale. Questi confronti sono descrittivi: nessuno dei metodi viene presentato come identico alla griglia locale convenzionale.

## Vicinati e Moran

Il protocollo principale definisce `A = 1*(D > 0 & D <= 260)`. La diagonale è nulla; ci sono 112 archi non orientati e `S0(A)=224`. I gradi sono 2 per i quattro angoli, 3 per i 24 siti sul bordo esclusi gli angoli e 4 per i 36 interni. `W` divide ogni riga di A per il relativo grado. Le somme di riga sono uno e `S0(W)=64`, ma W non è simmetrica in generale.

Per una matrice H, il motore usa

\[
I_H=\frac{n}{\sum_{ij}h_{ij}}\frac{\sum_{ij}h_{ij}(z_i-\bar z)(z_j-\bar z)}{\sum_i(z_i-\bar z)^2}.
\]

Il risultato è `I_A = 0.7195277292` e `I_W = 0.7975650044`. Lo scatter usa `v = z - mean(z)` in ascissa e `Wv` in ordinata: la pendenza della regressione con intercetta è I_W. L'intercetta effettiva è `0.01110904390`, perché W non è necessariamente doppiamente stocastica. I quadranti HH, LL, HL, LH sono classificazioni descrittive e non test locali di significatività.

Il riferimento originale di N14 usa 100 blocchi consecutivi di 64 uniformi da `casuali_comuni_v3.csv`. Per ciascun blocco, `order` definisce una permutazione dei valori. L'approfondimento usa 999 permutazioni ottenute da `set.seed(20261109)` e `sample`. Entrambi valutano I_A, con alternativa unilaterale di associazione positiva e formula `(1 + superamenti)/(B + 1)`. Ci sono zero superamenti: i p-value sono `1/101` e `1/1000`. Il riferimento richiede scambiabilità delle etichette; non separa trend e dipendenza residua.

Il piano `concentrazione ~ x_m + y_m` viene stimato per descrivere il gradiente. Sui residui, I_A vale `-0.03957848007` e I_W `-0.04155473348`. Non si applica una permutazione libera dei residui come test esatto: la stima OLS introduce vincoli e modifica la loro covarianza.

## Semivarianze, supporto e copertura

Le coppie sono i 2016 insiemi `{i,j}` con `i < j`; sono esclusi diagonali e doppioni orientati. Ogni contributo è `(z_i-z_j)^2/2`. I bin sono `(0,300]`, `(300,600]`, `(600,1000]`, `(1000,2500]` m. I conteggi sono rispettivamente 112, 362, 476 e 1066. Le ascisse del grafico sono le distanze medie effettive nei bin, non i centri geometrici degli intervalli. Le coppie condividono siti, perciò i conteggi non sono numerosità di osservazioni indipendenti e non generano automaticamente errori standard iid.

Le curve direzionali usano coppie entro 22,5° dagli assi Est-Ovest e Nord-Sud, con gli stessi bin. Il confronto prima/dopo il piano è descrittivo. Non si conclude anisotropia del campo residuo dalla sola differenza delle curve grezze.

Le curve teoriche esponenziale, gaussiana e sferica sono esempi dichiarati, non adattamenti al dataset. Usano nugget 0,2, sill parziale 4 e portata pratica circa 1200 m; i parametri di scala sono rispettivamente 400 m, `1200/sqrt(3)` m e 1200 m. La curva sferica raggiunge il sill a distanza finita; le altre due lo raggiungono asintoticamente. La semivarianza a h=0 è zero; il nugget rappresenta il limite da destra.

Le aggregazioni principali separano x<1000 e x>=1000, 32 siti ciascuna. I quattro blocchi x/y a soglia 1000 contengono 16 siti ciascuno. Le regioni sovrapposte A:x<=1250 e B:x>=750 producono 88 appartenenze e 24 siti duplicati. Fare la media delle righe del join peserebbe due volte questi siti. L'esempio della figura31 è invece costruito: numerosità 2/8 e medie 10/20 danno media per sito 18 e media per blocco 15. I dati reali con gruppi sbilanciati a x=750 restano nei CSV come approfondimento distinto.

La selezione lungo strada comprende y<=250, cioè 16 siti. La media è 15,86751 u.a., contro 17,19033 dell'intero reticolo. La differenza di -1,32283 u.a. descrive questa selezione nel dataset completo; non è un errore standard o una stima del bias sotto un disegno probabilistico non specificato. Le medie dei siti non diventano medie areali senza pesi e ipotesi sul campionamento.

## IDW e verifica geografica

La superficie descrittiva usa tutti i 64 siti, p=2 e una griglia di 45 × 45 posizioni. È una ricostruzione numerica; i 2025 valori della griglia non sono nuove osservazioni.

Il test principale tiene fuori tutti i siti x>=1250. Il train contiene 40 siti con x<1250 e si estende fino a x=1000. I 24 bersagli di test sono quindi esterni al suo inviluppo convesso: si valuta trasferimento geografico verso Est, con extrapolazione. IDW p=2 è fissato prima del test e usa tutti e soli i 40 siti del train. I riferimenti sono la media del train e il vicino più prossimo. Il segno dell'errore è sempre **osservato meno previsto**.

| Metodo | MAE | RMSE | Bias medio |
|---|---:|---:|---:|
| Media train | 4,201063 | 4,731467 | 4,194663 |
| Vicino più prossimo | 2,217838 | 2,632278 | 1,954545 |
| IDW p=2 | 3,257099 | 3,807826 | 3,175309 |

Tutte le metriche sono in u.a. In questo test il vicino più prossimo è migliore di IDW secondo MAE e RMSE. Il risultato riguarda questa geometria e questi valori, senza una graduatoria universale dei metodi. I 24 errori possono essere dipendenti fra loro; non sono 24 repliche indipendenti del protocollo.

L'approfondimento di selezione dell'esponente resta interamente nel train: tre frontiere a x=500, 750 e 1000. A ciascuna frontiera si usano i siti con x minore e si prevedono gli otto siti della colonna sulla frontiera. Per p=1,2,3 si ottengono 24 previsioni interne per candidato, con RMSE 2,412459, 2,099319 e 1,902455. La scelta interna è p=3. Questa estensione non sostituisce p=2 nel confronto principale. Il test finale non viene riutilizzato per scegliere l'esponente.

## Kriging: un esempio separato e verificabile

I siti sono (0,0), (500,0), (1000,0), con valori 10,15,12. Il bersaglio è (250,0). La covarianza dichiarata è `C(h)=4*exp(-(h/800)^2)`, con nugget zero e media costante ignota. Non viene stimata dai tre valori né attribuita al campo con gradiente del caso guida.

Il sistema usa il segno positivo del moltiplicatore:

\[
\begin{bmatrix}C&1\\1^T&0\end{bmatrix}\begin{bmatrix}\lambda\\\mu\end{bmatrix}=\begin{bmatrix}c_0\\1\end{bmatrix}.
\]

I pesi sono 0,4651253068, 0,6918785279 e -0,1570038347; la previsione è 13,14538497. La somma è uno e il terzo peso è negativo. La varianza dell'errore è

\[
C_{00}-2\lambda^Tc_0+\lambda^TC\lambda
=C_{00}-\lambda^Tc_0-\mu
=0,03696075338.
\]

La quantità è in (u.a.)² e condizionata al modello di covarianza. Non include incertezza di stima dei suoi parametri o errore nella scelta del modello. Con nugget zero la varianza è numericamente nulla nei siti osservati. Prevedere un campo latente, una nuova misura con errore o una media di blocco richiederebbe covarianze e bersagli coerenti.

## Verifiche e figure

`Verifiche/test_numerici.csv` registra 25 controlli eseguiti in R. Fra questi: perturbazione delle concentrazioni del test e ricostruzione del train per provare l'assenza di contaminazione; casi noti per IDW coincidente e kriging indipendente; equivalenza delle formule della varianza; controlli sf e rilettura GeoJSON.

`Verifiche/controlli_indipendenti.py` registra 20 controlli indipendenti in Python. Le proiezioni sono confrontate con pyproj 3.8.0 / PROJ 9.8.1, con scarto massimo rispetto a sf di circa `4.656613e-9` m. Il kriging viene anche risolto minimizzando direttamente la varianza sotto il vincolo di somma unitaria. Il rapporto completo è in `controlli_indipendenti.json`.

I 40 PDF sono monopagina e interamente vettoriali, senza immagini bitmap. `audit_figure.py` controlla pagine, bitmap e testo oltre il bordo. Le anteprime sono state renderizzate e ispezionate. Le figure 03,22,26 sono panoramiche; le altre sono dimensionate per la colonna delle slide. Le carte comparative usano una scala di concentrazione comune; residui ed errori hanno scale divergenti simmetriche attorno a zero. La copertina è un elaborato 3D separato e non deriva da questo motore.
