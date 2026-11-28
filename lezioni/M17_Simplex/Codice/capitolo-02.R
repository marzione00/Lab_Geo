d <- read.csv('dati/composizioni_v1.csv')
b <- d[d$litologia=='Basalto',]
s <- b[c('CaO','MgO','FeO')]
s <- 100*s/rowSums(s)
round(c(cor(b$MgO,b$FeO),
  cor(s$MgO,s$FeO),
  var(log(b$MgO/b$FeO)),
  var(log(s$MgO/s$FeO))), 3)
