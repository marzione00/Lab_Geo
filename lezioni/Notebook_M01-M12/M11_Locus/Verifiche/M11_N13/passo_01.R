d <- carica_dati("spazio_v3.csv")
audit_spazio(d)
 ps <- pesi_spaziali(d,260);A <- ps$A;W <- ps$W
 v <- d$concentrazione-mean(d$concentrazione);n <- length(v)
 I_A <- n/sum(A)*sum(A*outer(v,v))/sum(v^2)
 controllo <- as.numeric(n/sum(A)*crossprod(v,A%*%v)/crossprod(v))
 data.frame(matrice="A binaria",Moran_I=I_A,n=n,S0=sum(A),prodotto_quadratico=controllo)
 stopifnot(abs(I_A-controllo)<1e-12,abs(I_A-moran_I(d$concentrazione,A))<1e-12)
