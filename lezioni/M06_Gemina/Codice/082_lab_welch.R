# Rapporto fra SD: 2 -> 1
z82 <- lab_welch(ratio=2)
w82 <- lab_welch(ratio=1)
rbind(sd2=z82$metrics,
      sd1=w82$metrics)
z82$test$conf.int
w82$test$conf.int
