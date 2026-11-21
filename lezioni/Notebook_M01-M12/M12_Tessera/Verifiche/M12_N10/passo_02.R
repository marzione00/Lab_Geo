angoli <- c(0,10,45)
conversione <- data.frame(gradi=angoli,percento=100*tan(angoli*pi/180))
conversione
errore <- max(abs(atan(risultato$percento/100)*180/pi-risultato$gradi))
data.frame(errore_ritorno_gradi=errore)
stopifnot(abs(conversione$percento[3]-100)<1e-10,errore<1e-10)
