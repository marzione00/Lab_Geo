errata <- (P[2:23,3:30]-P[2:23,1:28])/30
data.frame(gx_corretto=mean(gx),gx_errato=mean(errata),rapporto=mean(errata)/mean(gx))
stopifnot(abs(mean(errata)-.24)<1e-12)
