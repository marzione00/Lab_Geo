# Motore scientifico di Tessera

Aprire la sessione R dalla cartella `M12_Tessera`. Occorre il pacchetto `terra` installato prima dell’analisi; nessuno script installa automaticamente pacchetti.

```r
source("Lezione_Tessera.R")       # stato della lezione, senza esportazioni
source("R/rigenera_calcoli.R")  # rigenera risultati, GeoTIFF e42PDF
```

## File e oggetti

`setup.R` verifica cartella e dipendenza. `R/funzioni_M12.R` definisce le funzioni di calcolo. `R/stato_lezione.R` legge i dati e crea gli oggetti seguenti.

| Oggetto | Significato |
|---|---|
| `d`, `casuali`, `u` | Tabelle originali ordinate e uniformi comuni |
| `Z`, `x`, `y`, `dx`, `dy` | Matrice24×30, prima riga a Sud; centri e passi30m |
| `r`, `M` | GeoTIFF originale e matrice letta da Nord a Sud |
| `mask`, `Z_mask` | TRUE nelle24celle escluse; quote con NA |
| `A2`, `x2`, `y2` | Aggregazione12×15 e centri da15m, passo60m |
| `gx`, `gy`, `g` | Componenti e modulo, matrici22×28 |
| `slope_deg`, `slope_pct`, `aspect_deg` | Gradi, percento, azimut di discesa; aspect piatto=NA |
| `inn` | 616righe coordinate/derivate/luce, ordinate per y poi x |
| `hill315`, `hill135` | Illuminazioni22×28, altezza45gradi |
| `R_band`, `NIR`, `indice` | Bande e indice sintetici in ordine della tabella d |
| `zone` | Due righe A/B con media, numero, area e sd |
| `block_means` | 12medie in ordine Sud→Nord, Ovest→Est |
| `boot300`, `boot1999` | Originali300uniformi ed estensione1999 seed20261109 |

## Funzioni

- `gradiente_centrato(Z,dx=30,dy=dx,centro_valido=TRUE)`: matrici interne `gx`, `gy`, `valido`; centro e quattro vicini devono essere finiti.
- `morfometria(Z,dx=30,dy=dx,flat_tol=1e-12)`: aggiunge modulo, pendenza in gradi/percento ed esposizione; le righe della matrice devono crescere verso Nord.
- `hillshade_normale(gx,gy,az=315,altezza=45)`: normale e luce unitarie, azimut/altezza in gradi, risultato in[0,1]. Conserva le dimensioni anche sui piani.
- `media_circolare(gradi,tol=1e-12)`: media normalizzata, risultante e numerosità valida; direzione NA se risultante nulla.
- `aggrega2(Z,na.rm=FALSE)`: medie di blocchi completi2×2; se `na.rm=TRUE`, i conteggi vanno mantenuti per le successive pesature.
- `indice_normalizzato(N,R,eps=1e-6)`: indice, denominatore e maschera; esclude non finiti e somma≤eps.
- `raster_locale(M,x,y,dx=30,dy=dx,offset=c(500015,4999295),crs="EPSG:32632")`: converte una matrice S→N con centri espliciti in SpatRaster N→S. L’offset è specifico della collocazione fittizia del corso.
- `matrice_locale(r)`: matrice S→N da SpatRaster; `row_values(M)` restituisce valori per righe.
- `superficie_analitica`, `gradiente_analitico`, `pesi_finestra`: esperimento separato900×600m, pesi di intersezione della finestra comune28ha.

## Risultati e verifiche

I CSV e `summary.json` contengono risultati realmente eseguiti. `R/manifest_figure.csv` stabilisce i42nomi e la scelta colonna/panorama. `Calcoli/figure_manifest.csv` aggiunge le descrizioni scientifiche. Le figure vengono rigenerate dagli stessi oggetti del motore; non derivano da dati numerici ricopiati nelle slide.

Il protocollo completo, le fonti e i limiti sono in `FONTI_E_NOTE.md`. Le letture/esportazioni terra, il piano analitico, gli indici, le maschere e le identità della luce sono verificati dal motore. Le ulteriori verifiche Python non riscrivono gli output R:

```bash
python Verifiche/controlli_indipendenti.py
python Verifiche/audit_figure.py
python Verifiche/render_figure.py
```

I due script PDF richiedono PyMuPDF; quello di rendering anche Pillow. La verifica indipendente richiede NumPy/rasterio. Le anteprime sono materiale di controllo, non sostituiscono i PDF vettoriali. Il rapporto automatico controlla pagine, bitmap e testi oltre bordo; la verifica di sovrapposizioni è anche visiva.

Le pendenze sono esportate in gradi, nel nome della banda `pendenza_gradi` e nella documentazione. FLOAT64 preserva la precisione del calcolo assegnato. Il ricampionamento può avere una precisione interna diversa: il confronto rasterio/terra usa una tolleranza0,0002m, motivata dallo scarto misurato. Le statistiche non calcolate nei tag GDAL non vengono usate per l’analisi.
