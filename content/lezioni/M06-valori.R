# Gemina M06 · valori citati nelle spiegazioni estese delle tappe.
# Eseguire dalla radice del repository: Rscript content/lezioni/M06-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M06_Gemina")
invisible(capture.output(source("setup.R", encoding = "UTF-8")))
v <- function(nome, x) cat(sprintf("%-38s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))
f <- read.csv("Dati/fossili_simulati.csv")
g <- split(f$diametro_tot_um, f$morfotipo)

# 4-9 · domanda, contrasto e sovrapposizione
v("4 range diametri, n per gruppo", c(range(f$diametro_tot_um), lengths(g)))
v("9 P(S > R), quota complementare", c(mean(outer(g$Spiky, g$Rounded, ">")), mean(outer(g$Spiky, g$Rounded, "<"))))
v("8 sd per gruppo", sapply(g, sd))
# 10-11 · intervallo di Welch e ipotesi
tt10 <- t.test(g$Spiky, g$Rounded)
v("10 df, quantile t, semiampiezza/SE", c(tt10$parameter, qt(.975, tt10$parameter), diff(tt10$conf.int) / 2 / tt10$stderr))
tt11 <- t.test(c(4, 6, 7, 8, 10), c(3, 4, 6, 7, 9))
v("11 stima, p bilaterale, p greater", c(diff(rev(tt11$estimate)), tt11$p.value, t.test(c(4, 6, 7, 8, 10), c(3, 4, 6, 7, 9), alternative = "greater")$p.value))
# 15-16 · permutazioni del generatore del laboratorio
set.seed(17); x15 <- c(rnorm(20), rnorm(20, .6)); g15 <- rep(0:1, each = 20)
obs15 <- diff(tapply(x15, g15, mean))
t15 <- replicate(200, { gp <- sample(g15); diff(tapply(x15, gp, mean)) })
v("15 osservato, range permutati, sd", c(obs15, range(t15), sd(t15)))
v("16 K, K/B, code sinistra e destra", c(sum(abs(t15) >= abs(obs15)), mean(abs(t15) >= abs(obs15)), sum(t15 <= -abs(obs15)), sum(t15 >= abs(obs15))))
# 17-19 · p-value Monte Carlo, bootstrap e vincoli
v("17 errore MC con q = .33, B = 200", sqrt(.33 * .67 / 200))
v("18 differenza osservata", mean(c(3, 5, 6, 8)) - mean(c(1, 2, 4, 5)))
set.seed(17); s19 <- sample(c(-1, 1), 4, replace = TRUE)
v("19 segni estratti, osservata", c(s19, mean(c(.4, -.2, .7, .5))))
# 25, 29-30 · intervalli, calibrazione e potenza
v("25 IC che contengono zero", c(.2 - 1.96 * .4, 1 - 1.96 * .8))
v("29 SE Monte Carlo per .05, scarto in es", c(sqrt(.05 * .95 / 5000), (.0526 - .05) / sqrt(.05 * .95 / 5000)))
eta30 <- .5 / sqrt(2 / 30)
v("30 eta, coda sinistra, coda destra", c(eta30, pnorm(-qnorm(.975), eta30), pnorm(qnorm(.975), eta30, lower.tail = FALSE)))
# 31-35 · potenza e numerosità
v("31 potenza normale vs t", c(pnorm(-qnorm(.975), .5 / sqrt(2 / 30)) + pnorm(qnorm(.975), .5 / sqrt(2 / 30), lower.tail = FALSE), power.t.test(n = 30, delta = .5, sd = 1, strict = TRUE)$power))
v("33 n teorico normale", 2 * (qnorm(.975) + qnorm(.8))^2 / .5^2)
r34 <- power.t.test(delta = .5, sd = 1, power = .8, strict = TRUE)
v("34 n teorico t, potenza con n = 64", c(r34$n, power.t.test(n = 64, delta = .5, sd = 1, strict = TRUE)$power))
set.seed(1); z <- apply(matrix(rnorm(100 * 100000), 100), 2, function(x) cumsum(x)[seq(10, 100, 10)] / sqrt(seq(10, 100, 10)))
v("35 P(almeno un superamento) su 1e5 percorsi", mean(apply(abs(z) > qnorm(.975), 2, any)))
set.seed(6035); X <- matrix(rnorm(100 * 5000), nrow = 100); Z <- apply(X, 2, cumsum)[seq(10, 100, 10), ] / sqrt(seq(10, 100, 10))
rj <- abs(Z) > qnorm(.975)
v("35 figura: finale a n = 100, qualsiasi entro 100", c(mean(rj[10, ]), mean(colSums(rj) > 0)))
# 38-41 · Welch sui fossili
va <- var(g$Rounded) / 80; vb <- var(g$Spiky) / 80
v("38 quota A, varianze s2", c(va / (va + vb), var(g$Rounded), var(g$Spiky)))
v("40 nu fossili, massimo n-2, curva n=30 a 1 e 2", c((va + vb)^2 / (va^2 / 79 + vb^2 / 79), 158, (1 + 1)^2 / (1 / 29 + 1 / 29), (1 + 4)^2 / (1 / 29 + 16 / 29)))
# 45-46 · effetti standardizzati e laboratorio Welch
v("45 sp, sA", c(sqrt((79 * var(g$Rounded) + 79 * var(g$Spiky)) / 158), sd(g$Rounded)))
set.seed(17); a46 <- rnorm(30); b46 <- rnorm(30, .5, 2); tt46 <- t.test(b46, a46)
v("46 SE, df, sd campionarie, t", c(tt46$stderr, tt46$parameter, sd(a46), sd(b46), tt46$statistic))
# 49-53 · misure appaiate
p <- read.csv("Dati/misure_appaiate_simulate.csv"); D <- p$dopo - p$prima
v("49 n, media D, sd D, negativi, range prima e dopo", c(length(D), mean(D), sd(D), sum(D < 0), range(p$prima), range(p$dopo)))
v("50 var prima, var dopo, cov", c(var(p$prima), var(p$dopo), cov(p$prima, p$dopo)))
ti <- t.test(p$dopo, p$prima)
v("52-53 SE appaiato, SE ignorando coppie, p Welch, IC Welch", c(sd(D) / sqrt(24), ti$stderr, ti$p.value, ti$conf.int))
v("51 SE teorici appaiato e indipendente (tau = 3)", c(sqrt(2 / 30), sqrt(2 * (9 + 1) / 30)))
# 56-59 · ranghi e segni
v("56 U = theta * 6400, W di wilcox", c(mean(outer(g$Spiky, g$Rounded, ">")) * 6400, wilcox.test(g$Spiky, g$Rounded, exact = FALSE)$statistic))
v("59 p binomiale esatto 4 su 6", c(2 * sum(dbinom(4:6, 6, .5)), binom.test(4, 6)$p.value))
# 62-66 · conteggi e più gruppi
O <- matrix(c(18, 12, 9, 21), 2, byrow = TRUE)
v("62 scarto al quadrato, p con Yates", c((18 - 13.5)^2, chisq.test(O)$p.value))
v("63 OR campionario, P(tabella osservata)", c(18 * 21 / (12 * 9), dhyper(18, 27, 33, 30)))
v("64 differenza quote", 25 / 60 - 15 / 50)
v("66 SST", sum((c(1, 3, 4, 6) - 3.5)^2))
# 68-72 · più gruppi e famiglie
r <- read.csv("Dati/rocce_simulate.csv")
v("68 n e medie per litologia", c(table(r$litologia_generatrice), tapply(r$densita, r$litologia_generatrice, mean)))
v("68 F classico, p", c(anova(lm(densita ~ litologia_generatrice, r))$`F value`[1], anova(lm(densita ~ litologia_generatrice, r))$`Pr(>F)`[1]))
set.seed(17); g69 <- rep(LETTERS[1:4], each = 30); y69 <- rnorm(120, rep(0:3, each = 30)); z69 <- split(y69, g69)
p69 <- sapply(z69[c("B", "C", "D")], function(z) t.test(z, z69$A)$p.value)
v("69 p grezzi", p69)
v("72 FWER teorico 20 test, SE MC grezzo e Holm, scarto in es", c(1 - .95^20, sqrt(.6415 * .3585 / 2000), sqrt(.05 * .95 / 2000), (0.6415141 - 0.6185) / sqrt(.6415 * .3585 / 2000)))
# 79-84 · laboratori
v("79 K con B = 1000, SE MC", c(0.3196803 * 1001 - 1, sqrt(.32 * .68 / 1000)))
v("82 ampiezze IC", c(1.0262567 + 0.9191145, 0.6426255 + 0.4368647))
