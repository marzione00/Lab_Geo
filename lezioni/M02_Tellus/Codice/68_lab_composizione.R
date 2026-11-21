# Stesso modello del laboratorio
scenari <- c(40, 80)
percentuali <- sapply(scenari,
  function(a) {
    v <- c(A = a, B = 35, C = 25)
    100 * v / sum(v)
  })
colnames(percentuali) <- scenari
percentuali
