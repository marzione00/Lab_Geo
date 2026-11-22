# Confronto, senza modificare f.
j52 <- which.max(cooks.distance(m0))
m_sens <- update(m0, data = f[-j52, ])
rbind(completo = coef(m0),
      senza_caso = coef(m_sens))
# Conserviamo l'identita' del caso.
f[j52, ]
