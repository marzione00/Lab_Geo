coppie$classe <- cut(coppie$h,c(0,300,600,1000,2500))
risultato <- aggregate(cbind(h,gamma)~classe,coppie,mean)
risultato$n <- as.numeric(table(coppie$classe)[as.character(risultato$classe)])
risultato
stopifnot(sum(risultato$n)==2016L,!anyNA(coppie$classe))
