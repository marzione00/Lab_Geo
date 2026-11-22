xc44 <- x43 - mean(x43)
rho44 <- sum(head(xc44, -1) *
               tail(xc44, -1)) / sum(xc44^2)
rho_R <- as.numeric(acf(x43, plot = FALSE)$acf[2])
stopifnot(abs(rho44 - rho_R) < 1e-12)
rho44 # 0.4
