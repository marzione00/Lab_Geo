# Nucleo numerico originale dal registro degli esperimenti.
G <- 12

m <- 6

u <- rnorm(G, 0, p$tau)

x <- matrix(10 + rep(u, each = m) + rnorm(G * m), nrow = m)

a <- replicate(p$B, mean(sample(as.vector(x), replace = TRUE)))

b <- replicate(p$B, mean(x[, sample(1:G, replace = TRUE)]))

data <- data.frame(media = c(a, b), metodo = rep(c("Singole misure", "Stazioni intere"), 
    each = p$B))

plots <- list(ggplot(data, aes(media, colour = metodo)) + geom_density(linewidth = 1.1) + 
    scale_colour_manual(values = col_geo) + labs(title = "Struttura del ricampionamento", 
    x = "Media bootstrap", y = "Densità"))

metrics <- metric(`SE singole misure` = f(sd(a)), `SE stazioni` = f(sd(b)), `Unità indipendenti` = G)
