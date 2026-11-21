I_W <- n/sum(W)*sum(W*outer(v,v))/sum(v^2)
confronto <- data.frame(matrice=c("A binaria","W per riga"),S0=c(sum(A),sum(W)),
  Moran_I=c(I_A,I_W))
confronto
write.csv(confronto,percorso_risultati("Moran_due_matrici.csv"),row.names=FALSE)
