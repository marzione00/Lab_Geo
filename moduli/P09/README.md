# P09 · Un livello raro e la sua incertezza

Massimi annuali, distribuzione di Gumbel e rischio su un orizzonte temporale.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Stima un livello raro e discuti quanto la conclusione dipenda dalla lunghezza del record e dalla forma della coda.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Definire l’evento

- **Dalle osservazioni ai massimi annuali** — Esaminare la distribuzione dei massimi di blocchi indipendenti. [Programma R](../../R/experiments/m14-massimi.R); rotta del sito: `#laboratorio/m14-massimi`.
- **Superamenti e separazione degli episodi** — Distinguere giorni sopra soglia ed eventi temporali. [Programma R](../../R/experiments/m14-episodi.R); rotta del sito: `#laboratorio/m14-episodi`.

### Stimare e ricampionare

- **Adattamento di Gumbel ai massimi** — Confrontare distribuzione empirica e modello stimato ai momenti. [Programma R](../../R/experiments/m14-gumbel.R); rotta del sito: `#laboratorio/m14-gumbel`.
- **Livelli di ritorno e incertezza bootstrap** — Esaminare l’incertezza di un livello raro condizionatamente al modello. [Programma R](../../R/experiments/m14-livelli-rari.R); rotta del sito: `#laboratorio/m14-livelli-rari`.

### Interpretare il rischio

- **Sensibilità alla forma della coda GEV** — Confrontare livelli rari sotto forme di coda differenti. [Programma R](../../R/experiments/m14-gev.R); rotta del sito: `#laboratorio/m14-gev`.
- **Tempo di ritorno e orizzonte temporale** — Distinguere probabilità annuale, attesa e rischio cumulato. [Programma R](../../R/experiments/m14-ritorno.R); rotta del sito: `#laboratorio/m14-ritorno`.
- **Pericolosità e conseguenze** — Calcolare la perdita attesa per classi di evento mutuamente esclusive. [Programma R](../../R/experiments/m14-conseguenze.R); rotta del sito: `#laboratorio/m14-conseguenze`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**16 slide · 7 figure · 3 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P09_R6.pdf) · [Codice R delle figure](../../materiali/R/P09_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P09_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Unità annuale e distribuzione dei massimi.
- Pagina 6: Stima di Gumbel e livello di ritorno.
- Pagina 11: Ricampionamento e incertezza condizionata.
- Pagina 14: Rischio temporale e sensibilità della coda.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P09_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
