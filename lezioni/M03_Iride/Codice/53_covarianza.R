# Scarti dalle rispettive medie
r_dx <- r_x - mean(r_x)
r_dy <- r_y - mean(r_y)
r_n <- length(r_x)
r_cov <- sum(r_dx * r_dy) /
  (r_n - 1)
c(manuale = r_cov, R = cov(r_x,r_y))
