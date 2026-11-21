deltaC <- diff(diff(y, lag = 12))
alternativaC <- diff(diff(y), lag = 12)
stopifnot(max(abs(deltaC - alternativaC)) < 1e-10)
length(deltaC) # 191 valori
plot(deltaC, ylab = "Differenza combinata (ppm)")
