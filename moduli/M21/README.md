# M21 · Inferenza bayesiana

Griglie, distribuzioni coniugate, distribuzioni a priori e algoritmo di Metropolis.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

4 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M21`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Distribuzione a posteriori e lunghezza del registro** · `#laboratorio/m21-registro` | Osservare come la distribuzione a posteriori del tasso eruttivo si restringe e si allontana dalla distribuzione a priori quando il registro storico si allunga. | [R](../../R/experiments/m21-registro.R) |
| **Intervalli per un tasso con pochi eventi** · `#laboratorio/m21-copertura` | Confrontare la copertura dell’intervallo di Wald, dell’intervallo di credibilità con la distribuzione a priori di Jeffreys e dell’intervallo esatto quando il numero atteso di eventi è piccolo. | [R](../../R/experiments/m21-copertura.R) |
| **Distribuzione a priori in conflitto con i dati** · `#laboratorio/m21-priori` | Valutare l’effetto di una distribuzione a priori centrata lontano dal tasso vero sulla media a posteriori e sulla copertura degli intervalli, e verificare se un controllo predittivo segnala il conflitto. | [R](../../R/experiments/m21-priori.R) |
| **Passo della proposta e mescolamento della catena** · `#laboratorio/m21-metropolis` | Osservare come la deviazione standard della proposta dell’algoritmo di Metropolis cambia il tasso di accettazione, l’autocorrelazione della catena e la precisione della media a posteriori. | [R](../../R/experiments/m21-metropolis.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Credentia: 32 tappe.**

[Presentazione PDF](../../assets/lezioni/M21/M21_Credentia.pdf) · [Progetto R della lezione](../../assets/lezioni/M21/Credentia_M21_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M21_Credentia/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M21`).

- Tappa 3: Il caso guida.
- Tappe 4–9: Il teorema di Bayes.
- Tappe 10–16: Coniugate e intervalli di credibilità.
- Tappe 17–23: Sensibilità alla distribuzione a priori.
- Tappe 24–30: Monte Carlo a catena di Markov.
- Tappa 31: Sintesi.
- Tappa 32: Riferimenti.

## Dati

`lezioni/M21_Credentia/dati/` contiene due file sintetici: `eruzioni_v1.csv`, anno e tipo, effusivo o esplosivo, delle nove eruzioni di un vulcano fra il 1650 e il 2025; `analoghi_v1.csv`, anni di osservazione, eruzioni ed eruzioni esplosive di quattordici vulcani analoghi. I file sono generati da `lezioni/M21_Credentia/R/genera_dati.R`; le figure e i valori della presentazione da `R/M21_figure.R`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione nel percorso. La lezione a tappe è in `content/lezioni/M21.json`, generata dai sorgenti in `lezioni/M21_Credentia/` (scritti da `lezioni/Edizione_M17-M21/genera.py`); la spiegazione estesa delle tappe è in `content/lezioni/M21.md`.
