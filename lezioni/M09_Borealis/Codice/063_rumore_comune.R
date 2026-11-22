set.seed(19063)
e63 <- rnorm(150)
ar63 <- function(phi) {
  x <- numeric(length(e63))
  for (t in 2:length(x))
    x[t] <- phi * x[t-1] + e63[t]
  x
}
# Le due traiettorie usano lo stesso e63.
matplot(cbind(ar63(0.3), ar63(0.9)),
        type = "l", ylab = "Valore")
