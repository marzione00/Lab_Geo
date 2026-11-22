# Stessa media, tassi differenti
a41 <- lab_poisson(rate=2,
                  exposure=3)
b41 <- lab_poisson(rate=1,
                  exposure=6)
a41$indicatori
b41$indicatori
all.equal(a41$dati, b41$dati)
