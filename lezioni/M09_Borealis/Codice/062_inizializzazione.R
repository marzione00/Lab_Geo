# Il CSV fornito parte da un valore fissato.
head(proc[, c("passo", "ar1")])
stopifnot(proc$ar1[1] == 0)
h62 <- 0:10
v62 <- (1 - 0.65^(2 * h62)) /
       (1 - 0.65^2)
data.frame(passi = h62, varianza = v62)
