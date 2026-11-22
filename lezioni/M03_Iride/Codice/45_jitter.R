set.seed(303)
g_f <- fossili$morfotipo
pos <- as.integer(g_f)
pos <- pos +
  runif(length(pos), -.12, .12)
plot(pos, diam, xaxt = "n",
     xlim = c(.5,2.5), ylim = c(3,9),
     xlab = "Morfotipo",
     ylab = "Diametro [um]")
axis(1, at = 1:2,
     labels = levels(g_f))
