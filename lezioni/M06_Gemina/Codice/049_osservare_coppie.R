d49 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
stopifnot(!anyDuplicated(d49$id))
D49 <- d49$dopo-d49$prima
# Una differenza per provino
c(n=length(D49), media=mean(D49))
plot(D49, ylab="Dopo - prima (u.c.)",
     xlab="Indice del provino")
abline(h=0, lty=2)
qqnorm(D49); qqline(D49)
