# Nucleo numerico originale dal registro degli esperimenti.
data <- data.frame(stazione = rep(c("A", "B", "C"), c(10, 10, p$nHigh)), valore = c(rnorm(10, 
    5), rnorm(10, 6), rnorm(p$nHigh, 12)))

a <- aggregate(valore ~ stazione, data, mean)

plots <- list(ggplot(data, aes(stazione, valore, fill = stazione)) + geom_boxplot() + scale_fill_manual(values = col_geo) + 
    labs(title = "Pesi delle unità campionarie", x = "Stazione", y = "Concentrazione"))

metrics <- metric(`Media misure` = f(mean(data$valore)), `Media stazioni` = f(mean(a$valore)))
