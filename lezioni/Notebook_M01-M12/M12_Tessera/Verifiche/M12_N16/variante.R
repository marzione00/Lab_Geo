nord30 <- as.vector(Z[2:24,]-Z[1:23,])
nord300 <- as.vector(Z[11:24,]-Z[1:14,])
data.frame(distanza_m=c(30,300),direzione="Nord-Sud",coppie=c(length(nord30),length(nord300)),
  media_abs=c(mean(abs(nord30)),mean(abs(nord300))))
stopifnot(length(nord30)==690L,length(nord300)==420L)
