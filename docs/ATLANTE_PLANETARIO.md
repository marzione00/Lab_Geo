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
| Entra nel laboratorio | Apre gli esperimenti del modulo |
| Vista completa del sistema | Riporta la camera alla vista orbitale |
| Nuova configurazione | Estrae un’altra configurazione sintetica nella sessione |
| Torna alla galassia | Ritorna ai 17 sistemi |

Il trascinamento e le frecce sul canvas controllano azimut e inclinazione; più, meno e rotella regolano lo zoom della vista generale. Home ripristina la camera. I menu dei corpi rimangono utilizzabili anche quando un altro oggetto nasconde un pianeta nella proiezione. I richiami galattici hanno spaziatura calcolata per evitare sovrapposizioni.

`#indice` e `#mappa` aprono lo stesso navigatore. `#sistema-M01`, e gli altri identificatori del corso, aprono direttamente un sistema. Le rotte invalide sono rifiutate; `#catalogo` mantiene l’indice del corso. La nuova configurazione resta in memoria durante la sessione; ricaricare la pagina ripristina il seme iniziale. L’estrazione non modifica l’associazione fra modulo e pianeta.

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
| `src/galaxy.css` | Impaginazione delle due viste e adattamento alle larghezze |
| `src/planets.js` | Identità e caratterizzazione dei mondi didattici |
| `src/space-cpu.js` | Proiezione software delle texture sulle sfere |
| `src/space.js`, `src/planet.frag` | Pianeti nelle altre pagine del corso |
| `scripts/bake-planets.py` | Generazione riproducibile delle texture procedurali |

Le 27 superfici non terrestri sono rigenerate a 2048 × 1024, con dettagli aggiunti nel procedimento, non mediante interpolazione di un’immagine piccola. La Terra conserva le mappe 2048 × 1024 già attribuite a Solar System Scope. I 27 WebP procedurali occupano circa 7,0 MiB; vengono richiesti soltanto per i mondi rappresentati. La build ordinaria usa i file inclusi e non richiede Python o una GPU. La rigenerazione richiede moderngl, NumPy, Pillow e EGL.

La galassia usa fino a 120.000 stelle WebGL (60.000 sugli schermi stretti); la vista software ne campiona un terzo preservando i quattro bracci. La scena dei sistemi ha un campo stellare più leggero. Le sfere WebGL hanno 96 × 64 suddivisioni e filtri mipmap. Canvas applica luce stellare, campionamento bilineare nei primi piani e aggiornamento delle superfici a 20 Hz; la cache geometrica è limitata. Le sue occlusioni e atmosfere sono semplificate rispetto a WebGL.

Pausa, movimento ridotto e visibilità della scheda controllano l’animazione. La navigazione resta disponibile senza grafica. Lasciando una vista si eliminano frame, gestori e risorse del renderer. La perdita del contesto rende disponibili i comandi testuali; nella galassia il ripristino ricrea le risorse WebGL. Script, CSS e texture sono locali; le regole CSP/SRI e i vincoli della distribuzione restano attivi.

## Verifiche

`npm test` verifica i riferimenti fisici solari, la legge di Keplero, il bilancio radiativo, la riproducibilità, le 85 identità planetarie, l’unicità della destinazione di ciascun modulo, le rotte e la visibilità iniziale delle orbite a diverse larghezze, oltre ai controlli preesistenti.

`npm run test:dom` verifica i 17 sistemi e le 85 schede, l’accesso ai moduli e lo smontaggio delle scene. `npm run test:browser` include camera, pausa, trasferimento, pianeti e assenza di overflow a 320/390/430/768/1440 px. Il workflow GitHub esegue Chromium; non va confuso con un controllo eseguito localmente.

`python3 scripts/check-galaxy-shaders.py` compila e collega gli shader condivisi in EGL/OpenGL ES. `python3 scripts/check-planet-rendering.py` verifica i pianeti procedurali nelle altre pagine.

Per la verifica interattiva di questa revisione il browser disponibile usa Canvas 2D. La compilazione WebGL è verificata separatamente con EGL; la resa WebGL nel browser richiede un dispositivo che lo esponga.
