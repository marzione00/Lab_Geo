# Rapporto di collaudo della sicurezza

> Rapporto storico. Il collaudo browser originario confrontava soltanto le coppie di valori numerici finiti e non verificava integralmente nomi, cardinalità e tipi delle metriche. Il consolidamento 3.1.1 corregge questo limite; le prove aggiornate sono riportate in [CONSOLIDAMENTO_3_1_1.md](CONSOLIDAMENTO_3_1_1.md).

**GeoStat Lab 3.1.0 · 10 novembre 2026**

La revisione ha interessato i confini dell’applicazione statica e la preparazione della pubblicazione GitHub. Le prove sono state eseguite sul checkout consegnato; non costituiscono un penetration test indipendente né una certificazione. I risultati dei componenti precedenti del corso sono conservati nei rispettivi rapporti storici.

## Prove completate

| Prova | Esito osservato |
|---|---|
| Test Node | 17 gruppi superati: copertura, materiali, rotte, parametri e regressioni di sicurezza |
| Conservazione R6 | Verifica byte per byte superata; 28 fascicoli e 861 slide conservati |
| Build e distribuzione | Risorse e collegamenti richiesti presenti; nessun segnaposto irrisolto |
| Test HTTP locale | MIME ES module/WASM, errori, metodi, Host estranei, traversal codificato, NUL, file nascosti e symlink verificati |
| DOM e matematica | 28 unità, 1.190 espressioni del corso e 540 dei laboratori verificate |
| SVG | 8 payload ostili respinti; 150 figure iniziali valide accettate; verificati anche identificativi clipPath prodotti da svglite |
| Importazione del codice | Il JSON e il comando ordinario non eseguono il programma importato; il comando esplicito dall’editor consente l’esecuzione |
| Integrità | 249 file vendorizzati, manifesti upstream webR e 23 archivi R verificati |
| Audit npm | 39 dipendenze di sviluppo; nessuna vulnerabilità nota segnalata dal registro nell’esecuzione documentata |
| Browser: intero catalogo R | **139 esperimenti superati, 0 errori; 150 SVG generati e validati** |
| Confronto numerico browser/R nativo | Nessuna differenza oltre la soglia del collaudo: massimo fra 10⁻⁵ e 2,5% della scala del valore |
| Browser: modifica dei parametri | M05 copertura osservata 0,935 con correlazione 0; 0,38 con correlazione 0,3 |
| Browser: codice modificato | Il comando ordinario ha mostrato la richiesta di revisione; il programma è partito solo dal comando dedicato |
| Browser: calcolo infinito | `while (TRUE) {}` arrestato dal limite di 60 secondi |
| Browser: recupero dopo arresto | Ripristino del codice e nuovo risultato R completato, copertura 0,935 |

I 139 esperimenti sono stati eseguiti in Chromium mediante la pagina di collaudo del progetto, che usa il medesimo motore e i medesimi programmi del sito. Il rapporto completo per attività è in [qa/security-browser-experiments.json](../qa/security-browser-experiments.json). La verifica comprende la validazione degli SVG live; non si limita alle figure iniziali precalcolate.

Le soglie di confronto numerico permettono di rilevare differenze rilevanti tra versioni dell’ambiente e non equivalgono a una dimostrazione generale di correttezza statistica. I controlli scientifici nativi più estesi della revisione precedente sono descritti in [COLLAUDO_LABORATORI.md](COLLAUDO_LABORATORI.md).

Lo ZIP viene inoltre estratto in una directory separata, aggiunto a un nuovo repository Git e ricostruito dai file che Git effettivamente conserva; `npm test` verifica anche questa copia. Ciò controlla esclusioni, file necessari e conservazione delle impronte dopo il checkout. Il solo `.env` didattico ignorato dal laboratorio M15_N17 è ricreato dal valore pubblico documentato e confrontato con il manifesto R6.

## Evidenze riproducibili

- `qa/security.json`: inventario e controlli strutturali.
- `qa/npm-audit.json`: risultato dell’audit npm.
- `qa/dom.json`: verifica del DOM e delle espressioni matematiche.
- `qa/security-browser-experiments.json`: esito reale di ciascuno dei 139 esperimenti nel browser.
- `tests/security.test.mjs` e `tests/security-dom.mjs`: regressioni degli ingressi, degli SVG e dell’importazione.
- `scripts/check-http.mjs`: prove delle richieste HTTP e delle risposte del server locale.
- `tests/browser.py`: collaudo GitHub predisposto, comprensivo dell’intero catalogo e della diagnostica.

## Prove non eseguite e limiti

- Il workflow completo GitHub Actions e CodeQL **non sono stati eseguiti nel repository GitHub dell’utente**. Sono inclusi e devono risultare verdi dopo il caricamento.
- Non sono stati eseguiti test DDoS, scansioni di infrastrutture altrui, verifiche degli account GitHub o delle impostazioni DNS/TLS del dominio finale.
- L’audit npm non copre esaustivamente R, WASM, MathJax, driver grafici o browser. Le impronte SHA-256 sono controlli d’integrità, non attestazioni di assenza di CVE.
- Le prove browser documentate riguardano Chromium; non attestano un nuovo collaudo completo di Safari o Firefox su tutti i dispositivi.
- Gli header configurati nel server locale non dimostrano che un provider li applichi in produzione. Su GitHub Pages il file `_headers` non sostituisce una configurazione del server.
- Il runtime R non è un ambiente di analisi per codice ostile. I limiti applicativi non impongono una quota rigida alla memoria del browser.

Per interpretare correttamente questi risultati consultare [SICUREZZA.md](SICUREZZA.md), [SECURITY.md](../SECURITY.md) e [DEPLOYMENT.md](../DEPLOYMENT.md).
