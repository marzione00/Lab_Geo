prior13 <- .4
pa13 <- .8; pb13 <- .2
pA13 <- pa13*prior13 +
  pb13*(1-prior13)
post13 <- pa13*prior13 / pA13
c(P_A = pA13, P_B_dato_A = post13)
# .44 e circa .72727
