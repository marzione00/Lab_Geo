nuovo <- data.frame(diametro_tot_um = 7)
# Incertezza della media condizionata.
predict(m0, newdata = nuovo,
        interval = "confidence")
# Variabilita di un nuovo individuo.
predict(m0, newdata = nuovo,
        interval = "prediction")
