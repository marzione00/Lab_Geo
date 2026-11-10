esterno <- c(8,5,NA,7)
interno <- c(6,6,4,5)
disponibile <- is.finite(esterno) & is.finite(interno)
valido <- disponibile & esterno>0 &
          interno>=0 & interno<=esterno
valido[is.na(valido)] <- FALSE
data.frame(esterno,interno,disponibile,valido)
