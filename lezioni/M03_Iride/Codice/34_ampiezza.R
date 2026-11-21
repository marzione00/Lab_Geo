h05 <- hist(diam, plot = FALSE,
            breaks = seq(2,14,by=.5))
h10 <- hist(diam, plot = FALSE,
            breaks = seq(2,14,by=1))
plot(h10, xlim = c(2,10),
     ylim = c(0,70), border = 2)
plot(h05, add = TRUE, border = 4)
