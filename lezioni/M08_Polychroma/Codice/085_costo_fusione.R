# Due gruppi, una sola coordinata.
A85 <- c(0,2)
B85 <- c(5,7)
w85 <- function(x) sum((x-mean(x))^2)
delta85 <- w85(c(A85,B85))-
           w85(A85)-w85(B85)
f85 <- length(A85)*length(B85) /
 (length(A85)+length(B85)) *
 (mean(A85)-mean(B85))^2
c(incremento=delta85,formula=f85)
