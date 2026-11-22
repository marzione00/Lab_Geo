# Medie e conteggi allineati per nome
m <- tapply(campioni$densita,
            campioni$stazione, mean)
n <- table(campioni$stazione)
weighted.mean(m, n[names(m)])
mean(campioni$densita)
mean(m)  # Quattro misure per stazione
