# Due provini: volumi in cm^3
v21 <- c(1, 9)
rho21 <- c(2, 4)  # Densita' g/cm^3
m21 <- rho21 * v21  # Masse in g
mean(rho21)                  # 3
sum(m21) / sum(v21)          # 3.8
weighted.mean(rho21, v21)    # 3.8
