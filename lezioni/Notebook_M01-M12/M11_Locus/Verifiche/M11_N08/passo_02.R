risultato <- data.frame(area=c("Ovest","Est"),n=c(sum(ovest),sum(est)),
  media=c(mean(d$concentrazione[ovest]),mean(d$concentrazione[est])))
risultato
data.frame(siti_sul_confine=sum(d$x_m==1000),area_assegnata=unique(aree[d$x_m==1000]))
write.csv(risultato,percorso_risultati("sintesi_aree.csv"),row.names=FALSE)
