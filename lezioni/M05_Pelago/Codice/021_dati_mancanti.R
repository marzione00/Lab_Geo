# Registrare ogni esito del prelievo
d21 <- data.frame(
 id=1:6,
 misura=c(2.4,NA,2.7,2.5,NA,2.8),
 esito=c("ok","perso","ok","ok",
         "non accessibile","ok"))
table(d21$esito)
mean(d21$misura,na.rm=TRUE)
