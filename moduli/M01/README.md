# M01 · Pensare con i dati

Osservazione, misura e inferenza nelle scienze della Terra.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

10 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M01`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Definire la quantità di interesse** · `#laboratorio/m01-estimando` | Distinguere media delle misure e media delle unità geologiche. | [R](../../R/experiments/m01-estimando.R) |
| **Misure replicate e unità indipendenti** · `#laboratorio/m01-gerarchia` | Separare variabilità fra stazioni e variabilità entro stazione. | [R](../../R/experiments/m01-gerarchia.R) |
| **Unità e analisi dimensionale** · `#laboratorio/m01-unita` | Verificare l’effetto delle unità sul valore numerico. | [R](../../R/experiments/m01-unita.R) |
| **Disegnare una campagna di misura** · `#laboratorio/m01-disegno` | Valutare la copertura di una raccolta su un territorio sintetico. | [R](../../R/experiments/m01-disegno.R) |
| **Bias e rumore di misura** · `#laboratorio/m01-misura` | Separare spostamento sistematico e dispersione casuale. | [R](../../R/experiments/m01-misura.R) |
| **Associazione aggregata e condizionata** · `#laboratorio/m01-confondimento` | Osservare il ruolo di una variabile comune a risposta e predittore. | [R](../../R/experiments/m01-confondimento.R) |
| **Sensibilità della conclusione** · `#laboratorio/m01-conclusione` | Documentare come una scelta analitica modifica una sintesi. | [R](../../R/experiments/m01-conclusione.R) |
| **Limite di rilevabilità e disponibilità** · `#laboratorio/m01-censura` | Distinguere valore osservato, mancante e censurato. | [R](../../R/experiments/m01-censura.R) |
| **Dal campione al riepilogo R** · `#laboratorio/m01-primo-r` | Leggere insieme tabella, grafico e statistiche descrittive. | [R](../../R/experiments/m01-primo-r.R) |
| **Confrontare campagne ripetute** · `#laboratorio/m01-confronto-disegni` | Valutare bias e dispersione di due disegni campionari. | [R](../../R/experiments/m01-confronto-disegni.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Terra: 84 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M01/R_analisi_dati_completa.pdf) · [Progetto R della lezione](../../assets/lezioni/M01/Terra_M01_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M01_Terra/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M01`).

- Tappa 3: Primi passi in R.
- Tappa 4: Dati nelle scienze della Terra.
- Tappa 5: Strumenti di lavoro.
- Tappa 6: Strutture dati.
- Tappa 7: Dati e script.
- Tappa 8: Unità e aggregazione.
- Tappa 9: Documentare il contesto.
- Tappa 10: Metodo di analisi.
- Tappa 11: Domanda e disegno.
- Tappa 12: Popolazione e campione.
- Tappa 13: Leggere la tabella.
- Tappa 14: Statistica di base.
- Tappa 15: Indicatori di posizione.
- Tappa 16: Formule e ordine dei dati.
- Tappa 17: Terra 01 · teoria.
- Tappa 18: Terra 01 · gerarchia.
- Tappa 19: Terra 01 · formule.
- Tappa 20: Terra 01 · calcolo.
- Tappa 21: Terra 01 · effetto dei pesi.
- Tappa 22: Terra 01 · generatore.
- Tappa 23: Terra 01 · codice.
- Tappa 24: Terra 01 · codice e output.
- Tappa 25: Terra 01 · leggere il grafico.
- Tappa 26: Laboratorio nel browser.
- Tappa 27: Terra 01 · attività.
- Tappa 28: Terra 01 · interpretazione.
- Tappe 29–53: Campionamento e statistica.
- Tappe 54–62: Statistica descrittiva.
- Tappe 63–66: Gestione dei dati.
- Tappa 67: Visualizzazione.
- Tappe 68–70: Trasformazioni.
- Tappe 71–83: Serie temporali.
- Tappa 84: Conclusioni.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M01_N01 | Prima di digitare: definire la domanda | [R](../../materiali/laboratori/M01/M01_N01.R) |
| M01_N02 | Una funzione, un argomento, un risultato | [R](../../materiali/laboratori/M01/M01_N02.R) |
| M01_N03 | Aprire il dataset senza modificarlo | [R](../../materiali/laboratori/M01/M01_N03.R) |
| M01_N04 | Leggere una colonna e selezionare una riga | [R](../../materiali/laboratori/M01/M01_N04.R) |
| M01_N05 | Quanti campioni abbiamo davvero? | [R](../../materiali/laboratori/M01/M01_N05.R) |
| M01_N06 | Dai tipi informatici al significato | [R](../../materiali/laboratori/M01/M01_N06.R) |
| M01_N07 | Calcolare e verificare la densità di tutti i provini | [R](../../materiali/laboratori/M01/M01_N07.R) |
| M01_N08 | Confrontare senza anticipare un test | [R](../../materiali/laboratori/M01/M01_N08.R) |
| M01_N09 | Salvare un risultato che un altro studente possa leggere | [R](../../materiali/laboratori/M01/M01_N09.R) |
| M01_N10 | Rileggere il disegno prima dei numeri | [R](../../materiali/laboratori/M01/M01_N10.R) |
| M01_N11 | Simulare una popolazione finita: un’aggiunta esplicita | [R](../../materiali/laboratori/M01/M01_N11.R) |
| M01_N12 | Casuale, sistematico e di convenienza | [R](../../materiali/laboratori/M01/M01_N12.R) |
| M01_N13 | Ripetere l’esperimento di campionamento | [R](../../materiali/laboratori/M01/M01_N13.R) |
| M01_N14 | Ripetere una misura non equivale a cambiare provino | [R](../../materiali/laboratori/M01/M01_N14.R) |
| M01_N15 | Un audit non è una cancellazione automatica | [R](../../materiali/laboratori/M01/M01_N15.R) |
| M01_N16 | Un possibile confondente: l’alterazione | [R](../../materiali/laboratori/M01/M01_N16.R) |
| M01_N17 | Metadati minimi e registro delle scelte | [R](../../materiali/laboratori/M01/M01_N17.R) |
| M01_N18 | La prova della sessione pulita | [R](../../materiali/laboratori/M01/M01_N18.R) |
| M01_N19 | Laboratorio applicativo — Campionamento più ampio | [R](../../materiali/laboratori/M01/M01_N19.R) |
| M01_N20 | Laboratorio applicativo — Conservare gli errori | [R](../../materiali/laboratori/M01/M01_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M01.json`, generata dai sorgenti in `lezioni/M01_Terra/`; la spiegazione estesa delle tappe è in `content/lezioni/M01.md`.
