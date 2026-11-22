stopifnot(all(grado>0))
W <- A/grado
stopifnot(max(abs(rowSums(W)-1))
          <1e-12)
