# P05 · CO₂: tendenza e calendario stagionale

Medie mensili derivate, dipendenza residua e forma del trend.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Separa variazioni stagionali e andamento di lungo periodo in una serie ambientale, verificando calendario e dipendenza.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Conservare il tempo

- **Calendario e osservazioni mancanti**: Distinguere distanza temporale e posizione nella tabella. [Programma R](../../R/experiments/m09-calendario.R); rotta del sito: `#laboratorio/m09-calendario`.
- **Risoluzione temporale e copertura**: Esaminare gli effetti dell’aggregazione di una serie. [Programma R](../../R/experiments/m09-aggregazione.R); rotta del sito: `#laboratorio/m09-aggregazione`.

### Separare le componenti

- **Trend, stagionalità e media mobile**: Confrontare componenti note e stima mediante smoothing. [Programma R](../../R/experiments/m09-smoothing.R); rotta del sito: `#laboratorio/m09-smoothing`.
- **Trasformazione e differenziazione**: Valutare la rimozione di un trend e i suoi effetti sulla dipendenza. [Programma R](../../R/experiments/m09-differenze.R); rotta del sito: `#laboratorio/m09-differenze`.

### Confrontare previsioni

- **Previsioni di riferimento e valutazione temporale**: Confrontare media, ultimo valore e riferimento stagionale. [Programma R](../../R/experiments/m10-riferimenti.R); rotta del sito: `#laboratorio/m10-riferimenti`.
- **Struttura ARIMA e stagionalità**: Confrontare specificazioni temporali sul medesimo campione. [Programma R](../../R/experiments/m10-arima.R); rotta del sito: `#laboratorio/m10-arima`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P05: 32 tappe.**

[Presentazione PDF](../../assets/lezioni/P05/P05_CO2.pdf) · [Progetto R della spedizione](../../assets/lezioni/P05/Spedizione_P05_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P05_CO2/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P05`).

- Tappa 3: Il caso guida.
- Tappe 4–8: Provenienza e aggregazione della serie.
- Tappe 9–14: Scale temporali e modello della media.
- Tappe 15–19: Dipendenza e incertezza della pendenza.
- Tappe 20–23: Curvatura, interpretazione e consegna.
- Tappe 24–30: Laboratori della spedizione.
- Tappa 31: Sintesi.
- Tappa 32: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P05_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P05.json`, generata dai sorgenti in `lezioni/P05_CO2/`.
