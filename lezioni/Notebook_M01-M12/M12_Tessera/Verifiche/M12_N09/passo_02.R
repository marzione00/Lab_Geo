prova <- gradienti_centrali(P)
data.frame(celle_interne=length(prova$gx),bordo_escluso=length(P)-length(prova$gx),
  errore_gx=max(abs(prova$gx-gx)),errore_gy=max(abs(prova$gy-gy)))
stopifnot(max(abs(prova$gx-gx))<1e-12,max(abs(prova$gy-gy))<1e-12)
