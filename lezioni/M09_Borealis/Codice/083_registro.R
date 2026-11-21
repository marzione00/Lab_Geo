registro83 <- data.frame(
  serie = c("livelli", "diff1", "diff12", "combinata"),
  n = sapply(forme76, length),
  prima_data = as.character(d$data[c(1,2,13,14)]),
  ultima_data = as.character(tail(d$data, 1)))
registro83
