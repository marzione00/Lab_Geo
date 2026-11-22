gr_f <- split(diam, g_f)
F_R <- ecdf(gr_f[["Rounded"]])
F_S <- ecdf(gr_f[["Spiky"]])
plot(F_R, xlim = c(3,9),
     verticals = TRUE, col = 4,
     xlab = "Diametro [um]")
plot(F_S, add = TRUE,
     verticals = TRUE, col = 2)
