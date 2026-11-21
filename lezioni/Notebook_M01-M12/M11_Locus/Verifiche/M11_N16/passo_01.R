d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 strada <- d$y_m<=250
 confronto <- data.frame(campione=c("Griglia di riferimento","Fascia strada"),
   n=c(nrow(d),sum(strada)),media=c(mean(d$concentrazione),mean(d$concentrazione[strada])))
 confronto
 stopifnot(sum(strada)==16L)
