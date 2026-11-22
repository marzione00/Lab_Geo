x17 <- c(2, 4, 6)
scarti2 <- function(a) {
  sum((x17 - a)^2)
}
sapply(c(3, 4, 5), scarti2)
# 11, 8, 11: minimo in a = 4
