# Esempio in mg/L: cinque misure.
x <- c(1, 2, 2, 3, 7)
diff(range(x))   # ampiezza: 6
sd(x)           # circa 2.35 mg/L
quantile(x)     # quartili e estremi
IQR(x)          # Q3 - Q1: 1 mg/L
