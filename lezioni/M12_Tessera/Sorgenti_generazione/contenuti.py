"""Tessera: 110 slide, risultati effettivi R e figure vettoriali incluse."""
from componenti import *
import parte01
import parte02
import parte03
import parte04
import parte05
assert len(SLIDES)==109

# Le figure con più carte occupano tutta la larghezza disponibile.
# Il codice dell'aggregazione è visibile nella pagina35, non nel panorama34.
PANORAMI={
 14:('02_orientamento',
     r'Gli stessi valori sono rappresentati con due ordinamenti: a sinistra la convenzione locale corretta, a destra l’inversione delle righe interpretata erroneamente come locale. Media e distribuzione restano uguali. Il confronto delle celle di posizione nota riconosce l’errore geografico.'),
 34:('08_aggregazione',
     r'Griglia da 30 m: 24×30 celle. Aggregazione 2×2: 12×15 medie su celle da 60 m. Estensione e scala cromatica restano comuni. La media globale si conserva perché ogni blocco completo comprende quattro valori con uguale peso; estremi e dettaglio morfologico possono cambiare.'),
 39:('12_ricampionamento_continuo',
     r'Griglia originale da 30 m e griglie di uscita da 15 m, ottenute con vicino più prossimo e interpolazione bilineare realmente eseguiti in terra. Il numero di celle e la levigatezza cambiano; le misure disponibili restano quelle del raster originale. Bordi e mancanti richiedono regole esplicite.')}
for s in SLIDES:
    if s['page'] in PANORAMI:
        name,caption=PANORAMI[s['page']]
        s.update(layout='panorama',figure=name,caption=caption,snippet=None)
    if s['page']==14:s['title']='Un’inversione conserva l’istogramma'
    if s['page']==35:
        s['snippet']=code('r60 <- terra::aggregate(r,fact=2,fun=mean)\nm30 <- mean(terra::values(r))\nm60 <- mean(terra::values(r60))\nstopifnot(terra::ncell(r60)==180,\n abs(m30-m60)<1e-9)','R · aggregare e verificare')
assert not any(s.get('layout')=='panorama' and s['snippet'] for s in SLIDES)
