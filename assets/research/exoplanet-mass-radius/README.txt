Massa e raggio: un modello da mettere alla prova
GeoStat Lab · Marzio De Corato

1. Estrarre l’intero archivio in una cartella.
2. Aprire R/RStudio e impostare quella cartella come directory di lavoro.
3. Installare ggplot2 se necessario: install.packages("ggplot2").
4. Consultare SOLUZIONE.txt per indizi, spiegazione dei passaggi e interpretazione.
5. Eseguire exoplanet-mass-radius.R. Le figure PDF e risultati.csv vengono scritti nella cartella.

La copia data.csv è il campione effettivamente utilizzato. provenance.json documenta fonti, data di acquisizione, trasformazioni, unità e limiti. I file raw conservano la risposta originale del fornitore. preview.json riporta l’ambiente R nativo e i parametri iniziali verificati.

Domanda: Quanto generalizza una relazione massa–raggio se la valutazione avviene su sistemi stellari esclusi dalla stima? Come cambia il risultato restringendo le incertezze ammesse?

La regressione ordinaria non propaga le incertezze di misura e non corregge gli effetti di selezione.

Il massimo degli errori relativi superiore e inferiore serve a filtrare; non è una nuova stima probabilistica dell’errore.

Il campione eterogeneo riunisce metodi osservativi diversi; default_flag non garantisce la misura più precisa disponibile.

La separazione per stella riduce la contaminazione fra insiemi, ma una sola partizione non quantifica la variabilità della prestazione.

Massa e raggio non determinano univocamente composizione, atmosfera o abitabilità.

Il mondo dell’atlante è immaginario; il dataset contiene osservazioni reali documentate. Il campione non si aggiorna automaticamente.
