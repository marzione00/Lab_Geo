# Valori citati nelle spiegazioni estese di Isocrona (M19). Uso: Rscript content/lezioni/M19-valori.R dalla radice.
# Figure e controlli numerici sono in lezioni/M19_Isocrona/R/M19_figure.R; i valori dei laboratori sono in
# lezioni/M19_Isocrona/Esperimenti/*.json.
source('lezioni/M19_Isocrona/R/york.R')
lam <- 1.3972e-11
d <- read.csv('lezioni/M19_Isocrona/dati/isocrone_v1.csv'); g <- d[d$suite == 'granito', ]; f <- d[d$suite == 'filone', ]
# Tappa 4: frazione di 87Rb decaduta in 300 milioni di anni e approssimazione lineare.
cat('Frazione decaduta in 300 Ma:', round(100 * (1 - exp(-lam * 3e8)), 3), '%  e^(lt)-1:', signif(exp(lam * 3e8) - 1, 5), ' lt:', signif(lam * 3e8, 5), '\n')
# Tappa 12: errore standard della pendenza dei minimi quadrati ordinari e residui.
m <- summary(lm(Sr87Sr86 ~ Rb87Sr86, data = g))
cat('OLS: errore standard della pendenza', signif(m$coefficients[2, 2], 3), ' deviazione standard dei residui', signif(m$sigma, 3), '\n')
cat('OLS: età', round(log(1 + m$coefficients[2, 1]) / lam / 1e6, 2), ' +/-', round(m$coefficients[2, 2] / (lam * (1 + m$coefficients[2, 1])) / 1e6, 2), '\n')
yg <- with(g, york(Rb87Sr86, sRb, Sr87Sr86, sSr))
# Tappa 14: peso relativo dei campioni nella regressione di York (W normalizzati).
W <- with(g, 1 / (sRb^2 * yg[['b']]^2 + sSr^2)); cat('Pesi relativi di York, primo e ultimo campione:', round(W[1] / sum(W), 3), round(W[10] / sum(W), 4), '\n')
# Tappa 19: quota della somma dei residui pesati del filone dovuta a F03 e F04.
yf <- with(f, york(Rb87Sr86, sRb, Sr87Sr86, sSr))
e <- with(f, (Sr87Sr86 - yf[['a']] - yf[['b']] * Rb87Sr86) / sqrt(sRb^2 * yf[['b']]^2 + sSr^2))
cat('Somma dei quadrati', round(sum(e^2), 2), ' quota di F03 e F04', round(sum(e[3:4]^2) / sum(e^2), 2), '\n')
cat('Filone: rapporto iniziale', round(yf[['a']], 6), ' +/-', signif(yf[['sa']], 2), '\n')
# Tappa 24: incertezza relativa della costante di 238U (1 sigma).
cat('Costante di 238U, incertezza relativa a 1 sigma:', round(100 * 0.00333 / 2 / 1.55125, 3), '%\n')
# Tappa 26: distanza di Z15 dalla media dei quattordici zirconi.
z <- read.csv('lezioni/M19_Isocrona/dati/date_v1.csv')
w <- 1 / z$s_Ma[-15]^2; m14 <- sum(w * z$data_Ma[-15]) / sum(w)
cat('Z15 - media:', round(z$data_Ma[15] - m14, 2), ' in unità della sua incertezza:', round((z$data_Ma[15] - m14) / z$s_Ma[15], 1), '\n')
cat('Probabilità di una MSWD di 19,4 con 14 gradi di libertà:', signif(pchisq(19.384 * 14, 14, lower.tail = FALSE), 2), '\n')
# Tappa 22: quota di MSWD oltre la soglia con errori corretti, quattromila isocrone simulate.
bt <- exp(lam * 3e8) - 1; xt <- seq(.2, 12, length.out = 10); set.seed(1)
ms <- replicate(4000, { x <- xt + rnorm(10, 0, .01 * xt); y <- .7085 + bt * xt + rnorm(10, 0, 1.1e-5); york(x, .01 * xt, y, rep(1.1e-5, 10))[['mswd']] })
cat('MSWD media', round(mean(ms), 3), ' quota oltre 2:', round(mean(ms > 2), 3), ' attesa dalla chi quadrato:', round(pchisq(16, 8, lower.tail = FALSE), 3), '\n')
