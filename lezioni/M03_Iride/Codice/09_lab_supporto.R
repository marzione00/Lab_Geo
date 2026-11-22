# Stesso seme, rumore diverso
a09 <- lab_supporto(noise = 1)
b09 <- lab_supporto(noise = 3)
a09$indicatori
b09$indicatori
# Ogni stazione conserva 8 misure
table(a09$dati$gruppo)
