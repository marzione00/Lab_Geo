# M15 · Riproducibilità e progetto di analisi

Dati, funzioni, controlli numerici e storia delle decisioni.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

6 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M15`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Dipendenze fra dati e risultati** · `#laboratorio/m15-dipendenze` | Seguire l’effetto di una modifica al dato di ingresso. | [R](../../R/experiments/m15-dipendenze.R) |
| **Identità e confronto numerico** · `#laboratorio/m15-tolleranze` | Scegliere una tolleranza coerente con la scala del problema. | [R](../../R/experiments/m15-tolleranze.R) |
| **Integrità dei file e identità dei dati** · `#laboratorio/m15-integrita` | Confrontare contenuto numerico, rappresentazione testuale e impronta di un file. | [R](../../R/experiments/m15-integrita.R) |
| **Verificare una funzione prima dell’uso** · `#laboratorio/m15-contratti` | Sottoporre una funzione a casi validi e invalidi. | [R](../../R/experiments/m15-contratti.R) |
| **Seme casuale e stato del generatore** · `#laboratorio/m15-casualita` | Riprodurre una sequenza dichiarando il piano casuale. | [R](../../R/experiments/m15-casualita.R) |
| **Parametri, versioni e sensibilità** · `#laboratorio/m15-provenienza` | Confrontare risultati prodotti da scelte analitiche tracciate. | [R](../../R/experiments/m15-provenienza.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Argenta: 58 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M15/M15_Argenta.pdf) · [Progetto R della lezione](../../assets/lezioni/M15/Argenta_M15_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M15_Argenta/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M15`).

- Tappa 3: Il caso guida.
- Tappe 4–11: Dati e dipendenze dell’analisi.
- Tappe 12–23: Identità e confronto numerico.
- Tappe 24–34: Funzioni e contratti di validità.
- Tappe 35–43: Casualità e ambiente di esecuzione.
- Tappe 44–56: Parametri, versioni e provenienza.
- Tappa 57: Sintesi.
- Tappa 58: Riferimenti.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M15_N01 | Separare dati grezzi e risultati | [R](../../materiali/laboratori/M15/M15_N01.R) |
| M15_N02 | Dizionario minimo verificabile | [R](../../materiali/laboratori/M15/M15_N02.R) |
| M15_N03 | Impronta del file: rilevare una modifica | [R](../../materiali/laboratori/M15/M15_N03.R) |
| M15_N04 | CSV di andata e ritorno | [R](../../materiali/laboratori/M15/M15_N04.R) |
| M15_N05 | Percorsi relativi, cartella corrente e progetto | [R](../../materiali/laboratori/M15/M15_N05.R) |
| M15_N06 | Registrare versione del runtime e pacchetti | [R](../../materiali/laboratori/M15/M15_N06.R) |
| M15_N07 | Un seme riproduce una sequenza nello stesso runtime | [R](../../materiali/laboratori/M15/M15_N07.R) |
| M15_N08 | Un piano casuale condiviso fra linguaggi | [R](../../materiali/laboratori/M15/M15_N08.R) |
| M15_N09 | Mancante, zero e campo vuoto nel CSV | [R](../../materiali/laboratori/M15/M15_N09.R) |
| M15_N10 | Validare gli input prima di calcolare | [R](../../materiali/laboratori/M15/M15_N10.R) |
| M15_N11 | Funzioni pure e input non modificati | [R](../../materiali/laboratori/M15/M15_N11.R) |
| M15_N12 | Test piccoli: valori noti e tolleranze | [R](../../materiali/laboratori/M15/M15_N12.R) |
| M15_N13 | Parametri in un file, non nascosti nello script | [R](../../materiali/laboratori/M15/M15_N13.R) |
| M15_N14 | Registro delle decisioni | [R](../../materiali/laboratori/M15/M15_N14.R) |
| M15_N15 | Git locale: creare un commit senza account | [R](../../materiali/laboratori/M15/M15_N15.R) |
| M15_N16 | Leggere un diff prima di registrare una modifica | [R](../../materiali/laboratori/M15/M15_N16.R) |
| M15_N17 | Ignorare file locali: non condividere segreti | [R](../../materiali/laboratori/M15/M15_N17.R) |
| M15_N18 | Payload di un’API: schema e archivio locale | [R](../../materiali/laboratori/M15/M15_N18.R) |
| M15_N19 | Manifest dei dati: lista e checksum | [R](../../materiali/laboratori/M15/M15_N19.R) |
| M15_N20 | Mini-pipeline deterministica da input a tabella | [R](../../materiali/laboratori/M15/M15_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M15.json`, generata dai sorgenti in `lezioni/M15_Argenta/`; la spiegazione estesa delle tappe è in `content/lezioni/M15.md`.
