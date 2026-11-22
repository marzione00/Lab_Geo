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

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Tessera: 110 tappe · 20 laboratori.**

[Presentazione PDF](../../assets/lezioni/M12/Tessera_M12_raster_telerilevamento_morfometria.pdf) · [Progetto R della lezione](../../assets/lezioni/M12/Tessera_M12_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M12_Tessera/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M12`).

- Tappe 6–19: II · Geometria raster.
- Tappe 20–32: III · Maschere e dominio.
- Tappe 33–48: IV · Risoluzione e allineamento.
- Tappe 49–66: V · Morfometria.
- Tappe 67–76: VI · Luce e rilievo.
- Tappe 77–90: VII · Bande e indici.
- Tappe 91–102: VIII · Sintesi territoriali.
- Tappe 103–110: IX · Consegna e verifica.

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

`modulo.json` raccoglie titolo, collocazione nel percorso e laboratori del modulo. La lezione a tappe è in `content/lezioni/M12.json`, generata dai sorgenti in `lezioni/M12_Tessera/`; la spiegazione estesa delle tappe è in `content/lezioni/M12.md`.
