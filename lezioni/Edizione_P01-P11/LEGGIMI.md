# GeoStat Lab · Presentazioni delle spedizioni

Undici presentazioni Beamer in italiano, in formato 16:10, una per ciascuna spedizione applicativa. Impaginazione, indice dei capitoli, segnalibri e pagine degli esperimenti seguono le lezioni planetarie; ogni pagina diventa una tappa del sito (`#lezione-P01`, …, `#lezione-P11`).

| Spedizione | Cartella | Argomento | Pagine |
|---|---|---|---:|
| P01 | `P01_Pori` | Geometria dei pori e permeabilità | 31 |
| P02 | `P02_Foraminiferi` | Foraminiferi, coppe e campagne | 32 |
| P03 | `P03_Nilo` | Il Nilo: livelli e dipendenza temporale | 31 |
| P04 | `P04_Geyser` | Un geyser: associazione e previsione | 31 |
| P05 | `P05_CO2` | CO₂: tendenza e calendario stagionale | 32 |
| P06 | `P06_Validazione` | Dai campioni alla validazione spaziale | 27 |
| P07 | `P07_Terreno` | Terreno, pendenze e sintesi territoriali | 27 |
| P08 | `P08_Proxy` | Collocare nel tempo il massimo di un proxy | 28 |
| P09 | `P09_Livelli` | Un livello raro e la sua incertezza | 26 |
| P10 | `P10_Ricostruibile` | Un’analisi ricostruibile e verificabile | 26 |
| P11 | `P11_Stazioni` | Classificare nuove stazioni sintetiche | 27 |

Ogni presentazione si apre con copertina, indice e caso guida; seguono i capitoli della spedizione, il capitolo dei laboratori con le tre fasi della missione, la sintesi e i riferimenti.

## Contenuto di una cartella

- Il file `.tex` principale, il PDF compilato e `Indice.csv` con i titoli delle pagine.
- `Codice` contiene i frammenti R citati dalle slide. Ogni file è autonomo e si esegue dalla cartella della spedizione.
- `R` contiene lo script `<id>_figure.R`, che ricostruisce le figure e i valori del caso dai dati, con `stile.R` e, dove serve, `covarianze.R` o `P10_funzioni.R`. Lo stesso programma è la soluzione ragionata della spedizione sul sito.
- `Figure` raccoglie i grafici vettoriali prodotti dallo script; `risultati/<id>` i valori, le tabelle e i piani di ricampionamento.
- `Diagrammi` contiene i disegni TikZ modificabili; `apertura.tex` e `fasi.tex` riassumono capitoli e fasi della missione.
- `Esperimenti` contiene, per la prima attività di ogni fase, i programmi R dei due scenari, i grafici SVG e PDF e un JSON con parametri e risultati. Gli scenari degli esperimenti m13, m14, m15 e m16 coincidono con quelli delle lezioni Strata, Ignis, Argenta e Prisma.
- `dati` contiene gli ingressi con i rispettivi file di provenienza; `Scena` il modello Blender della copertina.

## Ricompilare una presentazione

Servono XeLaTeX con Beamer, TikZ, tcolorbox, adjustbox, listings, bookmark, fontspec e babel in italiano, con Nimbus Sans e DejaVu Sans Mono. Dalla cartella della spedizione:

```sh
xelatex -halt-on-error P01_Pori.tex
xelatex -halt-on-error P01_Pori.tex
```

Il secondo passaggio consolida segnalibri e collegamenti interni. Il sorgente cerca i file `NimbusSans-*.otf` per nome e, se non li trova, ripiega su TeX Gyre Heros: quando i caratteri sono installati in una cartella personale, la variabile `OSFONTDIR` deve indicarla (per esempio `OSFONTDIR=~/.fonts xelatex …`).

## Riprodurre figure, valori ed esperimenti

- `Rscript R/P01_figure.R` scrive le figure in `figure/P01` e i valori in `risultati/P01`; i controlli del programma interrompono l’esecuzione se un dato non rispetta le condizioni dichiarate. Per aggiornare le slide si copiano i PDF in `Figure` e si ricompila. Lo script di P07 richiede anche terra, quello di P10 il programma git.
- `Rscript Esperimenti/m01-estimando-A.R` riproduce uno scenario e salva il grafico SVG; la versione PDF usata nelle slide si ottiene con `rsvg-convert -f pdf -o m01-estimando-A.pdf m01-estimando-A.svg`.
- `verifica_covarianze.py`, in questa cartella, confronta con statsmodels le covarianze HAC e HC3 calcolate in R nelle spedizioni P03, P04 e P05; il risultato è in `confronto_covarianze.json`.

## Rigenerare una copertina

Le scene sono costruite da `copertine.py`: camera ortografica, fondale stellare e tre luci ad area, come nelle copertine delle lezioni, più il pianeta della spedizione e un oggetto ricavato dai dati del caso (carote porose, volumi del Nilo, raster delle quote, massimi annuali e così via). Materiali e geometrie sono procedurali, senza texture esterne né immagini generate.

```sh
blender -b -P copertine.py -- P01
```

Lo stesso script funziona con il modulo `bpy` di Python (`python copertine.py P01`). Il render usa Cycles a 2400 × 1500 pixel con 16 campioni e il seme indicato in `Scena/render.json`; lo script scrive `copertina.blend`, `copertina.jpg` e `render.json` nella cartella della spedizione.

## Attribuzioni

Il corso GeoStat Lab e i materiali didattici sono di **Marzio De Corato**. L’impaginazione deriva dalla serie planetaria delle lezioni, a sua volta basata sulla presentazione **M12 Tessera**. Dati e fonti di ciascuna spedizione sono indicati nell’ultima pagina della presentazione e nei file di provenienza della cartella `dati`.

Materiali CC BY-NC-SA 4.0; codice PolyForm Noncommercial 1.0.0 (vedi `LICENSE.md` e `LICENSE-CODE.md` nella radice del repository).
