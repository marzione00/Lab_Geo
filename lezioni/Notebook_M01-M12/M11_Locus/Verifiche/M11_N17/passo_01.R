d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 d$blocco <- paste0(ifelse(d$y_m>=1000,"N","S"),ifelse(d$x_m>=1000,"E","O"))
 sintesi <- aggregate(concentrazione~blocco,d,mean)
 numerosita <- table(d$blocco)
 sintesi$n <- as.numeric(numerosita[sintesi$blocco])
 sintesi
 stopifnot(all(sintesi$n==16L),sum(sintesi$n)==64L)
