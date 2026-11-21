# Ordine esplicito dei morfotipi
r_g <- factor(fossili$morfotipo,
  levels=c("Rounded","Spiky"))
r_col <- c("#1D7890","#C57E42")[r_g]
plot(r_x,r_y,pch=c(16,17)[r_g],
  col=adjustcolor(r_col,alpha.f=.65),
  xlab="Diametro totale [um]",
  ylab="Diaframma [um]")
legend("topleft",levels(r_g),
 col=c("#1D7890","#C57E42"),pch=16:17)
