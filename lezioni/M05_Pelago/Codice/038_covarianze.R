# Quattro osservazioni, varianza 1
S38 <- matrix(.2, 4, 4)
diag(S38) <- 1
w38 <- rep(1/4, 4)
# Varianza della loro media
drop(t(w38) %*% S38 %*% w38)
sum(S38) / 4^2
