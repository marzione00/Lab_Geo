# L'effetto vero resta Delta=.3.
z88 <- lab_relazione(n=30)
w88 <- lab_relazione(n=120)
rbind(n30=z88$metrics,
      n120=w88$metrics)
z88$data[c("x","lo","hi")]
