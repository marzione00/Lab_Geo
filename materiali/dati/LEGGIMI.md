# Dati: provenienza, limiti e convenzioni

I CSV sono copie identiche a quelli già distribuiti nei moduli del corso. `ORIGINE_FILE.json` conserva percorso di origine e SHA-256; i file non sono stati rigenerati per adattarli ai nuovi esercizi. I notebook scrivono in `risultati/`, mai qui.

| File | Righe | Colonne | Natura |
|---|---:|---:|---|
| DIZIONARIO.csv | 71 | 5 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| campioni_modulo1.csv | 24 | 6 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| censura_esempio.csv | 4 | 5 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| co2_1985_2001.csv | 204 | 3 | osservazioni storiche; elaborazione didattica documentata |
| co2_mensile_derivata.csv | 526 | 3 | osservazioni storiche; elaborazione didattica documentata |
| co2_settimanale_storica.csv | 2284 | 2 | osservazioni storiche; elaborazione didattica documentata |
| fossili_da_controllare.csv | 25 | 5 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| fossili_simulati.csv | 160 | 7 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| microsonda_simulata.csv | 75 | 10 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| misure_appaiate_simulate.csv | 24 | 3 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| processi_simulati.csv | 300 | 6 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| rocce_simulate.csv | 90 | 11 | dati sintetici didattici, anche se il nome non contiene «simulato» |
| temperatura_simulata.csv | 240 | 5 | dati sintetici didattici, anche se il nome non contiene «simulato» |

## Distinzioni indispensabili

- Il caso iniziale contiene **24 provini simulati, sei stazioni e due affioramenti inventati**. Quattro misure nella stessa stazione non equivalgono automaticamente a quattro stazioni indipendenti.
- La morfometria pulita contiene **160 individui simulati, 80 Rounded e 80 Spiky**: non è il dataset da 1.080 osservazioni delle presentazioni originarie. Il bootstrap che mantiene le quote e quello che modifica la miscela rispondono a disegni diversi.
- `fossili_da_controllare.csv` usa il punto e virgola, formati decimali misti e errori intenzionali. Non usarlo come se fosse già pulito. Una copia del risultato pulito viene prodotta solo nel notebook 04.
- I limiti di rilevabilità nella tabella di censura non sono misure esatte. I dati censurati non vengono trasformati di nascosto in zeri o soglie.
- Nella microsonda Fe è trattato come FeO totale; Mg# è un rapporto molare. Le soglie 98–102 wt% sono una scelta illustrativa, non un criterio mineralogico universale.
- Le 90 rocce sono simulate. `resto_wt` è un completamento numerico della composizione; non identifica una fase reale. Le etichette del generatore vengono escluse dalle variabili del clustering.
- Le misure appaiate hanno unità convenzionali: non sono dichiarate densità o concentrazioni di una sostanza reale.
- La CO₂ deriva dalla copia storica distribuita in statsmodels 0.14.6; il distributore attribuisce i dati a Keeling e Whorf (2004), CDIAC, in pubblico dominio. Il settimanale contiene 2.284 righe, 2.225 valori e 59 mancanti. Fonte: https://www.statsmodels.org/stable/datasets/generated/co2.html
- Il mensile del corso è la **media aritmetica delle medie settimanali disponibili nel mese**, non il prodotto mensile ufficiale. Nessuna interpolazione. Il sottoinsieme 1985–2001 ha 204 mesi e almeno tre osservazioni settimanali per mese.
- Temperatura, processi AR/random walk e sistema VAR sono simulati. Eventuali nuove simulazioni direttamente nei notebook sono dichiarate esplicitamente e fissano un seme R; non devono replicare punto per punto le precedenti simulazioni Python.

## File di supporto

`DIZIONARIO.csv` aggiunge descrizioni operative; `PROVENIENZA_CORSO.json` conserva le note del pacchetto precedente. Il campo «forecast» di quelle note riguarda i materiali precedenti, non un’esecuzione R di questi notebook. `tipo_letto_python` è un controllo di lettura, non una dichiarazione del tipo che R deve sempre assegnare.
