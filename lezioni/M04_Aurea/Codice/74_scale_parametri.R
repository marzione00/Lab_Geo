s74 <- .3; cl74 <- .7
CV74 <- sqrt(expm1(s74^2))
c74 <- expm1(cl74*s74^2) /
       expm1(s74^2)
c(SD_log = s74, CV_originale = CV74,
  cor_log = cl74, cor_originale = c74)
