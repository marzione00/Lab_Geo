# Contribuire a GeoStat Lab

## Prima della modifica

Aprire un branch dedicato e descrivere il problema o l’obiettivo. Per una vulnerabilità non corretta seguire SECURITY.md, evitando di esporre pubblicamente i dettagli. Le modifiche devono conservare il template delle presentazioni, la leggibilità delle figure, la notazione matematica e la coerenza fra narrazione, ipotesi e programma R.

## Contenuti scientifici

Ogni esperimento deve dichiarare domanda, modello, grandezze controllate, seme, interpretazione e limiti. Il codice deve produrre `data`, `metrics` e `plots`, rispettando il contratto del motore. Quando si modifica una formula o una procedura, verificare un caso noto e almeno un caso limite pertinente; aggiornare figure iniziali e script autonomi insieme al catalogo. Evitare test che si limitino a ripetere il codice modificato.

La prosa va redatta in italiano accademico, con passaggi argomentativi espliciti e periodi leggibili. Un testo deve permettere allo studente di ricostruire il ragionamento senza dipendere dalla spiegazione orale. Le nuove figure devono mantenere palette, dimensioni delle etichette e convenzioni del tema comune.

## Codice e sicurezza

Validare gli ingressi al confine; inserire testo mediante `textContent`, `GeoHTML.escape` oppure il template `GeoHTML.html`, che applica l’escaping a ogni valore. Non definire funzioni di escaping locali. Prima della pull request eseguire `npm run format` e `npm test`, che comprende `npm run lint` e `npm run check:modules`; un nuovo script che legge variabili globali durante il caricamento va inserito in `index.html` dopo lo script che le definisce. Non usare JSON importato come HTML, nome di funzione, URL di script o configurazione eseguibile. Non aggiungere CDN, analytics, credenziali o nuove connessioni senza descriverne la necessità e le conseguenze.

Per dimensioni e colori usare i gradini `--fs-1`…`--fs-7` e i toni nominati in `src/space.css`; `tests/contrast.test.mjs` rifiuta dimensioni di carattere in pixel e toni sotto il contrasto 4,5:1. I testi del briefing stanno in `content/briefing.json`: se cambiano in modo sostanziale, aumentare `version` perché il briefing venga riproposto.

Per una dipendenza distribuita in `vendor/`, verificare fonte ufficiale, versione, licenza e impronte; aggiornare i manifesti nella stessa pull request e collaudare il comportamento interessato. Un checksum identico dimostra l’integrità rispetto al manifesto, non l’assenza di vulnerabilità nel componente.

## Collaudo della pull request

```sh
npm ci --ignore-scripts
npm test
npm run test:dom
npm audit --audit-level=high
```

Per modifiche a runtime, CSP, output scientifici o interfaccia, completare anche il test Chromium previsto dalla pipeline. Gli aggiornamenti dei calcoli richiedono i controlli R nativi pertinenti. Descrivere nella pull request ciò che è stato verificato e ciò che non è stato eseguito, senza sostituire i risultati con dichiarazioni generiche di sicurezza.

Non includere `dist/`, `node_modules/`, ambienti virtuali, segreti, sessioni browser o dati personali. Il revisore deve poter ricostruire l’output dai sorgenti e dai manifesti inclusi.
