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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Polychroma: 108 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M08/Polychroma_M08_multivariata.pdf) · [Progetto R della lezione](../../assets/lezioni/M08/Polychroma_M08_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M08_Polychroma/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M08`).

- Tappe 15–26: II · Ridondanza e composizioni.
- Tappe 27–44: III · Geometria della PCA.
- Tappe 45–57: IV · Interpretare le componenti.
- Tappe 58–72: VI · K-means.
- Tappe 73–82: VII · Numero dei gruppi.
- Tappe 83–93: VIII · Gerarchie di Ward.
- Tappe 94–103: VIII · Stabilità e interpretazione.
- Tappe 104–108: IX · Un’analisi completa.

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

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M08.json`, generata dai sorgenti in `lezioni/M08_Polychroma/`; la spiegazione estesa delle tappe è in `content/lezioni/M08.md`.
