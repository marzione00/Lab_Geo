d <- read.csv('dati/frane_v1.csv')
lv <- c('Argille', 'Flysch', 'Calcari')
d$litologia <- factor(d$litologia, lv)
X <- model.matrix(~ pendenza + litologia,
  data = d)
o <- log(d$area_km2)
nll <- function(p) -sum(dnbinom(d$frane,
  size = exp(p[5]),
  mu = exp(drop(X %*% p[1:4]) + o),
  log = TRUE))
f <- optim(rep(0, 5), nll,
  method = 'BFGS', hessian = TRUE)
se <- sqrt(diag(solve(f$hessian)))
round(c(b_pend = f$par[2], se = se[2],
  theta = exp(f$par[5])), 4)
