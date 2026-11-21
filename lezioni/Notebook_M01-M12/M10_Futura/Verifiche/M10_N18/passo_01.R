p <- carica_dati("processi_simulati.csv"); mod <- stima_var(p)
pr <- prevedi_var(mod,10)
obs <- as.matrix(p[251:260,c("x_VAR","y_VAR")])
tab <- data.frame(origine=250L,passo=251:260,h=1:10,
  X_osservata=obs[,1],Y_osservata=obs[,2],X_prevista=pr[,1],Y_prevista=pr[,2])
write.csv(tab,percorso_risultati("consegna_VAR.csv"),row.names=FALSE)
saveRDS(mod,percorso_risultati("modello_VAR.rds"))
head(tab,3)
