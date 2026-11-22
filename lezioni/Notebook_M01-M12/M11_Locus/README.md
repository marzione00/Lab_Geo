# Locus — 20 notebook svolti

**M11 · Statistica spaziale. Coordinate, associazione e previsione nel territorio.** Sono inclusi i 20 laboratori M11_N01–M11_N20 con i titoli originali, in RMarkdown e HTML autonomo. Ogni svolgimento contiene domanda, obiettivi, dati e unità, cinque blocchi R, risultati effettivamente calcolati, interpretazione, variante risolta, errore da riconoscere e risposta argomentata.

Aprire **[index.html](index.html)** per navigare. Gli HTML incorporano immagini, stili e formule MathML: si leggono senza connessione e senza R. I collegamenti alle fonti esterne sono facoltativi. Le formule richiedono un browser con supporto MathML. Il collegamento alle slide funziona nella struttura completa del pacchetto M11.

## Esecuzione effettiva

Il registro documenta **100 blocchi R eseguiti, 20 grafici, 0 errori e 0 avvisi**. Il runtime dell’edizione è **R 4.6.0 (2026-04-24) in WebR 0.6.1**. Nei notebook N05, N06 e N20 è stato usato **sf reale**, versione 1.1.3 restituita da `packageVersion("sf")`, con **GEOS 3.11.2, GDAL 3.8.1 e PROJ 9.2.0**. Le chiamate a st_transform, st_set_crs, st_write e st_read sono state eseguite; non sono sostituite da output manuali o da formule approssimate.

Ogni notebook parte in un ambiente nuovo rispetto agli altri. I suoi cinque blocchi condividono gli oggetti nell’ordine mostrato. I risultati testuali derivano da `source(..., print.eval=TRUE)`; le figure derivano da dispositivi PDF di R. Pandoc produce gli HTML con formule MathML e immagini incorporate. Prima del rendering viene confrontato il sorgente Rmd con la copia conservata al momento dell’esecuzione.

- [VERIFICA_NOTEBOOK.csv](VERIFICA_NOTEBOOK.csv): esito, blocchi, figure, runtime, durata e SHA-256 di ciascun Rmd e HTML.
- [Verifiche/esecuzione_blocchi.csv](Verifiche/esecuzione_blocchi.csv): registro dei 100 blocchi con output, errori e avvisi.
- [Verifiche/sessionInfo.txt](Verifiche/sessionInfo.txt): piattaforma e pacchetti caricati.
- [MAPPA_ORIGINALI.csv](MAPPA_ORIGINALI.csv): corrispondenza con gli originali, impronte Git/SHA-256 e adattamenti.
- [MAPPA_SLIDE.csv](MAPPA_SLIDE.csv): raccordo con le 110 slide della lezione.

La durata nel registro misura i blocchi nel runtime, escludendo avvio di WebR, installazione dei pacchetti e produzione degli HTML. Non è una valutazione delle prestazioni di un computer con R nativo.

N06 include un errore intenzionale: la trasformazione di un oggetto privo di CRS viene catturata e interpretata nel codice. Il registro riporta zero errori non gestiti; l’esempio controllato resta visibile nello svolgimento.

## Dati e coordinate

I dati sono **interamente sintetici** e provengono dal repository del corso, commit `649f7cc577b96bd1044d81e78a2f530813e4f96b`. I byte dei due CSV sono verificati sia con SHA-256 sia con SHA-1 del blob Git. [Dati/PROVENIENZA.json](Dati/PROVENIENZA.json) documenta le copie.

| File o colonne | Significato | Limite da conservare |
|---|---|---|
| `spazio_v3.csv` |64 siti, griglia 8×8, passo 250 m | Valori puntuali sintetici, non medie osservate di celle |
| `x_m`, `y_m` | Piano locale, da 0 a 1750 m per asse | Nessun codice EPSG; i metri non certificano un CRS |
| `concentrazione` | Misura sintetica in unità arbitrarie | Nessuna interpretazione ambientale o sanitaria reale |
| `quota_m` | Quota sintetica in metri | Attributo del caso didattico |
| `lon`, `lat` | Georiferimento sintetico separato vicino 9°E e 45°N | Relazione approssimata; non è una semplice traslazione UTM di x_m/y_m |
| `casuali_comuni_v3.csv` |12000 uniformi u e valori normali z | N14 usa i primi 6400 u in 100 blocchi consecutivi da 64 |

Il percorso geografico dichiara **OGC:CRS84**, con ordine longitudine, latitudine. N05 trasforma queste geometrie in **EPSG:32632, UTM zona 32 Nord**, e torna in CRS84 con tolleranza 10⁻⁷ gradi. La reversibilità numerica non dimostra che il CRS sorgente sia stato attribuito correttamente. N06 rende esplicita la distinzione fra rietichettatura e trasformazione.

N20 scrive un **GeoJSON RFC7946**, con dieci cifre decimali nelle coordinate, lo rilegge con sf e verifica 64 geometrie POINT, ID, coordinate e tutti gli attributi. La precisione della serializzazione non indica accuratezza di rilievo. Le coordinate locali rimangono attributi senza EPSG; non vengono usate come geometria geografica. I confronti si allineano per ID, non per posizione della riga.

## Decisioni scientifiche del percorso

La soglia di vicinato è 260 m. N12 costruisce **A binaria simmetrica**, con 112 collegamenti non diretti e somma totale 224, e **W normalizzata per riga**, con somma totale 64 e pesi generalmente asimmetrici. N13 mantiene distinti **I_A=0.7195277292** e **I_W=0.7975650044**. La pendenza del diagramma degli scarti contro il lag W coincide con I_W nelle condizioni verificate, non con I_A.

N14 conserva le 100 permutazioni originali, ottenute ordinando blocchi consecutivi da 64 valori u. L’alternativa positiva è dichiarata prima del conteggio e il p-value usa `(1 + eccedenze)/(B + 1)`. Il risultato originale è 1/101. La variante con 999 permutazioni usa un nuovo seme esplicito, 20261114, e non ricicla il file u. Una risoluzione Monte Carlo maggiore non aggiunge siti né giustifica da sola la scambiabilità.

N15 usa le 2016 coppie non ordinate dei 64 siti e le classi originali (0, 300], (300, 600], (600, 1000], (1000, 2500] m. Le coppie condividono osservazioni: non vengono trattate come 2016 repliche indipendenti e non si costruiscono errori standard ingenui basati su tale ipotesi. La semivarianza mantiene l’unità (u.a.)².

N16 confronta i 16 siti con y ≤ 250 m con la griglia finita di 64 siti. La copertura è descritta rispetto a questa griglia di riferimento; non è un errore di previsione o una misura completa di rappresentatività territoriale. N17 mostra perché la media semplice di quattro medie coincide con la media dei siti solo nel caso bilanciato con 16 siti per blocco. La variante sbilanciata distingue media per blocchi 15 e media per individui 18.

N18 usa IDW con potenze 1, 2, 3 nel punto (900, 900) m e dichiara il comportamento nei siti coincidenti. Non c’è un valore osservato al bersaglio da usare per scegliere p. **N19 fissa p=2**, 40 siti train con x<1250 m e 24 test con x ≥ 1250 m; confronta anche media del train e vicino più prossimo. Il test viene usato per misurare errori, senza cambiare p dopo il confronto. La divisione descrittiva Ovest/Est del CSV usa invece 1000 m e non può sostituire questo split.

Nel test geografico gli RMSE sono 3.8078259792 u.a. per IDW p 2, 4.73146668 per la media del train e 2.63227839 per il vicino più prossimo. Questi valori riguardano un solo settore escluso di un dataset sintetico; non definiscono una graduatoria universale degli interpolatori. Tutti i bersagli sono a Est del massimo x del train: il compito comporta extrapolazione geografica.

## Percorso di lettura

| Notebook | Attività |
|---|---|
| N01–N06 | Audit, ordine degli assi, distanze, CRS, trasformazioni e rietichettatura |
| N07–N10 | Carte puntuali, confini, molteplicità del join e buffer |
| N11–N14 | Pareggi, pesi spaziali, Moran e riferimento di permutazione |
| N15–N17 | Semivarianza, copertura del campione e medie di blocco |
| N18–N20 | IDW, verifica geografica e consegna GeoJSON |

Ogni notebook è autonomo: si può eseguire N20 senza avere aperto N05. Preparazione e dipendenze sono esplicite in ogni file.

## Eseguire in R o RStudio

1. Estrarre completamente l’archivio mantenendo le cartelle.
2. Aprire `GeoStat_Lab_Notebooks.Rproj` dentro `M11_Locus`, oppure il progetto generale dei notebook.
3. Aprire un Rmd ed eseguire i blocchi in ordine.
4. Consultare `Risultati/M11_Nxx/` per gli output esportati.

N05, N06 e N20 richiedono **sf installato prima dell’analisi**. Gli altri notebook usano R base e pacchetti standard. Per il comando Knit servono anche rmarkdown, knitr e Pandoc; RStudio normalmente fornisce Pandoc. La preparazione iniziale può richiedere connessione e, per sf su alcuni sistemi, librerie GDAL, GEOS e PROJ:

```r
source("R/00_installazione.R")
rmarkdown::render("M11_N05.Rmd", encoding="UTF-8")
```

Non si installano pacchetti né si scaricano dati nei blocchi analitici. Per creare tutti gli HTML con knitr è disponibile `R/crea_html_con_rmarkdown.R`. Questo percorso esegue il medesimo codice e può differire in dettagli di impaginazione dall’edizione distribuita.

## Riprodurre il percorso di audit

Dalla cartella `M11_Locus`, con R nativo e sf installato:

```r
source("R/esegui_notebook.R", encoding="UTF-8")
esegui_notebook()
```

L’esecutore salva il sorgente eseguito, estrae i blocchi, cattura output e condizioni e registra i PDF sotto `Verifiche/`. Si arresta con errore finale se almeno un blocco fallisce. Con `ids="M11_N05"` esegue solo un notebook; il registro viene sostituito a ogni chiamata. Per ricostruire l’intera edizione e il suo indice occorre eseguire tutta la serie.

Con Python 3, PyMuPDF e Pandoc disponibili:

```bash
python Sorgenti_generazione/crea_html.py
python Sorgenti_generazione/crea_indice.py
python Sorgenti_generazione/verifica_html.py
```

Il rendering rifiuta Rmd diversi dalla copia eseguita. Gli HTML incorporano i PNG ottenuti dai PDF e mantengono i collegamenti alle versioni vettoriali. `Sorgenti_generazione/genera_notebook.py` ricrea il contenuto editoriale originale e sovrascrive eventuali modifiche manuali agli Rmd: non è necessario per leggere o rieseguire il pacchetto.

L’esecuzione distribuita ha usato WebR con una libreria persistente di pacchetti WASM già preparata. Lo script opzionale `Sorgenti_generazione/esegui_webr.mjs` accetta il percorso di quella libreria come argomento; richiede Node, WebR 0.6.1 e sf compilato per WebR. La cache WASM non è inclusa: il percorso ordinario riproducibile su un computer è R nativo con sf. Gli HTML già pronti non dipendono da nessuno di questi runtime.

## Originali, fonti e struttura

I 20 script in `R/Originali_corso/` sono copie byte per byte dei blob Git del commit dichiarato. Il loro progetto originale usa `.geologia-v3` e `Corso_Geologia.Rproj`; gli Rmd del pacchetto sostituiscono quella preparazione con percorsi autonomi. Le integrazioni didattiche, le varianti e l’uso esplicito di CRS84 sono documentati nella mappa degli originali.

`Dati/` contiene gli input immutati. `R/` contiene funzioni di servizio, esecutore e originali. `Risultati/` conserva CSV, GeoJSON e schede. `Verifiche/` conserva log, sorgenti eseguiti e grafici. `Sorgenti_generazione/` contiene i generatori editoriali e HTML.

Riferimenti primari: [modulo M11 del corso](https://marzione00.github.io/Lab_Geo/#modulo-M11), [repository](https://github.com/marzione00/Lab_Geo), [sf st_transform](https://r-spatial.github.io/sf/reference/st_transform.html), [sf st_crs](https://r-spatial.github.io/sf/reference/st_crs.html), [sf st_write](https://r-spatial.github.io/sf/reference/st_write.html), [GeoJSON RFC7946](https://www.rfc-editor.org/rfc/rfc7946), [R dist](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/dist.html) e [R sample](https://stat.ethz.ch/R-manual/R-devel/library/base/html/sample.html).
