# x0 = 1 mm: rapporto senza unita.
x0 <- 1
demo$log_pioggia <-
  log1p(demo$pioggia / x0)
s <- sd(demo$tmax)
stopifnot(s > 0)
demo$z_tmax <-
  (demo$tmax - mean(demo$tmax)) / s
