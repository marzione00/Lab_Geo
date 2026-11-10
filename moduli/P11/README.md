# P11 · Classificare nuove stazioni sintetiche

Separazione dei dati, standardizzazione e classificatore dei centroidi.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Valuta un classificatore su nuove stazioni, distinguendo geometria, probabilità previste e decisioni operative.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Definire il trasferimento

- **Bersaglio predittivo e nuove stazioni** — Confrontare predizione di misure e trasferimento a nuove unità. [Programma R](../../R/experiments/m16-bersaglio.R); rotta del sito: `#laboratorio/m16-bersaglio`.
- **Standardizzazione e confine decisionale** — Esaminare un classificatore a centroidi nella metrica scelta. [Programma R](../../R/experiments/m16-geometria.R); rotta del sito: `#laboratorio/m16-geometria`.

### Selezionare e addestrare

- **Selezione dei predittori e contaminazione** — Valutare la selezione di variabili su puro rumore. [Programma R](../../R/experiments/m16-selezione.R); rotta del sito: `#laboratorio/m16-selezione`.
- **Alberi e aggregazione di classificatori** — Confrontare un albero con un insieme di alberi su campioni bootstrap. [Programma R](../../R/experiments/m16-alberi.R); rotta del sito: `#laboratorio/m16-alberi`.

### Verificare probabilità e decisioni

- **Soglia, discriminazione e calibrazione** — Separare probabilità previste e decisione binaria. [Programma R](../../R/experiments/m16-metriche.R); rotta del sito: `#laboratorio/m16-metriche`.
- **Trasferibilità e cambiamento della relazione** — Valutare un modello su una popolazione differente. [Programma R](../../R/experiments/m16-trasferimento.R); rotta del sito: `#laboratorio/m16-trasferimento`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**17 slide · 6 figure · 4 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P11_R6.pdf) · [Codice R delle figure](../../materiali/R/P11_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P11_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Bersaglio e protocollo di valutazione.
- Pagina 7: Geometria standardizzata e centroidi.
- Pagina 12: Prestazione e limiti dell’interpretazione.
- Pagina 16: Scheda del modello e consegna.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P11_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
