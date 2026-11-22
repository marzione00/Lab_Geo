# M04 · Probabilità, variabilità e simulazione

Modelli del caso e propagazione dell’incertezza in R.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

9 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M04`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Eventi e frequenze relative** · `#laboratorio/m04-eventi` | Confrontare probabilità dichiarata e frequenza simulata. | [R](../../R/experiments/m04-eventi.R) |
| **Probabilità condizionata** · `#laboratorio/m04-condizionamento` | Distinguere probabilità marginale e probabilità entro un gruppo. | [R](../../R/experiments/m04-condizionamento.R) |
| **Distribuzione cumulativa e quantili** · `#laboratorio/m04-distribuzione` | Collegare densità, area e probabilità cumulativa. | [R](../../R/experiments/m04-distribuzione.R) |
| **Bernoulli e distribuzione binomiale** · `#laboratorio/m04-binomiale` | Collegare prove elementari e conteggio dei successi. | [R](../../R/experiments/m04-binomiale.R) |
| **Conteggi ed esposizione** · `#laboratorio/m04-poisson` | Distinguere tasso e numero atteso di eventi. | [R](../../R/experiments/m04-poisson.R) |
| **Standardizzazione e quantili normali** · `#laboratorio/m04-normale` | Collegare unità originali e unità standardizzate. | [R](../../R/experiments/m04-normale.R) |
| **Variabilità moltiplicativa** · `#laboratorio/m04-moltiplicazione` | Esaminare un prodotto di fattori positivi. | [R](../../R/experiments/m04-moltiplicazione.R) |
| **Precisione della simulazione Monte Carlo** · `#laboratorio/m04-monte-carlo` | Separare incertezza numerica e variabilità del fenomeno. | [R](../../R/experiments/m04-monte-carlo.R) |
| **Propagare incertezze correlate** · `#laboratorio/m04-propagazione` | Valutare l’incertezza di un rapporto fra misure positive. | [R](../../R/experiments/m04-propagazione.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Aurea: 81 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M04/Aurea_M04_probabilita_simulazione.pdf) · [Progetto R della lezione](../../assets/lezioni/M04/Aurea_M04_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M04_Aurea/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M04`).

- Tappe 3–8: Eventi e probabilità.
- Tappa 9: Laboratorio · eventi.
- Tappe 10–15: Condizionamento.
- Tappa 16: Laboratorio · condizionamento.
- Tappa 17: Condizionamento.
- Tappe 18–24: Variabili e distribuzioni.
- Tappa 25: Laboratorio · distribuzione.
- Tappe 26–33: Bernoulli e binomiale.
- Tappe 34–41: Poisson ed esposizione.
- Tappe 42–49: Distribuzione normale.
- Tappe 50–56: Variabilità moltiplicativa.
- Tappe 57–65: Monte Carlo.
- Tappe 66–76: Propagazione dell'incertezza.
- Tappe 77–81: Applicazioni e consegna.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M04_N01 | Evento e probabilità: una regola dichiarata | [R](../../materiali/laboratori/M04/M04_N01.R) |
| M04_N02 | Eventi complementari e soglie | [R](../../materiali/laboratori/M04/M04_N02.R) |
| M04_N03 | Una tabella per la probabilità condizionata | [R](../../materiali/laboratori/M04/M04_N03.R) |
| M04_N04 | Indipendenza: non basta una somiglianza visiva | [R](../../materiali/laboratori/M04/M04_N04.R) |
| M04_N05 | La binomiale: numero di successi in n prove | [R](../../materiali/laboratori/M04/M04_N05.R) |
| M04_N06 | Calcolare probabilità di eventi composti | [R](../../materiali/laboratori/M04/M04_N06.R) |
| M04_N07 | Verificare una probabilità con simulazioni | [R](../../materiali/laboratori/M04/M04_N07.R) |
| M04_N08 | Poisson: conteggi con esposizione dichiarata | [R](../../materiali/laboratori/M04/M04_N08.R) |
| M04_N09 | Una miscela può violare il modello semplice | [R](../../materiali/laboratori/M04/M04_N09.R) |
| M04_N10 | Un modello continuo non assegna probabilità ai singoli punti | [R](../../materiali/laboratori/M04/M04_N10.R) |
| M04_N11 | Standardizzare e ritrovare le probabilità | [R](../../materiali/laboratori/M04/M04_N11.R) |
| M04_N12 | Dati positivi e asimmetria | [R](../../materiali/laboratori/M04/M04_N12.R) |
| M04_N13 | Disegnare l’esperimento di incertezza | [R](../../materiali/laboratori/M04/M04_N13.R) |
| M04_N14 | Propagare l’incertezza con molte estrazioni | [R](../../materiali/laboratori/M04/M04_N14.R) |
| M04_N15 | Leggere la distribuzione del risultato | [R](../../materiali/laboratori/M04/M04_N15.R) |
| M04_N16 | Controllo con un’approssimazione analitica | [R](../../materiali/laboratori/M04/M04_N16.R) |
| M04_N17 | Che cosa cambia se gli errori sono correlati? | [R](../../materiali/laboratori/M04/M04_N17.R) |
| M04_N18 | Errore casuale e bias non sono la stessa cosa | [R](../../materiali/laboratori/M04/M04_N18.R) |
| M04_N19 | Laboratorio applicativo — Probabilità normale | [R](../../materiali/laboratori/M04/M04_N19.R) |
| M04_N20 | Laboratorio applicativo — Migliorare uno strumento | [R](../../materiali/laboratori/M04/M04_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M04.json`, generata dai sorgenti in `lezioni/M04_Aurea/`; la spiegazione estesa delle tappe è in `content/lezioni/M04.md`.
