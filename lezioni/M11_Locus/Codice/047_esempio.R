grado <- rowSums(A)
table(grado)
stopifnot(sum(grado)==224,
          sum(A)/2==112)
