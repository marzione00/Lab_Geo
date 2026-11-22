# Due code del 2.5% ciascuna
i47 <- qnorm(c(.025,.975), 10, 2)
i47  # 6.080072, 13.919928
diff(pnorm(i47, mean=10, sd=2))
# Quantile unilaterale: altra soglia
qnorm(.95, mean=10, sd=2)
