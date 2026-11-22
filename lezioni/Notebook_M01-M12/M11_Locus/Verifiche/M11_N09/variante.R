elenco <- aggregate(zona~id,relazioni,function(x) paste(sort(unique(x)),collapse="+"))
unico <- merge(d,elenco,by="id")
head(unico[,c("id","zona","concentrazione")],8)
stopifnot(nrow(unico)==64L,!anyDuplicated(unico$id))
