# Stesso seme: stesso rumore
s0 <- lab_mappa(gradient=0,seed=17)
s4 <- lab_mappa(gradient=4,seed=17)
rbind(A=s4$indicatori,
      B=s0$indicatori)
range(s4$dati$x)            # 1, 20
