# Esempio costruito
x58 <- c(4.1,4.7,5,5.2,5.4,5.6,5.8,6)
z58 <- x58
z58[8] <- 12  # Un valore cambiato
rbind(prima = c(mean(x58), sd(x58)),
      dopo = c(mean(z58), sd(z58)))
rbind(t.test(x58)$conf.int,
      t.test(z58)$conf.int)
