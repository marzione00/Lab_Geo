# Colonne usate realmente dal modello.
X59 <- model.matrix(m_add)
colnames(X59)
head(X59, 6)
# La colonna iniziale vale sempre 1.
stopifnot(all(X59[, 1] == 1))
