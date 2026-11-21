x64 <- c(4, 5, 7, 8)
# Tutte le 4^4 sequenze ordinate
j64 <- as.matrix(expand.grid(
  rep(list(1:4), 4)))
m64 <- apply(j64, 1,
  function(j) mean(x64[j]))
length(m64)               # 256
mean(m64)                 # 6
mean((m64-mean(m64))^2)    # .625
