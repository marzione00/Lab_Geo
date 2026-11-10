# Revisione delle stratificazioni e delle incoerenze · 3.2.2

Revisione del 10 novembre 2026, successiva alla consegna 3.2.1. Il controllo riguarda sorgenti applicativi, navigazione, distribuzione, documentazione e copie generate. Le verifiche scientifiche precedenti conservano data e ambito propri.

## Problemi confermati e interventi

| Rilievo | Impatto | Correzione |
|---|---|---|
| Rimandi delle spedizioni conservati in una lista distinta dalle attività | P04 indicava M10, benché le attività utilizzino M07 e M06; P06 indicava anche M16, assente dalle sue attività; P10 ometteva M02 | I collegamenti «Moduli preparatori» derivano dalle attività effettive delle undici spedizioni. L'origine grafica dei loro pianeti è separata dalla relazione didattica |
| Stili della vecchia home e di componenti eliminati ancora presenti | Specificità artificiale e maggiore rischio di regressione a ogni modifica | Rimossi 136 selettori obsoleti; eliminato l'alias `orbital-home`; la galassia ha un solo componente e i propri stili |
| Regole desktop aggiunte dopo le regole responsive degli esperimenti | Dimensioni dei pianeti e altezza dell'intestazione mobile sovrascritte dalla coda del foglio | Ricondotte le dichiarazioni alle regole di base e alle rispettive soglie responsive |
| Coordinate dei pianeti associate per posizione nell'array | Un riordino del catalogo poteva spostare le destinazioni involontariamente | Coordinate associate agli identificativi; settori e conteggi della home ricavati dai cataloghi condivisi |
| Sfondo e sovrapposizione del pannello della galassia definiti da correzioni in fondo al file | Regole della stessa superficie distribuite in punti diversi | Riunite accanto al componente, conservando il livello del pianeta rispetto a sfondo e testo |
| Tre log di compilazione inclusi nell'archivio R6 scaricabile | Residui di lavorazione nella consegna | Esclusi dal download; i materiali originali restano intatti. Entrambi gli ZIP e il CSV sono ora rigenerati dallo stesso script |
| Controllo ZIP limitato ai membri presenti e con esclusione del LEGGIMI | Un archivio privo di un file o con membri duplicati poteva superare la verifica | Confronto dell'insieme completo dei membri, rifiuto dei duplicati, confronto dei byte di tutti i file, verifica CRC durante la lettura e controllo del CSV |
| README e architettura chiamavano «correnti» rapporti 3.1.1 e 3.1.2 | Evidenze storiche confondibili con collaudi della versione consegnata | Collegamento al presente rapporto; riferimenti storici identificati con la loro versione; documentata la galassia e la configurazione dell'autore |

## Verifiche della revisione

- `npm test`: superati 23 test, controlli di distribuzione e sicurezza, conservazione dei materiali R6 e coerenza dei contenuti.
- `npm run test:dom`: superati i percorsi dei 28 fascicoli e la composizione di 1.190 espressioni del corso e 540 dei laboratori; respinti 8 SVG ostili e accettate 150 figure R valide.
- Archivi: confrontati 1.095 membri complessivi e la mappa CSV, compreso il LEGGIMI generato.
- Chromium: i 28 percorsi dei moduli e delle spedizioni non producono overflow orizzontale a 1.363 e 340 pixel CSS; verificati la selezione della galassia, il viaggio verso M14, il ritorno alla mappa su schermo stretto e le dimensioni responsive del laboratorio M14. La larghezza di 340 pixel è ottenuta con zoom nativo al 400%, senza emulazione di un dispositivo mobile. Evidenza numerica in `qa/browser-layout-3.2.2.json`.
- Verifica visiva desktop della galassia: migliorato il contrasto delle etichette dei settori rispetto al nucleo luminoso.

Gli esiti aggiornati sono registrati in `qa/consistency.json`, `qa/dom.json` e nel changelog. I test degli archivi includono casi intenzionalmente mancanti, duplicati, aggiunti e alterati; quelli delle spedizioni controllano anche i tre casi di incoerenza sopra descritti. La prova DOM verifica i collegamenti delle schede, le 17 destinazioni, i 28 percorsi e la composizione delle formule.

## Limiti e materiale preservato

Questa revisione non costituisce una nuova rilettura visiva delle 861 slide, un ricalcolo integrale dei 139 esperimenti o un penetration test indipendente. I programmi R, i parametri scientifici, le figure, il testo didattico e il template originale non sono modificati. Le differenze di versione fra R nativo e webR sono dichiarate e intenzionali. La presenza di copie generate in cataloghi, script autonomi e archivi è necessaria per la distribuzione e viene verificata automaticamente.

La pipeline GitHub continua a usare il sistema operativo e le dipendenze browser fissati e conserva il controllo rigoroso dell'overflow. Il controllo locale non certifica l'esito di una nuova esecuzione GitHub Actions. L'attivazione di Pages rimane un'impostazione del repository, come descritto in [DEPLOYMENT.md](../DEPLOYMENT.md).
