potenze <- 1:3
pesi <- sapply(potenze,function(p) {w<-r^-p;w/sum(w)})
q <- as.numeric(crossprod(d$concentrazione,pesi))
risultato <- data.frame(potenza=potenze,previsione=q,somma_pesi=colSums(pesi),
  peso_massimo=apply(pesi,2,max))
risultato
stopifnot(max(abs(colSums(pesi)-1))<1e-12,all(pesi>=0),
  all(q>=min(d$concentrazione)&q<=max(d$concentrazione)))
