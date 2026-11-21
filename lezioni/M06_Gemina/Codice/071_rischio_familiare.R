# Nulle vere; test indipendenti
m71 <- c(1,6,10,20,50)
a71 <- .05
risk71 <- 1-(1-a71)^m71
cbind(test=m71,FWER=risk71)
