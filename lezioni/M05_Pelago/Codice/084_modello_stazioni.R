G84 <- 12
m84 <- 6
tau84 <- 2     # SD fra stazioni
rho84 <- tau84^2/(tau84^2+1)
se84 <- sqrt(tau84^2/G84 +
             1/(G84*m84))
c(rho_intra = rho84, SE = se84)
