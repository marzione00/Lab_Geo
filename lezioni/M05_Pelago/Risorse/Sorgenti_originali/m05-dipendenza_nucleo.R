# Nucleo numerico originale dal registro degli esperimenti.
means <- replicate(p$B, {
    u <- rnorm(1)
    mean(sqrt(p$rho) * u + sqrt(1 - p$rho) * rnorm(p$n))
})

actual <- sqrt((1 + (p$n - 1) * p$rho)/p$n)

data <- data.frame(media = means)

plots <- list(hist_plot(means, "Medie di campioni correlati", "Media") + geom_vline(xintercept = c(-1.96, 
    1.96)/sqrt(p$n), linetype = 2, colour = col_geo[2]))

metrics <- metric(`SE assumendo indipendenza` = f(1/sqrt(p$n)), `SE corretto teorico` = f(actual), 
    `SD delle repliche` = f(sd(means)), `n effettivo` = f(p$n/(1 + (p$n - 1) * p$rho)))
