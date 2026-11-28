# Numerus (M20): copertina procedurale, 2400 x 1500 pixel. Fondale stellare, pianeta con bande di colore e
# le frequenze dei conteggi di frane del caso. Nessuna immagine esterna.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
suppressPackageStartupMessages(library(ggplot2))
set.seed(4504)
d <- read.csv('dati/frane_v1.csv'); fq <- tabulate(pmin(d$frane, 12) + 1, 13)
stelle <- data.frame(x = runif(900, 0, 2.56), y = runif(900, 0, 1.6), s = rexp(900, 9), a = runif(900, .25, .9))
th <- seq(0, 2 * pi, length.out = 400)
g2 <- expand.grid(u = seq(-1, 1, length.out = 700), v = seq(-1, 1, length.out = 700))
g2 <- g2[g2$u^2 + g2$v^2 < 1, ]
w <- sqrt(1 - g2$u^2 - g2$v^2)
luce <- c(.55, .35, .76) / sqrt(sum(c(.55, .35, .76)^2))
lam <- pmax(0, g2$u * luce[1] + g2$v * luce[2] + w * luce[3])
fasce <- colorRampPalette(c('#2c3a2a', '#4f6140', '#7a8a5a', '#a9a878', '#c9b48a', '#93a874', '#7a8a5a', '#3d4c33', '#2c3a2a'))(256)
lat <- asin(g2$v) + .07 * sin(7 * asin(g2$v) + 5 * g2$u)
rgbc <- col2rgb(fasce[pmin(256, pmax(1, round((lat / pi + .5) * 255) + 1))]) / 255
g2$fill <- rgb(t(rgbc) * (.16 + .84 * lam))
g2$x <- 2.08 + .80 * g2$u; g2$y <- .55 + .80 * g2$v
# Riquadro delle frequenze: barre proporzionali al numero di celle con 0, 1, ..., 12 o più frane.
bx <- c(1.10, 1.98); by <- c(.18, .98)
barre <- data.frame(xmin = bx[1] + .06 + (0:12) * .058, ymin = by[1] + .06)
barre$xmax <- barre$xmin + .046; barre$ymax <- barre$ymin + .66 * fq / max(fq)
p <- ggplot() +
  geom_point(data = stelle, aes(x, y, size = s, alpha = a), colour = 'white', shape = 16) +
  geom_tile(data = g2, aes(x, y), fill = g2$fill, width = .80 * 2 / 699 + 1e-4, height = .80 * 2 / 699 + 1e-4) +
  geom_polygon(data = data.frame(x = 2.08 + .806 * cos(th), y = .55 + .806 * sin(th)), aes(x, y), fill = NA, colour = '#b8d4a0', linewidth = 2.2, alpha = .35) +
  annotate('rect', xmin = bx[1], xmax = bx[2], ymin = by[1], ymax = by[2], fill = '#112236', alpha = .6, colour = '#72D8C8', linewidth = 1.1) +
  geom_rect(data = barre, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), fill = '#ABB5FF', alpha = .85) +
  scale_size_continuous(range = c(.15, 1.6), guide = 'none') + scale_alpha_identity() +
  coord_equal(xlim = c(0, 2.56), ylim = c(0, 1.6), expand = FALSE) + theme_void() +
  theme(plot.background = element_rect(fill = '#112236', colour = NA), panel.background = element_rect(fill = '#112236', colour = NA))
dir.create('Scena', showWarnings = FALSE)
png('Scena/copertina.png', width = 2400, height = 1500, type = 'cairo', bg = '#112236')
print(p); invisible(dev.off())
