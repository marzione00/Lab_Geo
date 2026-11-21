# GeoStat Lab · Presentazioni planetarie

Cinque presentazioni Beamer in italiano, in formato 16:10. I PDF hanno un indice con collegamenti ai capitoli, segnalibri e rimandi ai laboratori web.

| Modulo | Pianeta | Argomento | Pagine |
|---|---|---|---:|
| T00 | Basalto | Programmazione scientifica in R e Python | 66 |
| M13 | Strata | Cronologie e archivi sedimentari | 63 |
| M14 | Ignis | Estremi, pericolosità e rischio | 66 |
| M15 | Argenta | Riproducibilità e progetto di analisi | 58 |
| M16 | Prisma | Classificazione e validazione | 62 |

## Modificare una presentazione

Apri il PDF in `02_PDF`. Il progetto corrispondente si trova in `01_Sorgenti_LaTeX`. Ogni cartella di modulo contiene un file principale `.tex` e un indice delle pagine in CSV.

Per ricompilare serve XeLaTeX con Beamer, TikZ, tcolorbox, adjustbox, listings, bookmark, fontspec e il supporto italiano di babel. Per riprodurre i caratteri dell'edizione, installa Nimbus Sans dalla cartella `Font` e DejaVu Sans Mono. Il sorgente prevede anche TeX Gyre Heros e Latin Modern Mono. Esegui entrambi i comandi dalla cartella del singolo modulo. Per Strata, ad esempio, usa:

```sh
xelatex -halt-on-error M13_Strata.tex
xelatex -halt-on-error M13_Strata.tex
```

Il secondo passaggio consolida le posizioni delle pagine e la navigazione. Modifica gli schemi intervenendo direttamente sui file TikZ in `Diagrammi`. Le pagine con il grafico di uno scenario incorporano un PDF vettoriale.

## Riprodurre risultati e grafici

- `Codice/capitolo-*.R` contiene i calcoli dei casi guida. I risultati registrati con R sono in `Codice/risultati-capitoli.json`. Basalto include anche gli esempi Python corrispondenti, eseguibili con Python 3.10 o successivo.
- `Esperimenti` contiene 33 coppie di scenari nell'intera raccolta. Il JSON di ciascun laboratorio riporta i parametri, il seme e i risultati di entrambe le esecuzioni. Per ciascuno scenario sono inclusi il programma R, il grafico SVG e il PDF usato nelle slide. I programmi sono stati eseguiti nel runtime webR del corso. Le versioni dei pacchetti sono documentate in `Provenienza/r-packages-lock.json`.
- Per ricalcolare un grafico, entra nella cartella `Esperimenti` del modulo. L'esempio seguente usa R con ggplot2 e svglite e converte il grafico in PDF con Inkscape.

```sh
Rscript m13-interpolazione-A.R
inkscape m13-interpolazione-A.svg --export-text-to-path --export-filename=m13-interpolazione-A.pdf
```

- `Figure` raccoglie i grafici dell'edizione R6 utilizzati nelle slide. Per rigenerare quelli di Strata, esegui `Rscript R/M13_figure.R` dalla cartella del modulo. Lo script originale scrive in `figure/M13`. Per aggiornare le slide, copia i PDF desiderati nella cartella `Figure` e ricompila. Per gli altri moduli cambia l'identificativo. Gli script del corso usano ggplot2 e jsonlite. Alcuni calcoli di Prisma impiegano inoltre class, rpart e randomForest.
- Le cartelle `dati` contengono gli ingressi dei rispettivi moduli. Dove presenti, `Archivi` e `Tabelle` raccolgono i programmi dei laboratori R6 citati nelle slide e i CSV di riferimento. Per eseguire uno di questi programmi, avvia R dalla cartella del modulo, ad esempio con `Rscript Archivi/M13_N01.R`. Il programma scrive il risultato in `risultati/R/M13_N01`. I valori dei casi guida, dei laboratori R6 e dei confronti web vanno letti con i rispettivi dati e parametri.

## Rigenerare una copertina

Apri `Scena/copertina.blend` in Blender e scegli **Render → Render Image**. Il progetto contiene geometrie, materiali procedurali, luci e camera. La scena è stata renderizzata con Blender 4.3.2 e Cycles a 2400 × 1500 pixel. La copertina stampata usa il JPEG salvato accanto al progetto. Il file `render.json` conserva le impostazioni.

Per ricostruire anche il modello, esegui dalla radice dell'archivio:

```sh
blender -b --python-exit-code 3 -P copertine.py -- M13 scena-rigenerata
```

Il comando produce `copertina.blend` e `copertina.png`. Per usare il nuovo render nella presentazione, sostituisci `Scena/copertina.jpg` con una conversione JPEG oppure modifica il percorso nel file TeX per incorporare il PNG.

## Attribuzioni

Il corso GeoStat Lab e i materiali didattici originali sono di **Marzio De Corato**. L'impaginazione deriva dalla presentazione ristrutturata **M12 Tessera**, fornita insieme agli altri undici modelli della serie. L'adattamento comprende nuove scene 3D, l'indice dei capitoli, i casi guida, i disegni di apertura, i confronti fra scenari e la selezione dei risultati R6.

Per gli adattamenti dei materiali didattici soggetti a CC BY-NC-SA 4.0 valgono gli stessi termini. I dati, i programmi e i caratteri conservano le rispettive condizioni. Le licenze e le note originali sono in `Provenienza` e `Font`.

[Repository GeoStat Lab, revisione utilizzata](https://github.com/marzione00/Lab_Geo/tree/649f7cc577b96bd1044d81e78a2f530813e4f96b)
