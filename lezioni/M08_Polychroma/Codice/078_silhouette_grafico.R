# Distribuzione delle 90 silhouette.
ord78 <- order(km$cluster,sil)
barplot(sil[ord78], space=0,
 col=km$cluster[ord78], border=NA,
 ylab="Silhouette",xlab="Campioni")
abline(h=0,lty=2)
c(media=mean(sil),minimo=min(sil),
  massimo=max(sil))
