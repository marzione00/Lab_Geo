# M03 · Descrivere e visualizzare i dati

Distribuzioni, confronti e relazioni nelle misure geologiche.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

9 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M03`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Supporto della rappresentazione** · `#laboratorio/m03-supporto` | Confrontare misure puntuali e medie di stazione. | [R](../../R/experiments/m03-supporto.R) |
| **Frequenze, denominatori e pesi** · `#laboratorio/m03-denominatori` | Confrontare conteggi e proporzioni fra gruppi di dimensione diversa. | [R](../../R/experiments/m03-denominatori.R) |
| **Media e mediana sotto contaminazione** · `#laboratorio/m03-posizione` | Valutare la sensibilità delle misure di posizione. | [R](../../R/experiments/m03-posizione.R) |
| **Dispersione e intervallo interquartile** · `#laboratorio/m03-quantili` | Confrontare dispersione quadratica e dispersione centrale. | [R](../../R/experiments/m03-quantili.R) |
| **Istogramma e stima di densità** · `#laboratorio/m03-smoothing` | Distinguere struttura dei dati e scelte di rappresentazione. | [R](../../R/experiments/m03-smoothing.R) |
| **Confronti fra distribuzioni** · `#laboratorio/m03-gruppi` | Separare differenze di posizione e dispersione. | [R](../../R/experiments/m03-gruppi.R) |
| **Relazione lineare e non lineare** · `#laboratorio/m03-relazioni` | Confrontare forma del legame e coefficiente di correlazione. | [R](../../R/experiments/m03-relazioni.R) |
| **Posizione e rappresentazione spaziale** · `#laboratorio/m03-mappa` | Riconoscere una struttura geografica nascosta in un riepilogo. | [R](../../R/experiments/m03-mappa.R) |
| **Scale lineari e logaritmiche** · `#laboratorio/m03-scale` | Esaminare un processo moltiplicativo su due scale. | [R](../../R/experiments/m03-scale.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Iride: 79 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M03/Iride_M03_descrivere_visualizzare.pdf) · [Progetto R della lezione](../../assets/lezioni/M03/Iride_M03_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M03_Iride/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M03`).

- Tappe 3–8: Domanda e supporto.
- Tappa 9: Laboratorio · supporto.
- Tappe 10–14: Frequenze e denominatori.
- Tappa 15: Laboratorio · denominatori.
- Tappe 16–22: Misure di posizione.
- Tappa 23: Laboratorio · posizione.
- Tappe 24–31: Dispersione e quantili.
- Tappe 32–41: Distribuzioni.
- Tappe 42–50: Confronti fra gruppi.
- Tappe 51–59: Relazioni fra misure.
- Tappe 60–66: Posizione e spazio.
- Tappe 67–73: Scale e trasformazioni.
- Tappe 74–79: Figure e consegna.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M03_N01 | Il campione da descrivere | [R](../../materiali/laboratori/M03/M03_N01.R) |
| M03_N02 | Frequenza assoluta, relativa e percentuale | [R](../../materiali/laboratori/M03/M03_N02.R) |
| M03_N03 | Quando mancano le categorie | [R](../../materiali/laboratori/M03/M03_N03.R) |
| M03_N04 | Una tabella a doppia entrata | [R](../../materiali/laboratori/M03/M03_N04.R) |
| M03_N05 | Media e mediana: due domande differenti | [R](../../materiali/laboratori/M03/M03_N05.R) |
| M03_N06 | Dispersione: la media non basta | [R](../../materiali/laboratori/M03/M03_N06.R) |
| M03_N07 | Quantili e intervallo interquartile | [R](../../materiali/laboratori/M03/M03_N07.R) |
| M03_N08 | Una tabella completa per morfotipo | [R](../../materiali/laboratori/M03/M03_N08.R) |
| M03_N09 | Media di individui o media di gruppi? | [R](../../materiali/laboratori/M03/M03_N09.R) |
| M03_N10 | Scrivere una descrizione che rispetti i dati | [R](../../materiali/laboratori/M03/M03_N10.R) |
| M03_N11 | Dati e domanda prima del tipo di grafico | [R](../../materiali/laboratori/M03/M03_N11.R) |
| M03_N12 | Istogramma: il ruolo delle classi | [R](../../materiali/laboratori/M03/M03_N12.R) |
| M03_N13 | Densità e area: non confondere altezza e frequenza | [R](../../materiali/laboratori/M03/M03_N13.R) |
| M03_N14 | Boxplot con punti: centro, dispersione e numerosità | [R](../../materiali/laboratori/M03/M03_N14.R) |
| M03_N15 | La distribuzione cumulativa empirica | [R](../../materiali/laboratori/M03/M03_N15.R) |
| M03_N16 | Scatterplot: due misure dello stesso individuo | [R](../../materiali/laboratori/M03/M03_N16.R) |
| M03_N17 | Trasformazione logaritmica e standardizzazione | [R](../../materiali/laboratori/M03/M03_N17.R) |
| M03_N18 | Facoltativo: costruire una figura con ggplot2 | [R](../../materiali/laboratori/M03/M03_N18.R) |
| M03_N19 | Salvare una figura e una didascalia | [R](../../materiali/laboratori/M03/M03_N19.R) |
| M03_N20 | Laboratorio applicativo — Classi esplicite | [R](../../materiali/laboratori/M03/M03_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M03.json`, generata dai sorgenti in `lezioni/M03_Iride/`; la spiegazione estesa delle tappe è in `content/lezioni/M03.md`.
