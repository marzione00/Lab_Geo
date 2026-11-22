# Diagnosi del modello simulato.
mod <- lm(tmax ~ tmin, data = demo)
e <- residuals(mod)
plot(fitted(mod), e,
     xlab = "Valori stimati",
     ylab = "Residui [C]")
abline(h = 0, col = "grey50")
acf(e, main = "Residui nel tempo")
