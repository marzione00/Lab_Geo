# Iniziare con GeoStat Lab

## Consultare il corso

Dalla pagina iniziale selezionare «Esplora gli esperimenti» oppure un pianeta nell’atlante. La ricerca comprende argomenti e moduli. Ogni laboratorio permette di variare i parametri, leggere il formalismo, osservare le figure e ricostruire il risultato in R.

Per un primo confronto, aprire **M05 · Copertura degli intervalli di confidenza**. Conservare lo scenario A con correlazione nulla, aumentare la correlazione comune a 0,3 e conservare lo scenario B dopo il ricalcolo. Il confronto mostra quanto cambia la copertura quando viene meno l’indipendenza assunta dalla formula.

La scheda «Formalismo e codice» contiene la definizione dei simboli e l’editor R eseguibile. I pulsanti consentono di scaricare dati, SVG, configurazione e script autonomo. Le presentazioni originali sono disponibili nei materiali di consultazione di ciascun modulo.

La [guida dei laboratori](docs/LABORATORI_INTERATTIVI.md) descrive copertura, versioni, controlli e limiti delle simulazioni.

## Avviare la versione locale

Aprire un terminale nella cartella che contiene `package.json`:

```sh
npm ci --ignore-scripts
npm test
npm run test:dom
npm start
```

Il server mostra l’indirizzo dell’anteprima, normalmente `http://127.0.0.1:4173/`. La build richiede Node.js 22 o successivo. La directory `dist/` è generata e può essere ricostruita.

## Eseguire i codici

Aprire `materiali/Corso_Geologia.Rproj` in RStudio. Installare esplicitamente le dipendenze descritte nella guida prima di eseguire le analisi.

```r
source("R/controlla_ambiente.R")
source("R/M07_figure.R")
source("laboratori/M07/M07_N01.R")
```

I percorsi sono riferiti alla cartella `materiali/`. Questi comandi riguardano i materiali originali. Gli esperimenti interattivi eseguono R anche nel browser e forniscono script autonomi in `R/experiments/`.

## Portare il repository su GitHub

Seguire [la procedura di pubblicazione](DEPLOYMENT.md). Caricare il contenuto estratto, compresa `.github/`, affinché GitHub possa eseguire il workflow. La consegna contiene i file pronti per il repository; l’indirizzo pubblico sarà quello assegnato da GitHub Pages dopo la pubblicazione.
