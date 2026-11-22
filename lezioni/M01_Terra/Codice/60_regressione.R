# Esempio didattico simulato.
mod <- lm(tmax ~ tmin, data = demo)
coef(mod)              # coefficienti
residui <- residuals(mod)
plot(demo$tmin, demo$tmax,
     xlab = "Tmin [C]",
     ylab = "Tmax [C]")
abline(mod, col = "steelblue")
