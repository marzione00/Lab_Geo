indice <- (NIR-R_band)/(NIR+R_band)
stopifnot(all(is.finite(indice)),
          all(abs(indice)<=1))
