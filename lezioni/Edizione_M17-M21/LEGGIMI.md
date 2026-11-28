# GeoStat Lab · Lezioni M17-M21

Le lezioni dei moduli M17-M21 seguono l'impaginazione delle presentazioni planetarie T00 e M13-M16: formato 16:10, cornice con capitolo, «Da ricordare» e numero di pagina, due colonne per pagina, riquadri del codice R, pagine Scenario A e Confronto per gli esperimenti del browser.

| Modulo | Cartella | Argomento | Pagine |
|---|---|---|---:|
| M17 | `M17_Simplex` | Dati composizionali | 32 |

## Strumenti di questa cartella

- `genera.py` scrive il sorgente Beamer e `Indice.csv` di una lezione a partire dalla sua specifica `spec_<id>.py`. Il preambolo è quello di Prisma (M16) con titolo e numero di pagine della nuova lezione; le pagine si numerano da sole e l'indice dei capitoli, i segnalibri e i collegamenti ai laboratori seguono la specifica. I risultati dei frammenti R vengono letti da `Codice/risultati-capitoli.json`.
- `scenari.R` esegue gli scenari A e B di un esperimento del catalogo e scrive in `Esperimenti/` i due programmi, i grafici SVG, i PDF usati nelle slide (convertiti con `rsvg-convert`) e il JSON con parametri e metriche.

Dalla radice del repository, per Simplex:

```sh
python3 -I scripts/labs/aggiungi_esperimenti.py content/esperimenti/M17.json
LC_ALL=C.UTF-8 Rscript lezioni/Edizione_M17-M21/scenari.R lezioni/M17_Simplex m17-chiusura '{"D":3}' '{"D":8}'
python3 -I lezioni/Edizione_M17-M21/genera.py M17
cd lezioni/M17_Simplex && xelatex -halt-on-error M17_Simplex.tex && xelatex -halt-on-error M17_Simplex.tex
```

## Contenuto di una cartella di lezione

- `dati/` contiene gli ingressi; per Simplex il file sintetico `composizioni_v1.csv`, ricostruito da `R/genera_dati.R` con un seme fissato.
- `R/<id>_figure.R` ricostruisce figure e valori e interrompe l'esecuzione se un controllo numerico fallisce; scrive in `figure/<id>` e `risultati/<id>`. Per aggiornare le slide si copiano i PDF in `Figure/` e si ricompila. Lo script va eseguito con una localizzazione UTF-8 (`LC_ALL=C.UTF-8`), necessaria per le lettere accentate nelle etichette.
- `R/copertina.R` disegna la copertina procedurale `Scena/copertina.jpg` (2400 × 1500 pixel): fondale stellare, pianeta con illuminazione calcolata per pixel e un elemento ricavato dai dati del caso.
- `Codice/` contiene i frammenti delle pagine, autonomi; `Diagrammi/` i disegni TikZ; `Esperimenti/` gli scenari dei laboratori.

Le pagine sono importate nel sito con `python3 -I scripts/lessons/import_lesson.py <id>`; le uscite dei frammenti vengono registrate in webR con `python3 -I scripts/lessons/verify_webr.py <id>` dopo `npm run build`.
