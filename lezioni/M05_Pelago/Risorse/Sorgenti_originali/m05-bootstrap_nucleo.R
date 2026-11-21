# Nucleo numerico originale dal registro degli esperimenti.
x <- rlnorm(p$n, 0, 0.6)

boot <- replicate(p$B, mean(sample(x, replace = TRUE)))

data <- data.frame(replica = seq_along(boot), media = boot)

ci <- quantile(boot, c(0.025, 0.975))

plots <- list(hist_plot(boot, "Distribuzione bootstrap della media", "Media ricampionata") + 
    geom_vline(xintercept = ci, linetype = 2, colour = col_geo[2]))

metrics <- metric(`Media osservata` = f(mean(x)), `SE bootstrap` = f(sd(boot)), `Percentile 2,5%` = f(ci[1]), 
    `Percentile 97,5%` = f(ci[2]))
