# X lognormale: formula esatta
s53 <- c(.1, .3, .6)
cv53 <- sqrt(expm1(s53^2))
data.frame(sdlog = s53, CV = cv53,
           percento = 100*cv53)
