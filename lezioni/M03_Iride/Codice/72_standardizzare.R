# Esempio deterministico asimmetrico
l_s <- c(1,2,3,12)
stopifnot(sd(l_s)>0)
l_z <- as.numeric(scale(l_s))
c(media=mean(l_z),sd=sd(l_z))
all.equal(l_z,
  (l_s-mean(l_s))/sd(l_s))
