# Esperimento m04-binomiale
a33 <- lab_binomiale(n=20, prob=.3)
b33 <- lab_binomiale(n=40, prob=.3)
a33$indicatori
b33$indicatori
# Il sito usa 400 repliche
length(a33$simulazioni)
