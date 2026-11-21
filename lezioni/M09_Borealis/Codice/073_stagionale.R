ds73 <- diff(y, lag = 12)
# Il primo valore confronta due gennaio.
data.frame(
  data = tail(d$data, -12),
  variazione_annua = as.numeric(ds73))[1:4, ]
c(start(ds73), end(ds73))
length(ds73)
