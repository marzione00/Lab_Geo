# Credentia (M21): copertina procedurale, 2400 x 1500 pixel. Fondale stellare, pianeta con bande di colore e
# le densità a priori e a posteriori del tasso eruttivo del caso. Nessuna immagine esterna.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
suppressPackageStartupMessages(library(ggplot2))
set.seed(4504)
stelle <- data.frame(x = runif(900, 0, 2.56), y = runif(900, 0, 1.6), s = rexp(900, 9), a = runif(900, .25, .9))
th <- seq(0, 2 * pi, length.out = 400)
g2 <- expand.grid(u = seq(-1, 1, length.out = 700), v = seq(-1, 1, length.out = 700))
g2 <- g2[g2$u^2 + g2$v^2 < 1, ]
w <- sqrt(1 - g2$u^2 - g2$v^2)
luce <- c(.55, .35, .76) / sqrt(sum(c(.55, .35, .76)^2))
lam <- pmax(0, g2$u * luce[1] + g2$v * luce[2] + w * luce[3])
fasce <- colorRampPalette(c('#2e2233', '#5a4050', '#9a6b7a', '#c49a8f', '#d9c2b0', '#b48896', '#9a6b7a', '#4a3442', '#2e2233'))(256)
lat <- asin(g2$v) + .07 * sin(7 * asin(g2$v) + 5 * g2$u)
rgbc <- col2rgb(fasce[pmin(256, pmax(1, round((lat / pi + .5) * 255) + 1))]) / 255
g2$fill <- rgb(t(rgbc) * (.16 + .84 * lam))
g2$x <- 2.08 + .80 * g2$u; g2$y <- .55 + .80 * g2$v
# Riquadro delle densità: gamma a priori (tratteggio) e a posteriori del tasso eruttivo, 0-8 eruzioni per secolo.
bx <- c(1.10, 1.98); by <- c(.18, .98)
xx <- seq(0, 8, length.out = 300); d1 <- dgamma(xx, 5.147, 1.807); d2 <- dgamma(xx, 14.147, 5.557); sc <- .66 / max(d2)
curve <- rbind(data.frame(x = bx[1] + .06 + xx / 8 * .76, y = by[1] + .06 + sc * d1, f = 'a'),
               data.frame(x = bx[1] + .06 + xx / 8 * .76, y = by[1] + .06 + sc * d2, f = 'b'))
p <- ggplot() +
  geom_point(data = stelle, aes(x, y, size = s, alpha = a), colour = 'white', shape = 16) +
  geom_tile(data = g2, aes(x, y), fill = g2$fill, width = .80 * 2 / 699 + 1e-4, height = .80 * 2 / 699 + 1e-4) +
  geom_polygon(data = data.frame(x = 2.08 + .806 * cos(th), y = .55 + .806 * sin(th)), aes(x, y), fill = NA, colour = '#e0b0c0', linewidth = 2.2, alpha = .35) +
  annotate('rect', xmin = bx[1], xmax = bx[2], ymin = by[1], ymax = by[2], fill = '#112236', alpha = .6, colour = '#72D8C8', linewidth = 1.1) +
  geom_line(data = curve, aes(x, y, linetype = f), colour = '#ABB5FF', linewidth = 2) + scale_linetype_manual(values = c(a = 2, b = 1), guide = 'none') +
  scale_size_continuous(range = c(.15, 1.6), guide = 'none') + scale_alpha_identity() +
  coord_equal(xlim = c(0, 2.56), ylim = c(0, 1.6), expand = FALSE) + theme_void() +
  theme(plot.background = element_rect(fill = '#112236', colour = NA), panel.background = element_rect(fill = '#112236', colour = NA))
dir.create('Scena', showWarnings = FALSE)
png('Scena/copertina.png', width = 2400, height = 1500, type = 'cairo', bg = '#112236')
print(p); invisible(dev.off())
