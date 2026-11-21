classe <- cut(h_pair,
 breaks=c(0,300,600,1000,2500))
aggregate(cbind(h=h_pair,gamma=g_pair),
          list(classe=classe),mean)
