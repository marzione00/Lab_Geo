# Densita: g/cm^3, dati costruiti
n09 <- c(2,8)
m09 <- c(2.4,2.8)
weighted.mean(m09,n09) # 2.72
mean(m09)             # 2.60
c(peso_misure=n09[1]/sum(n09),
  peso_stazioni=1/length(n09))
