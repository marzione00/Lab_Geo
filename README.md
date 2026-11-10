# GeoStat Lab

**Laboratori interattivi di statistica e coding R per le scienze della Terra**
**Autore: Marzio De Corato** · Modulo didattico di [Topological Manifolds](https://marzione00.github.io/Personal_web_page/) ([repository del sito principale](https://github.com/marzione00/Personal_web_page)).

Versione applicativa **3.2.3** · materiali didattici **R6** · lingua italiana

GeoStat Lab accompagna lo studio dei metodi statistici attraverso 139 esperimenti nei quali, modificando parametri e ipotesi, si osservano le conseguenze sui dati simulati, sulle figure e sulle conclusioni. Ogni attività collega il problema scientifico al formalismo matematico e al programma R che ne produce i risultati. L’atlante di 17 pianeti rotanti organizza il percorso; le 11 spedizioni applicative riuniscono i metodi necessari ad affrontare un’indagine più articolata.

Il progetto è un sito statico: l’interprete R opera nel browser mediante webR, mentre ggplot2 genera le rappresentazioni. La distribuzione comprende il motore di calcolo, i pacchetti R e MathJax, affinché l’esecuzione ordinaria non dipenda da CDN esterne. Le presentazioni conservano il template e i caratteri del corso.

[Avvio rapido](#avvio-rapido) · [Pubblicazione su GitHub](#pubblicazione-su-github) · [Moduli](#moduli-e-spedizioni) · [Sicurezza](#sicurezza-e-modello-di-fiducia) · [Documentazione](#documentazione)

## Contenuti e funzioni

| Ambito | Disponibilità |
|---|---|
| Esperimenti interattivi | 139 attività distribuite nei 17 moduli |
| Percorso applicativo | 11 spedizioni, ciascuna articolata in tre fasi |
| Materiali del corso | 28 fascicoli, 861 slide vettoriali, 261 figure R e 232 diagrammi TikZ |
| Programmi originali | 340 laboratori R e 20 laboratori Python |
| Esperimenti riproducibili | 139 programmi R autonomi, parametri e seme casuale espliciti |
| Esplorazione | Parametri modificabili, confronto fra due scenari, tabella dei risultati |
| Esportazione | Script R, figure SVG, dati CSV e configurazione JSON |
| Lettura | Percorso guidato, esplorazione libera, formalismo e codice |
| Accessibilità | Navigazione da tastiera, testo alternativo, formule vettoriali, pausa delle rotazioni |

Le simulazioni dichiarano le proprie ipotesi e impiegano dati sintetici. I risultati illustrano il comportamento dei metodi nelle condizioni specificate; l’applicazione a dati osservati richiede una valutazione del disegno di campionamento, della qualità delle misure e dell’adeguatezza del modello.

## La galassia del corso

La pagina iniziale riunisce i 17 moduli in una galassia illustrativa originale. Passando il puntatore su un pianeta si apre la scheda con argomento, descrizione e numero di esperimenti; il pulsante **Viaggia** avvia la transizione verso il modulo. La scheda rimane selezionata quando il puntatore lascia il pianeta. Un breve ritardo esclude gli attraversamenti accidentali durante lo spostamento verso il pulsante.

Su schermi piccoli i pianeti sono disposti in tre colonne, con bersagli ampi: un tocco mostra la scheda e **Scegli un altro pianeta** riporta alla mappa. Tab e le frecce consentono di selezionare le destinazioni da tastiera. **Pausa rotazione** e la preferenza di sistema per il movimento ridotto restano disponibili. L’indice testuale conserva l’accesso diretto a tutti i fascicoli.

L’illustrazione è generata da `scripts/generate-galaxy.py`, mediante Python e Pillow con seme deterministico. Il file WebP già incluso non richiede Python per la build. Le distanze e le velocità sono illustrative; le descrizioni dei moduli provengono dal catalogo condiviso.

## Avvio rapido

Occorrono **Node.js 22 o successivo** e un browser aggiornato con JavaScript e WebAssembly. Node 22 e Ubuntu 24.04 costituiscono l’ambiente della pipeline GitHub; Python 3.12 serve soltanto per i test Playwright. La consultazione del sito non richiede un’installazione locale di R.

Dopo aver estratto lo ZIP, aprire un terminale nella directory che contiene `package.json`:

```sh
npm ci --ignore-scripts
npm test
npm run test:dom
npm start
```

Aprire l’indirizzo locale stampato dal server, normalmente `http://127.0.0.1:4173/`. L’installazione npm riguarda gli strumenti di collaudo; la sola build usa le librerie standard di Node e può essere eseguita senza pacchetti npm:

```sh
npm run build
npm start
```

L’apertura diretta di `index.html` tramite `file://` non è supportata: moduli JavaScript, worker e risorse WebAssembly richiedono un server HTTP. Il server incluso ascolta soltanto sull’interfaccia locale ed è destinato allo sviluppo, non all’esposizione pubblica.

Il primo ingresso in un laboratorio scarica il motore R e i pacchetti dal medesimo sito; su una connessione lenta o un dispositivo con poca memoria può richiedere tempo. Durante l’avvio rimane disponibile una figura iniziale, esplicitamente distinta dal risultato ricalcolato. L’esecuzione viene interrotta dopo 60 secondi; il pulsante **Interrompi il calcolo** permette di riavviare il motore prima di tale limite.

## Pubblicazione su GitHub

Lo ZIP è un **repository sorgente completo**, non un file da caricare come pagina web. Estrarlo e trasferire il contenuto della cartella principale, comprese `.github`, `.gitignore` e `.nvmrc`, nella radice del repository GitHub. Non occorre pubblicare manualmente `dist/`: viene prodotto dalla pipeline.

Per un repository nuovo, dopo aver sostituito `OWNER` e `REPOSITORY` con i valori effettivi:

```sh
git init -b main
git add .
git commit -m "Initial release of GeoStat Lab"
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
```

Per un repository già esistente, lavorare su un branch e aprire una pull request, preservando la cronologia. Date le dimensioni del corso e il numero dei file, è preferibile Git o GitHub Desktop al caricamento manuale via browser. Nessun file del pacchetto supera il limite ordinario di 100 MiB per singolo oggetto Git.

1. In **Settings → Pages**, selezionare **GitHub Actions** come sorgente di pubblicazione.
2. Verificare che GitHub Actions sia abilitato e avviare **Verify and publish GeoStat Lab**, oppure eseguire il push su `main` o `master`.
3. Controllare che build, audit delle dipendenze, verifiche matematiche e test Chromium terminino correttamente. La pubblicazione dipende dal loro successo.
4. In **Settings → Pages**, abilitare **Enforce HTTPS**, quando disponibile. Per un dominio personalizzato configurare e verificare DNS e certificato secondo la documentazione GitHub.
5. Attivare le protezioni del repository descritte in [DEPLOYMENT.md](DEPLOYMENT.md), inclusa la segnalazione privata delle vulnerabilità.

Il workflow ricava automaticamente l’URL da GitHub Pages; i percorsi relativi supportano sia il dominio principale sia una sottocartella di progetto. In `config/site.json` si possono specificare autore (`author`), nome del sito principale (`mainSiteName`) e indirizzi `mainSiteUrl`, `repositoryUrl` e `siteUrl`; i valori non vuoti devono essere URL HTTPS. La build GitHub sovrascrive URL del sito e repository con i valori della pubblicazione.

Il laboratorio M15_N17 dimostra come escludere un file `.env` da Git. Il suo unico file dimostrativo contiene esclusivamente `SEGNAPOSTO_NON_SEGRETO`: viene ricreato da `npm test` e verificato contro il manifesto originale, senza leggere credenziali o sostituire contenuti diversi. `vendor/` conserva i byte originali anche su sistemi con fine riga differenti.

All’interno dello ZIP, `SHA256SUMS.txt` riporta l’impronta di ogni file e `RELEASE.json` identifica la revisione sorgente.

Il pacchetto non include credenziali, cronologia Git, identificativi della pubblicazione privata o dipendenze npm installate. Il sito distribuito con GitHub Pages va considerato pubblico: non inserire dati riservati nei materiali, nei file di configurazione o nei sorgenti.

## Uso dei laboratori e riproducibilità

Nel **percorso guidato** si formula una previsione e si confronta il risultato con il modello; nell’**esplorazione libera** si osservano i cambiamenti prodotti dai parametri; in **Formalismo e codice** si ricostruiscono il ragionamento matematico e il programma. Il confronto conserva due configurazioni insieme alle rispettive figure.

Il seme controlla la generazione pseudocasuale. Il risultato comprende versione di R e ggplot2, valori dei parametri e programma utilizzato. L’esportazione JSON conserva il contesto dell’esperimento; la sua importazione accetta soltanto il formato e l’attività previsti. Un programma personalizzato importato richiede sempre la revisione e l’esecuzione esplicita dall’editor.

Gli script autonomi in `R/experiments/` comprendono le funzioni comuni necessarie a riprodurre l’esperimento. Per i materiali originali R6 aprire invece `materiali/Corso_Geologia.Rproj` in RStudio: i relativi percorsi assumono `materiali/` come directory di lavoro. Le versioni effettivamente collaudate sono registrate nei manifesti; risultati ottenuti con versioni diverse possono presentare differenze numeriche o grafiche.

I CSV esportati neutralizzano le celle testuali che potrebbero essere interpretate come formule da un foglio elettronico, anteponendo un apostrofo. Le quantità numeriche negative restano numeriche. Per conservare esattamente un valore testuale che inizia con un segno di formula, utilizzare il JSON o il programma R.

## Architettura

| Percorso | Responsabilità |
|---|---|
| `src/` | Interfaccia, navigazione, grafica dei pianeti e gestione dei laboratori |
| `src/security.js` | Validazione di configurazioni, parametri, risultati, SVG e CSV |
| `content/experiments.json` | Catalogo scientifico, codice e controlli dei 139 esperimenti |
| `content/catalogue.json` | Indice delle unità e dei materiali |
| `moduli/` | Scheda e contenuto strutturato di ciascuna unità |
| `materiali/` | Consegna R6 originale: PDF, LaTeX, TikZ, R, Python, dati e verifiche |
| `R/` | Codice riproducibile dei nuovi esperimenti e tema grafico |
| `assets/` | Slide SVG, figure iniziali, texture e archivi scaricabili |
| `vendor/` | Distribuzioni locali di MathJax, webR e 23 pacchetti R, con licenze |
| `config/` | Configurazione del sito e politica di sicurezza della pagina |
| `security/` | Impronte delle dipendenze distribuite e requisiti Python con hash |
| `scripts/` | Build, verifica, server locale e preparazione della consegna |
| `tests/` | Test funzionali, matematici e di regressione della sicurezza |
| `.github/` | CI, pubblicazione Pages, CodeQL e Dependabot |
| `docs/` e `qa/` | Documentazione e rapporti di verifica |
| `dist/` | Output generato, escluso dal repository e dallo ZIP sorgente |

Il browser carica il catalogo, apre il laboratorio selezionato e avvia R in un worker. Parametri e codice producono tabelle, riepiloghi e figure ggplot2; l’interfaccia verifica il formato prima di mostrarli. Appunti e progresso restano nel `localStorage` del dispositivo. Non sono presenti backend applicativo, database, account degli studenti, analytics o servizi di caricamento dei loro dati.

## Sicurezza e modello di fiducia

La versione 3.1 introduce verifiche agli ingressi, controlli sui risultati e protezioni della distribuzione. La [documentazione di sicurezza](docs/SICUREZZA.md) descrive minacce, controlli, prove e limitazioni; [SECURITY.md](SECURITY.md) disciplina la segnalazione delle vulnerabilità.

| Superficie | Protezione implementata |
|---|---|
| URL e JSON importati | Formato, dimensioni, profondità, chiavi ammesse, tipi e domini dei parametri |
| Codice R personalizzato | Revisione esplicita prima dell’esecuzione; ricalcolo automatico disattivato all’importazione |
| Pagina web | Escaping dell’output, CSP senza JavaScript inline o `unsafe-eval`, SRI su script e stili |
| Risultati R | Contratto strutturale, limiti di righe, colonne, figure e dimensione |
| SVG scaricabili | Elementi grafici ammessi; rifiuto di script, eventi, contenuti HTML e riferimenti esterni |
| CSV | Neutralizzazione delle celle testuali interpretabili come formule |
| Calcoli e memoria | Interruzione manuale, scadenza del calcolo, limiti dell’output, eliminazione delle richieste obsolete |
| Server di sviluppo | Lettura soltanto, loopback, controllo Host, percorsi e symlink, MIME e header di sicurezza |
| Dipendenze | Versioni e hash, verifica dei file vendorizzati, lockfile npm e installazione senza lifecycle script |
| CI | Azioni dirette fissate a SHA, permessi minimi, separazione tra verifica e pubblicazione, diagnostica e aggiornamenti Dependabot |

**Confine di fiducia.** L’editor serve a eseguire programmi R intenzionalmente scelti dallo studente. Un worker non equivale a un sistema per analizzare codice ostile: non incollare programmi di provenienza sconosciuta e non usare dati sensibili. Il runtime Emscripten richiede valutazione dinamica di JavaScript nel worker; tale eccezione è separata dalla politica più restrittiva del documento principale.

**Hosting.** La CSP presente nell’HTML opera anche su GitHub Pages. Gli header HTTP aggiuntivi, compresi anti-framing e restrizioni del worker, richiedono invece un hosting o un proxy che li supporti: il solo file `_headers` non li attiva su GitHub Pages. La build produce `_headers` per piattaforme compatibili. Un dominio dedicato evita di condividere l’origine con altre applicazioni; WAF, protezione DDoS, TLS e sicurezza dell’account GitHub appartengono alla configurazione dell’infrastruttura.

Non viene dichiarata un’immunità agli attacchi, né una certificazione OWASP. L’audit npm copre le dipendenze npm conosciute dal registro alla data dell’esecuzione; non sostituisce il monitoraggio di R, WebAssembly, MathJax, browser e provider.

## Verifiche e manutenzione

| Comando | Verifica |
|---|---|
| `npm test` | Test Node, build, copertura dei materiali, protocollo HTTP e controlli di sicurezza |
| `npm run test:consistency` | Coerenza editoriale, schede dei moduli, copie del catalogo, archivi scaricabili e collegamenti locali |
| `npm run test:dom` | Navigazione, 1.730 espressioni matematiche, compatibilità SVG e blocco dell’esecuzione automatica del codice importato |
| `npm run test:security` | Regressioni degli ingressi e controllo di dipendenze, CSP, SRI e workflow; richiede `dist/` aggiornato |
| `npm audit --audit-level=high` | Vulnerabilità note delle dipendenze npm; richiede rete |
| `npm run test:browser` | Test Chromium, esecuzione R, navigazione e diagnostica; richiede l’ambiente Python previsto |
| `npm run labs:check` | Controlli scientifici R e invarianti, in un ambiente R nativo predisposto |
| `npm run check:course` | Verifica della consegna originale R6 |

Installazione dei soli strumenti browser su Ubuntu 24.04 con Python 3.12:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --require-hashes --only-binary=:all: -r security/requirements.txt
python3 -m playwright install --with-deps chromium
npm run test:browser
```

I test browser producono schermate, esito JSON e una traccia in `qa/browser/`; GitHub conserva la diagnostica per sette giorni anche quando il collaudo fallisce. CodeQL è configurato per repository pubblici; nei repository privati richiede il relativo servizio GitHub e l’abilitazione esplicita tramite variabile `ENABLE_PRIVATE_CODEQL=true`.

Dependabot propone aggiornamenti settimanali. Ogni modifica a webR, ai pacchetti R, alla CSP o a MathJax richiede un nuovo collaudo dei calcoli e delle formule, oltre all’aggiornamento motivato dei manifesti. Le impronte non devono essere rigenerate automaticamente per far passare una verifica fallita. La revisione strutturale 3.2.2 è documentata in [docs/REVISIONE_3_2_2.md](docs/REVISIONE_3_2_2.md); le successive correzioni sono in [CHANGELOG.md](CHANGELOG.md); i rapporti storici conservano la propria data e il proprio ambito.

## Moduli e spedizioni

| Codice | Unità didattica | Slide | Materiali |
|---|---|---:|---|
| T00 | [Dal codice al calcolo scientifico](moduli/T00/README.md) | 33 | [PDF](materiali/pdf/T00_R6.pdf) · [R](materiali/R/T00_figure.R) |
| M01 | [Pensare con i dati](moduli/M01/README.md) | 58 | [PDF](materiali/pdf/M01_R6.pdf) · [R](materiali/R/M01_figure.R) |
| M02 | [R e gestione dei dati](moduli/M02/README.md) | 43 | [PDF](materiali/pdf/M02_R6.pdf) · [R](materiali/R/M02_figure.R) |
| M03 | [Descrivere e visualizzare i dati](moduli/M03/README.md) | 33 | [PDF](materiali/pdf/M03_R6.pdf) · [R](materiali/R/M03_figure.R) |
| M04 | [Probabilità, variabilità e simulazione](moduli/M04/README.md) | 35 | [PDF](materiali/pdf/M04_R6.pdf) · [R](materiali/R/M04_figure.R) |
| M05 | [Campionamento, stima e incertezza](moduli/M05/README.md) | 105 | [PDF](materiali/pdf/M05_R6.pdf) · [R](materiali/R/M05_figure.R) |
| M06 | [Confrontare gruppi e valutare ipotesi](moduli/M06/README.md) | 35 | [PDF](materiali/pdf/M06_R6.pdf) · [R](materiali/R/M06_figure.R) |
| M07 | [Relazioni tra variabili e regressione](moduli/M07/README.md) | 33 | [PDF](materiali/pdf/M07_R6.pdf) · [R](materiali/R/M07_figure.R) |
| M08 | [Analisi multivariata dei campioni](moduli/M08/README.md) | 33 | [PDF](materiali/pdf/M08_R6.pdf) · [R](materiali/R/M08_figure.R) |
| M09 | [Serie temporali ambientali](moduli/M09/README.md) | 33 | [PDF](materiali/pdf/M09_R6.pdf) · [R](materiali/R/M09_figure.R) |
| M10 | [Previsione e progetto statistico](moduli/M10/README.md) | 33 | [PDF](materiali/pdf/M10_R6.pdf) · [R](materiali/R/M10_figure.R) |
| M11 | [Statistica spaziale](moduli/M11/README.md) | 32 | [PDF](materiali/pdf/M11_R6.pdf) · [R](materiali/R/M11_figure.R) |
| M12 | [Raster, telerilevamento e morfometria](moduli/M12/README.md) | 30 | [PDF](materiali/pdf/M12_R6.pdf) · [R](materiali/R/M12_figure.R) |
| M13 | [Cronologie e archivi sedimentari](moduli/M13/README.md) | 30 | [PDF](materiali/pdf/M13_R6.pdf) · [R](materiali/R/M13_figure.R) |
| M14 | [Estremi, pericolosità e rischio](moduli/M14/README.md) | 31 | [PDF](materiali/pdf/M14_R6.pdf) · [R](materiali/R/M14_figure.R) |
| M15 | [Riproducibilità e progetto di analisi](moduli/M15/README.md) | 27 | [PDF](materiali/pdf/M15_R6.pdf) · [R](materiali/R/M15_figure.R) |
| M16 | [Classificazione e validazione](moduli/M16/README.md) | 29 | [PDF](materiali/pdf/M16_R6.pdf) · [R](materiali/R/M16_figure.R) |
| P01 | [Geometria dei pori e permeabilità](moduli/P01/README.md) | 21 | [PDF](materiali/pdf/P01_R6.pdf) · [R](materiali/R/P01_figure.R) |
| P02 | [Foraminiferi, coppe e campagne](moduli/P02/README.md) | 22 | [PDF](materiali/pdf/P02_R6.pdf) · [R](materiali/R/P02_figure.R) |
| P03 | [Il Nilo: livelli e dipendenza temporale](moduli/P03/README.md) | 21 | [PDF](materiali/pdf/P03_R6.pdf) · [R](materiali/R/P03_figure.R) |
| P04 | [Un geyser: associazione e previsione](moduli/P04/README.md) | 21 | [PDF](materiali/pdf/P04_R6.pdf) · [R](materiali/R/P04_figure.R) |
| P05 | [CO₂: tendenza e calendario stagionale](moduli/P05/README.md) | 22 | [PDF](materiali/pdf/P05_R6.pdf) · [R](materiali/R/P05_figure.R) |
| P06 | [Dai campioni alla validazione spaziale](moduli/P06/README.md) | 17 | [PDF](materiali/pdf/P06_R6.pdf) · [R](materiali/R/P06_figure.R) |
| P07 | [Terreno, pendenze e sintesi territoriali](moduli/P07/README.md) | 17 | [PDF](materiali/pdf/P07_R6.pdf) · [R](materiali/R/P07_figure.R) |
| P08 | [Collocare nel tempo il massimo di un proxy](moduli/P08/README.md) | 18 | [PDF](materiali/pdf/P08_R6.pdf) · [R](materiali/R/P08_figure.R) |
| P09 | [Un livello raro e la sua incertezza](moduli/P09/README.md) | 16 | [PDF](materiali/pdf/P09_R6.pdf) · [R](materiali/R/P09_figure.R) |
| P10 | [Un’analisi ricostruibile e verificabile](moduli/P10/README.md) | 16 | [PDF](materiali/pdf/P10_R6.pdf) · [R](materiali/R/P10_figure.R) |
| P11 | [Classificare nuove stazioni sintetiche](moduli/P11/README.md) | 17 | [PDF](materiali/pdf/P11_R6.pdf) · [R](materiali/R/P11_figure.R) |

## Documentazione

- [DEPLOYMENT.md](DEPLOYMENT.md): pubblicazione, impostazioni GitHub e rollback.
- [SECURITY.md](SECURITY.md): gestione e segnalazione delle vulnerabilità.
- [CONTRIBUTING.md](CONTRIBUTING.md): modifiche al codice e ai contenuti scientifici.
- [CHANGELOG.md](CHANGELOG.md): modifiche della versione 3.2.3.
- [docs/SICUREZZA.md](docs/SICUREZZA.md): modello di minaccia e controlli.
- [docs/REVISIONE_3_2_2.md](docs/REVISIONE_3_2_2.md): rilievi, correzioni, verifiche e limiti della revisione 3.2.2.
- [docs/CORREZIONE_LAYOUT_3_1_2.md](docs/CORREZIONE_LAYOUT_3_1_2.md): correzione mobile e verifiche della versione 3.1.2.
- [docs/CONSOLIDAMENTO_3_1_1.md](docs/CONSOLIDAMENTO_3_1_1.md): revisione delle stratificazioni e collaudo della versione 3.1.1.
- [docs/COLLAUDO_SICUREZZA.md](docs/COLLAUDO_SICUREZZA.md): rapporto storico della revisione di sicurezza 3.1.0.
- [docs/LABORATORI_INTERATTIVI.md](docs/LABORATORI_INTERATTIVI.md): struttura didattica degli esperimenti.
- [docs/ARCHITETTURA.md](docs/ARCHITETTURA.md): organizzazione e aggiornamento dei contenuti.
- [docs/ATLANTE_PLANETARIO.md](docs/ATLANTE_PLANETARIO.md): grafica, navigazione e movimento.
- [Guida al corso](materiali/Guida_corso_R6.pdf). Il [rapporto di lavorazione R6](materiali/audit/Rapporto_revisione_R6.pdf) è conservato nei sorgenti per la manutenzione ed escluso dal sito e dal download didattico.

## Licenze, provenienza e attribuzioni

[LICENSE.md](LICENSE.md) conserva le condizioni dei materiali didattici; questa distribuzione non assegna automaticamente una licenza generale a tutti i contenuti. Le licenze delle componenti software, dei caratteri e delle texture sono indicate in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) e incluse nei rispettivi percorsi. Per webR e i pacchetti R sono riportati anche i riferimenti ai sorgenti corrispondenti.

L’organizzazione autonoma dei moduli riprende l’impostazione di [QuantumLab_Public](https://github.com/marzione00/QuantumLab_Public). I suoi programmi e contenuti non sono incorporati nel progetto. I pianeti hanno funzione illustrativa: superfici e velocità di rotazione non rappresentano osservazioni astronomiche.
