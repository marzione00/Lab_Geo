z <- read.csv('dati/date_v1.csv')
mp <- function(t, s) {
  w <- 1 / s^2; m <- sum(w * t) / sum(w)
  c(media = m, se = sqrt(1 / sum(w)),
    mswd = sum(w * (t - m)^2) /
      (length(t) - 1))
}
round(rbind(
  tutti = mp(z$data_Ma, z$s_Ma),
  senza_Z15 = mp(z$data_Ma[-15],
    z$s_Ma[-15])), 3)
