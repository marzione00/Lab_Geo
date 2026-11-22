# P08 · Collocare nel tempo il massimo di un proxy

Ancore cronologiche, propagazione dell’incertezza e discontinuità sedimentarie.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Costruisci una cronologia di archivio e segui la propagazione delle incertezze nella datazione di un evento.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Stabilire le ancore

- **Ancore cronologiche e convenzioni temporali**: Collegare profondità, età e riferimento temporale. [Programma R](../../R/experiments/m13-ancore.R); rotta del sito: `#laboratorio/m13-ancore`.
- **Interpolazione e tassi di accumulo**: Ricostruire una cronologia fra ancore e valutarne la pendenza. [Programma R](../../R/experiments/m13-interpolazione.R); rotta del sito: `#laboratorio/m13-interpolazione`.

### Propagare l’incertezza

- **Scenari cronologici e propagazione**: Costruire cronologie perturbate conservando l’associazione fra età e profondità. [Programma R](../../R/experiments/m13-incertezza.R); rotta del sito: `#laboratorio/m13-incertezza`.
- **Durate entro uno stesso scenario**: Propagare la covarianza nella durata fra due eventi. [Programma R](../../R/experiments/m13-durate.R); rotta del sito: `#laboratorio/m13-durate`.

### Valutare interpretazioni alternative

- **Risoluzione temporale di un proxy**: Confrontare un campionamento uniforme in profondità con il suo supporto temporale. [Programma R](../../R/experiments/m13-proxy.R); rotta del sito: `#laboratorio/m13-proxy`.
- **Discontinuità e sensibilità della cronologia**: Rappresentare un intervallo temporale privo di sedimentazione. [Programma R](../../R/experiments/m13-hiatus.R); rotta del sito: `#laboratorio/m13-hiatus`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P08: 28 tappe.**

[Presentazione PDF](../../assets/lezioni/P08/P08_Proxy.pdf) · [Progetto R della spedizione](../../assets/lezioni/P08/Spedizione_P08_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P08_Proxy/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P08`).

- Tappa 3: Il caso guida.
- Tappe 4–8: Ancore e interpolazione cronologica.
- Tappe 9–12: Scenari di incertezza cronologica.
- Tappe 13–16: Massimo osservato e interpretazione temporale.
- Tappe 17–19: Hiatus e conclusione condizionata.
- Tappe 20–26: Laboratori della spedizione.
- Tappa 27: Sintesi.
- Tappa 28: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P08_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P08.json`, generata dai sorgenti in `lezioni/P08_Proxy/`.
