# Mostrare insieme dati e sintesi.
media31 <- stats::filter(demo$tmax,
  rep(1/31, 31), sides = 2)
plot(demo$data, demo$tmax, type = "l",
     col = "grey75", xlab = "Data",
     ylab = "Tmax [C]")
lines(demo$data, as.numeric(media31),
      col = "steelblue", lwd = 2)
etichette <- c("Dati", "Media 31 g")
legend("topleft", etichette,
       col = c("grey75", "steelblue"),
       lty = 1, bty = "n")
