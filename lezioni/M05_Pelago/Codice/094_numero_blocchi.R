n94 <- 120
L94 <- c(1, 8, 30)
data.frame(lunghezza = L94,
  blocchi = ceiling(n94/L94))
# L=1: 120 blocchi individuali
# L=8: 15 blocchi
# L=30: 4 blocchi
