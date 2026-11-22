acf_res <- acf(res,lag.max=36,
               plot=FALSE)
acf_res$acf[c(2,13,25)]
