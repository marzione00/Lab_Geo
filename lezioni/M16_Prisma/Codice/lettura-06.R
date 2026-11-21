d <- read.csv('dati/ml_v3.csv')
tr <- d$split=='train'; te <- !tr
stopifnot(!anyDuplicated(d$id),
 sum(tr)==150,sum(te)==30,
 length(intersect(d$stazione[tr],
 d$stazione[te]))==0)
table(d$litologia,d$split)
