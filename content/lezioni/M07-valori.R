# Annula M07 · valori citati nelle spiegazioni estese delle tappe.
# Eseguire dalla radice del repository: Rscript content/lezioni/M07-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M07_Annula")
invisible(capture.output(source("setup.R", encoding = "UTF-8")))
v <- function(nome, x) cat(sprintf("%-38s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))
f <- read.csv("Dati/fossili_simulati.csv"); f$morfotipo <- factor(f$morfotipo, levels = c("Rounded", "Spiky"))
x <- f$diametro_tot_um; y <- f$diametro_int_um
m <- lm(diametro_int_um ~ diametro_tot_um, f)
# 6 · media marginale e condizionata
v("6 media y, sd y, sigma residua, r", c(mean(y), sd(y), sigma(m), cor(x, y)))
v("4 media e sd spessore", c(mean(f$spessore_um), sd(f$spessore_um)))
# 8-12 · correlazione
v("9 r, slope y su x, slope x su y", c(cor(x, y), coef(m)[2], coef(lm(x ~ y))[2]))
rho <- function(vx) sqrt(4 * vx / (4 * vx + 1))
set.seed(17); u <- runif(1000, -4, 4)
v("12 rho teorico intero e ristretto, n centrali", c(rho(64 / 12), rho(4 / 12), sum(abs(u) < 1)))
# 14-20 · minimi quadrati
v("15-20 coef, Sxx, Sxy, SSE", c(coef(m), sum((x - mean(x))^2), sum((x - mean(x)) * (y - mean(y))), sum(residuals(m)^2)))
v("17 SSE retta proposta, rapporto", c(sum((y - (-.5 + .9 * x))^2), sum((y - (-.5 + .9 * x))^2) / sum(residuals(m)^2)))
v("19 somma residui", sum(residuals(m)))
# 21-27 · stime e disegno
s0 <- summary(m)
v("23 sigma, R2, R2 adj, SE coef", c(s0$sigma, s0$r.squared, s0$adj.r.squared, coef(s0)[, 2]))
v("24 previsione a 7 e a media x", c(predict(m, data.frame(diametro_tot_um = 7)), mean(y) + coef(m)[2] * (7 - mean(x))))
X <- model.matrix(m)
v("27 X'e massimo, coef da formula", c(max(abs(crossprod(X, residuals(m)))), solve(crossprod(X), crossprod(X, y))))
v("34 SE pendenza da formula, sqrt(Sxx)", c(sigma(m) / sqrt(sum((x - mean(x))^2)), sqrt(sum((x - mean(x))^2))))
# 35-41 · intervalli
h0 <- function(x0) 1 / length(x) + (x0 - mean(x))^2 / sum((x - mean(x))^2)
v("36-39 h0(7), SE media, SE pred, quantile t", c(h0(7), sigma(m) * sqrt(h0(7)), sigma(m) * sqrt(1 + h0(7)), qt(.975, 158)))
v("40 h0(11), semiampiezza pred a 11 e a 7, h0 a media", c(h0(11), qt(.975, 158) * sigma(m) * sqrt(1 + h0(11)), qt(.975, 158) * sigma(m) * sqrt(1 + h0(7)), h0(mean(x))))
v("41 semiampiezza pred limite n infinito", qt(.975, 158) * sigma(m))
# 44-48 · diagnostica
mq <- lm(diametro_int_um ~ diametro_tot_um + I(diametro_tot_um^2), f)
v("44 coef quadratico, p, SSE quad, SSE lin", c(coef(summary(mq))[3, c(1, 4)], sum(residuals(mq)^2), sum(residuals(m)^2)))
set.seed(746); e46 <- as.numeric(arima.sim(model = list(ar = .75), n = 80))
v("46 acf lag 1 e 2, banda 2/sqrt(80)", c(acf(e46, plot = FALSE)$acf[2:3], 2 / sqrt(80)))
rs <- rstandard(m)
v("48 n |r| > 2, atteso 5%", c(sum(abs(rs) > 2), .05 * 160, range(rs)))
# 49-55 · leva, influenza, scala logaritmica
h <- hatvalues(m); D <- cooks.distance(m); j <- which.max(D)
v("49 leva media, max, x del max, leva F091", c(mean(h), max(h), x[which.max(h)], h[j]))
v("51 Cook max, secondo, 4/n, n > 4/n, rstandard F091", c(max(D), sort(D, TRUE)[2], 4 / 160, sum(D > 4 / 160), rstandard(m)[j]))
v("53 rapporto attenuazione teorico e campionario", c(1 / 1.64, 0.884271 / 1.445182))
ml <- lm(log(diametro_int_um) ~ log(diametro_tot_um), f)
v("54-55 sigma log, fattore exp(s2/2)", c(sigma(ml), exp(sigma(ml)^2 / 2)))
# 56-62 · più predittori e interazioni
ma <- lm(diametro_int_um ~ diametro_tot_um + morfotipo, f)
mi <- lm(diametro_int_um ~ diametro_tot_um * morfotipo, f)
v("56 sigma add vs semplice, riduzione %", c(sigma(ma), sigma(m), 100 * (1 - sigma(ma) / sigma(m))))
v("57 differenza marginale int Spiky-Rounded, tot", c(diff(tapply(y, f$morfotipo, mean)), diff(tapply(x, f$morfotipo, mean))))
v("58 SE e p del gruppo", coef(summary(ma))[3, c(2, 4)])
v("61 SE e p interazione, pendenza Spiky", c(coef(summary(mi))[4, c(2, 4)], sum(coef(mi)[c(2, 4)])))
v("62 range x per Rounded e Spiky", c(tapply(x, f$morfotipo, range), recursive = TRUE))
# 63-68 · centraggio e incertezza dei contrasti
f$x_c <- x - 7; mc <- lm(diametro_int_um ~ x_c * morfotipo, f)
v("63 intercetta centrata vs predict Rounded a 7", c(coef(mc)[1], predict(mi, data.frame(diametro_tot_um = 7, morfotipo = "Rounded"))))
v("64 SE contrasto a 7, SE beta2 a x=0, cov b2 b3", c(sqrt(vcov(mc)[3, 3]), sqrt(vcov(mi)[3, 3]), vcov(mi)[3, 4]))
cc <- c(0, 0, 1, 7); v("64 SE a 7 da vcov(m_int)", sqrt(drop(t(cc) %*% vcov(mi) %*% cc)))
# 71-77 · logistica
f$spiky <- as.integer(f$morfotipo == "Spiky")
ml2 <- glm(spiky ~ diametro_tot_um, f, family = binomial())
b <- coef(ml2)
v("74 x con p = .5, pendenza massima b1/4", c(-b[1] / b[2], b[2] / 4))
v("75 IC OR per 1 um (Wald)", exp(b[2] + c(-1, 1) * 1.96 * sqrt(vcov(ml2)[2, 2])))
pp <- plogis(b[1] + b[2] * c(6, 7, 8))
v("76 derivate locali a 6,7,8", b[2] * pp * (1 - pp))
v("77 classi 1 con soglia .5, frazione", c(sum(fitted(ml2) >= .5), mean(fitted(ml2) >= .5)))
# 85-90 · valutazione
is_test <- seq_len(nrow(f)) %% 5L == 0L; tr <- f[!is_test, ]; te <- f[is_test, ]
v("83 morfotipi nel test", table(te$morfotipo))
fo <- list(lin = diametro_int_um ~ diametro_tot_um, add = diametro_int_um ~ diametro_tot_um + morfotipo,
           pol = diametro_int_um ~ poly(diametro_tot_um, 3, raw = TRUE))
v("88 RMSE di training lin, add, pol", sapply(fo, function(fm) sqrt(mean(residuals(lm(fm, tr))^2))))
v("90 riduzione RMSE rispetto alla media, sd y test", c(1 - 0.199439 / 1.00291, sd(te$diametro_int_um)))
# 92 · sovradattamento simulato
set.seed(17); sim <- data.frame(x = seq(-1, 1, length.out = 24)); sim$y <- sin(3 * sim$x) + rnorm(24)
mp <- lm(y ~ poly(x, 3, raw = TRUE), sim)
nu <- data.frame(x = seq(-1, 1, length.out = 150)); nu$y <- sin(3 * nu$x) + rnorm(150)
v("92 RMSE training, RMSE nuovi, RMSE funzione vera su nuovi", c(sqrt(mean(residuals(mp)^2)), sqrt(mean((nu$y - predict(mp, nu))^2)), sqrt(mean((nu$y - sin(3 * nu$x))^2))))
v("95 IC additivo gruppo", coef(ma)[3] + c(-1, 1) * qt(.975, 157) * coef(summary(ma))[3, 2])
