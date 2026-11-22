# Manteniamo i gruppi appena trovati.
g62 <- max.col(-dist261,
              ties.method = "first")
cent62 <- rowsum(u59, g62) /
 as.vector(table(g62))
cent62
# Controllo prima e dopo le medie.
c(prima = sum((u59-
               cent61[g62, ])^2),
  dopo = sum((u59-
              cent62[g62, ])^2))
