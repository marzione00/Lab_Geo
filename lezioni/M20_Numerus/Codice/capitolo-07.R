s <- read.csv('dati/conteggi_v1.csv')
s$p <- s$feldspato / s$punti
m <- lm(p ~ distanza_km, data = s)
x <- c(0, 60, 90)
nd <- data.frame(distanza_km = x)
round(predict(m, nd), 3)
