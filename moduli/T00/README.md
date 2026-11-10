# T00 · Dal codice al calcolo scientifico

Fondamenti operativi in R e confronto con Python.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

8 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-T00`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Dal dato alla trasformazione** · `#laboratorio/t00-programma` | Seguire gli oggetti prodotti da una sequenza di istruzioni. | [R](../../R/experiments/t00-programma.R) |
| **Tipi, vettori e selezioni** · `#laboratorio/t00-tipi` | Esaminare una selezione logica e la sua applicazione a un vettore. | [R](../../R/experiments/t00-tipi.R) |
| **Dalla tabella alla sintesi** · `#laboratorio/t00-lettura` | Confrontare aggregazioni ottenute da misure appartenenti a gruppi. | [R](../../R/experiments/t00-lettura.R) |
| **Diagnosi di un calcolo incompleto** · `#laboratorio/t00-errori` | Individuare l’effetto di un valore mancante sulla sintesi. | [R](../../R/experiments/t00-errori.R) |
| **Sessione pulita e dipendenze** · `#laboratorio/t00-sessione` | Riconoscere un risultato che dipende da un oggetto precedente. | [R](../../R/experiments/t00-sessione.R) |
| **Ciclo e calcolo vettoriale** · `#laboratorio/t00-prestazioni` | Verificare l’equivalenza numerica di due procedimenti. | [R](../../R/experiments/t00-prestazioni.R) |
| **Ricostruire un risultato salvato** · `#laboratorio/t00-persistenza` | Separare oggetto in memoria e dato persistente. | [R](../../R/experiments/t00-persistenza.R) |
| **Confrontare implementazioni** · `#laboratorio/t00-confronto` | Valutare una tolleranza numerica dichiarata. | [R](../../R/experiments/t00-confronto.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**33 slide · 5 figure · 12 diagrammi TikZ · 40 laboratori.**

[PDF del modulo](../../materiali/pdf/T00_R6.pdf) · [Codice R delle figure](../../materiali/R/T00_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/T00_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Dalla domanda al programma.
- Pagina 7: Valori, tipi e operazioni.
- Pagina 11: Lettura e trasformazione dei dati.
- Pagina 18: Errori e controllo del procedimento.
- Pagina 20: Preparazione ed esecuzione locale.
- Pagina 24: Scelte di strumenti e prestazioni.
- Pagina 28: Esecuzione remota e persistenza.
- Pagina 31: Confronti e consegna del lavoro.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/T00_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| T00_N01 | Da un algoritmo a una densità | [R](../../materiali/laboratori/T00/T00_N01.R) |
| T00_N02 | Indici e selezioni | [R](../../materiali/laboratori/T00/T00_N02.R) |
| T00_N03 | Mancanti non uguali a zero | [R](../../materiali/laboratori/T00/T00_N03.R) |
| T00_N04 | Controllare prima di dividere | [R](../../materiali/laboratori/T00/T00_N04.R) |
| T00_N05 | Scrivere una funzione riutilizzabile | [R](../../materiali/laboratori/T00/T00_N05.R) |
| T00_N06 | Percorsi e cartella di lavoro | [R](../../materiali/laboratori/T00/T00_N06.R) |
| T00_N07 | Leggere una tabella e riconoscere i tipi | [R](../../materiali/laboratori/T00/T00_N07.R) |
| T00_N08 | Audit del campione importato | [R](../../materiali/laboratori/T00/T00_N08.R) |
| T00_N09 | Filtrare senza alterare il dato grezzo | [R](../../materiali/laboratori/T00/T00_N09.R) |
| T00_N10 | Creare una variabile e verificarne le unità | [R](../../materiali/laboratori/T00/T00_N10.R) |
| T00_N11 | Raggruppare cambia l’unità della tabella | [R](../../materiali/laboratori/T00/T00_N11.R) |
| T00_N12 | Ripetere con un ciclo | [R](../../materiali/laboratori/T00/T00_N12.R) |
| T00_N13 | Vettorializzazione e riciclo | [R](../../materiali/laboratori/T00/T00_N13.R) |
| T00_N14 | Runtime, pacchetti e installazione | [R](../../materiali/laboratori/T00/T00_N14.R) |
| T00_N15 | Default numerici e confronto R–Python | [R](../../materiali/laboratori/T00/T00_N15.R) |
| T00_N16 | Esportare risultati senza sovrascrivere gli input | [R](../../materiali/laboratori/T00/T00_N16.R) |
| T00_N17 | Identificare il processo di calcolo | [R](../../materiali/laboratori/T00/T00_N17.R) |
| T00_N18 | Una copia in memoria non modifica il CSV | [R](../../materiali/laboratori/T00/T00_N18.R) |
| T00_N19 | Stimare la memoria prima del cloud | [R](../../materiali/laboratori/T00/T00_N19.R) |
| T00_N20 | Cloud simulato: recuperare un output effimero | [R](../../materiali/laboratori/T00/T00_N20.R) |
| T00_PY_N01 | Da un algoritmo a una densità | [Python](../../materiali/laboratori_python/T00/T00_N01.py) |
| T00_PY_N02 | Indici e selezioni | [Python](../../materiali/laboratori_python/T00/T00_N02.py) |
| T00_PY_N03 | Mancanti non uguali a zero | [Python](../../materiali/laboratori_python/T00/T00_N03.py) |
| T00_PY_N04 | Controllare prima di dividere | [Python](../../materiali/laboratori_python/T00/T00_N04.py) |
| T00_PY_N05 | Scrivere una funzione riutilizzabile | [Python](../../materiali/laboratori_python/T00/T00_N05.py) |
| T00_PY_N06 | Percorsi e cartella di lavoro | [Python](../../materiali/laboratori_python/T00/T00_N06.py) |
| T00_PY_N07 | Leggere una tabella e riconoscere i tipi | [Python](../../materiali/laboratori_python/T00/T00_N07.py) |
| T00_PY_N08 | Audit del campione importato | [Python](../../materiali/laboratori_python/T00/T00_N08.py) |
| T00_PY_N09 | Filtrare senza alterare il dato grezzo | [Python](../../materiali/laboratori_python/T00/T00_N09.py) |
| T00_PY_N10 | Creare una variabile e verificarne le unità | [Python](../../materiali/laboratori_python/T00/T00_N10.py) |
| T00_PY_N11 | Raggruppare cambia l’unità della tabella | [Python](../../materiali/laboratori_python/T00/T00_N11.py) |
| T00_PY_N12 | Ripetere con un ciclo | [Python](../../materiali/laboratori_python/T00/T00_N12.py) |
| T00_PY_N13 | Vettorializzazione e riciclo | [Python](../../materiali/laboratori_python/T00/T00_N13.py) |
| T00_PY_N14 | Runtime, pacchetti e installazione | [Python](../../materiali/laboratori_python/T00/T00_N14.py) |
| T00_PY_N15 | Default numerici e confronto R–Python | [Python](../../materiali/laboratori_python/T00/T00_N15.py) |
| T00_PY_N16 | Esportare risultati senza sovrascrivere gli input | [Python](../../materiali/laboratori_python/T00/T00_N16.py) |
| T00_PY_N17 | Identificare il processo di calcolo | [Python](../../materiali/laboratori_python/T00/T00_N17.py) |
| T00_PY_N18 | Una copia in memoria non modifica il CSV | [Python](../../materiali/laboratori_python/T00/T00_N18.py) |
| T00_PY_N19 | Stimare la memoria prima del cloud | [Python](../../materiali/laboratori_python/T00/T00_N19.py) |
| T00_PY_N20 | Cloud simulato: recuperare un output effimero | [Python](../../materiali/laboratori_python/T00/T00_N20.py) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
