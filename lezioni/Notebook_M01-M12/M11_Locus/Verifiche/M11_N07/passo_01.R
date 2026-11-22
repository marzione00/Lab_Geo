d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 data.frame(n=nrow(d),minimo=min(d$concentrazione),massimo=max(d$concentrazione),
   media=mean(d$concentrazione),deviazione_standard=sd(d$concentrazione),unita="u.a.")
 quantile(d$concentrazione,c(0,.25,.5,.75,1))
