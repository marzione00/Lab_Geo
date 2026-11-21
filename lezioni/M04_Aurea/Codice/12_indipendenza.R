# Esempio indipendente
pA12 <- .4; pB12 <- .5
pAB12 <- .2
pAB12 / pB12       # .4 = P(A)
isTRUE(all.equal(pAB12, pA12*pB12))
# Incompatibili: P(A e B)=0
0 == pA12*pB12     # FALSE
