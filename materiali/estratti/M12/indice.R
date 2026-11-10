R <- c(.2,0,1e-10,.3)
N <- c(.4,0,2e-10,.2)
den <- N+R
ok <- den > 1e-6
I <- rep(NA_real_,length(den))
I[ok] <- (N[ok]-R[ok])/den[ok]
stopifnot(sum(is.na(I))==2)
data.frame(R,N,den,ok,I)
