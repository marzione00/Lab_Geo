f <- carica_dati("fossili_simulati.csv")
copia <- rbind(f,f[1,])
data.frame(originale=nrow(f),copia=nrow(copia),duplicati=sum(duplicated(copia$id)))
copia[duplicated(copia$id),]
stopifnot(nrow(f)==160L,nrow(copia)==161L)
