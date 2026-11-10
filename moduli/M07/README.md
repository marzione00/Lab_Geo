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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**33 slide · 9 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M07_R6.pdf) · [Codice R delle figure](../../materiali/R/M07_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M07_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Risposta, predittori e dominio.
- Pagina 6: Correlazione e forma della relazione.
- Pagina 9: Modello lineare e minimi quadrati.
- Pagina 14: Incertezza e previsione.
- Pagina 17: Diagnostica e osservazioni influenti.
- Pagina 22: Predittori multipli e interazioni.
- Pagina 26: Risposte binarie e probabilità.
- Pagina 29: Valutazione su nuovi dati.
- Pagina 32: Laboratorio e riferimenti.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M07_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

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

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
