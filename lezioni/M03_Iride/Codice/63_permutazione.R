# Trasporre cambia solo la posizione
s_z2 <- as.vector(t(s_mat))
all(sort(s_z2)==sort(s_rete$valore))
rbind(A=table(s_rete$valore),
      B=table(s_z2))
