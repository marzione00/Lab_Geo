incompleta <- Z;incompleta[1,1] <- NA_real_
a_na <- aggrega_blocchi(incompleta,2,2)
confronto <- data.frame(media_celle=mean(incompleta,na.rm=TRUE),
  media_blocchi=mean(a_na$media),media_pesata=weighted.mean(a_na$media,a_na$numero))
confronto
stopifnot(abs(confronto$media_celle-confronto$media_pesata)<1e-10)
