# Isocrona (M19): copertina procedurale, 2400 x 1500 pixel. Fondale stellare, pianeta con bande di colore e
# l'isocrona del granito del caso. Nessuna immagine esterna.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
suppressPackageStartupMessages(library(ggplot2))
set.seed(4503)
d <- read.csv('dati/isocrone_v1.csv'); g <- d[d$suite == 'granito', ]
stelle <- data.frame(x = runif(900, 0, 2.56), y = runif(900, 0, 1.6), s = rexp(900, 9), a = runif(900, .25, .9))
th <- seq(0, 2 * pi, length.out = 400)
g2 <- expand.grid(u = seq(-1, 1, length.out = 700), v = seq(-1, 1, length.out = 700))
g2 <- g2[g2$u^2 + g2$v^2 < 1, ]
w <- sqrt(1 - g2$u^2 - g2$v^2)
luce <- c(.55, .35, .76) / sqrt(sum(c(.55, .35, .76)^2))
lam <- pmax(0, g2$u * luce[1] + g2$v * luce[2] + w * luce[3])
fasce <- colorRampPalette(c('#2a2330', '#5a3f45', '#8a6a5c', '#c79a72', '#d9b98c', '#b07a62', '#8a6a5c', '#4a3438', '#2a2330'))(256)
lat <- asin(g2$v) + .07 * sin(7 * asin(g2$v) + 5 * g2$u)
rgbc <- col2rgb(fasce[pmin(256, pmax(1, round((lat / pi + .5) * 255) + 1))]) / 255
g2$fill <- rgb(t(rgbc) * (.16 + .84 * lam))
g2$x <- 2.08 + .80 * g2$u; g2$y <- .55 + .80 * g2$v
# Riquadro dell'isocrona: assi normalizzati sul campo dei dati.
bx <- c(1.10, 1.98); by <- c(.18, .98)
px <- bx[1] + .06 + .76 * (g$Rb87Sr86 - 0) / 12
py <- by[1] + .06 + .68 * (g$Sr87Sr86 - .706) / (.760 - .706)
lx <- bx[1] + .06 + .76 * c(0, 12) / 12; ly <- by[1] + .06 + .68 * (.708506 + .0042158 * c(0, 12) - .706) / (.760 - .706)
p <- ggplot() +
  geom_point(data = stelle, aes(x, y, size = s, alpha = a), colour = 'white', shape = 16) +
  geom_tile(data = g2, aes(x, y), fill = g2$fill, width = .80 * 2 / 699 + 1e-4, height = .80 * 2 / 699 + 1e-4) +
  geom_polygon(data = data.frame(x = 2.08 + .806 * cos(th), y = .55 + .806 * sin(th)), aes(x, y), fill = NA, colour = '#e3a98a', linewidth = 2.2, alpha = .35) +
  annotate('rect', xmin = bx[1], xmax = bx[2], ymin = by[1], ymax = by[2], fill = '#112236', alpha = .6, colour = '#72D8C8', linewidth = 1.1) +
  annotate('segment', x = lx[1], xend = lx[2], y = ly[1], yend = ly[2], colour = '#72D8C8', linewidth = 1.3) +
  geom_point(data = data.frame(x = px, y = py), aes(x, y), colour = '#ABB5FF', size = 5) +
  scale_size_continuous(range = c(.15, 1.6), guide = 'none') + scale_alpha_identity() +
  coord_equal(xlim = c(0, 2.56), ylim = c(0, 1.6), expand = FALSE) + theme_void() +
  theme(plot.background = element_rect(fill = '#112236', colour = NA), panel.background = element_rect(fill = '#112236', colour = NA))
dir.create('Scena', showWarnings = FALSE)
png('Scena/copertina.png', width = 2400, height = 1500, type = 'cairo', bg = '#112236')
print(p); invisible(dev.off())
