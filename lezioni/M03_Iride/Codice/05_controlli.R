# Variabile e unita': diametro in um
x05 <- fossili$diametro_tot_um
c(n = length(x05),
  mancanti = sum(is.na(x05)))
stopifnot(!anyDuplicated(fossili$id))
stopifnot(all(is.finite(x05)))
stopifnot(all(x05 > 0))
summary(x05)
