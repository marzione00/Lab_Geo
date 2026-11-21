# Esempio con un pareggio: valore 3
a54 <- c(1,3,5); b54 <- c(2,3,6)
M54 <- outer(b54,a54,">")+
       .5*outer(b54,a54,"==")
M54  # Righe B, colonne A
c(U=sum(M54),theta=mean(M54))
