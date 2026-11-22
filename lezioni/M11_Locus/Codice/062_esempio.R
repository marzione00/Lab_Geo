stopifnot(abs(moran_I(100+2*z,A)-
              moran_I(z,A))<1e-12)
stopifnot(abs(moran_I(-z,A)-
              moran_I(z,A))<1e-12)
