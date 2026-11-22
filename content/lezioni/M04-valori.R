# Aurea M04 · valori citati nelle spiegazioni estese delle tappe.
# Eseguire dalla radice del repository: Rscript content/lezioni/M04-valori.R
# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
setwd("lezioni/M04_Aurea")
invisible(capture.output(source("setup.R", encoding = "UTF-8")))
v <- function(nome, x) cat(sprintf("%-38s %s\n", nome, paste(format(x, digits = 7), collapse = "  ")))

# 9 · scarti delle frequenze finali da p
v("9 scarti |f - p|", abs(c(0.295, 0.29875, 0.31375) - 0.3))
# 16 · probabilità inverse
v("16 P(A) con prior .1", 0.8 * 0.1 + 0.2 * 0.9)
# 25 · code della normale standard oltre +-4
v("25 P(|Z| > 4)", 2 * pnorm(-4))
# 28 · binomiale n = 20, p = 0.3
v("28 P(K = 8), P(K >= 8)", c(dbinom(8, 20, 0.3), 1 - pbinom(7, 20, 0.3)))
# 44-49 · normale
v("44 z di 14, P(X <= 14)", c((14 - 10) / 2, pnorm(14, 10, 2)))
v("45 P(8 < X <= 12)", pnorm(12, 10, 2) - pnorm(8, 10, 2))
v("46 q.95, 10 + 2 z", c(qnorm(.95, 10, 2), 10 + 2 * qnorm(.95)))
v("47 estremi, 10 -+ 1.96*2", c(qnorm(c(.025, .975), 10, 2), 10 + c(-1, 1) * 1.96 * 2))
v("48 P(X<0) N(1,.8), N(10,2); z di 0", c(pnorm(0, 1, .8), pnorm(0, 10, 2), (0 - 1) / .8, (0 - 10) / 2))
v("49 q.95 N(20,4), z", c(qnorm(.95, 20, 4), (qnorm(.95, 20, 4) - 20) / 4))
# 50-56 · variabilità moltiplicativa
v("50 prodotto, 1.2*0.8", c(prod(c(1.2, .8, 1.1)), 1.2 * .8))
set.seed(17); x51 <- rlnorm(500, 0, .6)
v("51 range, log(range)", c(range(x51), log(range(x51))))
v("52 mediana, media teorica", c(exp(0), exp(.6^2 / 2)))
cv <- sqrt(expm1(c(.1, .3, .6)^2))
v("53 CV, CV/s", c(cv, cv / c(.1, .3, .6)))
set.seed(17); g54 <- rbinom(500, 1, .65)
f54 <- function(x) .65 * dnorm(x, 2, .7) + .35 * dnorm(x, 6, 1)
v("54 media, quota gruppo 1, f(3.4), f(2), f(6)", c(.65 * 2 + .35 * 6, mean(g54), f54(3.4), f54(2), f54(6)))
v("55 P(X<=0) N(1,.6), lognormale", c(pnorm(0, 1, .6), plnorm(0, 0, .6)))
v("56 medie teoriche, mode exp(-s^2)", c(exp(c(.3, .8)^2 / 2), exp(-c(.3, .8)^2)))
# 57 · Monte Carlo per E[X^2]
set.seed(17); y57 <- rnorm(5000)^2
v("57 stima, errore std teorico, scarto in es", c(mean(y57), sqrt(2 / 5000), (1 - mean(y57)) / sqrt(2 / 5000)))
# 58-64 · precisione Monte Carlo
p58 <- pbinom(7, 20, .3, lower.tail = FALSE)
v("58 SE con p esatta, scarto, scarto in es", c(sqrt(p58 * (1 - p58) / 10000), p58 - 0.2226, (p58 - 0.2226) / sqrt(p58 * (1 - p58) / 10000)))
set.seed(17); i60 <- rbinom(2000, 1, .1); p60 <- cumsum(i60) / seq_len(2000)
v("60 frequenza a B = 20, 100, 500, 2000", p60[c(20, 100, 500, 2000)])
v("61 B con p noto: quoziente diretto, ceiling", c(.1 * .9 / .01^2, ceiling(.1 * .9 / .01^2), ceiling((.1 / .01) * (.9 / .01))))
v("63 SD teorica lognormale (0, .6)", sqrt(expm1(.36)) * exp(.18))
v("64 densita vera, registrata, Delta d, SE media, rapporto", c(106 / 40, 108 / 40, 2 / 40, 1 / (40 * sqrt(20000)), (2 / 40) / (1 / (40 * sqrt(20000)))))
# 65 · laboratorio Monte Carlo
v("65 errori assoluti, in es, rapporto", c(abs(.075 - .1), abs(.09625 - .1), abs(.075 - .1) / sqrt(.09 / 200), abs(.09625 - .1) / sqrt(.09 / 800), abs(.075 - .1) / abs(.09625 - .1)))
# 67-72 · propagazione dell'incertezza
v("67 sdlog e meanlog per la massa", c(sqrt(log1p((1 / 106)^2)), log(106) - log1p((1 / 106)^2) / 2))
v("68 d0 -+ 1.96 uD lineare", 2.65 + c(-1, 1) * 1.96 * sqrt((1 / 40)^2 + (106 * .6 / 40^2)^2))
v("69 rapporto esatto a V = 40.6, tangente", c(106 / 40.6, 2.65 - 106 / 40^2 * .6))
q70 <- c((1 / 40)^2, (106 * .6 / 40^2)^2)
v("70 contributi, somma, somma delle SD", c(q70, sum(q70), sqrt(q70), sum(sqrt(q70))))
v("71 alpha, beta, rapporto SD c=-.7 / c=.7", c(1 / 106, .6 / 40, 0.05996926 / 0.02852740))
sig <- function(c) .1 * sqrt(2 - 2 * c)
sdR <- function(c) 2 * exp(sig(c)^2 / 2) * sqrt(expm1(sig(c)^2))
v("72 SD log R, SD R teorica con c = .7 e 0", c(sig(.7), sdR(.7), sig(0), sdR(0)))
# 73-78 · rapporto esatto e scelta dello strumento
v("73 tau^2", 2 * .1^2 * (1 - .7))
u78 <- function(um, uV) 2.65 * sqrt((um / 106)^2 + (uV / 40)^2)
v("78 riduzioni percentuali massa, volume", 100 * (1 - c(u78(.5, .6), u78(1, .3)) / u78(1, .6)))
# 81 · situazioni e controlli
v("81 P(nessun evento) con p = 0,001 e B = 500", (1 - 0.001)^500)
