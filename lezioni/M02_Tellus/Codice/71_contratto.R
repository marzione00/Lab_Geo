densita_controllata <- function(m,v) {
  stopifnot(is.numeric(m),
    is.numeric(v), length(m)>0,
    length(m)==length(v))
  stopifnot(all(is.finite(m)),
    all(is.finite(v)))
  stopifnot(all(m>0), all(v>0))
  m / v
}
