# Molte prove, p piccolo: n*p=6
k38 <- 0:25
b38 <- dbinom(k38, 200, .03)
p38 <- dpois(k38, 6)
max(abs(b38-p38))
c(var_bin=200*.03*.97, var_pois=6)
