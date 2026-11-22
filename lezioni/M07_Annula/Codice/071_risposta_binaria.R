# 1 indica Spiky, 0 indica Rounded.
f$spiky <- as.integer(
  f$morfotipo == "Spiky")
table(f$morfotipo, f$spiky)
stopifnot(all(f$spiky %in% c(0, 1)))
