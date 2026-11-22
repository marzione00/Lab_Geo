# Figure scientifiche del modulo, rigenerabili in R di base dai CSV archiviati.
source("setup.R")
dest <- if (dir.exists("Risorse")) file.path("Risorse","Figure") else "Figure"
dir.create(dest, recursive=TRUE, showWarnings=FALSE)
ink <- "#253344"; teal <- "#1D7890"; amber <- "#C57E42"
paper <- "#F8F6F1"; muted <- "#657180"

# Geometria: il colore riguarda soltanto i vincoli sui due diametri.
g <- fossili[is.finite(fossili$diametro_tot_um) &
             is.finite(fossili$diametro_int_um), ]
ok <- with(g, diametro_tot_um > 0 & diametro_int_um >= 0 &
            diametro_int_um <= diametro_tot_um)
pdf(file.path(dest,"geometria_fossili.pdf"), width=4.8, height=3,
    pointsize=11, family="Helvetica", bg=paper)
par(mar=c(3.2,3.4,.5,.5), mgp=c(2,.6,0), tcl=-.22,
    col.axis=ink, col.lab=ink, fg=muted, las=1, pty="s")
plot(g$diametro_tot_um, g$diametro_int_um, type="n",
     xlim=c(-6,13), ylim=c(-6,13), xaxs="i", yaxs="i", asp=1,
     xlab=expression(D[esterno]~"["*mu*"m]"),
     ylab=expression(D[interno]~"["*mu*"m]"))
abline(h=0,v=0,col="#D6DAD9",lwd=.7)
abline(a=0,b=1,col=muted,lty=2,lwd=1)
points(g$diametro_tot_um[ok],g$diametro_int_um[ok],pch=16,col=teal,cex=.7)
points(g$diametro_tot_um[!ok],g$diametro_int_um[!ok],pch=17,col=amber,cex=.9)
text(g$diametro_tot_um[!ok],g$diametro_int_um[!ok],g$id[!ok],
     pos=c(4,4),offset=.4,cex=.8,col=ink)
legend("bottomright",c("Compatibile","Da verificare"),pch=c(16,17),
       col=c(teal,amber),bty="n",cex=.78,inset=.015)
dev.off()
cat("Geometria:",nrow(g),"coppie finite;",sum(!ok),"coppie incompatibili.\n")
