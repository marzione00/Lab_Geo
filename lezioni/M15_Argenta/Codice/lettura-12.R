densita <- function(m,v) {
 stopifnot(is.numeric(m),is.numeric(v),
  length(m)==length(v),length(m)>0,
  all(is.finite(m)),all(is.finite(v)),
  all(m>0),all(v>0))
 m/v
}
stopifnot(densita(10,4)==2.5)
errore <- tryCatch({densita(10,0);FALSE},
 error=function(e)TRUE)
stopifnot(errore)
