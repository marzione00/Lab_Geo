controllo <- data.frame(media_celle=mean(d$quota_m),media_zone=mean(risultato$media),
  media_zone_pesata=weighted.mean(risultato$media,risultato$n))
controllo
stopifnot(abs(controllo$media_celle-controllo$media_zone_pesata)<1e-10)
