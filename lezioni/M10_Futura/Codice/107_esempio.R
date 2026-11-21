tab <- data.frame(
  data=co2$data[169:204],
  osservato=as.numeric(test), fc)
stopifnot(!anyDuplicated(tab$data))
names(tab)
