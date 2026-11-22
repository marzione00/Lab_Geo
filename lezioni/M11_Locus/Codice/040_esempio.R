data.frame(raggio=raggi,
 n=sapply(raggi,function(r)
   sum(dist0<=r)),
 media=sapply(raggi,function(r)
   mean(z[dist0<=r])))
