d <- data.frame(id=1:3,m=c(107.2,121.95,132.5))
f <- tempfile(fileext=".csv")
write.csv(d,f,row.names=FALSE)
isTRUE(all.equal(d,read.csv(f)))
