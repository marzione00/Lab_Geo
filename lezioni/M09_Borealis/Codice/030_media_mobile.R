ma3 <- stats::filter(z, rep(1/3, 3),
                     sides = 2)
ma13 <- stats::filter(z, rep(1/13, 13),
                      sides = 2)
plot(z, col = "grey60")
lines(ma3, col = "#C57E42")
lines(ma13, col = "#7363AA", lwd = 2)
