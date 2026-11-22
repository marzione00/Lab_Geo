# M07 · Relazioni tra variabili e regressione

Dalla geometria dei minimi quadrati alla valutazione predittiva.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

8 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M07`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Dominio osservato ed estrapolazione** · `#laboratorio/m07-dominio` | Distinguere previsione entro e oltre il campo osservato. | [R](../../R/experiments/m07-dominio.R) |
| **Correlazione e restrizione del campo** · `#laboratorio/m07-correlazione` | Osservare l’effetto del dominio dei predittori sulla correlazione. | [R](../../R/experiments/m07-correlazione.R) |
| **La geometria dei minimi quadrati** · `#laboratorio/m07-minimi-quadrati` | Confrontare una retta proposta con la soluzione che minimizza gli scarti quadratici. | [R](../../R/experiments/m07-minimi-quadrati.R) |
| **Intervallo della media e di una nuova osservazione** · `#laboratorio/m07-previsione` | Separare incertezza della risposta media e variabilità di un evento futuro. | [R](../../R/experiments/m07-previsione.R) |
| **Leva e influenza di un’osservazione** · `#laboratorio/m07-influenza` | Distinguere distanza nel predittore e influenza sul modello. | [R](../../R/experiments/m07-influenza.R) |
| **Predittori multipli e interazione** · `#laboratorio/m07-interazioni` | Osservare una pendenza che dipende dal gruppo. | [R](../../R/experiments/m07-interazioni.R) |
| **Dalla risposta binaria alla probabilità** · `#laboratorio/m07-logistica` | Collegare predittore lineare, probabilità e osservazioni binarie. | [R](../../R/experiments/m07-logistica.R) |
| **Complessità e prestazione su nuovi dati** · `#laboratorio/m07-validazione` | Confrontare errore di adattamento e di previsione. | [R](../../R/experiments/m07-validazione.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Annula: 100 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M07/Annula_M07_regressione.pdf) · [Progetto R della lezione](../../assets/lezioni/M07/Annula_M07_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M07_Annula/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M07`).

- Tappe 14–29: II · Modello lineare.
- Tappe 30–41: III · Incertezza e previsione.
- Tappe 42–55: IV · Diagnostica.
- Tappe 56–70: V · Predittori e interazioni.
- Tappe 71–81: VI · Risposte binarie.
- Tappe 82–93: VII · Valutazione su nuovi dati.
- Tappe 94–100: VIII · Un’analisi completa.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M07_N01 | Definire risposta e predittore | [R](../../materiali/laboratori/M07/M07_N01.R) |
| M07_N02 | Pearson e Spearman: quale relazione riassumono? | [R](../../materiali/laboratori/M07/M07_N02.R) |
| M07_N03 | La retta dei minimi quadrati a mano | [R](../../materiali/laboratori/M07/M07_N03.R) |
| M07_N04 | Stimare con lm e leggere i coefficienti | [R](../../materiali/laboratori/M07/M07_N04.R) |
| M07_N05 | R² ed errore residuo non sono la stessa cosa | [R](../../materiali/laboratori/M07/M07_N05.R) |
| M07_N06 | Media prevista e nuovo individuo | [R](../../materiali/laboratori/M07/M07_N06.R) |
| M07_N07 | Residui contro valori stimati | [R](../../materiali/laboratori/M07/M07_N07.R) |
| M07_N08 | Forma dei residui e informazione di gruppo | [R](../../materiali/laboratori/M07/M07_N08.R) |
| M07_N09 | Influenza: un punto può cambiare la stima | [R](../../materiali/laboratori/M07/M07_N09.R) |
| M07_N10 | Il protocollo prima di guardare gli errori | [R](../../materiali/laboratori/M07/M07_N10.R) |
| M07_N11 | Una previsione di riferimento | [R](../../materiali/laboratori/M07/M07_N11.R) |
| M07_N12 | Validazione interna: dividere soltanto il training | [R](../../materiali/laboratori/M07/M07_N12.R) |
| M07_N13 | Ristimare e valutare una volta sul test | [R](../../materiali/laboratori/M07/M07_N13.R) |
| M07_N14 | Errore di training e generalizzazione | [R](../../materiali/laboratori/M07/M07_N14.R) |
| M07_N15 | Trasformazioni stimate sul training | [R](../../materiali/laboratori/M07/M07_N15.R) |
| M07_N16 | Approfondimento: risposta binaria e regressione logistica | [R](../../materiali/laboratori/M07/M07_N16.R) |
| M07_N17 | Probabilità e classi: due valutazioni diverse | [R](../../materiali/laboratori/M07/M07_N17.R) |
| M07_N18 | Calibrazione descrittiva e pochi dati | [R](../../materiali/laboratori/M07/M07_N18.R) |
| M07_N19 | Laboratorio applicativo — MAE e RMSE | [R](../../materiali/laboratori/M07/M07_N19.R) |
| M07_N20 | Laboratorio applicativo — Probabilità contro classe | [R](../../materiali/laboratori/M07/M07_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M07.json`, generata dai sorgenti in `lezioni/M07_Annula/`; la spiegazione estesa delle tappe è in `content/lezioni/M07.md`.
