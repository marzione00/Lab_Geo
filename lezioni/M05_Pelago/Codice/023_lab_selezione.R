# Il sito genera direttamente stime.
a23 <- lab_selezione(n=60,bias=1)
b23 <- lab_selezione(n=300,bias=1)
a23$indicatori
b23$indicatori
c23 <- lab_selezione(n=60,bias=0)
c23$indicatori
