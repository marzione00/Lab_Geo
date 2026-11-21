# Un prelievo uniforme fra 6 provini
m05 <- c(104,106,108,110,112,114)
tipo05 <- c("F","M","F","M","F","M")
A05 <- m05 >= 110   # massa in g
B05 <- tipo05 == "M"
mean(A05)           # P(A) = 3/6
which(A05)          # provini 4,5,6
