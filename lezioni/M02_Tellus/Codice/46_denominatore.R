x_na <- c(4, NA, 6)
n_oss <- sum(!is.na(x_na))
media_oss <- if (n_oss > 0)
  mean(x_na, na.rm = TRUE) else NA
c(totali = length(x_na),
  disponibili = n_oss,
  media = media_oss)
