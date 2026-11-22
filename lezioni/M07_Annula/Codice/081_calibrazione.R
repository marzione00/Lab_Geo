# Intervalli fissi di probabilita'.
d81 <- data.frame(
  bin = cut(p_log, breaks = seq(0, 1, 0.2),
            include.lowest = TRUE),
  p = p_log, y = f$spiky)
aggregate(cbind(p, y) ~ bin,
          data = d81, FUN = mean)
table(d81$bin)
