d <- read.csv('dati/campioni_modulo1.csv')
d$densita <- d$massa_g/d$volume_cm3
sintesi <- function(x) c(
 n=length(x), disponibili=sum(!is.na(x)),
 media=mean(x,na.rm=TRUE), sd=sd(x,na.rm=TRUE))
aggregate(densita ~ stazione,d,sintesi,
          na.action=na.pass)
