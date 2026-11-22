D58 <- c(1,-2,3,-4) # Esempio
z58 <- D58[D58!=0]  # Escludere zeri
r58 <- rank(abs(z58))
sum(r58[z58>0])     # W+ = 4
wilcox.test(D58,mu=0,
            exact=FALSE,correct=TRUE)
# Ipotesi: simmetria attorno a zero
