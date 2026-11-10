# P05 · CO₂: tendenza e calendario stagionale

Medie mensili derivate, dipendenza residua e forma del trend.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Separa variazioni stagionali e andamento di lungo periodo in una serie ambientale, verificando calendario e dipendenza.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Conservare il tempo

- **Calendario e osservazioni mancanti** — Distinguere distanza temporale e posizione nella tabella. [Programma R](../../R/experiments/m09-calendario.R); rotta del sito: `#laboratorio/m09-calendario`.
- **Risoluzione temporale e copertura** — Esaminare gli effetti dell’aggregazione di una serie. [Programma R](../../R/experiments/m09-aggregazione.R); rotta del sito: `#laboratorio/m09-aggregazione`.

### Separare le componenti

- **Trend, stagionalità e media mobile** — Confrontare componenti note e stima mediante smoothing. [Programma R](../../R/experiments/m09-smoothing.R); rotta del sito: `#laboratorio/m09-smoothing`.
- **Trasformazione e differenziazione** — Valutare la rimozione di un trend e i suoi effetti sulla dipendenza. [Programma R](../../R/experiments/m09-differenze.R); rotta del sito: `#laboratorio/m09-differenze`.

### Confrontare previsioni

- **Previsioni di riferimento e valutazione temporale** — Confrontare media, ultimo valore e riferimento stagionale. [Programma R](../../R/experiments/m10-riferimenti.R); rotta del sito: `#laboratorio/m10-riferimenti`.
- **Struttura ARIMA e stagionalità** — Confrontare specificazioni temporali sul medesimo campione. [Programma R](../../R/experiments/m10-arima.R); rotta del sito: `#laboratorio/m10-arima`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**22 slide · 10 figure · 5 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P05_R6.pdf) · [Codice R delle figure](../../materiali/R/P05_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P05_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Provenienza e aggregazione della serie.
- Pagina 8: Scale temporali e modello della media.
- Pagina 14: Dipendenza e incertezza della pendenza.
- Pagina 19: Curvatura, interpretazione e consegna.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P05_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
