# m_c e' centrato a 7 um.
j64 <- match("morfotipoSpiky",
             names(coef(m_c)))
d64 <- coef(m_c)[j64]
se64 <- sqrt(vcov(m_c)[j64, j64])
t64 <- qt(0.975, df.residual(m_c))
c(stima = d64,
  basso = d64 - t64*se64,
  alto = d64 + t64*se64)
