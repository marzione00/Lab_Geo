n89 <- 120
rho89 <- .7
h89 <- 1:(n89-1)
v89 <- (n89 + 2*sum(
  (n89-h89)*rho89^h89))/n89^2
sqrt(v89)      # SE teorico: .215
1/sqrt(n89)    # Ipotesi iid: .091
