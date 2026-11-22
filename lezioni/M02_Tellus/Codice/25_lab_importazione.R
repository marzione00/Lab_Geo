# Cinque stringhe del laboratorio
testi <- c("1,2", "2,4", "3,1",
           "4,8", "ND")
z <- converti_misura(testi)
sum(!is.na(z$valore)) # Quattro numeri
mean(z$valore, na.rm = TRUE)
# 2.875: media delle quattro misure
