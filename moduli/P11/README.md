# P11 · Classificare nuove stazioni sintetiche

Separazione dei dati, standardizzazione e classificatore dei centroidi.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Valuta un classificatore su nuove stazioni, distinguendo geometria, probabilità previste e decisioni operative.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Definire il trasferimento

- **Bersaglio predittivo e nuove stazioni**: Confrontare predizione di misure e trasferimento a nuove unità. [Programma R](../../R/experiments/m16-bersaglio.R); rotta del sito: `#laboratorio/m16-bersaglio`.
- **Standardizzazione e confine decisionale**: Esaminare un classificatore a centroidi nella metrica scelta. [Programma R](../../R/experiments/m16-geometria.R); rotta del sito: `#laboratorio/m16-geometria`.

### Selezionare e addestrare

- **Selezione dei predittori e contaminazione**: Valutare la selezione di variabili su puro rumore. [Programma R](../../R/experiments/m16-selezione.R); rotta del sito: `#laboratorio/m16-selezione`.
- **Alberi e aggregazione di classificatori**: Confrontare un albero con un insieme di alberi su campioni bootstrap. [Programma R](../../R/experiments/m16-alberi.R); rotta del sito: `#laboratorio/m16-alberi`.

### Verificare probabilità e decisioni

- **Soglia, discriminazione e calibrazione**: Separare probabilità previste e decisione binaria. [Programma R](../../R/experiments/m16-metriche.R); rotta del sito: `#laboratorio/m16-metriche`.
- **Trasferibilità e cambiamento della relazione**: Valutare un modello su una popolazione differente. [Programma R](../../R/experiments/m16-trasferimento.R); rotta del sito: `#laboratorio/m16-trasferimento`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P11: 27 tappe.**

[Presentazione PDF](../../assets/lezioni/P11/P11_Stazioni.pdf) · [Progetto R della spedizione](../../assets/lezioni/P11/Spedizione_P11_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P11_Stazioni/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P11`).

- Tappa 3: Il caso guida.
- Tappe 4–7: Bersaglio e protocollo di valutazione.
- Tappe 8–12: Geometria standardizzata e centroidi.
- Tappe 13–16: Prestazione e limiti dell’interpretazione.
- Tappe 17–18: Scheda del modello e consegna.
- Tappe 19–25: Laboratori della spedizione.
- Tappa 26: Sintesi.
- Tappa 27: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P11_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P11.json`, generata dai sorgenti in `lezioni/P11_Stazioni/`.
