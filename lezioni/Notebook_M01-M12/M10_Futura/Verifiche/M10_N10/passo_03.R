scarto <- f$diametro_int_um-(f$diametro_tot_um-2*f$spessore_um)
data.frame(n=nrow(f),massimo_scarto_geometrico=max(abs(scarto)))
stile_grafico()
plot(f$diametro_tot_um,f$diametro_int_um,pch=19,col=palette_geo[1],
  xlab="Diametro totale (micrometri)",ylab="Diametro interno (micrometri)",
  main="Misure sintetiche geometricamente legate")
abline(0,1,lty=2)
