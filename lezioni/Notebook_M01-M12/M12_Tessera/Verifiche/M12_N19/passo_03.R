celle <- c(1:3,31:33)
a <- terra::xyFromCell(r,celle);b <- terra::xyFromCell(spostato,celle)
a <- sweep(a,2,c(500000,4999940),"-");b <- sweep(b,2,c(500000,4999940),"-")
stile_grafico()
plot(a,type="n",asp=1,xlim=c(-5,115),ylim=c(-5,90),
  xlab="E relativo al corner (m)",ylab="N relativo al riquadro (m)",
  main="Stesse dimensioni: centri traslati di 15 m")
for(x in seq(0,90,30)) segments(x,0,x,60,col="#B6CDD5")
for(y in seq(0,60,30)) segments(0,y,90,y,col="#B6CDD5")
arrows(a[,1],a[,2],b[,1],b[,2],length=.07,col="grey55")
points(a,pch=19,col=palette_geo[1]);points(b,pch=17,col=palette_geo[2])
legend("topleft",c("Originale","Traslato"),pch=c(19,17),col=palette_geo[1:2],bty="n",cex=.8)
write.csv(risultato,percorso_risultati("disallineamento.csv"),row.names=FALSE)
write.csv(audit,percorso_risultati("ricampionamento.csv"),row.names=FALSE)
