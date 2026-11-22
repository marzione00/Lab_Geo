v_b <- 1:8
quantile(v_b, c(.25,.5,.75),
         type = 7)
# Cerniere e mediana di R base
boxplot.stats(v_b)$stats[2:4]
