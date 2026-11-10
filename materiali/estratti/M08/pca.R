d <- read.csv('dati/rocce_simulate.csv')
v <- c('SiO2','CaO','MgO','FeO',
       'densita','grana_mm','colore','fossili')
pc <- prcomp(d[v],center=TRUE,scale.=TRUE)
quota <- pc$sdev^2/sum(pc$sdev^2)
round(quota,3)
round(pc$rotation[,1:2],3)
head(predict(pc,d[v]))
