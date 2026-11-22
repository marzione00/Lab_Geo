d50 <- read.csv(
  "Dati/misure_appaiate_simulate.csv")
a50 <- d50$prima; b50 <- d50$dopo
v50 <- var(b50)+var(a50)-
       2*cov(b50,a50)
stopifnot(isTRUE(all.equal(
  v50,var(b50-a50))))
c(var_D=v50,cor=cor(a50,b50))
