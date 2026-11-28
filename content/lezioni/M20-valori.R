# Valori citati nelle spiegazioni estese di Numerus (M20). Uso: Rscript content/lezioni/M20-valori.R dalla radice.
# Figure e controlli numerici sono in lezioni/M20_Numerus/R/M20_figure.R; i valori dei laboratori sono in
# lezioni/M20_Numerus/Esperimenti/*.json.
d <- read.csv('lezioni/M20_Numerus/dati/frane_v1.csv')
d$litologia <- factor(d$litologia, levels = c('Argille', 'Flysch', 'Calcari'))
# Tappa 4: celle per litologia, quota di zeri e pendenza a cui la retta prevede zero frane.
print(table(d$litologia)); cat('Quota di celle senza frane:', round(mean(d$frane == 0), 3), '\n')
ml <- lm(frane ~ pendenza, data = d)
z0 <- -coef(ml)[[1]] / coef(ml)[[2]]
cat('Pendenza con previsione nulla:', round(z0, 2), ' celle con pendenza inferiore:', sum(d$pendenza < z0), ' pendenza minima:', min(d$pendenza), '\n')
# Tappa 5: pendenza media e frane per km2 per litologia.
print(round(cbind(pendenza = tapply(d$pendenza, d$litologia, mean),
                  densita = tapply(d$frane, d$litologia, sum) / tapply(d$area_km2, d$litologia, sum)), 2))
m <- glm(frane ~ pendenza + litologia + offset(log(area_km2)), family = poisson, data = d)
b <- coef(m); se <- sqrt(diag(vcov(m)))
# Tappa 7: tasso delle argille a 0 e a 20 gradi; correlazione fra log(area) e pendenza.
cat('Tasso argille a 0 gradi:', round(exp(b[[1]]), 3), ' a 20 gradi:', round(exp(b[[1]] + 20 * b[[2]]), 2),
    ' correlazione log(area)-pendenza:', round(cor(log(d$area_km2), d$pendenza), 3), '\n')
m_senza <- glm(frane ~ pendenza + litologia, family = poisson, data = d)
cat('Rapporto per 10 gradi senza offset:', round(exp(10 * coef(m_senza)[['pendenza']]), 2), '\n')
# Tappa 10: iterazioni usate da glm.
cat('Iterazioni di glm:', m$iter, '\n')
# Tappa 12: calcari rispetto al flysch.
cat('Calcari / flysch:', round(exp(b[['litologiaCalcari']] - b[['litologiaFlysch']]), 3), '\n')
# Tappa 13: statistica di Wald della pendenza, devianza nulla e probabilità di coda della devianza residua.
cat('Wald pendenza:', round(b[['pendenza']] / se[['pendenza']], 2), ' devianza nulla:', round(m$null.deviance, 1), 'con', m$df.null,
    'gl  coda della devianza residua:', signif(pchisq(deviance(m), m$df.residual, lower.tail = FALSE), 2), '\n')
# Tappa 17: somma dei quadrati dei residui di Pearson e devianza divisa per i gradi di libertà.
cat('Somma Pearson:', round(sum(residuals(m, 'pearson')^2), 1), ' devianza / gl:', round(deviance(m) / m$df.residual, 3), '\n')
# Tappe 18-19: varianze attese nell'ultimo gruppo e intervallo del parametro di forma.
X <- model.matrix(m); o <- log(d$area_km2); y <- d$frane
nll <- function(p) -sum(dnbinom(y, size = exp(p[5]), mu = exp(drop(X %*% p[1:4]) + o), log = TRUE))
nb <- optim(c(b, 0), nll, method = 'BFGS', hessian = TRUE, control = list(reltol = 1e-14, maxit = 1000))
snb <- sqrt(diag(solve(nb$hessian))); th <- exp(nb$par[5]); phi <- sum(residuals(m, 'pearson')^2) / m$df.residual
mu9 <- 9.414429
cat('Media 9,41: Poisson', mu9, ' quasi', round(phi * mu9, 1), ' binomiale negativa', round(mu9 + mu9^2 / th, 1), '\n')
cat('Parametro di forma:', round(th, 2), ' intervallo', round(exp(nb$par[5] + c(-1.96, 1.96) * snb[5]), 2), '\n')
cat('Binomiale negativa, rapporti litologia:', round(exp(nb$par[3:4]), 3), '\n')
# Tappa 20: rapporto vero del generatore per 10 gradi.
cat('Rapporto vero per 10 gradi (generatore 0,07):', round(exp(0.7), 3), '\n')
# Tappe 24-28: conteggio per punti.
s <- read.csv('lezioni/M20_Numerus/dati/conteggi_v1.csv'); s$prop <- s$feldspato / s$punti
lp <- lm(prop ~ distanza_km, data = s)
cat('Distanza massima:', max(s$distanza_km), ' la retta tocca zero a', round(-coef(lp)[[1]] / coef(lp)[[2]], 1), 'km\n')
bl <- glm(cbind(feldspato, punti - feldspato) ~ distanza_km, family = binomial, data = s)
a <- coef(bl)[[1]]; bb <- coef(bl)[[2]]; sb <- sqrt(vcov(bl)[2, 2]); phib <- sum(residuals(bl, 'pearson')^2) / bl$df.residual
cat('Distanza a cui p = 0,1:', round((qlogis(.1) - a) / bb, 1), 'km\n')
cat('Rapporto per 10 km, intervallo binomiale:', round(exp(10 * (bb + c(-1.96, 1.96) * sb)), 3),
    ' quasi-binomiale:', round(exp(10 * (bb + c(-1.96, 1.96) * sb * sqrt(phib))), 3), '\n')
p0 <- plogis(a); p60 <- plogis(a + 60 * bb)
cat('Variazione di p per km a 0 e a 60 km:', round(bb * p0 * (1 - p0), 4), round(bb * p60 * (1 - p60), 5), '\n')
cat('Punti contati: totale', sum(s$punti), ' frazione media', round(mean(s$prop), 3), '\n')
