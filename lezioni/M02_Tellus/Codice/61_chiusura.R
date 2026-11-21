# Tre parti nelle stesse unita
comp <- c(A = 40, B = 35, C = 25)
tot_comp <- sum(comp)
stopifnot(all(comp >= 0),
          tot_comp > 0)
chiusa <- 100 * comp / tot_comp
chiusa
sum(chiusa)                 # 100
