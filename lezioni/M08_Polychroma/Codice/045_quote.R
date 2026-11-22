quota <- pc$sdev^2 / sum(pc$sdev^2)
data.frame(PC = 1:8,
  quota = quota, cumulata = cumsum(quota))
