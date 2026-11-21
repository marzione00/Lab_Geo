stile_grafico()
plot(d$x_m,d$y_m,pch=19,col=palette_geo[1],asp=1,ylim=c(0,1900),
  xlab="x locale (m)",ylab="y locale (m)",main="64 siti su una griglia locale")
text(d$x_m[c(1,8,57,64)],d$y_m[c(1,8,57,64)],d$id[c(1,8,57,64)],pos=3,cex=.8)
write.csv(controlli,percorso_risultati("audit.csv"),row.names=FALSE)
write.csv(intervalli,percorso_risultati("intervalli_coordinate.csv"),row.names=FALSE)
