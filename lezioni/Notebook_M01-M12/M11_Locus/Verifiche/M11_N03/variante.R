deformate <- xy;deformate[,1] <- 2*deformate[,1]
D2 <- as.matrix(dist(deformate))
data.frame(coppia=c("S01-S02","S01-S09","S01-S64"),
  prima=D[1,c(2,9,64)],dopo=D2[1,c(2,9,64)])
stopifnot(D2[1,2]==2*D[1,2],D2[1,9]==D[1,9])
