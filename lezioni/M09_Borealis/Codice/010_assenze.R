cal_es <- data.frame(
  data = seq(as.Date("2001-01-01"),
             by = "month", length.out = 8),
  valore = c(5, 7, 6, NA, 9, 7, 6, 4))
cal_es[is.na(cal_es$valore), ]
# Il NA mantiene la posizione di aprile.
