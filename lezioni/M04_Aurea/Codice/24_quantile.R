# Uniforme [0,2]: F(q)=.75
qunif(.75, min=0, max=2)  # 1.5
# Caso discreto delle pagine 18-23
k24 <- 0:2
F24 <- cumsum(c(.49,.42,.09))
k24[which(F24 >= .75)[1]] # 1
# F(1)=.91: il salto supera .75
