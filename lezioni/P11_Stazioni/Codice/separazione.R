d <- read.csv('dati/ml_v3.csv')
tr <- d$split=='train'
te <- d$split=='test'
stopifnot(sum(tr)==150,sum(te)==30,
 length(intersect(d$stazione[tr],
 d$stazione[te]))==0)
table(d$litologia,d$split)
