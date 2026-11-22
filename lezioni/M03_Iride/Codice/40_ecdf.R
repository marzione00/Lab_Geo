x_e <- c(4.1,4.8,5.2,5.2,6.4)
F_e <- ecdf(x_e)
F_e(5.2)                    # 0.8
plot(F_e, verticals = TRUE,
     xlab = "Misura [mm]",
     ylab = "Quota cumulata")
