# M08 · Analisi multivariata dei campioni

Geometria della PCA, partizioni e interpretazione geologica.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

8 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M08`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Scale e distanze multivariate** · `#laboratorio/m08-standardizzazione` | Valutare l’effetto delle unità sulla geometria del campione. | [R](../../R/experiments/m08-standardizzazione.R) |
| **Correlazione indotta dalla chiusura** · `#laboratorio/m08-composizioni` | Esaminare variabili positive prima e dopo la normalizzazione. | [R](../../R/experiments/m08-composizioni.R) |
| **Ruotare un asse e misurare la varianza** · `#laboratorio/m08-pca-geometria` | Costruire geometricamente la prima componente principale. | [R](../../R/experiments/m08-pca-geometria.R) |
| **Componenti, contributi e ricostruzione** · `#laboratorio/m08-pca-ricostruzione` | Confrontare dati originali e ricostruzione a rango ridotto. | [R](../../R/experiments/m08-pca-ricostruzione.R) |
| **Iterazioni di K-means** · `#laboratorio/m08-kmeans` | Seguire assegnazione ai centroidi e aggiornamento delle posizioni. | [R](../../R/experiments/m08-kmeans.R) |
| **Numero dei gruppi e silhouette** · `#laboratorio/m08-silhouette` | Valutare coesione e separazione di una partizione. | [R](../../R/experiments/m08-silhouette.R) |
| **Gerarchie e criterio di Ward** · `#laboratorio/m08-ward` | Esaminare fusioni successive e taglio della gerarchia. | [R](../../R/experiments/m08-ward.R) |
| **Sensibilità di una partizione** · `#laboratorio/m08-robustezza` | Valutare la stabilità rispetto a perturbazioni dei dati. | [R](../../R/experiments/m08-robustezza.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**33 slide · 9 figure · 11 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M08_R6.pdf) · [Codice R delle figure](../../materiali/R/M08_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M08_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Campioni, variabili e scale.
- Pagina 7: Ridondanza e composizioni.
- Pagina 10: Geometria delle componenti principali.
- Pagina 16: Interpretazione e calcolo della PCA.
- Pagina 19: Partizioni mediante K-means.
- Pagina 23: Numero dei gruppi e silhouette.
- Pagina 26: Gerarchie e criterio di Ward.
- Pagina 29: Robustezza e significato geologico.
- Pagina 32: Laboratorio e riferimenti.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M08_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M08_N01 | La matrice delle misure e le colonne da escludere | [R](../../materiali/laboratori/M08/M08_N01.R) |
| M08_N02 | Standardizzare non significa rendere indipendenti | [R](../../materiali/laboratori/M08/M08_N02.R) |
| M08_N03 | PCA: costruire nuovi assi | [R](../../materiali/laboratori/M08/M08_N03.R) |
| M08_N04 | Varianza spiegata e perdita di informazione | [R](../../materiali/laboratori/M08/M08_N04.R) |
| M08_N05 | Scores: che cosa rappresenta un punto? | [R](../../materiali/laboratori/M08/M08_N05.R) |
| M08_N06 | Loadings e correlazioni con le componenti | [R](../../materiali/laboratori/M08/M08_N06.R) |
| M08_N07 | Ricostruire con due componenti | [R](../../materiali/laboratori/M08/M08_N07.R) |
| M08_N08 | Ridondanza esatta nelle misure derivate | [R](../../materiali/laboratori/M08/M08_N08.R) |
| M08_N09 | Approfondimento: composizioni e log-ratio | [R](../../materiali/laboratori/M08/M08_N09.R) |
| M08_N10 | Preparare le distanze senza usare l’etichetta | [R](../../materiali/laboratori/M08/M08_N10.R) |
| M08_N11 | K-means: centroidi e variabilità interna | [R](../../materiali/laboratori/M08/M08_N11.R) |
| M08_N12 | Silhouette: separazione relativa del campione | [R](../../materiali/laboratori/M08/M08_N12.R) |
| M08_N13 | Confrontare k senza imporre la risposta attesa | [R](../../materiali/laboratori/M08/M08_N13.R) |
| M08_N14 | Visualizzare i cluster con PCA | [R](../../materiali/laboratori/M08/M08_N14.R) |
| M08_N15 | Profili: ritornare alle unità originali | [R](../../materiali/laboratori/M08/M08_N15.R) |
| M08_N16 | Ward: una gerarchia senza fissare subito k | [R](../../materiali/laboratori/M08/M08_N16.R) |
| M08_N17 | Stabilità senza confrontare i nomi dei cluster | [R](../../materiali/laboratori/M08/M08_N17.R) |
| M08_N18 | Campioni atipici e sensibilità alle variabili | [R](../../materiali/laboratori/M08/M08_N18.R) |
| M08_N19 | Laboratorio applicativo — K=4 | [R](../../materiali/laboratori/M08/M08_N19.R) |
| M08_N20 | Laboratorio applicativo — PCA equivalente | [R](../../materiali/laboratori/M08/M08_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
