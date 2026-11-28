# M20 · Modelli lineari generalizzati

Poisson, offset, sovradispersione e regressione logistica.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

4 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M20`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Retta e modello di Poisson per i conteggi** · `#laboratorio/m20-lineare` | Confrontare la retta dei minimi quadrati e il modello di Poisson con legame logaritmico su conteggi che crescono in modo esponenziale con un predittore. | [R](../../R/experiments/m20-lineare.R) |
| **Offset e superfici diverse** · `#laboratorio/m20-offset` | Valutare la stima del rapporto di tasso quando le unità hanno superfici diverse e la superficie dipende dal predittore. | [R](../../R/experiments/m20-offset.R) |
| **Sovradispersione e copertura degli intervalli** · `#laboratorio/m20-dispersione` | Misurare quanto spesso l’intervallo di confidenza del modello di Poisson contiene il valore vero quando i conteggi sono sovradispersi. | [R](../../R/experiments/m20-dispersione.R) |
| **Punti contati e variabilità fra stazioni** · `#laboratorio/m20-punti` | Valutare quanto il numero di punti contati per sezione migliora la stima della pendenza logistica quando le stazioni differiscono fra loro. | [R](../../R/experiments/m20-punti.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Numerus: 32 tappe.**

[Presentazione PDF](../../assets/lezioni/M20/M20_Numerus.pdf) · [Progetto R della lezione](../../assets/lezioni/M20/Numerus_M20_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M20_Numerus/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M20`).

- Tappa 3: Il caso guida.
- Tappe 4–9: Conteggi e regressione lineare.
- Tappe 10–16: Il modello di Poisson.
- Tappe 17–23: Sovradispersione.
- Tappe 24–30: Proporzioni e regressione logistica.
- Tappa 31: Sintesi.
- Tappa 32: Riferimenti.

## Dati

`lezioni/M20_Numerus/dati/` contiene due file sintetici: `frane_v1.csv`, numero di frane, superficie, pendenza media e litologia di novantasei celle di un bacino; `conteggi_v1.csv`, punti contati (fra 250 e 400) e punti di feldspato in trentasei sezioni sottili di dodici stazioni lungo un percorso di trasporto. I file sono generati da `lezioni/M20_Numerus/R/genera_dati.R`; le figure e i valori della presentazione da `R/M20_figure.R`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione nel percorso. La lezione a tappe è in `content/lezioni/M20.json`, generata dai sorgenti in `lezioni/M20_Numerus/` (scritti da `lezioni/Edizione_M17-M21/genera.py`); la spiegazione estesa delle tappe è in `content/lezioni/M20.md`.
