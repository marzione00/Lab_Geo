# Valori citati nelle spiegazioni estese di Azimut (M18). Uso: Rscript content/lezioni/M18-valori.R dalla radice.
# Figure e controlli numerici sono in lezioni/M18_Azimut/R/M18_figure.R; i valori dei laboratori sono in
# lezioni/M18_Azimut/Esperimenti/*.json.
dir <- 'lezioni/M18_Azimut/dati/'
gr <- pi / 180
Rb <- function(a) sqrt(mean(cos(a))^2 + mean(sin(a))^2)
dirm <- function(a) (atan2(mean(sin(a)), mean(cos(a))) / gr) %% 360
d <- read.csv(paste0(dir, 'correnti_v1.csv'))
# Tappa 4: due gruppi di valori ai due estremi della scala.
alto <- d$azimut >= 180
cat('Misure >= 180:', sum(alto), ' media', round(mean(d$azimut[alto]), 1), ' misure < 180:', sum(!alto), ' media',
    round(mean(d$azimut[!alto]), 1), '\n')
# Tappa 6: classe modale con due origini delle classi di 15 gradi.
for (o in c(0, 7.5)) {
  cl <- cut((d$azimut - o) %% 360, seq(0, 360, 15), right = FALSE)
  k <- which.max(table(cl)); cat('Origine', o, ': classe modale da', (15 * (k - 1) + o) %% 360, 'gradi, n =', max(table(cl)), '\n')
}
# Tappa 7: deviazione standard degli scarti dalla direzione media e deviazione standard circolare in S1.
a <- d$azimut[d$stazione == 'S1'] * gr; sc <- ((a / gr - dirm(a) + 180) %% 360) - 180
cat('S1: sd degli scarti', round(sd(sc), 1), ' sd circolare', round(sqrt(-2 * log(Rb(a))) / gr, 1), '\n')
# Tappa 10: concentrazione 8.
A1 <- function(k) besselI(k, 1) / besselI(k, 0)
cat('kappa 8: A1 =', round(A1(8), 3), ' 1/sqrt(kappa) in gradi', round(1 / sqrt(8) / gr, 1), ' sd circolare', round(sqrt(-2 * log(A1(8))) / gr, 1),
    ' rapporto delle densità a 0 e 180 gradi', signif(exp(16), 3), '\n')
# Tappa 11: R dell'insieme e media degli R di stazione.
Rs <- tapply(d$azimut * gr, d$stazione, Rb)
cat('R insieme', round(Rb(d$azimut * gr), 3), ' media degli R di stazione', round(mean(Rs), 3), '\n')
# Tappa 13: probabilità di coda al valore critico simulato con la chi quadrato e con la correzione.
z <- 2.9106; n <- 20
cat('chi quadrato:', round(exp(-z), 4), ' correzione:', round(exp(-z) * (1 + (2 * z - z^2) / (4 * n) - (24 * z - 132 * z^2 + 76 * z^3 - 9 * z^4) / (288 * n^2)), 4), '\n')
# Tappa 14: potenza del test con kappa = 0,64 e n = 20.
rvm <- function(n, mu, k) {
  a <- 1 + sqrt(1 + 4 * k^2); b <- (a - sqrt(2 * a)) / (2 * k); r <- (1 + b^2) / (2 * b); out <- numeric(0)
  while (length(out) < n) {
    u1 <- runif(n); u2 <- runif(n); u3 <- runif(n); z <- cos(pi * u1); f <- (1 + r * z) / (r + z); g <- k * (r - f)
    ok <- g * (2 - g) - u2 > 0 | log(g / u2) + 1 - g >= 0; out <- c(out, sign(u3[ok] - 0.5) * acos(f[ok]))
  }
  (mu + out[1:n]) %% (2 * pi)
}
pv <- function(Z, n) exp(-Z) * (1 + (2 * Z - Z^2) / (4 * n) - (24 * Z - 132 * Z^2 + 76 * Z^3 - 9 * Z^4) / (288 * n^2))
set.seed(3); R1 <- replicate(4000, Rb(rvm(20, 0, .64)))
cat('Potenza con kappa 0,64 e n 20:', round(mean(pv(20 * R1^2, 20) < .05), 3), '\n')
# Tappe 18-20: famiglie di fratture.
fr <- read.csv(paste0(dir, 'fratture_v1.csv'))
j1 <- fr$direzione[fr$famiglia == 'J1']
cat('J1 registrate fra 180 e 360:', sum(j1 >= 180), 'su', length(j1), '\n')
R2 <- tapply(fr$direzione * gr * 2, fr$famiglia, Rb); nn <- table(fr$famiglia)
cat('R2 insieme atteso da due famiglie opposte:', round((nn[['J1']] * R2[['J1']] - nn[['J2']] * R2[['J2']]) / sum(nn), 3),
    ' calcolato', round(Rb(2 * fr$direzione * gr), 3), '\n')
# Tappa 23: posizione della direzione del dipolo nella proiezione.
Ig <- atan(2 * tan(42 * gr)) / gr
cat('Raggio nella proiezione per I =', round(Ig, 2), ':', round(sqrt(2) * sin((90 - Ig) * gr / 2), 3), '\n')
# Tappe 24-26: paleomagnetismo.
pm <- read.csv(paste0(dir, 'paleomag_v1.csv'))
X <- cbind(cos(pm$I * gr) * cos(pm$D * gr), cos(pm$I * gr) * sin(pm$D * gr), sin(pm$I * gr))
s <- colSums(X); N <- nrow(X); R <- sqrt(sum(s^2)); k <- (N - 1) / (N - R)
cat('Deviazione angolare 81/sqrt(k):', round(81 / sqrt(k), 1), ' inclinazione media', round(asin(s[3] / R) / gr, 2),
    ' differenza rispetto al dipolo', round(asin(s[3] / R) / gr - Ig, 2), '\n')
cat('Inclinazioni delle colate: da', min(pm$I), 'a', max(pm$I), ' declinazioni da', min((pm$D + 180) %% 360 - 180), 'a', max((pm$D + 180) %% 360 - 180), '\n')
# Tappa 28: asse stimato e asse del generatore 300/15.
st <- read.csv(paste0(dir, 'strati_v1.csv'))
P <- cbind(cos((90 - st$inclinazione) * gr) * cos((st$immersione + 180) * gr), cos((90 - st$inclinazione) * gr) * sin((st$immersione + 180) * gr),
           sin((90 - st$inclinazione) * gr))
v <- eigen(crossprod(P) / nrow(P))$vectors[, 3]
g <- c(cos(15 * gr) * cos(300 * gr), cos(15 * gr) * sin(300 * gr), sin(15 * gr))
cat('Angolo fra asse stimato e asse del generatore:', round(acos(abs(sum(v * g))) / gr, 1), 'gradi\n')
cat('Immersioni degli strati: fianco nord', sum(st$immersione < 90 | st$immersione > 270), ' fianco sud', sum(st$immersione >= 90 & st$immersione <= 270), '\n')
# Tappa 6: misure lontane dal gruppo principale, per stazione.
lon <- d$azimut > 100 & d$azimut < 300
cat('Misure fra 100 e 300 gradi:', sum(lon), ' di cui in S6:', sum(lon & d$stazione == 'S6'), '\n')
# Tappa 16: potenza con kappa = 0,3 e 150 misure.
set.seed(5); R1 <- replicate(2000, Rb(rvm(150, 0, .3)))
cat('Potenza con kappa 0,3 e n 150:', round(mean(pv(150 * R1^2, 150) < .05), 3), '\n')
