d <- carica_dati("raster_v3.csv")
audit_raster(d)
d <- d[order(d$riga,d$colonna),]
Z <- matrice_quote(d)
richiedi_terra()
r <- terra::rast(percorso_dati("raster_v3.tif"))
 g <- gradienti_centrali(Z);s <- g$gradi
 risultato <- data.frame(x_m=rep((1:28)*30,22),y_m=rep((1:22)*30,each=28),
   pendenza_gradi=as.vector(t(s)))
 file_csv <- percorso_risultati("pendenze.csv")
 write.csv(risultato,file_csv,row.names=FALSE)
 csv_letto <- read.csv(file_csv)
 data.frame(celle=nrow(csv_letto),minimo=min(csv_letto$pendenza_gradi),
   massimo=max(csv_letto$pendenza_gradi),errore_roundtrip=max(abs(csv_letto$pendenza_gradi-risultato$pendenza_gradi)))
 stopifnot(nrow(csv_letto)==616L,all(is.finite(csv_letto$pendenza_gradi)),
   max(abs(csv_letto$pendenza_gradi-risultato$pendenza_gradi))<1e-10)
