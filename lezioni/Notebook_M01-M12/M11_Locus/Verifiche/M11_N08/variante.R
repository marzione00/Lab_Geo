A <- d$x_m<=1000;B <- d$x_m>=1000
data.frame(punti=nrow(d),appartenenze=sum(A)+sum(B),punti_doppi=sum(A&B))
stopifnot(sum(A&B)==8L)
