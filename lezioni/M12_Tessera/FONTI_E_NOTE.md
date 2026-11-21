# Tessera — fonti, protocolli e limiti dei risultati

## Provenienza e natura dei dati

Il materiale di riferimento è il modulo **M12 — Raster, telerilevamento e morfometria** del sito [Lab_Geo](https://marzione00.github.io/Lab_Geo/#indice), nel repository [marzione00/Lab_Geo](https://github.com/marzione00/Lab_Geo), revisione **649f7cc577b96bd1044d81e78a2f530813e4f96b**. I 20 laboratori originali conservano gli identificativi M12_N01–M12_N20. Le 37 fonti recuperate sono state confrontate byte per byte con i Git blob della revisione; il registro è `Verifiche/PROVENIENZA_GIT_SITO.json`.

`Dati/raster_v3.csv`, `Dati/raster_v3.tif` e `Dati/casuali_comuni_v3.csv` sono copie degli originali. Le loro impronte SHA-256 sono in `Dati/PROVENIENZA.json`. Il terreno, le zone A/B e le bande spettrali sono **sintetici**. Il GeoTIFF usa EPSG:32632 con una collocazione convenzionale: non rappresenta un rilievo osservato e non coincide con i siti del modulo Locus. L’esperimento spettrale non usa immagini Landsat o Sentinel.

## Griglia, orientamento e area

La tabella contiene 24 righe × 30 colonne, cioè 720 celle. Gli indici originali partono da zero; il passo è 30 m su entrambi gli assi. I centri locali sono `x = 0,30,…,870 m` e `y = 0,30,…,690 m`. La matrice R `Z` ha la prima riga a **Sud**, mentre `as.matrix(r, wide=TRUE)` legge il GeoTIFF con la prima riga a **Nord**. Il confronto dei valori richiede quindi `Z[24:1,]`.

Il GeoTIFF originale è FLOAT64, PixelIsArea, con NoData = −9999 e trasformazione affine GDAL `(500000,30,0,5000000,0,-30)`. L’estensione è:

| Asse | Limite inferiore | Limite superiore |
|---|---:|---:|
| Est | 500000 m | 500900 m |
| Nord | 4999280 m | 5000000 m |

L’origine affine è un **angolo**, non un centro. Per i centri del dataset, dopo aver rispettato l’ordine delle righe, la relazione esatta è:

\[
E=x+500015,\qquad N=y+4999295.
\]

Il primo centro Nord-Ovest è `(500015,4999985)`. L’estensione locale completa è `[-15,885] × [-15,705] m`. Queste convenzioni seguono la definizione di centro a mezzo pixel della [documentazione GDAL sulle geotrasformazioni](https://gdal.org/en/stable/tutorials/geotransforms_tut.html).

L’area usata nel corso è **planimetrica**: 900 m² = 0,09 ha per cella, 64,8 ha complessivi. Non è l’area della superficie inclinata del terreno né una stima geodetica della superficie terrestre. Per dati reali in coordinate angolari o proiezioni non equivalenti la regola va rivista; [`terra::cellSize`](https://rspatial.github.io/terra/reference/cellSize.html) documenta anche la correzione delle aree per raster proiettati. Non si sostituisce tale calcolo ai 64,8 ha del piano didattico.

## Maschere, dominio e aggregazione

Il GeoTIFF originale dichiara una sentinella NoData ma contiene 720 valori validi. La mancanza è introdotta **nell’esperimento**, escludendo le righe R 5–8 e le colonne 10–15: 24 celle, corrispondenti agli indici originali riga 4–7 e colonna 9–14. Restano 696 celle, copertura 96,6667% e area planimetrica 62,64 ha. Il valore NA non viene sostituito da zero nelle analisi corrette.

Le medie effettive sono 1015,3110087 m per il terreno completo, 1015,1779191 m per i disponibili e 981,3386552 m dopo la sostituzione impropria con zero. La finestra dei centri `300≤x≤600`, `180≤y≤510` comprende 132 celle, 11,88 ha, media 1071,4709764 m. Il criterio riguarda i centri; l’unione delle celle selezionate ha bordi a mezzo passo oltre i centri estremi.

L’aggregazione 2×2 produce 180 medie su una griglia 12×15, passo 60 m e stessa estensione. La media globale si conserva perché tutti i blocchi contengono quattro valori con lo stesso peso. Il massimo scende da 1103,1125373 a 1101,3980314 m. Se mancano valori, la media delle medie ricostruisce quella dei disponibili soltanto con i pesi appropriati.

Le zone originali A/B hanno 360 celle e 32,4 ha ciascuna. La maschera cade tutta in A: restano 336 celle in A e 360 in B. La media zonale pesata per area osservata ricostruisce la media delle 696 celle disponibili; non ricostruisce automaticamente quella del dominio completo.

## Ricampionamento e precisione numerica

I ricampionamenti sono stati eseguiti realmente con [`terra::resample`](https://rspatial.github.io/terra/reference/resample.html). Il confronto continuo trasferisce la griglia originale da 30 m a una griglia da 15 m con lo stesso dominio usando `near` e `bilinear`. La maggiore densità di celle è una proprietà dell’uscita, non una nuova risoluzione osservativa. Per categorie nominali il caso N08 mostra perché un codice interpolato, come 1,5 fra le classi 1 e 2, non è una nuova classe valida; è inoltre eseguito un confronto reale con `terra`.

Le traslazioni di ±15 m spostano la georeferenziazione dei medesimi valori. La sottrazione ingenua delle matrici darebbe zero pur associando luoghi diversi. Il riallineamento bilineare è valutato sulle celle per le quali il software restituisce valori finiti. Il conteggio può differire alle due estremità del dominio per le regole del bordo; non si assume simmetria dell’extrapolazione. Sul piano noto, nella parte interna, la traslazione verso Est di δ produce lo scarto −0,12δ.

Nel runtime usato, il percorso di ricampionamento introduce arrotondamenti compatibili con passaggi interni a precisione singola. Il confronto indipendente bilineare fra `terra` e `rasterio` ha scarto massimo **6,09483×10⁻⁵ m**, verificato con tolleranza **2×10⁻⁴ m**. Il notebook documenta anche circa 6,10015×10⁻⁵ m dopo `near` sulla stessa griglia, con tolleranza 10⁻⁴ m. Geometria identica e identità numerica esatta sono controlli distinti. Scrivere successivamente FLOAT64 conserva il risultato calcolato, ma non recupera precisione eventualmente perduta prima.

## Morfometria, piani e direzioni

Le derivate principali sono differenze centrate con quattro vicini, denominatore 60 m e orientamento locale positivo verso Est/Nord. Il dominio interno contiene `(24−2)(30−2)=616` celle; le 104 celle esterne hanno pendenza NA nel raster completo. Nel caso mascherato sono necessari **centro valido e quattro vicini validi**: restano 572 pendenze valide e 148 NA nella griglia completa.

La pendenza in gradi è `atan(sqrt(gx²+gy²))*180/pi`; quella percentuale è `100*sqrt(gx²+gy²)`. Il piano indipendente `z=900+0,12x+0,08y` verifica entrambe le componenti su tutte le celle: pendenza 8,2067271°, 14,4222051%, azimut di discesa 236,3099325°. Il confronto con `terra::terrain(neighbors=4,unit="degrees")` sul terreno ha scarto massimo 2,0961×10⁻¹³°. Il metodo predefinito a otto vicini è diverso: qui la differenza media assoluta è 0,0585361°, non un errore di arrotondamento. Le opzioni e la convenzione dei piani sono documentate in [`terrain`](https://rspatial.github.io/terra/reference/terrain.html).

L’esposizione è l’azimut di massima discesa, orario dal Nord: `atan2(-gx,-gy)`. Con modulo del gradiente ≤10⁻¹² il motore assegna NA; `terra` documenta invece 90° come valore convenzionale sui piani. Per le direzioni si riportano media circolare e risultante. Nel caso 359°/1° la media è Nord e la risultante è 0,9998477; per 0°/180° la risultante è praticamente zero e la direzione media viene lasciata indeterminata.

`Calcoli/confronto_operazioni.csv` confronta media delle quote→pendenza e pendenza→media sullo stesso supporto di 130 celle interne da 60 m. Le medie dei due risultati sono 16,1016244° e 16,4451476°; la differenza assoluta media è 0,3569303°. L’ordine delle operazioni va quindi dichiarato.

## Esperimento analitico a 10, 30 e 100 m

Questo approfondimento è **distinto dal raster originale di 720 celle**. Usa il campo noto

\[
f(x,y)=900+0,12x+0,08y+80\exp\!\left[-\frac{(x-450)^2+(y-300)^2}{2\,120^2}\right]
\]

sul dominio `[0,900] × [0,600] m`, pari a 54 ha. A ogni passo h i centri sono `h/2+k·h`; i valori sono valutazioni puntuali del campo analitico nei centri, non medie areali né nuove osservazioni. Le griglie hanno rispettivamente 5400, 600 e 54 celle.

Gli errori delle differenze centrate sono confrontati con la derivata esatta sullo stesso rettangolo fisico `[100,800] × [100,500] m`. I pesi sono le aree esatte d’intersezione delle celle con tale rettangolo: sommano sempre a **28 ha**, anche quando il bordo attraversa celle da 30 m. La RMSE della pendenza, pesata con queste aree, vale 0,0274002°, 0,2444133° e 2,4529583°. È una comparazione numerica su supporti discretizzati con pesi dichiarati, non un confronto fra DEM osservati a tre risoluzioni.

## Luce, bande e indice

L’hillshade usa il prodotto della normale unitaria `(-gx,-gy,1)` con la direzione unitaria della sorgente, troncato inferiormente a zero. Azimut 315°/135°, altezza 45°, fattore verticale 1. Il prodotto scalare è verificato anche con una formula trigonometrica indipendente; gli ordini delle matrici sono controllati. Il modello è locale: non include ombre proiettate da rilievi lontani, occlusione dell’orizzonte o proprietà radiometriche del materiale. La documentazione [`terra::shade`](https://rspatial.github.io/terra/reference/shade.html) chiarisce anche la distinzione fra radianti di pendenza/esposizione e gradi della sorgente luminosa.

Le bande del caso guida sono `R=0,2+0,05*cos(y/150)` e `N=0,4+0,1*sin(x/180)`. Sono adimensionali, positive e sintetiche. L’indice `(N−R)/(N+R)` usa la stessa algebra dell’[NDVI documentato da USGS](https://www.usgs.gov/landsat-missions/landsat-normalized-difference-vegetation-index), ma qui non autorizza una classificazione ecologica. L’intervallo ottenuto è 0,0910818–0,5380818.

L’esperimento del denominatore conserva due esclusioni su quattro coppie originali con soglia 10⁻⁶. La soglia è didattica, non universale. L’esperimento di scala/offset codifica le bande sintetiche con fattore 0,0000275 e offset −0,2, parametri documentati da [USGS per la riflettanza Landsat Collection 2](https://www.usgs.gov/faqs/how-do-i-use-a-scale-factor-landsat-level-2-science-products). Non utilizza DN Landsat osservati: mostra che una scala comune si cancella nel rapporto, un offset comune no.

## Dipendenza e bootstrap: due protocolli distinti

Le differenze a 30 e 300 m sono lungo Est–Ovest: 696 e 480 coppie, con differenze assolute medie 5,5028746 e 53,0970550 m. Le coppie condividono celle; il campo ha una tendenza. Queste quantità sono descrittive e non sono test fra repliche indipendenti.

I 12 blocchi sono rettangoli non sovrapposti di 6×10 celle, 60 valori e 5,4 ha ciascuno. Sono ordinati da Sud a Nord e, in ciascuna fascia, da Ovest a Est. La loro media equiponderata coincide con la media del raster completo.

| Protocollo | Generazione | Quantile 2,5% | Quantile 97,5% |
|---|---|---:|---:|
| N17 originale: 300 repliche | primi 3600 uniformi, `floor(u*12)+1`, 12 estrazioni per replica | 992,2173166 m | 1041,0025417 m |
| Figura originale: 1999 repliche | `set.seed(20261109)`, 12 blocchi con reinserimento | 990,2844252 m | 1038,9578886 m |
| Confronto didattico di celle: 1999 repliche | `set.seed(20261110)`, 720 celle con reinserimento | 1011,8660173 m | 1018,7317902 m |

Il confronto a celle singole della figura usa il seme 20261110; la variante autonoma del notebook N17 usa invece il seme esplicito 20261117. I due output sono esperimenti distinti e restano documentati nei rispettivi sorgenti.

I quantili sono calcolati con `quantile(type=7)`. L’aumento delle repliche riguarda la precisione Monte Carlo, non la validità delle ipotesi. La superficie finita completamente nota ha una media esatta: per attribuire incertezza a un processo o ad altri territori occorre un bersaglio inferenziale esplicito. I 12 blocchi non sono automaticamente indipendenti o scambiabili. I quantili riportati sono sensibilità allo schema, **non intervalli con copertura garantita**.

## Finestre, esportazioni e prove effettive

La finestra originale legge righe TIFF 5–10 e colonne 10–17: 48 valori. Per produrre tutte le sue differenze centrate si legge il contorno di una cella, 8×10 = 80 valori. La derivata del nucleo coincide con quella calcolata sull’intero dataset. I costi di memoria nei grafici contano soltanto 8 byte per valore double; distinguono MB decimali e MiB nel CSV e non includono copie, strutture degli oggetti o compressione.

Sono prodotti e riletti con R/terra:

| File | Dimensioni | Validi | NoData |
|---|---:|---:|---:|
| `pendenze_interne.tif` | 22×28 | 616 | 0 |
| `pendenze_con_bordo_NA.tif` | 24×30 | 616 | 104 |
| `quote_maschera.tif` | 24×30 | 696 | 24 |

Tutti usano FLOAT64/FLT8S, NoData −9999 e `COMPRESS=NONE`. L’export interno ha estensione Est `[500030,500870]`, Nord `[4999310,4999970]` m. Geometria, maschera e valori riletti sono verificati; lo scarto massimo dei valori è zero. I rapporti `GDAL_*.txt` registrano i tag effettivi. I campi `STATISTICS_MEAN/STDDEV=-9999` non calcolati dal writer non sono usati come statistiche; le statistiche pubblicate sono calcolate dai valori in R e conservate nei CSV. [`writeRaster`](https://rspatial.github.io/terra/reference/writeRaster.html) documenta tipo numerico e sentinella; [GDAL GeoTIFF](https://gdal.org/en/stable/drivers/raster/gtiff.html) documenta il formato.

## Esecuzione e fonti software

Il motore è stato realmente eseguito in **R 4.6.0**, tramite **WebR 0.6.1**, con **terra 1.9-50**, **GDAL 3.8.1**, **PROJ 9.2.0**, **GEOS 3.11.2**, TBB non attivo. I pacchetti R-WASM provengono dal [repository ufficiale](https://repo.r-wasm.org/bin/emscripten/contrib/4.6/). Non sono stati simulati output R. `R/stato_lezione.R` prepara gli oggetti senza scrivere risultati; `R/rigenera_calcoli.R` rigenera calcoli, esportazioni e figure.

Le verifiche comprendono 37 controlli R, 31 controlli indipendenti Python/NumPy/rasterio e 42 PDF scientifici monopagina interamente vettoriali. Python 3.12.14 usa NumPy 2.5.5, rasterio 1.5.2 e GDAL 3.12.2. La differenza di binding/versione rende il controllo GeoTIFF e del ricampionamento indipendente dall’accesso R, pur condividendo la famiglia GDAL. Le prove del piano, delle normali, degli indici e delle aree sono anche analitiche. Registri dettagliati in `Verifiche/`.

Ulteriori riferimenti primari: [`terra::rast`](https://rspatial.github.io/terra/reference/rast.html), per geometria e lettura differita dei pixel; [`readValues` e lettura per blocchi](https://rspatial.github.io/terra/reference/readwrite.html); [WebR](https://docs.r-wasm.org/webr/latest/). Le fonti online sono state consultate il 20 novembre 2026; la riproducibilità del caso del corso è ancorata alla revisione Git e ai dati inclusi.
