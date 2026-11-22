# P10 · Un’analisi ricostruibile e verificabile

Dati immutati, funzioni, controlli numerici e storia delle modifiche.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

Ricostruisci un’analisi verificabile, rendendo espliciti dati, dipendenze, criteri numerici e piano casuale.

Le tre fasi collegano esperimenti preparatori con dati sintetici. Il caso applicativo, con dati e codice, è nella presentazione a tappe descritta sotto.

### Controllare i dati

- **Collegare tabelle senza moltiplicare le misure**: Verificare la cardinalità di un collegamento mediante una chiave. [Programma R](../../R/experiments/m02-join.R); rotta del sito: `#laboratorio/m02-join`.
- **Verificare una tabella analitica**: Controllare righe, chiavi e unità prima dell’analisi. [Programma R](../../R/experiments/m02-tabella.R); rotta del sito: `#laboratorio/m02-tabella`.

### Verificare le funzioni

- **Verificare una funzione prima dell’uso**: Sottoporre una funzione a casi validi e invalidi. [Programma R](../../R/experiments/m15-contratti.R); rotta del sito: `#laboratorio/m15-contratti`.
- **Identità e confronto numerico**: Scegliere una tolleranza coerente con la scala del problema. [Programma R](../../R/experiments/m15-tolleranze.R); rotta del sito: `#laboratorio/m15-tolleranze`.

### Conservare la provenienza

- **Integrità dei file e identità dei dati**: Confrontare contenuto numerico, rappresentazione testuale e impronta di un file. [Programma R](../../R/experiments/m15-integrita.R); rotta del sito: `#laboratorio/m15-integrita`.
- **Parametri, versioni e sensibilità**: Confrontare risultati prodotti da scelte analitiche tracciate. [Programma R](../../R/experiments/m15-provenienza.R); rotta del sito: `#laboratorio/m15-provenienza`.


Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la presentazione a tappe della spedizione.
<!-- END INTERACTIVE GUIDE -->

**Spedizione P10: 26 tappe.**

[Presentazione PDF](../../assets/lezioni/P10/P10_Ricostruibile.pdf) · [Progetto R della spedizione](../../assets/lezioni/P10/Spedizione_P10_progetto_R.zip) · [Sorgenti della presentazione](../../lezioni/P10_Ricostruibile/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-P10`).

- Tappa 3: Il caso guida.
- Tappe 4–8: Dati e trasformazioni dichiarate.
- Tappe 9–13: Prove del codice e integrità dei file.
- Tappe 14–17: Piani casuali, versioni e consegna.
- Tappe 18–24: Laboratori della spedizione.
- Tappa 25: Sintesi.
- Tappa 26: Riferimenti.

## Esecuzione

Estrarre il progetto R della spedizione e avviare R nella sua cartella principale, che contiene `R/` e `dati/`:

```r
source("R/P10_figure.R")
```

Lo script ricostruisce figure e valori del caso ed è la soluzione ragionata della spedizione sul sito; i frammenti delle slide sono nella cartella `Codice/`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione della spedizione nel percorso. La presentazione a tappe è in `content/lezioni/P10.json`, generata dai sorgenti in `lezioni/P10_Ricostruibile/`.
