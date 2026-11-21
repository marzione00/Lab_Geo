x40 <- proc$ar1
coppie1 <- data.frame(
  passato = head(x40, -1),
  presente = tail(x40, -1))
head(coppie1)
nrow(coppie1)
# 300 valori generano 299 coppie al ritardo 1.
