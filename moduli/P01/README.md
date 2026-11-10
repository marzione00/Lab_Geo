# P01 · Geometria dei pori e permeabilità

Sezioni, carote e inferenza su un piccolo campione osservativo.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Confronta supporto delle misure, relazione statistica e sensibilità dell’analisi, ricostruendo un’argomentazione su porosità e permeabilità.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Definire l’unità

- **Definire la quantità di interesse** — Distinguere media delle misure e media delle unità geologiche. [Programma R](../../R/experiments/m01-estimando.R); rotta del sito: `#laboratorio/m01-estimando`.
- **Misure replicate e unità indipendenti** — Separare variabilità fra stazioni e variabilità entro stazione. [Programma R](../../R/experiments/m01-gerarchia.R); rotta del sito: `#laboratorio/m01-gerarchia`.

### Esaminare la relazione

- **Scale lineari e logaritmiche** — Esaminare un processo moltiplicativo su due scale. [Programma R](../../R/experiments/m03-scale.R); rotta del sito: `#laboratorio/m03-scale`.
- **La geometria dei minimi quadrati** — Confrontare una retta proposta con la soluzione che minimizza gli scarti quadratici. [Programma R](../../R/experiments/m07-minimi-quadrati.R); rotta del sito: `#laboratorio/m07-minimi-quadrati`.

### Valutare la stabilità

- **Leva e influenza di un’osservazione** — Distinguere distanza nel predittore e influenza sul modello. [Programma R](../../R/experiments/m07-influenza.R); rotta del sito: `#laboratorio/m07-influenza`.
- **Ricampionamento per stazioni** — Confrontare bootstrap delle misure e delle unità indipendenti. [Programma R](../../R/experiments/m05-ricampionamento.R); rotta del sito: `#laboratorio/m05-ricampionamento`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**21 slide · 7 figure · 5 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P01_R6.pdf) · [Codice R delle figure](../../materiali/R/P01_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P01_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Domanda geologica e supporto della misura.
- Pagina 8: Visualizzazione e unità di analisi.
- Pagina 10: Modello e interpretazione del parametro.
- Pagina 15: Ricampionamento e sensibilità.
- Pagina 20: Argomentazione geologica e consegna.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P01_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
