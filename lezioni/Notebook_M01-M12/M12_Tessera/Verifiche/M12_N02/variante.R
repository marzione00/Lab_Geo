mescolata <- d[nrow(d):1,]
ricostruita <- matrice_quote(mescolata)
data.frame(massimo_scarto=max(abs(ricostruita-Z)),
  errore_senza_ordine=max(abs(matrix(mescolata$quota_m,24,byrow=TRUE)-Z)))
stopifnot(identical(ricostruita,Z))
