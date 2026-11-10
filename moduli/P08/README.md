# P08 · Collocare nel tempo il massimo di un proxy

Ancore cronologiche, propagazione dell’incertezza e discontinuità sedimentarie.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Costruisci una cronologia di archivio e segui la propagazione delle incertezze nella datazione di un evento.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Stabilire le ancore

- **Ancore cronologiche e convenzioni temporali** — Collegare profondità, età e riferimento temporale. [Programma R](../../R/experiments/m13-ancore.R); rotta del sito: `#laboratorio/m13-ancore`.
- **Interpolazione e tassi di accumulo** — Ricostruire una cronologia fra ancore e valutarne la pendenza. [Programma R](../../R/experiments/m13-interpolazione.R); rotta del sito: `#laboratorio/m13-interpolazione`.

### Propagare l’incertezza

- **Scenari cronologici e propagazione** — Costruire cronologie perturbate conservando l’associazione fra età e profondità. [Programma R](../../R/experiments/m13-incertezza.R); rotta del sito: `#laboratorio/m13-incertezza`.
- **Durate entro uno stesso scenario** — Propagare la covarianza nella durata fra due eventi. [Programma R](../../R/experiments/m13-durate.R); rotta del sito: `#laboratorio/m13-durate`.

### Valutare interpretazioni alternative

- **Risoluzione temporale di un proxy** — Confrontare un campionamento uniforme in profondità con il suo supporto temporale. [Programma R](../../R/experiments/m13-proxy.R); rotta del sito: `#laboratorio/m13-proxy`.
- **Discontinuità e sensibilità della cronologia** — Rappresentare un intervallo temporale privo di sedimentazione. [Programma R](../../R/experiments/m13-hiatus.R); rotta del sito: `#laboratorio/m13-hiatus`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**18 slide · 8 figure · 3 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P08_R6.pdf) · [Codice R delle figure](../../materiali/R/P08_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P08_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Ancore e interpolazione cronologica.
- Pagina 8: Scenari di incertezza cronologica.
- Pagina 12: Massimo osservato e interpretazione temporale.
- Pagina 16: Hiatus e conclusione condizionata.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P08_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
