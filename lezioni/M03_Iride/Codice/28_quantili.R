# Esempio ordinato, in mm
x_q <- c(1, 2, 4, 7, 8, 9, 10, 12)
quantile(x_q, c(.25, .5, .75),
         type = 7)
# Primo quartile interpolato
.25 * 2 + .75 * 4           # 3.5
