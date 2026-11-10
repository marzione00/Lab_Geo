# Dizionario dei dati e unità di osservazione

Non sono necessarie richieste online per eseguire gli script. Conservare `PROVENIENZA.json` insieme ai CSV. Dati reali e storici; i piani di ricampionamento e lo split sono prodotti computazionali, non osservazioni nuove.

## rock.csv — 48 sezioni su 12 carote

| Colonna | Significato e unità |
|---|---|
| image_id | Ordine della riga distribuita, identificativo aggiunto |
| area_pixels | Area totale dei pori, pixel su immagine 256×256 |
| perimeter_pixels | Perimetro dei pori, pixel |
| shape_original | Colonna originale conservata; formula documentale incoerente con i valori, non usata |
| permeability_md | Permeabilità della carota, millidarcy; ripetuta per le quattro sezioni |
| core_id | Identificativo ricostruito a blocchi di quattro righe, NON originale |

Derivate: `pore_area_pct=100*area_pixels/65536`; `log10_k=log10(permeability_md)`. È frazione areale 2D, non porosità efficace 3D. La ricostruzione delle carote è coerente con i valori, ma richiede conferma sui metadati primari per una ricerca non didattica.

## foraminiferi.csv — 36 coppe

| Colonna | Significato e unità |
|---|---|
| row_id | ID aggiunto dell’estratto |
| trap_year | Campagna di trappola come etichetta originale |
| cup_id | Numero di coppa nella campagna |
| date | Data centrale di raccolta indicata dalla fonte |
| depth_m | Profondità della trappola, 170 m |
| diam_mean_um | Media dei diametri **massimi** dei gusci della coppa, µm |
| diam_min_um | Minimo dei diametri massimi, µm |
| diam_max_um | Massimo dei diametri massimi, µm |
| diam_median_um | Mediana dei diametri massimi, µm |

Estratte colonne 1–4 e 9–12 della tabella originale PANGAEA.902776. Non confondere questa media con le altre colonne di diametro medio della tabella completa. Non sono incluse misure individuali né conteggi dei gusci: non ricostruirli da minimi e massimi.

Derivate: fascia `Ott-Mar` o `Apr-Set` secondo il mese della data centrale; medie delle coppe entro campagna-fascia; differenza Ott-Mar meno Apr-Set per quattro campagne complete. Pesi uguali alle coppe entro fascia, poi uguali alle campagne complete. Nessun peso per durata, flusso o numero di individui.

## nile.csv — 100 volumi annuali, 1871–1970

`year`: anno intero. `volume_1e8_m3`: volume annuale ad Aswan in **10^8 m³**, non m³/s. `post` è una derivata pari a uno dal 1898. La data è suggerita dal caso storico, non pre-registrata indipendentemente dal dataset.

## faithful.csv — 272 eventi

`row_id`: ID aggiunto. `eruption_min`: durata dell’eruzione, minuti. `waiting_min`: attesa alla **successiva** eruzione, minuti. Misure arrotondate, nessuna data disponibile. Split casuale 190/82 salvato in `piani_ricampionamento/faithful_split.csv`; `set` vale `train` o `test`. Una verifica su questo split è interna, non prospettica.

## co2_weekly.csv — calendario settimanale storico

`date`: data della settimana, 1958–2001. `co2_ppm`: concentrazione in ppm, con valori mancanti mantenuti come celle vuote. Il calendario ha 2.284 righe; la documentazione riporta 2.225 osservazioni valide. La diversa numerosità deriva dai mancanti, non da due fonti mescolate.

Derivate: medie delle settimane disponibili raggruppate per mese (`MS` in Python), conteggio `n_valid`, anno, mese, tempo centrato `year+(month-0.5)/12-1993`. Audit 1980–2000; finestra analitica 1985–2000, 192 mesi con almeno tre valori settimanali ciascuno. Aprile 1984 ha un solo valore. Non è il prodotto mensile ufficiale NOAA né un dataset aggiornato.

## Piani condivisi tra le lingue

`rock_cores.csv`: 4.000 righe ×12 estrazioni, indici 1–12, ordine delle carote crescente. `paleo_years.csv`: 4.000×4, campagne complete ordinate lessicograficamente. **R usa direttamente gli indici, Python sottrae uno.** I quantili usano convenzione lineare/type 7.

Lo stesso seme in linguaggi diversi non garantisce gli stessi numeri. I CSV eliminano questa ambiguità per il confronto didattico. Il bootstrap cambia le estrazioni, non la numerosità delle unità reali.
