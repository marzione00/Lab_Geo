# Controllo sistematico della versione 3.9.1

Revisione del 13 novembre 2026. Ambito: coerenza fra interfaccia, navigazione, sorgenti, guide, risultati e archivi scaricabili. I materiali originali R6 sono preservati. Questo controllo non costituisce una nuova rilettura visiva individuale delle 861 slide.

## Rilievi e correzioni

| Rilievo | Conseguenza | Correzione |
|---|---|---|
| Due navigatori per passi nel terminale dei progetti | La numerazione scientifica e quella dei blocchi R potevano essere confuse; il download era duplicato | Il terminale della soluzione controlla passaggi e download. Il codice completo conserva commenti e numeri di riga |
| Ritorno dall’esplorazione senza parametro di configurazione | Un collegamento aperto direttamente poteva riportare a una stella diversa | Collegamenti di sistema con `?v=`, validazione 0–9999 e conservazione del valore nel ritorno e nel ricaricamento |
| Interruzione durante il caricamento del CSV | Il programma poteva partire dopo che l’utente aveva premuto Interrompi | Annullamento della richiesta e controllo prima e dopo l’esecuzione R; nuovo tentativo indipendente |
| Ordinamento linguistico dei nomi degli esopianeti | Il medesimo seme selezionava sistemi diversi in R locale e webR | Ordinamento radix esplicito, indipendente dalla lingua; anteprime, guide e archivi rigenerati |
| Nuovi derivati esclusi dai controlli di coerenza precedenti | Guide testuali, script scaricabili e ZIP potevano divergere dai sorgenti | Confronto esatto delle guide, dei programmi e di tutti i membri dei cinque archivi; ZIP rigenerabili byte per byte; equivalenza delle espressioni R delle undici spedizioni |
| Documentazione di funzioni superate | Descrizione di sole letture complementari, conteggio errato dei temi, configurazioni dichiarate effimere | README e guide correnti allineati a cinque missioni, sei temi astronomici, tredici famiglie e collegamenti riproducibili |
| Due campi descrittivi duplicati e non utilizzati | Copie della domanda senza un consumatore nel percorso delle missioni | Eliminati i campi ridondanti, conservando la domanda canonica |

## Riproducibilità della separazione per sistemi stellari

Prima della correzione, con gli stessi dati e parametri, `LC_COLLATE=C` produceva β = 1,816628 e RMSE = 0,2249034 dex; `LC_COLLATE=C.UTF-8` produceva β = 1,766086 e RMSE = 0,2170758 dex. Il problema precedeva il campionamento: cambiava l’ordine dei nomi da cui estrarre i sistemi.

Con `sort(unique(data$hostname), method="radix")`, entrambi gli ambienti producono la stessa lista di sistemi selezionati e gli stessi risultati, β = 1,816628 e RMSE = 0,2249034 dex. Nessun dato osservato è stato modificato. Il comportamento dell’ordinamento è documentato nel [manuale ufficiale R](https://stat.ethz.ch/R-manual/R-devel/library/base/html/sort.html).

## Verifiche

- 54 test automatici superati, inclusi routing, regressione dell’annullamento e unicità dei comandi del terminale.
- Controlli DOM su 28 moduli e 1.730 espressioni matematiche, oltre alle regressioni SVG e agli ingressi non attendibili.
- Controlli strutturali su tutte le 68 destinazioni complementari e copertura delle 16 soluzioni disponibili.
- 143 configurazioni R delle cinque missioni, inclusi i limiti dei parametri; confronto aggiuntivo fra le due impostazioni linguistiche.
- Esecuzione dei 23 programmi intermedi e degli 11 programmi completi P01–P11, confrontati con le espressioni originali.
- Coerenza dei 139 esperimenti, delle 28 schede dei moduli, delle guide derivate, degli archivi e dei collegamenti locali.
- Ricerca strutturale dei residui editoriali segnalati nei 861 record delle slide: nessuna corrispondenza nei campi pubblicabili. Controllo delle ripetizioni esatte in 229 passaggi lunghi delle narrazioni e guide dei progetti: nessuna duplicazione. Non è una misura automatica della qualità letteraria.

La verifica interattiva Chromium ha confermato, sul progetto degli esopianeti, 462 pianeti, 224 sistemi di stima, 96 di verifica, β = 1,82, RMSE = 0,225 dex e riferimento costante = 0,368 dex, coerenti con le metriche dell’anteprima nativa. È stato verificato il percorso sistema → osservatorio → ricaricamento → sistema: Talos conserva la configurazione 1 e la classe K V. Nessun overflow orizzontale nella pagina controllata a 1348 px; zero errori di composizione matematica. Questa revisione non ripete il collaudo mobile della versione precedente.

Gli esiti eseguibili sono in `qa/consistency.json`, `qa/research-r.json`, `qa/solution-stages.json`, `qa/course-solutions.json` e `qa/editorial-consistency.json`. I rapporti precedenti conservano il loro ambito storico; le loro evidenze non sono attribuite a questa revisione.

## Copertura didattica effettiva

I 68 mondi complementari condividono cinque mini-progetti su dati osservati. Le destinazioni sono differenti, ma non offrono ancora 68 indagini autonome. Le undici spedizioni originali hanno soluzioni complete eseguibili in R/RStudio locale; l’esecuzione dei relativi programmi nel browser non è implementata.

La narrazione sperimentale con previsione e commento numerico specifico è completa nelle nove attività M05. Le altre 130 attività conservano la prosa precedente. Questo limite rimane esplicito nel README: la correzione delle incoerenze non equivale a un’estensione della copertura narrativa.

Il controllo strutturale non sostituisce una revisione visiva di ogni presentazione, un collaudo su tutti i dispositivi o un’analisi indipendente di sicurezza. I test di sicurezza esistenti continuano a far parte della verifica della distribuzione.
