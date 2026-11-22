# Nucleo numerico originale dal registro degli esperimenti.
x <- ar_series(120, p$rho)

n <- length(x)

L <- p$length

individual <- replicate(p$B, mean(sample(x, replace = TRUE)))

blocks <- replicate(p$B, {
    start <- sample(1:n, ceiling(n/L), replace = TRUE)
    indices <- unlist(lapply(start, function(s) ((s - 1 + 0:(L - 1))%%n) + 1))
    mean(x[indices[1:n]])
})

data <- data.frame(media = c(individual, blocks), metodo = rep(c("Singole osservazioni", 
    "Blocchi circolari"), each = p$B))

plots <- list(ggplot(data, aes(media, colour = metodo)) + geom_density(linewidth = 1.1) + 
    scale_colour_manual(values = col_geo) + labs(title = "Ricampionamento della stessa serie", 
    x = "Media bootstrap", y = "Densità"))

metrics <- metric(`SE osservazioni` = f(sd(individual)), `SE blocchi` = f(sd(blocks)), `Lunghezza del blocco` = L, 
    `Osservazioni originali` = n)
