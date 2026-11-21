# Esempio costruito: gruppi A e B
t12 <- matrix(c(10, 40, 20, 80),
  nrow = 2, byrow = TRUE,
  dimnames = list(c("A", "B"),
    c("evento", "assenza")))
t12
prop.table(t12, margin = 1) # Per riga
prop.table(t12, margin = 2) # Colonne
