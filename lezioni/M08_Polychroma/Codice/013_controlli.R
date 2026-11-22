data.frame(variabile = colnames(X),
  mancanti = colSums(is.na(X)),
  deviazione = apply(X, 2, sd))
# Un valore NA non significa zero.
# Una colonna costante non ammette z-score.
