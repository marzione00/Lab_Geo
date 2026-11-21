# Aprire il progetto Locus e usare questa cartella come directory corrente.
source("R/funzioni_M11.R",encoding="UTF-8")
d<-read.csv("Dati/spazio_v3.csv",stringsAsFactors=FALSE)
casuali<-read.csv("Dati/casuali_comuni_v3.csv")
xy<-as.matrix(d[c("x_m","y_m")]);z<-d$concentrazione;n<-nrow(d)
stopifnot(n==64,!anyDuplicated(d$id),!anyDuplicated(data.frame(xy)),
 !anyNA(d),all(is.finite(xy)),identical(sort(unique(d$x_m)),seq(0,1750,250)),
 identical(sort(unique(d$y_m)),seq(0,1750,250)))
D<-as.matrix(dist(xy));A<-1*(D>0&D<=260);nv<-rowSums(A);W<-normalizza_righe(A)
v<-z-mean(z);I_A<-moran_I(z,A);I_W<-moran_I(z,W)
lag_W<-as.vector(W%*%v)
train_idx<-d$x_m<1250;test_idx<-!train_idx
train<-d[train_idx,];test<-d[test_idx,]
stopifnot(sum(A)==224,sum(upper.tri(A)&A==1)==112,nrow(train)==40,nrow(test)==24)
options(width=100,digits=7)
