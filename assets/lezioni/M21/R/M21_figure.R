# Credentia (M21): figure e valori della lezione sull'inferenza bayesiana come stima.
# Uso: LC_ALL=C.UTF-8 Rscript R/M21_figure.R dalla cartella della lezione. Scrive figure/M21 e risultati/M21.
# Tassi in eruzioni per secolo; durate in secoli. Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
source('R/stile.R')
out <- 'risultati/M21'; dir.create(out, recursive = TRUE, showWarnings = FALSE)
v <- list()
e <- leggi('eruzioni_v1.csv'); a <- leggi('analoghi_v1.csv')
n <- nrow(e); T <- (2025 - 1650) / 100; h <- 0.5
a$T <- a$anni_osservati / 100

# 1. Stima di massima verosimiglianza, intervallo esatto e probabilità con il valore stimato.
v$registro <- c(eruzioni = n, secoli = T, stima = n / T, inf = qchisq(.025, 2 * n) / 2 / T, sup = qchisq(.975, 2 * n + 2) / 2 / T,
                p50_plugin = 1 - exp(-h * n / T))
# 2. Approssimazione su griglia con distribuzione a priori uniforme.
g <- seq(0, 10, length.out = 4001); dg <- g[2] - g[1]
post <- dpois(n, g * T); post <- post / sum(post * dg)
mg <- sum(g * post * dg); cdf <- cumsum(post * dg)
v$griglia <- c(media = mg, inf = g[which.max(cdf >= .025)], sup = g[which.max(cdf >= .975)])
verifica('griglia uniforme coincide con la gamma(n + 1, T)', abs(mg - (n + 1) / T) < 1e-4)
# 3. Distribuzione a priori dai vulcani analoghi: massima verosimiglianza della binomiale negativa marginale.
nll <- function(q) -sum(dnbinom(a$eruzioni, size = exp(q[1]), mu = exp(q[1] - q[2]) * a$T, log = TRUE))
o <- optim(c(1, 0), nll, control = list(reltol = 1e-12))
verifica('stima della distribuzione a priori convergente', o$convergence == 0)
A <- exp(o$par[1]); B <- exp(o$par[2]); A1 <- A + n; B1 <- B + T
v$priori <- c(a = A, b = B, media = A / B, inf = qgamma(.025, A, B), sup = qgamma(.975, A, B))
pa <- dgamma(g, A, B) * dpois(n, g * T); pa <- pa / sum(pa * dg)
verifica('aggiornamento coniugato coincide con la griglia', abs(sum(g * pa * dg) - A1 / B1) < 1e-4)
hpd <- function(a, b, lev = .95) { f <- function(l) qgamma(l + lev, a, b) - qgamma(l, a, b)
  l <- optimize(f, c(0, 1 - lev), tol = 1e-10)$minimum; qgamma(c(l, l + lev), a, b) }
v$posteriori <- c(a = A1, b = B1, media = A1 / B1, inf = qgamma(.025, A1, B1), sup = qgamma(.975, A1, B1),
                  hpd_inf = hpd(A1, B1)[1], hpd_sup = hpd(A1, B1)[2], peso_priori = B / B1)
pred <- function(a, b) 1 - (b / (b + h))^a
set.seed(20261214)
mc <- mean(1 - exp(-h * rgamma(2e5, A1, B1)))
verifica('probabilità predittiva: formula e Monte Carlo', abs(mc - pred(A1, B1)) < .003)
v$p50 <- c(plugin = 1 - exp(-h * n / T), uniforme = pred(n + 1, T), jeffreys = pred(n + .5, T), analoghi = pred(A1, B1))
kk <- 0:5
v$predittiva <- rbind(binomiale_negativa = dnbinom(kk, size = A1, mu = A1 / B1 * h), poisson = dpois(kk, n / T * h))
# 4. Frazione esplosiva: beta-binomiale.
k <- sum(e$tipo == 'esplosiva')
bnll <- function(q) -sum(lchoose(a$eruzioni, a$esplosive) + lbeta(a$esplosive + exp(q[1]), a$eruzioni - a$esplosive + exp(q[2])) - lbeta(exp(q[1]), exp(q[2])))
ob <- optim(c(0, 0), bnll, control = list(reltol = 1e-12)); al <- exp(ob$par[1]); be <- exp(ob$par[2])
verifica('stima della beta a priori convergente', ob$convergence == 0)
bp <- rbind(uniforme = c(1, 1), jeffreys = c(.5, .5), analoghi = c(al, be))
v$beta <- cbind(alfa = bp[, 1], beta = bp[, 2], media = (k + bp[, 1]) / (n + rowSums(bp)),
                inf = qbeta(.025, k + bp[, 1], n - k + bp[, 2]), sup = qbeta(.975, k + bp[, 1], n - k + bp[, 2]))
set.seed(20261215)
lam <- rgamma(2e5, A1, B1); pp <- rbeta(2e5, k + al, n - k + be)
v$esplosiva50 <- c(bayes = mean(1 - exp(-h * lam * pp)), plugin = 1 - exp(-h * n / T * k / n))
# 5. Sensibilità: quattro distribuzioni a priori, compresa una tratta da vulcani di altro tipo.
pr <- rbind(uniforme = c(1, 0), jeffreys = c(.5, 0), analoghi = c(A, B), altro_tipo = c(10, 1))
v$sensibilita <- cbind(media = (pr[, 1] + n) / (pr[, 2] + T), inf = qgamma(.025, pr[, 1] + n, pr[, 2] + T),
                       sup = qgamma(.975, pr[, 1] + n, pr[, 2] + T),
                       p_predittiva = c(NA, NA, pnbinom(n, size = A, mu = A / B * T), pnbinom(n, size = 10, mu = 10 * T)))
# 6. Tempi di riposo: Weibull con dato censurato e algoritmo di Metropolis.
rip <- diff(e$anno); s <- 2025 - max(e$anno)
lp <- function(th) sum(dweibull(rip, exp(th[1]), exp(th[2]), log = TRUE)) + pweibull(s, exp(th[1]), exp(th[2]), lower.tail = FALSE, log.p = TRUE) +
  dnorm(th[1], 0, 1, log = TRUE) + dnorm(th[2], log(40), 1, log = TRUE)
metropolis <- function(N, passo, seme) { set.seed(seme); th <- c(0, log(40)); ch <- matrix(NA, N, 2); acc <- 0
  for (i in 1:N) { p <- th + rnorm(2, 0, passo); if (log(runif(1)) < lp(p) - lp(th)) { th <- p; acc <- acc + 1 }; ch[i, ] <- th }
  list(ch = ch, acc = acc / N) }
m <- metropolis(5000, .25, 2026)
kc <- exp(m$ch[-(1:500), 1]); sc <- exp(m$ch[-(1:500), 2])
ess <- function(x) length(x) / (1 + 2 * sum(acf(x, plot = FALSE, lag.max = 100)$acf[-1][1:which.max(acf(x, plot = FALSE, lag.max = 100)$acf[-1] < .05)]))
# Integrazione su griglia bidimensionale come riferimento.
g1 <- seq(-2, 3, length.out = 401); g2 <- seq(log(15), log(150), length.out = 401)
L <- outer(g1, g2, Vectorize(function(x, y) lp(c(x, y)))); W <- exp(L - max(L)); W <- W / sum(W)
k_griglia <- sum(rowSums(W) * exp(g1)); pk1_griglia <- sum(rowSums(W)[g1 > 0])
m2 <- metropolis(40000, .25, 7)
k_lunga <- mean(exp(m2$ch[-(1:2000), 1]))
verifica('catena lunga di Metropolis coincide con la griglia', abs(k_lunga - k_griglia) < .05)
cond <- 1 - exp(-((s + 50) / sc)^kc + (s / sc)^kc)
v$weibull <- c(riposo_medio = mean(rip), dev_std = sd(rip), forma_mv = exp(optim(c(0, log(40)), function(t) -(lp(t) - dnorm(t[1], 0, 1, log = TRUE) - dnorm(t[2], log(40), 1, log = TRUE)))$par[1]),
               accettazione = m$acc, forma_media = mean(kc), forma_inf = quantile(kc, .025)[[1]], forma_sup = quantile(kc, .975)[[1]],
               p_forma_1 = mean(kc > 1), forma_griglia = k_griglia, p_forma_1_griglia = pk1_griglia, ess = ess(kc),
               p50_weibull = mean(cond), dall_ultima = s)

# Figure.
d1 <- rbind(data.frame(x = g, y = dgamma(g, A, B), f = 'A priori, analoghi'),
            data.frame(x = g, y = post, f = 'Verosimiglianza'),
            data.frame(x = g, y = pa, f = 'A posteriori'))
d1$f <- factor(d1$f, levels = c('A priori, analoghi', 'A posteriori', 'Verosimiglianza'))
salva('M21', 'F01', ggplot(d1[d1$x <= 9, ], aes(x, y, colour = f, linetype = f)) + geom_line(linewidth = 1) +
  scale_colour_manual(values = c(geo[6], geo[1], geo[3])) + scale_linetype_manual(values = c(2, 1, 1)) +
  scale_x_continuous(labels = fmt) + scale_y_continuous(labels = fmt) +
  labs(x = 'Eruzioni per secolo', y = 'Densità') + theme(legend.position = c(.99, .97), legend.justification = c(1, 1), legend.text = element_text(size = 14),
        legend.background = element_rect(fill = paper, colour = NA)), w = 5.6, h = 4)
ga <- data.frame(id = a$vulcano, r = a$eruzioni / a$T, i = qchisq(.025, 2 * a$eruzioni) / 2 / a$T, u = qchisq(.975, 2 * a$eruzioni + 2) / 2 / a$T, t = 'Analoghi')
ga <- rbind(ga[order(ga$r), ], data.frame(id = 'Caso', r = n / T, i = v$registro[['inf']], u = v$registro[['sup']], t = 'Caso'))
ga$id <- factor(ga$id, levels = ga$id)
salva('M21', 'F02', ggplot(ga, aes(r, id, colour = t)) +
  annotate('rect', xmin = v$priori[['inf']], xmax = v$priori[['sup']], ymin = -Inf, ymax = Inf, fill = geo[1], alpha = .08) +
  geom_vline(xintercept = A / B, linetype = 2, colour = geo[1]) + geom_errorbarh(aes(xmin = i, xmax = u), height = .3, linewidth = .7) +
  geom_point(size = 2.4) + scale_colour_manual(values = c(geo[6], geo[3])) + scale_x_continuous(labels = fmt) +
  labs(x = 'Eruzioni per secolo', y = NULL) + theme(axis.text.y = element_text(size = 12), legend.position = 'none'), w = 5.4, h = 4.4)
d3 <- data.frame(k = factor(rep(kk, 2)), p = c(v$predittiva[1, ], v$predittiva[2, ]), f = rep(c('Predittiva a posteriori', 'Poisson con il tasso stimato'), each = 6))
salva('M21', 'F03', ggplot(d3, aes(k, p, fill = f)) + geom_col(position = position_dodge(.75), width = .7) +
  scale_fill_manual(values = c(geo[3], geo[1])) + scale_y_continuous(labels = fmt) +
  labs(x = 'Eruzioni nei prossimi 50 anni', y = 'Probabilità') + guides(fill = guide_legend(nrow = 2)), w = 5.4, h = 4)
q <- seq(0, 1, length.out = 501)
d4 <- rbind(data.frame(x = q, y = dbeta(q, k + 1, n - k + 1), f = 'Uniforme'), data.frame(x = q, y = dbeta(q, k + .5, n - k + .5), f = 'Jeffreys'),
            data.frame(x = q, y = dbeta(q, k + al, n - k + be), f = 'Analoghi'), data.frame(x = q, y = dbeta(q, al, be), f = 'A priori, analoghi'))
d4$f <- factor(d4$f, levels = c('Uniforme', 'Jeffreys', 'Analoghi', 'A priori, analoghi'))
salva('M21', 'F04', ggplot(d4, aes(x, y, colour = f, linetype = f)) + geom_line(linewidth = 1) +
  scale_colour_manual(values = c(geo[3], geo[2], geo[1], geo[6])) + scale_linetype_manual(values = c(1, 1, 1, 2)) +
  scale_x_continuous(labels = fmt) + scale_y_continuous(labels = fmt) + labs(x = 'Frazione di eruzioni esplosive', y = 'Densità') +
  guides(colour = guide_legend(nrow = 2)), w = 5.6, h = 4)
d5 <- data.frame(t = c('Massima verosimiglianza', 'Uniforme', 'Jeffreys', 'Analoghi', 'Vulcani di altro tipo'),
                 m = c(n / T, v$sensibilita[, 'media']), i = c(v$registro[['inf']], v$sensibilita[, 'inf']), u = c(v$registro[['sup']], v$sensibilita[, 'sup']))
d5$t <- factor(d5$t, levels = rev(d5$t))
salva('M21', 'F05', ggplot(d5, aes(m, t)) + geom_errorbarh(aes(xmin = i, xmax = u), height = .25, colour = geo[1], linewidth = .8) +
  geom_point(colour = geo[2], size = 3) + scale_x_continuous(labels = fmt) + labs(x = 'Eruzioni per secolo', y = NULL) +
  theme(axis.text.y = element_text(size = 15)), w = 6, h = 3.6)
d6 <- rbind(data.frame(x = 1:2000, y = exp(m$ch[1:2000, 1]), p = 'Traccia'),
            data.frame(x = NA, y = kc, p = 'A posteriori'))
d6$p <- factor(d6$p, levels = c('Traccia', 'A posteriori'))
salva('M21', 'F06', ggplot() + geom_line(data = d6[d6$p == 'Traccia', ], aes(x, y), colour = geo[1], linewidth = .3) +
  geom_histogram(data = data.frame(y = kc, p = factor('A posteriori', levels = levels(d6$p))), aes(y = y), bins = 40, fill = '#8FC7BE', colour = NA) +
  geom_hline(data = data.frame(p = factor(levels(d6$p), levels = levels(d6$p)), y = 1), aes(yintercept = y), linetype = 2, colour = ink) +
  facet_wrap(~p, scales = 'free_x') + labs(x = NULL, y = 'Forma della Weibull, k') + theme(axis.text = element_text(size = 15), strip.text = element_text(size = 16)), w = 6.4, h = 3.8)

capture <- function(x) paste(capture.output(print(x)), collapse = '\n')
jsonlite::write_json(lapply(v, function(x) if (is.table(x) || is.matrix(x) || is.data.frame(x)) capture(x) else as.list(x)),
                     file.path(out, 'valori.json'), auto_unbox = TRUE, pretty = TRUE, digits = 8)
print(v)
