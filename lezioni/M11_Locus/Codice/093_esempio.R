w0 <- idw_weights(xy,c(900,900),p=2)
stopifnot(all(w0>=0),
          abs(sum(w0)-1)<1e-12)
c(stima=sum(w0*z),min=min(z),max=max(z))
