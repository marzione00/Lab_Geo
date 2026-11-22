# Dati della slide 24
d_sc <- x_disp - mean(x_disp)
somma_q <- sum(d_sc^2)
s2 <- somma_q / (length(x_disp)-1)
c(formula = s2, R = var(x_disp))
sqrt(s2)
sd(x_disp)                  # 1 mm
