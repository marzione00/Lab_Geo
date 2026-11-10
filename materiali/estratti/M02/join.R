campioni <- data.frame(id=c('p1','p2','p3'),
 sito=c('A','A','B'))
siti <- data.frame(sito=c('A','B'),quota=c(10,20))
stopifnot(!anyDuplicated(siti$sito))
j <- merge(campioni,siti,by='sito',all.x=TRUE)
stopifnot(nrow(j)==nrow(campioni))
stopifnot(!anyNA(j$quota))
