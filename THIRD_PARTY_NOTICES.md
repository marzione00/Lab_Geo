# Componenti e provenienza

| Componente | Versione o fonte | Avviso incluso |
|---|---|---|
| MathJax | 3.2.2 · https://github.com/mathjax/MathJax | [Apache 2.0](vendor/mathjax/LICENSE) |
| Nimbus Sans | Caratteri conservati nel template del corso | [Licenza Nimbus](materiali/sorgenti/font/LICENZA_Nimbus.txt) |
| Latin Modern | Carattere monospaziato e componenti matematiche del corso | [Licenza Latin Modern](materiali/sorgenti/font/LICENZA_LatinModern.txt) |

I PDF e gli SVG derivano dai materiali R6. L’immagine topografica della copertina è una composizione illustrativa e non rappresenta una superficie osservata.

Il repository [QuantumLab_Public](https://github.com/marzione00/QuantumLab_Public), esaminato al commit `275b07805da69af75ba6c2f64ea0ba99ae4144ea`, è il riferimento organizzativo. Il suo motore di simulazione e i suoi contenuti non sono incorporati in GeoStat Lab.

La provenienza del pacchetto MathJax è registrata in [vendor/mathjax/provenienza.json](vendor/mathjax/provenienza.json).
# Atlante planetario

Le texture della Terra provengono da Solar System Scope, con licenza Creative Commons Attribution 4.0 International:
https://www.solarsystemscope.com/textures/
https://creativecommons.org/licenses/by/4.0/

I file di partenza `earth_day_4096.jpg`, `earth_night_4096.jpg` e `earth_bump_roughness_clouds_4096.jpg` sono le versioni ridimensionate e combinate presenti nell'esempio ufficiale Three.js `webgpu_tsl_earth.html`. Le copie incluse sono ulteriormente ridimensionate e convertite in WebP. L'attribuzione è visibile anche nel sito.

Gli altri pianeti sono mondi illustrativi generati da funzioni procedurali nei sorgenti del progetto. Le associazioni con i moduli hanno funzione di orientamento; superfici e velocità non rappresentano osservazioni astronomiche. Il fondale di spazio profondo è un'illustrazione originale generata per il progetto.

## Interprete R e pacchetti dei laboratori

webR 0.6.0 proviene dalla distribuzione ufficiale [r-wasm/webr](https://github.com/r-wasm/webr/releases/tag/v0.6.0). I binari includono R 4.6.0 e sono distribuiti sotto GNU GPL v3; gli strumenti di supporto hanno le licenze indicate nel [testo integrale incluso](vendor/webr/LICENSE.md). I sorgenti corrispondenti, le istruzioni di compilazione e i riferimenti alle dipendenze sono disponibili nel [tag v0.6.0](https://github.com/r-wasm/webr/tree/v0.6.0). I file sono conservati senza modifiche; le impronte sono registrate in `vendor/webr-provenance.json`.

I 23 pacchetti R WebAssembly provengono dal repository ufficiale `https://repo.r-wasm.org/bin/emscripten/contrib/4.6/`. Gli archivi originali sono inclusi in `vendor/r-repo/`; ogni pacchetto conserva DESCRIPTION e gli eventuali file LICENSE. Una copia consultabile di questi avvisi è in `vendor/r-package-licenses/`. Nomi, versioni, licenze e SHA-256 sono registrati in [vendor/r-packages-lock.json](vendor/r-packages-lock.json). Le fonti dei pacchetti CRAN sono disponibili nelle rispettive pagine `https://cran.r-project.org/package=NOME` e negli archivi sorgente delle versioni indicate.

Le nuove figure scientifiche provengono dai programmi originali di `R/experiments/`, applicati a dati sintetici. Le relative superfici spaziali rappresentano simulazioni didattiche, non misurazioni del territorio. La palette e il tema sono definiti in `R/lab-common.R`.

Le copie web degli SVG sono ottimizzate mediante [SVGO 4.0.0](https://github.com/svg/svgo/tree/v4.0.0), strumento di sviluppo con licenza MIT. La trasformazione conserva otto cifre decimali; gli originali PDF e i font del corso non sono modificati.

I 232 pannelli TikZ nella lettura testuale riutilizzano lo stesso SVG della slide mediante una finestra vettoriale sulle coordinate originali del diagramma. Le copie dei pannelli rimangono nel repository; la distribuzione evita di trasferire due volte lo stesso contenuto.

## Strumenti di collaudo della versione 3.1

Le dipendenze npm sono esclusivamente strumenti di sviluppo, fissati con integrità nel `package-lock.json`; non sono incluse nella distribuzione web. jsdom 26.1.0 è distribuito con licenza MIT; le licenze dei pacchetti transitivi sono indicate nei rispettivi package.json installati. Playwright 1.65.0 (Apache-2.0) e greenlet 3.5.6 (MIT e Python-2.0 per le componenti indicate dal progetto) sono fissati con hash in `security/requirements.txt`. I file dei workflow rimandano alle distribuzioni ufficiali delle azioni GitHub tramite commit completi.

La build aggiunge CSP e SRI ai documenti generati e CSP con hash per gli script delle pagine HTML accessorie; i file distribuiti upstream di webR e MathJax restano invariati.

## Osservazioni nei mini-progetti (3.8)

I dati provengono da USGS Earthquake Hazards Program, NASA/JPL Small-Body Database, NOAA/NSIDC Sea Ice Index v4, NOAA/NCEI GOES XRS e NASA Exoplanet Archive (NASA Exoplanet Science Institute, Caltech/IPAC). I rispettivi `assets/research/<id>/provenance.json` conservano attribuzioni, condizioni indicate dal fornitore, query e riferimenti. Per JPL non viene attribuita una licenza CC inesistente; per gli esopianeti sono conservati i riferimenti alle pubblicazioni. Loghi e marchi dei fornitori non vengono impiegati come endorsement.

Le tredici famiglie planetarie richiamano una convenzione ludica di varietà ambientale; nessuna texture, modello, audio o altro asset di Haegemonia o Mass Effect è incluso. Le albedo sono generate da `scripts/bake-research-planets.py`; documentazione in `docs/planet-family-assets.md`.
