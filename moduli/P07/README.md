# P07 · Terreno, pendenze e sintesi territoriali

Geometria raster, unità fisiche e ricampionamento di blocchi.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Ricostruisci grandezze morfometriche a partire da un raster, verificando unità, risoluzione e dominio valido.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Verificare la griglia

- **Geometria di una griglia raster**: Collegare numero di celle, risoluzione e superficie. [Programma R](../../R/experiments/m12-griglia.R); rotta del sito: `#laboratorio/m12-griglia`.
- **Maschere, dominio e superficie valida**: Distinguere celle escluse e celle a valore nullo. [Programma R](../../R/experiments/m12-maschere.R); rotta del sito: `#laboratorio/m12-maschere`.

### Derivare e rappresentare

- **Gradiente, pendenza ed esposizione**: Ricostruire derivate da differenze centrate e unità metriche. [Programma R](../../R/experiments/m12-pendenza.R); rotta del sito: `#laboratorio/m12-pendenza`.
- **Illuminazione del rilievo**: Separare forma del terreno e condizioni di illuminazione. [Programma R](../../R/experiments/m12-hillshade.R); rotta del sito: `#laboratorio/m12-hillshade`.

### Valutare la sensibilità

- **Aggregazione e ricampionamento di una griglia**: Confrontare risoluzioni senza attribuire nuova informazione ai pixel interpolati. [Programma R](../../R/experiments/m12-ricampionamento.R); rotta del sito: `#laboratorio/m12-ricampionamento`.
- **Allineamento e ricampionamento fra griglie**: Valutare lo scarto introdotto da griglie con origine diversa. [Programma R](../../R/experiments/m12-allineamento.R); rotta del sito: `#laboratorio/m12-allineamento`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P07: 27 tappe.**

[Presentazione PDF](../../assets/lezioni/P07/P07_Terreno.pdf) · [Progetto R della spedizione](../../assets/lezioni/P07/Spedizione_P07_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P07_Terreno/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P07`).

- Tappa 3: Il caso guida.
- Tappe 4–7: Geometria e orientamento del raster.
- Tappe 8–11: Gradiente e pendenza fisica.
- Tappe 12–14: Zone e unità della sintesi.
- Tappe 15–18: Ricampionamento e limiti della conclusione.
- Tappe 19–25: Laboratori della spedizione.
- Tappa 26: Sintesi.
- Tappa 27: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P07_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P07.json`, generata dai sorgenti in `lezioni/P07_Terreno/`.
