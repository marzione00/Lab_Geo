# Formule definite nel progetto.
formule <- formule_annula()
# Stessi fold per tutti i modelli.
cv <- valida_annula(training, fold,
                   formule)
cv[order(cv$RMSE), ]
scelta <- cv$modello[
  which.min(cv$RMSE)]
