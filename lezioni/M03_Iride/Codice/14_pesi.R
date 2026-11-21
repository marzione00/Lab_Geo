# Medie e numerosita' di due gruppi
m14 <- c(2, 8)
n14 <- c(2, 8)
mean(m14)                 # 5
weighted.mean(m14, n14)   # 6.8
sum(n14 * m14) / sum(n14)
