# Atlante scientifico di GeoStat Lab

L’atlante organizza la navigazione su tre livelli: una galassia con 17 sistemi stellari, cinque pianeti in ciascun sistema e un mondo associato al modulo didattico. I contenuti del corso restano 139 esperimenti e 11 spedizioni applicative.

## Navigazione

| Azione | Risultato |
|---|---|
| Passaggio del puntatore o fuoco su un richiamo galattico | Mostra la scheda del sistema |
| Clic sul richiamo o sul punto stellare | Avvicina la camera e apre il sistema |
| Esplora il sistema | Esegue lo stesso trasferimento |
| Clic sul pianeta o sul suo nome nel menu | Apre il primo piano e la scheda scientifica |
| Localizza la destinazione | Seleziona il pianeta che ospita il modulo |
| Entra nel modulo | Apre gli esperimenti del modulo |
| Avvia il mini-progetto / Accedi all’osservatorio | Apre la missione su dati osservati e la sua soluzione R |
| Vista completa del sistema | Riporta la camera alla vista orbitale |
| Nuova configurazione | Estrae un’altra configurazione sintetica e aggiorna il collegamento |
| Torna alla galassia | Ritorna ai 17 sistemi |

Il trascinamento e le frecce sul canvas controllano azimut e inclinazione; più, meno e rotella regolano lo zoom della vista generale. Home ripristina la camera. I menu dei corpi rimangono utilizzabili anche quando un altro oggetto nasconde un pianeta nella proiezione. I richiami galattici hanno spaziatura calcolata per evitare sovrapposizioni.

`#indice` e `#mappa` aprono lo stesso navigatore. `#sistema-M01`, e gli altri identificatori del corso, aprono direttamente un sistema. Le rotte invalide sono rifiutate; `#catalogo` mantiene l’indice del corso. La configurazione è conservata nel parametro `?v=`, da 0 a 9999; il collegamento di ritorno dall’esplorazione mantiene lo stesso valore. Senza parametro si usa la configurazione già visitata nella sessione, oppure quella iniziale. L’estrazione non modifica l’associazione fra modulo e pianeta.

## Due percorsi, livelli indipendenti

Il corso è identificato da ciano, doppio anello e codice del modulo; gli approfondimenti complementari da ambra, simbolo disciplinare ed etichetta «Esplorazione». Il colore non è l’unico segnale. Schede, collegamenti da tastiera e menu mobili espongono preparazione consigliata e livello; nessun prerequisito impedisce l’accesso.

Le rotte `#esplorazione/M05-e?v=0` e analoghe conservano l’identificatore del mondo e la configurazione sintetica. I mondi principali vengono rifiutati da queste rotte, perché appartengono al percorso del corso. Le 68 destinazioni condividono cinque missioni su dati osservati, associate al livello didattico delle tredici famiglie planetarie. Ogni missione offre suggerimenti, soluzione ragionata, codice completo e pacchetto autonomo. Nei dettagli del modello sintetico restano sei temi astronomici di contesto: mondi rocciosi, vulcanici, temperati, gassosi, desertici e ghiacciati. I sei temi, i cinque progetti e le tredici famiglie descrivono aspetti differenti dell’atlante.

Il taccuino `#taccuino-esplorazioni` utilizza la chiave `geostat-explorations-v1`. Una registrazione richiede una risposta e un salvataggio esplicito; il completamento è una autovalutazione separata. Il semplice accesso non scrive dati. I valori importati dallo storage sono validati e il testo viene escapato prima della visualizzazione. L’esportazione JSON permette di conservare il lavoro; non è previsto un caricamento di annotazioni da file. Il taccuino del corso mantiene la copertura M05 già disponibile, senza estenderla implicitamente a tutti i moduli.

## Modello fisico e limiti

I sistemi sono immaginari. La scelta uniforme delle classi F, G, K e M serve alla varietà didattica e non rappresenta la distribuzione galattica delle popolazioni stellari. I parametri seguenti sono esempi plausibili, non valori universali di classe.

| Classe | Massa M☉ | Raggio R☉ | Temperatura K |
|---|---:|---:|---:|
| F V | 1,30 | 1,30 | 6500 |
| G V | 1,00 | 1,00 | 5772 |
| K V | 0,75 | 0,72 | 4700 |
| M V | 0,30 | 0,31 | 3400 |

La luminosità è calcolata con `L/L☉ = (R/R☉)² (T/5772 K)⁴`. Il periodo segue `P/anno = √[(a/UA)³ / (M/M☉)]`, trascurando la massa planetaria. Le orbite sono circolari; una sola scala temporale per sistema conserva i rapporti dei periodi. La rotazione assiale delle superfici è illustrativa.

La temperatura di equilibrio usa `278,3 K [(L/L☉)(1−A_B)/(a/UA)²]^(1/4)`. Ogni scheda espone la propria albedo di Bond. Si assumono emissività unitaria, redistribuzione uniforme del calore e assenza di effetto serra e calore interno. Il risultato non è una stima della temperatura superficiale e non determina l’abitabilità.

I raggi grafici sono ingranditi e le separazioni orbitali sono scelte per la leggibilità; i valori fisici sono nelle schede. Le superfici sono illustrative e non permettono di dedurre composizione o età. Anche il nome Terra identifica qui un mondo didattico, non una ricostruzione del Sistema solare.

### Fonti

- [NASA — Stars in an Exoplanet World](https://science.nasa.gov/exoplanets/stars/)
- [NASA — Orbits and Kepler’s Laws](https://science.nasa.gov/solar-system/orbits-and-keplers-laws/)
- [NASA Exoplanet Archive — Calculated Parameters](https://exoplanetarchive.ipac.caltech.edu/docs/pscp_calc.html)

## Sorgenti

| File | Responsabilità |
|---|---|
| `src/astro-model.js` | Sistemi, estrazione deterministica, parametri e relazioni fisiche |
| `src/galaxy-model.js` | Coordinate galattiche, particelle, proiezione e disposizione dei richiami |
| `src/galaxy-scene.js` | Renderer condivisi WebGL/Canvas e camera della galassia |
| `src/system-scene.js` | Orbite, luce stellare, camera e primi piani |
| `src/galaxy.js` | Navigatore, schede, formule, fonti e collegamenti al corso |
| `src/planet-families.js` | Tredici famiglie, livelli L1–L5 e selezione delle texture 2K/4K |
| `src/research-projects.js` | Missioni osservate, controlli, esecuzione e download |
| `src/solution-terminal.js` | Suggerimenti, passaggi scientifici e programmi completi |
| `src/learning-paths.js` | Percorsi, livelli, preparazione, letture e fonti |
| `src/explorations.js` | Confronti, annotazioni ed esportazioni delle esplorazioni |
| `src/learning-paths.css` | Segnali visivi dei percorsi e pagine complementari |
| `src/galaxy.css` | Impaginazione delle due viste e adattamento alle larghezze |
| `src/planets.js` | Identità e caratterizzazione dei mondi didattici |
| `src/space-cpu.js` | Proiezione software delle texture sulle sfere |
| `src/space.js`, `src/planet.frag` | Pianeti nelle altre pagine del corso |
| `scripts/bake-planets.py` | Generazione riproducibile delle texture procedurali |

Le 27 superfici non terrestri sono rigenerate a 2048 × 1024, con dettagli aggiunti nel procedimento, non mediante interpolazione di un’immagine piccola. La Terra conserva le mappe 2048 × 1024 già attribuite a Solar System Scope. I 27 WebP procedurali occupano circa 7,0 MiB; vengono richiesti soltanto per i mondi rappresentati. La build ordinaria usa i file inclusi e non richiede Python o una GPU. La rigenerazione richiede moderngl, NumPy, Pillow e EGL.

Le famiglie complementari aggiungono tredici superfici originali in 2K e 4K; il primo piano WebGL desktop può caricare progressivamente il dettaglio maggiore. Mobile e rendering software usano il livello 2K. Provenienza e generazione sono descritte in [planet-family-assets.md](planet-family-assets.md).

La galassia usa fino a 120.000 stelle WebGL (60.000 sugli schermi stretti); la vista software ne campiona un terzo preservando i quattro bracci. La scena dei sistemi ha un campo stellare più leggero. Le sfere WebGL hanno 96 × 64 suddivisioni e filtri mipmap. Canvas applica luce stellare, campionamento bilineare nei primi piani e aggiornamento delle superfici a 20 Hz; la cache geometrica è limitata. Le sue occlusioni e atmosfere sono semplificate rispetto a WebGL.

Pausa, movimento ridotto e visibilità della scheda controllano l’animazione. La navigazione resta disponibile senza grafica. Lasciando una vista si eliminano frame, gestori e risorse del renderer. La perdita del contesto rende disponibili i comandi testuali; nella galassia il ripristino ricrea le risorse WebGL. Script, CSS e texture sono locali; le regole CSP/SRI e i vincoli della distribuzione restano attivi.

## Verifiche

`npm test` verifica i riferimenti fisici solari, la legge di Keplero, il bilancio radiativo, la riproducibilità, le 85 identità planetarie, l’unicità della destinazione di ciascun modulo, le rotte e la visibilità iniziale delle orbite a diverse larghezze, oltre ai controlli preesistenti.

`npm run test:dom` verifica i 17 sistemi e le 85 schede, l’accesso ai moduli e lo smontaggio delle scene. `npm run test:browser` include camera, pausa, trasferimento, pianeti e assenza di overflow a 320/390/430/768/1440 px. Il workflow GitHub esegue Chromium; non va confuso con un controllo eseguito localmente.

`python3 scripts/check-galaxy-shaders.py` compila e collega gli shader condivisi in EGL/OpenGL ES. `python3 scripts/check-planet-rendering.py` verifica i pianeti procedurali nelle altre pagine.

I rapporti di revisione indicano il renderer e l’ambiente effettivamente verificati. Il controllo tramite Canvas 2D e la compilazione degli shader con EGL non equivalgono a una verifica visiva WebGL su un dispositivo fisico.
