# P02 · Foraminiferi, coppe e campagne

Copertura temporale, confronti appaiati e limiti di quattro repliche.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Ricostruisci un confronto fra campagne, distinguendo numerosità delle misure e numero delle unità indipendenti.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Delimitare il confronto

- **Definire la quantità di interesse**: Distinguere media delle misure e media delle unità geologiche. [Programma R](../../R/experiments/m01-estimando.R); rotta del sito: `#laboratorio/m01-estimando`.
- **Aggregazione e pesi delle osservazioni**: Confrontare media complessiva e media delle medie. [Programma R](../../R/experiments/m02-aggregazioni.R); rotta del sito: `#laboratorio/m02-aggregazioni`.

### Valutare l’incertezza

- **Definire un contrasto fra gruppi**: Collegare disegno e differenza di interesse. [Programma R](../../R/experiments/m06-contrasto.R); rotta del sito: `#laboratorio/m06-contrasto`.
- **Ricampionamento per stazioni**: Confrontare bootstrap delle misure e delle unità indipendenti. [Programma R](../../R/experiments/m05-ricampionamento.R); rotta del sito: `#laboratorio/m05-ricampionamento`.

### Preparare una nuova raccolta

- **Disegnare una campagna di misura**: Valutare la copertura di una raccolta su un territorio sintetico. [Programma R](../../R/experiments/m01-disegno.R); rotta del sito: `#laboratorio/m01-disegno`.
- **Confrontare campagne ripetute**: Valutare bias e dispersione di due disegni campionari. [Programma R](../../R/experiments/m01-confronto-disegni.R); rotta del sito: `#laboratorio/m01-confronto-disegni`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P02: 32 tappe.**

[Presentazione PDF](../../assets/lezioni/P02/P02_Foraminiferi.pdf) · [Progetto R della spedizione](../../assets/lezioni/P02/Spedizione_P02_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P02_Foraminiferi/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P02`).

- Tappa 3: Il caso guida.
- Tappe 4–6: Fonte e supporto delle osservazioni.
- Tappe 7–14: Copertura e definizione del confronto.
- Tappe 15–20: Incertezza con quattro unità.
- Tappe 21–23: Interpretazione e nuova raccolta.
- Tappe 24–30: Laboratori della spedizione.
- Tappa 31: Sintesi.
- Tappa 32: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P02_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P02.json`, generata dai sorgenti in `lezioni/P02_Foraminiferi/`.
