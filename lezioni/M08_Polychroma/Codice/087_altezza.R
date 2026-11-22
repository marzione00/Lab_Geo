# Prima fusione: due campioni.
f87 <- -h$merge[1, ]
delta87 <- sum((Z[f87[1], ]-
                Z[f87[2], ])^2)/2
c(deltaW=delta87,
  altezza2_su_2=h$height[1]^2/2)
stopifnot(abs(delta87-
             h$height[1]^2/2)<1e-8)
