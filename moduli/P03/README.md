# P03 · Il Nilo: livelli e dipendenza temporale

Volumi annuali, contrasto fra periodi e covarianza HAC.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Esamina una variazione del livello di una serie idrologica, considerando il ruolo della dipendenza temporale.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Leggere la serie

- **Calendario e osservazioni mancanti** — Distinguere distanza temporale e posizione nella tabella. [Programma R](../../R/experiments/m09-calendario.R); rotta del sito: `#laboratorio/m09-calendario`.
- **Trend, stagionalità e media mobile** — Confrontare componenti note e stima mediante smoothing. [Programma R](../../R/experiments/m09-smoothing.R); rotta del sito: `#laboratorio/m09-smoothing`.

### Diagnosticare la dipendenza

- **Ritardi e autocorrelazione** — Collegare coppie temporali e dipendenza a un ritardo. [Programma R](../../R/experiments/m09-autocorrelazione.R); rotta del sito: `#laboratorio/m09-autocorrelazione`.
- **Trasformazione e differenziazione** — Valutare la rimozione di un trend e i suoi effetti sulla dipendenza. [Programma R](../../R/experiments/m09-differenze.R); rotta del sito: `#laboratorio/m09-differenze`.

### Sostenere la conclusione

- **Bootstrap a blocchi di una serie dipendente** — Confrontare ricampionamento individuale e ricampionamento di sequenze temporali. [Programma R](../../R/experiments/m05-blocchi.R); rotta del sito: `#laboratorio/m05-blocchi`.
- **Effetto, intervallo ed evidenza** — Ricostruire una conclusione quantitativa completa. [Programma R](../../R/experiments/m06-relazione.R); rotta del sito: `#laboratorio/m06-relazione`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**21 slide · 8 figure · 5 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P03_R6.pdf) · [Codice R delle figure](../../materiali/R/P03_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P03_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Serie storica e contrasto dichiarato.
- Pagina 8: Modello del livello e residui.
- Pagina 13: Covarianza HAC e analisi di sensibilità.
- Pagina 20: Interpretazione idrologica e consegna.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P03_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
