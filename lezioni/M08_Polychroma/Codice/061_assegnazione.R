# Centri provvisori dello schema.
cent61 <- rbind(c(1,1), c(6,3))
dist261 <- sapply(1:2, function(g) {
 rowSums(sweep(u59, 2,
               cent61[g, ])^2)
})
# Righe: punti. Colonne: centri.
round(dist261, 2)
max.col(-dist261,
        ties.method = "first")
