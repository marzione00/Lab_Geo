x <- c(SiO2=85.1, Al2O3=6.2, CaO=2.0,
       MgO=0, FeO=1.1, Altro=5.6)
dl <- 0.1; z <- x == 0
y <- x; y[z] <- 0.65*dl
y[!z] <- x[!z]*(100-sum(y[z]))/sum(x[!z])
round(c(somma=sum(y),
  prima=unname(x[1]/x[2]),
  dopo=unname(y[1]/y[2])), 4)
