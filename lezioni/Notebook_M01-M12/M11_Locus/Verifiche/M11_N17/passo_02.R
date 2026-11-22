media_siti <- mean(d$concentrazione)
media_blocchi <- mean(sintesi$concentrazione)
media_pesata <- weighted.mean(sintesi$concentrazione,sintesi$n)
data.frame(calcolo=c("Tutti i siti","Blocchi con peso uguale","Blocchi pesati per n"),
  valore=c(media_siti,media_blocchi,media_pesata))
stopifnot(abs(media_siti-media_blocchi)<1e-12,abs(media_siti-media_pesata)<1e-12)
