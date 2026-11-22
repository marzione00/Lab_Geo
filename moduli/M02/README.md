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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Tellus: 82 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M02/Tellus_M02_gestione_dati.pdf) · [Progetto R della lezione](../../assets/lezioni/M02/Tellus_M02_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M02_Tellus/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M02`).

- Tappa 3: Progetto e dati.
- Tappe 4–7: Progetto e riproducibilità.
- Tappa 8: Laboratorio · progetto.
- Tappe 9–14: Vettori e selezioni.
- Tappa 15: Laboratorio · selezioni.
- Tappe 16–24: Importazione e conversioni.
- Tappa 25: Laboratorio · importazione.
- Tappe 26–32: Trasformazioni e aggregazioni.
- Tappa 33: Laboratorio · aggregazioni.
- Tappe 34–42: Chiavi e relazioni.
- Tappe 43–50: Mancanti e censura.
- Tappe 51–58: Controlli dei dati.
- Tappe 59–68: Derivate e composizioni.
- Tappe 69–75: Funzioni e controlli.
- Tappe 76–82: Tabella analitica.

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

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M02.json`, generata dai sorgenti in `lezioni/M02_Tellus/`; la spiegazione estesa delle tappe è in `content/lezioni/M02.md`.
