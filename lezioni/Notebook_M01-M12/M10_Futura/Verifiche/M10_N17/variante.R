stopifnot(isTRUE(all.equal(prev,prevedi_var(mod,h))),
  isTRUE(all.equal(as.numeric(prev[2,]),as.numeric(mod$intercetta+mod$A%*%prev[1,]))))
data.frame(controllo=c("Funzione e ciclo coincidono","Secondo passo usa il primo previsto"),esito=TRUE)
