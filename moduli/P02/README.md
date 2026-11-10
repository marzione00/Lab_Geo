# P02 · Foraminiferi, coppe e campagne

Copertura temporale, confronti appaiati e limiti di quattro repliche.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Ricostruisci un confronto fra campagne, distinguendo numerosità delle misure e numero delle unità indipendenti.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Delimitare il confronto

- **Definire la quantità di interesse** — Distinguere media delle misure e media delle unità geologiche. [Programma R](../../R/experiments/m01-estimando.R); rotta del sito: `#laboratorio/m01-estimando`.
- **Aggregazione e pesi delle osservazioni** — Confrontare media complessiva e media delle medie. [Programma R](../../R/experiments/m02-aggregazioni.R); rotta del sito: `#laboratorio/m02-aggregazioni`.

### Valutare l’incertezza

- **Definire un contrasto fra gruppi** — Collegare disegno e differenza di interesse. [Programma R](../../R/experiments/m06-contrasto.R); rotta del sito: `#laboratorio/m06-contrasto`.
- **Ricampionamento per stazioni** — Confrontare bootstrap delle misure e delle unità indipendenti. [Programma R](../../R/experiments/m05-ricampionamento.R); rotta del sito: `#laboratorio/m05-ricampionamento`.

### Preparare una nuova raccolta

- **Disegnare una campagna di misura** — Valutare la copertura di una raccolta su un territorio sintetico. [Programma R](../../R/experiments/m01-disegno.R); rotta del sito: `#laboratorio/m01-disegno`.
- **Confrontare campagne ripetute** — Valutare bias e dispersione di due disegni campionari. [Programma R](../../R/experiments/m01-confronto-disegni.R); rotta del sito: `#laboratorio/m01-confronto-disegni`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**22 slide · 8 figure · 6 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P02_R6.pdf) · [Codice R delle figure](../../materiali/R/P02_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P02_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Fonte e supporto delle osservazioni.
- Pagina 6: Copertura e definizione del confronto.
- Pagina 14: Incertezza con quattro unità.
- Pagina 20: Interpretazione e nuova raccolta.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P02_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
