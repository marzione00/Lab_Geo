# Variabilita' totale, entro e fra.
T67 <- sum(scale(Z,scale=FALSE)^2)
W67 <- km$tot.withinss
B67 <- sum(km$size *
             rowSums(km$centers^2))
c(T = T67, W = W67, B = B67)
stopifnot(abs(T67-W67-B67)<1e-8)
