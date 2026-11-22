# P04 · Un geyser: associazione e previsione

Durata dell’eruzione, intervalli e valutazione su eventi separati.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Distingui previsione della durata media e previsione di un nuovo evento, conservando una porzione separata per la verifica.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Separare stima e verifica

- **Complessità e prestazione su nuovi dati**: Confrontare errore di adattamento e di previsione. [Programma R](../../R/experiments/m07-validazione.R); rotta del sito: `#laboratorio/m07-validazione`.
- **Dominio osservato ed estrapolazione**: Distinguere previsione entro e oltre il campo osservato. [Programma R](../../R/experiments/m07-dominio.R); rotta del sito: `#laboratorio/m07-dominio`.

### Costruire il modello

- **La geometria dei minimi quadrati**: Confrontare una retta proposta con la soluzione che minimizza gli scarti quadratici. [Programma R](../../R/experiments/m07-minimi-quadrati.R); rotta del sito: `#laboratorio/m07-minimi-quadrati`.
- **Leva e influenza di un’osservazione**: Distinguere distanza nel predittore e influenza sul modello. [Programma R](../../R/experiments/m07-influenza.R); rotta del sito: `#laboratorio/m07-influenza`.

### Interpretare le previsioni

- **Intervallo della media e di una nuova osservazione**: Separare incertezza della risposta media e variabilità di un evento futuro. [Programma R](../../R/experiments/m07-previsione.R); rotta del sito: `#laboratorio/m07-previsione`.
- **Effetto, intervallo ed evidenza**: Ricostruire una conclusione quantitativa completa. [Programma R](../../R/experiments/m06-relazione.R); rotta del sito: `#laboratorio/m06-relazione`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P04: 31 tappe.**

[Presentazione PDF](../../assets/lezioni/P04/P04_Geyser.pdf) · [Progetto R della spedizione](../../assets/lezioni/P04/Spedizione_P04_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P04_Geyser/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P04`).

- Tappa 3: Il caso guida.
- Tappe 4–7: Fonte, bersaglio e separazione dei dati.
- Tappe 8–12: Associazione nel campione di adattamento.
- Tappe 13–15: Incertezza della media e di un evento.
- Tappe 16–20: Valutazione su eventi separati.
- Tappe 21–22: Struttura interna e discussione.
- Tappe 23–29: Laboratori della spedizione.
- Tappa 30: Sintesi.
- Tappa 31: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P04_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P04.json`, generata dai sorgenti in `lezioni/P04_Geyser/`.
