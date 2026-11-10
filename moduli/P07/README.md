# P07 · Terreno, pendenze e sintesi territoriali

Geometria raster, unità fisiche e ricampionamento di blocchi.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Ricostruisci grandezze morfometriche a partire da un raster, verificando unità, risoluzione e dominio valido.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo e i suoi dati rimangono nei materiali R6 descritti sotto.

### Verificare la griglia

- **Geometria di una griglia raster** — Collegare numero di celle, risoluzione e superficie. [Programma R](../../R/experiments/m12-griglia.R); rotta del sito: `#laboratorio/m12-griglia`.
- **Maschere, dominio e superficie valida** — Distinguere celle escluse e celle a valore nullo. [Programma R](../../R/experiments/m12-maschere.R); rotta del sito: `#laboratorio/m12-maschere`.

### Derivare e rappresentare

- **Gradiente, pendenza ed esposizione** — Ricostruire derivate da differenze centrate e unità metriche. [Programma R](../../R/experiments/m12-pendenza.R); rotta del sito: `#laboratorio/m12-pendenza`.
- **Illuminazione del rilievo** — Separare forma del terreno e condizioni di illuminazione. [Programma R](../../R/experiments/m12-hillshade.R); rotta del sito: `#laboratorio/m12-hillshade`.

### Valutare la sensibilità

- **Aggregazione e ricampionamento di una griglia** — Confrontare risoluzioni senza attribuire nuova informazione ai pixel interpolati. [Programma R](../../R/experiments/m12-ricampionamento.R); rotta del sito: `#laboratorio/m12-ricampionamento`.
- **Allineamento e ricampionamento fra griglie** — Valutare lo scarto introdotto da griglie con origine diversa. [Programma R](../../R/experiments/m12-allineamento.R); rotta del sito: `#laboratorio/m12-allineamento`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**17 slide · 7 figure · 3 diagrammi TikZ · 0 laboratori.**

[PDF del modulo](../../materiali/pdf/P07_R6.pdf) · [Codice R delle figure](../../materiali/R/P07_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/P07_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Geometria e orientamento del raster.
- Pagina 7: Gradiente e pendenza fisica.
- Pagina 11: Zone e unità della sintesi.
- Pagina 14: Ricampionamento e limiti della conclusione.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/P07_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.


## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
