# Terra01: stessi dati, due domande.
hist(terra$valore,
     xlab = "Concentrazione [mg/L]",
     main = "Tutte le misure")
boxplot(valore ~ stazione,
        data = terra,
        ylab="Concentrazione [mg/L]")
