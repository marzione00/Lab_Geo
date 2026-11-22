copia <- d;ii <- which(copia$unita=="A")[1:20];copia$quota_m[ii] <- NA_real_
do.call(rbind,lapply(split(copia$quota_m,copia$unita),function(v)
  data.frame(totali=length(v),disponibili=sum(is.finite(v)),copertura=mean(is.finite(v)),
    media_disponibili=mean(v,na.rm=TRUE))))
