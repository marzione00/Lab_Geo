# Una riga per stazione
medie <- aggregate(densita ~ stazione,
                   data = campioni,
                   FUN = mean)
medie
nrow(medie)         # Sei stazioni
