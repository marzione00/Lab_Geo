# Bersaglio comune theta=10
v20 <- c(casuale=4/60,
         selettiva=4/300)
b20 <- c(casuale=0,selettiva=-1)
data.frame(se=sqrt(v20),
 bias=b20,mse=v20+b20^2)
