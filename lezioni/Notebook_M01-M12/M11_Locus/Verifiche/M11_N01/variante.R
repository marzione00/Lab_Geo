copia <- rbind(d,d[1,])
duplicati <- duplicated(copia$id)|duplicated(copia$id,fromLast=TRUE)
copia[duplicati,c("id","x_m","y_m")]
data.frame(righe=nrow(copia),id_distinti=length(unique(copia$id)),occorrenze_coinvolte=sum(duplicati))
stopifnot(sum(duplicati)==2L,nrow(d)==64L)
