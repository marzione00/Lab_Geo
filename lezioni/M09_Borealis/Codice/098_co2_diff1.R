delta1 <- diff(y)
plot(delta1, ylab = "Differenza (ppm)")
acf(as.numeric(delta1), lag.max = 24,
    main = "Differenza mensile")
length(delta1) # 203 valori
