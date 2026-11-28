# Oggetti notevoli della galassia

La galassia dell’atlante ospita cinque oggetti estremi, ciascuno con una pagina propria: una scena tridimensionale WebGL2, una scheda con i valori fisici calcolati dal modello, una spiegazione, i collegamenti con il corso e le fonti. Gli oggetti sono immaginari; le leggi che ne descrivono l’aspetto sono quelle della letteratura citata.

| Rotta | Oggetto | Scena |
|---|---|---|
| `#oggetto-buco-nero` | Erebo, buco nero di Schwarzschild di 4,3 × 10⁶ M☉ al centro della galassia | Cielo deviato lungo le geodetiche, disco di accrescimento con immagini primaria, secondaria e terziaria, corona, getti relativistici, traiettorie della luce |
| `#oggetto-pulsar` | Faro, pulsar con P = 40 ms e Ṗ = 5 × 10⁻¹³ | Stella di neutroni con calotte polari, plasma sulle linee di dipolo chiuse, fasci a cono cavo, cilindro di luce, foglio di corrente del vento |
| `#oggetto-asteroidi` | Lapis, stella di una massa solare con un gigante a 5,2 UA | Fascia kepleriana con lacune di Kirkwood, gruppo di Hilda, Troiani in L4 e L5; asteroide craterizzato con satellite |
| `#oggetto-cometa` | Clio, cometa con perielio 0,6 UA ed eccentricità 0,97 | Code di polvere e di ioni lungo l’orbita; nucleo a due lobi con getti dalle regioni attive |
| `#oggetto-binaria` | Diade, nana bianca di 0,8 M☉ e nana rossa di 0,25 M☉, P = 3,2 h | Lobo di Roche, flusso balistico da L1, disco con bracci di marea e punto caldo, curva di luce con eclisse |

Nella galassia ogni oggetto ha un marcatore che segue la rotazione dei bracci; sotto la mappa una sezione raccoglie le cinque schede. Le etichette dei sistemi del corso restano sopra i marcatori.

## Modelli fisici

I valori delle schede sono calcolati in `src/objects-model.js` con le costanti CODATA 2018 e i valori nominali IAU 2015.

**Erebo.** Raggio di Schwarzschild 2GM/c², sfera dei fotoni a 3GM/c², ombra con parametro d’impatto critico 3√3 GM/c², orbita stabile più interna a 6GM/c². Il flusso del disco segue la forma chiusa di Page e Thorne (1974) per un buco nero non rotante; con un accrescimento pari al 10% del limite di Eddington il massimo vale circa 1,5 × 10⁵ K a 9,55 r_g. Le temperature mostrate sono moltiplicate per un fattore costante che porta il massimo a 7500 K; i rapporti restano quelli calcolati. Il fattore di frequenza di una particella in orbita circolare è g = √(1 − 3/r) / [√(1 − 2/r_c)(1 − Ωλ)], e la luminosità di ogni immagine cresce come g⁴.

**Faro.** Campo di dipolo nel vuoto B = 3,2 × 10¹⁹ (PṖ)^(1/2) G, età caratteristica P/(2Ṗ), potenza di frenamento 4π²IṖ/P³ con I = 10³⁸ kg m², cilindro di luce cP/2π, calotte polari di raggio R(R/R_L)^(1/2). Il profilo degli impulsi usa la geometria del vettore rotante con due fasci gaussiani; il foglio di corrente segue la latitudine arctan[tan χ sin(φ − Ω(t − r/c))] del monopolo diviso inclinato (Bogovalov 1999).

**Lapis.** Terza legge di Keplero, risonanze di moto medio a = a_G (q/p)^(2/3). La distribuzione dei semiassi ha lacune alle risonanze 3:1, 5:2, 7:3 e 2:1; gli asteroidi di Hilda hanno longitudine del perielio λ_G0 − 2M₀/3, condizione della risonanza 3:2; i Troiani hanno longitudine media 60° avanti o indietro rispetto al gigante.

**Clio.** Equazione di Keplero risolta con il metodo di Newton; vis viva per le velocità; attività proporzionale a 1/r² entro 3 UA. I grani di polvere hanno rapporto β fra pressione di radiazione e gravità da 0,02 a 1 e si muovono sotto la gravità ridotta (1 − β)GM (Finson e Probstein 1968); gli ioni seguono il vento stellare a 400 km/s nella direzione antisolare corretta per la velocità della cometa.

**Diade.** Separazione dalla terza legge di Keplero, lobi di Roche di Eggleton (1983), punto L1 dalla derivata del potenziale di Roche, raggio di circolarizzazione (1 + q)(0,5 − 0,227 log q)⁴ (Warner 1995). La curva di luce somma l’emissione del disco, del punto caldo e della nana bianca e nasconde i punti coperti dalla sfera di raggio pari al lobo della nana rossa. Il flusso balistico è integrato fino al bordo del disco, a 0,369 volte la separazione dalla nana bianca (0,765 volte il suo lobo); lì si trova il punto caldo, la cui emissione cresce con la proiezione sulla linea di vista della normale opposta alla velocità del flusso rispetto al gas del bordo. La normale forma un angolo di 47° con la congiungente delle stelle e la gobba orbitale culmina alla fase 0,87, nell’intervallo 0,8–0,9 osservato nelle binarie cataclismiche a eclisse. Con il lobo di Roche al posto della sfera, la nana bianca è eclissata sopra 74,6° di inclinazione (73,5° con la sfera).

## Rendering

`src/objects-engine.js` crea un contesto WebGL2 con un buffer HDR a mezza precisione e multicampionamento 4×, un bloom a catena di mipmap (Jimenez 2014) e la curva ACES; la volta stellare dell’atlante è disegnata nello stesso buffer, o in una cube map per il buco nero. Le particelle non hanno buffer di attributi: posizione, colore e luminosità derivano dall’indice del vertice con una funzione di hash nel vertex shader. Le mesh dense sono costruite in `src/objects-geometry.js` da un worker.

| Elemento | Alta | Media | Bassa |
|---|---:|---:|---:|
| Disco di Erebo (particelle) | 3.200.000 | 1.100.000 | 180.000 |
| Corona e getti di Erebo | 1.320.000 | 470.000 | 90.000 |
| Plasma, fasci e vento di Faro | 3.400.000 | 1.240.000 | 220.000 |
| Asteroidi di Lapis | 1.600.000 | 600.000 | 120.000 |
| Polvere e ioni di Clio | 2.100.000 | 780.000 | 140.000 |
| Disco e flusso di Diade | 1.760.000 | 660.000 | 124.000 |
| Asteroide, nucleo, nana rossa (triangoli) | 327.680 | 327.680 | 81.920 |

Il livello dipende dal rasterizzatore e dal dispositivo: i rasterizzatori software usano il livello basso, i dispositivi con puntatore grossolano o texture massime sotto 8192 il medio. Quando i fotogrammi superano 55 ms la scena riduce le particelle e poi la risoluzione. La chiave `geostat:objects-tier` del `localStorage` fissa il livello per i controlli nel browser.

**Lente gravitazionale.** Per dodici distanze dell’osservatore fra 42 e 260 r_g il worker integra con Runge-Kutta del quarto ordine l’equazione dell’orbita della luce, d²u/dφ² = −u + 3u², per 3072 raggi (1536 nel livello basso), più fitti vicino all’angolo critico. Le tabelle associano a ogni raggio di emissione (256 righe logaritmiche fra 3,05 e 320 r_g) e a ogni angolo percorso (1024 colonne fino a 3π + 0,2) la direzione d’arrivo, con il raggio tangente aggiunto esattamente per ogni riga; una seconda tabella dà l’angolo totale dei raggi che sfuggono e deforma il cielo. Lo shader interpola fra le due distanze vicine. La luminosità di ogni immagine usa la distanza di diametro angolare ricavata dalle derivate della tabella, nella forma meglio condizionata fra le due disponibili.

**Superfici.** `scripts/bake-objects.py` genera per sintesi spettrale periodica le texture `assets/space/objects/regolite` e `nucleo` in 4096 × 4096 e 2048 × 2048 pixel: RGB contiene l’albedo, alfa un campo di quota usato per il rilievo. Le superfici si ripetono senza giunture e sono proiettate lungo i tre assi. L’asteroide e il nucleo sono icosaedri suddivisi sette volte, deformati da rumore a più scale e da crateri con distribuzione N(>r) ∝ r⁻²; le ombre usano una mappa di profondità con filtro a 25 campioni. La nana rossa è l’equipotenziale critica del potenziale di Roche, cercata per bisezione lungo ogni direzione.

## File

| File | Responsabilità |
|---|---|
| `src/objects-model.js` | Catalogo, costanti, relazioni fisiche, curva di luce e colori di corpo nero |
| `src/objects-geometry.js` | Geodetiche e tabelle della lente, mesh dense, lobo di Roche, flusso da L1 |
| `src/objects-worker.js` | Calcoli pesanti fuori dal thread principale (unito alle due librerie nella build) |
| `src/objects-engine.js` | Contesto WebGL2, HDR, bloom, camera, worker, risorse |
| `src/objects-common.js` | Stelle, pianeti, corpi rocciosi con ombre, linee, bagliori, etichette |
| `src/objects-blackhole.js`, `objects-pulsar.js`, `objects-belt.js`, `objects-comet.js`, `objects-binary.js` | Le cinque scene |
| `src/objects.js`, `src/objects-texts.js`, `src/objects.css` | Pagine, testi, figure e stile |
| `scripts/bake-objects.py` | Texture della regolite e della crosta cometaria |

La build unisce motore e scene in `assets/objects-scenes.js`, caricato con SRI alla prima visita di una pagina degli oggetti.

## Verifiche e limiti

`tests/objects.test.mjs` confronta la forma chiusa del flusso con la quadratura diretta della formula di Page e Thorne, verifica che i raggi delle tabelle passino per i punti di emissione tabulati, controlla le formule della pulsar, le risonanze della fascia, l’equazione di Keplero e la vis viva della cometa, i lobi di Roche (raggio equivalente in volume entro l’1% dalla formula di Eggleton) l’eclisse della binaria, la posizione del punto caldo sul bordo del disco e la fase della gobba orbitale. `tests/dom.mjs` apre le cinque pagine e i marcatori della galassia.

Il buco nero non ruota: un buco nero di Kerr avrebbe un’ombra asimmetrica e un disco interno più vicino all’orizzonte. Le particelle del disco sono emettitori otticamente sottili; il cielo di sfondo è deviato pixel per pixel, le particelle punto per punto. La pulsar mostra la rotazione rallentata di 62,5 volte, la binaria di 288 volte. Raggi della stella e del gigante di Lapis sono ingranditi; orbite, periodi e dimensioni della binaria sono in scala. La curva di luce di Diade approssima la nana rossa con una sfera.
