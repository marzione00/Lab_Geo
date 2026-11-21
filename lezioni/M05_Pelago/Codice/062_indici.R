x62 <- c(4, 5, 7, 8)
# Replica scelta per il diagramma
j62 <- c(3, 3, 1, 4)
x62[j62]        # 7, 7, 4, 8
mean(x62[j62])  # 6.5
# Una replica estratta casualmente
set.seed(17)
sample.int(4, 4, replace = TRUE)
