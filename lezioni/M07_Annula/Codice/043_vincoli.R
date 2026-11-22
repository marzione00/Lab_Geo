# Con intercetta e minimi quadrati:
e43 <- residuals(m0)
c(somma = sum(e43),
  media = mean(e43))
# Anche X trasposta per e e' quasi 0.
X43 <- model.matrix(m0)
drop(crossprod(X43, e43))
