d <- read.csv('dati/frane_v1.csv')
m <- glm(frane ~ pendenza + litologia +
  offset(log(area_km2)), poisson, d)
r <- residuals(m, type = 'pearson')
phi <- sum(r^2) / m$df.residual
q <- update(m, family = quasipoisson)
se <- function(f) sqrt(diag(vcov(f)))[[2]]
round(c(phi = phi, se_poisson = se(m),
  se_quasi = se(q)), 4)
