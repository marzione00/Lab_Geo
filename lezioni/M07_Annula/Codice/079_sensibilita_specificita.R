# tab78: righe osservate, colonne previste.
TP79 <- tab78["1", "1"]
FN79 <- tab78["1", "0"]
TN79 <- tab78["0", "0"]
FP79 <- tab78["0", "1"]
c(sensibilita = TP79/(TP79+FN79),
  specificita = TN79/(TN79+FP79))
