Dimensione e riflettività degli asteroidi
GeoStat Lab · Marzio De Corato

1. Estrarre l’intero archivio in una cartella.
2. Aprire R/RStudio e impostare quella cartella come directory di lavoro.
3. Installare ggplot2 se necessario: install.packages("ggplot2").
4. Consultare SOLUZIONE.txt per indizi, spiegazione dei passaggi e interpretazione.
5. Eseguire jpl-asteroids.R. Le figure PDF e risultati.csv vengono scritti nella cartella.

La copia data.csv è il campione effettivamente utilizzato. provenance.json documenta fonti, data di acquisizione, trasformazioni, unità e limiti. I file raw conservano la risposta originale del fornitore. preview.json riporta l’ambiente R nativo e i parametri iniziali verificati.

Domanda: L’associazione fra diametro e albedo resta simile quando cambi la soglia dimensionale? Quali oggetti non possono entrare nel confronto?

I primi 2.500 asteroidi numerati non costituiscono un campione casuale o completo della popolazione.

L’albedo è geometrica; non coincide con l’albedo di Bond impiegata nel bilancio radiativo dei pianeti sintetici.

Le incertezze dei diametri sono conservate nel CSV quando disponibili, ma il confronto descrittivo non le propaga.

Una correlazione interna al catalogo può riflettere selezione osservativa e metodi di stima condivisi.

Il mondo dell’atlante è immaginario; il dataset contiene osservazioni reali documentate. Il campione non si aggiorna automaticamente.
