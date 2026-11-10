# GeoStat Lab · Laboratori interattivi

La versione 3.2.4 pone l’esperimento al centro del percorso. I 17 pianeti conservano la rotazione continua, le superfici e i caratteri Nimbus dell’atlante; ciascun modulo si apre sull’indice delle attività. PDF, slide, diagrammi TikZ e codici R6 rimangono consultabili attraverso una sezione di approfondimento.

## Copertura didattica

Sono disponibili **139 esperimenti**, distribuiti nei 17 moduli T00–M16. L’inventario comprende 147 sezioni: 134 hanno dimostrazioni dedicate; 13 sezioni introduttive o di riepilogo rimandano al percorso del rispettivo modulo. La mappa completa è in `content/experiments.json`, campo `coverage`, e nel CSV scaricabile.

Le 11 spedizioni P01–P11 riuniscono attività preparatorie in tre fasi. Gli esperimenti usano dati sintetici e generatori espliciti; i dati e le consegne dei casi applicativi restano nei materiali originali. Le spedizioni costituiscono un percorso ragionato di esercitazione, non un’analisi automatica dei dataset originali.

Ogni attività presenta domanda scientifica, operazione suggerita, interpretazione, formula, definizione dei simboli, due paragrafi di spiegazione e limiti. Le modalità «Percorso guidato», «Esplorazione libera» e «Formalismo e codice» organizzano gli stessi contenuti secondo il compito di studio.

## Funzioni disponibili

- Parametri numerici, cursori e scelte discrete con validazione del dominio.
- Ricalcolo automatico o esplicito; seme riproducibile e nuovo campione.
- Confronto A/B con figure, parametri e riepiloghi numerici.
- Appunti conservati nel browser; nessuna sincronizzazione remota degli appunti.
- Esportazione di figure SVG, dati CSV completi, configurazione JSON e script R autonomo.
- Importazione della configurazione e collegamento con parametri condivisibili. Il codice personalizzato si trasferisce mediante JSON o script, poiché il collegamento conserva soltanto i parametri.
- Editor R effettivamente eseguibile. Dopo l’importazione di codice personalizzato, l’esecuzione richiede il pulsante esplicito.
- Indicazione dei risultati precedenti quando i parametri cambiano; esportazione e confronto dei risultati vengono disabilitati durante il ricalcolo.
- Interruzione con riavvio dell’interprete, che azzera l’ambiente di esecuzione.

## Calcolo e riproducibilità

Il browser esegue R 4.6.0 mediante webR 0.6.0. Grafici e riepiloghi provengono dal medesimo codice R; ggplot2 4.0.3 e svglite 2.2.2 producono le figure vettoriali. Il motore e i 23 pacchetti sono ospitati nel sito, con versioni e impronte SHA-256 in `vendor/r-packages-lock.json`. Il primo avvio richiede il caricamento dell’interprete e dei pacchetti; i calcoli successivi riutilizzano l’ambiente.

Prima dell’avvio viene mostrata una figura statica, chiaramente denominata «Configurazione iniziale», generata dal collaudo in R 4.5.0 e ggplot2 3.5.1. Appena il calcolo locale termina, la figura e i riepiloghi vengono sostituiti dai risultati dell’interprete nel browser. Le versioni sono sempre visibili. Questa anteprima consente di leggere l’esperimento anche se il caricamento del motore non riesce.

Le attività applicano modelli didattici espliciti. Il test ADF/KPSS include riferimenti Monte Carlo specifici; la coda KPSS basata su rumore indipendente non è una calibrazione generale per ogni processo dipendente. Il kriging impiega un modello di covarianza dichiarato. Gli algoritmi per alberi e interpolazione sono implementazioni didattiche documentate nel codice. La dipendenza, l’incertezza Monte Carlo e i limiti del dominio fanno parte dell’interpretazione.

## Struttura dei sorgenti

| Percorso | Contenuto |
|---|---|
| `scripts/labs/build_catalogue.py` | Modelli, controlli, formalismo e raccordo alle sezioni |
| `content/prose-*.json` | Spiegazioni e definizioni dei simboli, per attività |
| `content/experiments.json` | Catalogo generato utilizzato dall’interfaccia |
| `R/lab-common.R` | Tema grafico e funzioni statistiche comuni |
| `R/experiments/` | 139 programmi autonomi, inclusi gli ausili necessari |
| `src/lab-engine.js` | Avvio R, esecuzione, figure e serializzazione |
| `src/experiments.js` | Interfaccia didattica, esportazioni e confronti |
| `src/experiments.css` | Layout e leggibilità dei laboratori |
| `assets/experiments/` | Figure iniziali e riepiloghi verificati in R |
| `qa/experiments-*.json` | Esiti delle verifiche numeriche |

Per modificare un’attività, aggiornare il generatore e il file di prosa pertinente. Il catalogo e gli script autonomi sono prodotti dal seguente flusso, avviato dalla radice del repository:

```sh
python3 scripts/labs/build_catalogue.py
Rscript scripts/labs/format-code.R
Rscript scripts/labs/check-r.R . content/experiments-draft.json edges
Rscript scripts/labs/check-invariants.R .
python3 scripts/labs/package-downloads.py
npm test
```

Per il collaudo R occorrono ggplot2 e jsonlite. Per esportare SVG con `ggsave()` nel proprio ambiente è necessario anche svglite. `R/experiments/` contiene programmi già pronti, che possono essere eseguiti senza ricostruire il catalogo. La build ordinaria del sito richiede soltanto Node.js 22 o successivo; R e Python servono per rigenerare i contenuti.

Il collaudo DOM viene eseguito con `npm run test:dom`, dopo `npm ci --ignore-scripts`. Il test completo `npm run test:browser` prepara automaticamente la pagina di collaudo con `node scripts/prepare-browser-harness.mjs`, esegue Chromium e rimuove i file temporanei alla conclusione. L’ambiente è descritto in [DEPLOYMENT.md](../DEPLOYMENT.md).

Per una verifica manuale, eseguire il preparatore dopo la build e aprire direttamente `experiments-harness.html` nel server locale. Il viewport mobile va impostato negli strumenti del browser: la politica anti-incorporamento esclude un’anteprima mediante iframe. Prima della pubblicazione ricostruire `dist/`.

Il confronto delle metriche richiede nomi univoci e identico insieme di grandezze. I valori numerici, compresi quelli serializzati come stringhe decimali, sono confrontati con soglia `max(10⁻⁵, 0,025 × max(|x|, |y|))`; testi, valori logici e valori nulli devono corrispondere esattamente nel proprio tipo. Metriche assenti, aggiunte, rinominate o di tipo incompatibile fanno fallire il collaudo, così come gli scarti oltre soglia.

Il sito conserva la navigazione da tastiera, etichette dei controlli e annunci dello stato di calcolo. Su schermi stretti i grafici rimangono scorribili orizzontalmente, così da conservare dimensioni leggibili di assi e valori. Le formule hanno una descrizione dei simboli nel testo adiacente.

## Dimensioni della distribuzione

Le copie SVG delle slide e dei pannelli sono ottimizzate con SVGO 4.0.0, mantenendo otto cifre decimali e verificandone la resa. I PDF, i font e i sorgenti R6 restano identici agli originali. Dopo una nuova importazione con `--render`, l’ottimizzazione può essere ripetuta con `node scripts/optimize-svg.mjs` nell’ambiente che contiene SVGO; il pacchetto è necessario soltanto per questa operazione facoltativa. Gli SVG già ottimizzati sono inclusi nel repository e la build ordinaria continua a utilizzare soltanto Node.js.

La distribuzione web esclude i file nascosti e i formati di chiave previsti dalla politica di build, i file temporanei di compilazione LaTeX e le copie PDF della cartella di collaudo `materiali/verifiche/`; i PDF consultabili sono in `materiali/pdf/`. Tutti i file originali restano conservati nel repository.

I 232 pannelli TikZ nella lettura testuale riutilizzano lo stesso SVG della slide mediante una finestra vettoriale sulle coordinate originali del diagramma. Le copie dei pannelli rimangono nel repository; la distribuzione evita di trasferire due volte lo stesso contenuto.
