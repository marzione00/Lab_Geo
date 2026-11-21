Zzero <- Zm
Zzero[is.na(Zzero)] <- 0
c(completa=mean(Z),
 disponibile=mean(Zm,na.rm=TRUE),
 sostituita=mean(Zzero))
