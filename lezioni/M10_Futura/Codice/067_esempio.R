acf_quadrati <- acf(res^2,
  lag.max=24, plot=FALSE)
head(as.numeric(acf_quadrati$acf))
