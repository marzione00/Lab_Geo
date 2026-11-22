parti <- c("SiO2", "CaO", "MgO",
           "FeO", "resto_wt")
comp <- as.matrix(d[parti])
range(rowSums(comp))
max(abs(rowSums(comp) - 100))
