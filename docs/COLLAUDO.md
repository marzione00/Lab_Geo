# Collaudo della consegna

Questo documento conserva gli esiti della consegna iniziale del 9 novembre. Gli esperimenti interattivi e la pubblicazione successiva sono documentati in [COLLAUDO_LABORATORI.md](COLLAUDO_LABORATORI.md). Il collaudo automatizzato su GitHub Actions va verificato nel repository remoto effettivo.

Verifica del 9 novembre 2026. I controlli distinguono l’integrità del corso, il funzionamento del codice del portale e la verifica nel browser.

| Ambito | Esito della verifica locale |
|---|---|
| Catalogo | 17 moduli e 11 macroprogetti; 861 slide con numerazione continua |
| Materiali R6 | Corrispondenza SHA-256 con il manifesto originale |
| Testi e formule | Corrispondenza dei campi importati con i sorgenti del corso |
| Codici | 340 laboratori R e 20 Python, verificati mediante impronta dei file |
| Distribuzione | 861 slide SVG, 494 pannelli visuali e collegamenti ai materiali presenti |
| Funzioni del portale | Ricerca, rotte, limiti delle pagine e gestione del progresso: sei gruppi di test superati |
| DOM virtuale | Apertura delle 28 unità, selezione dei codici, navigazione e progresso verificati |
| Matematica | 1.190 espressioni, comprese quelle nel testo, elaborate da MathJax senza errori |
| Browser Chromium | Controllo predisposto nel workflow; non eseguito in questa consegna |
| GitHub Pages | Workflow predisposto; repository remoto e deployment non creati |

I 494 pannelli comprendono 262 impieghi di figure R e 232 diagrammi TikZ. Le figure R distinte sono 261, poiché una figura ricorre in due slide.

## Procedure correnti

Questo rapporto conserva le evidenze del 9 novembre e non prescrive l’ambiente delle revisioni successive. Per installazione e comandi usare il [README](../README.md), per CI e pubblicazione [DEPLOYMENT.md](../DEPLOYMENT.md), per gli esiti aggiornati [CONSOLIDAMENTO_3_1_1.md](CONSOLIDAMENTO_3_1_1.md).

## Limiti della verifica locale

Il controllo del DOM virtuale non misura il layout, il contrasto o l’applicazione della Content Security Policy da parte di Chromium. Le anteprime HTML rese come documenti sono servite come riscontro preliminare della composizione; il loro motore di impaginazione differisce da quello del browser.

L’ambiente di lavoro non ha consentito l’anteprima nel browser dei file locali. Di conseguenza, la verifica visiva del portale in Chromium, la resa su dispositivo mobile e il primo deployment sono indicati come attività ancora da completare. Il collaudo R6 delle slide e dei codici è conservato in `materiali/verifiche/` e `materiali/audit/`; questa riorganizzazione non ne modifica i file.
