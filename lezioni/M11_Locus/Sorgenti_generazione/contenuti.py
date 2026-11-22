"""Locus: 110 slide, dati e risultati provenienti dal motore R incluso."""
from componenti import *
import parte01
import parte02
import parte03
import parte04
import parte05
assert len(SLIDES) == 109

# Le figure con più carte occupano tutta la larghezza per mantenere leggibili
# assi, legende e campioni. I frammenti R restano nelle pagine a due colonne.
PANORAMI = {
 11: ('03_supporto_blocchi',
      r'Quattro blocchi, 16 siti ciascuno. La media dei siti pesa ogni osservazione allo stesso modo; la media semplice dei blocchi pesa ogni blocco allo stesso modo. Qui coincidono perché le numerosità sono uguali. Per interpretare una media come areale servono pesi coerenti con le aree rappresentate o con il disegno.'),
 67: ('22_trend_residui',
      r'Sui dati $I_A='+value('Moran','I_A')+r'$; sui residui del piano $I_A='+value('Moran','I_residui_A')+r'$. Il confronto è descrittivo: parte dell’associazione globale è legata alla variazione della media. La domanda sulla dipendenza residua richiede un riferimento coerente con la stima del piano. Non si presenta una permutazione libera dei residui come test esatto.'),
 77: ('26_direzionali',
      r'Le coppie sono raggruppate per distanza e direzione con tolleranze dichiarate nei calcoli. Un riassunto omnidirezionale può nascondere differenze orientate. Trend, numerosità e geometria del campione incidono sul confronto: la differenza fra curve non basta da sola a identificare anisotropia del processo.'),
}
for s in SLIDES:
    if s['page'] in PANORAMI:
        name,caption=PANORAMI[s['page']]
        s.update(layout='panorama',figure=name,caption=caption)

