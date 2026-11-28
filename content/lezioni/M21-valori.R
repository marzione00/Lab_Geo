# Valori citati nelle spiegazioni estese di Credentia (M21). Uso: Rscript content/lezioni/M21-valori.R dalla radice.
# Figure e controlli numerici sono in lezioni/M21_Credentia/R/M21_figure.R; i valori dei laboratori sono in
# lezioni/M21_Credentia/Esperimenti/*.json. Tassi in eruzioni per secolo.
e <- read.csv('lezioni/M21_Credentia/dati/eruzioni_v1.csv'); a <- read.csv('lezioni/M21_Credentia/dati/analoghi_v1.csv')
n <- nrow(e); T <- 3.75; A <- 5.146730; B <- 1.807466; A1 <- A + n; B1 <- B + T
# Tappa 4: intervallo di Wald per confronto.
cat('Wald:', round(n / T + c(-1.96, 1.96) * sqrt(n) / T, 2), '\n')
# Tappa 5: probabilità marginale del registro con la distribuzione a priori dei vulcani analoghi.
cat('p(N = 9):', round(dnbinom(n, size = A, mu = A / B * T), 4), '\n')
# Tappa 6: mediana e moda a posteriori con distribuzione a priori uniforme; passo della griglia.
cat('Uniforme: mediana', round(qgamma(.5, n + 1, T), 3), ' moda', n / T, ' passo griglia', 10 / 4000, '\n')
# Tappa 7: media a posteriori come media pesata.
w <- B / B1; cat('Peso', round(w, 3), ' media pesata', round(w * A / B + (1 - w) * n / T, 3), ' dev. std. a priori', round(sqrt(A) / B, 3),
                ' a posteriori', round(sqrt(A1) / B1, 3), '\n')
# Tappa 11: intervallo di massima densità a posteriori.
hpd <- function(a, b, lev = .95) { f <- function(l) qgamma(l + lev, a, b) - qgamma(l, a, b); l <- optimize(f, c(0, 1 - lev), tol = 1e-10)$minimum; qgamma(c(l, l + lev), a, b) }
cat('HPD', round(hpd(A1, B1), 3), ' ampiezze', round(diff(hpd(A1, B1)), 3), round(diff(qgamma(c(.025, .975), A1, B1)), 3), '\n')
# Tappa 12: tassi dei vulcani analoghi e loro dispersione.
r <- a$eruzioni / a$anni_osservati * 100
cat('Tassi analoghi: media', round(mean(r), 2), ' dev. std.', round(sd(r), 2), ' eruzioni totali', sum(a$eruzioni), ' secoli totali', sum(a$anni_osservati) / 100, '\n')
# Tappa 14: numero atteso di eruzioni in mezzo secolo e probabilità di tre o più.
cat('Media in 50 anni: predittiva', round(A1 / B1 * .5, 3), ' Poisson', n / T * .5,
    '  P(>=3):', round(1 - pnbinom(2, size = A1, mu = A1 / B1 * .5), 3), round(1 - ppois(2, n / T * .5), 3), '\n')
# Tappa 17: frazione esplosiva dei vulcani analoghi.
cat('Esplosive analoghi:', sum(a$esplosive), 'su', sum(a$eruzioni), ' frazione', round(sum(a$esplosive) / sum(a$eruzioni), 3), '\n')
# Tappa 20: probabilità a priori di un tasso inferiore a 4 con la distribuzione dei vulcani di altro tipo.
cat('Altro tipo: P(lambda < 4) a priori', round(pgamma(4, 10, 1), 4), ' media predittiva a priori', 10 * T, '\n')
# Tappa 24: funzione di rischio della Weibull con le stime di massima verosimiglianza, a 10 e a 40 anni.
k <- 3.957250; eta <- 44.56997
hz <- function(t) k / eta * (t / eta)^(k - 1)
cat('Rischio per anno a 10 e 40 anni:', signif(hz(10), 3), signif(hz(40), 3), ' esponenziale', round(1 / mean(diff(e$anno)), 4), '\n')
# Tappa 28: probabilità condizionata vera con i parametri del generatore.
kv <- 1.8; sv <- 42 / gamma(1 + 1 / kv)
cat('Probabilità condizionata vera:', round(1 - exp((37 / sv)^kv - (87 / sv)^kv), 3), ' scala vera', round(sv, 1), '\n')
