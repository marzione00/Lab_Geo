# Dati costruiti, in micrometri
a06 <- c(4, 5, 6)
b06 <- c(6, 7, 8)
mean(b06)-mean(a06)  # +2 um
mean(a06)-mean(b06)  # -2 um
# Cambio di unita: um -> mm
(mean(b06)-mean(a06))/1000
