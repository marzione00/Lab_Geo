# Correlazione dei log uguale a 0
s75 <- c(.02, .1, .2, .3)
t275 <- 2*s75^2
a75 <- 2*sqrt(t275)
e75 <- 2*sqrt(expm1(t275)*exp(t275))
data.frame(sdlog = s75,
  approssimata = a75, esatta = e75,
  scarto_percento = 100*(e75-a75)/e75)
