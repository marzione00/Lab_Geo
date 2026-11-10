d <- read.csv('dati/progetti/faithful.csv')
s <- read.csv(paste0('dati/progetti/',
 'piani_ricampionamento/faithful_split.csv'))
d <- merge(d,s,by='row_id')
tr <- d[d$set=='train',]; te <- d[d$set=='test',]
f <- lm(waiting_min~eruption_min,tr)
pred <- predict(f,te)
sqrt(mean((te$waiting_min-pred)^2))
