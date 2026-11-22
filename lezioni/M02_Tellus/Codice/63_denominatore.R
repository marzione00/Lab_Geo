comp2 <- comp
comp2["A"] <- 80
chiusa2 <- 100 * comp2 / sum(comp2)
# Confronto di scenari deterministici
rbind(prima = chiusa,
      dopo = chiusa2)
chiusa2["B"] / chiusa2["C"]  # 1.4
