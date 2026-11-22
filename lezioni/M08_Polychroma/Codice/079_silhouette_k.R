# Le soluzioni di k = 2,...,7.
S79 <- vapply(fits, function(m)
 mean(silhouette_base(m$cluster,D)),
 numeric(1))
indici <- data.frame(k=ks,WSS=W75,
                      silhouette=S79)
indici
plot(ks,S79,type="b",pch=19,
 xlab="k",ylab="Silhouette media")
