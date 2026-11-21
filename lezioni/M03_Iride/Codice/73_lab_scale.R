# Stesso seme; diversa dispersione
lA <- lab_scale(sdlog=.7,seed=17)
lB <- lab_scale(sdlog=1.2,seed=17)
rbind(A=lA$indicatori,
      B=lB$indicatori)
head(lA$dati)
