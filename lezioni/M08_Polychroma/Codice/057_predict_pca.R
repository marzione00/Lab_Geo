# Esempio su righe già presenti:
# verifica della trasformazione.
scores_nuovi <- predict(pc, X[1:3, ])
max(abs(scores_nuovi - pc$x[1:3, ]))
# Per veri nuovi campioni mantenere
# nomi, unità e ordine delle variabili.
