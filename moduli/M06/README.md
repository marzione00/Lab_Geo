# M06 · Confrontare gruppi e valutare ipotesi

Contrasti, distribuzioni di riferimento e interpretazione dell’evidenza.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

11 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M06`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Definire un contrasto fra gruppi** · `#laboratorio/m06-contrasto` | Collegare disegno e differenza di interesse. | [R](../../R/experiments/m06-contrasto.R) |
| **Costruire il riferimento di permutazione** · `#laboratorio/m06-permutazione` | Seguire la redistribuzione delle etichette sotto scambiabilità. | [R](../../R/experiments/m06-permutazione.R) |
| **Leggere il p-value nel riferimento nullo** · `#laboratorio/m06-pvalue` | Collegare statistica osservata e area di coda. | [R](../../R/experiments/m06-pvalue.R) |
| **Potenza, effetto e numerosità** · `#laboratorio/m06-potenza` | Esaminare la probabilità di rifiuto sotto un’alternativa dichiarata. | [R](../../R/experiments/m06-potenza.R) |
| **Due medie con varianze differenti** · `#laboratorio/m06-welch` | Calcolare l’incertezza di un contrasto con il test di Welch. | [R](../../R/experiments/m06-welch.R) |
| **Confrontare misure appaiate** · `#laboratorio/m06-appaiati` | Separare differenze entro unità e variabilità fra unità. | [R](../../R/experiments/m06-appaiati.R) |
| **Ranghi e forma delle distribuzioni** · `#laboratorio/m06-ranghi` | Interpretare un confronto basato sull’ordinamento. | [R](../../R/experiments/m06-ranghi.R) |
| **Associazione fra categorie** · `#laboratorio/m06-categorie` | Confrontare conteggi osservati e attesi sotto indipendenza. | [R](../../R/experiments/m06-categorie.R) |
| **Molteplicità dei confronti** · `#laboratorio/m06-multipli` | Osservare falsi positivi in famiglie di test sotto l’ipotesi nulla. | [R](../../R/experiments/m06-multipli.R) |
| **Confrontare più medie** · `#laboratorio/m06-anova` | Valutare un’ipotesi globale su quattro gruppi con dispersioni controllate. | [R](../../R/experiments/m06-anova.R) |
| **Effetto, intervallo ed evidenza** · `#laboratorio/m06-relazione` | Ricostruire una conclusione quantitativa completa. | [R](../../R/experiments/m06-relazione.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**35 slide · 8 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M06_R6.pdf) · [Codice R delle figure](../../materiali/R/M06_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M06_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Disegno, contrasto e ipotesi.
- Pagina 6: Permutazione e scambiabilità.
- Pagina 9: P-value e contenuto dell’evidenza.
- Pagina 12: Errori, potenza e pianificazione.
- Pagina 16: Due medie indipendenti: Welch.
- Pagina 19: Confronti appaiati.
- Pagina 22: Ranghi e ipotesi sulla distribuzione.
- Pagina 26: Conteggi e associazione fra categorie.
- Pagina 29: Più gruppi e confronti multipli.
- Pagina 34: Relazione e verifica del confronto.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M06_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M06_N01 | Una domanda e un contrasto con segno | [R](../../materiali/laboratori/M06/M06_N01.R) |
| M06_N02 | Guardare le distribuzioni prima del risultato numerico | [R](../../materiali/laboratori/M06/M06_N02.R) |
| M06_N03 | Una singola permutazione delle etichette | [R](../../materiali/laboratori/M06/M06_N03.R) |
| M06_N04 | Molte permutazioni e p-value Monte Carlo | [R](../../materiali/laboratori/M06/M06_N04.R) |
| M06_N05 | Il grafico della distribuzione nulla | [R](../../materiali/laboratori/M06/M06_N05.R) |
| M06_N06 | Welch: differenza tra medie senza imporre varianze uguali | [R](../../materiali/laboratori/M06/M06_N06.R) |
| M06_N07 | Il numero di osservazioni cambia l’incertezza | [R](../../materiali/laboratori/M06/M06_N07.R) |
| M06_N08 | Effetto nelle unità originali e standardizzato | [R](../../materiali/laboratori/M06/M06_N08.R) |
| M06_N09 | Confrontare i test senza mescolare le ipotesi | [R](../../materiali/laboratori/M06/M06_N09.R) |
| M06_N10 | La coppia è parte del dato | [R](../../materiali/laboratori/M06/M06_N10.R) |
| M06_N11 | Mostrare le coppie con segmenti | [R](../../materiali/laboratori/M06/M06_N11.R) |
| M06_N12 | Il test appaiato è un test sulle differenze | [R](../../materiali/laboratori/M06/M06_N12.R) |
| M06_N13 | Ignorare le coppie cambia l’incertezza | [R](../../materiali/laboratori/M06/M06_N13.R) |
| M06_N14 | Ranghi indipendenti: quale ipotesi? | [R](../../materiali/laboratori/M06/M06_N14.R) |
| M06_N15 | Ranghi appaiati: non basta cambiare un argomento | [R](../../materiali/laboratori/M06/M06_N15.R) |
| M06_N16 | Categorie: osservato e atteso in una tabella | [R](../../materiali/laboratori/M06/M06_N16.R) |
| M06_N17 | Più gruppi: ANOVA come confronto globale | [R](../../materiali/laboratori/M06/M06_N17.R) |
| M06_N18 | Confronti multipli: la famiglia di domande | [R](../../materiali/laboratori/M06/M06_N18.R) |
| M06_N19 | Una tabella di decisione ragionata | [R](../../materiali/laboratori/M06/M06_N19.R) |
| M06_N20 | Laboratorio applicativo — Differenze a mano | [R](../../materiali/laboratori/M06/M06_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
