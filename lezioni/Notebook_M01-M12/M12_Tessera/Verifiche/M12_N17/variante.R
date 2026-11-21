set.seed(20261117)
celle <- as.vector(Z)
iid <- replicate(300,mean(celle[sample.int(length(celle),length(celle),replace=TRUE)]))
confronto <- data.frame(schema=c("Blocchi originali","Singole celle: ipotesi iid"),
  sd_repliche=c(sd(b),sd(iid)),basso=c(unname(q[1]),unname(quantile(iid,.025))),
  alto=c(unname(q[2]),unname(quantile(iid,.975))))
confronto
write.csv(confronto,percorso_risultati("confronto_meccanismi_bootstrap.csv"),row.names=FALSE)
