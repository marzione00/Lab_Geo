d <- read.csv('dati/progetti/faithful.csv')
s <- read.csv(paste0('dati/progetti/',
 'piani_ricampionamento/faithful_split.csv'))
d <- merge(d,s,by='row_id',sort=TRUE)
tr <- d[d$set=='train',]
te <- d[d$set=='test',]
stopifnot(nrow(tr)==190,nrow(te)==82,
 !length(intersect(tr$row_id,te$row_id)))
