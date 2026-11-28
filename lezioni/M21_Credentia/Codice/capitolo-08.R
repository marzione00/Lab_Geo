e <- read.csv('dati/eruzioni_v1.csv')
r <- diff(e$anno); s <- 2025 - max(e$anno)
lp <- function(t) sum(dweibull(r,
  exp(t[1]), exp(t[2]), log = TRUE)) +
  pweibull(s, exp(t[1]), exp(t[2]),
    FALSE, TRUE) +
  dnorm(t[1], 0, 1, TRUE) +
  dnorm(t[2], log(40), 1, TRUE)
set.seed(2026); t <- c(0, log(40))
ch <- numeric(5000); acc <- 0
for (i in 1:5000) {
  p <- t + rnorm(2, 0, 0.25)
  if (log(runif(1)) < lp(p) - lp(t)) {
    t <- p; acc <- acc + 1 }
  ch[i] <- exp(t[1]) }
k <- ch[-(1:500)]
round(c(acc = acc / 5000, k = mean(k),
  p_k1 = mean(k > 1)), 3)
