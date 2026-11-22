distanze <- distanze_incrociate(d[c("x_m","y_m")],d[strada,c("x_m","y_m")])
copertura <- apply(distanze,1,min)
data.frame(distanza_media_m=mean(copertura),distanza_massima_m=max(copertura),
  siti_oltre500m=sum(copertura>500))
write.csv(confronto,percorso_risultati("confronto_strada.csv"),row.names=FALSE)
write.csv(data.frame(id=d$id,selezionato=strada,distanza_piu_vicino_m=copertura),
  percorso_risultati("copertura_strada.csv"),row.names=FALSE)
