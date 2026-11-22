scalato <- (100*nir-100*rosso)/(100*nir+100*rosso)
offset <- ((nir+.1)-(rosso+.1))/((nir+.1)+(rosso+.1))
data.frame(errore_fattore_comune=max(abs(scalato-indice)),
  variazione_offset=max(abs(offset-indice)))
stopifnot(max(abs(scalato-indice))<1e-12,max(abs(offset-indice))>0)
