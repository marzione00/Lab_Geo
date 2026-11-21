pred30 <- rep(ultimo_anno,length.out=30)
stopifnot(identical(pred30[25:30],ultimo_anno[1:6]))
data.frame(h=25:30,previsto=pred30[25:30])
