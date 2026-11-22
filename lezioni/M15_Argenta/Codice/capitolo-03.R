rho <- function(m,v) {
 stopifnot(all(is.finite(v)),all(v>0))
 m/v
}
c(valida=rho(100,40),
  rifiuta_zero=inherits(try(rho(100,0),silent=TRUE),"try-error"))
