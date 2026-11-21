do.call(rbind,lapply(c(12,24,36),function(L) {
  q <- Box.test(res,lag=L,type="Ljung-Box",fitdf=2)
  data.frame(lag=L,df=as.numeric(q$parameter),p_value=q$p.value)
}))
