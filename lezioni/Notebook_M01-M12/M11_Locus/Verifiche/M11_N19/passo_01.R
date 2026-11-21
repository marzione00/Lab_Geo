d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 tr <- d$x_m<1250;te <- !tr
 stopifnot(sum(tr)==40L,sum(te)==24L,!any(tr&te),all(tr|te))
 data.frame(ruolo=c("Train","Test"),n=c(sum(tr),sum(te)),
   minimo_x=c(min(d$x_m[tr]),min(d$x_m[te])),massimo_x=c(max(d$x_m[tr]),max(d$x_m[te])))
 table(area_del_CSV=d$area,ruolo=ifelse(tr,"Train","Test"))
