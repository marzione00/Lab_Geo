densita <- function(m,v) m/v
atteso <- 2.5
isTRUE(all.equal(densita(100,40),atteso))
