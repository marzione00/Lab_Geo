p <- carica_dati("processi_simulati.csv")
v <- p[1:250,c("x_VAR","y_VAR")]
lagged <- data.frame(x=v$x_VAR[-1],y=v$y_VAR[-1],
  x_lag=head(v$x_VAR,-1),y_lag=head(v$y_VAR,-1))
head(lagged,4)
stopifnot(nrow(lagged)==249L,lagged$x_lag[1]==v$x_VAR[1],lagged$x[1]==v$x_VAR[2])
