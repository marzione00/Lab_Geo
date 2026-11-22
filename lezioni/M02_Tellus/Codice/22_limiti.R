# Un'informazione espressa come limite
t <- c("<0,05", "0,12", "ND")
z <- converti_misura(t)
data.frame(testo = t,
           valore = z$valore,
           limite = z$limite,
           stato = z$stato)
