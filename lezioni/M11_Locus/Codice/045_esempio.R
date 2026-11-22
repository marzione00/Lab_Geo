A <- 1*(D>0 & D<=260)
stopifnot(all(diag(A)==0),
          identical(A,t(A)))
c(archi=sum(A)/2,S0=sum(A))
