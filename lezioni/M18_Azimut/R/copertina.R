# Azimut (M18): copertina procedurale, 2400 x 1500 pixel. Fondale stellare, pianeta con bande di colore e la rosa
# delle paleocorrenti del caso, a settori di uguale area. Nessuna immagine esterna.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
suppressPackageStartupMessages(library(ggplot2))
set.seed(4502)
d <- read.csv('dati/correnti_v1.csv')
fq <- as.vector(table(cut(d$azimut, seq(0, 360, 15), right = FALSE)))
stelle <- data.frame(x = runif(900, 0, 2.56), y = runif(900, 0, 1.6), s = rexp(900, 9), a = runif(900, .25, .9))
th <- seq(0, 2 * pi, length.out = 400)
# Pianeta come griglia di pixel: fasce inclinate e illuminazione lambertiana da destra in alto.
g <- expand.grid(u = seq(-1, 1, length.out = 700), v = seq(-1, 1, length.out = 700))
g <- g[g$u^2 + g$v^2 < 1, ]
w <- sqrt(1 - g$u^2 - g$v^2)
luce <- c(.55, .35, .76) / sqrt(sum(c(.55, .35, .76)^2))
lam <- pmax(0, g$u * luce[1] + g$v * luce[2] + w * luce[3])
fasce <- colorRampPalette(c('#1f3340', '#3f6f7a', '#5f8f9a', '#a9b9a0', '#d8c79a', '#8fb7b8', '#5f8f9a', '#2e5260', '#1f3340'))(256)
lat <- asin(.94 * g$v + .34 * g$u) + .05 * sin(11 * asin(g$v) + 4 * g$u)
rgbc <- col2rgb(fasce[pmin(256, pmax(1, round((lat / pi + .5) * 255) + 1))]) / 255
k <- .16 + .84 * lam
g$fill <- rgb(t(rgbc) * k)
g$x <- 2.08 + .80 * g$u; g$y <- .55 + .80 * g$v
# Rosa a settori: raggio proporzionale alla radice della frequenza, centro in basso a sinistra.
cx <- 1.52; cy <- .58; sc <- .40 / sqrt(max(fq))
settori <- do.call(rbind, lapply(seq_along(fq), function(i) {
  a <- seq((i - 1) * 15, i * 15, length.out = 8) * pi / 180; r <- sc * sqrt(fq[i])
  data.frame(x = c(cx, cx + r * sin(a)), y = c(cy, cy + r * cos(a)), s = i)
}))
anello <- data.frame(x = cx + .44 * cos(th), y = cy + .44 * sin(th))
p <- ggplot() +
  geom_point(data = stelle, aes(x, y, size = s, alpha = a), colour = 'white', shape = 16) +
  geom_tile(data = g, aes(x, y), fill = g$fill, width = .80 * 2 / 699 + 1e-4, height = .80 * 2 / 699 + 1e-4) +
  geom_polygon(data = data.frame(x = 2.08 + .806 * cos(th), y = .55 + .806 * sin(th)), aes(x, y), fill = NA, colour = '#9fd3d8', linewidth = 2.2, alpha = .35) +
  geom_polygon(data = anello, aes(x, y), fill = '#112236', alpha = .55, colour = '#72D8C8', linewidth = 1.1) +
  geom_polygon(data = settori, aes(x, y, group = s), fill = '#ABB5FF', alpha = .8, colour = '#112236', linewidth = .4) +
  annotate('segment', x = cx, xend = cx, y = cy + .44, yend = cy + .49, colour = '#72D8C8', linewidth = 1.1) +
  scale_size_continuous(range = c(.15, 1.6), guide = 'none') + scale_alpha_identity() +
  coord_equal(xlim = c(0, 2.56), ylim = c(0, 1.6), expand = FALSE) + theme_void() +
  theme(plot.background = element_rect(fill = '#112236', colour = NA), panel.background = element_rect(fill = '#112236', colour = NA))
dir.create('Scena', showWarnings = FALSE)
png('Scena/copertina.png', width = 2400, height = 1500, type = 'cairo', bg = '#112236')
print(p); invisible(dev.off())
