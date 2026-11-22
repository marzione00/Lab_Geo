# Grafici di supporto alle slide 45 e 47.
# Nuova simulazione dichiarata: variabili indipendenti Exp(rate=1), seed 17.
# La banda LLN e' una guida +/-2/sqrt(n), non una banda simultanea esatta.
# Nel progetto distribuito aggiorna Risorse/Figure; in una cartella di lavoro
# autonoma senza Risorse usa Figure.
dir_fig <- if (dir.exists("Risorse")) file.path("Risorse","Figure") else "Figure"
dir.create(dir_fig, showWarnings=FALSE, recursive=TRUE)

set.seed(17)
x <- rexp(1000, rate=1)
n <- seq_along(x)
m <- cumsum(x)/n
stopifnot(min(m)>=-1,max(m)<=3)
cat("Intervallo delle medie cumulative:",range(m),"\n")
pdf(file.path(dir_fig,"lln_leggibile.pdf"), width=7.1, height=1.9,
    pointsize=11, family="Helvetica", useDingbats=FALSE)
par(mar=c(3.1,3.5,.3,.6), mgp=c(1.85,.55,0), tcl=-.2,
    col.axis="#253344", col.lab="#253344", bty="l", las=1)
plot(n,m,type="l",col="#1D7890",lwd=1.4,
     xlab="Numerosità cumulativa n",ylab="Media cumulativa",ylim=c(-1,3))
abline(h=1,col="#7363AA",lwd=1.2)
lines(n,1+2/sqrt(n),col="#657180",lty=2,lwd=.9)
lines(n,1-2/sqrt(n),col="#657180",lty=2,lwd=.9)
legend("topright",legend=expression("Media cumulativa","Media teorica = 1",
                                    "Guida: "*(1 %+-% 2/sqrt(n))),
       col=c("#1D7890","#7363AA","#657180"),lty=c(1,1,2),lwd=c(1.4,1.2,.9),
       bty="n",cex=.9,horiz=TRUE,x.intersp=.6,y.intersp=.9)
dev.off()

set.seed(17)
numerosita <- c(1L,5L,30L)
z_pannelli <- lapply(numerosita,function(nn) {
  set.seed(17)
  sqrt(nn)*(replicate(3000,mean(rexp(nn,rate=1)))-1)
})
limiti_z <- c(min(-4,floor(min(unlist(z_pannelli)))),
              max(6,ceiling(max(unlist(z_pannelli)))))
cat("Range z simulati:",range(unlist(z_pannelli)),"; finestra comune:",limiti_z,"\n")
pdf(file.path(dir_fig,"clt_leggibile.pdf"), width=7.1, height=2.0,
    pointsize=11, family="Helvetica", useDingbats=FALSE)
par(mfrow=c(1,3),mar=c(3.1,3.1,1.6,.4),mgp=c(1.85,.5,0),tcl=-.2,
    col.axis="#253344",col.lab="#253344",col.main="#15283E",bty="l",las=1,
    cex=1,cex.main=1)
for (j in seq_along(numerosita)) {
  n <- numerosita[j]
  z <- z_pannelli[[j]] # Stesso seed 17 per ciascun pannello.
  hist(z,probability=TRUE,breaks=30,main=paste("n =",n),
       xlim=limiti_z,ylim=c(0,1),xlab="Z",ylab=if(n==1) "Densità" else "",
       col="#BFDDE1",border="#FFFFFF")
  curve(dnorm(x),add=TRUE,col="#7363AA",lwd=1.4)
}
dev.off()
cat("LLN e CLT: PDF aggiornati con font 11, seed 17.\n")
