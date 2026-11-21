# Popolazione finita costruita
U04 <- data.frame(
  id=1:12,
  valore=seq(2.1,3.2,by=.1))
set.seed(17)
i04 <- sample(U04$id, size=4)
U04[i04, ]        # un campione
mean(U04$valore)  # media nota qui
