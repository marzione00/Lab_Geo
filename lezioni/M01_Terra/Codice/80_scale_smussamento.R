# Confronto dei numeri di punti.
n <- nrow(demo)
finestra <- 31
span <- 0.2
c(media_mobile = finestra,
  loess_circa = span * n)
# In demo: 31 contro circa 219 punti.
