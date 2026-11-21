# Medie teoriche A=3, B=7, C=10
n_A <- c(10, 20, 50, 100)
attesa_m <- (3*n_A + 170)/(n_A + 20)
attesa_s <- rep(20/3, length(n_A))

data.frame(n_A, attesa_m, attesa_s)
# Misure: 6.67, 5.75, 4.57, 3.92
# Stazioni: sempre 6.67 (circa)
