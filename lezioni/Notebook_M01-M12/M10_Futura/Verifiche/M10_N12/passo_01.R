f <- carica_dati("fossili_simulati.csv"); s <- prepara_fossili(f)
tr <- s$train; te <- s$test
mod <- lm(diametro_int_um~diametro_tot_um,data=tr)
prev <- as.numeric(predict(mod,newdata=te))
stile_grafico()
lim <- range(prev,te$diametro_int_um)
plot(prev,te$diametro_int_um,pch=19,col=palette_geo[1],xlim=lim,ylim=lim,asp=1,
  xlab="Previsto nel test (micrometri)",ylab="Osservato nel test (micrometri)",
  main="32 individui esclusi dalla stima")
abline(0,1,lty=2)
