# Verifica dei notebook M12

## Esecuzione e provenienza

I 20 notebook sono stati eseguiti dopo l’integrazione della mappa definitiva delle slide. I registri documentano 100 blocchi, zero errori, zero avvisi e zero messaggi. I sorgenti Rmd coincidono con le copie conservate durante l’esecuzione e gli HTML incorporano gli output dello stesso svolgimento. Le 20 figure derivano dai dispositivi PDF di R.

I 20 originali R e i tre input CSV/TIFF coincidono byte per byte con i blob Git del commit dichiarato. Il controllo finale usa SHA-256, SHA-1 del blob Git e dimensione dei file; il dettaglio è in `audit_provenienza_finale.json`.

## Verifica spaziale indipendente

Le operazioni terra sono state effettivamente eseguite: lettura del TIFF, ricampionamenti, finestre, traslazioni, scrittura e rilettura. N20 produce un raster interno 22 × 28 e una griglia completa 24 × 30 con 104 celle di bordo NoData. Entrambi sono FLOAT64, con sentinel −9999 e la georeferenziazione fittizia dichiarata.

Un secondo controllo usa rasterio e NumPy, distinti da R/terra: 21 verifiche sull’originale, sul CSV e sui due GeoTIFF effettivamente distribuiti. Sono verificati forma, dtype, CRS, affine, risoluzione, sentinel, maschera e valori, ricalcolando le derivate dal CSV originale. Il risultato è in `audit_geotiff_indipendente.json`.

I log GDAL conservano il tag NoData effettivamente scritto. Eventuali campi opzionali `STATISTICS_MEAN` e `STATISTICS_STDDEV` con valore −9999 indicano statistiche non calcolate nel percorso di scrittura; non sono usati come medie o deviazioni standard. Tutte le verifiche numeriche usano i valori delle celle letti dai file.

N08 riporta il piccolo arrotondamento del percorso di resampling near sulla griglia identica e lo confronta con una tolleranza dichiarata di 10⁻⁴ m. Non viene affermata identità bit per bit. La successiva scrittura FLOAT64 non recupera precisione persa in una trasformazione precedente.

## Verifica visiva e HTML

Sono stati ispezionati tutti i 20 grafici nel montaggio `grafici_montaggio.jpg`. Titoli, assi, legende, unità e annotazioni risultano presenti, senza ritagli o sovrapposizioni rilevati.

Le anteprime `index_layout.png`, `M12_N08_layout.png`, `M12_N17_layout.png` e `M12_N20_layout.png` mostrano il primo foglio di un rendering temporaneo WeasyPrint70, media screen, 1400 × 1000 px. Sono stati controllati anche il titolo lungo originale N08, navigazione, indicatori di esecuzione e indice. Questa verifica non equivale a un collaudo nel browser: WeasyPrint non convalida il rendering MathML e i PDF temporanei non sono distribuiti come notebook.

L’audit strutturale delle 22 pagine HTML verifica immagini incorporate, assenza di runtime esterni, riferimenti interni, impronte Rmd/HTML e collegamenti al PDF della lezione. Il riepilogo finale è `RIEPILOGO_QA.json`. Il generatore permette di ripetere la verifica dopo eventuali cambiamenti di posizione nel pacchetto completo.
