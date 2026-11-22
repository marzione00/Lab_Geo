# M10 · Previsione e progetto statistico

Modelli temporali, valutazione e argomentazione scientifica.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

7 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M10`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Definire l’orizzonte di previsione** · `#laboratorio/m10-orizzonte` | Confrontare futuro previsto e futuro simulato. | [R](../../R/experiments/m10-orizzonte.R) |
| **Previsioni di riferimento e valutazione temporale** · `#laboratorio/m10-riferimenti` | Confrontare media, ultimo valore e riferimento stagionale. | [R](../../R/experiments/m10-riferimenti.R) |
| **Memoria autoregressiva e innovazioni** · `#laboratorio/m10-innovazioni` | Seguire la propagazione di una perturbazione. | [R](../../R/experiments/m10-innovazioni.R) |
| **Struttura ARIMA e stagionalità** · `#laboratorio/m10-arima` | Confrontare specificazioni temporali sul medesimo campione. | [R](../../R/experiments/m10-arima.R) |
| **Diagnostica delle innovazioni stimate** · `#laboratorio/m10-diagnostica` | Verificare la dipendenza che rimane nei residui. | [R](../../R/experiments/m10-diagnostica.R) |
| **Valutazione a origine mobile** · `#laboratorio/m10-copertura` | Valutare ripetutamente una previsione usando solo il passato. | [R](../../R/experiments/m10-copertura.R) |
| **Contributo predittivo di una seconda serie** · `#laboratorio/m10-multivariato` | Confrontare un modello autoregressivo con uno che include un predittore ritardato. | [R](../../R/experiments/m10-multivariato.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Futura: 110 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M10/Futura_M10_previsione_progetto.pdf) · [Progetto R della lezione](../../assets/lezioni/M10/Futura_M10_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M10_Futura/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M10`).

- Tappe 11–22: II · Riferimenti.
- Tappe 23–39: III · Memoria e innovazioni.
- Tappe 40–57: IV · ARIMA e stagione.
- Tappe 58–69: V · Diagnostica.
- Tappe 70–82: VI · Validazione temporale.
- Tappe 83–93: VII · Errori e intervalli.
- Tappe 94–101: VIII · Sistemi multivariati.
- Tappe 102–110: IX · Progetto statistico.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M10_N01 | Fissare l’origine della previsione | [R](../../materiali/laboratori/M10/M10_N01.R) |
| M10_N02 | Modelli di riferimento disponibili all’origine | [R](../../materiali/laboratori/M10/M10_N02.R) |
| M10_N03 | Stimare il modello sui livelli, non sulle differenze già calcolate | [R](../../materiali/laboratori/M10/M10_N03.R) |
| M10_N04 | Residui: controlli prima della previsione | [R](../../materiali/laboratori/M10/M10_N04.R) |
| M10_N05 | Valutazione progressiva interna al train | [R](../../materiali/laboratori/M10/M10_N05.R) |
| M10_N06 | Previsione e intervallo condizionale | [R](../../materiali/laboratori/M10/M10_N06.R) |
| M10_N07 | Aprire il test e confrontare gli errori | [R](../../materiali/laboratori/M10/M10_N07.R) |
| M10_N08 | Orizzonte e copertura descrittiva | [R](../../materiali/laboratori/M10/M10_N08.R) |
| M10_N09 | Esportare una previsione verificabile | [R](../../materiali/laboratori/M10/M10_N09.R) |
| M10_N10 | Percorso obbligatorio e approfondimento | [R](../../materiali/laboratori/M10/M10_N10.R) |
| M10_N11 | Dichiarare prima il confronto predittivo | [R](../../materiali/laboratori/M10/M10_N11.R) |
| M10_N12 | Un grafico e una diagnostica utili alla domanda | [R](../../materiali/laboratori/M10/M10_N12.R) |
| M10_N13 | Generare una relazione che riporti i risultati reali | [R](../../materiali/laboratori/M10/M10_N13.R) |
| M10_N14 | Approfondimento: un VAR(1) come due regressioni | [R](../../materiali/laboratori/M10/M10_N14.R) |
| M10_N15 | Stabilità e residui del sistema | [R](../../materiali/laboratori/M10/M10_N15.R) |
| M10_N16 | Granger: confronto condizionato, non causalità fisica | [R](../../materiali/laboratori/M10/M10_N16.R) |
| M10_N17 | Previsione ricorsiva senza osservazioni future | [R](../../materiali/laboratori/M10/M10_N17.R) |
| M10_N18 | Consegnare e verificare | [R](../../materiali/laboratori/M10/M10_N18.R) |
| M10_N19 | Laboratorio applicativo — Audit prima del modello | [R](../../materiali/laboratori/M10/M10_N19.R) |
| M10_N20 | Laboratorio applicativo — Baseline stagionale | [R](../../materiali/laboratori/M10/M10_N20.R) |

## Tracciabilità

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M10.json`, generata dai sorgenti in `lezioni/M10_Futura/`; la spiegazione estesa delle tappe è in `content/lezioni/M10.md`.
