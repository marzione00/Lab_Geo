# Fattori positivi adimensionali
f50 <- c(1.2, .8, 1.1)
prod(f50)       # Prodotto: 1.056
exp(sum(log(f50)))
# Stesso risultato entro precisione
all.equal(log(prod(f50)),
          sum(log(f50)))
