# Nucleo numerico originale dal registro degli esperimenti.
a <- rnorm(p$B, 10, 2/sqrt(p$n))

b <- rnorm(p$B, 10 - p$bias, 2/sqrt(p$n))

data <- data.frame(valore = c(a, b), disegno = rep(c("Casuale", "Selezionato"), each = p$B))

plots <- list(ggplot(data, aes(valore, fill = disegno)) + geom_histogram(bins = 25, alpha = 0.6, 
    position = "identity") + scale_fill_manual(values = col_geo) + geom_vline(xintercept = 10, 
    linetype = 2) + labs(title = "Medie in campagne ripetute", x = "Stima", y = "Repliche"))

metrics <- metric(`Bias teorico selezionato` = -p$bias, `SD teorica` = f(2/sqrt(p$n)), `MSE selezionato` = f(mean((b - 
    10)^2)))
