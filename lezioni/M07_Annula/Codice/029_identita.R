# Deviazioni standard con lo stesso denominatore.
b_da_r <- cor(x, y) * sd(y) / sd(x)
c(formula = b_da_r,
  lm = unname(coef(m0)[2]))
# R2 = r^2: solo regressione semplice
# OLS con intercetta, sugli stessi casi.
c(r2 = cor(x, y)^2,
  R2 = summary(m0)$r.squared)
