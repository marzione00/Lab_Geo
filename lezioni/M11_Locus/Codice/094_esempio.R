sapply(1:3,function(p)
 idw_pred(xy,z,
          matrix(c(900,900),nrow=1),
          p=p))
