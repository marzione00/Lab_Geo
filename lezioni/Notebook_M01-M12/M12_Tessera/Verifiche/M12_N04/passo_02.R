osservati <- sum(!is.na(mascherata))
data.frame(n_disponibili=osservati,n_totale=length(Z),
  rapporto_medie=mean(errata)/mean(mascherata,na.rm=TRUE),
  copertura=osservati/length(Z),
  differenza_dalla_media_completa=mean(mascherata,na.rm=TRUE)-mean(Z))
stopifnot(abs(mean(errata)-mean(mascherata,na.rm=TRUE)*osservati/length(Z))<1e-10)
