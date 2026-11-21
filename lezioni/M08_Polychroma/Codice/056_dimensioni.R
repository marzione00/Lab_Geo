# Perdita relativa per q = 1,...,8.
data.frame(q = 1:8,
  conservata = cumsum(quota),
  persa = 1 - cumsum(quota))
