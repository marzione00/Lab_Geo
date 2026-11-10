# P04 · Un geyser: associazione e previsione

Durata dell’eruzione, intervalli e valutazione su eventi separati.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Distingui previsione della durata media e previsione di un nuovo evento, conservando una porzione separata per la verifica.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Separare stima e verifica

- **Complessità e prestazione su nuovi dati** — Confrontare errore di adattamento e di previsione. [Programma R](../../R/experiments/m07-validazione.R); rotta del sito: `#laboratorio/m07-validazione`.
- **Dominio osservato ed estrapolazione** — Distinguere previsione entro e oltre il campo osservato. [Programma R](../../R/experiments/m07-dominio.R); rotta del sito: `#laboratorio/m07-dominio`.

### Costruire il modello

- **La geometria dei minimi quadrati** — Confrontare una retta proposta con la soluzione che minimizza gli scarti quadratici. [Programma R](../../R/experiments/m07-minimi-quadrati.R); rotta del sito: `#laboratorio/m07-minimi-quadrati`.
- **Leva e influenza di un’osservazione** — Distinguere distanza nel predittore e influenza sul modello. [Programma R](../../R/experiments/m07-influenza.R); rotta del sito: `#laboratorio/m07-influenza`.

### Interpretare le previsioni

- **Intervallo della media e di una nuova osservazione** — Separare incertezza della risposta media e variabilità di un evento futuro. [Programma R](../../R/experiments/m07-previsione.R); rotta del sito: `#laboratorio/m07-previsione`.
- **Effetto, intervallo ed evidenza** — Ricostruire una conclusione quantitativa completa. [Programma R](../../R/experiments/m06-relazione.R); rotta del sito: `#laboratorio/m06-relazione`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**21 slide · 9 figure · 5 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P04_R6.pdf) · [Codice R delle figure](../../materiali/R/P04_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P04_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Fonte, bersaglio e separazione dei dati.
- Pagina 7: Associazione nel campione di adattamento.
- Pagina 12: Incertezza della media e di un evento.
- Pagina 15: Valutazione su eventi separati.
- Pagina 20: Struttura interna e discussione.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P04_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
