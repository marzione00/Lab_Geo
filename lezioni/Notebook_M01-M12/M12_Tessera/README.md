# Tessera — 20 notebook svolti

**M12 · Raster, telerilevamento e morfometria. Dalla geometria della griglia alle grandezze derivate.** Sono inclusi i 20 laboratori M12_N01–M12_N20 con identificativi e titoli originali, in RMarkdown e HTML autonomo. Ogni svolgimento contiene una domanda, obiettivi, dati e unità, cinque blocchi R, risultati calcolati, interpretazione, variante risolta, errore da riconoscere e risposta argomentata.

Aprire **[index.html](index.html)** per navigare. Gli HTML incorporano immagini, stili e formule MathML: si leggono senza connessione e senza R. I collegamenti alle fonti esterne sono facoltativi. Le formule richiedono un browser con supporto MathML. Il raccordo al PDF funziona nella struttura completa del pacchetto M12.

## Esecuzione effettiva

Il registro dell’edizione documenta **100 blocchi R eseguiti, 20 grafici, 0 errori e 0 avvisi**. Il runtime è **R 4.6.0 (2026-04-24) in WebR 0.6.1**, con **terra reale**, versione **1.9.50** restituita da `packageVersion("terra")`, corrispondente al rilascio 1.9-50. Le librerie geografiche sono **GDAL 3.8.1, PROJ 9.2.0 e GEOS 3.11.2**.

N03 legge realmente il TIFF originale. N08 e N19 eseguono ricampionamenti con terra; N18 legge finestre dal file; N20 scrive e rilegge due GeoTIFF. Non sono simulazioni delle chiamate o trascrizioni manuali dei risultati. Le altre operazioni usano R base e i pacchetti standard.

Ogni notebook parte in un ambiente nuovo rispetto agli altri. I suoi cinque blocchi condividono gli oggetti nell’ordine mostrato. Gli output derivano da `source(..., print.eval=TRUE)` e le figure da dispositivi PDF di R. Pandoc produce gli HTML con MathML e immagini incorporate. Il rendering rifiuta un Rmd diverso dalla copia conservata al momento dell’esecuzione.

- [VERIFICA_NOTEBOOK.csv](VERIFICA_NOTEBOOK.csv): esito, blocchi, figure, runtime, durata e SHA-256 di ciascun Rmd e HTML.
- [Verifiche/esecuzione_blocchi.csv](Verifiche/esecuzione_blocchi.csv): registro dei 100 blocchi, errori e avvisi.
- [Verifiche/sessionInfo.txt](Verifiche/sessionInfo.txt): piattaforma e pacchetti caricati.
- [MAPPA_ORIGINALI.csv](MAPPA_ORIGINALI.csv): originali immutati, impronte Git/SHA-256 e ampliamenti dichiarati.
- [MAPPA_SLIDE.csv](MAPPA_SLIDE.csv): raccordo con la lezione estesa.
- [Verifiche/RIEPILOGO_QA.json](Verifiche/RIEPILOGO_QA.json): riepilogo delle verifiche finali.

Le durate nel registro misurano i blocchi, escludendo avvio del runtime, installazione e produzione HTML. Non sono un confronto prestazionale con R nativo.

## Dati, centri e orientamento

Tutti i dati sono **sintetici** e provengono dal repository del corso, commit `649f7cc577b96bd1044d81e78a2f530813e4f96b`. I tre input sono conservati byte per byte: `raster_v3.csv`, `raster_v3.tif` e `casuali_comuni_v3.csv`. [Dati/PROVENIENZA.json](Dati/PROVENIENZA.json) riporta SHA-256 e SHA-1 del blob Git.

| Elemento | Convenzione conservata | Conseguenza |
|---|---|---|
| Dimensioni | 24 righe × 30 colonne = 720 celle | Ogni cella ha una coppia unica di indici |
| Indici CSV | `riga` 0…23 e `colonna` 0…29 | La riga zero è a Sud |
| Centri locali | `x_m = 30 × colonna`, `y_m = 30 × riga` | Centri x 0…870 m, y 0…690 m |
| Bordi locali | x −15…885 m, y −15…705 m | Dominio di 900 × 720 m |
| Quota | Metri sintetici | Nessun rilievo geografico reale |
| Classi | Unità A e B, 360 celle ciascuna | Etichette discrete, non misure continue |
| TIFF | Righe da Nord a Sud | Occorre ribaltare le righe della matrice locale |
| Pixel | PixelIsArea, passo 30 × 30 m | Area planimetrica di 900 m² per cella |
| Georeferenziazione | EPSG:32632, UTM zona 32 Nord, **fittizia** | L’etichetta CRS non rende reale il dataset |
| Corner Nord-Ovest TIFF | E 500000, N 5000000 | Non coincide con il centro della prima cella |
| Centro della prima cella TIFF | E 500015, N 4999985 | Corrisponde al centro locale x 0, y 690 |
| File originale | FLOAT64, NoData −9999 | Il sentinel non è una quota pari a zero |

La corrispondenza dei centri è **E = x_locale + 500015** e **N = y_locale + 4999295**. L’estensione originale è E 500000…500900 e N 4999280…5000000. Queste coordinate sono parte di una costruzione didattica dichiarata. Il controllo completo confronta le 720 quote del TIFF con il CSV dopo il corretto ribaltamento delle righe.

Gli indici della matrice R partono da uno. La maschera originale N04, righe R 5:8 e colonne R 10:15, corrisponde quindi a righe CSV 4:7 e colonne CSV 9:14. Questa distinzione evita uno spostamento silenzioso della maschera.

## Risultati e decisioni del percorso

Il dominio completo ha **64,8 ettari planimetrici** e quota media sintetica **1015,31100866453 m**. N05 seleziona i centri x 300…600 e y 180…510 m, estremi inclusi: **132 celle**, area **11,88 ha**, media **1071,47097643699 m**. Le due medie rispondono a domini differenti; una selezione dei soli centri non è un ritaglio geometrico con frazioni di cella.

N04 elimina 24 quote in una maschera rettangolare: la copertura è **696/720 = 96,6667%**. La media dei valori disponibili è circa **1015,177919 m**; sostituire i mancanti con zero la porta a **981,338655 m**. La variante mostra che una perdita legata alle quote può alterare la media anche con una copertura elevata. NoData e zero rimangono distinti in analisi, figure e consegna.

N07 aggrega blocchi completi 2 × 2 in **180 celle da 60 m**. La media si conserva perché tutti i blocchi hanno quattro celle della stessa area. Il massimo scende da **1103,112537 m** a **1101,398031 m**. La variante con una cella mancante mostra perché la media semplice dei blocchi e quella pesata rispondono a domande diverse quando cambiano le numerosità.

N08 conserva l’esempio monodimensionale originale dei codici 1 e 2 e aggiunge `terra::resample` effettivo. Sul bersaglio traslato di 15 m, bilinear produce codici intermedi inesistenti; near mantiene i codici ammessi. La scelta del metodo dipende dal significato della variabile e non garantisce da sola conservazione di area o copertura. Nel controllo near sulla griglia identica, il percorso numerico del runtime introduce uno scarto massimo di circa **6,10015 × 10⁻⁵ m**: è riportato e verificato rispetto a una tolleranza dichiarata di **10⁻⁴ m**. La precisione FLOAT64 di un file successivo non recupera precisione già persa nel ricampionamento.

N09 verifica le derivate centrali sul piano noto **z = 900 + 0,12x + 0,08y**. Il denominatore è 60 m, la distanza fra i due vicini: non 30 m. Sono valide **616 celle interne**; il bordo viene escluso. N10 distingue angolo in gradi e pendenza percentuale: **45° corrispondono a 100%**. N11 tratta le esposizioni come direzioni circolari, dichiara Nord e senso orario e rende indefinita la media quando la risultante è quasi nulla.

N12 conserva il confronto di illuminazione con azimut 315° e 135° e altezza 45°. Verifica la formula con un prodotto fra normale unitaria e luce e la ripete a 20° e 70° di altezza. Il modello restituisce intensità locale 0–1; non produce nuove quote, misure radiometriche o ombre portate da ostacoli lontani.

N13 usa le bande sintetiche originali, allineate per costruzione. Il rapporto normalizzato non è una diagnosi ambientale e non aggiunge osservazioni indipendenti. N14 conserva i quattro casi e la soglia del denominatore **10⁻⁶**, rendendo esplicita la maschera. Una divisione finita può essere molto sensibile se il denominatore è piccolo.

N15 riassume le unità A e B con **media, deviazione standard e n**. La deviazione standard descrive dispersione delle celle, non incertezza della media. N16 conserva le differenze orizzontali a 30 e 300 m: **696 e 480 coppie**, con differenza assoluta media rispettivamente **5,502874638 e 53,097054964 m**. Le coppie condividono celle; trend e direzione contribuiscono alla sintesi.

N17 conserva i **12 blocchi di 6 × 10 celle** e le **300 repliche** determinate dai primi 3600 uniformi salvati. I quantili 2,5% e 97,5% sono circa **992,217317 e 1041,002542 m**. Sono quantili del meccanismo di ricampionamento, **non un intervallo con copertura garantita al 95%**. Il campo finito è interamente noto nell’esercizio; una vera inferenza richiederebbe un parametro, un disegno di campionamento o un modello aleatorio. La variante iid usa un nuovo seme esplicito, 20261117, e rende visibile la dipendenza dei risultati dall’unità ricampionata senza presentare uno dei due schemi come automaticamente valido.

N18 legge realmente **48 valori** della finestra TIFF originale (righe 5:10, colonne 10:17 in R) e ne verifica ordinamento e uguaglianza con la matrice completa. `object.size` descrive gli oggetti R, non la memoria totale del processo o un benchmark di I/O. N19 mostra che la stessa forma e lo stesso passo non garantiscono allineamento: trasla il raster di **mezzo pixel** e ricampiona esplicitamente sul bersaglio originale.

## Consegna delle pendenze — N20

La cartella [Risultati/M12_N20](Risultati/M12_N20/) contiene:

- [pendenze.csv](Risultati/M12_N20/pendenze.csv): 616 centri locali e pendenza in gradi, ordinati da Sud a Nord.
- [pendenze_interne.tif](Risultati/M12_N20/pendenze_interne.tif): 22 × 28 celle valide, FLOAT64, passo 30 m, CRS fittizio ereditato; estensione E 500030…500870 e N 4999310…4999970.
- [pendenze_con_bordo_NoData.tif](Risultati/M12_N20/pendenze_con_bordo_NoData.tif): geometria originale 24 × 30, con 616 valori interni e 104 celle di bordo NoData.
- [audit_consegna.csv](Risultati/M12_N20/audit_consegna.csv), [audit_tag_NoData.csv](Risultati/M12_N20/audit_tag_NoData.csv) e [scheda_consegna.txt](Risultati/M12_N20/scheda_consegna.txt): controlli e metadati leggibili.

La scrittura usa `terra::writeRaster`, tipo `FLT8S`, sentinel NoData **−9999** e nessuna compressione. Entrambi i file sono riaperti con `terra::rast`. La verifica controlla CRS, risoluzione, estensione, centri Nord-Ovest e Sud-Est, orientamento, maschera, quantità di valori e corrispondenza numerica. `terra::describe` documenta il tag NoData effettivamente scritto. Il bordo è assente perché la differenza centrale non è definita senza ulteriori convenzioni; non è pendenza zero.

## Percorso di lettura

| Notebook | Attività |
|---|---|
| N01–N04 | Griglia, centri, orientamento, GeoTIFF e NoData |
| N05–N08 | Dominio, area, aggregazione e ricampionamento |
| N09–N12 | Derivate, pendenza, esposizione e illuminazione |
| N13–N17 | Bande, maschere, zone, dipendenza e bootstrap |
| N18–N20 | Finestre, allineamento e consegna verificata |

Ogni notebook è autonomo. N20 può essere eseguito senza aprire prima N03 o N10; preparazione, dati e dipendenze sono espliciti in ogni file.

## Eseguire in R o RStudio

1. Estrarre completamente l’archivio mantenendo le cartelle.
2. Aprire `GeoStat_Lab_Notebooks.Rproj` dentro `M12_Tessera`, oppure il progetto generale dei notebook.
3. Aprire un Rmd ed eseguire i blocchi in ordine.
4. Consultare `Risultati/M12_Nxx/` per gli output esportati.

N03, N08, N18, N19 e N20 richiedono **terra installato prima dell’analisi**. Per Knit servono anche rmarkdown, knitr e Pandoc; RStudio normalmente fornisce Pandoc. La preparazione può richiedere connessione e, per terra su alcuni sistemi, librerie geografiche di sistema:

```r
source("R/00_installazione.R")
rmarkdown::render("M12_N03.Rmd", encoding="UTF-8")
```

Nei blocchi analitici non avvengono download o installazioni. `R/crea_html_con_rmarkdown.R` crea tutta la serie con il percorso Knit convenzionale; i dettagli di impaginazione possono differire dall’edizione distribuita.

## Riprodurre il percorso di audit

Dalla cartella `M12_Tessera`, con R nativo e terra installato:

```r
source("R/esegui_notebook.R", encoding="UTF-8")
esegui_notebook()
```

L’esecutore salva il sorgente, estrae i cinque blocchi, cattura output e condizioni e registra i PDF sotto `Verifiche/`. Si arresta con errore finale se almeno un blocco fallisce. Con `ids="M12_N03"` esegue soltanto quel notebook; il registro viene sostituito a ogni chiamata. Per ricostruire tutta l’edizione, eseguire l’intera serie.

Con Python 3, PyMuPDF e Pandoc disponibili:

```bash
python Sorgenti_generazione/crea_html.py
python Sorgenti_generazione/crea_indice.py
python Sorgenti_generazione/verifica_html.py
python Sorgenti_generazione/riepilogo_qa.py
```

Il rendering rifiuta Rmd diversi dalla copia eseguita. Gli HTML incorporano i PNG ricavati dai PDF e mantengono i collegamenti alle figure vettoriali. `Sorgenti_generazione/genera_notebook.py` ricrea il contenuto editoriale e sovrascrive eventuali modifiche manuali degli Rmd; non serve per leggere o rieseguire i notebook.

La verifica indipendente dei file prodotti usa NumPy e rasterio: **21 controlli superati** su TIFF originale, CSV e due GeoTIFF N20. Il dettaglio è in [Verifiche/audit_geotiff_indipendente.json](Verifiche/audit_geotiff_indipendente.json). Lo script opzionale `Sorgenti_generazione/audit_geotiff.py` ripete questo controllo con Python e i due pacchetti installati; non è necessario per leggere gli HTML o per eseguire gli Rmd in R.

Il percorso distribuito ha usato WebR con una libreria persistente WASM già preparata. Lo script opzionale `Sorgenti_generazione/esegui_webr.mjs` richiede Node, WebR 0.6.1 e una libreria terra compilata per WebR, passata come argomento. Tale cache non è inclusa: su un computer ordinario il percorso riproducibile è R nativo con terra. Gli HTML pronti non dipendono da questi runtime.

## Originali e struttura

I 20 file `R/Originali_corso/M12_Nxx.R` coincidono byte per byte con i blob Git del commit dichiarato. La preparazione originale usa `.geologia-v3` e `Corso_Geologia.Rproj`; gli Rmd la sostituiscono con percorsi autonomi. Gli ampliamenti sono documentati in `MAPPA_ORIGINALI.csv`. I protocolli originali vengono conservati; le varianti aggiuntive sono dichiarate separatamente.

`Dati/` contiene gli input immutati. `R/` contiene funzioni, esecutore e originali. `Risultati/` conserva CSV, GeoTIFF e schede. `Verifiche/` contiene log, copie eseguite, figure e QA. `Sorgenti_generazione/` raccoglie i generatori editoriali e HTML.

Riferimenti primari: [modulo M12](https://marzione00.github.io/Lab_Geo/#modulo-M12), [repository del corso](https://github.com/marzione00/Lab_Geo), [terra rast](https://rspatial.github.io/terra/reference/rast.html), [terra resample](https://rspatial.github.io/terra/reference/resample.html), [terra readValues](https://rspatial.github.io/terra/reference/readValues.html), [terra writeRaster](https://rspatial.github.io/terra/reference/writeRaster.html), [R image](https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/image.html) e [R quantile](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html).
