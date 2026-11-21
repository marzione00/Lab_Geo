x13 <- c(1, 2, 4, 7)
# Scegliere 2 dei 4 indici per A.
i13 <- combn(4, 2)
t13 <- apply(i13, 2, function(i) {
  mean(x13[-i])-mean(x13[i])
})
t13
mean(abs(t13) >= 4) # 2/6 esatto
