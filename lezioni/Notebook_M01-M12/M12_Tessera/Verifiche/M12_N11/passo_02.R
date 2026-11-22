g <- gradienti_centrali(Z)
soglia <- 1e-8
esposizione <- g$azimut_discesa;esposizione[g$modulo<=soglia] <- NA_real_
data.frame(celle_interne=length(esposizione),direzioni_valide=sum(is.finite(esposizione)),
  minimo= min(esposizione,na.rm=TRUE),massimo=max(esposizione,na.rm=TRUE),
  soglia_gradiente=soglia)
stopifnot(all(esposizione[is.finite(esposizione)]>=0 & esposizione[is.finite(esposizione)]<360))
