stile_grafico(); acf(rx,lag.max=20,main="VAR: ACF residui equazione X")
stile_grafico(); acf(ry,lag.max=20,main="VAR: ACF residui equazione Y")
data.frame(equazione=c("X","Y"),n=c(length(rx),length(ry)),
           media=c(mean(rx),mean(ry)),sd=c(sd(rx),sd(ry)))
