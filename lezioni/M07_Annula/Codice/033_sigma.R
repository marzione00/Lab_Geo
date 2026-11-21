e <- residuals(m0)
n <- nobs(m0)
p <- m0$rank
s <- sqrt(sum(e^2) / (n - p))
c(calcolo = s, R = sigma(m0))
# RMSE in campione usa invece n.
sqrt(mean(e^2))
