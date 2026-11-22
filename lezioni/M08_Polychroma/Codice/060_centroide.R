# Tre osservazioni di un gruppo.
A60 <- rbind(c(0,0), c(2,0),
             c(1,3))
mu60 <- colMeans(A60)
mu60  # Il centroide e' (1, 1).
w60 <- function(candidato) {
 sum(sweep(A60, 2, candidato)^2)
}
c(centroide = w60(mu60),
  alternativa = w60(c(1,2)))
