# Stessa geometria per tutti i k.
set.seed(817)
ks <- 2:7
fits <- lapply(ks, function(k)
 kmeans(Z, k, nstart=50,
        iter.max=100))
W75 <- vapply(fits, function(m)
 m$tot.withinss, numeric(1))
data.frame(k=ks, WSS=W75)
plot(ks,W75,type="b",pch=19,
     xlab="k",ylab="WSS")
