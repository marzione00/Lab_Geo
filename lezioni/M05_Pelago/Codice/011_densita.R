# Due provini costruiti
m11 <- c(96,168)   # massa: g
v11 <- c(40,60)    # volume: cm^3
rho11 <- m11/v11
mean(rho11)       # 2.60 g/cm^3
sum(m11)/sum(v11) # 2.64 g/cm^3
weighted.mean(rho11,v11)
