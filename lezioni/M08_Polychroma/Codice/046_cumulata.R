barplot(100 * quota, names.arg = 1:8,
  xlab = "Componente",
  ylab = "Varianza (%)")
cumsum(quota)
