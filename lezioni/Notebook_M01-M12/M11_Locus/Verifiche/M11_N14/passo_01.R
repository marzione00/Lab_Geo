d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 A <- pesi_spaziali(d,260)$A
 v <- d$concentrazione-mean(d$concentrazione)
 f <- function(a) length(a)/sum(A)*sum(A*outer(a,a))/sum(a^2)
 osservato <- f(v)
 u <- carica_dati("casuali_comuni_v3.csv")$u
 B <- 100L
 stopifnot(length(u)>=B*length(v))
 data.frame(I_osservato=osservato,B=B,uniformi_usati=B*length(v),alternativa="positiva")
