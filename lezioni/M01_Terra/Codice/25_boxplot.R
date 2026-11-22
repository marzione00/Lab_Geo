# Usa l'anteprima archiviata in terra
boxplot(valore ~ stazione, data = terra,
        ylab = "Concentrazione [mg/L]")
# Le medie non sono la linea nel box
tapply(terra$valore,
       terra$stazione, mean)
