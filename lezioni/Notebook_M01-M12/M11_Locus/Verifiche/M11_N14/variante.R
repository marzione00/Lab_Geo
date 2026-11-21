set.seed(20261114)
B2 <- 999L
nullo2 <- replicate(B2,f(v[sample.int(length(v))]))
p2 <- (1+sum(nullo2>=osservato))/(B2+1)
data.frame(protocollo=c("Originale: file u","Variante: seed 20261114"),
  B=c(B,B2),p=c(p,p2),risoluzione=c(1/(B+1),1/(B2+1)))
write.csv(data.frame(permutazione=seq_len(B2),I=nullo2),percorso_risultati("permutazioni_variante999.csv"),row.names=FALSE)
