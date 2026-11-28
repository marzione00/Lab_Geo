# M19 · Datazione radiometrica

Isocrone, regressione di York, MSWD e incertezza delle età.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

4 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M19`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Età modello e rapporto iniziale** · `#laboratorio/m19-modello` | Valutare come un errore sul rapporto iniziale 87Sr/86Sr sposta l’età calcolata da un solo campione, al variare del rapporto 87Rb/86Sr. | [R](../../R/experiments/m19-modello.R) |
| **Minimi quadrati ordinari e regressione di York** · `#laboratorio/m19-york` | Confrontare le età ottenute con i minimi quadrati ordinari e con la regressione di York quando anche il rapporto 87Rb/86Sr ha errori di misura. | [R](../../R/experiments/m19-york.R) |
| **MSWD con errori sottostimati** · `#laboratorio/m19-mswd` | Osservare la distribuzione della MSWD quando gli errori dichiarati sono corretti e quando sottostimano la dispersione reale. | [R](../../R/experiments/m19-mswd.R) |
| **Media pesata e dispersione geologica** · `#laboratorio/m19-media` | Valutare la media pesata di date di singoli cristalli quando le date hanno una dispersione reale oltre a quella analitica. | [R](../../R/experiments/m19-media.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Isocrona: 32 tappe.**

[Presentazione PDF](../../assets/lezioni/M19/M19_Isocrona.pdf) · [Progetto R della lezione](../../assets/lezioni/M19/Isocrona_M19_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M19_Isocrona/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M19`).

- Tappa 3: Il caso guida.
- Tappe 4–9: Il decadimento come orologio.
- Tappe 10–16: L’isocrona.
- Tappe 17–23: MSWD e dispersione in eccesso.
- Tappe 24–30: Incertezza e confronto delle età.
- Tappa 31: Sintesi.
- Tappa 32: Riferimenti.

## Dati

`lezioni/M19_Isocrona/dati/` contiene due file sintetici: `isocrone_v1.csv`, rapporti ⁸⁷Rb/⁸⁶Sr e ⁸⁷Sr/⁸⁶Sr con le incertezze di dieci campioni di un granito e otto di un filone; `date_v1.csv`, date U-Pb di quindici zirconi del granito. I file sono generati da `lezioni/M19_Isocrona/R/genera_dati.R`; le figure e i valori della presentazione da `R/M19_figure.R`, la regressione di York da `R/york.R`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione nel percorso. La lezione a tappe è in `content/lezioni/M19.json`, generata dai sorgenti in `lezioni/M19_Isocrona/` (scritti da `lezioni/Edizione_M17-M21/genera.py`); la spiegazione estesa delle tappe è in `content/lezioni/M19.md`.
