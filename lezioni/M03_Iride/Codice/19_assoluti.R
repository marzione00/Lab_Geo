x19 <- c(2, 4, 6)
scarti1 <- function(a) {
  sum(abs(x19 - a))
}
sapply(c(3, 4, 5), scarti1)
# 5, 4, 5: minimo in a = 4
