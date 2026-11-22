t22 <- 2
nu22 <- 20
# Alternativa: Delta > 0, scelta prima
pt(t22, nu22, lower.tail = FALSE)
# Alternativa: Delta diverso da zero
2 * pt(-abs(t22), nu22)
