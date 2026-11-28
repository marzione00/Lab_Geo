# Azimut (M18): generatore dei quattro file di dati direzionali sintetici.
# correnti_v1.csv: azimut di immersione delle lamine oblique (paleocorrenti), sei stazioni, von Mises per stazione.
# fratture_v1.csv: direzioni di due famiglie di fratture subverticali, registrate con l'una o l'altra estremità.
# paleomag_v1.csv: direzioni di magnetizzazione di quattordici colate, distribuzione di Fisher.
# strati_v1.csv: giaciture della stratificazione attorno a una piega cilindrica.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
set.seed(20261129)
gr <- pi / 180
# Generatore di von Mises (Best e Fisher, 1979): accettazione e rifiuto con inviluppo di Cauchy avvolta.
rvm <- function(n, mu, k) {
  a <- 1 + sqrt(1 + 4 * k^2); b <- (a - sqrt(2 * a)) / (2 * k); r <- (1 + b^2) / (2 * b)
  out <- numeric(0)
  while (length(out) < n) {
    u1 <- runif(n); u2 <- runif(n); u3 <- runif(n)
    z <- cos(pi * u1); f <- (1 + r * z) / (r + z); g <- k * (r - f)
    ok <- g * (2 - g) - u2 > 0 | log(g / u2) + 1 - g >= 0
    out <- c(out, sign(u3[ok] - 0.5) * acos(f[ok]))
  }
  (mu + out[1:n]) %% (2 * pi)
}
# Direzioni nello spazio: coordinate (Nord, Est, Basso) da azimut e inclinazione verso il basso, e ritorno.
vett <- function(az, inc) cbind(cos(inc * gr) * cos(az * gr), cos(inc * gr) * sin(az * gr), sin(inc * gr))
angoli <- function(v) cbind(az = (atan2(v[, 2], v[, 1]) / gr) %% 360, inc = asin(pmax(-1, pmin(1, v[, 3]))) / gr)
# Fisher: angolo dal centro per inversione della funzione di ripartizione, azimut uniforme attorno al centro.
rfisher <- function(n, m, k) {
  ct <- 1 + log(1 - runif(n) * (1 - exp(-2 * k))) / k; st <- sqrt(1 - ct^2); ph <- runif(n, 0, 2 * pi)
  u <- if (abs(m[3]) < .9) c(0, 0, 1) else c(1, 0, 0)
  e1 <- u - sum(u * m) * m; e1 <- e1 / sqrt(sum(e1^2)); e2 <- c(m[2] * e1[3] - m[3] * e1[2], m[3] * e1[1] - m[1] * e1[3],
                                                               m[1] * e1[2] - m[2] * e1[1])
  outer(ct, m) + outer(st * cos(ph), e1) + outer(st * sin(ph), e2)
}

# 1. Paleocorrenti: direzione regionale 352 gradi, scarti di stazione e concentrazioni diverse.
staz <- data.frame(stazione = paste0('S', 1:6), mu = 352 + c(-10, -3, 5, 12, -6, 18), k = c(4, 6, 3, 5, 2.5, .4))
cor <- do.call(rbind, lapply(seq_len(nrow(staz)), function(i)
  data.frame(stazione = staz$stazione[i], azimut = round(rvm(20, staz$mu[i] * gr, staz$k[i]) / gr) %% 360)))
cor <- data.frame(id = sprintf('L%03d', seq_len(nrow(cor))), cor)
write.csv(cor, 'dati/correnti_v1.csv', row.names = FALSE)

# 2. Fratture: due famiglie, J1 a 40 gradi e J2 a 128 gradi; concentrazione assegnata agli angoli raddoppiati.
fam <- data.frame(famiglia = c('J1', 'J2'), asse = c(40, 128), k2 = c(8, 5), n = c(70, 40))
fr <- do.call(rbind, lapply(1:2, function(i) {
  a <- (rvm(fam$n[i], 2 * fam$asse[i] * gr, fam$k2[i]) / 2) / gr
  a <- (a + 180 * rbinom(fam$n[i], 1, .5)) %% 360
  data.frame(stazione = sample(c('F1', 'F2', 'F3'), fam$n[i], TRUE), famiglia = fam$famiglia[i], direzione = round(a) %% 360)
}))
fr <- fr[order(fr$stazione, runif(nrow(fr))), ]
fr <- data.frame(id = sprintf('F%03d', seq_len(nrow(fr))), fr)
write.csv(fr, 'dati/fratture_v1.csv', row.names = FALSE)

# 3. Paleomagnetismo: quattordici colate, direzione media D = 344, I = 56, concentrazione k = 55.
pm <- angoli(rfisher(14, vett(344, 56)[1, ], 55))
pm <- data.frame(colata = sprintf('C%02d', 1:14), D = round(pm[, 'az'], 1), I = round(pm[, 'inc'], 1))
stopifnot(all(pm$I > 0))
write.csv(pm, 'dati/paleomag_v1.csv', row.names = FALSE)

# 4. Stratificazione: piega cilindrica con asse 300/15; i poli ruotano attorno all'asse, con dispersione di Fisher.
asse <- vett(300, 15)[1, ]
u <- c(0, 0, 1) - sum(c(0, 0, 1) * asse) * asse; u <- u / sqrt(sum(u^2))
w <- c(asse[2] * u[3] - asse[3] * u[2], asse[3] * u[1] - asse[1] * u[3], asse[1] * u[2] - asse[2] * u[1])
phi <- c(rnorm(30, 48, 9), rnorm(24, -55, 9), rnorm(6, 0, 12)) * gr
poli <- t(sapply(phi, function(f) rfisher(1, cos(f) * u + sin(f) * w, 90)[1, ]))
poli <- poli * sign(poli[, 3])
pa <- angoli(poli)
st <- data.frame(id = sprintf('B%02d', seq_len(nrow(pa))), stazione = sample(c('A', 'B', 'C'), nrow(pa), TRUE),
                 immersione = round((pa[, 'az'] + 180) %% 360) %% 360, inclinazione = round(90 - pa[, 'inc']))
write.csv(st, 'dati/strati_v1.csv', row.names = FALSE)
cat('Paleocorrenti:', nrow(cor), ' fratture:', nrow(fr), ' colate:', nrow(pm), ' strati:', nrow(st), '\n')
print(table(fr$famiglia, fr$stazione))
