x <- c(SiO2=46.7, Al2O3=13.4, CaO=10.4,
       MgO=8.2, FeO=13.4, Altro=6.0)
s <- x[1:5]; s <- 100*s/sum(s)
round(c(intera=unname(x[1]/x[3]),
        silicati=unname(s[1]/s[3])), 3)
