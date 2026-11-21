x70 <- c(10, 13, 12, 16)
diff(x70)
# Il secondo incremento e' negativo.
stopifnot(identical(diff(x70),
                    c(3, -1, 4)))
