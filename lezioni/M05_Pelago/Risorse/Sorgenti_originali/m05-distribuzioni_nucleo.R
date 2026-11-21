# Nucleo numerico originale dal registro degli esperimenti.
means <- replicate(p$B, mean(if (p$population == "normal") rnorm(p$n, 1, 1) else rexp(p$n)))

data <- data.frame(media = means)

plots <- list(hist_plot(means, "Distribuzione delle medie", "Media campionaria") + geom_vline(xintercept = 1, 
    linetype = 2))

metrics <- metric(`Media delle medie` = f(mean(means)), `SD empirica` = f(sd(means)), `SE teorico` = f(1/sqrt(p$n)))
