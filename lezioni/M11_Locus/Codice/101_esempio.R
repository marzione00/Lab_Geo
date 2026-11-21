s <- c(0,500,1000); s0 <- 250
C <- 4*exp(-(outer(s,s,"-")/800)^2)
c0 <- 4*exp(-((s-s0)/800)^2)
K <- rbind(cbind(C,1),c(1,1,1,0))
sol <- solve(K,c(c0,1))
stopifnot(abs(sum(sol[1:3])-1)<1e-12)
