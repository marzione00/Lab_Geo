# Due stazioni illustrative
n80 <- c(2, 8)
medie80 <- c(2.4, 2.8)  # g/cm^3
mean(medie80)           # 2.60
weighted.mean(medie80, n80) # 2.72
# L'aggregazione definisce i pesi.
