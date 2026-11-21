metriche(ritorno$osservato,ritorno$previsto)
write.csv(as.data.frame(t(metriche(ritorno$osservato,ritorno$previsto))),
  percorso_risultati("metriche_da_csv.csv"),row.names=FALSE)
