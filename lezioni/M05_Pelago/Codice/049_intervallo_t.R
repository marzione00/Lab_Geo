# Esempio costruito, n = 6
x49 <- c(4.2, 5.1, 5.4, 6, 6.3, 7)
n49 <- length(x49)
se49 <- sd(x49)/sqrt(n49)
q49 <- qt(.975, n49-1)
mean(x49) + c(-1,1)*q49*se49
