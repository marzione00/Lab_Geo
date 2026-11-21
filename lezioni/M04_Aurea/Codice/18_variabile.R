# Due prove indipendenti, p=.3
esiti18 <- c("00","01","10","11")
x18 <- c(0, 1, 1, 2)  # successi
p18 <- c(.49, .21, .21, .09)
# Somma i pesi per lo stesso X
tapply(p18, x18, sum)
