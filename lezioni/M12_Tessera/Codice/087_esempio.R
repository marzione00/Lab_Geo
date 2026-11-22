okI <- is.finite(R_band) &
 is.finite(NIR) & (R_band+NIR>1e-6)
Ival <- rep(NA_real_,length(NIR))
Ival[okI] <- (NIR[okI]-R_band[okI])/
              (NIR[okI]+R_band[okI])
