# M02 · R e gestione dei dati

Dall’importazione alla tabella analitica verificabile.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

10 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M02`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Oggetti espliciti e stato dell’analisi** · `#laboratorio/m02-progetto` | Ricostruire le dipendenze di un risultato. | [R](../../R/experiments/m02-progetto.R) |
| **Selezioni logiche e tipi** · `#laboratorio/m02-selezioni` | Combinare due condizioni di selezione. | [R](../../R/experiments/m02-selezioni.R) |
| **Importare numeri con convenzioni differenti** · `#laboratorio/m02-importazione` | Diagnosticare errori prodotti da separatori decimali incompatibili. | [R](../../R/experiments/m02-importazione.R) |
| **Aggregazione e pesi delle osservazioni** · `#laboratorio/m02-aggregazioni` | Confrontare media complessiva e media delle medie. | [R](../../R/experiments/m02-aggregazioni.R) |
| **Collegare tabelle senza moltiplicare le misure** · `#laboratorio/m02-join` | Verificare la cardinalità di un collegamento mediante una chiave. | [R](../../R/experiments/m02-join.R) |
| **Meccanismo di indisponibilità** · `#laboratorio/m02-mancanti` | Confrontare dati mancanti casualmente e mancanti associati al valore. | [R](../../R/experiments/m02-mancanti.R) |
| **Controlli di plausibilità fisica** · `#laboratorio/m02-controlli` | Distinguere validità sintattica e coerenza fisica. | [R](../../R/experiments/m02-controlli.R) |
| **Chiusura di una composizione** · `#laboratorio/m02-composizione` | Osservare l’effetto del vincolo di somma costante. | [R](../../R/experiments/m02-composizione.R) |
| **Contratti di validità di una funzione** · `#laboratorio/m02-funzioni` | Verificare precondizioni prima di eseguire un calcolo. | [R](../../R/experiments/m02-funzioni.R) |
| **Verificare una tabella analitica** · `#laboratorio/m02-tabella` | Controllare righe, chiavi e unità prima dell’analisi. | [R](../../R/experiments/m02-tabella.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**43 slide · 10 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M02_R6.pdf) · [Codice R delle figure](../../materiali/R/M02_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M02_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Progetto e stato della sessione.
- Pagina 7: Vettori, tipi e selezioni.
- Pagina 11: Importazione e conversioni.
- Pagina 15: Trasformazioni e aggregazioni.
- Pagina 19: Chiavi e relazioni fra tabelle.
- Pagina 23: Mancanti e censura.
- Pagina 27: Coerenza fisica e registro delle decisioni.
- Pagina 31: Variabili derivate e composizione chimica.
- Pagina 35: Funzioni, parametri e controlli.
- Pagina 39: Tabella analitica e consegna.
- Pagina 43: Fonti e laboratori.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M02_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M02_N01 | Una tabella ben importata non è scontata | [R](../../materiali/laboratori/M02/M02_N01.R) |
| M02_N02 | Vettori: tipi e operazioni | [R](../../materiali/laboratori/M02/M02_N02.R) |
| M02_N03 | Scegliere righe e colonne in modo esplicito | [R](../../materiali/laboratori/M02/M02_N03.R) |
| M02_N04 | Raggruppare: cambia l’unità della tabella | [R](../../materiali/laboratori/M02/M02_N04.R) |
| M02_N05 | Join molti-a-uno con controllo delle chiavi | [R](../../materiali/laboratori/M02/M02_N05.R) |
| M02_N06 | Un esempio di tabella lunga | [R](../../materiali/laboratori/M02/M02_N06.R) |
| M02_N07 | Una funzione con un contratto chiaro | [R](../../materiali/laboratori/M02/M02_N07.R) |
| M02_N08 | Applicare una sintesi a più variabili | [R](../../materiali/laboratori/M02/M02_N08.R) |
| M02_N09 | Un’alternativa tidyverse, non un secondo corso | [R](../../materiali/laboratori/M02/M02_N09.R) |
| M02_N10 | Esportazione e controllo di ritorno | [R](../../materiali/laboratori/M02/M02_N10.R) |
| M02_N11 | Importazione conservativa | [R](../../materiali/laboratori/M02/M02_N11.R) |
| M02_N12 | Convertire il testo senza nascondere gli errori | [R](../../materiali/laboratori/M02/M02_N12.R) |
| M02_N13 | Categorie e duplicati richiedono regole diverse | [R](../../materiali/laboratori/M02/M02_N13.R) |
| M02_N14 | Controlli geometrici e disponibilità | [R](../../materiali/laboratori/M02/M02_N14.R) |
| M02_N15 | Visualizzare il controllo e derivare le misure | [R](../../materiali/laboratori/M02/M02_N15.R) |
| M02_N16 | Sotto il limite: non eliminare il simbolo e basta | [R](../../materiali/laboratori/M02/M02_N16.R) |
| M02_N17 | Microsonda: totale e qualità analitica | [R](../../materiali/laboratori/M02/M02_N17.R) |
| M02_N18 | Mg#: convertire le masse in quantità molari | [R](../../materiali/laboratori/M02/M02_N18.R) |
| M02_N19 | Sensibilità delle soglie e conservazione dei dati | [R](../../materiali/laboratori/M02/M02_N19.R) |
| M02_N20 | Laboratorio applicativo — Massa contro moli | [R](../../materiali/laboratori/M02/M02_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
