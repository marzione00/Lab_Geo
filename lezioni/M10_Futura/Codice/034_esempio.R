theta <- 0.6
c(rho1=theta/(1+theta^2),
  rho2=0)
ARMAacf(ma=theta, lag.max=5)
