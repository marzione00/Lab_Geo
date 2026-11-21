set.seed(19058)
# arima.sim gestisce il tratto iniziale.
a58 <- arima.sim(
  model = list(ar = 0.65), n = 300)
plot(a58, ylab = "Valore",
     main = "AR(1), phi = 0.65")
acf(a58, lag.max = 24)
