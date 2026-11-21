selettiva <- Z;selettiva[Z>quantile(Z,.9)] <- NA_real_
data.frame(caso=c("Completo","Maschera rettangolare","Decile alto escluso"),
  copertura=c(1,mean(!is.na(mascherata)),mean(!is.na(selettiva))),
  media=c(mean(Z),mean(mascherata,na.rm=TRUE),mean(selettiva,na.rm=TRUE)))
