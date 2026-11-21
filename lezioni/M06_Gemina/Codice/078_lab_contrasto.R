source("setup.R", encoding="UTF-8")
# Cambia solo la differenza vera.
z78 <- lab_contrasto(delta=1)
w78 <- lab_contrasto(delta=0)
rbind(delta1=z78$metrics,
      delta0=w78$metrics)
