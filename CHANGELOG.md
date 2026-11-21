# Registro delle modifiche

## Modifiche successive alla 4.2.0

- Due licenze: materiali didattici CC BY-NC-SA 4.0, codice PolyForm Noncommercial 1.0.0 (`LICENSE-CODE.md`, con la riga Required Notice nelle intestazioni del codice R); esclusioni delle componenti di terzi in `LICENSE.md`; avviso nel piè di pagina, nelle pagine testuali e in `package.json`.
- Codice R degli esperimenti senza interruzioni di riga dentro le parentesi quadre: `scripts/labs/format-code.R` ricongiunge e riavvolge le righe e verifica che il programma analizzato resti identico; 15 esperimenti riformattati.
- Lezione Pelago (M05) a tappe: 109 tappe, una per slide, con la slide ricomposta in un pannello del sito (colonne, formule, 107 figure compilate dal sorgente TikZ), codice R eseguibile nel browser (`GeoREngine.runSnippet`) e laboratori con i parametri del codice; spiegazioni estese per le tappe 16-25; codice di tappa «Sul sito: Pelago · N» nel PDF e nel sorgente; quaderno di nove esercizi con verifica degli indicatori sul pianeta compagno Nereide c. Importatore in `scripts/lessons/`, prove in `tests/lessons.test.mjs` e `tests/dom.mjs`.
- Lezioni a tappe per tutte le diciassette presentazioni (T00, M01-M16): 1487 tappe, 1165 figure e 864 file di codice; codice di tappa nei PDF distribuiti. L’importatore legge anche il modello di T00 e M13-M16 (colonne `\Colonna`, diagrammi in file separati, riquadri con il codice e con l’uscita registrata, laboratori del piè di pagina con i parametri degli scenari A e B, script R6 dei materiali); i rimandi fra slide diventano collegamenti alle tappe e gli indirizzi del sito diventano relativi. La compilazione controlla collegamenti, figure e file delle lezioni.
- Uscite attese registrate in webR (`scripts/lessons/verify_webr.py`); i frammenti con pacchetti non disponibili nel browser conservano l’uscita di R sul computer. Nel codice delle tappe messaggi, avvisi ed errori compaiono nell’uscita (webR non li inoltrava al sink dei messaggi) e `help()` mostra la pagina di documentazione come testo. La compilazione del sito conserva il preludio dei frammenti (`R/stato_lezione.R` per M10-M12), prima sostituito da `setup.R`.
- Spiegazioni estese per tutte le tappe di Pelago (2-109), in prosa continua nello stesso riquadro del testo della slide; i valori citati sono calcolati in `content/lezioni/M05-valori.R`.
- Spiegazioni estese per tutte le tappe di Terra (2-84), con i valori calcolati in `content/lezioni/M01-valori.R` sui dati del progetto e sulle serie Meteostat di Roma Ciampino.
- Spiegazioni estese per tutte le tappe di Tellus (2-82), con i valori calcolati in `content/lezioni/M02-valori.R` sui file del progetto (provini, fossili, microsonda, censura) e sui generatori dei laboratori.
- Spiegazioni estese per tutte le tappe di Iride (2-79), con i valori calcolati in `content/lezioni/M03-valori.R` sui fossili, sulle rocce e sui generatori dei laboratori.
- Pianeti compagni: quaderni di Tellus, Iride, Aurea e Gemina accanto a quello di Pelago (48 schede) e 240 notebook svolti M01-M12, pubblicati in `notebook/` con i file che citano e con la stessa politica di sicurezza delle altre pagine. Le tappe di M10-M12 rimandano ai notebook citati nelle slide; nei notebook i rimandi alle pagine del PDF portano alle tappe.
- Tappe senza immagini della pagina: la copertina è ricomposta come testo del pannello (pianeta, modulo, titolo, sottotitoli, autore, licenza) e le 1165 figure sono portate sul pannello scuro da `scripts/lessons/figure_tone.py` (palette delle presentazioni sui token del sito, testo e tratti chiari, campiture invertite in modo monotono in OKLab, intestazioni di tabella scure con testo chiaro, scale continue e raster intatti). I grafici prodotti eseguendo il codice delle tappe ricevono la stessa trasformazione nel browser; lo scaricamento conserva l’SVG di R. La slide 3 di M01-M04 e M06, prima ritagliata dal PDF, è trascritta con riquadri, codice e diagramma TikZ.
- Nomi dei pianeti M10-M12 allineati alle presentazioni (Futura, Locus, Tessera); nelle briciole di pane il sistema porta il nome della stella; le regioni delle lezioni conservano acronimi e nomi propri.
- Escaping automatico del markup: tutte le viste usano `html```, che restituisce markup sicuro, mantiene il markup annidato e sfugge ogni interpolazione. ESLint vieta di assegnare `innerHTML` con valori diversi da `html```; Prettier non riformatta più il contenuto dei template.

## 4.2.0 – ambiente cosmico tridimensionale (15 novembre 2026)

- Galassia WebGL da 1.200.000 stelle, con worker, buffer trasferibili e cache fra le visite.
- Nucleo volumetrico, bracci, disco diffuso, alone e 18.000 particelle di gas galattico.
- Eliminato il fondale Canvas 2D: nebulose a densità 3D con emissione/assorbimento, 52.000 punti ambientali, fascia galattica e galassie lontane.
- Ambiente condiviso con la camera orbitale e mantenuto nel passaggio al dossier planetario.
- Risoluzione adattiva delle nebulose e ripristino del contesto WebGL nei sistemi.
- Shader e dati procedurali locali, senza nuove immagini o dipendenze runtime.
- Dettagli e collaudo: [docs/REVISIONE_4_2_0.md](docs/REVISIONE_4_2_0.md).

## 4.1.0: impianto grafico, briefing e audio di bordo

- Scala tipografica di sette gradini in rem (minimo 12 px) al posto di 31 dimensioni in pixel; 199 colori del testo ridotti a otto toni, con ruoli e superfici nominati e un test di contrasto WCAG AA.
- Intestazione da 190 a 102 px sui telefoni e da 151 a 105 px sui desktop; navigazione che scorre lateralmente; pulsante del movimento a icona.
- Home con la mappa galattica nella prima schermata e il testo introduttivo nel «Dossier della spedizione»; barra del sistema selezionato sugli schermi stretti; nessuno spostamento del layout.
- Catalogo degli esperimenti raggruppato per modulo (sul telefono da 34.646 a 2.728 px), barra degli strumenti visibile durante lo scorrimento, vista a elenco.
- Testo corrente limitato a 60ch, da 58 a 75 caratteri per riga.
- Briefing di cinque schede alla prima visita della home, con riquadro sull’elemento reale, tastiera, Esc e ritorno del focus; suggerimenti di una riga alla prima visita di sistemi, moduli e laboratori.
- Audio sintetizzato con la Web Audio API, spento per impostazione predefinita, caricato solo dopo il consenso; CSP invariata.
- Galassia con renderer CPU disegnata su richiesta, con campo stellare memorizzato: nessun task lungo a regime nella home.
- Dettagli, misure e scelte in [docs/REVISIONE_4_1_0.md](docs/REVISIONE_4_1_0.md).

## 4.0.0: revisione della qualità del codice e del sito

- Nessuno scorrimento laterale a 320 px; lo spostamento del layout al primo caricamento scende da 0,70–0,98 a non oltre 0,002.
- Con grafica software (SwiftShader, llvmpipe) o con fotogrammi lenti, pianeti e vista di sistema passano al renderer canvas; il thread principale resta libero.
- Campi estesi degli esperimenti e soluzioni ragionate caricati soltanto nelle viste che li usano: la parte comune della pagina scende da 1,11 MB a 0,63 MB, e da 314 a 188 KB compressi.
- Nessuna violazione axe-core sulle 254 rotte raggiungibili, a 390 e a 1440 px; codice e formule scorrevoli raggiungibili da tastiera; avviso quando il browser non conserva gli appunti.
- Escaping centralizzato in `src/html.js`, Trusted Types obbligatori nella CSP, verifica delle versioni dei pacchetti R rispetto al lock.
- Sorgenti formattati con Prettier; ESLint, Stylelint e Prettier in `npm test` con soglia di complessità non crescente; controllo dell’ordine delle dipendenze fra script; copertura misurabile; scomposte le cinque funzioni più complesse con verifica di equivalenza.
- CSS ripulito: 104 dichiarazioni inattive rimosse, una sola definizione della tavolozza, breakpoint da 14 a 11.
- Metadati Open Graph con immagine di anteprima, titoli dei laboratori e 29 pagine testuali senza script in `percorso/`; conteggi della pagina derivati dai dati.
- Dal controllo finale del pacchetto: la verifica dei pacchetti R interroga soltanto i pacchetti del lock e non scarica più 3,4 MB inutilizzati; il controllo dei fotogrammi lenti usa la mediana degli ultimi otto intervalli e interviene anche sulla pagina di modulo; l’anteprima verificata di un laboratorio resta leggibile mentre R la ricalcola.
- Dettagli e motivazioni in [docs/REVISIONE_4_0_0.md](docs/REVISIONE_4_0_0.md).

## 3.9.1 — Coerenza dei percorsi, delle soluzioni e dei risultati

- Rimosso il secondo navigatore per passi e il download duplicato nei terminali dei progetti; lettura autonoma degli esperimenti preservata.
- Configurazione stellare conservata nei collegamenti e nel ritorno dall’esplorazione, anche dopo ricaricamento.
- Interruzione efficace anche durante il caricamento del campione, con possibilità di ripetere il calcolo.
- Ordinamento dei sistemi di esopianeti indipendente dalla lingua del sistema operativo; anteprime, soluzioni e programmi riallineati.
- Controllo dei byte e dei membri dei cinque pacchetti osservativi, delle guide derivate e dei programmi scaricabili.
- Documentazione corrente riallineata alle funzioni disponibili; corretta la distinzione fra cinque missioni, sei temi astronomici e tredici famiglie. I 68 mondi condividono ancora cinque progetti.

## 3.9.0 — Soluzioni ragionate e terminali dei progetti

- Cinque mini-progetti con 23 passaggi spiegati ed eseguibili, suggerimenti progressivi, interpretazioni specifiche e programmi completi.
- Undici spedizioni del corso con 44 passaggi e script R formattati, equivalenti agli originali e scaricabili per RStudio; requisiti locali espliciti.
- Varianti modificabili ed esportabili, separate dall’interpretazione di riferimento. Tabelle dei risultati intermedi e stato dei risultati aggiornato dopo modifiche dei parametri.
- Guide testuali nei pacchetti delle cinque missioni. Nessun cambiamento ai dati, alle presentazioni o ai 139 esperimenti esistenti.

## 3.8.0 — Ambienti planetari e missioni su dati reali

- Tredici famiglie visive originali, livelli L1–L5 e texture 2K/4K.
- Cinque progetti osservativi con campioni ufficiali congelati, provenienza, formule, codice R commentato e pacchetti autonomi.
- Associazione coerente dei mondi complementari a missioni condivise dello stesso livello; identità dei pianeti del corso conservata.
- Verifica SHA-256 dei campioni, stato esplicito dei risultati dopo modifiche e annullamento del calcolo.
- 143 scenari R nativi; test aggiuntivi su famiglie, missioni, archivi e integrità dei dati.
- Compattazione dei soli SVG generati durante la build: 17,6 MB risparmiati, con confronto pixel per pixel identico per tutte le 1.123 slide e figure pubblicate. Sorgenti originali conservati.

## 3.7.0 — Percorso del corso ed esplorazioni complementari

- Distinzione visiva dei 17 mondi del corso e delle 68 destinazioni complementari mediante colore, anelli, simboli ed etichette testuali.
- Livello indipendente dall’appartenenza, preparazione consigliata e collegamenti diretti al modulo.
- Sei letture scientifiche riutilizzate per tipologia di mondo, con domande, confronto dei parametri sintetici, formule, fonti NASA/USGS ed esportazione CSV.
- Taccuino separato delle esplorazioni: salvataggio esplicito, conclusione per autovalutazione ed esportazione JSON, senza modificare il progresso del corso.
- Anteprime al puntamento e da tastiera, pulsanti di accesso e impaginazione adattiva. Nessuna nuova dipendenza.

## 3.6.0 — Paesaggio cosmico e terminale R

- Sfondo procedurale condiviso: nebulose, polveri, stelle con parallasse e galassie lontane; generazione della texture in un worker locale.
- Un solo comando di pausa per sfondo, pianeti e mappa, con rispetto del movimento ridotto e sospensione in background.
- Sorgente visibile in tutti i 139 esperimenti, commenti per istruzione, numeri di riga, parametri sincronizzati e lettura per passi.
- Download degli script completi con commenti, preservando le istruzioni R; spiegazioni del modello sospese per codice modificato.
- Caratteri originali del corso conservati; disposizione affiancata su desktop ampi e sequenziale su mobile.

## 3.5.0 — Narrazione scientifica e ricognizione di Pelago

La pagina iniziale introduce il motivo della spedizione e i 17 sistemi collegano la propria destinazione a una domanda scientifica. Il modulo M05 comprende nove sequenze narrative originali, articolate in tre fasi, con previsione prima del calcolo, interpretazioni riferite alle metriche R e raccordi fra attività. Le altre 130 attività conservano i testi didattici precedenti.

Il taccuino di Pelago registra soltanto configurazioni eseguite e salvate esplicitamente dall’utente, con parametri, osservazioni e due eventuali scenari. Le registrazioni rimangono nel browser e sono esportabili. Cambiamenti di parametri o codice invalidano il commento corrente; il codice personalizzato sospende l’interpretazione automatica del modello originale.

## 3.4.0 — Sistemi stellari e superfici planetarie

- Navigazione unificata: punti nella galassia, zoom nel sistema, esplorazione dei cinque pianeti e ingresso nel modulo.
- 17 sistemi sintetici e 85 pianeti, con stelle F/G/K/M estratte mediante seme riproducibile e nuova configurazione nella sessione.
- Parametri coerenti di luminosità, periodo e bilancio radiativo, formule esplicite, scale dichiarate e fonti scientifiche.
- Superfici procedurali rigenerate a 2048 × 1024; nuovi dettagli, campionamento bilineare e luce proveniente dalla stella nei sistemi.
- Eliminata la seconda mappa a schede: home e voce Mappa stellare condividono il navigatore.
- Verifiche dei modelli fisici, dei collegamenti dei 17 sistemi e delle 85 schede; shader compilati con EGL.

## 3.3.1 · 13 novembre 2026

- Ampliata la carta stellare e aumentata la popolazione da 24.000 a 120.000 stelle sul desktop; il modello per schermi stretti ne comprende 60.000. Aggiunte distribuzioni interbraccio, polveri più estese e maggiore varietà luminosa.
- Sostituite le etichette sovrapposte ai pianeti con richiami a segmenti e due colonne distanziate. Ogni destinazione riporta nome, codice e argomento; selezione e puntamento sono evidenziati in ambra.
- Ridisegnati cornice, controlli e scheda del modulo, con ritratto planetario e testi più grandi. La camera riserva spazio ai richiami e mantiene la rotazione dei mondi.
- Ottimizzata la proiezione software e limitato il suo aggiornamento a circa 30 fotogrammi al secondo. Verificati determinismo delle particelle, separazione delle etichette e navigazione.
- Riallineato il metadato di `symbol-tree` alla versione 3.2.4 del tarball già bloccato; aggiunto il controllo di coerenza fra versione e URL di ogni dipendenza npm.

## 3.3.0 · 13 novembre 2026

- Sostituita l’immagine della galassia con un modello tridimensionale: quattro bracci di particelle, nucleo volumetrico, pianeti sferici e anelli, con rotazioni indipendenti.
- Aggiunti camera prospettica, trascinamento, zoom, comandi da tastiera, ripristino della vista e avvicinamento al pianeta prima dell’apertura del modulo.
- Conservate le schede dei 17 moduli; aggiunto il menu delle destinazioni per raggiungere ogni pianeta anche in una vista affollata. La scena si adatta agli schermi stretti e rispetta la pausa e la preferenza per il movimento ridotto.
- Alternativa Canvas con le stesse coordinate spaziali, campionamento che conserva tutti i bracci e aggiornamento delle texture in pausa. Risorse e animazioni della galassia vengono liberate uscendo dalla home.
- Rimossi immagine e generatore della galassia precedente. Nessuna nuova dipendenza npm o CDN; asset locali, CSP e SRI rimangono in uso.
- Verificati modello e proiezione, navigazione, formule e controlli di sicurezza. Compilati e collegati i sei shader in OpenGL ES. Il browser disponibile ha consentito il collaudo della modalità Canvas; la resa WebGL nel browser non è stata verificata in questo ambiente.

## 3.2.4 · 10 novembre 2026

- Rigenerato `package-lock.json` dal registro pubblico npm mantenendo `jsdom@26.1.0`. Corretti la versione inesistente `@asamuzakjp/css-color@3.2.1` e il vincolo errato di `cssstyle@4.6.0`; la dipendenza risolta è `@asamuzakjp/css-color@3.2.0`.
- Installazione CI con cache dedicata al runner e registro esplicito; aggiunta la verifica dell'albero installato mediante `npm ls --all`. Restano attivi il blocco degli script di installazione e l'audit delle vulnerabilità.
- Aggiornate le istruzioni per l'errore E404. Le slide R6 e i programmi degli esperimenti conservano i contenuti della consegna precedente.
- Collaudo locale: riprodotto il 404 della 3.2.3; `npm ci` riuscito in una directory isolata con cache vuota, albero delle dipendenze valido e audit npm senza vulnerabilità note. Superati 24 test e i controlli DOM su 28 moduli e 1.730 espressioni. Verifica eseguita con Node 24.22.1 e npm 11.9.0; il workflow GitHub resta configurato per Node 22 e la suite Chromium sarà eseguita sul runner.

## 3.2.3 · 10 novembre 2026

- Rimosso il collegamento «Revisione delle slide» dal piè di pagina e i richiami al rapporto dal catalogo, dalla pagina Materiali e dall'indice HTML dei PDF.
- Rimosse le note di lavorazione dal lettore delle slide e i relativi metadati dai dati pubblicati.
- Rapporti, registri editoriali e file di lavorazione esclusi dalla distribuzione web e dal download didattico; originali conservati nei sorgenti del progetto.
- I manifesti pubblici descrivono ora soltanto i file realmente distribuiti. Un controllo della build impedisce di reintrodurre documenti o collegamenti editoriali nell'interfaccia.


## 3.2.2 · 10 novembre 2026

- Corrette le associazioni fra spedizioni e moduli preparatori, ora derivate dalle attività effettive.
- Eliminati 136 selettori obsoleti e l'alias della vecchia home; consolidate regole del pannello galattico e dimensioni responsive dei laboratori.
- Coordinate della galassia legate agli identificativi; settori e conteggi derivati dai cataloghi; etichette leggibili sul nucleo luminoso.
- Rigenerazione unica dei due ZIP scaricabili e del CSV; rimossi tre log di compilazione dal download R6. Il controllo rileva anche membri mancanti, aggiunti, duplicati e alterati.
- Aggiornati architettura e rimandi ai rapporti, distinguendo verifiche correnti e storiche.
- Collaudo: 23 test, 1.730 espressioni matematiche, 1.095 membri degli archivi e 28 percorsi controllati in Chromium a 1.363 e 340 pixel CSS senza overflow. Dettagli e limiti in [REVISIONE_3_2_2.md](docs/REVISIONE_3_2_2.md).


## 3.2.1 — 10 novembre 2026

- Attribuzione a Marzio De Corato nella barra introduttiva, nel piè di pagina e nei metadati della pagina.
- Collegamento a Topological Manifolds, il sito principale di cui GeoStat Lab è un modulo didattico, disponibile da ogni percorso.
- Autore, nome e indirizzo del sito principale centralizzati nella configurazione e inseriti nella pagina durante la build; rimosso il precedente inserimento del link tramite JavaScript.


## 3.2.0 — 10 novembre 2026

- Home trasformata in una galassia con 17 pianeti rotanti, cinque regioni e rotte illustrative.
- Selezione mediante puntatore, tocco e tastiera; scheda persistente e pulsante Viaggia collegati al catalogo del corso.
- Transizione avviata anche verso la Terra dalla home; selezioni accidentali durante gli spostamenti del mouse filtrate.
- Disposizione mobile in tre colonne, ritorno alla mappa e controlli di navigazione nel DOM virtuale e nella pipeline Chromium.
- Nessuna modifica ai metodi statistici, ai programmi R o ai materiali R6.

Validazione: `npm test` e `npm run test:dom`; controlli interattivi in Chromium sulle larghezze CSS 340, 681 e 1363. La suite completa Python/Playwright resta affidata alla pipeline GitHub e non è stata eseguita localmente per questa modifica della home.


## 3.1.2 — Correzione dell’ingombro dei pianeti

- Contenuto l’overflow dei riferimenti geometrici della Terra e dei pianeti nelle intestazioni, mediante un contenitore riservato alla decorazione. Testi e comandi restano esterni al ritaglio.
- Conservati geometria, dimensioni e motore WebGL delle rotazioni.
- Esteso il test Chromium a home, 28 moduli e lettura con formule a 320, 390, 430, 768 e 1440 px; invariata l’asserzione rigorosa sulla larghezza.
- Aggiunto `qa/browser/layout.json` agli artefatti diagnostici, con URL, larghezze ed elementi candidati in caso di errore.

## 3.1.1 — Consolidamento editoriale e del collaudo

- Corretto il confronto delle metriche: struttura, denominazioni, tipi, valori testuali e tolleranze numeriche; ogni discrepanza fa fallire l’attività.
- Riscritti i limiti generici di 121 esperimenti dopo confronto con i rispettivi algoritmi, conservando i 18 già specifici.
- Allineate le 28 schede dei moduli al percorso interattivo mediante generazione riproducibile.
- Unificate istruzioni di pubblicazione e preparazione del collaudo browser; rimossa l’anteprima iframe incompatibile con la CSP.
- Eliminate le pagine obsolete non richiamate dal routing; introdotto il controllo delle copie generate e degli archivi.
- Separati rapporti storici e prove della revisione corrente. Codici R, parametri e materiali R6 conservati.


## 3.1.0 — 10 novembre 2026

### Sicurezza applicativa

- Validazione rigorosa dei parametri, dei JSON importati e dei risultati R, con limiti di dimensione e rifiuto di chiavi pericolose.
- Blocco dell’esecuzione automatica di codice importato o modificato prima del comando esplicito nell’editor.
- Eliminazione delle richieste di calcolo obsolete, scadenza di avvio e calcolo, ripristino del runtime dopo codice personalizzato.
- Validazione degli SVG prima di mostrarli e scaricarli; neutralizzazione delle formule nei CSV.
- CSP della pagina rafforzata, integrità SRI per script e stili, restrizione delle estensioni TeX di MathJax.
- Server locale con controlli su metodi, Host, percorsi, file nascosti e collegamenti simbolici.

### Distribuzione e manutenzione

- Lockfile npm e requisiti Python con versioni e hash; Playwright aggiornato a 1.65.0 mantenendo Ubuntu 24.04 e Python 3.12.
- Verifica SHA-256 di 249 file vendorizzati e delle impronte ufficiali disponibili per webR e pacchetti R.
- Azioni GitHub dirette fissate a commit; Dependabot, CodeQL, audit npm e test di regressione della sicurezza.
- Generazione di header per hosting compatibili e documentazione dei limiti di GitHub Pages.
- README completo, politiche di sicurezza e contribuzione, guida operativa e archivio sorgente per GitHub.

### Conservazione dei contenuti

Restano disponibili i 139 esperimenti, le 11 spedizioni e tutti i materiali originali R6. Template, font, formule e codice scientifico non ricevono modifiche intenzionali in questa revisione. I controlli verificano la conservazione byte per byte della consegna originale.
