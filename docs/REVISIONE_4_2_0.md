# GeoStat Lab 4.2.0 — ambiente cosmico 3D

Data: 15 novembre 2026. Rendering sviluppato sull’archivio 4.1.0 «solo effetti» e integrato nella repository Lab_Geo. Le modifiche ad audio, briefing e navigazione già presenti su GitHub sono conservate.

## Risultato

Il fondale precedente, calcolato in un'immagine Canvas 2D e traslato sullo schermo, è sostituito da un ambiente WebGL. Tutti i nuovi elementi sono generati da codice: nessuna immagine IA, fotografia di sfondo, cubemap o risorsa remota. Le texture dei pianeti già presenti nel progetto restano quelle originali.

| Componente | Implementazione |
| --- | --- |
| Galassia | 1.200.000 stelle con coordinate 3D, nucleo gaussiano, quattro bracci, disco diffuso e alone. Nessuna riduzione del conteggio sui dispositivi stretti. |
| Gas galattico | 18.000 particelle distribuite lungo i bracci, con sfumature fredde e regioni calde. |
| Ambiente lontano | 52.000 punti: campo stellare, fascia galattica e tre galassie lontane a particelle. |
| Nebulose | Tre regioni volumetriche di densità procedurale, rumore 3D deformato, filamenti, emissione e assorbimento. Integrazione lungo i raggi della camera in 56 passi. |
| Continuità | Galassia e sistema usano lo stesso renderer ambientale. Durante l'avvicinamento al pianeta l'ambiente segue la camera; il dossier conserva l'ultima posa del sistema. |

Le coordinate e le scale sono illustrative. Non si tratta di una simulazione astrofisica o di un catalogo osservativo. La polvere scura del fondale attenua il campo stellare posto dietro i volumi; le discontinuità scure dei bracci sono anche modellate nella luminosità delle stelle galattiche. Non viene simulata una dinamica dei gas.

## Struttura e costo

- `src/galaxy-model.js`: genera buffer interlacciati; il buffer delle stelle occupa 38.400.000 byte. Una promessa conserva il catalogo per le visite successive.
- `src/cosmos-worker.js`: costruisce il catalogo fuori dal thread dell'interfaccia e trasferisce i buffer. Se il worker non è disponibile, il calcolo locale garantisce gli stessi dati.
- `src/universe.js`: pass stellare e ray marching volumetrico condivisi; risorse e shader WebGL 1 locali.
- `src/cosmos.js`: fondale persistente 3D, aggiornato quando cambia la posa della camera o la dimensione della finestra.
- `src/galaxy-scene.js` e `src/system-scene.js`: integrazione ambientale, caricamento progressivo e gestione delle risorse.

Solo il pass volumetrico viene calcolato a risoluzione ridotta (larghezza massima iniziale 640 pixel, 400 quando il sistema rileva fotogrammi lenti). Il risultato viene ricomposto con stelle a piena risoluzione. A camera ferma il volume viene riutilizzato: non cambia nel tempo. Le nebulose restano volumi 3D anche quando il loro pass intermedio usa una texture renderizzata dalla GPU.

L'avvio e il ripristino di un contesto WebGL caricano le risorse prima di mostrare il conteggio finale. L'API `GeoGalaxy.debug()` espone il numero di stelle effettivamente caricato; il test del renderer controlla anche l'invio di 1.200.000 punti alla GPU.

Il percorso preesistente di compatibilità software conserva un catalogo ridotto quando WebGL non è disponibile o viene riconosciuto un rasterizzatore software. Quel percorso non equivale al profilo completo da 1,2 milioni di punti. Nessun limite di fluidità viene garantito senza una misura sul dispositivo reale.

## Verifica

- Suite Node, lint, ordine dei moduli, build, distribuzione, HTTP, sicurezza e coerenza del progetto.
- Test dedicati a quantità, memoria, determinismo e finitezza delle coordinate; trasferimento dei buffer nel worker; invio dei punti e rilascio delle risorse GPU.
- DOM virtuale: navigazione e formule; controlli SVG e importazione sicura.
- Compilazione e collegamento degli shader reali con EGL/OpenGL ES: stelle, sfere, linee, volumi, ambiente e ricomposizione.
- Ispezione visiva della galassia e dei fondali usando gli stessi dati e shader con Mesa/llvmpipe. Corrette concentrazione del nucleo, intensità della polvere luminosa e disposizione dei volumi rispetto alla camera.

Il browser Chromium di collaudo non è stato avviabile nell'ambiente di lavoro. La verifica EGL e il DOM virtuale non sostituiscono una prova completa in browser o misure di FPS su GPU fisica. Per ripetere il controllo GLSL: `python3 scripts/check-galaxy-shaders.py` (richiede Mesa EGL).

## Avvio

Dalla cartella estratta, con Node.js 22 o successivo e Python 3:

```sh
npm ci --ignore-scripts
npm run build
npm start
```

Aprire l'indirizzo locale indicato dal server. Per la verifica completa del progetto eseguire `npm test` e `npm run test:dom`.
