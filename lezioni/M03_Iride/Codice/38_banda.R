k15 <- density(diam, bw = .15,
  from = 2, to = 14, n = 256)
k40 <- density(diam, bw = .4,
  from = 2, to = 14, n = 256)
k12 <- density(diam, bw = 1.2,
  from = 2, to = 14, n = 256)
plot(k15, xlim = c(3,9),
     ylim = c(0,.65))
lines(k40, col = 2)
lines(k12, col = 4)
