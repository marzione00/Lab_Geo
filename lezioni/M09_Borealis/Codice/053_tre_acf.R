for (nome in c("rumore_bianco", "ar1",
               "random_walk")) {
  acf(proc[[nome]], lag.max = 24, main = nome)
}
