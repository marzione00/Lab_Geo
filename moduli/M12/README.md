# M12 · Raster, telerilevamento e morfometria

Dalla geometria della griglia alle grandezze derivate.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

9 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M12`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Geometria di una griglia raster** · `#laboratorio/m12-griglia` | Collegare numero di celle, risoluzione e superficie. | [R](../../R/experiments/m12-griglia.R) |
| **Maschere, dominio e superficie valida** · `#laboratorio/m12-maschere` | Distinguere celle escluse e celle a valore nullo. | [R](../../R/experiments/m12-maschere.R) |
| **Aggregazione e ricampionamento di una griglia** · `#laboratorio/m12-ricampionamento` | Confrontare risoluzioni senza attribuire nuova informazione ai pixel interpolati. | [R](../../R/experiments/m12-ricampionamento.R) |
| **Allineamento e ricampionamento fra griglie** · `#laboratorio/m12-allineamento` | Valutare lo scarto introdotto da griglie con origine diversa. | [R](../../R/experiments/m12-allineamento.R) |
| **Gradiente, pendenza ed esposizione** · `#laboratorio/m12-pendenza` | Ricostruire derivate da differenze centrate e unità metriche. | [R](../../R/experiments/m12-pendenza.R) |
| **Illuminazione del rilievo** · `#laboratorio/m12-hillshade` | Separare forma del terreno e condizioni di illuminazione. | [R](../../R/experiments/m12-hillshade.R) |
| **Bande spettrali e indice normalizzato** · `#laboratorio/m12-indici` | Esaminare il ruolo di numeratore e denominatore in un indice. | [R](../../R/experiments/m12-indici.R) |
| **Sintesi zonali e dipendenza delle celle** · `#laboratorio/m12-zone` | Confrontare numero di pixel e unità informative. | [R](../../R/experiments/m12-zone.R) |
| **Dimensioni del raster e memoria** · `#laboratorio/m12-memoria` | Quantificare la crescita del costo di una griglia. | [R](../../R/experiments/m12-memoria.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente conserva la numerazione delle slide e dei laboratori originali R6.
<!-- END INTERACTIVE GUIDE -->

**30 slide · 11 figure · 10 diagrammi TikZ · 20 laboratori.**

[PDF del modulo](../../materiali/pdf/M12_R6.pdf) · [Codice R delle figure](../../materiali/R/M12_figure.R) · [Sorgente LaTeX](../../materiali/sorgenti/M12_R6.tex) · [Indice del repository](../../README.md)

## Percorso

- Pagina 3: Griglia, celle e georeferenziazione.
- Pagina 7: Maschere, dominio e superficie.
- Pagina 10: Aggregazione, ricampionamento e allineamento.
- Pagina 14: Derivate, pendenza ed esposizione.
- Pagina 20: Ombreggiatura e rappresentazione del rilievo.
- Pagina 23: Bande e indici normalizzati.
- Pagina 26: Sintesi zonali e dipendenza.
- Pagina 29: Memoria, esportazione e verifica.

## Esecuzione

Aprire `materiali/Corso_Geologia.Rproj`, oppure avviare R nella cartella `materiali/`, quindi eseguire:

```r
source("R/M12_figure.R")
```

Le dipendenze comuni e i dati restano nella cartella `materiali/`; scaricare l’intero repository prima di eseguire gli script.

## Laboratori

| Codice | Attività | File |
|---|---|---|
| M12_N01 | Audit della griglia: celle uniche e passo | [R](../../materiali/laboratori/M12/M12_N01.R) |
| M12_N02 | Orientamento: nord e sud nella matrice | [R](../../materiali/laboratori/M12/M12_N02.R) |
| M12_N03 | GeoTIFF: leggere valori e georeferenziazione | [R](../../materiali/laboratori/M12/M12_N03.R) |
| M12_N04 | NoData non è quota zero | [R](../../materiali/laboratori/M12/M12_N04.R) |
| M12_N05 | Ritagliare significa cambiare dominio | [R](../../materiali/laboratori/M12/M12_N05.R) |
| M12_N06 | Area delle celle: dal conteggio agli ettari | [R](../../materiali/laboratori/M12/M12_N06.R) |
| M12_N07 | Aggregazione 2×2 e conservazione della media | [R](../../materiali/laboratori/M12/M12_N07.R) |
| M12_N08 | Quote continue e classi discrete richiedono ricampionamenti diversi | [R](../../materiali/laboratori/M12/M12_N08.R) |
| M12_N09 | Derivata su un piano noto: prova del codice | [R](../../materiali/laboratori/M12/M12_N09.R) |
| M12_N10 | Pendenza in gradi e in percentuale | [R](../../materiali/laboratori/M12/M12_N10.R) |
| M12_N11 | Esposizione e statistiche circolari | [R](../../materiali/laboratori/M12/M12_N11.R) |
| M12_N12 | Hillshade: cambiare luce senza cambiare terreno | [R](../../materiali/laboratori/M12/M12_N12.R) |
| M12_N13 | Bande sintetiche e indice normalizzato | [R](../../materiali/laboratori/M12/M12_N13.R) |
| M12_N14 | Denominatore piccolo: maschera dichiarata | [R](../../materiali/laboratori/M12/M12_N14.R) |
| M12_N15 | Statistiche zonali e nuovo livello della tabella | [R](../../materiali/laboratori/M12/M12_N15.R) |
| M12_N16 | Dipendenza: differenze a 30 e 300 metri | [R](../../materiali/laboratori/M12/M12_N16.R) |
| M12_N17 | Bootstrap di blocchi: un’ipotesi esplicita | [R](../../materiali/laboratori/M12/M12_N17.R) |
| M12_N18 | Finestre di lettura e memoria | [R](../../materiali/laboratori/M12/M12_N18.R) |
| M12_N19 | Stessa forma, origini diverse | [R](../../materiali/laboratori/M12/M12_N19.R) |
| M12_N20 | Consegna delle pendenze interne | [R](../../materiali/laboratori/M12/M12_N20.R) |

## Tracciabilità

La numerazione coincide con il fascicolo R6. Il registro completo della rilettura si trova in [audit](../../materiali/audit/Registro_slide_R6.html). `modulo.json` raccoglie il contenuto destinato alla navigazione web e viene rigenerato dai sorgenti del corso.
