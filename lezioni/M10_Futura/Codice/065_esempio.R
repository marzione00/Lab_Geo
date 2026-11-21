lb <- Box.test(res, lag=24,
  type="Ljung-Box", fitdf=2)
c(Q=unname(lb$statistic),
  df=unname(lb$parameter),
  p=lb$p.value)
