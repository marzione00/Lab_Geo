ampiezza <- 1        # Ripetere con 0
x_lab <- 5 + ampiezza * (-2:2)
sd_lab <- sd(x_lab)
ok_lab <- sd_lab > 0
z_lab <- if (ok_lab) {
  as.vector(scale(x_lab))
} else {
  rep(NA_real_, length(x_lab))
}
c(sd = sd_lab, media_z = mean(z_lab))
