x_b <- c(1:8, 20)
bx <- boxplot.stats(x_b, coef = 1.5)
bx$stats                  # 1 3 5 7 8
bx$out                      # 20
boxplot(x_b, horizontal = TRUE,
        xlab = "Misura [mm]")
