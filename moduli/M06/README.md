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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Gemina: 93 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M06/Gemina_M06_confronti_ipotesi.pdf) · [Progetto R della lezione](../../assets/lezioni/M06/Gemina_M06_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M06_Gemina/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M06`).

- Tappe 3–19: I · Definire il confronto.
- Tappe 20–36: II · Interpretare l’evidenza.
- Tappe 37–46: III · Confrontare due gruppi.
- Tappe 47–53: Coppie e differenze.
- Tappe 54–59: Confronti basati sui ranghi.
- Tappe 60–64: Conteggi e associazione.
- Tappe 65–69: Più gruppi.
- Tappe 70–77: Famiglie di confronti.
- Tappe 78–93: V · Applicazioni e verifica.

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

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M06.json`, generata dai sorgenti in `lezioni/M06_Gemina/`; la spiegazione estesa delle tappe è in `content/lezioni/M06.md`.
