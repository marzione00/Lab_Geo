inverso <- d[nrow(d):1,]
Di <- as.matrix(dist(inverso[c("x_m","y_m")]));diag(Di) <- Inf
ji <- apply(Di,1,which.min)
vicini_i <- setNames(inverso$id[ji],inverso$id)
confronto <- data.frame(id=d$id,prima=risultato$vicino,dopo=unname(vicini_i[d$id]))
data.frame(scelte_cambiate=sum(confronto$prima!=confronto$dopo),siti=nrow(d))
head(confronto,6)
