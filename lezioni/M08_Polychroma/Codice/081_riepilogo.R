# Indici per le stesse soluzioni.
data.frame(k=ks,
 WSS=round(W75,2),
 silhouette=round(S79,3),
 minimo_gruppo=vapply(fits,
  function(m)min(m$size),numeric(1)))
# La scelta non legge la litologia.
ks[which.max(S79)]
