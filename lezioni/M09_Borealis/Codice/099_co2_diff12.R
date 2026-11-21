delta12 <- diff(y, lag = 12)
plot(delta12,
     ylab = "Differenza rispetto a 12 mesi (ppm)")
length(delta12) # 192 valori
acf(as.numeric(delta12), lag.max = 24)
