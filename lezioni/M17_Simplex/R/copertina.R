# Simplex (M17): copertina procedurale, 2400 x 1500 pixel. Fondale stellare, pianeta con bande di colore e il
# simplesso a tre parti con le composizioni del caso. Nessuna immagine esterna.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
suppressPackageStartupMessages(library(ggplot2))
set.seed(4501)
d <- read.csv('dati/composizioni_v1.csv')
x <- as.matrix(d[c('SiO2', 'CaO')]); x <- cbind(x, mf = pmax(d$MgO + d$FeO, .065))
x <- x / rowSums(x)
tri <- function(a, b, c) data.frame(x = b + c / 2, y = c * sqrt(3) / 2)
pt <- tri(x[, 1], x[, 2], x[, 3]); pt$x <- 1.12 + pt$x * .95; pt$y <- .16 + pt$y * .95
stelle <- data.frame(x = runif(900, 0, 2.56), y = runif(900, 0, 1.6), s = rexp(900, 9), a = runif(900, .25, .9))
th <- seq(0, 2 * pi, length.out = 400)
# Pianeta come griglia di pixel: fasce di colore in latitudine e illuminazione lambertiana da destra in alto.
g <- expand.grid(u = seq(-1, 1, length.out = 700), v = seq(-1, 1, length.out = 700))
g <- g[g$u^2 + g$v^2 < 1, ]
w <- sqrt(1 - g$u^2 - g$v^2)
luce <- c(.55, .35, .76) / sqrt(sum(c(.55, .35, .76)^2))
lam <- pmax(0, g$u * luce[1] + g$v * luce[2] + w * luce[3])
fasce <- colorRampPalette(c('#2b2846', '#6f5f93', '#8c7aa8', '#c9bf9c', '#d9cfa8', '#a493bd', '#8c7aa8', '#4a3f6b', '#2b2846'))(256)
lat <- asin(g$v) + .06 * sin(9 * asin(g$v) + 3 * g$u)
rgbc <- col2rgb(fasce[pmin(256, pmax(1, round((lat / pi + .5) * 255) + 1))]) / 255
k <- .16 + .84 * lam
g$fill <- rgb(t(rgbc) * k)
g$x <- 2.08 + .80 * g$u; g$y <- .55 + .80 * g$v
p <- ggplot() +
  geom_point(data = stelle, aes(x, y, size = s, alpha = a), colour = 'white', shape = 16) +
  geom_tile(data = g, aes(x, y), fill = g$fill, width = .80 * 2 / 699 + 1e-4, height = .80 * 2 / 699 + 1e-4) +
  geom_polygon(data = data.frame(x = 2.08 + .806 * cos(th), y = .55 + .806 * sin(th)), aes(x, y), fill = NA, colour = '#b7a6e8', linewidth = 2.2, alpha = .35) +
  geom_polygon(data = data.frame(x = 1.12 + c(0, .95, .475), y = .16 + c(0, 0, .823)), aes(x, y), fill = '#112236', alpha = .55, colour = '#72D8C8', linewidth = 1.1) +
  geom_point(data = pt, aes(x, y), colour = '#ABB5FF', size = 2.6, alpha = .8) +
  scale_size_continuous(range = c(.15, 1.6), guide = 'none') + scale_alpha_identity() +
  coord_equal(xlim = c(0, 2.56), ylim = c(0, 1.6), expand = FALSE) + theme_void() +
  theme(plot.background = element_rect(fill = '#112236', colour = NA), panel.background = element_rect(fill = '#112236', colour = NA))
dir.create('Scena', showWarnings = FALSE)
png('Scena/copertina.png', width = 2400, height = 1500, type = 'cairo', bg = '#112236')
print(p); invisible(dev.off())
