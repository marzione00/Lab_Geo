# Nucleo numerico originale dal registro degli esperimenti.
x <- rlnorm(30, 0, 0.6)

q <- replicate(30, quantile(replicate(p$B, mean(sample(x, replace = TRUE))), 0.975))

data <- data.frame(x = 1:30, y = q)

plots <- list(point_plot(data, title = "Ripetizioni del calcolo bootstrap", xl = "Ripetizione del calcolo", 
    yl = "Limite superiore 97,5%"))

metrics <- metric(`Repliche per calcolo` = p$B, `SD dei limiti superiori` = f(sd(q)), `Campione fisso: n` = 30)
