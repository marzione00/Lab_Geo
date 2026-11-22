R0 <- c(.2,0,1e-10,.3)
N0 <- c(.4,0,2e-10,.2)
ok0 <- N0+R0>1e-6
Itoy <- rep(NA_real_,4)
Itoy[ok0] <- (N0[ok0]-R0[ok0])/
              (N0[ok0]+R0[ok0])
