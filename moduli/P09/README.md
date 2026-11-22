# P09 · Un livello raro e la sua incertezza

Massimi annuali, distribuzione di Gumbel e rischio su un orizzonte temporale.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Stima un livello raro e discuti quanto la conclusione dipenda dalla lunghezza del record e dalla forma della coda.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Definire l’evento

- **Dalle osservazioni ai massimi annuali**: Esaminare la distribuzione dei massimi di blocchi indipendenti. [Programma R](../../R/experiments/m14-massimi.R); rotta del sito: `#laboratorio/m14-massimi`.
- **Superamenti e separazione degli episodi**: Distinguere giorni sopra soglia ed eventi temporali. [Programma R](../../R/experiments/m14-episodi.R); rotta del sito: `#laboratorio/m14-episodi`.

### Stimare e ricampionare

- **Adattamento di Gumbel ai massimi**: Confrontare distribuzione empirica e modello stimato ai momenti. [Programma R](../../R/experiments/m14-gumbel.R); rotta del sito: `#laboratorio/m14-gumbel`.
- **Livelli di ritorno e incertezza bootstrap**: Esaminare l’incertezza di un livello raro condizionatamente al modello. [Programma R](../../R/experiments/m14-livelli-rari.R); rotta del sito: `#laboratorio/m14-livelli-rari`.

### Interpretare il rischio

- **Sensibilità alla forma della coda GEV**: Confrontare livelli rari sotto forme di coda differenti. [Programma R](../../R/experiments/m14-gev.R); rotta del sito: `#laboratorio/m14-gev`.
- **Tempo di ritorno e orizzonte temporale**: Distinguere probabilità annuale, attesa e rischio cumulato. [Programma R](../../R/experiments/m14-ritorno.R); rotta del sito: `#laboratorio/m14-ritorno`.
- **Pericolosità e conseguenze**: Calcolare la perdita attesa per classi di evento mutuamente esclusive. [Programma R](../../R/experiments/m14-conseguenze.R); rotta del sito: `#laboratorio/m14-conseguenze`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P09: 26 tappe.**

[Presentazione PDF](../../assets/lezioni/P09/P09_Livelli.pdf) · [Progetto R della spedizione](../../assets/lezioni/P09/Spedizione_P09_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P09_Livelli/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P09`).

- Tappa 3: Il caso guida.
- Tappe 4–6: Unità annuale e distribuzione dei massimi.
- Tappe 7–11: Stima di gumbel e livello di ritorno.
- Tappe 12–14: Ricampionamento e incertezza condizionata.
- Tappe 15–17: Rischio temporale e sensibilità della coda.
- Tappe 18–24: Laboratori della spedizione.
- Tappa 25: Sintesi.
- Tappa 26: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P09_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P09.json`, generata dai sorgenti in `lezioni/P09_Livelli/`.
