# Isocrona (M19): generatore dei file di dati sintetici per la datazione radiometrica.
# isocrone_v1.csv: rapporti 87Rb/86Sr e 87Sr/86Sr di un granito (sistema chiuso) e di un filone con dispersione del
#   rapporto iniziale; incertezze analitiche dichiarate (1 sigma), correlazione degli errori posta a zero.
# date_v1.csv: date U-Pb di singoli zirconi del granito, con un granulo ereditato.
# Costante di decadimento di 87Rb: 1,3972e-11 per anno (raccomandazione IUPAC-IUGS, Villa e colleghi, 2015).
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
set.seed(20261130)
lambda <- 1.3972e-11
isocrona <- function(suite, t, r0, x, sx_rel, sy_rel, geo = 0) {
  m <- exp(lambda * t) - 1
  y <- r0 + rnorm(length(x), 0, geo) + m * x
  sx <- sx_rel * x; sy <- sy_rel * y
  data.frame(suite = suite, x = x + rnorm(length(x), 0, sx), sx = sx, y = y + rnorm(length(x), 0, sy), sy = sy)
}
g <- isocrona('granito', 300e6, 0.7085, c(0.15, 0.42, 0.95, 1.6, 2.4, 3.3, 4.6, 6.1, 8.0, 11.5), .01, 1.5e-5)
f <- isocrona('filone', 250e6, 0.7062, c(0.35, 0.8, 1.4, 2.1, 2.9, 3.8, 5.0, 6.6), .01, 1.5e-5, geo = 1.2e-4)
d <- rbind(g, f)
d <- data.frame(campione = c(sprintf('G%02d', 1:10), sprintf('F%02d', 1:8)), suite = d$suite,
                Rb87Sr86 = signif(d$x, 5), sRb = signif(d$sx, 3), Sr87Sr86 = round(d$y, 6), sSr = round(d$sy, 6), rho = 0)
write.csv(d, 'dati/isocrone_v1.csv', row.names = FALSE)
# Date U-Pb di quindici zirconi: quattordici cristallizzati a 300 Ma, uno ereditato a 318 Ma.
s <- round(runif(15, .8, 2.0), 2)
t <- c(rep(300, 14), 318) + rnorm(15, 0, s)
z <- data.frame(zircone = sprintf('Z%02d', 1:15), data_Ma = round(t, 2), s_Ma = s)
write.csv(z, 'dati/date_v1.csv', row.names = FALSE)
print(d); print(z)
