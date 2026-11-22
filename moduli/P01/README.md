# P01 · Geometria dei pori e permeabilità

Sezioni, carote e inferenza su un piccolo campione osservativo.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Confronta supporto delle misure, relazione statistica e sensibilità dell’analisi, ricostruendo un’argomentazione su porosità e permeabilità.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Definire l’unità

- **Definire la quantità di interesse**: Distinguere media delle misure e media delle unità geologiche. [Programma R](../../R/experiments/m01-estimando.R); rotta del sito: `#laboratorio/m01-estimando`.
- **Misure replicate e unità indipendenti**: Separare variabilità fra stazioni e variabilità entro stazione. [Programma R](../../R/experiments/m01-gerarchia.R); rotta del sito: `#laboratorio/m01-gerarchia`.

### Esaminare la relazione

- **Scale lineari e logaritmiche**: Esaminare un processo moltiplicativo su due scale. [Programma R](../../R/experiments/m03-scale.R); rotta del sito: `#laboratorio/m03-scale`.
- **La geometria dei minimi quadrati**: Confrontare una retta proposta con la soluzione che minimizza gli scarti quadratici. [Programma R](../../R/experiments/m07-minimi-quadrati.R); rotta del sito: `#laboratorio/m07-minimi-quadrati`.

### Valutare la stabilità

- **Leva e influenza di un’osservazione**: Distinguere distanza nel predittore e influenza sul modello. [Programma R](../../R/experiments/m07-influenza.R); rotta del sito: `#laboratorio/m07-influenza`.
- **Ricampionamento per stazioni**: Confrontare bootstrap delle misure e delle unità indipendenti. [Programma R](../../R/experiments/m05-ricampionamento.R); rotta del sito: `#laboratorio/m05-ricampionamento`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P01: 31 tappe.**

[Presentazione PDF](../../assets/lezioni/P01/P01_Pori.pdf) · [Progetto R della spedizione](../../assets/lezioni/P01/Spedizione_P01_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P01_Pori/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P01`).

- Tappa 3: Il caso guida.
- Tappe 4–8: Domanda geologica e supporto della misura.
- Tappe 9–10: Visualizzazione e unità di analisi.
- Tappe 11–15: Modello e interpretazione del parametro.
- Tappe 16–20: Ricampionamento e sensibilità.
- Tappe 21–22: Argomentazione geologica e consegna.
- Tappe 23–29: Laboratori della spedizione.
- Tappa 30: Sintesi.
- Tappa 31: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P01_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P01.json`, generata dai sorgenti in `lezioni/P01_Pori/`.
