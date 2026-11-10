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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**30 slide · 12 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M13_R6.pdf) · [Codice R delle figure](../../materiali/R/M13_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M13_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Archivio, ancore e convenzioni temporali.
- Pagina 7: Interpolazione e tassi di accumulo.
- Pagina 11: Scenari cronologici e propagazione.
- Pagina 16: Proxy e risoluzione temporale.
- Pagina 21: Discontinuità e sensibilità del modello.
- Pagina 25: Pendenze, durate ed eventi.
- Pagina 30: Consegna e studio autonomo.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M13_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

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

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
