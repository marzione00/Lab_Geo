# Stessi dati e grado, due intorni.
demo$giorno <- seq_len(nrow(demo))
f1 <- loess(tmax ~ giorno, demo,
            span = .1, degree = 1)
f3 <- loess(tmax ~ giorno, demo,
            span = .3, degree = 1)
curve <- cbind(predict(f1),
               predict(f3))
matplot(curve, type = "l", lty = 1,
  xlab = "Giorno", ylab = "Tmax [C]")
