# Calcolo teorico, sd comune = 1
z81 <- lab_potenza(n=30)
w81 <- lab_potenza(n=120)
rbind(n30=z81$metrics,
      n120=w81$metrics)
# Delta=.5 e alfa=.05 restano fissi.
