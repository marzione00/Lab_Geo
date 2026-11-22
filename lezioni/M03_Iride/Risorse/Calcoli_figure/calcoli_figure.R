f <- read.csv("Dati/fossili_simulati.csv")
x <- f$diametro_tot_um
dir.create("figure_data", showWarnings = FALSE)
for (b in c(.15, .4, 1.2)) {
  k <- density(x, bw = b, from = 2, to = 14, n = 256)
  write.csv(data.frame(x=k$x, y=k$y),
    paste0("figure_data/density_",b,".csv"),row.names=FALSE)
}
for (b in c(.5,1)) {
  h <- hist(x, breaks=seq(2,14,by=b), plot=FALSE)
  write.csv(data.frame(left=head(h$breaks,-1),right=tail(h$breaks,-1),
    n=h$counts,density=h$density),paste0("figure_data/hist_",b,".csv"),row.names=FALSE)
}
for (g in c("Rounded","Spiky")) {
  v <- x[f$morfotipo==g]
  k <- density(v,bw=.4,from=2,to=14,n=256)
  write.csv(data.frame(x=k$x,y=k$y),paste0("figure_data/group_",g,".csv"),row.names=FALSE)
  b <- boxplot.stats(v)
  write.csv(data.frame(pos=1:5,value=b$stats),paste0("figure_data/box_",g,".csv"),row.names=FALSE)
  q <- quantile(v,c(.25,.5,.75),type=7)
  cat(g,length(v),mean(v),sd(v),q,IQR(v,type=7),"\n")
}
print(quantile(c(1,2,4,7,8,9,10,12),c(.25,.5,.75),type=7))
print(boxplot.stats(c(1,2,4,7,8,9,10,12))$stats)
print(boxplot.stats(c(1,2,3,4,5,6,7,8,20)))
set.seed(303)
pos <- as.integer(factor(f$morfotipo, levels=c("Rounded","Spiky")))
pos <- pos + runif(length(pos), -.12, .12)
write.csv(data.frame(pos=pos, diam=x, gruppo=f$morfotipo),
          "figure_data/jitter.csv", row.names=FALSE)
