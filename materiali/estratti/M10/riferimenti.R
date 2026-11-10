d <- read.csv('dati/co2_1985_2001.csv')
tr <- d$co2_ppm[1:168]; h <- 36
ultimo <- rep(tail(tr,1),h)
stagionale <- rep(tail(tr,12),length.out=h)
deriva <- (tail(tr,1)-head(tr,1))/(length(tr)-1)
con_deriva <- tail(tr,1)+(1:h)*deriva
head(data.frame(ultimo,stagionale,con_deriva))
