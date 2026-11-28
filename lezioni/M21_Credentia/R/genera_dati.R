# Credentia (M21): generatore dei file di dati sintetici per l'inferenza bayesiana.
# eruzioni_v1.csv: anni e tipo delle eruzioni di un vulcano nel registro storico 1650-2025; tempi di riposo da una
#   distribuzione di Weibull con forma 1,8 e media 42 anni, tipo esplosivo con probabilità 0,3.
# analoghi_v1.csv: anni di osservazione, eruzioni ed eruzioni esplosive di quattordici vulcani analoghi; tassi da una
#   gamma di forma 4 e media 0,025 per anno, frazioni esplosive da una beta(3, 7).
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
set.seed(20261212)
k <- 1.8; sc <- 42 / gamma(1 + 1 / k)
t <- 1580; anni <- c()
while (t < 2025) { t <- t + rweibull(1, k, sc); if (t >= 1650 && t < 2025) anni <- c(anni, t) }
anni <- floor(anni)
set.seed(20261213)
tipo <- ifelse(rbinom(length(anni), 1, .3) == 1, 'esplosiva', 'effusiva')
e <- data.frame(eruzione = sprintf('E%d', seq_along(anni)), anno = anni, tipo = tipo)
write.csv(e, 'dati/eruzioni_v1.csv', row.names = FALSE)
lam <- rgamma(14, shape = 4, rate = 160)
oss <- sample(seq(120, 480, 10), 14, TRUE)
n <- rpois(14, lam * oss)
p <- rbeta(14, 3, 7)
a <- data.frame(vulcano = sprintf('A%02d', 1:14), anni_osservati = oss, eruzioni = n, esplosive = rbinom(14, n, p))
write.csv(a, 'dati/analoghi_v1.csv', row.names = FALSE)
print(e); print(a)
cat('Eruzioni:', nrow(e), ' esplosive:', sum(e$tipo == 'esplosiva'), ' riposi:', diff(e$anno), ' dall’ultima:', 2025 - max(e$anno), '\n')
