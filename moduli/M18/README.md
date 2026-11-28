# M18 · Dati direzionali

Medie circolari, von Mises, assi e direzioni nello spazio.

<!-- BEGIN INTERACTIVE GUIDE -->
## Percorso interattivo

4 esperimenti eseguibili nel browser. Dopo aver avviato il sito con la procedura del [README principale](../../README.md#avvio-rapido), aprire `#modulo-M18`; le rotte seguenti si aggiungono all’URL del sito, non a quello di GitHub.

| Esperimento | Domanda e operazione | Codice riproducibile |
|---|---|---|
| **Media aritmetica e direzione media** · `#laboratorio/m18-media` | Confrontare la media aritmetica degli azimut con la direzione media circolare al variare della direzione del generatore. | [R](../../R/experiments/m18-media.R) |
| **Potenza del test di Rayleigh** · `#laboratorio/m18-rayleigh` | Stimare con una simulazione la probabilità che il test di Rayleigh riconosca una direzione preferenziale, al variare della concentrazione e del numero di misure. | [R](../../R/experiments/m18-rayleigh.R) |
| **Angoli raddoppiati e famiglie di fratture** · `#laboratorio/m18-assiali` | Osservare come il raddoppio degli angoli riassume dati assiali registrati con l’una o l’altra estremità, e che cosa accade con due famiglie. | [R](../../R/experiments/m18-assiali.R) |
| **Cono di confidenza di Fisher** · `#laboratorio/m18-fisher` | Osservare come il cono di confidenza al 95% della direzione media si restringe al crescere del numero di direzioni. | [R](../../R/experiments/m18-fisher.R) |

Ogni attività esplicita formula, simboli, ipotesi e limiti del procedimento. Il materiale seguente descrive la lezione a tappe e i laboratori del modulo.
<!-- END INTERACTIVE GUIDE -->

**Lezione Azimut: 32 tappe.**

[Presentazione PDF](../../assets/lezioni/M18/M18_Azimut.pdf) · [Progetto R della lezione](../../assets/lezioni/M18/Azimut_M18_progetto_R.zip) · [Sorgenti della lezione](../../lezioni/M18_Azimut/) · [Indice del repository](../../README.md)

## Percorso

Ogni slide della presentazione è una tappa del sito (`#lezione-M18`).

- Tappa 3: Il caso guida.
- Tappe 4–9: Angoli e direzioni medie.
- Tappe 10–16: La distribuzione di von Mises.
- Tappe 17–22: Dati assiali.
- Tappe 23–30: Direzioni nello spazio.
- Tappa 31: Sintesi.
- Tappa 32: Riferimenti.

## Dati

`lezioni/M18_Azimut/dati/` contiene quattro file sintetici: `correnti_v1.csv`, 120 azimut di immersione di lamine oblique in sei stazioni; `fratture_v1.csv`, 110 direzioni di fratture di due famiglie, registrate con l’una o l’altra estremità; `paleomag_v1.csv`, declinazione e inclinazione di 14 colate; `strati_v1.csv`, immersione e inclinazione di 60 strati piegati. I file sono generati da `lezioni/M18_Azimut/R/genera_dati.R`; le figure e i valori della presentazione da `R/M18_figure.R`.

## Tracciabilità

`modulo.json` raccoglie titolo e collocazione nel percorso. La lezione a tappe è in `content/lezioni/M18.json`, generata dai sorgenti in `lezioni/M18_Azimut/` (scritti da `lezioni/Edizione_M17-M21/genera.py`); la spiegazione estesa delle tappe è in `content/lezioni/M18.md`.
