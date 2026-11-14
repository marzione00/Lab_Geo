Quando il sensore raggiunge il limite
GeoStat Lab · Marzio De Corato

1. Estrarre l’intero archivio in una cartella.
2. Aprire R/RStudio e impostare quella cartella come directory di lavoro.
3. Installare ggplot2 se necessario: install.packages("ggplot2").
4. Consultare SOLUZIONE.txt per indizi, spiegazione dei passaggi e interpretazione.
5. Eseguire solar-flares.R. Le figure PDF e risultati.csv vengono scritti nella cartella.

La copia data.csv è il campione effettivamente utilizzato. provenance.json documenta fonti, data di acquisizione, trasformazioni, unità e limiti. I file raw conservano la risposta originale del fornitore. preview.json riporta l’ambiente R nativo e i parametri iniziali verificati.

Domanda: L’associazione fra durata e irradiamento di picco dei brillamenti solari del 2003 rimane simile dopo aver cambiato soglia di selezione e trattamento degli eventi in sequenza?

I tempi sono riferiti alla definizione operativa GOES; una durata mancante non viene ricostruita né sostituita con zero.

Il segnale XRS-B è un irradiamento di picco mediato su un minuto, non l’energia totale emessa dal brillamento.

I valori saturati sono esclusi da ogni modello. La selezione dei soli eventi con fine disponibile può introdurre distorsioni.

L’analisi riguarda il 2003, con soglie configurabili e dipendenze fra eventi possibili; non stima frequenze complete, causalità, pericolosità terrestre o previsioni operative.

Il mondo dell’atlante è immaginario; il dataset contiene osservazioni reali documentate. Il campione non si aggiorna automaticamente.
