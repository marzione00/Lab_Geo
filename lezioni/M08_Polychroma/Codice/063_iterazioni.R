# Lloyd: una dimostrazione esplicita.
cent63 <- cent61
W63 <- numeric(5)
for (passo in 1:5) {
 dd <- sapply(1:2, function(g)
  rowSums(sweep(u59,2,cent63[g,])^2))
 lab <- max.col(-dd,
                ties.method="first")
 cent63 <- rowsum(u59,lab) /
   as.vector(table(lab))
 scarti63 <- u59-cent63[lab,]
 W63[passo] <- sum(scarti63^2)
}
W63
