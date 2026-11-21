n_geo <- nrow(geometria)
n_chiavi <- length(
  unique(geometria$id))
stopifnot(!anyNA(geometria$id),
          all(nzchar(geometria$id)),
          n_chiavi == n_geo)
c(righe = n_geo, chiavi = n_chiavi)
