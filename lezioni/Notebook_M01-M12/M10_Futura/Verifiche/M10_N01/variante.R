tr97 <- window(c2$y,end=c(1997,12)); te97 <- window(c2$y,start=c(1998,1))
data.frame(origine="1997-12",n_train=length(tr97),n_test=length(te97))
stopifnot(length(tr97)+length(te97)==204L)
