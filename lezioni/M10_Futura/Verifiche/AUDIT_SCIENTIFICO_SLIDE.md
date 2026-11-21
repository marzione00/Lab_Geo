# Audit scientifico indipendente delle slide M10 Futura

Data: 20 novembre 2026. Ambito:109 pagine di contenuto scientifico (pagine 2–110), oltre alla copertina;48 frammenti di codice R. Revisione svolta sulla sorgente leggibile `Sorgenti_generazione/contenuti.py`, sui diagrammi in `componenti.py` e sui risultati effettivi del motore.

## Correzioni concrete recepite

| Pagina | Riscontro | Correzione |
|---:|---|---|
|16|Il calcolo della deriva propagava la classe `ts` di uno scalare; la moltiplicazione con 36 orizzonti falliva.|Conversione esplicita del train con `as.numeric` prima del calcolo.|
|34|La didascalia dichiarava un confronto fra ACF teorica e campionaria, mentre il PDF mostra solo l'ACF teorica.|Didascalia allineata alla figura.|
|44|La didascalia citava livelli e trasformazioni, mentre la figura contiene tre trasformazioni differenziate.|Corrette sia didascalia ordinaria sia variante panoramica.|
|53|Il numero n nella formula BIC poteva essere confuso con 168 mesi.|Esplicitato il campione efficace della verosimiglianza n=155; aggiunto `nobs(fit)`.|
|54|Le altezze rappresentano deltaAIC, le etichette gli AIC assoluti.|Didascalia rende esplicite entrambe le scale.|
|97|Il testo menzionava un secondo ritardo in un VAR(1).|Sostituito con il ritardo dell'altra variabile.|
|106|Una sovrastima era espressa con valore negativo senza distinguerla dal bias.|Il testo riporta il bias negativo nella convenzione osservato−previsto.|

Sono state inoltre recepite due correzioni di coerenza editoriale della revisione finale: pagina 18 descrive soltanto i tre riferimenti effettivamente rappresentati nel grafico; pagina 102 distingue CO2 come guida della lezione, morfometria come progetto base N10–N13 e VAR facoltativo.

## Controlli scientifici eseguiti

- Convenzione MA positiva di R; polinomi ordinari e stagionali, espansione del termine al ritardo 13, condizioni di causalità e invertibilità.
- Coerenza fra radici AR esterne al cerchio unitario e autovalori VAR interni; collocazione corretta della radice MA negativa nell'esempio con theta positivo.
- Formule di media e varianza previsionali AR(1), somma degli shock futuri, MA(1) e limite della varianza, crescita nel random walk.
- Differenze ordinaria e stagionale, quattro termini della differenza combinata e perdita di13 posizioni; unica differenziazione nella chiamata SARIMA.
- Separazione calendario 168/36; origini 120/132/144 a dicembre 1994/1995/1996 con valutazione 1995/1996/1997;37 origini aggiuntive sempre interne al train.
- Segno osservato−previsto in metriche, grafici e conclusioni; unità ppm per MAE/RMSE/bias e ppm² per la varianza delle innovazioni.
- Distinzione fra residui nel train, errori futuri, SE da modello e RMSE realizzata; residui 14:168, Ljung–Box lag 24 e fitdf2.
- Intervalli puntuali gaussiani condizionati al modello stimato, esclusione dell'incertezza dei parametri e della selezione;36/36 descritto senza trasformarlo in prova di calibrazione.
- Monte Carlo con 2000 traiettorie indipendenti e dipendenza fra orizzonti all'interno della traiettoria.
- VAR con 250 tempi,249 coppie ritardate, regressori allineati e ricorsione 10 passi senza reinserire il test; due confronti di Granger con correzione Holm e limiti causali espliciti.
- Fossili simulati, split 128/32 ogni quinta riga, baseline dal train, identità geometrica fra diametri e spessore e limiti di generalizzazione.

Dopo le correzioni sopra non sono emerse ulteriori incoerenze scientifiche sostanziali nei contenuti esaminati. Questa revisione non sostituisce l'audit visivo del PDF completo e non certifica il modello come spiegazione del sistema fisico.

## Evidenze eseguibili

`Verifiche/frammenti_slide.csv` contiene gli esiti delle 48 esecuzioni sequenziali reali in R 4.6.0. Il log completo è `Verifiche/esecuzione_frammenti_slide.log`. I12 controlli del motore, i14 controlli indipendenti NumPy/SciPy e l'audit dei 45 PDF scientifici sono conservati nella stessa cartella.

L'esecuzione si avvia dalla radice del modulo con:

```r
source("Codice/esegui_frammenti.R", encoding="UTF-8")
```

Il driver prepara lo stato didattico e poi esegue i frammenti nell'ordine delle slide. Un errore interrompe l'esecuzione; il file degli esiti finali viene scritto soltanto dopo l'ultimo frammento.
