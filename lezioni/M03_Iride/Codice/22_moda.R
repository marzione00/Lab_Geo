# Esempio discreto con ripetizioni
x22 <- c(1, 1, 2, 3, 4)
f22 <- table(x22)
names(f22)[f22 == max(f22)] # "1"
# mode() descrive il tipo, non la moda
mode(x22)                  # "numeric"
