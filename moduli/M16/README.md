# M16 · Classificazione e validazione

Geometria dei modelli, probabilità e trasferibilità delle prestazioni.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

6 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M16`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Bersaglio predittivo e nuove stazioni** · `#laboratorio/m16-bersaglio` | Confrontare predizione di misure e trasferimento a nuove unità. | [R](../../R/experiments/m16-bersaglio.R) |
| **Standardizzazione e confine decisionale** · `#laboratorio/m16-geometria` | Esaminare un classificatore a centroidi nella metrica scelta. | [R](../../R/experiments/m16-geometria.R) |
| **Selezione dei predittori e contaminazione** · `#laboratorio/m16-selezione` | Valutare la selezione di variabili su puro rumore. | [R](../../R/experiments/m16-selezione.R) |
| **Alberi e aggregazione di classificatori** · `#laboratorio/m16-alberi` | Confrontare un albero con un insieme di alberi su campioni bootstrap. | [R](../../R/experiments/m16-alberi.R) |
| **Soglia, discriminazione e calibrazione** · `#laboratorio/m16-metriche` | Separare probabilità previste e decisione binaria. | [R](../../R/experiments/m16-metriche.R) |
| **Trasferibilità e cambiamento della relazione** · `#laboratorio/m16-trasferimento` | Valutare un modello su una popolazione differente. | [R](../../R/experiments/m16-trasferimento.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**29 slide · 11 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M16_R6.pdf) · [Codice R delle figure](../../materiali/R/M16_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M16_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Campione e domanda predittiva.
- Pagina 7: Trasformazioni e geometria della decisione.
- Pagina 13: Selezione e validazione per gruppi.
- Pagina 16: Alberi e insiemi di classificatori.
- Pagina 19: Metriche e probabilità.
- Pagina 27: Diagnostica e trasferibilità.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M16_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M16_N01 | Campione, stazione, classe: audit gerarchico | [R](../../materiali/laboratori/M16/M16_N01.R) |
| M16_N02 | Split per stazione: nessuna sovrapposizione | [R](../../materiali/laboratori/M16/M16_N02.R) |
| M16_N03 | Modello di riferimento: predire la classe più frequente | [R](../../materiali/laboratori/M16/M16_N03.R) |
| M16_N04 | Standardizzare solo sul training | [R](../../materiali/laboratori/M16/M16_N04.R) |
| M16_N05 | Nearest centroid: classificare con una formula trasparente | [R](../../materiali/laboratori/M16/M16_N05.R) |
| M16_N06 | k vicini: voto locale e sensibilità a k | [R](../../materiali/laboratori/M16/M16_N06.R) |
| M16_N07 | Logistica binaria: una probabilità per una domanda | [R](../../materiali/laboratori/M16/M16_N07.R) |
| M16_N08 | Albero poco profondo: regole e unità | [R](../../materiali/laboratori/M16/M16_N08.R) |
| M16_N09 | Aumentare la complessità riduce sempre l’errore utile? | [R](../../materiali/laboratori/M16/M16_N09.R) |
| M16_N10 | Validazione interna per stazioni | [R](../../materiali/laboratori/M16/M16_N10.R) |
| M16_N11 | Scegliere k senza guardare il test | [R](../../materiali/laboratori/M16/M16_N11.R) |
| M16_N12 | Random forest: un insieme di alberi | [R](../../materiali/laboratori/M16/M16_N12.R) |
| M16_N13 | Matrice di confusione con ordine fisso | [R](../../materiali/laboratori/M16/M16_N13.R) |
| M16_N14 | Classi sbilanciate: accuracy e balanced accuracy | [R](../../materiali/laboratori/M16/M16_N14.R) |
| M16_N15 | Precision e recall per una classe definita | [R](../../materiali/laboratori/M16/M16_N15.R) |
| M16_N16 | Soglia decisionale: probabilità e scelta | [R](../../materiali/laboratori/M16/M16_N16.R) |
| M16_N17 | Brier score e calibrazione | [R](../../materiali/laboratori/M16/M16_N17.R) |
| M16_N18 | Importanza per permutazione: sensibilità del modello | [R](../../materiali/laboratori/M16/M16_N18.R) |
| M16_N19 | Controesempio di leakage: copiare il target | [R](../../materiali/laboratori/M16/M16_N19.R) |
| M16_N20 | Mini-progetto: una scheda modello con limiti | [R](../../materiali/laboratori/M16/M16_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
