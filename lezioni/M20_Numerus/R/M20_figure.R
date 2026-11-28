# Numerus (M20): figure e valori della lezione sui modelli lineari generalizzati.
# Uso: LC_ALL=C.UTF-8 Rscript R/M20_figure.R dalla cartella della lezione. Scrive figure/M20 e risultati/M20.
# Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
source('R/stile.R')
out <- 'risultati/M20'; dir.create(out, recursive = TRUE, showWarnings = FALSE)
v <- list()
d <- leggi('frane_v1.csv'); d$litologia <- factor(d$litologia, levels = c('Argille', 'Flysch', 'Calcari'))

# 1. Descrizione e regressione lineare sui conteggi.
v$frane <- c(celle = nrow(d), totale = sum(d$frane), zeri = sum(d$frane == 0), media = mean(d$frane), varianza = var(d$frane),
             densita = sum(d$frane) / sum(d$area_km2))
ml <- lm(frane ~ pendenza, data = d)
v$lm_predizione_4 <- predict(ml, data.frame(pendenza = 4))
v$lm_coef <- coef(ml)

# 2. Modello di Poisson con offset; verifica dell'algoritmo IRLS scritto a mano.
m <- glm(frane ~ pendenza + litologia + offset(log(area_km2)), family = poisson, data = d)
X <- model.matrix(m); o <- log(d$area_km2); y <- d$frane
b <- rep(0, ncol(X)); for (k in 1:25) { eta <- drop(X %*% b) + o; mu <- exp(eta); z <- eta - o + (y - mu) / mu
  b <- drop(solve(crossprod(X, mu * X), crossprod(X, mu * z))) }
verifica('IRLS scritto a mano coincide con glm', max(abs(b - coef(m))) < 1e-8)
se <- sqrt(diag(vcov(m)))
v$poisson <- cbind(stima = coef(m), se = se)
v$rr <- exp(cbind(stima = coef(m), inf = coef(m) - 1.96 * se, sup = coef(m) + 1.96 * se))[-1, ]
v$rr10 <- exp(10 * c(stima = coef(m)[['pendenza']], inf = coef(m)[['pendenza']] - 1.96 * se[['pendenza']],
                     sup = coef(m)[['pendenza']] + 1.96 * se[['pendenza']]))
m0 <- update(m, . ~ . - litologia)
v$lrt <- c(devianza_m0 = deviance(m0), devianza_m = deviance(m), differenza = deviance(m0) - deviance(m), gl = 2,
           p = pchisq(deviance(m0) - deviance(m), 2, lower.tail = FALSE))
v$devianza_residua <- c(devianza = deviance(m), gl = m$df.residual)
mu <- fitted(m)
k <- 0:12
oss <- sapply(k, function(j) if (j < 12) sum(y == j) else sum(y >= 12))
att <- sapply(k, function(j) if (j < 12) sum(dpois(j, mu)) else sum(ppois(11, mu, lower.tail = FALSE)))
v$frequenze <- rbind(osservate = oss, attese_poisson = round(att, 1))

# 3. Sovradispersione: quasi-Poisson e binomiale negativa (stima per massima verosimiglianza con optim).
phi <- sum(residuals(m, 'pearson')^2) / m$df.residual
q <- glm(frane ~ pendenza + litologia + offset(log(area_km2)), family = quasipoisson, data = d)
verifica('quasi-Poisson: errori standard moltiplicati per la radice di phi', max(abs(sqrt(diag(vcov(q))) / se - sqrt(phi))) < 1e-4)
nll <- function(p) -sum(dnbinom(y, size = exp(p[5]), mu = exp(drop(X %*% p[1:4]) + o), log = TRUE))
nb <- optim(c(coef(m), 0), nll, method = 'BFGS', hessian = TRUE, control = list(reltol = 1e-14, maxit = 1000))
se_nb <- sqrt(diag(solve(nb$hessian)))
v$phi <- phi
v$binomiale_negativa <- rbind(stima = nb$par, se = se_nb)
v$theta <- exp(nb$par[5])
if (requireNamespace('MASS', quietly = TRUE)) {
  g <- MASS::glm.nb(frane ~ pendenza + litologia + offset(log(area_km2)), data = d)
  verifica('binomiale negativa con optim coincide con MASS::glm.nb', max(abs(coef(g) - nb$par[1:4])) < 1e-4 && abs(g$theta - v$theta) / g$theta < 1e-3)
}
ci <- function(b, s) exp(10 * c(b - 1.96 * s, b, b + 1.96 * s))
v$rr10_confronto <- rbind(Poisson = ci(coef(m)[[2]], se[[2]]), quasi = ci(coef(m)[[2]], se[[2]] * sqrt(phi)), binneg = ci(nb$par[2], se_nb[2]))
v$aic <- c(poisson = AIC(m), binomiale_negativa = 2 * nb$value + 2 * 5)
gr <- cut(mu, quantile(mu, 0:8 / 8), include.lowest = TRUE)
vm <- data.frame(media = tapply(mu, gr, mean), varianza = tapply((y - mu)^2, gr, mean))
v$varianza_gruppi <- vm

# 4. Proporzioni: conteggio per punti del feldspato, modello logistico e sovradispersione binomiale.
s <- leggi('conteggi_v1.csv'); s$prop <- s$feldspato / s$punti
lp <- lm(prop ~ distanza_km, data = s)
v$lm_proporzioni <- c(coef(lp), predizione_90 = predict(lp, data.frame(distanza_km = 90)))
bl <- glm(cbind(feldspato, punti - feldspato) ~ distanza_km, family = binomial, data = s)
phib <- sum(residuals(bl, 'pearson')^2) / bl$df.residual
seb <- sqrt(diag(vcov(bl)))
v$logistica <- c(a = coef(bl)[[1]], b = coef(bl)[[2]], se_b = seb[[2]], phi = phib, se_b_quasi = seb[[2]] * sqrt(phib),
                 or10 = exp(10 * coef(bl)[[2]]), p0 = plogis(coef(bl)[[1]]), p60 = plogis(coef(bl)[[1]] + 60 * coef(bl)[[2]]),
                 p90 = plogis(coef(bl)[[1]] + 90 * coef(bl)[[2]]))
v$errore_conteggio <- c(p = .25, n = 300, sd = sqrt(.25 * .75 / 300), due_sd = 2 * sqrt(.25 * .75 / 300))
# Varianza delle proporzioni entro stazione e varianza binomiale attesa.
w <- tapply(s$prop, s$stazione, var); pb <- tapply(s$prop, s$stazione, mean); nb_ <- tapply(s$punti, s$stazione, mean)
v$varianza_entro <- c(osservata = mean(w), binomiale = mean(pb * (1 - pb) / nb_))

# Figure.
nd <- expand.grid(pendenza = seq(4, 38, .5), litologia = levels(d$litologia)); nd$area_km2 <- 1
nd$mu <- predict(m, nd, type = 'response')
rg <- tapply(d$pendenza, d$litologia, range)
nd <- nd[mapply(function(x, l) x >= rg[[l]][1] && x <= rg[[l]][2], nd$pendenza, as.character(nd$litologia)), ]
d$densita <- d$frane / d$area_km2
ll <- lm(densita ~ pendenza, data = d)
salva('M20', 'F01', ggplot(d, aes(pendenza, densita, colour = litologia)) + geom_point(size = 2, alpha = .8) +
  geom_line(data = nd, aes(pendenza, mu, colour = litologia), linewidth = 1) +
  geom_abline(intercept = coef(ll)[1], slope = coef(ll)[2], linetype = 2, colour = ink) +
  scale_colour_manual(values = geo[c(3, 1, 2)]) + scale_y_continuous(labels = fmt) +
  labs(x = 'Pendenza media (gradi)', y = expression('Frane per km'^2)))
rr <- data.frame(t = c('Pendenza, +10°', 'Flysch / argille', 'Calcari / argille'),
                 s = c(v$rr10[['stima']], v$rr[2:3, 'stima']), i = c(v$rr10[['inf']], v$rr[2:3, 'inf']), u = c(v$rr10[['sup']], v$rr[2:3, 'sup']))
rr$t <- factor(rr$t, levels = rev(rr$t))
salva('M20', 'F02', ggplot(rr, aes(s, t)) + geom_vline(xintercept = 1, linetype = 2, colour = ink) +
  geom_errorbarh(aes(xmin = i, xmax = u), height = .2, colour = geo[1], linewidth = .8) + geom_point(colour = geo[2], size = 3) +
  scale_x_log10(breaks = c(.2, .5, 1, 2, 3), labels = fmt) + labs(x = 'Rapporto fra tassi (scala logaritmica)', y = NULL) +
  theme(axis.text.y = element_text(size = 17)), w = 6, h = 3.6)
fr <- data.frame(k = factor(c(0:11, '12+'), levels = c(0:11, '12+')), o = oss, a = att)
salva('M20', 'F03', ggplot(fr, aes(k)) + geom_col(aes(y = o), fill = '#8FC7BE', width = .7) +
  geom_point(aes(y = a), colour = geo[3], size = 3) + geom_line(aes(y = a, group = 1), colour = geo[3]) +
  labs(x = 'Frane per cella', y = 'Numero di celle') + theme(axis.text.x = element_text(size = 14)), w = 5.6, h = 3.8)
cm <- seq(0, max(vm$media) * 1.05, length.out = 100)
fv <- rbind(data.frame(m = cm, v = cm, f = 'Poisson'), data.frame(m = cm, v = phi * cm, f = 'Quasi-Poisson'),
            data.frame(m = cm, v = cm + cm^2 / v$theta, f = 'Binomiale negativa'))
salva('M20', 'F04', ggplot(fv, aes(m, v, colour = f)) + geom_line(linewidth = 1) + geom_point(data = vm, aes(media, varianza), inherit.aes = FALSE, size = 3, colour = ink) +
  scale_colour_manual(values = geo[c(2, 6, 1)]) + scale_x_continuous(labels = fmt) + scale_y_continuous(labels = fmt) +
  labs(x = 'Media stimata del gruppo', y = 'Varianza dei residui') + theme(legend.text = element_text(size = 14)) +
  guides(colour = guide_legend(nrow = 2)), w = 5.4, h = 4.2)
cf <- data.frame(t = c('Poisson', 'Quasi-Poisson', 'Binomiale negativa'), i = v$rr10_confronto[, 1], s = v$rr10_confronto[, 2], u = v$rr10_confronto[, 3])
cf$t <- factor(cf$t, levels = rev(cf$t))
salva('M20', 'F05', ggplot(cf, aes(s, t)) + geom_errorbarh(aes(xmin = i, xmax = u), height = .2, colour = geo[1], linewidth = .8) +
  geom_point(colour = geo[2], size = 3) + scale_x_continuous(labels = fmt) +
  labs(x = 'Rapporto fra tassi, +10 gradi', y = NULL) + theme(axis.text.y = element_text(size = 17)), w = 6, h = 3.4)
xs <- data.frame(distanza_km = seq(0, 90, .5)); xs$p <- predict(bl, xs, type = 'response'); xs$l <- predict(lp, xs)
salva('M20', 'F06', ggplot(s, aes(distanza_km, prop)) + geom_hline(yintercept = 0, colour = ink, linewidth = .3) +
  geom_point(colour = geo[1], size = 2.2) + geom_line(data = xs, aes(distanza_km, p), colour = geo[2], linewidth = 1) +
  geom_line(data = xs, aes(distanza_km, l), colour = geo[3], linewidth = .9, linetype = 2) +
  scale_y_continuous(labels = fmt) + labs(x = 'Distanza lungo il trasporto (km)', y = 'Frazione di feldspato'))

capture <- function(x) paste(capture.output(print(x)), collapse = '\n')
jsonlite::write_json(lapply(v, function(x) if (is.table(x) || is.matrix(x) || is.data.frame(x)) capture(x) else as.list(x)),
                     file.path(out, 'valori.json'), auto_unbox = TRUE, pretty = TRUE, digits = 8)
print(v)
