passato13 <- stats::filter(z,
  rep(1/13, 13), sides = 1)
# Ogni valore usa presente e 12 mesi precedenti.
head(cbind(z, ma13, passato13), 15)
