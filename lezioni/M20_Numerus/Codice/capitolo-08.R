s <- read.csv('dati/conteggi_v1.csv')
b <- glm(cbind(feldspato,
  punti - feldspato) ~ distanza_km,
  family = binomial, data = s)
r <- residuals(b, type = 'pearson')
phi <- sum(r^2) / b$df.residual
se <- sqrt(diag(vcov(b)))[[2]]
round(c(b = coef(b)[[2]], se = se,
  phi = phi, se_quasi = se * sqrt(phi),
  OR_10km = exp(10 * coef(b)[[2]])), 4)
