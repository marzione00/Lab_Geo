duplicati <- wk[
  duplicated(wk$data) |
    duplicated(wk$data, fromLast = TRUE), ]
nrow(duplicati)
# Qui il risultato e' zero.
# Con piu' sensori, controllare data + sensore.
