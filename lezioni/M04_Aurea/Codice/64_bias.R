# V fissato; scostamento di 2 g noto
set.seed(17)
m64 <- rnorm(20000, 108, 1)
d64 <- m64/40
dc64 <- (m64-2)/40
c(senza_correzione = mean(d64),
  con_correzione = mean(dc64))
