# Confronto teorico
n19 <- c(60,300)
data.frame(
 n=n19,
 se=2/sqrt(n19),
 bias=rep(-1,2),
 mse=4/n19+1)
