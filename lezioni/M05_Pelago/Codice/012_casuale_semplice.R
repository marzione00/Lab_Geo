# Tutti i campioni di 2 fra 6 unita
u12 <- c(2,4,5,7,8,10)
ind12 <- combn(seq_along(u12),2)
medie12 <- apply(ind12,2,
  function(i) mean(u12[i]))
length(medie12)       # 15 campioni
c(pop=mean(u12),
  attesa=mean(medie12))
