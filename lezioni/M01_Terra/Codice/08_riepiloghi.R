# Usa la tabella della slide 6
mean(misure$valore)  # 4.4
# Una media per ciascuna stazione
tapply(misure$valore,
       misure$stazione, mean)
# A: 3.05; B: 7.10
