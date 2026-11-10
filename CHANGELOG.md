# Registro delle modifiche

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
