writeLines(rapporto,percorso_risultati("relazione_progetto_base.txt"),useBytes=TRUE)
write.csv(audit,percorso_risultati("audit_progetto.csv"),row.names=FALSE)
write.csv(confronto,percorso_risultati("metriche_progetto.csv"),row.names=FALSE)
write.csv(data.frame(id=te$id,osservato=te$diametro_int_um,previsto=prev),
  percorso_risultati("previsioni_fossili.csv"),row.names=FALSE)
saveRDS(mod,percorso_risultati("modello_fossili.rds"))
stopifnot(identical(readLines(percorso_risultati("relazione_progetto_base.txt"),warn=FALSE),rapporto))
data.frame(righe_relazione=length(rapporto),previsioni=nrow(te),rilettura_identica=TRUE)
