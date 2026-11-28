e <- read.csv('dati/eruzioni_v1.csv')
r <- diff(e$anno); s <- 2025 - max(e$anno)
ll <- function(t) sum(dweibull(r,
  exp(t[1]), exp(t[2]), log = TRUE)) +
  pweibull(s, exp(t[1]), exp(t[2]),
    lower.tail = FALSE, log.p = TRUE)
o <- optim(c(0, log(40)),
  function(t) -ll(t))
round(c(k = exp(o$par[1]),
  scala = exp(o$par[2])), 2)
round(c(media = mean(r),
  cv = sd(r) / mean(r)), 2)
