op <- par(no.readonly=TRUE);layout(matrix(1:3,nrow=1),widths=c(4,4,.7))
for(k in 1:2) {
  stile_grafico();par(mar=c(4.2,4,3,.4),cex=.8)
  image((1:28)*30,(1:22)*30,t(list(h1,h2)[[k]]),asp=1,col=gray.colors(40,start=0,end=1),
    zlim=c(0,1),xlab="x locale (m)",ylab="y locale (m)",main=paste("Azimut",c(315,135)[k]),useRaster=TRUE)
}
par(mar=c(4.2,0,3,2.7));plot.new();plot.window(xlim=c(0,1),ylim=c(0,1))
br <- seq(0,1,length.out=41)
rect(0,head(br,-1),.5,tail(br,-1),col=gray.colors(40,start=0,end=1),border=NA)
axis(4,at=c(0,.5,1),las=1);mtext("I",side=3,line=.5)
layout(1);par(op)
write.csv(risultato,percorso_risultati("illuminazioni.csv"),row.names=FALSE)
