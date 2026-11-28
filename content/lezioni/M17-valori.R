# Valori citati nelle spiegazioni estese di Simplex (M17). Uso: Rscript content/lezioni/M17-valori.R dalla radice.
# Le figure, i bilanci, il biplot e i controlli numerici sono in lezioni/M17_Simplex/R/M17_figure.R; i valori dei
# laboratori sono in lezioni/M17_Simplex/Esperimenti/*.json.
d <- read.csv('lezioni/M17_Simplex/dati/composizioni_v1.csv')
parti <- c('SiO2', 'Al2O3', 'CaO', 'MgO', 'FeO', 'Altro')
X <- as.matrix(d[parti]); lit <- d$litologia
cat('Campioni:', nrow(X), ' stazioni:', length(unique(d$stazione)), '\n')
cat('Correlazione SiO2-CaO, tutti:', round(cor(X[, 'SiO2'], X[, 'CaO']), 2), '\n')
for (k in c('Arenaria', 'Basalto', 'Calcare'))
  cat('  ', k, round(cor(X[lit == k, 'SiO2'], X[lit == k, 'CaO']), 2), '\n')
# Tappa 4: basalto riferito ai cinque ossidi.
x <- c(46.7, 13.4, 10.4, 8.2, 13.4, 6.0); s <- 100 * x[1:5] / sum(x[1:5])
cat('Somma dei cinque ossidi:', sum(x[1:5]), ' SiO2 e CaO riferiti:', round(s[c(1, 3)], 1), '\n')
# Tappa 12: media geometrica del basalto.
cat('Media geometrica:', round(exp(mean(log(x))), 2), '\n')
# Tappa 6: identità di Chayes sui campioni completi.
z <- rowSums(X == 0) > 0; C <- cov(100 * X[!z, ] / rowSums(X[!z, ]))
cat('var(SiO2):', round(C[1, 1]), ' somma delle altre covarianze:', round(sum(C[1, -1])), '\n')
# Tappa 15: rapporto fra le due distanze di Aitchison.
clr <- function(v) log(v) - mean(log(v))
ait <- function(p, q) sqrt(sum((clr(p) - clr(q))^2))
a1 <- c(50, 20, 15, .1, 9.9, 5); a2 <- a1; a2[c(1, 4)] <- c(49.9, .2)
c1 <- c(50, 20, 15, 5, 5, 5); c2 <- c1; c2[1:2] <- c(50.1, 19.9)
cat('Rapporto fra le distanze di Aitchison:', round(ait(a1, a2) / ait(c1, c2)), '\n')
# Tappa 24: valori fissati e negativi nel file di Prisma.
m <- read.csv('materiali/dati/ml_v3.csv')
cat('ml_v3: SiO2 negativi', sum(m$SiO2 < 0), ' valori fissati a 0,05', sum(as.matrix(m[c('CaO', 'MgO', 'FeO')]) == 0.05), '\n')
