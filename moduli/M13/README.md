# M13 · Cronologie e archivi sedimentari

Modelli età–profondità, proxy e propagazione dell’incertezza.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

6 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M13`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Ancore cronologiche e convenzioni temporali** · `#laboratorio/m13-ancore` | Collegare profondità, età e riferimento temporale. | [R](../../R/experiments/m13-ancore.R) |
| **Interpolazione e tassi di accumulo** · `#laboratorio/m13-interpolazione` | Ricostruire una cronologia fra ancore e valutarne la pendenza. | [R](../../R/experiments/m13-interpolazione.R) |
| **Scenari cronologici e propagazione** · `#laboratorio/m13-incertezza` | Costruire cronologie perturbate conservando l’associazione fra età e profondità. | [R](../../R/experiments/m13-incertezza.R) |
| **Risoluzione temporale di un proxy** · `#laboratorio/m13-proxy` | Confrontare un campionamento uniforme in profondità con il suo supporto temporale. | [R](../../R/experiments/m13-proxy.R) |
| **Discontinuità e sensibilità della cronologia** · `#laboratorio/m13-hiatus` | Rappresentare un intervallo temporale privo di sedimentazione. | [R](../../R/experiments/m13-hiatus.R) |
| **Durate entro uno stesso scenario** · `#laboratorio/m13-durate` | Propagare la covarianza nella durata fra due eventi. | [R](../../R/experiments/m13-durate.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Strata: 63 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M13/M13_Strata.pdf) · [Progetto R della lezione](../../assets/lezioni/M13/Strata_M13_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M13_Strata/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M13`).

- Tappa 3: Il caso guida.
- Tappe 4–12: Archivio, ancore e convenzioni temporali.
- Tappe 13–21: Interpolazione e tassi di accumulo.
- Tappe 22–31: Scenari cronologici e propagazione.
- Tappe 32–40: Proxy e risoluzione temporale.
- Tappe 41–49: Discontinuità e sensibilità del modello.
- Tappe 50–58: Pendenze, durate ed eventi.
- Tappe 59–61: Consegna e studio autonomo.
- Tappa 62: Sintesi.
- Tappa 63: Riferimenti.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M13_N01 | Audit delle ancore età–profondità | [R](../../materiali/laboratori/M13/M13_N01.R) |
| M13_N02 | BP è riferito al 1950 | [R](../../materiali/laboratori/M13/M13_N02.R) |
| M13_N03 | Quanto sono lontane le ancore? | [R](../../materiali/laboratori/M13/M13_N03.R) |
| M13_N04 | Interpolazione lineare a tratti | [R](../../materiali/laboratori/M13/M13_N04.R) |
| M13_N05 | Fuori dalle ancore: rifiutare l’estrapolazione implicita | [R](../../materiali/laboratori/M13/M13_N05.R) |
| M13_N06 | Tassi: centimetri/anno, millimetri/anno | [R](../../materiali/laboratori/M13/M13_N06.R) |
| M13_N07 | Tassi medi: scegliere i pesi | [R](../../materiali/laboratori/M13/M13_N07.R) |
| M13_N08 | Scenari Monte Carlo senza riordinare le età | [R](../../materiali/laboratori/M13/M13_N08.R) |
| M13_N09 | Età a 100 cm: quantili degli scenari | [R](../../materiali/laboratori/M13/M13_N09.R) |
| M13_N10 | Lo stesso proxy, due assi | [R](../../materiali/laboratori/M13/M13_N10.R) |
| M13_N11 | Finestre di campioni e finestre di tempo | [R](../../materiali/laboratori/M13/M13_N11.R) |
| M13_N12 | Una griglia regolare non aggiunge misure | [R](../../materiali/laboratori/M13/M13_N12.R) |
| M13_N13 | Una lacuna di sedimentazione come scenario | [R](../../materiali/laboratori/M13/M13_N13.R) |
| M13_N14 | Inversione cronologica: trovare, non nascondere | [R](../../materiali/laboratori/M13/M13_N14.R) |
| M13_N15 | Retta globale contro interpolazione | [R](../../materiali/laboratori/M13/M13_N15.R) |
| M13_N16 | Togliere un’ancora interna per controllare la sensibilità | [R](../../materiali/laboratori/M13/M13_N16.R) |
| M13_N17 | Pendenza del proxy: per centimetro o per anno | [R](../../materiali/laboratori/M13/M13_N17.R) |
| M13_N18 | Durata di un intervallo e dipendenza delle età | [R](../../materiali/laboratori/M13/M13_N18.R) |
| M13_N19 | Una cronologia con metadati riproducibili | [R](../../materiali/laboratori/M13/M13_N19.R) |
| M13_N20 | Mini-indagine: quando si colloca il massimo del proxy? | [R](../../materiali/laboratori/M13/M13_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M13.json`, generata dai sorgenti in `lezioni/M13_Strata/`; la spiegazione estesa delle tappe è in `content/lezioni/M13.md`.
