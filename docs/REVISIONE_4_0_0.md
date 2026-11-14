# Revisione della versione 4.0.0

Revisione del 14 novembre 2026. Ambito: qualità del codice, prestazioni, accessibilità, sicurezza difensiva e reperibilità del sito, a partire dall’analisi della versione 3.9.1. I materiali didattici R6, i dati, le slide e i 139 programmi R non sono stati modificati nel contenuto. La storia della revisione è suddivisa in commit per fase: correzioni immediate, prestazioni e accessibilità, sicurezza, manutenibilità, reperibilità.

## Rilievi e correzioni

| Rilievo nella 3.9.1 | Conseguenza | Correzione nella 4.0.0 |
|---|---|---|
| A 320 px la pagina P01 scorreva lateralmente di 51 px | La suite Chromium falliva e il CI non avrebbe pubblicato il rilascio | `overflow-wrap: anywhere` sugli elenchi della soluzione locale; suite completa superata |
| Spostamento del layout al primo caricamento fra 0,70 e 0,98 | La pagina si spostava sotto il lettore su quasi ogni rotta | Segnaposto senza margine collassante e `main` alto quanto la finestra; valore massimo misurato 0,002 |
| WebGL scelto anche con rasterizzazione software | Pagine di sistema e di modulo con il thread principale occupato per l’intera osservazione | Riconoscimento di SwiftShader e llvmpipe, passaggio al canvas quando la mediana degli ultimi otto intervalli tra fotogrammi supera 100 ms; override di collaudo `geostat:force-webgl` |
| Dati estesi e soluzioni caricati su ogni pagina | 653 KB di script non necessari alla navigazione | Campi estesi degli esperimenti e soluzioni ragionate caricati su richiesta con SRI |
| Cinque regole axe violate | Nomi accessibili diversi dal testo visibile, blocco scorrevole non raggiungibile da tastiera, contenuti fuori dai landmark, gerarchia dei titoli | Nessuna violazione axe-core 4.14 sulle 254 rotte raggiungibili, a 390 e a 1440 px |
| Nove copie della funzione di escaping | Correttezza affidata a ogni punto di inserimento dell’HTML | `src/html.js` con escaping unico, template con escaping automatico e politica Trusted Types predefinita, resa obbligatoria dalla CSP |
| Lock dei pacchetti R caricato senza verifica | Una deriva delle versioni sarebbe passata inosservata | Confronto dei pacchetti installati con `vendor/r-packages-lock.json` prima del primo calcolo |
| Sorgente compresso a mano, nessun lint nel CI | Differenze illeggibili, funzioni con complessità fino a 33 | Prettier, ESLint, Stylelint e soglia di complessità non crescente in `npm test`; le cinque funzioni più complesse scomposte |
| Dipendenze fra script implicite | L’ordine dei tag era l’unica documentazione | `scripts/check-modules.mjs` verifica che ogni lettura durante il caricamento abbia un proprietario precedente |
| Conteggi scritti a mano in pagina | Testi destinati a divergere dai dati | Conteggi derivati in build; il controllo di coerenza rifiuta i letterali |
| Un solo URL indicizzabile, nessuna anteprima dei collegamenti | Moduli ed esperimenti non reperibili | Metadati Open Graph, titoli dei laboratori, 29 pagine testuali senza script in `percorso/`, sitemap estesa |

## Controllo finale del pacchetto

Il pacchetto 4.0.0 è stato ricontrollato con gli strumenti dell’analisi iniziale, senza riusare la suite del progetto. Il controllo ha rilevato quattro difetti, corretti prima della pubblicazione.

| Rilievo nel pacchetto | Conseguenza | Correzione |
|---|---|---|
| Verifica dei pacchetti R basata su `installed.packages()` | La lettura dell’intera libreria montava `parallel`, `tcltk` e `translations`: 6 richieste e 3,4 MB in più al primo calcolo | Interrogazione dei soli 23 pacchetti del lock con `packageDescription`; stesse versioni rilevate, 46 richieste e 48,3 MiB come nella 3.9.1 |
| Controllo dei fotogrammi lenti con otto intervalli consecutivi oltre 120 ms | Con WebGL software forzato la pagina di modulo alternava intervalli di 117 e 133 ms, il contatore si azzerava e il thread principale restava occupato per 10 s su 10 | Mediana degli ultimi otto intervalli oltre 100 ms; passaggio al canvas entro due secondi; test unitario e controllo Chromium sulla pagina di modulo |
| Anteprima verificata di un laboratorio attenuata durante l’avvio di R | Nei 130 laboratori che avviano R all’apertura, testo a contrasto 3,4:1 fino al termine dell’avvio, circa 25 secondi; l’attenuazione dipendeva da quale richiesta terminava per prima (39 laboratori attenuati nella scansione a 390 px) | Attenuazione riservata ai risultati di una configurazione diversa da quella mostrata |
| Titoli senza livello intermedio e blocchi scorrevoli senza fermata da tastiera | Pagine dei codici, pagine delle spedizioni e formule larghe a 390 px segnalate da axe-core | Titoli di sezione per gli screen reader, `tabindex` sul codice e sulle formule che eccedono la colonna, contorno di focus comune |

## Scelte motivate

- **Moduli ES non adottati.** jsdom, usato da `npm run test:dom`, non esegue gli script `type="module"`. La migrazione avrebbe disattivato il controllo delle 1.190 formule e delle regressioni di sicurezza sul DOM. Le dipendenze restano globali ma sono dichiarate e verificate da `check-modules.mjs`; la copertura è misurabile con `npm run coverage`.
- **Ciclo dei pixel del renderer canvas.** `paint` è stato scomposto, ma il ciclo per pixel resta in `resampleSurface`: la versione suddivisa in funzioni per pixel è risultata circa il 20% più lenta in Chromium, e questo renderer serve proprio i dispositivi senza GPU.
- **Selettori CSS ripetuti fra file.** I gruppi di selettori presenti in più fogli scendono da 91 a 68. I rimanenti sono sovrascritture del tema spaziale su regole di base; unirli cambierebbe l’ordine della cascata.
- **Breakpoint.** Da 14 a 11 valori: 650 diventa 600, 800 diventa 850, 1100 diventa 1150 px. A 390, 768 e 1440 px le pagine restano identiche al pixel; negli intervalli 601–649, 801–849 e 1101–1149 px si applica il layout della fascia vicina, senza scorrimento laterale.
- **Lint del codice R.** Non aggiunto: l’immagine del CI non contiene R.

## Verifiche di equivalenza

- 36 schermate (12 rotte a 390, 768 e 1440 px, movimento ridotto) identiche al pixel dopo la pulizia del CSS e dopo i refactoring.
- 32 rotte renderizzate in jsdom con titolo e contenuto identici prima e dopo la scomposizione di `render`, `experiment` e `result` (`scripts/characterize-routes.mjs`).
- 480 impronte dei pixel del renderer canvas identiche dopo la scomposizione di `paint`; tempo per fotogramma invariato.

## Verifiche del rilascio

- `npm test`: 61 test Node, lint, ordine delle dipendenze, build, distribuzione con 29 pagine testuali, HTTP, sicurezza e coerenza.
- `npm run test:dom`: 28 moduli, 1.190 espressioni matematiche, 540 espressioni dei laboratori, 8 SVG ostili rifiutati.
- `npm run test:browser`: 18 gruppi di controlli in Chromium, compresi spostamento del layout, budget del thread principale, percorso WebGL forzato su sistema e modulo, axe-core su 11 rotte e i 139 esperimenti R con Trusted Types attivi.
- `npm audit --audit-level=high`: nessuna vulnerabilità nota.
