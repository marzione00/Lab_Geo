stile_grafico()
acf(res,lag.max=36,main="ACF dei residui del train")
lb <- Box.test(res,lag=24,type="Ljung-Box",fitdf=2)
data.frame(statistica=as.numeric(lb$statistic),df=as.numeric(lb$parameter),
           p_value=lb$p.value,lag=24,fitdf=2)
