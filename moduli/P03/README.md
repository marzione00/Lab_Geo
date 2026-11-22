# P03 · Il Nilo: livelli e dipendenza temporale

Volumi annuali, contrasto fra periodi e covarianza HAC.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Esamina una variazione del livello di una serie idrologica, considerando il ruolo della dipendenza temporale.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Leggere la serie

- **Calendario e osservazioni mancanti**: Distinguere distanza temporale e posizione nella tabella. [Programma R](../../R/experiments/m09-calendario.R); rotta del sito: `#laboratorio/m09-calendario`.
- **Trend, stagionalità e media mobile**: Confrontare componenti note e stima mediante smoothing. [Programma R](../../R/experiments/m09-smoothing.R); rotta del sito: `#laboratorio/m09-smoothing`.

### Diagnosticare la dipendenza

- **Ritardi e autocorrelazione**: Collegare coppie temporali e dipendenza a un ritardo. [Programma R](../../R/experiments/m09-autocorrelazione.R); rotta del sito: `#laboratorio/m09-autocorrelazione`.
- **Trasformazione e differenziazione**: Valutare la rimozione di un trend e i suoi effetti sulla dipendenza. [Programma R](../../R/experiments/m09-differenze.R); rotta del sito: `#laboratorio/m09-differenze`.

### Sostenere la conclusione

- **Bootstrap a blocchi di una serie dipendente**: Confrontare ricampionamento individuale e ricampionamento di sequenze temporali. [Programma R](../../R/experiments/m05-blocchi.R); rotta del sito: `#laboratorio/m05-blocchi`.
- **Effetto, intervallo ed evidenza**: Ricostruire una conclusione quantitativa completa. [Programma R](../../R/experiments/m06-relazione.R); rotta del sito: `#laboratorio/m06-relazione`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P03: 31 tappe.**

[Presentazione PDF](../../assets/lezioni/P03/P03_Nilo.pdf) · [Progetto R della spedizione](../../assets/lezioni/P03/Spedizione_P03_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P03_Nilo/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P03`).

- Tappa 3: Il caso guida.
- Tappe 4–8: Serie storica e contrasto dichiarato.
- Tappe 9–13: Modello del livello e residui.
- Tappe 14–20: Covarianza HAC e analisi di sensibilità.
- Tappe 21–22: Interpretazione idrologica e consegna.
- Tappe 23–29: Laboratori della spedizione.
- Tappa 30: Sintesi.
- Tappa 31: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P03_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P03.json`, generata dai sorgenti in `lezioni/P03_Nilo/`.
