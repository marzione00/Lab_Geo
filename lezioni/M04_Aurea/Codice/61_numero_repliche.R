# Obiettivo: SE_MC <= 0.01
eps61 <- .01; p61 <- .1
B61 <- ceiling((p61/eps61) *
               ((1-p61)/eps61))
Bmax61 <- ceiling(1/(4*eps61^2))
c(con_p_noto = B61,
  limite_generale = Bmax61)
