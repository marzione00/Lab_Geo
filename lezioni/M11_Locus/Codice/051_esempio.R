lag_z <- drop(W%*%z)
stopifnot(max(abs(W%*%rep(1,n)-1))
          <1e-12)
head(data.frame(id=d$id,z,lag_z))
