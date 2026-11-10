# P10 · Un’analisi ricostruibile e verificabile

Dati immutati, funzioni, controlli numerici e storia delle modifiche.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Ricostruisci un’analisi verificabile, rendendo espliciti dati, dipendenze, criteri numerici e piano casuale.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Controllare i dati

- **Collegare tabelle senza moltiplicare le misure** — Verificare la cardinalità di un collegamento mediante una chiave. [Programma R](../../R/experiments/m02-join.R); rotta del sito: `#laboratorio/m02-join`.
- **Verificare una tabella analitica** — Controllare righe, chiavi e unità prima dell’analisi. [Programma R](../../R/experiments/m02-tabella.R); rotta del sito: `#laboratorio/m02-tabella`.

### Verificare le funzioni

- **Verificare una funzione prima dell’uso** — Sottoporre una funzione a casi validi e invalidi. [Programma R](../../R/experiments/m15-contratti.R); rotta del sito: `#laboratorio/m15-contratti`.
- **Identità e confronto numerico** — Scegliere una tolleranza coerente con la scala del problema. [Programma R](../../R/experiments/m15-tolleranze.R); rotta del sito: `#laboratorio/m15-tolleranze`.

### Conservare la provenienza

- **Integrità dei file e identità dei dati** — Confrontare contenuto numerico, rappresentazione testuale e impronta di un file. [Programma R](../../R/experiments/m15-integrita.R); rotta del sito: `#laboratorio/m15-integrita`.
- **Parametri, versioni e sensibilità** — Confrontare risultati prodotti da scelte analitiche tracciate. [Programma R](../../R/experiments/m15-provenienza.R); rotta del sito: `#laboratorio/m15-provenienza`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**16 slide · 3 figure · 5 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P10_R6.pdf) · [Codice R delle figure](../../materiali/R/P10_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P10_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Dati e trasformazioni dichiarate.
- Pagina 8: Prove del codice e integrità dei file.
- Pagina 13: Piani casuali, versioni e consegna.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P10_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
