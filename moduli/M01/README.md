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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**58 slide · 10 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M01_R6.pdf) · [Codice R delle figure](../../materiali/R/M01_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M01_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Domande e quantità di interesse.
- Pagina 9: Popolazione e gerarchia del campione.
- Pagina 14: Variabili e analisi dimensionale.
- Pagina 20: Disegno della raccolta.
- Pagina 26: Misura e componenti dell’errore.
- Pagina 32: Dipendenza e confondimento.
- Pagina 38: Dalla raccolta alla conclusione.
- Pagina 43: Metadati, disponibilità e censura.
- Pagina 49: Il primo laboratorio in R.
- Pagina 54: Confronto dei disegni e verifica finale.
- Pagina 58: Fonti e materiali.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M01_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

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

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
