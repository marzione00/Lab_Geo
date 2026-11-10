set.seed(311)
indici <- sample.int(n,n,replace=TRUE)
replica <- x[indici]
frequenze <- tabulate(indici,nbins=n)
