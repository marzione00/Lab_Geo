Leggere un catalogo sismico
GeoStat Lab · Marzio De Corato

1. Estrarre l’intero archivio in una cartella.
2. Aprire R/RStudio e impostare quella cartella come directory di lavoro.
3. Installare ggplot2 se necessario: install.packages("ggplot2").
4. Consultare SOLUZIONE.txt per indizi, spiegazione dei passaggi e interpretazione.
5. Eseguire usgs-quakes.R. Le figure PDF e risultati.csv vengono scritti nella cartella.

La copia data.csv è il campione effettivamente utilizzato. provenance.json documenta fonti, data di acquisizione, trasformazioni, unità e limiti. I file raw conservano la risposta originale del fornitore. preview.json riporta l’ambiente R nativo e i parametri iniziali verificati.

Domanda: Come cambia la distribuzione delle magnitudo quando elevi la soglia di selezione, e quali conclusioni sul territorio rimangono ingiustificate?

Estrazione regionale e temporale delimitata; non è un campione casuale della sismicità mondiale.

Scale di magnitudo eterogenee: magType è conservato nel CSV e distingue i punti nel grafico.

La soglia di estrazione non dimostra la completezza del catalogo; repliche e sequenze possono introdurre dipendenza.

Le profondità possono essere negative rispetto al riferimento del catalogo; sono conservate, senza trasformarle arbitrariamente in zero.

Il mondo dell’atlante è immaginario; il dataset contiene osservazioni reali documentate. Il campione non si aggiorna automaticamente.
