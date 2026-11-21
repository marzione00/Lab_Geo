x63 <- c(4, 5, 7, 8)
j63 <- c(3, 3, 1, 4)
N63 <- tabulate(j63, nbins = 4)
N63              # 1, 0, 2, 1
sum(N63)         # 4 estrazioni
sum(N63*x63)/4   # Media: 6.5
mean(x63[j63])   # Stesso valore
