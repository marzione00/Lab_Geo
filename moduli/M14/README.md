# M14 · Estremi, pericolosità e rischio

Superamenti, tempi di ritorno e incertezza dei livelli rari.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

7 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M14`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Dalle osservazioni ai massimi annuali** · `#laboratorio/m14-massimi` | Esaminare la distribuzione dei massimi di blocchi indipendenti. | [R](../../R/experiments/m14-massimi.R) |
| **Tempo di ritorno e orizzonte temporale** · `#laboratorio/m14-ritorno` | Distinguere probabilità annuale, attesa e rischio cumulato. | [R](../../R/experiments/m14-ritorno.R) |
| **Adattamento di Gumbel ai massimi** · `#laboratorio/m14-gumbel` | Confrontare distribuzione empirica e modello stimato ai momenti. | [R](../../R/experiments/m14-gumbel.R) |
| **Livelli di ritorno e incertezza bootstrap** · `#laboratorio/m14-livelli-rari` | Esaminare l’incertezza di un livello raro condizionatamente al modello. | [R](../../R/experiments/m14-livelli-rari.R) |
| **Sensibilità alla forma della coda GEV** · `#laboratorio/m14-gev` | Confrontare livelli rari sotto forme di coda differenti. | [R](../../R/experiments/m14-gev.R) |
| **Superamenti e separazione degli episodi** · `#laboratorio/m14-episodi` | Distinguere giorni sopra soglia ed eventi temporali. | [R](../../R/experiments/m14-episodi.R) |
| **Pericolosità e conseguenze** · `#laboratorio/m14-conseguenze` | Calcolare la perdita attesa per classi di evento mutuamente esclusive. | [R](../../R/experiments/m14-conseguenze.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Ignis: 66 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M14/M14_Ignis.pdf) · [Progetto R della lezione](../../assets/lezioni/M14/Ignis_M14_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M14_Ignis/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M14`).

- Tappa 3: Il caso guida.
- Tappe 4–13: Massimi annuali e probabilità empiriche.
- Tappe 14–23: Ritorno, attesa e orizzonte temporale.
- Tappe 24–33: Modello Gumbel e verifica dell’adattamento.
- Tappe 34–44: Livelli rari e incertezza della stima.
- Tappe 45–50: Forma della coda e sensibilità GEV.
- Tappe 51–57: Superamenti giornalieri ed episodi.
- Tappe 58–64: Pericolosità, conseguenze e comunicazione.
- Tappa 65: Sintesi.
- Tappa 66: Riferimenti.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M14_N01 | Audit dei massimi annuali | [R](../../materiali/laboratori/M14/M14_N01.R) |
| M14_N02 | Posizioni empiriche di superamento | [R](../../materiali/laboratori/M14/M14_N02.R) |
| M14_N03 | CDF e probabilità di superamento | [R](../../materiali/laboratori/M14/M14_N03.R) |
| M14_N04 | Tempo di ritorno non significa appuntamento | [R](../../materiali/laboratori/M14/M14_N04.R) |
| M14_N05 | Probabilità durante una vita utile | [R](../../materiali/laboratori/M14/M14_N05.R) |
| M14_N06 | Simulare i tempi di attesa geometrici | [R](../../materiali/laboratori/M14/M14_N06.R) |
| M14_N07 | Quantili empirici e supporto osservato | [R](../../materiali/laboratori/M14/M14_N07.R) |
| M14_N08 | Gumbel: stima dei parametri con i momenti | [R](../../materiali/laboratori/M14/M14_N08.R) |
| M14_N09 | CDF e quantile Gumbel: controllo inverso | [R](../../materiali/laboratori/M14/M14_N09.R) |
| M14_N10 | QQ plot: dove il modello descrive peggio? | [R](../../materiali/laboratori/M14/M14_N10.R) |
| M14_N11 | Livelli di ritorno e distanza dall’osservato | [R](../../materiali/laboratori/M14/M14_N11.R) |
| M14_N12 | Bootstrap dei massimi annuali | [R](../../materiali/laboratori/M14/M14_N12.R) |
| M14_N13 | Lunghezza del record e stabilità della stima | [R](../../materiali/laboratori/M14/M14_N13.R) |
| M14_N14 | Quanto conta il massimo isolato? | [R](../../materiali/laboratori/M14/M14_N14.R) |
| M14_N15 | Due periodi: descrivere prima di attribuire | [R](../../materiali/laboratori/M14/M14_N15.R) |
| M14_N16 | Forma della GEV: una sensibilità, non un fit | [R](../../materiali/laboratori/M14/M14_N16.R) |
| M14_N17 | Superamenti giornalieri e numero di episodi | [R](../../materiali/laboratori/M14/M14_N17.R) |
| M14_N18 | Declustering di sequenze consecutive | [R](../../materiali/laboratori/M14/M14_N18.R) |
| M14_N19 | Pericolosità ed esposizione: perdita attesa di scenario | [R](../../materiali/laboratori/M14/M14_N19.R) |
| M14_N20 | Relazione finale: livello, metodo e condizioni | [R](../../materiali/laboratori/M14/M14_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M14.json`, generata dai sorgenti in `lezioni/M14_Ignis/`; la spiegazione estesa delle tappe è in `content/lezioni/M14.md`.
