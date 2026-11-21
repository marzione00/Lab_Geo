# Due ACF teoriche con lo stesso primo lag.
lag81 <- 0:8
acf_diff81 <- c(1, -0.5, rep(0, 7))
acf_ar81 <- (-0.5)^lag81
data.frame(lag = lag81,
  rumore_differenziato = acf_diff81,
  ar_negativo = acf_ar81)
