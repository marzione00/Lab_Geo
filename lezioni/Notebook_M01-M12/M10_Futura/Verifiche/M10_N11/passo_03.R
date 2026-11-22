confronto <- rbind(Media_train=metriche(te$diametro_int_um,base),
                    Regressione=metriche(te$diametro_int_um,prev))
confronto
write.csv(confronto,percorso_risultati("metriche_fossili.csv"))
