alpha33 <- 0.05
pot33 <- 0.80
sigma33 <- 1
delta33 <- 0.5
n33 <- 2 * sigma33^2 *
  (qnorm(1 - alpha33 / 2) +
   qnorm(pot33))^2 / delta33^2
ceiling(n33)  # 63 per gruppo
