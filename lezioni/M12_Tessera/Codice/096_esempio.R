d30 <- as.vector(Z[,2:30]-Z[,1:29])
d300 <- as.vector(Z[,11:30]-Z[,1:20])
stopifnot(length(d30)==696,
          length(d300)==480)
c(mean(abs(d30)),mean(abs(d300)))
