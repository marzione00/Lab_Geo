# Numerus (M20): generatore dei file di dati sintetici per i modelli lineari generalizzati.
# frane_v1.csv: frane cartografate in 96 celle di un bacino, con area, pendenza media e litologia; conteggi da una
#   binomiale negativa (Poisson con fattore gamma di cella) con logaritmo della media lineare nei predittori.
# conteggi_v1.csv: conteggio per punti del feldspato in 36 sezioni sottili di 12 stazioni lungo un percorso di
#   trasporto; probabilità logistica nella distanza con un effetto casuale di stazione.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
set.seed(20261201)
n <- 96
lit <- sample(rep(c('Argille', 'Flysch', 'Calcari'), c(36, 32, 28)))
pend <- round(pmin(38, pmax(4, rnorm(n, c(Argille = 16, Flysch = 22, Calcari = 27)[lit], 6))), 1)
area <- round(exp(log(1.2) + 0.03 * (pend - 20) + rnorm(n, 0, .45)), 2)
eta <- log(area) - 0.2 + 0.07 * pend + c(Argille = 0, Flysch = -0.4, Calcari = -1.3)[lit]
mu <- exp(eta)
frane <- rnbinom(n, size = 4, mu = mu)
d <- data.frame(cella = sprintf('C%02d', 1:n), area_km2 = area, pendenza = pend, litologia = lit, frane = frane)
write.csv(d, 'dati/frane_v1.csv', row.names = FALSE)
# Conteggio per punti: probabilità del feldspato decrescente con la distanza, variabilità fra stazioni.
staz <- data.frame(stazione = sprintf('S%02d', 1:12), distanza_km = round(seq(2, 60, length.out = 12) + runif(12, -1.5, 1.5), 1))
staz$u <- rnorm(12, 0, .25)
s <- staz[rep(1:12, each = 3), ]
s$sezione <- paste0(s$stazione, letters[1:3])
s$punti <- sample(seq(250, 400, 10), 36, TRUE)
p <- plogis(-0.6 - 0.035 * s$distanza_km + s$u + rnorm(36, 0, .1))
s$feldspato <- rbinom(36, s$punti, p)
write.csv(s[c('sezione', 'stazione', 'distanza_km', 'punti', 'feldspato')], 'dati/conteggi_v1.csv', row.names = FALSE)
cat('Celle:', n, ' frane totali:', sum(frane), ' zeri:', sum(frane == 0), ' media', round(mean(frane), 2), ' varianza', round(var(frane), 2), '\n')
print(table(lit)); print(summary(area)); print(head(s))
