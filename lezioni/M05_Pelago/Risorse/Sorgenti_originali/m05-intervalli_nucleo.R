# Nucleo numerico originale dal registro degli esperimenti.
z <- t(replicate(p$B, {
    u <- rnorm(1)
    x <- 10 + sqrt(p$rho) * u + sqrt(1 - p$rho) * rnorm(p$n)
    c(mean(x), sd(x)/sqrt(p$n))
}))

q <- qt((1 + p$level)/2, p$n - 1)

data <- data.frame(replica = 1:p$B, media = z[, 1], inferiore = z[, 1] - q * z[, 2], superiore = z[, 
    1] + q * z[, 2])

data$copre <- data$inferiore <= 10 & data$superiore >= 10

shown <- head(data, 80)

plots <- list(ggplot(shown, aes(media, replica, colour = copre)) + geom_segment(aes(x = inferiore, 
    xend = superiore, yend = replica), linewidth = 0.7) + geom_point(size = 1.5) + geom_vline(xintercept = 10, 
    linetype = 2) + scale_colour_manual(values = c(`FALSE` = col_geo[2], `TRUE` = col_geo[1]), 
    labels = c("Non include μ", "Include μ")) + labs(title = "Intervalli: prime 80 repliche", 
    x = "Media e intervallo", y = "Replica"))

metrics <- metric(`Copertura osservata` = f(mean(data$copre)), `Livello nominale` = p$level, 
    Repliche = p$B, `MC SE copertura` = f(sqrt(mean(data$copre) * (1 - mean(data$copre))/p$B)))
