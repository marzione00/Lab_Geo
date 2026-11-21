# Ogni colonna e' un nuovo campione.
set.seed(17)
X25 <- replicate(5,
  rnorm(4,mean=10,sd=2))
round(X25,2)
colMeans(X25) # una stima per campione
dim(X25)     # 4 misure x 5 campioni
