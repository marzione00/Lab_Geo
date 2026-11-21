# b66 contiene 2000 medie bootstrap
sd(b66)      # SE bootstrap: circa .783
# Errore MC della media delle repliche
sd(b66)/sqrt(length(b66))  # .0175
# Dispersione delle quattro misure
sd(x66)      # Circa 1.826
