x14 <- c(1, 2, 4, 7)
g14 <- c("A","A","B","B")
# Una riassegnazione ammessa
gp14 <- g14[c(1, 4, 2, 3)]
diff(tapply(x14, g14, mean))  # 4
diff(tapply(x14, gp14, mean)) # 2
# Per un riordino casuale:
sample(g14)
