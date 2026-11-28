# M17 · Dati composizionali

Chiusura, log-rapporti e geometria del simplesso.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

4 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M17`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Chiusura e correlazione spuria** · `#laboratorio/m17-chiusura` | Osservare le correlazioni che la chiusura a cento introduce fra parti generate indipendenti. | [R](../../R/experiments/m17-chiusura.R) |
| **Distanza euclidea e distanza di Aitchison** · `#laboratorio/m17-distanze` | Confrontare l’effetto dello stesso spostamento assoluto su una parte minore e su una parte maggiore. | [R](../../R/experiments/m17-distanze.R) |
| **Media aritmetica e centro composizionale** · `#laboratorio/m17-centro` | Confrontare media aritmetica e media geometrica chiusa quando una parte è piccola e dispersa. | [R](../../R/experiments/m17-centro.R) |
| **Valori sotto il limite e sostituzione moltiplicativa** · `#laboratorio/m17-zeri` | Valutare come la sostituzione dei valori sotto il limite di rivelabilità sposta la media di un log-rapporto. | [R](../../R/experiments/m17-zeri.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Simplex: 32 tappe.**

[Presentazione PDF](../../assets/lezioni/M17/M17_Simplex.pdf) · [Progetto R della lezione](../../assets/lezioni/M17/Simplex_M17_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M17_Simplex/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M17`).

- Tappa 3: Il caso guida.
- Tappe 4–10: La chiusura e i suoi effetti.
- Tappe 11–17: Rapporti logaritmici.
- Tappe 18–23: Descrivere un insieme di composizioni.
- Tappe 24–30: Zeri, limiti di rivelabilità e modelli.
- Tappa 31: Sintesi.
- Tappa 32: Riferimenti.

## Dati

`lezioni/M17_Simplex/dati/composizioni_v1.csv` contiene 144 composizioni sintetiche a sei parti (SiO₂, Al₂O₃, CaO, MgO, FeO e una parte residua) di 18 stazioni e tre litologie, con la densità. Il file è generato da `lezioni/M17_Simplex/R/genera_dati.R`; le figure e i valori della presentazione da `R/M17_figure.R`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione nel percorso. La lezione a tappe è in `content/lezioni/M17.json`, generata dai sorgenti in `lezioni/M17_Simplex/` (scritti da `lezioni/Edizione_M17-M21/genera.py`); la spiegazione estesa delle tappe è in `content/lezioni/M17.md`.
