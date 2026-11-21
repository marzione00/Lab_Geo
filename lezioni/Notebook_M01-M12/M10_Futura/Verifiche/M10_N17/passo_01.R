p <- carica_dati("processi_simulati.csv"); mod <- stima_var(p)
h <- 10L
stato <- as.numeric(tail(mod$v,1))
prev <- matrix(NA_real_,h,2,dimnames=list(NULL,c("X","Y")))
for(k in seq_len(h)) {
  stato <- as.numeric(mod$intercetta+mod$A%*%stato)
  prev[k,] <- stato
}
data.frame(passo=251:260,prev)
