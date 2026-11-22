# Una dipendenza da ricalcolare
x <- 1:3
a <- 2
z <- a * x
a <- 3
z                 # Ancora 2, 4, 6
z <- a * x        # Ricalcolo
z                 # Ora 3, 6, 9
