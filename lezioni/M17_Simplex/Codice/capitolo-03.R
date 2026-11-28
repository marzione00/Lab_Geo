x <- c(SiO2=46.7, Al2O3=13.4, CaO=10.4,
       MgO=8.2, FeO=13.4, Altro=6.0)
alr <- log(x[1:5]/x[6])
clr <- log(x) - mean(log(x))
round(rbind(alr=c(alr,Altro=0),
            clr=clr), 3)
round(sum(clr), 12)
