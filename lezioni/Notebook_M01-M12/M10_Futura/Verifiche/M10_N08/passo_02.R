data.frame(dentro=sum(p$dentro95),totale=nrow(p),quota=mean(p$dentro95),
           ampiezza_media=mean(p$superiore-p$inferiore))
p$blocco <- factor(rep(c("1-12 mesi","13-24 mesi","25-36 mesi"),each=12),
                  levels=c("1-12 mesi","13-24 mesi","25-36 mesi"))
do.call(rbind,lapply(split(p,p$blocco),function(d) {
  data.frame(blocco=as.character(d$blocco[1]),n=nrow(d),MAE=mean(abs(d$errore)),
             quota_dentro95=mean(d$dentro95),ampiezza=mean(d$superiore-d$inferiore))
}))
