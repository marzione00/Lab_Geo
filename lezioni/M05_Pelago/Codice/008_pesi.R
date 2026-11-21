# Medie costruite di tre stazioni
m08 <- c(A=5,B=6,C=12)
w08 <- c(A=.2,B=.3,C=.5)
sum(w08)           # somma: 1
sum(w08*m08)       # media pesata
weighted.mean(m08,w08)
# Ogni stazione conta 1/3.
mean(m08)
