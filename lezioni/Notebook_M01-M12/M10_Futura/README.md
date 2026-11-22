# Futura — 20 notebook svolti

**M10 · Previsione e progetto statistico.** Il pacchetto comprende 20 RMarkdown e i corrispondenti 20 HTML autonomi, con codice visibile, output effettivamente eseguiti, interpretazioni e una variante svolta per laboratorio. Gli identificativi M10_N01–M10_N20 conservano la corrispondenza con i laboratori del sito del corso.

Aprire **[index.html](index.html)** per navigare. Gli HTML contengono stili, immagini e formule MathML: si leggono senza connessione e senza R. I collegamenti alle fonti esterne sono consultazioni facoltative; la lettura, il codice e i risultati non dipendono da essi. Le formule richiedono un browser che supporti MathML.

## Che cosa è stato eseguito

Il registro allegato documenta **100 blocchi R eseguiti, 20 grafici, 0 errori e 0 avvisi**. L’edizione è stata calcolata con **R 4.6.0 (2026-04-24) in WebR 0.6.1**, usando soltanto R base e i pacchetti standard. Il codice viene eseguito in un ambiente nuovo per ciascun notebook; i cinque blocchi di uno stesso notebook condividono gli oggetti nell’ordine mostrato.

Gli output testuali provengono da `source(..., print.eval=TRUE)`; i grafici da dispositivi PDF di R, rasterizzati per essere incorporati negli HTML. Il generatore verifica che ogni Rmd coincida con la copia conservata al momento dell’esecuzione. Non ci sono numeri inseriti manualmente negli output. Le frasi di interpretazione distinguono i risultati calcolati dalle loro implicazioni scientifiche.

- [VERIFICA_NOTEBOOK.csv](VERIFICA_NOTEBOOK.csv) riporta esito, blocchi, figure, runtime, durata e impronte SHA-256 di Rmd e HTML.
- [Verifiche/esecuzione_blocchi.csv](Verifiche/esecuzione_blocchi.csv) riporta ogni blocco e i suoi file di output.
- [Verifiche/sessionInfo.txt](Verifiche/sessionInfo.txt) conserva versione, piattaforma e pacchetti caricati.
- [MAPPA_ORIGINALI.csv](MAPPA_ORIGINALI.csv) collega ogni laboratorio originale allo svolgimento, con hash e adattamenti.

Il tempo registrato riguarda l’esecuzione dei blocchi nel runtime, escluso l’avvio di WebR e la produzione degli HTML. Non rappresenta una misura delle prestazioni di un normale computer con R.

## Percorso didattico

| Notebook | Attività | Risultato da saper discutere |
|---|---|---|
| N01–N03 | Origine, riferimenti e SARIMA sui livelli | Una specifica temporale senza uso del futuro |
| N04–N06 | Residui, validazione interna, intervalli | Diagnostica e incertezza condizionate al modello |
| N07–N09 | Test, orizzonti, esportazione | Metriche, copertura descrittiva e file ricostruibili |
| N10–N13 | Progetto morfometrico obbligatorio | Confronto predittivo e relazione con risultati reali |
| N14–N18 | Approfondimento VAR facoltativo | Sistema bivariato, Granger, ricorsione e consegna |
| N19–N20 | Laboratori applicativi | Audit dei duplicati e baseline stagionale oltre un anno |

Ogni notebook contiene una domanda, tre obiettivi, descrizione dei dati e delle unità, preparazione autonoma, tre passaggi svolti, variante, errore da riconoscere e risposta argomentata. Un notebook può quindi essere eseguito senza avere aperto quelli precedenti. Gli argomenti del VAR sono separati dal progetto morfometrico di base.

## Dati locali e significato scientifico

I tre CSV sono copie identiche all’archivio precedente M01–M09. [Dati/PROVENIENZA.json](Dati/PROVENIENZA.json) riporta origine e SHA-256. Gli script di analisi li leggono senza modificarli.

| File | Natura e unità | Protocollo |
|---|---|---|
| `co2_1985_2001.csv` | 204 mesi storici, ppm; aggregato didattico da osservazioni settimanali | 168 mesi 1985–1998 per il train; 36 mesi 1999–2001 per il test |
| `fossili_simulati.csv` | 160 individui sintetici, diametri in micrometri | Test ogni quinta riga: 32 individui; train 128 |
| `processi_simulati.csv` | Processi sintetici, senza unità fisica | VAR sui passi 1–250; previsione a origine fissa sui passi 251–260 |

L’aggregato mensile di CO₂ segue la convenzione del corso e non deve essere presentato come una serie mensile ufficiale o una misura attuale. Nel progetto fossili il diametro interno è geometricamente legato al totale e allo spessore: la buona previsione non costituisce una scoperta causale. Lo split morfometrico è un protocollo didattico già noto, non una nuova validazione prospettica.

Nel caso CO₂ gli intervalli sono gaussiani, puntuali e condizionati alla specifica SARIMA stimata. `predict.Arima` non include l’incertezza di stima dei parametri. La quota di bersagli inclusi nelle bande per 36 orizzonti di una sola origine descrive questa traiettoria; non dimostra calibrazione al 95% né copertura simultanea dell’intero percorso.

I due confronti di Granger sono pianificati, corretti insieme con Holm e interpretati come contributo predittivo condizionato alla specifica. La ricorsione VAR non inserisce osservazioni del test nei passi intermedi. La perturbazione di stato in N15 non è un impulso strutturale identificato.

## Eseguire in R o RStudio

1. Estrarre completamente il pacchetto, mantenendo la struttura delle cartelle.
2. Aprire `GeoStat_Lab_Notebooks.Rproj` nella cartella `M10_Futura`, oppure il progetto generale dei notebook. La preparazione cerca la cartella del modulo nei livelli previsti e usa percorsi assoluti per dati e risultati.
3. Aprire un `M10_Nxx.Rmd` ed eseguire i blocchi in ordine. Non occorre installare pacchetti per i calcoli scientifici.
4. Consultare `Risultati/M10_Nxx/` per i CSV, testi e modelli esportati dal notebook. I notebook esclusivamente esplorativi producono soprattutto output e figure nel documento.

Per usare **Knit** occorrono `rmarkdown`, `knitr` e Pandoc. RStudio normalmente fornisce Pandoc. L’installazione iniziale, se necessaria, richiede connessione:

```r
source("R/00_installazione.R")
rmarkdown::render("M10_N06.Rmd", encoding = "UTF-8")
```

La configurazione YAML richiede HTML autonomo, CSS locale e MathML, senza MathJax. Per generare i venti HTML tramite knitr è disponibile `R/crea_html_con_rmarkdown.R`. Questo percorso esegue il medesimo codice e può produrre dettagli di impaginazione diversi da quelli dell’edizione distribuita; il registro di audit viene creato dal percorso seguente.

## Riprodurre l’edizione distribuita

Dalla cartella `M10_Futura`, con R nativo:

```r
source("R/esegui_notebook.R", encoding = "UTF-8")
esegui_notebook()
```

L’esecutore legge i blocchi dagli Rmd, conserva la copia del sorgente, cattura output e condizioni, e scrive i PDF e il registro in `Verifiche/`. Si arresta con errore finale se almeno un blocco non riesce. Non cancella i CSV originali. Per eseguire un solo notebook si può passare `ids="M10_N06"`; prima di produrre l’indice completo occorre eseguire l’intera serie, perché il registro viene sostituito a ogni chiamata.

Per ricreare gli HTML dell’edizione servono Python 3 con PyMuPDF (`fitz`) e Pandoc:

```bash
python Sorgenti_generazione/crea_html.py
python Sorgenti_generazione/crea_indice.py
```

Gli HTML incorporano i PNG generati dai PDF, includono output visibili e formule MathML e conservano i collegamenti ai PDF vettoriali. Dopo una modifica agli Rmd, rieseguire i blocchi prima di rigenerare gli HTML: il generatore rifiuta un sorgente diverso dalla copia eseguita. `Sorgenti_generazione/genera_notebook.py` ricostruisce gli Rmd dal contenuto editoriale originale e **sovrascrive** eventuali modifiche manuali agli Rmd; non è necessario per leggere o rieseguire il pacchetto.

Come alternativa a R nativo, lo script `Sorgenti_generazione/esegui_webr.mjs` usa Node e WebR. L’edizione distribuita è stata verificata con WebR 0.6.1. Il runtime va installato prima dell’uso e non è una dipendenza degli HTML già pronti:

```bash
npm install webr@0.6.1
node Sorgenti_generazione/esegui_webr.mjs
python Sorgenti_generazione/crea_html.py
python Sorgenti_generazione/crea_indice.py
```

## Struttura e fonti

`Dati/` contiene i dati immutati. `R/` contiene le funzioni di servizio, l’esecutore e gli script originali. `Risultati/` contiene gli output analitici esportati. `Verifiche/` conserva sorgenti eseguiti, log, PDF e PNG dei grafici. `Sorgenti_generazione/` contiene i generatori editoriali e HTML.

Le copie in `R/Originali_corso/` provengono dal repository [marzione00/Lab_Geo](https://github.com/marzione00/Lab_Geo), commit `649f7cc577b96bd1044d81e78a2f530813e4f96b`, percorso `materiali/laboratori/M10/`, e non sono state modificate. Il loro progetto originario si chiama `Notebook_R_Geologia.Rproj`: nel presente pacchetto gli Rmd sostituiscono quella preparazione con percorsi autonomi. Gli script cumulativi del sito sono stati articolati in passaggi leggibili, conservando il tema, i dati e il protocollo di ciascun identificativo.

Le fonti dei metodi sono la documentazione ufficiale di R: [arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/arima.html), [predict.Arima](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.arima.html), [Box.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/box.test.html) e [p.adjust](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html). Il [sito del corso](https://marzione00.github.io/Lab_Geo/#indice) resta il riferimento per il percorso generale.
