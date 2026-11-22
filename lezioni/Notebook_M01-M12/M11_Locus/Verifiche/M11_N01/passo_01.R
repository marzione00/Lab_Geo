d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 controlli <- data.frame(controllo=c("64 siti","ID unici","Posizioni locali uniche",
   "Coordinate complete","Concentrazione completa"),
   esito=c(nrow(d)==64L,!anyDuplicated(d$id),!anyDuplicated(d[c("x_m","y_m")]),
     !anyNA(d[c("x_m","y_m","lon","lat")]),all(is.finite(d$concentrazione))))
 controlli
 stopifnot(all(controlli$esito))
