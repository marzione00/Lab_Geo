# Densita in g/cm^3, 4 provini/sito
st78 <- aggregate(densita ~ stazione,
                  provini, mean)
st78
mean(provini$densita)
mean(st78$densita)  # Stesso valore
table(provini$stazione)
