# Valori fissi, etichette mobili
x12 <- c(1, 2, 4, 7)
g12 <- c("A","A","B","B")
set.seed(17)
gp12 <- sample(g12)
data.frame(valore=x12,
 originale=g12, permutato=gp12)
table(gp12) # 2 per gruppo
