# Soglia con il 95% a sinistra
q46 <- qnorm(.95, mean=10, sd=2)
q46  # 13.28971
qnorm(.95)  # 1.644854
pnorm(q46, mean=10, sd=2)
